# Calculette Impôts - Explorateur Web

## Installation

Le langage Python 3 est utilisé.

Il est nécessaire d'avoir au préalable installé le paquet [calculette-impots-python](https://git.framasoft.org/openfisca/calculette-impots-python).

Ce paquet n'est pas publié sur le dépôt [PyPI](https://pypi.python.org/pypi) donc pour l'installer il faut passer par `git clone`.

```
git clone https://git.framasoft.org/openfisca/calculette-impots-web-explorer.git
cd calculette-impots-web-explorer
pip3 install --editable . --user
```

> L'option `--user` sert sur les systèmes GNU/Linux.

Un utilisateur plus expérimenté en Python peut utiliser
un [`virtualenv`](https://virtualenv.readthedocs.org/en/latest/) s'il le souhaite.

Mettre à jour les variables de configuration dans le fichier `instance/config.py` notamment `M_SOURCE_FILES_DIR_PATH`.

## Démarrer le serveur

```
calculette-impots web-explorer
```

Ou en exécutant directement le script :

``
python3 calculette_impots_web_explorer/scripts/serve.py
``

Puis ouvrir l'URL http://localhost:5010/

## Qualité du code

```
flake8 --max-line-length 120 .
```
