"""Explicit preorder / inorder / postorder traversals of the
expression tree.

`evaluator.py` already does a post-order traversal internally, but
these are kept separate and exposed on their own because "traversals"
is a named part of the syllabus this project is meant to demonstrate,
and because `inorder_with_parentheses` doubles as a correctness check:
it reconstructs a fully-parenthesized infix expression from the tree,
which should always evaluate to the same result as the tree itself.
"""

from .tree import TreeNode


def preorder(node: TreeNode) -> list[str]:
    """Root, then left subtree, then right subtree."""
    if node.is_leaf():
        return [node.value]
    return [node.value] + preorder(node.left) + preorder(node.right)


def postorder(node: TreeNode) -> list[str]:
    """Left subtree, then right subtree, then root."""
    if node.is_leaf():
        return [node.value]
    return postorder(node.left) + postorder(node.right) + [node.value]


def inorder_with_parentheses(node: TreeNode) -> str:
    """Left subtree, root, right subtree -- with parentheses added
    around every operator so the result is unambiguous, e.g. the tree
    for "3 + 4 * 2" renders as "(3 + (4 * 2))".
    """
    if node.is_leaf():
        return node.value
    left_text = inorder_with_parentheses(node.left)
    right_text = inorder_with_parentheses(node.right)
    return f"({left_text} {node.value} {right_text})"
