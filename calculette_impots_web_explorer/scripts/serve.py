#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys

from calculette_impots_web_explorer import application


def main():
    app = application.make_app()
    app.run(debug=True, port=5010)


if __name__ == '__main__':
    sys.exit(main())
