"""Binary expression tree: the node definition and the stack-based
builder that turns a postfix token list into a tree.
"""

from dataclasses import dataclass
from typing import Optional

from .exceptions import InvalidExpressionError
from .tokenizer import is_number_token


@dataclass
class TreeNode:
    """A single node in the expression tree.

    Leaf nodes hold a number (as a string, e.g. "3.5") and have no
    children. Internal nodes hold an operator ("+", "-", "*", "/",
    "^") and always have exactly two children.
    """

    value: str
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


def build_expression_tree(postfix_tokens: list[str]) -> TreeNode:
    """Build a binary expression tree from a postfix token list.

    Classic algorithm: scan postfix left to right, push numbers onto
    a stack of tree nodes, and whenever an operator is seen, pop its
    two operands off the stack, make them the operator's children,
    and push the new subtree back on.
    """
    if not postfix_tokens:
        raise InvalidExpressionError("Cannot build a tree from an empty expression")

    node_stack: list[TreeNode] = []

    for token in postfix_tokens:
        if is_number_token(token):
            node_stack.append(TreeNode(token))
        else:
            if len(node_stack) < 2:
                raise InvalidExpressionError(
                    f"Operator '{token}' is missing operand(s) -- "
                    "check your expression for a missing number"
                )
            right_child = node_stack.pop()
            left_child = node_stack.pop()
            node_stack.append(TreeNode(token, left_child, right_child))

    if len(node_stack) != 1:
        raise InvalidExpressionError(
            "Expression has leftover values with no operator to combine them "
            "-- check for a missing operator"
        )

    return node_stack.pop()
