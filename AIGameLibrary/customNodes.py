from .nodes import *


def QuadraticFormula(a: Node, b: Node, c: Node):
    """
    Returns:
        tuple:
        - Solution exists: Bool Node
        - First solution (+): Float Node
        - Second solution (-): Float Node
    """
    d = b**2 - 4 * a * c
    sqrtD = Sqrt(d)
    root1 = (-b + sqrtD) / (2 * a)
    root2 = (-b - sqrtD) / (2 * a)
    return d >= 0, root1, root2


def Power(node0: Node, node1: Node):
    """
    custom x^y node using x^y = e^(y*ln(x))
    """
    return Exp(node1 * Ln(node0))
