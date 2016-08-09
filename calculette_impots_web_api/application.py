# -*- coding: utf-8 -*-


import os

from flask import Flask, jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

from .views import calculate, variables


# From http://flask.pocoo.org/snippets/83/
def make_json_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    """
    def make_json_error(ex):
        response_dict = {'description': ex.description, 'message': str(ex)} \
            if isinstance(ex, HTTPException) \
            else {'message': u'500: Internal server error', 'description': str(ex)}
        response = jsonify(response_dict)
        response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
        return response

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.keys():
        # app.error_handler_spec[None][code] = make_json_error
        app.register_error_handler(code, make_json_error)

    return app


app = make_json_app('calculette_impots_web_api')

@app.route('/')
def index():
    return jsonify({'message': 'Hello, this is "calculette-impots-web-api". Hint: use /api/1/calculate endpoint.'})

@app.route('/fail')
def fail():
    #assert 1==2, "1 is not equal to 2!!!"
    boom


app.route('/api/1/calculate')(calculate.calculate)

app.route('/api/1/variables')(variables.variables)
app.route('/api/1/variables/<variable_name_or_alias>')(variables.variable)


# Read optional config from another file.

env_variable_name = 'CALCULETTE_IMPOTS_WEB_API_SETTINGS'
if os.getenv(env_variable_name):
    app.config.from_envvar(env_variable_name)


# Setup error emails

if app.config.get('ADMIN_EMAILS'):
    from logging import Formatter
    from logging.handlers import SMTPHandler
    import logging

    mail_handler = SMTPHandler(
        '127.0.0.1',
        'webmaster+api.ir@openfisca.fr',
        app.config['ADMIN_EMAILS'],
        'calculette-impots-web-api failed',
        )
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(Formatter('''
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s

Message:

%(message)s
'''))
    app.logger.addHandler(mail_handler)
