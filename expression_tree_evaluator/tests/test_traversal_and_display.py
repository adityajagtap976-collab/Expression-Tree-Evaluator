from expression_tree_evaluator.display import render_tree
from expression_tree_evaluator.infix_to_postfix import infix_to_postfix
from expression_tree_evaluator.tokenizer import tokenize
from expression_tree_evaluator.traversal import (
    inorder_with_parentheses,
    postorder,
    preorder,
)
from expression_tree_evaluator.tree import build_expression_tree


def build(expression: str):
    return build_expression_tree(infix_to_postfix(tokenize(expression)))


def test_preorder():
    tree = build("3 + 4 * 2")
    assert preorder(tree) == ["+", "3", "*", "4", "2"]


def test_postorder_matches_original_postfix_input():
    tree = build("3 + 4 * 2")
    assert postorder(tree) == ["3", "4", "2", "*", "+"]


def test_inorder_reconstructs_unambiguous_expression():
    tree = build("3 + 4 * 2")
    assert inorder_with_parentheses(tree) == "(3 + (4 * 2))"


def test_render_tree_contains_every_node_value():
    tree = build("(3 + 4) * 2")
    diagram = render_tree(tree)
    for expected_value in ("*", "+", "3", "4", "2"):
        assert expected_value in diagram
