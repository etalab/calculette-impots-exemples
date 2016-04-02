import math

def product(l):
    accu = 1.
    for e in l:
        accu *= e
    return accu

def boolean_or(l):
    for e in l:
        if l:
            return 1.
    return 0.

def boolean_et(l):
    for e in l:
        if not l:
            return 0.
    return 1.

functions_mapping = {
    '+': sum,
    '*': product,
    '-': (lambda x: -x[0]),
    'unary:-': (lambda x: -x[0]),
    'positif': (lambda x: float(x[0]>0)),
    'positif_ou_nul': (lambda x: float(x[0]>=0)),
    'null': (lambda x: float(x[0]==0)),
    'operator:>=': (lambda x: float(x[0]>=x[1])),
    'operator:>': (lambda x: float(x[0]>x[1])),
    'operator:<': (lambda x: float(x[0]<x[1])),
    'operator:=': (lambda x: float(x[0]==x[1])),
    'ternary': (lambda x: x[1] if x[0] else x[2]),
    'si': (lambda x: x[1] if x[0] else 0.),
    'inverse': (lambda x: 1/x[0] if x[0] else 0.),
    'max': max,
    'min': min,
    'inf': (lambda x: math.floor(x[0])),
    'arr': (lambda x: round(x[0])),
    'abs': (lambda x: abs(x[0])),
    'present': (lambda x: x[0] != 0.),
    'boolean:ou': boolean_or,
    'boolean:et': boolean_et,
    'dans': (lambda x: 1. if (x[0] in x[1:]) else 0.)
}
