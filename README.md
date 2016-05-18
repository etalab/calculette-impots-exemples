# Optimisation du calcul des impôts

https://forum.openfisca.fr/t/optimisation-du-temps-de-calcul/78

## Arbre du projet

* dossier `graph` : représentation des graphes obtenus en graphml
* dossier `json` : résultats de calculs
* dossier `notebooks` : code sous la forme de notebooks
* dossier `src` : code sous la forme de .py, parfois utilisé dans les notebooks


## Exécuter le code sur son poste

Le fichier `config.ini.example` doit être copié en `config.ini` et modifier pour correspondre à l'environnement.

Le code est largement expérimental. Des erreurs peuvent survenir en raison de changements apportés au code ou d'un environnement différent. Ne pas hésiter à contacter les auteurs.


## Simplification de l'AST

Le fichier `simplify_ast.py` prend en entrée l'AST du projet openfisca/calculette-impots-m-language-parser et le simplifie pour ne garder que 3 types de noeuds :
* contantes
* variables
* appels de fonction

Les résultats sont enregistrés dans les fichiers suivants :
* formulas.json : Formule des variables
* constants.json : Constantes
* input_variables.json : Variables en entrée, avec leur `name` (référencé dans les formules) et leur `alias` (référencé dans le formulaire 2042).


## Etude du graphe de quelques variables importantes

* Calcul des dépendances d'une dizaine de variables
* Vérification que le graphe est bien acyclique
* Détermination d'une ordre tel que qu'un variable ne dépend que de variables d'index inférieur.

Fichiers de sortie :
* formulas_light.json : formules des variables utilisées dans le calcul
* constants_light.json : constantes utilisées par le calcul
* inputs_light.json : variables d'entrée utilisées dans le calcul
* children_light.json : Dépendances directes pour chaque variables utilisée dans le calcul
* unknowns_light.json : variables utilisées dans le calcul mais que ne sont pas définies dans le code m.
* computing_order.json : ordre d'exécution non récursif

## Calculs

Un "moteur d'execution" permet d'exécuter un calcul sur l'arbre des formules, et en appliquant les 20 opérations du langages m. Les moteurs d'exécution sont assez semblables mais ces 20 fonctions peuvent avoir des implémentation très différentes :
* `function_set_std` définit une implémentation non vectorielle
* `function_set_np.py` définit une implémentation vectorielle du calcul
* le notebook  `compute_tf` contient une implémentation pour tensorflow.
* voir le repo `calculette-impots-javascript` pour une implémentation en javascript

## Simplification du graphe

Environ 200 variables 'communes' sont sélectionées et les autres sont supposées nulle. Cette situation est censée correspondre à la plupart des situations fiscales. Le graphe de calcul est pré-calculé et les nœuds qui ne dépendent plus de variables d'entrée sont éliminés. Le graphe simplifié contrient 1658 nœuds de type formule.
