#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Transpile (roughly means convert) a JSON AST file to Python source code.
"""


import argparse
import copy
import glob
import itertools
import json
import logging
import os
import pprint
import sys
import textwrap


# Globals


args = None
script_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(script_name)

script_dir_path = os.path.dirname(os.path.abspath(__file__))
generated_dir_path = os.path.abspath(os.path.join(script_dir_path, '..', 'generated'))


# Source code helper functions


def read_ast_json_file(json_file_name):
    json_file_path = os.path.join(args.json_dir, json_file_name)
    with open(json_file_path) as json_file:
        json_str = json_file.read()
    nodes = json.loads(json_str)
    return nodes


def sanitized_variable_name(value):
    # Python variables must not begin with a digit.
    return '_' + value if value[0].isdigit() else value


def value_to_python_source(value):
    return pprint.pformat(value, indent=4, width=120)


def write_source(file_name, json_file_name, original_file_name, transpilation_function):
    header = """\
# -*- coding: utf-8 -*-


# WARNING: This file is automatically generated by a script. No not modify it by hand!

# Original files are "{}" and "{}"


""".format(json_file_name, original_file_name)
    global args
    file_path = os.path.join(generated_dir_path, file_name)
    if os.path.exists(file_path) and not args.force and args.json is None:
        log.info('Output file "{}" exists => skip.'.format(file_path))
    elif args.json is None or json_file_name in args.json:
        log.debug(
            'Transpiling JSON file "{}" with function "{}"'.format(json_file_name, transpilation_function.__name__),
            )
        source = transpilation_function(json_file_name)
        with open(file_path, 'w') as output_file:
            output_file.write(header + source)
        log.info('Output file "{}" was written with success.'.format(file_path))


# Generic transpilation function


def infix_expression_to_python_source(node, operators={}):
    def merge(*iterables):
        for values in itertools.zip_longest(*iterables, fillvalue=UnboundLocalError):
            for index, value in enumerate(values):
                if value != UnboundLocalError:
                    yield index, value

    tokens = (
        node_to_python_source(operand_or_operator)
        if index == 0
        else operators.get(operand_or_operator, operand_or_operator)
        for index, operand_or_operator in merge(node['operands'], node['operators'])
        )
    return ' '.join(map(str, tokens))


class TranspilationError(Exception):
    pass


deep_level = 0


def node_to_python_source(node, parenthesised=False):
    global deep_level
    transpilation_function_name = node['type'] + '_to_python_source'
    if transpilation_function_name not in globals():
        error_message = '"def {}(node):" is not defined, node = {}'.format(
            transpilation_function_name,
            value_to_python_source(node),
            )
        raise NotImplementedError(error_message)
    node_str = textwrap.indent(
        value_to_python_source(node),
        prefix='>' + ' ' * (deep_level * 4 + len('DEBUG:' + script_name) + len(transpilation_function_name) + 1),
        )[1:].lstrip()
    log.debug('{}{}({})'.format(' ' * deep_level * 4, transpilation_function_name, node_str))
    transpilation_function = globals()[transpilation_function_name]
    deep_level += 1
    try:
        source = transpilation_function(node)
    except (NotImplementedError, TranspilationError):
        # Bubble up all nested calls of node_to_python_source.
        raise
    except Exception:  # We really want to catch all exceptions to debug.
        raise TranspilationError(value_to_python_source(node))
    source = str(source)
    if parenthesised and node['type'] not in ('integer', 'float', 'string', 'symbol'):
        source = '({})'.format(source)
    deep_level -= 1
    log.debug('{}=> {}'.format(' ' * deep_level * 4, textwrap.indent(source, prefix='> ')[1:].lstrip()))
    assert deep_level >= 0, deep_level
    return source


# Specific transpilation functions


def boolean_expression_to_python_source(node):
    return infix_expression_to_python_source(node, operators={'et': 'and', 'ou': 'or'})


def comparaison_to_python_source(node):
    return '{} {} {}'.format(
        node_to_python_source(node['left_operand']),
        {'=': '=='}.get(node['operator'], node['operator']),
        node_to_python_source(node['right_operand']),
        )


def dans_to_python_source(node):
    if not all(option['type'] == 'symbol' for option in node['options']):
        raise NotImplementedError(node)
    return '{} in {}'.format(
        node_to_python_source(node['expression'], parenthesised=True),
        '({})'.format(', '.join(option['value'] for option in node['options']))
        )


def expression_to_python_source(node):
    return node_to_python_source(node)


def float_to_python_source(node):
    return node['value']


def formula_to_python_source(node):
    def find_symbols(node):
        """Find all nodes matching `type` recursively in the AST tree."""
        if isinstance(node, dict):
            if node['type'] == 'symbol':
                symbols.append(node)
            else:
                find_symbols(list(node.values()))
        elif isinstance(node, list):
            for child_node in node:
                if isinstance(child_node, (list, dict)):
                    find_symbols(child_node)

    expression_source = node_to_python_source(node['expression'])
    symbols = []
    find_symbols(node['expression'])
    return 'def {name}({parameters}):\n{docstring}    return {expression}\n'.format(
        docstring='    """{}"""\n'.format(node['__docstring__']) if '__docstring__' in node else '',
        expression=expression_source,
        name=sanitized_variable_name(node['name']),
        parameters=', '.join(sorted(set(map(node_to_python_source, symbols)))),
        )


def function_call_to_python_source(node):
    return '{name}({arguments})'.format(
        arguments=', '.join(map(node_to_python_source, node['arguments'])),
        name=node['name'],
        )


def integer_to_python_source(node):
    return node['value']


def loop_expression_to_python_source(node):
    # TODO
    return node_to_python_source(node['expression'])


def pour_formula_to_python_source(node):
    def create_unlooped_formula_node(formula_node, loop_variable_name, loop_variable_value):
        new_formula_node = copy.deepcopy(formula_node)
        new_formula_node.update({
            'name': formula_node['name'].replace(loop_variable_name, loop_variable_value, 1),
            '__docstring__': 'Original formula "{}" having {} = {}'.format(
                formula_node['name'],
                loop_variable_name,
                loop_variable_value,
                ),
            })
        unloop_symbols(
            node=new_formula_node,
            loop_variable_name=loop_variable_name,
            loop_variable_value=loop_variable_value,
            )
        return new_formula_node

    def unloop_symbols(node, loop_variable_name, loop_variable_value):
        """
        Replace `loop_variable_name` by `loop_variable_value` in symbols recursively found in `node`.
        This function mutates `node` and returns nothing.
        """
        if isinstance(node, dict):
            if node['type'] == 'symbol':
                node['value'] = node['value'].replace(loop_variable_name, loop_variable_value, 1)
            else:
                unloop_symbols(list(node.values()), loop_variable_name, loop_variable_value)
        elif isinstance(node, list):
            for child_node in node:
                if isinstance(child_node, (list, dict)):
                    unloop_symbols(child_node, loop_variable_name, loop_variable_value)

    def iter_unlooped_formulas(formula_node, loop_variable_domain_nodes, loop_variable_name):
        """
        Yield many formulas given one formula and a loop variable name and domains (symbols and/or integer ranges).
        The loop_variable_name is replaced in the formula name.
        """
        # Do not use "in" operator, strictly check for 1 occurence.
        assert formula_node['name'].count(loop_variable_name) == 1, (loop_variable_name, formula_node)

        for domain_node in loop_variable_domain_nodes:
            if domain_node['type'] == 'symbol':
                yield create_unlooped_formula_node(
                    formula_node=formula_node,
                    loop_variable_name=loop_variable_name,
                    loop_variable_value=domain_node['value'],
                    )
            elif domain_node['type'] == 'integer_range':
                for index in range(domain_node['first'], domain_node['last'] + 1):
                    yield create_unlooped_formula_node(
                        formula_node=formula_node,
                        loop_variable_name=loop_variable_name,
                        loop_variable_value=str(index),
                        )
            else:
                raise NotImplementedError('Unknown type for domain_node = {}'.format(domain_node))

    formulas = itertools.chain.from_iterable(
        iter_unlooped_formulas(
            formula_node=node['formula'],
            loop_variable_domain_nodes=loop_variable['domains'],
            loop_variable_name=loop_variable['name'],
            )
        for loop_variable in node['loop_variables']
        )
    return (2 * '\n').join(map(node_to_python_source, formulas))


def product_expression_to_python_source(node):
    return infix_expression_to_python_source(node)


def regle_to_python_source(node):
    return (2 * '\n').join(map(node_to_python_source, node['formulas'])) + '\n'


def sum_expression_to_python_source(node):
    return infix_expression_to_python_source(node)


def symbol_to_python_source(node):
    return sanitized_variable_name(node['value'])


def ternary_operator_to_python_source(node):
    return '{} if {} else {}'.format(
        node_to_python_source(node['value_if_true'], parenthesised=True),
        node_to_python_source(node['condition'], parenthesised=True),
        node_to_python_source(node['value_if_false'], parenthesised=True) if 'value_if_false' in node else 0,
        )


# File transpilation functions


def chap_to_python_source(json_file_name):
    global args
    regle_nodes = list(filter(
        lambda node: args.application in node['applications'],
        read_ast_json_file(json_file_name),
        ))
    source = '\n'.join(map(node_to_python_source, regle_nodes))
    return source


def tgvH_json_to_python_source(json_file_name):
    nodes = read_ast_json_file(json_file_name)
    variable_definition_by_name = {
        node['name']: node
        for node in nodes
        if node['type'] in ('variable_calculee', 'variable_saisie')
        }
    source = 'variable_definition_by_name = ' + value_to_python_source(variable_definition_by_name)
    return source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--application', default='batch', help='Application name')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='Display debug messages')
    parser.add_argument('-f', '--force', action='store_true', default=False, help='Transpile files which exist')
    parser.add_argument('--json', nargs='+', help='Transpile these JSON files only (give only file name)')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Increase output verbosity')
    parser.add_argument('json_dir', help='Directory containing the JSON AST files')
    global args
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.debug else (logging.INFO if args.verbose else logging.WARNING),
        stream=sys.stdout,
        )

    if args.json is not None:
        for json_file_name in args.json:
            json_file_path = os.path.join(args.json_dir, json_file_name)
            if not os.path.exists(json_file_path):
                parser.error('JSON file "{}" does not exist.'.format(json_file_path))

    write_source(
        file_name='variables_definitions.py',
        json_file_name='tgvH.json',
        original_file_name='tgvH.m',
        transpilation_function=tgvH_json_to_python_source,
        )

    for json_file_path in sorted(glob.iglob(os.path.join(args.json_dir, 'chap-*.json'))):
        json_file_name = os.path.basename(json_file_path)
        file_name_head, _ = os.path.splitext(json_file_name)
        write_source(
            file_name=file_name_head.replace('-', '_') + '.py',
            json_file_name=json_file_name,
            original_file_name=file_name_head + '.m',
            transpilation_function=chap_to_python_source,
            )

    return 0


if __name__ == '__main__':
    sys.exit(main())
