"""Expression Tree Evaluator.

A CLI tool that converts an infix arithmetic expression to postfix
using a stack, builds a binary expression tree from that postfix
form, and evaluates it via recursive post-order traversal.
"""

from .cli import main
from .display import render_tree
from .evaluator import evaluate
from .exceptions import (
    DivisionByZeroError,
    ExpressionError,
    InvalidExpressionError,
    InvalidTokenError,
    MismatchedParenthesesError,
)
from .infix_to_postfix import infix_to_postfix
from .tokenizer import tokenize
from .traversal import inorder_with_parentheses, postorder, preorder
from .tree import TreeNode, build_expression_tree

__all__ = [
    "main",
    "tokenize",
    "infix_to_postfix",
    "build_expression_tree",
    "TreeNode",
    "evaluate",
    "render_tree",
    "preorder",
    "postorder",
    "inorder_with_parentheses",
    "ExpressionError",
    "InvalidTokenError",
    "MismatchedParenthesesError",
    "InvalidExpressionError",
    "DivisionByZeroError",
]

__version__ = "0.1.0"
