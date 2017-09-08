import math

def product(operands):
    accu = 1.
    for e in operands:
        accu *= e
    return accu

def boolean_or(operands):
    for e in operands:
        if e:
            return 1.
    return 0.

def boolean_et(operands):
    for e in operands:
        if not operands:
            return 0.
    return 1.

functions_mapping = {
    'sum': sum,
    'product': product,
    'negate': (lambda x: -x[0]),
    'unary:-': (lambda x: -x[0]),
    'positif': (lambda x: float(x[0]>0)),
    'positif_ou_nul': (lambda x: float(x[0]>=0)),
    'null': (lambda x: float(x[0]==0)),
    'operator:>=': (lambda x: float(x[0]>=x[1])),
    'operator:<=': (lambda x: float(x[0]<=x[1])),
    'operator:>': (lambda x: float(x[0]>x[1])),
    'operator:<': (lambda x: float(x[0]<x[1])),
    'operator:=': (lambda x: float(x[0]==x[1])),
    'ternary': (lambda x: x[1] if x[0] else x[2]),
    'si': (lambda x: x[1] if x[0] else 0.),
    'invert': (lambda x: 1/x[0] if x[0] else 0.),
    'max': max,
    'min': min,
    'inf': (lambda x: float(math.floor(x[0]))),
    'arr': (lambda x: float(round(x[0]))),
    'abs': (lambda x: abs(x[0])),
    'present': (lambda x: float(x[0] != 0.)),
    'boolean:ou': boolean_or,
    'boolean:et': boolean_et,
    'dans': (lambda x: 1. if (x[0] in x[1:]) else 0.)
}
