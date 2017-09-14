#! /usr/bin/env python3
# -*- coding: utf-8 -*-


# cf http://flask.pocoo.org/docs/0.10/patterns/distribute/


from setuptools import find_packages, setup


setup(
    name='calculette_impots_web_explorer',
    version='0.0.0.dev0',

    author='Emmanuel Raviart',
    author_email='emmanuel.raviart@data.gouv.fr',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Information Analysis',
        ],
    description='Explorateur web des variables et formules de la calculette des impôts',
    keywords='calculator tax web explorer',
    license='http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    url='https://git.framasoft.org/openfisca/calculette-impots-web-explorer',

    entry_points={
        'console_scripts': ['calculette-impots-web-explorer=calculette_impots_web_explorer.scripts.serve:main'],
        },
    include_package_data=True,
    install_requires=[
        'calculette_impots >= 0.0.0.dev0',
        'calculette_impots_m_language_parser >= 0.0.0.dev0',
        'Flask >= 0.10.1',
        'toolz >= 0.7.4',
        ],
    packages=find_packages(),
    )
