# -*- coding: utf-8 -*-


from flask import Flask

from . import views


app = Flask('calculette_impots_web_explorer', instance_relative_config=True)

app.config.from_pyfile('config.py')

app.route('/')(views.variables)
app.route('/<variable_name_or_alias>')(views.variable)
