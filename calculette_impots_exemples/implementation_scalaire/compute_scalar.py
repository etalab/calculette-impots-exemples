import json

from .function_set_scalaire import functions_mapping
from ..loader import load_json


class ScalarComputationEngine(object):
    def __init__(self, millesime):
        self.millesime = millesime

        self.computing_order, self.children_light, self.formulas_light, self.constants_light, self.inputs_light, self.unknowns_light, self.input_variables = load_json(millesime)

        self.alias2name = {i['alias']: i['name'] for i in self.input_variables}


    def compute(self, alias_values, formula_names):

        def get_value(name, input_values, computed_values):
            if name in self.formulas_light:
                return computed_values[name]

            if name in self.constants_light:
                return self.constants_light[name]

            if name in self.inputs_light:
                return input_values[name]

            if name in self.unknowns_light:
                return 0.

            raise Exception('Unknown variable category.')

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
                return value

            if nodetype == 'call':
                name = node['name']
                args = [compute_formula(child, input_values, computed_values) for child in node['args']]
                function = functions_mapping[name]
                value = function(args)
                return value

            raise ValueError('Unknown type : %s'%nodetype)

        input_values = prepare(alias_values)

        computed_values = {}
        for variable in self.computing_order:
            formula = self.formulas_light[variable]
            computed_values[variable] = compute_formula(formula, input_values, computed_values)

        return {var: computed_values[var] for var in formula_names}
