# -*- coding: utf-8 -*-


from flask import Flask

from . import variables


def make_app():
    app = Flask('calculette_impots_web_explorer')

    app.route('/')(variables.variables)
    app.route('/oembed')(variables.oembed)
    app.route('/<variable_name>')(variables.variable)

    return app
