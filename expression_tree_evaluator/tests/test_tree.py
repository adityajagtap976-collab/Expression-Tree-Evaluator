import pytest

from expression_tree_evaluator.exceptions import InvalidExpressionError
from expression_tree_evaluator.tree import build_expression_tree


def test_single_number_is_a_leaf():
    tree = build_expression_tree(["5"])
    assert tree.value == "5"
    assert tree.is_leaf()


def test_simple_addition_tree_shape():
    tree = build_expression_tree(["3", "4", "+"])
    assert tree.value == "+"
    assert tree.left.value == "3"
    assert tree.right.value == "4"


def test_nested_tree_shape():
    # postfix for (3 + 4) * 2
    tree = build_expression_tree(["3", "4", "+", "2", "*"])
    assert tree.value == "*"
    assert tree.left.value == "+"
    assert tree.left.left.value == "3"
    assert tree.left.right.value == "4"
    assert tree.right.value == "2"


def test_rejects_empty_postfix():
    with pytest.raises(InvalidExpressionError):
        build_expression_tree([])


def test_rejects_operator_with_missing_operand():
    with pytest.raises(InvalidExpressionError):
        build_expression_tree(["3", "+"])


def test_rejects_leftover_operands():
    with pytest.raises(InvalidExpressionError):
        build_expression_tree(["3", "4"])
