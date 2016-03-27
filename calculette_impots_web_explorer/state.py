# -*- coding: utf-8 -*-


from calculette_impots import loaders
from calculette_impots.variables_definitions import VariablesDefinitions


"""Global variables loaded once at application start."""


constants = loaders.load_constants()
definition_by_error_name = loaders.load_errors_definitions()
dependencies_by_formula_name = loaders.load_formulas_dependencies()
variables_definitions = VariablesDefinitions(constants=constants)
