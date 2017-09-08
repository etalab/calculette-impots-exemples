import numpy as np


def get_functions_mapping(n):

    def produit(operands):
        accu = np.ones(n)
        for e in operands:
            accu *= e
        return accu

    def dans(operands):
        accu = np.zeros(n)
        for i in range(1, len(operands)):
            accu += (operands[0] == operands[i])
        return (accu != 0).astype(np.float)

    def boolean_or(operands):
        accu = np.zeros(n)
        for e in operands:
            accu += (e != 0)
        return (accu != 0).astype(np.float)

    def boolean_et(operands):
        accu = np.ones(n)
        for e in operands:
            accu *= (e != 0)
        return accu

    def plus(operands):
        accu = np.zeros(n)
        for e in operands:
            accu += e
        return accu

    def moins(operands):
        return -operands[0]

    def positif(operands):
        return (operands[0] > 0).astype(np.float)

    def positif_ou_nul(operands):
        return (operands[0] >= 0).astype(np.float)

    def nul(operands):
        return (operands[0] == 0).astype(np.float)

    def non_nul(operands):
        return (operands[0] != 0).astype(np.float)

    def superieur_ou_egal(operands):
        return (operands[0] >= operands[1]).astype(np.float)

    def inferieur_ou_egal(operands):
        return (operands[0] <= operands[1]).astype(np.float)

    def superieur_strictement(operands):
        return (operands[0] > operands[1]).astype(np.float)

    def inferieur_strictement(operands):
        return (operands[0] < operands[1]).astype(np.float)

    def egal(operands):
        return (operands[0] == operands[1]).astype(np.float)

    def ternaire(operands):
        condition = (operands[0]!=0).astype(np.float)
        return (operands[1]*condition) + (operands[2] * (1 - condition))

    def si(operands):
        condition = (operands[0]!=0).astype(np.float)
        return (operands[1]*condition)

    def invert(operands):
        denominateur_nul = (operands[0] == 0)
        denominateur = operands[0] + denominateur_nul
        return (1 / denominateur) * (1 - denominateur_nul)

    def maximum(operands):
        accu = operands[0]
        for i in range(1, len(operands)):
            accu = np.maximum(accu, operands[i])
        return accu

    def minimum(operands):
        accu = operands[0]
        for i in range(1, len(operands)):
            accu = np.minimum(accu, operands[i])
        return accu

    def plancher(operands):
        return np.floor(operands[0])

    def arrondi(operands):
        return np.around(operands[0])

    def absolue(operands):
        return np.absolute(operands[0])

    functions_mapping = {
        'sum': plus,
        'product': produit,
        'negate': moins,
        'unary:-': moins,
        'positif': positif,
        'positif_ou_nul': positif_ou_nul,
        'null': nul,
        'operator:>=': superieur_ou_egal,
        'operator:<=': inferieur_ou_egal,
        'operator:>': superieur_strictement,
        'operator:<': inferieur_strictement,
        'operator:=': egal,
        'ternary': ternaire,
        'si': si,
        'invert': invert,
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
