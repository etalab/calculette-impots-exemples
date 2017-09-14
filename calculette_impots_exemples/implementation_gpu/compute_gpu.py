import json

import numpy as np
import tensorflow as tf

from .function_set_gpu import get_functions_mapping
from ..loader import load_json


class GPUComputationEngine(object):
    def __init__(self, millesime, n_batch):
        self.millesime = millesime
        self.n_batch = n_batch

        self.computing_order, self.children_light, self.formulas_light, self.constants_light, self.inputs_light, self.unknowns_light, self.input_variables = load_json(millesime)

        self.alias2name = {i['alias']: i['name'] for i in self.input_variables}

        self.functions_mapping, self.tf_constant_zero, self.tf_constant_one, self.tf_constant_false, self.tf_constant_true = get_functions_mapping(n_batch)

        # Index and reverse index for formulas, constants and input variables

        self.n_formulas = len(self.computing_order)
        self.reverse_index_formulas = self.computing_order
        self.index_formulas = {
            v: i
            for i, v in enumerate(self.reverse_index_formulas)
        }

        self.n_inputs = len(self.inputs_light)
        self.reverse_index_inputs = self.inputs_light
        self.index_inputs = {
            v: i
            for i, v in enumerate(self.reverse_index_inputs)
        }

        self.tf_inputs = tf.placeholder(tf.float64, shape=(self.n_batch, self.n_inputs))

        def build_graph(node):
            if node['nodetype'] == 'float':
                scalar_constant = tf.constant(node['value'], dtype=tf.float64)
                vector_constant = tf.multiply(self.tf_constant_one, scalar_constant)
                return vector_constant
            
            if node['nodetype'] == 'symbol':
                name = node['name']
                if name in self.formulas_light:
                    return self.tf_formulas[name]

                if name in self.constants_light:
                    value = self.constants_light[name]
                    return build_graph({'nodetype': 'float', 'value': value})

                if name in self.inputs_light:
                    index = self.index_inputs[name]
                    begin = [0, index]
                    size = [self.n_batch, 1]
                    tmp = tf.slice(self.tf_inputs, begin, size)
                    return tf.reshape(tmp, [self.n_batch])

                if name in self.unknowns_light:
                    return self.tf_constant_zero

                raise Exception('Unknown variable category.')

            if node['nodetype'] == 'call':
                name = node['name']
                args = [build_graph(child) for child in node['args']]
                function = self.functions_mapping[name]
                value = function(args)
                return value

            raise ValueError('Unknown type : %s'%nodetype)

        self.tf_formulas = {}
        for var in self.computing_order:
            self.tf_formulas[var] = build_graph(self.formulas_light[var])


    def compute(self, alias_values, formula_name):

        def prepare(alias_values):
            input_values = np.zeros((self.n_batch, self.n_inputs))

            for alias, values in alias_values.items():
                if alias in self.alias2name:
                    name = self.alias2name[alias]
                else:
                    name = alias

                index = self.index_inputs[name]
                input_values[:, index] = values

            return input_values

        input_values = prepare(alias_values)

        # Make the computation
        with tf.Session() as sess:
            result = sess.run(self.tf_formulas[formula_name], feed_dict={self.tf_inputs: input_values})

        return result
