# -*- coding: utf-8 -*-


import sys

from logging import Formatter, StreamHandler
from logging.handlers import SMTPHandler
import logging

from calculette_impots_web_explorer.application import app as application


application.config.update({
    # Display application exceptions in Apache log.
    # Disabled because logging handlers are not executed due to exception.
    #'PROPAGATE_EXCEPTIONS': True,

    # Overload application instance config.
    'M_SOURCE_FILES_DIR_PATH': '/home/openfisca/calculette-impots-m-source-code/src',
    })


# Log exceptions in /var/log/apache2/error.log

stream_handler = StreamHandler(stream=sys.stderr)
stream_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
    ))
stream_handler.setLevel(logging.WARNING)
application.logger.addHandler(stream_handler)


# Setup email sending on application exception.

ADMINS = ['contact@openfisca.fr']
mail_handler = SMTPHandler(
    '127.0.0.1',
    'webmaster+calc.ir@openfisca.fr',
    ADMINS,
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
application.logger.addHandler(mail_handler)
