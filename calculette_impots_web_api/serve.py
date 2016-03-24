# -*- coding: utf-8 -*-


from collections import defaultdict
import json
import os
import pkg_resources

from flask import Flask, jsonify, request
from toolz.curried import map, pipe, unique, valfilter

from calculette_impots import core
from calculette_impots.generated import formulas, verifs


app = Flask(__name__)


def load_errors_definitions():
    m_language_parser_dir_path = pkg_resources.get_distribution('calculette_impots_m_language_parser').location
    errors_definitions_file_path = os.path.join(m_language_parser_dir_path, 'json', 'ast', 'errH.json')
    with open(errors_definitions_file_path) as errors_definitions_file:
        errors_definitions_str = errors_definitions_file.read()
    errors_definitions = json.loads(errors_definitions_str)
    return errors_definitions


@app.route('/')
def index():
    return jsonify(message='Hello, this is "calculette-impots-web-api". Hint: use /api/1/calculate endpoint.')


@app.route('/api/1/calculate')
def calculate():
    # Validate inputs

    calculees_arg = request.args.getlist('calculee') or None
    saisies_arg = request.args.get('saisies')
    saisie_variables = {}
    if saisies_arg is not None:
        try:
            saisie_variables = json.loads(saisies_arg)
        except ValueError:
            return jsonify({'errors': ['"saisies" GET parameter must contain a valid JSON.']})

    wrong_saisie_variable_names = list(filter(
        lambda variable_name: core.get_variable_type(variable_name) != 'variable_saisie',
        saisie_variables.keys(),
        ))
    if wrong_saisie_variable_names:
        return jsonify({'errors': [
            '"saisies" GET parameter contains the variable "{}" which is not a "saisie" variable.'.format(variable_name)
            for variable_name in wrong_saisie_variable_names
            ]})

    warning_messages_by_section = defaultdict(list)

    if calculees_arg is None:
        calculee_variable_names = core.find_restituee_variables()
    else:
        calculee_variable_names = calculees_arg
        for calculee_variable_name in calculee_variable_names:
            if not core.is_restituee_variable(calculee_variable_name):
                warning_messages_by_section['saisies'].append(
                    'Variable "{}" is not a variable of type "calculee restituee"'.format(calculee_variable_name)
                    )

    if 'V_ANREV' not in saisie_variables:
        warning_messages_by_section['saisies'].append(
            'V_ANREV should be given as a "saisie" variable. Hint: saisies={"V_ANREV":2014}.'
            )

    # Load formula functions with a new cache for each HTTP request

    result_by_formula_name_cache = {}
    formulas_functions = formulas.get_formulas(
        cache=result_by_formula_name_cache,
        saisie_variables=saisie_variables,
        )

    # Apply verifs

    errors = verifs.get_errors(
        formulas=formulas_functions,
        saisie_variables=saisie_variables,
        )
    if errors is not None:
        errors_definitions = load_errors_definitions()
        definition_by_error_name = pipe(errors_definitions, map(lambda d: (d['name'], d)), dict)
        warning_messages_by_section['verif_errors'] = [
            (error, definition_by_error_name.get(error, {}).get('description'))
            for error in unique(errors)  # Keep order
            ]

    # Calculate results

    results = {
        calculee_variable_name: formulas_functions[calculee_variable_name]()
        for calculee_variable_name in calculee_variable_names
        }
    if calculees_arg is None:
        results = valfilter(lambda val: val > 0, results)

    return jsonify({'results': results})


if __name__ == '__main__':
    app.run(debug=True)
