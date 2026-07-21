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


# Power is a native Unity node — use `Power(base, exponent)` from nodes / `from AIGamePyLibrary import *`.
# Kept as a re-export so older `from AIGamePyLibrary.customNodes import Power` imports still work.
