import numpy as np
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) + '/config.ini')

def get_functions_mapping(n):

    def produit(l):
        accu = np.ones(n)
        for e in l:
            accu *= e
        return accu

    def dans(l):
        accu = np.zeros(n)
        for i in range(1, len(l)):
            accu += (l[0] == l[i])
        return (accu != 0).astype(np.float)

    def boolean_or(l):
        accu = np.zeros(n)
        for e in l:
            accu += (e != 0)
        return (accu != 0).astype(np.float)

    def boolean_et(l):
        accu = np.ones(n)
        for e in l:
            accu *= (e != 0)
        return accu

    def plus(l):
        accu = np.zeros(n)
        for e in l:
            accu += e
        return accu

    def moins(l):
        return -l[0]

    def positif(l):
        return (l[0] > 0).astype(np.float)

    def positif_ou_nul(l):
        return (l[0] >= 0).astype(np.float)

    def nul(l):
        return (l[0] == 0).astype(np.float)

    def non_nul(l):
        return (l[0] != 0).astype(np.float)

    def superieur_ou_egal(l):
        return (l[0] >= l[1]).astype(np.float)

    def egal(l):
        return (l[0] == l[1]).astype(np.float)

    def ternaire(l):
        condition = (l[0]!=0).astype(np.float)
        return (l[1]*condition) + (l[2] * (1 - condition))

    def si(l):
        condition = (l[0]!=0).astype(np.float)
        return (l[1]*condition)

    def inverse(l):
        denominateur_nul = (l[0] == 0)
        denominateur = l[0] + denominateur_nul
        return (1 / denominateur) * (1 - denominateur_nul)

    def maximum(l):
        accu = l[0]
        for i in range(1, len(l)):
            accu = np.maximum(accu, l[i])
        return accu

    def minimum(l):
        accu = l[0]
        for i in range(1, len(l)):
            accu = np.minimum(accu, l[i])
        return accu

    def plancher(l):
        return np.floor(l[0])

    def arrondi(l):
        return np.around(l[0])

    def absolue(l):
        return np.absolute(l[0])

    functions_mapping = {
        '+': plus,
        '*': produit,
        '-': moins,
        'positif': positif,
        'positif_ou_nul': positif_ou_nul,
        'null': nul,
        'operator:>=': superieur_ou_egal,
        'operator:=': egal,
        'ternary': ternaire,
        'si': si,
        'inverse': inverse,
        'max': maximum,
        'min': minimum,
        'inf': plancher,
        'arr': arrondi,
        'abs': absolue,
        'present': non_nul,
        'boolean:ou': boolean_or,
        'boolean:et': boolean_et,
        'dans': dans
    }

    return functions_mapping
