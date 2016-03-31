# -*- coding: utf-8 -*-


from flask import jsonify
from toolz import valfilter
from werkzeug.exceptions import NotFound

from .. import state


def variable(variable_name_or_alias):
    variable_definition = state.variables_definitions.definition_by_variable_name.get(variable_name)
    if variable_definition is None:
        raise NotFound('The variable {!r} is not defined.'.format(variable_name))
    variable_dependencies = state.dependencies_by_formula_name.get(variable_name)
    if variable_dependencies is not None:
        variable_dependencies = sorted(variable_dependencies)
    variable_reverse_dependencies = sorted(valfilter(
        lambda val: variable_name in val,
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
