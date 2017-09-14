# calculatrice-impots-exemples

Ce repository contient plusieurs applications basées sur la calculatrice M de l'impôt sur le revenu.

## Dossiers

* dossier `calculette_impots_exemples` : implémentations en python de la calculatrice
* dossier `graph` : représentation des graphes obtenus en graphml (actuellement non maintenu)
* dossier `json` : résultats intermédiaires de calculs (actuellement non maintenu)
* dossier `notebooks` : exemples d'applications sous la forme de notebooks jupyter


## Exécuter le code sur son poste

Il est nécessaire d'installer la dépendance [`calculette-impots-m-language-parser`](https://github.com/etalab/calculette-impots-m-language-parser).

Ce paquet n'est pas publié sur le dépôt [PyPI](https://pypi.python.org/pypi) donc pour l'installer il faut passer par `git clone`. 
```
git clone https://github.com/etalab/calculette-impots-exemples.git
cd calculette-impots-exemples
pip3 install --editable . --user
```

> L'option `--user` sert sur les systèmes GNU/Linux.

> Pour les utilisateurs expérimentés, il est préférable d'utiliser un environnement virtuel. Voir par exemples [pew](https://github.com/berdario/pew).

Après le lancement du serveur jupyter notebook (exécuter la commande `jupyter notebook`), les notebook sont accessible par le navigateur, par exemple `http://localhost:8888/notebooks/notebooks/diachronie.ipynb`

## Calculs

Un "moteur d'execution" permet d'exécuter un calcul sur l'arbre des formules, et en appliquant les 20 opérations du langages m. Les moteurs d'exécution sont assez semblables mais ces 20 fonctions peuvent avoir des implémentations différentes :
* `function_set_scalaire` définit une implémentation non vectorielle
* `function_set_numpy.py` définit une implémentation vectorielle du calcul
* `function_set_gpu.py` définit une implémentation pour tensorflow, permettant d'utiliser une carte graphique.

Le notebook `exemples.ipynb` donne un exemple d'utilisation de chaque moteur d'exécution.

Le notebook `diachronie.ipynb` donne des exemples d'utilisation basés sur les différentes années d'imposition.

Les résultats peuvent être comparés au simulateur en ligne pis à disposition par la DGFiP : `http://www3.finances.gouv.fr/calcul_impot/XXXX/index.htm` où `XXXX` est l'année de l'imposition.

## Etude du graphe de quelques variables importantes (actuellement non maintenu)

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


## Simplification du graphe (actuellement non maintenu)

Environ 200 variables 'communes' sont sélectionées et les autres sont supposées nulle. Cette situation est censée correspondre à la plupart des situations fiscales. Le graphe de calcul est pré-calculé et les nœuds qui ne dépendent plus de variables d'entrée sont éliminés. Le graphe simplifié contrient 1658 nœuds de type formule.


## Licences

Les fichiers (json ou autre) dérivés du code M sont soumis à la licence CeCILL v2.1.

Les autres codes sources sont soumis à la licence MIT.
