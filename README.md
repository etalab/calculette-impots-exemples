# Calculette Impôts - API Web

## Installation

Le langage Python 3 est utilisé.

```
pip3 install --editable . --user
```

> L'option `--user` sert sur les systèmes GNU/Linux.

Un utilisateur plus expérimenté en Python peut utiliser
un [`virtualenv`](https://virtualenv.readthedocs.org/en/latest/) s'il le souhaite.

## Démarrer le serveur

```
python3 calculette_impots_web_api/serve.py
```

## Appel de l'API Web

Exemple d'URL :

http://localhost:5000/api/1/calculate?calculee=IINET&saisies={%22V_ANREV%22:2014,%22TSHALLOV%22:30000,%22V_0DA%22:1980}

> Les ``%22` représentent des guillemets (`"`) url-encodés.

## Qualité du code

```
flake8 --max-line-length 120 .
```
