
from setuptools import setup, find_packages


setup(
    name='calculette_impots_exemples',
    version='1.0.0',

    author='Etalab',
    author_email='info@data.gouv.fr',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Information Analysis',
        ],
    description="Exemples de calculs de l'impôt sur le revenu",
    keywords='calculette impôts tax france',
    license='http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    url='https://git.framasoft.org/openfisca/calculette-impots-m-???',

    install_requires=[
        'jupyter >= 1.0',
        'numpy >= 1.13',
        'matplotlib >= 2.0',
        'tensorflow >= 1.3',
        ],
    packages=find_packages(),
    )
