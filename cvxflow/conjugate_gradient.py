"""Solve a linear system with conjugate gradient."""

import tensorflow as tf

from cvxflow.tf_util import dot

def conjugate_gradient_solve(A, b, x_init, tol=1e-12, name=None):
    """Solve linear equation `A x = b`, using conjugate gradient."""

    with tf.op_scope([A, b, x_init], name, "conjugate_gradient_solve"):
        def body(x, k, r_norm_sq, r, p):
            Ap = A(p)
            alpha = r_norm_sq / dot(p, Ap)
            x = x + alpha*p
            r = r - alpha*Ap
            r_norm_sq_prev = r_norm_sq
            r_norm_sq = dot(r, r)
            beta = r_norm_sq / r_norm_sq_prev
            p = r + beta*p
            return (x, k+1, r_norm_sq, r, p)

        def cond(x, k, r_norm_sq, r, p):
            return r_norm_sq > tol

        r = b - A(x_init)
        loop_vars = (x_init, tf.constant(0), dot(r, r), r, r)
        return tf.while_loop(cond, body, loop_vars)[:3]
