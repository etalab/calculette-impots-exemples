# Optimisation du temps de calcul

## Arbre du projet

* dossier `json`
  * résultas de calculs
  * src : scripts pythons
  * notebooks : notebooks jupyter pour executer interactivement du code python

## Simplification de l'AST

Le fichier `simplify_ast.py` prend en entrée l'AST du projet openfisca/calculette-impots-m-language-parser et le simplifie pour ne garder que 3 types de noeuds :
* contantes
* variables
* appels de fonction

Les résultats sont enregistrés dans les fichiers suivants :
* formulas.json : Formule des variables
* constants.json : Constantes
* input_variables.json : Variables en entrée, avec leur `name` (référencé dans les formules) et leur `alias` (référencé dans le formulaire 2042).


## Etude du graphe de la variable 'IRN'

* Calcul des dépendances de la variables 'IRN'
* Vérification que le graphe est bien acyclique
* Détermination d'une ordre tel que qu'un variable ne dépend que de variables d'index inférieur.

Fichiers de sortie :
* formulas_light.json : formules des variables utilisées dans le calcul de 'IRN'
* constants_light.json : constantes utilisées par le calcul de 'IRN'
* inputs_light.json : variables d'entrée utilisées dans le calcul de 'IRN'
* children_light.json : Dépendances directes pour chaque variables utilisée dans le calcul de 'IRN'
* unknowns_light.json : variables utilisées dans le calcul de 'IRN' mais que ne sont pas définies dans le code m.

## Execution

Un "moteur d'execution" permet d'exécuter un calcul sur l'arbre des formules, et en appliquant les 20 opérations du langages m. Les moteurs d'exécution sont assez semblables mais ces 20 fonctions peuvent avoir des implémentation très différentes :
* function_set_std définit une implémentation non vectorielle
* function_set_np.py définit une implémentation vectorielle du calcul
* le notebook compute_tf contient une implémentation pour tensorflow.
