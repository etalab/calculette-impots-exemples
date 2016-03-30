# Calculette Impôts - Explorateur Web

## Installation

Le langage Python 3 est utilisé.

```
pip3 install --editable . --user
```

> L'option `--user` sert sur les systèmes GNU/Linux.

Un utilisateur plus expérimenté en Python peut utiliser
un [`virtualenv`](https://virtualenv.readthedocs.org/en/latest/) s'il le souhaite.

Mettre à jour les variables de configuration dans le fichier `instance/config.py` notamment `M_SOURCE_FILES_DIR_PATH`.

## Démarrer le serveur

```
calculette-impots-web-explorer
```

## Qualité du code

```
flake8 --max-line-length 120 .
```
