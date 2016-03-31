# Calculette Impôts - API Web

Ce logiciel est installé sur un serveur public et est accessible via l'URL http://api.ir.openfisca.fr/.
Il n'est donc pas nécessaire de l'installer sur votre ordinateur à moins que vous ne souhaitiez travailler sur son
code source.

## Utilisation

L'API web peut être appelée depuis le navigateur, depuis un outil en ligne de commande comme
[`curl`](https://curl.haxx.se/) ou bien depuis le langage JavaScript via une requête AJAX.

L'API fournit différents points d'entrée :

### `/api/1/calculate`

Calculer un cas-type.

Paramètres :

- `saisies` est un paramètre GET qui contient un objet JSON dont les clés sont des noms de variables saisies
  (ou des aliases)
- `calculee` est un paramètre GET multi-valué qui donne le nom des variables à calculer

Exemples :
- http://api.ir.openfisca.fr/api/1/calculate?saisies={%22V_ANREV%22:2014,%22TSHALLOV%22:30000,%22V_0DA%22:1980}
- http://api.ir.openfisca.fr/api/1/calculate?calculee=IRN&calculee=IDRS2&saisies={%22V_ANREV%22:2014,%221AJ%22:30000,%22V_0DA%22:1980}

> Les ``%22` représentent des guillemets (`"`) url-encodés.

### `/api/1/variables`

Lister toutes les variables connues.

Exemple :
http://api.ir.openfisca.fr/api/1/variables

> Attention : comme beaucoup de données sont renvoyées par le serveur, votre navigateur peut avoir du mal à tout afficher.

### `/api/1/variables/<variable_name_or_alias>`

Afficher les informations sur une variable

- `variable_name_or_alias` peut être un nom de variable saisie ou un alias

Exemples :
- http://api.ir.openfisca.fr/api/1/variable/TSHALLOV
- http://api.ir.openfisca.fr/api/1/variable/1AJ

Si un alias est utilisé, une redirection HTTP est effectuée vers l'URL avec le nom de la variable de saisie.

## Cas-types

Voir les cas-types documentés dans le projet [calculette-impots-python](https://git.framasoft.org/openfisca/calculette-impots-python).

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
En réalité cette URL ne sert à rien en l'état et il faut appeler un point d'entrée.

## Qualité du code

```
flake8 --max-line-length 120 .
```
