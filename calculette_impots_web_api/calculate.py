# -*- coding: utf-8 -*-


from collections import defaultdict
import json

from calculette_impots.generated import formulas, verifs
from flask import jsonify, request
from toolz.curried import unique, valfilter
from werkzeug.exceptions import BadRequest

from . import state


def calculate_controller():
    # Validate inputs

    calculees_arg = request.args.getlist('calculee') or None
    saisies_arg = request.args.get('saisies')
    saisie_variables = {}
    if saisies_arg is not None:
        try:
            saisie_variables = json.loads(saisies_arg)
        except ValueError:
            raise BadRequest('"saisies" GET parameter must contain a valid JSON.')

    wrong_saisie_variable_names = list(filter(
        lambda variable_name: state.variables_definitions.get_type(variable_name) != 'variable_saisie',
        saisie_variables.keys(),
        ))
    if wrong_saisie_variable_names:
        raise BadRequest([
            '"saisies" GET parameter contains the variable "{}" which is not a "saisie" variable.'.format(variable_name)
            for variable_name in wrong_saisie_variable_names
            ])

    warning_messages_by_section = defaultdict(list)

    if calculees_arg is None:
        calculee_variable_names = state.variables_definitions.filter_calculees(kind='restituee')
    else:
        calculee_variable_names = calculees_arg
        for calculee_variable_name in calculee_variable_names:
            if not state.variables_definitions.is_calculee(calculee_variable_name, kind='restituee'):
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
        constants=state.constants,
        saisie_variables=saisie_variables,
        )

    # Apply verifs

    errors = verifs.get_errors(
        formulas=formulas_functions,
        saisie_variables=saisie_variables,
        )
    if errors is not None:
        warning_messages_by_section['verif_errors'] = [
            (error, state.definition_by_error_name.get(error, {}).get('description'))
            for error in unique(errors)  # Keep order
            ]

    # Calculate results

    results = {
        calculee_variable_name: formulas_functions[calculee_variable_name]()
        for calculee_variable_name in calculee_variable_names
        }
    if calculees_arg is None:
        results = valfilter(lambda val: val != 0, results)

    return jsonify(valfilter(
        lambda val: val is not None,
        {
            'calculate_results': results,
            'warnings': warning_messages_by_section or None,
            },
        ))
