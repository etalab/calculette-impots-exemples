# -*- coding: utf-8 -*-

from collections import OrderedDict
import os

from calculette_impots.generated import formulas  # , verifs
from flask import render_template, request, url_for
from toolz import concatv, unique, valfilter
from werkzeug.exceptions import NotFound
from werkzeug.routing import RequestRedirect

from . import state


def build_variable(variable_name_or_alias, saisie_variable_value_by_name):
    from .application import app  # Import here to avoid cyclic modules import.

    variable_definition = state.variables_definitions.definition_by_variable_name.get(variable_name_or_alias)
    if variable_definition is None:
        alias_variables_definitions = list(filter(
            lambda definition: definition.get('alias') == variable_name_or_alias,
            state.variables_definitions.definition_by_variable_name.values(),
            ))
        if alias_variables_definitions:
            raise RequestRedirect(url_for(
                'variable',
                variable_name_or_alias=alias_variables_definitions[0]['name'],
                **request.args
                ))
    if variable_definition is None:
        if variable_name_or_alias not in state.constants:
            return None
        variable_definition = dict(name=variable_name_or_alias)

    variable_dependencies = sorted(state.dependencies_by_formula_name.get(variable_name_or_alias) or [])
    variable_reverse_dependencies = sorted(valfilter(
        lambda val: variable_name_or_alias in val,
        state.dependencies_by_formula_name,
        ).keys())

    variable = OrderedDict()
    variable.update(variable_definition)
    if variable_dependencies:
        variable['dependencies'] = variable_dependencies
    if variable_reverse_dependencies:
        variable['reverse_dependencies'] = variable_reverse_dependencies

    if variable_definition.get('type') == 'variable_calculee' and not variable_definition.get('base'):
        ((startline, _), (endline, _)) = variable_definition['formula_linecol'] or \
            variable_definition['pour_formula_linecol']
        source_file_path = os.path.join(app.config['M_SOURCE_FILES_DIR_PATH'], variable_definition['source_file_name'])
        with open(source_file_path) as source_file:
            formula_source = ''.join(source_file.readlines()[startline - 1:endline]).strip()
        formula_source_html = formula_source
        for dependency_name in variable_dependencies:
            dependency_description = state.variables_definitions.get_description(dependency_name)
            if dependency_description is not None:
                formula_source_html = formula_source_html.replace(
                    dependency_name,
                    '<abbr title="{}">{}</abbr>'.format(dependency_description, dependency_name),
                    )
        variable['formula_source_html'] = formula_source_html
        evaluated_formula_source_html = formula_source
        for dependency_name in variable_dependencies:
            dependency_value = saisie_variable_value_by_name.get(dependency_name, 0)
            evaluated_formula_source_html = evaluated_formula_source_html.replace(
                dependency_name,
                str(dependency_value).rjust(len(dependency_name)),
                )
        variable['evaluated_formula_source_html'] = evaluated_formula_source_html
        variable['source_file_git_url'] = '{}{}#L{}-{}'.format(
            app.config['SOURCE_FILE_GIT_BASE_URL'],
            variable_definition['source_file_name'],
            startline,
            endline,
            )

    return variable


def variable(variable_name_or_alias):
    # Process controller arguments.

    input_error_by_name = {}

    saisie_variable_input_by_name = {}
    for name, value in request.args.items():
        if name == 'historique':
            continue
        if state.variables_definitions.is_saisie(name):
            if value:
                saisie_variable_input_by_name[name] = value
            else:
                input_error_by_name[name] = u"L'argument {!r} n'a pas de valeur.".format(name)
        else:
            input_error_by_name[name] = u"L'argument {!r} n'est pas une variable de saisie.".format(name)

    saisie_variable_value_by_name = {}
    for name, input in saisie_variable_input_by_name.items():
        try:
            saisie_variable_value_by_name[name] = float(input)
        except ValueError:
            input_error_by_name[name] = u"La valeur {!r} n'est pas un nombre.".format(input)

    variable = build_variable(variable_name_or_alias, saisie_variable_value_by_name)
    if variable is None:
        raise NotFound(u"La variable {!r} n'est pas définie.".format(variable_name_or_alias))

    history_input = request.args.get('historique') or ''
    history = list(unique(concatv(
        [variable['name']],
        filter(
            lambda name: name and name not in saisie_variable_input_by_name and (
                name in state.variables_definitions.definition_by_variable_name or name in state.constants),
            map(lambda name: name.strip(), history_input.split('-')),
            ),
        )))

    # Verify input variables & calculate formulas.

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

    # Return rendered page.

    return render_template(
        'variable.html',
        history=history,
        history_str='-'.join(history),
        input_error_by_name=OrderedDict(sorted(input_error_by_name.items())),
        saisie_variable_input_by_name=OrderedDict(sorted(saisie_variable_input_by_name.items())),
        state=state,
        variable=variable,
        variable_value_by_name=variable_value_by_name,
        )


def variables():
    definition_by_variable_name = state.variables_definitions.definition_by_variable_name
    return render_template(
        'variables.html',
        calculee_variables=OrderedDict([
            (variable_name, definition)
            for variable_name, definition in sorted(definition_by_variable_name.items())
            if definition['type'] == 'variable_calculee'
            ]),
        saisie_variables=OrderedDict([
            (variable_name, definition)
            for variable_name, definition in sorted(definition_by_variable_name.items())
            if definition['type'] == 'variable_saisie'
            ]),
        )
