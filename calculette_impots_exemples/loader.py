
import inspect
import os
import json

import calculette_impots_m_language_parser

package_base_dir = os.path.dirname(os.path.dirname(inspect.getfile(calculette_impots_m_language_parser)))
json_dir = os.path.join(package_base_dir, 'json')

def load_json(millesime):
    simplified_ast_dir = os.path.join(json_dir, millesime, '2_simplified_ast')
    light_ast_dir = os.path.join(json_dir, millesime, '3_light_ast')

    with open(os.path.join(light_ast_dir, 'computing_order.json'), 'r') as f:
        computing_order = json.load(f)

    with open(os.path.join(light_ast_dir, 'children_light.json'), 'r') as f:
        children_light = json.load(f)

    with open(os.path.join(light_ast_dir, 'formulas_light.json'), 'r') as f:
        formulas_light = json.load(f)

    with open(os.path.join(light_ast_dir, 'constants_light.json'), 'r') as f:
        constants_light = json.load(f)

    with open(os.path.join(light_ast_dir, 'inputs_light.json'), 'r') as f:
        inputs_light = json.load(f)

    with open(os.path.join(light_ast_dir, 'unknowns_light.json'), 'r') as f:
        unknowns_light = json.load(f)

    with open(os.path.join(simplified_ast_dir, 'input_variables.json'), 'r') as f:
        input_variables = json.load(f)

    return computing_order, children_light, formulas_light, constants_light, inputs_light, unknowns_light, input_variables
