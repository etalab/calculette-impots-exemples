# -*- coding: utf-8 -*-


from logging.handlers import SMTPHandler
import logging

from calculette_impots_web_explorer.application import app as application


application.config.update({
    # Display application exceptions in Apache log.
    'PROPAGATE_EXCEPTIONS': True,

    # Overload application instance config.
    'M_SOURCE_FILES_DIR_PATH': '/home/openfisca/calculette-impots-m-source-code/src',
    })

# Setup email sending on application exception.

ADMINS = ['contact@openfisca.fr']
mail_handler = SMTPHandler(
    '127.0.0.1',
    'webmaster+calc.ir@openfisca.fr',
    ADMINS,
    'calculette-impots-web-explorer failed',
    )
mail_handler.setLevel(logging.ERROR)
application.logger.addHandler(mail_handler)
