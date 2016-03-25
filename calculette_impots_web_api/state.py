# -*- coding: utf-8 -*-


from calculette_impots import loaders
from calculette_impots.variables_definitions import VariablesDefinitions


"""Global variables loaded once at application start."""


constants = loaders.load_constants()
definition_by_error_name = loaders.load_errors_definitions()
variables_definitions = VariablesDefinitions(constants=constants)
