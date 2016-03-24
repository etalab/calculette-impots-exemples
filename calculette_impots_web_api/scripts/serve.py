# -*- coding: utf-8 -*-


import sys

from calculette_impots_web_api import application


def main():
    app = application.create_application()
    app.run(debug=True)


if __name__ == '__main__':
    sys.exit(main())
