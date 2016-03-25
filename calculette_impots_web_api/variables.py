# -*- coding: utf-8 -*-


from flask import jsonify
from werkzeug.exceptions import NotFound

from . import state


def variable_controller(name):
    variable = state.variables_definitions.definition_by_variable_name.get(name)
    if variable is None:
        raise NotFound('The variable {!r} is not defined.'.format(name))
    return jsonify({'variable': variable})


def variables_controller():
    return jsonify({'variables': state.variables_definitions.definition_by_variable_name})
