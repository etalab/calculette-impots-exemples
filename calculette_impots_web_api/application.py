# -*- coding: utf-8 -*-


from flask import Flask, jsonify


from . import calculate, variables


def create_application():
    app = Flask('calculette-impots-web-api')

    @app.route('/')
    def index_controller():
        return jsonify(message='Hello, this is "calculette-impots-web-api". Hint: use /api/1/calculate endpoint.')

    app.route('/api/1/calculate')(calculate.calculate_controller)

    app.route('/api/1/variables')(variables.variables_controller)

    return app
