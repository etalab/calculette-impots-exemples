import json

import numpy as np

from .function_set_numpy import get_functions_mapping
from ..loader import load_json


class VectorComputationEngine(object):
    def __init__(self, millesime, n):
        self.millesime = millesime
        self.n = n

        self.computing_order, self.children_light, self.formulas_light, self.constants_light, self.inputs_light, self.unknowns_light, self.input_variables = load_json(millesime)

        self.alias2name = {i['alias']: i['name'] for i in self.input_variables}

        self.functions_mapping = get_functions_mapping(n)

    def compute(self, alias_values, formula_names):

        def get_value(name, input_values, computed_values):
            if name in self.formulas_light:
                return computed_values[name]

            if name in self.constants_light:
                return self.constants_light[name]*np.ones(self.n)

            if name in self.inputs_light:
                return input_values[name]

            if name in self.unknowns_light:
                return np.zeros(self.n)

            raise Exception('Unknown variable category.')

        def compute_formula(node, input_values, computed_values):
            nodetype = node['nodetype']

            if nodetype == 'symbol':
                name = node['name']
                value = get_value(name, input_values, computed_values)
                return value

            if nodetype == 'float':
                value = node['value']
                return value*np.ones(self.n)

            if nodetype == 'call':
                name = node['name']
                args = [
                    compute_formula(child, input_values, computed_values) 
                    for child in node['args']
                ]
                function = self.functions_mapping[name]
                value = function(args)
                return value

            raise ValueError('Unknown type : %s'%nodetype)

        def prepare(alias_values):
            input_values = {}
            for alias, value in alias_values.items():
                if alias in self.alias2name:
                    name = self.alias2name[alias]
                else:
                    name = alias
                input_values[name] = value

            input_values_complete = {}
            for name in self.inputs_light:
                if (name in input_values):
                    input_values_complete[name] = input_values[name]
                else:
                    input_values_complete[name] = np.zeros(self.n)

            return input_values_complete

        input_values = prepare(alias_values)

        computed_values = {}
        for variable in self.computing_order:
            formula = self.formulas_light[variable]
            computed_values[variable] = compute_formula(formula, input_values, computed_values)

        return {var: computed_values[var] for var in formula_names}


















