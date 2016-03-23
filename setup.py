#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
    name='calculette_impots_web_api',
    version='0.0.0.dev0',

    author='Christophe Benz',
    author_email='christophe.benz@data.gouv.fr',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Information Analysis',
        ],
    description='Calculateur des impôts compilé en Python',
    keywords='calculateur impôts tax',
    license='http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    url='https://git.framasoft.org/openfisca/calculette-impots-web-api',

    install_requires=[
        'Flask >= 0.10.1',
        'toolz >= 0.7.4',
        ],
    packages=find_packages(),
    )
