import numpy as np
import tensorflow as tf


def get_functions_mapping(n_batch):

    # Constants

    tf_constant_zero = tf.constant(np.zeros(n_batch), dtype=tf.float64)
    tf_constant_one = tf.constant(np.ones(n_batch), dtype=tf.float64)
    tf_constant_false = tf.constant(np.zeros(n_batch, dtype=np.bool))
    tf_constant_true = tf.constant(np.ones(n_batch, dtype=np.bool))

    def produit(operands):
        accu = tf_constant_one
        for i in range(len(operands)):
            accu = tf.multiply(accu, operands[i])
        return accu

    def dans(operands):
        accu = tf_constant_false
        for i in range(1, len(operands)):
            tmp = tf.equal(operands[0], operands[1])
            accu = tf.logical_or(accu, tmp)
        return tf.cast(accu, tf.float64)

    def boolean_or(operands):
        accu = tf_constant_false
        for i in range(len(operands)):
            tmp = tf.cast(operands[i], dtype=tf.bool)
            accu = tf.logical_or(accu, tmp)
        return tf.cast(accu, dtype=tf.float64)

    def boolean_et(operands):
        accu = tf_constant_true
        for i in range(len(operands)):
            tmp = tf.cast(operands[i], dtype=tf.bool)
            accu = tf.logical_and(accu, tmp)
        return tf.cast(accu, dtype=tf.float64)

    def plus(operands):
        return tf.add_n(operands)

    def moins(operands):
        return tf.negative(operands[0])

    def positif(operands):
        tmp = tf.greater(operands[0], tf_constant_zero)
        return tf.cast(tmp, dtype=tf.float64)

    def positif_ou_nul(operands):
        tmp = tf.greater_equal(operands[0], tf_constant_zero)
        return tf.cast(tmp, dtype=tf.float64)

    def nul(operands):
        tmp = tf.cast(operands[0], dtype=tf.bool)
        tmp = tf.logical_not(tmp)
        return tf.cast(tmp, dtype=tf.float64)

    def non_nul(operands):
        tmp = tf.cast(operands[0], dtype=tf.bool)
        return tf.cast(tmp, dtype=tf.float64)

    def superieur_ou_egal(operands):
        tmp = tf.greater_equal(operands[0], operands[1])
        return tf.cast(tmp, dtype=tf.float64)

    def superieur(operands):
        tmp = tf.greater(operands[0], operands[1])
        return tf.cast(tmp, dtype=tf.float64)

    def inferieur(operands):
        tmp = tf.greater(operands[1], operands[0])
        return tf.cast(tmp, dtype=tf.float64)

    def egal(operands):
        tmp = tf.equal(operands[0], operands[1])
        return tf.cast(tmp, dtype=tf.float64)

    def ternaire(operands):
        condition = tf.cast(operands[0], dtype=tf.bool)
        return tf.where(condition, operands[1], operands[2])

    def si(operands):
        condition = tf.cast(operands[0], dtype=tf.bool)
        return tf.where(condition, operands[1], tf_constant_zero)

    def invert(operands):
        inv = tf.reciprocal(operands[0])
        est_non_nul = tf.cast(operands[0], dtype=bool)
        return tf.where(est_non_nul, inv, tf_constant_zero)

    def maximum(operands):
        accu = operands[0]
        for i in range(1, len(operands)):
            accu = tf.maximum(accu, operands[i])
        return accu

    def minimum(operands):
        accu = operands[0]
        for i in range(1, len(operands)):
            accu = tf.minimum(accu, operands[i])
        return accu

    def plancher(operands):
        return tf.floor(operands[0])

    def arrondi(operands):
        return tf.round(operands[0])

    def absolue(operands):
        return np.abs(operands[0])


    functions_mapping = {
        'sum': plus,
        'product': produit,
        'negate': moins,
        'unary:-': moins,
        'positif': positif,
        'positif_ou_nul': positif_ou_nul,
        'null': nul,
        'operator:>=': superieur_ou_egal,
        'operator:>': superieur,
        'operator:<': inferieur,
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

    return functions_mapping, tf_constant_zero, tf_constant_one, tf_constant_false, tf_constant_true
