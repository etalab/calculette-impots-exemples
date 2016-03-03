#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Transpile (roughly means convert) a JSON AST file to Python source code.
"""


from operator import itemgetter
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

from toolz.curried import concat, filter, map, mapcat, pipe, sorted, valmap

from calculateur_impots import python_source_visitors


# Globals


args = None
script_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(script_name)

script_dir_path = os.path.dirname(os.path.abspath(__file__))
generated_dir_path = os.path.abspath(os.path.join(script_dir_path, '..', 'generated'))


# Source code helper functions


def lines_to_python_source(sequence):
    return ''.join(itertools.chain.from_iterable(zip(sequence, itertools.repeat('\n'))))


def read_ast_json_file(json_file_name):
    nodes = read_json_file(os.path.join('ast', json_file_name))
    assert isinstance(nodes, list)
    return nodes


def read_json_file(json_file_name):
    json_file_path = os.path.join(args.json_dir, json_file_name)
    with open(json_file_path) as json_file:
        json_str = json_file.read()
    return json.loads(json_str)


def write_source_file(file_name, source):
    header = """\
# -*- coding: utf-8 -*-
# flake8: noqa
# WARNING: This file is automatically generated by a script. No not modify it by hand!
"""
    file_path = os.path.join(generated_dir_path, file_name)
    with open(file_path, 'w') as output_file:
        output_file.write(lines_to_python_source((header, source)))
    log.info('Output file "{}" written with success'.format(file_path))


# Load files functions


def iter_ast_json_file_names(*pathnames):
    for json_file_path in sorted(mapcat(
                lambda pathname: glob.iglob(os.path.join(args.json_dir, 'ast', pathname)),
                pathnames,
                )):
        json_file_name = os.path.basename(json_file_path)
        if args.json is None or json_file_name in args.json:
            file_name_head = os.path.splitext(json_file_name)[0]
            yield json_file_name


def load_regles_file(json_file_name):
    log.info('Loading "{}"...'.format(json_file_name))
    regles_nodes = read_ast_json_file(json_file_name)
    batch_application_regles_nodes = filter(
        lambda node: 'batch' in node['applications'],
        regles_nodes,
        )
    formula_name_and_source_pairs = mapcat(python_source_visitors.visit_node, batch_application_regles_nodes)
    return formula_name_and_source_pairs


# def load_verifs_file(json_file_name):
#     log.info('Loading "{}"...'.format(json_file_name))
#     verifs_nodes = read_ast_json_file(json_file_name)


# Main


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='Display debug messages')
    parser.add_argument('--json', nargs='+', help='Parse only this JSON file and exit')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Increase output verbosity')
    parser.add_argument('json_dir', help='Directory containing the JSON AST files and semantic data')
    global args
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.debug else (logging.INFO if args.verbose else logging.WARNING),
        stream=sys.stdout,
        )

    if not os.path.isdir(generated_dir_path):
        os.mkdir(generated_dir_path)

    if args.json is not None:
        for json_file_name in args.json:
            json_file_path = os.path.join(args.json_dir, 'ast', json_file_name)
            if not os.path.exists(json_file_path):
                parser.error('JSON file "{}" does not exist.'.format(json_file_path))

    # Transpile constants

    constants_file_name = os.path.join('semantic_data', 'constants.json')
    constants = read_json_file(json_file_name=constants_file_name)
    constants_source = pipe(
        constants.items(),
        sorted,
        map(lambda item: '{} = {}'.format(*item)),
        lines_to_python_source,
        )
    write_source_file(
        file_name='constants.py',
        source=constants_source,
        )

    # Transpile variables definitions

    variables_definitions_file_name = os.path.join('semantic_data', 'variables_definitions.json')
    variable_definition_by_name = read_json_file(json_file_name=variables_definitions_file_name)
    write_source_file(
        file_name='variables_definitions.py',
        source='variable_definition_by_name = {}\n'.format(pprint.pformat(variable_definition_by_name, width=120)),
        )

    # Transpile formulas

    formula_source_by_name = dict(list(mapcat(
        load_regles_file,
        iter_ast_json_file_names('chap-*.json', 'res-ser*.json'),
        )))
    assert formula_source_by_name

    variables_dependencies_file_name = os.path.join('semantic_data', 'variables_dependencies.json')
    variable_dependencies_by_name = read_json_file(json_file_name=variables_dependencies_file_name)

    ordered_formulas_names_file_name = os.path.join('semantic_data', 'ordered_formulas.json')
    ordered_formulas_names = read_json_file(json_file_name=ordered_formulas_names_file_name)

    write_source_file(
        file_name='formulas.py',
        source=lines_to_python_source(itertools.chain(
            (
                'from ..core import *',
                'from .constants import *',
                '\n',
                ),
            pipe(
                ordered_formulas_names,
                map(python_source_visitors.sanitized_variable_name),
                map(lambda formula_name: formula_source_by_name.get(formula_name, '{} = 0'.format(formula_name))),
                ),
            ),
        ))

    # for json_file_name in iter_ast_json_file_names('coc*.json', 'coi*.json'):
        # load_verifs_file(json_file_name)

    return 0


if __name__ == '__main__':
    sys.exit(main())
