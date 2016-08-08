# -*- coding: utf-8 -*-


import os

from flask import Flask

from . import views


app = Flask('calculette_impots_web_explorer')

app.config.from_pyfile('config.py')

# Read optional config from another file.
env_variable_name = 'CALCULETTE_IMPOTS_WEB_EXPLORER_SETTINGS'
if os.getenv(env_variable_name):
    app.config.from_envvar(env_variable_name)

app.route('/')(views.variables)
app.route('/<variable_name_or_alias>')(views.variable)
