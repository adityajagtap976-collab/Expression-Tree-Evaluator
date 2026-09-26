"""Evaluates an expression tree via recursive post-order traversal:
evaluate the left subtree, evaluate the right subtree, then apply the
operator at the current node to those two results.
"""

import operator as operator_module

from .exceptions import DivisionByZeroError
from .tree import TreeNode

_BINARY_OPERATIONS = {
    "+": operator_module.add,
    "-": operator_module.sub,
    "*": operator_module.mul,
    "^": operator_module.pow,
}


def evaluate(node: TreeNode) -> float:
    """Recursively evaluate the expression tree rooted at `node`."""
    if node.is_leaf():
        return float(node.value)

    # Post-order: children first, then the operator at this node.
    left_value = evaluate(node.left)
    right_value = evaluate(node.right)

    if node.value == "/":
        if right_value == 0:
            raise DivisionByZeroError(
                f"Division by zero: {left_value} / {right_value}"
            )
        return left_value / right_value

    return _BINARY_OPERATIONS[node.value](left_value, right_value)
