# -*- coding: utf-8 -*-


from flask import jsonify, redirect, url_for
from toolz import valfilter
from werkzeug.exceptions import NotFound

from .. import state


def variable(variable_name_or_alias):
    variable_definition = state.variables_definitions.definition_by_variable_name.get(variable_name_or_alias)
    if variable_definition is None:
        alias_variables_definitions = list(filter(
            lambda definition: definition.get('alias') == variable_name_or_alias,
            state.variables_definitions.definition_by_variable_name.values(),
            ))
        if alias_variables_definitions:
            return redirect(url_for('variable', variable_name_or_alias=alias_variables_definitions[0]['name']))
        else:
            raise NotFound('The variable {!r} is not defined.'.format(variable_name_or_alias))
    variable_dependencies = state.dependencies_by_formula_name.get(variable_definition['name'])
    if variable_dependencies is not None:
        variable_dependencies = sorted(variable_dependencies)
    variable_reverse_dependencies = sorted(valfilter(
        lambda val: variable_definition['name'] in val,
        state.dependencies_by_formula_name,
        ).keys()) or None
    return jsonify(valfilter(
        lambda val: val is not None,
        {
            'variable_definition': variable_definition,
            'variable_dependencies': variable_dependencies,
            'variable_reverse_dependencies': variable_reverse_dependencies,
            },
        ))


def variables():
    return jsonify({'variables_definitions': state.variables_definitions.definition_by_variable_name})
