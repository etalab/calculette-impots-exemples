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


# Setup error emails

if app.config.get('ADMIN_EMAILS'):
    from logging import Formatter
    from logging.handlers import SMTPHandler
    import logging

    mail_handler = SMTPHandler(
        '127.0.0.1',
        'webmaster+calc.ir@openfisca.fr',
        app.config['ADMIN_EMAILS'],
        'calculette-impots-web-explorer failed',
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
