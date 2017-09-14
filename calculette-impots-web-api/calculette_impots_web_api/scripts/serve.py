#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys

from calculette_impots_web_api.application import app


def main():
    app.run(debug=True, port=5000)


if __name__ == '__main__':
    sys.exit(main())
