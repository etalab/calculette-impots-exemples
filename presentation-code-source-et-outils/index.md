class: middle, center

# Calculette impôts

## Code source et outils

---

# Code source de la calculette impôts

https://git.framasoft.org/openfisca/calculette-impots-m-source-code

Des [règles](https://git.framasoft.org/openfisca/calculette-impots-m-source-code/blob/master/src/chap-2.m#L50) :
```
regle isf 201050:
application : batch, iliad ;
ISF4BASE = ISF4BIS * positif_ou_nul(ISF4BIS - SEUIL_12);  
ISFIN = ISF4BASE ;
```

Et un glossaire des variables (fichier [tgvH.m](https://git.framasoft.org/openfisca/calculette-impots-m-source-code/blob/master/src/tgvH.m)) :
```
ISF4BASE : calculee : "base des penalites en ISF" ;
ISF4BIS : calculee restituee : "Net a payer ISF avec contribution exceptionnelle" ;
ISFIN : calculee restituee : "IMPOT ISF SERVANT AU CALCUL BASES DES MAJOS 1728 ET INR" ;
SEUIL_12 : const=12.00000  ;
```
