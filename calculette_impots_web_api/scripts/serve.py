#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys

from calculette_impots_web_api import application


def main():
    app = application.make_app()
    app.run(debug=True, port=5000)


if __name__ == '__main__':
    sys.exit(main())
