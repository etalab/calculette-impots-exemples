"""
Compare with http://www3.finances.gouv.fr/calcul_impot/2015/index.htm

"""

import json
import configparser
import numpy as np
import os

from function_set_np import functions_mapping

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) + '/config.ini')
n = int(config['numpy']['n'])

with open('../json/computing_order.json', 'r') as f:
    computing_order = json.load(f)

with open('../json/children_light.json', 'r') as f:
    children_light = json.load(f)

with open('../json/formulas_light.json', 'r') as f:
    formulas_light = json.load(f)

with open('../json/constants_light.json', 'r') as f:
    constants_light = json.load(f)

with open('../json/inputs_light.json', 'r') as f:
    inputs_light = json.load(f)

with open('../json/unknowns_light.json', 'r') as f:
    unknowns_light = json.load(f)

with open('../json/input_variables.json', 'r') as f:
    input_variables = json.load(f)


alias2name = {i['alias']: i['name'] for i in input_variables}

def get_value(name, input_values, computed_values):
    if name in formulas_light:
        return computed_values[name]*np.ones(n)

    if name in constants_light:
        return constants_light[name]*np.ones(n)

    if name in inputs_light:
        return input_values[name]*np.ones(n)

    if name in unknowns_light:
        return np.zeros(n)

    raise Exception('Unknown variable category.')


def prepare(alias_values):
    input_values = {alias2name[alias]: value for alias, value in alias_values.items()}

    input_values_complete = {}
    for name in inputs_light:
        if (name in input_values):
            input_values_complete[name] = input_values[name]
        else:
            input_values_complete[name] = 0.

    return input_values_complete


def compute_formula(node, input_values, computed_values):
    nodetype = node['nodetype']

    if nodetype == 'symbol':
        name = node['name']
        value = get_value(name, input_values, computed_values)
        return value

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
        formula = formulas_light[variable]
        computed_values[variable] = compute_formula(formula, input_values, computed_values)

    important_vars = ['NBPT', 'REVKIRE', 'BCSG', 'BCSG', 'BRDS', 'IBM23', 'TXMOYIMP', 'NAPTIR', 'IINET', 'RRRBG', 'RNI', 'IDRS3', 'IAVIM']
    return {var: computed_values[var] for var in important_vars}
