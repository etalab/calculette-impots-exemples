# -*- coding: utf-8 -*-


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
        response = jsonify({'description': ex.description, 'message': str(ex)})
        response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
        return response

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.keys():
        app.error_handler_spec[None][code] = make_json_error

    return app


app = make_json_app('calculette_impots_web_api')


@app.route('/')
def index():
    return jsonify({'message': 'Hello, this is "calculette-impots-web-api". Hint: use /api/1/calculate endpoint.'})

app.route('/api/1/calculate')(calculate.calculate)

app.route('/api/1/variables')(variables.variables)
app.route('/api/1/variables/<variable_name_or_alias>')(variables.variable)
