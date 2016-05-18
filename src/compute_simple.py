"""
Compare with http://www3.finances.gouv.fr/calcul_impot/2015/index.htm

"""

import json
import numpy as np
import os

import function_set_np

n = 10
functions_mapping = function_set_np.get_functions_mapping(n)


with open('../json/computing_order_simple.json', 'r') as f:
    computing_order = json.load(f)

with open('../json/formulas_simple.json', 'r') as f:
    formulas_simple = json.load(f)

with open('../json/inputs_simple.json', 'r') as f:
    inputs_simple = json.load(f)

with open('../json/input_variables.json', 'r') as f:
    input_variables = json.load(f)


alias2name = {i['alias']: i['name'] for i in input_variables}



def prepare(alias_values):
    input_values = {alias2name[alias]: value for alias, value in alias_values.items()}

    input_values_complete = {}
    for name in inputs_simple:
        if (name in input_values):
            input_values_complete[name] = input_values[name]
        else:
            input_values_complete[name] = 0.

    return input_values_complete


def compute_formula(node, input_values, computed_values):
    nodetype = node['nodetype']

    if nodetype == 'symbol':
        name = node['name']
        if name in formulas_simple:
            return computed_values[name]*np.ones(n)

        if name in inputs_simple:
            return input_values[name]*np.ones(n)

        raise Exception('Unknown variable category.')

    if nodetype == 'float':
        value = node['value']
        return value*np.ones(n)

    if nodetype == 'call':
        name = node['name']
        args = [compute_formula(child, input_values, computed_values) for child in node['args']]
        function = functions_mapping[name]
        value = function(args)
        return value

    raise ValueError('Unknown type : %s'%nodetype)


def compute(input_values):
    computed_values = {}

    for variable in computing_order:
        formula = formulas_simple[variable]
        computed_values[variable] = compute_formula(formula, input_values, computed_values)

    return computed_values['IRN']
