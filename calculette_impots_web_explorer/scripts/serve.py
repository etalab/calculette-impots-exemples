#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys

from calculette_impots_web_explorer.application import app


def main():
    app.run(debug=True, port=app.config['PORT'])


if __name__ == '__main__':
    sys.exit(main())
