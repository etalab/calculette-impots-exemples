# -*- coding: utf-8 -*-

from collections import OrderedDict
from urllib.parse import urlparse

from calculette_impots.generated import formulas  # , verifs
from flask import jsonify, render_template, request, url_for
from toolz import concatv, unique, valfilter
from werkzeug.exceptions import NotFound, NotImplemented

from . import state


def build_variable(variable_name):
    variable_definition = state.variables_definitions.definition_by_variable_name.get(variable_name)
    if variable_definition is None:
        if variable_name not in state.constants:
            return None
        variable_definition = dict(name = variable_name)

    variable_dependencies = sorted(state.dependencies_by_formula_name.get(variable_name) or [])
    variable_reverse_dependencies = sorted(valfilter(
        lambda val: variable_name in val,
        state.dependencies_by_formula_name,
        ).keys())

    variable = OrderedDict()
    variable.update(variable_definition)
    if variable_dependencies:
        variable['dependencies'] = variable_dependencies
    if variable_reverse_dependencies:
        variable['reverse_dependencies'] = variable_reverse_dependencies

    return variable


def oembed():
    # cf http://oembed.com/

    format = request.args.get('format')
    if format not in (None, '', 'json'):
        raise NotImplemented("Le format {!r} n'est pas supporté.".format(format))
    maxheight = request.args.get('maxheight', -1, int)
    maxwidth = request.args.get('maxwidth', -1, int)
    url = request.args.get('url')
    if not url:
        raise NotFound("Le paramètre 'url' est requis.")
    parsed_url = urlparse(url)
    variable_name = parsed_url.path.strip('/').split('/')[0]
    variable = build_variable(variable_name)
    if variable is None:
        raise NotFound("La variable {!r} n'est pas définie.".format(variable_name))

    return jsonify(dict(
        height=min(600, maxheight) if maxheight > 0 else 600,
        html=render_template(
            'variable-oembed.html',
            variable=variable,
            ),
        provider_name='Explorateur des variables de la calculette impôts',
        provider_url=url_for('variables', _external=True),
        title=variable['name'],
        type='rich',
        version='1.0',
        width=min(200, maxwidth) if maxwidth > 0 else 200,
        ))


def variable(variable_name):
    # Process controller arguments.

    variable = build_variable(variable_name)
    if variable is None:
        raise NotFound("La variable {!r} n'est pas définie.".format(variable_name))

    input_error_by_name = {}

    history_input = request.args.get('historique') or ''
    history = list(unique(concatv(
        [variable_name],
        filter(
            lambda name: name and (name in state.variables_definitions.definition_by_variable_name or
                name in state.constants),
            map(lambda name: name.strip(), history_input.split('|')),
            ),
        )))

    saisie_variable_input_by_name = {}
    for name, value in request.args.items():
        if name == 'historique':
            continue
        if state.variables_definitions.is_saisie(name) and value:
            saisie_variable_input_by_name[name] = value
        else:
            input_error_by_name[name] = "L'argument {!r} n'est pas une variable de saisie.".format(name)

    saisie_variable_value_by_name = {}
    for name, input in saisie_variable_input_by_name.items():
        try:
            saisie_variable_value_by_name[name] = float(input)
        except ValueError:
            input_error_by_name[name] = "La valeur {!r} n'est pas un nombre.".format(input)

    # Varify input variables & calculate formulas.

    function_by_name = formulas.get_formulas(
        cache={},
        constants=state.constants,
        saisie_variables=saisie_variable_value_by_name,
        )

    # errors = verifs.get_errors(
    #     formulas=formulas_functions,
    #     saisie_variables=saisie_variables,
    #     )
    # if errors is not None:
    #     warning_messages_by_section['verif_errors'] = [
    #         (error, state.definition_by_error_name.get(error, {}).get('description'))
    #         for error in unique(errors)  # Keep order
    #         ]

    output_variables_name = set()
    if variable['name'] in function_by_name:
        output_variables_name.add(variable['name'])
    output_variables_name.update(variable.get('reverse_dependencies', []))
    for name in variable.get('dependencies', []):
        output_variables_name.add(name)
    for name in history:
        output_variables_name.add(name)

    calculee_variable_value_by_name = {
        name: function_by_name[name]()
        for name in output_variables_name
        }

    # Merge the values of all variables into a single dictionary.
    variable_value_by_name = {}
    variable_value_by_name.update(state.constants)
    variable_value_by_name.update(saisie_variable_value_by_name)
    variable_value_by_name.update(calculee_variable_value_by_name)

    # Return rendred page.

    return render_template(
        'variable.html',
        history = history,
        history_str = '|'.join(history),
        input_error_by_name=OrderedDict(sorted(input_error_by_name.items())),
        saisie_variable_input_by_name=saisie_variable_input_by_name,
        variable=variable,
        variable_value_by_name=variable_value_by_name,
        )


def variables():
    return render_template('variables.html',
        variables_name=sorted(state.variables_definitions.definition_by_variable_name))
