# Calculette Impôts - API Web

## Installation

Le langage Python 3 est utilisé.

Il est nécessaire d'avoir au préalable installé le paquet [calculette-impots-python](https://git.framasoft.org/openfisca/calculette-impots-python).

Ce paquet n'est pas publié sur le dépôt [PyPI](https://pypi.python.org/pypi) donc pour l'installer il faut passer par `git clone`.

```
git clone https://git.framasoft.org/openfisca/calculette-impots-web-api.git
cd calculette-impots-web-api
pip3 install --editable . --user
```

> L'option `--user` sert sur les systèmes GNU/Linux.

Un utilisateur plus expérimenté en Python peut utiliser
un [`virtualenv`](https://virtualenv.readthedocs.org/en/latest/) s'il le souhaite.

## Démarrer le serveur

```
calculette-impots web-api
```

Ou en exécutant directement le script :

``
python3 calculette_impots_web_api/scripts/serve.py
``

Puis ouvrir l'URL http://localhost:5000/.
En réalité cette URL ne sert à rien en l'état et il faut appeler un point d'entrée,
et c'est l'objet de la section suivante.

## Utilisation

L'API web peut être appelée depuis le navigateur, depuis un outil en ligne de commande comme
[`curl`](https://curl.haxx.se/) ou bien depuis le langage JavaScript via une requête AJAX.

L'API fournit différents points d'entrée :

### `/api/1/calculate` : calculer un cas-type

Exemple :
http://localhost:5000/api/1/calculate?saisies={%22V_ANREV%22:2014,%22TSHALLOV%22:30000,%22V_0DA%22:1980}

> Les ``%22` représentent des guillemets (`"`) url-encodés.

### `/api/1/variables` : lister toutes les variables connues

Exemple :
http://localhost:5000/api/1/variables

> Attention : comme beaucoup de données sont renvoyées par le serveur, votre navigateur peut avoir du mal à tout afficher.

### `/api/1/variables/<name>` : afficher les informations sur une variable

Exemple :
http://localhost:5000/api/1/variable/TSHALLOV

## Cas-types

Voir les cas-types documentés dans le projet [calculette-impots-python](https://git.framasoft.org/openfisca/calculette-impots-python).

## Qualité du code

```
flake8 --max-line-length 120 .
```
