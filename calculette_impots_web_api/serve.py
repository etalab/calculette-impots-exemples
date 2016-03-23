# -*- coding: utf-8 -*-


import json
import os
import pkg_resources

from flask import Flask, jsonify, request
from toolz.curried import map, pipe, unique

from calculateur_impots import core
from calculateur_impots.generated import formulas, verifs


app = Flask(__name__)


def load_errors_definitions():
    m_language_parser_dir_path = pkg_resources.get_distribution('m_language_parser').location
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
    response_json = {}
    if 'V_ANREV' not in saisie_variables:
        response_json['warnings'] = [
            'V_ANREV should be given as a "saisie" variable. Hint: saisies={"V_ANREV":2014}.',
            ]

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
        response_json['verif_errors'] = [
            (
                error,
                definition_by_error_name.get(error, {}).get('description'),
                )
            for error in unique(errors)  # Keep order
            ]

    # Calculate results

    restituee_variables = core.find_restituee_variables()
    calculee_variables = calculees_arg or restituee_variables
    response_json['results'] = {
        calculee_variable: formulas_functions[calculee_variable]()
        for calculee_variable in calculee_variables
        }
    if calculees_arg is None:
        response_json['results'] = {
            key: val
            for key, val in response_json['results'].items()
            if val > 0
            }

    return jsonify(response_json)


if __name__ == '__main__':
    app.run(debug=True)
