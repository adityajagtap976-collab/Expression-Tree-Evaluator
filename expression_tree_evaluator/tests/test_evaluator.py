import pytest

from expression_tree_evaluator.evaluator import evaluate
from expression_tree_evaluator.exceptions import DivisionByZeroError
from expression_tree_evaluator.infix_to_postfix import infix_to_postfix
from expression_tree_evaluator.tokenizer import tokenize
from expression_tree_evaluator.tree import build_expression_tree


def run(expression: str) -> float:
    tokens = tokenize(expression)
    postfix = infix_to_postfix(tokens)
    tree = build_expression_tree(postfix)
    return evaluate(tree)


def test_addition():
    assert run("3 + 4") == 7.0


def test_precedence():
    assert run("3 + 4 * 2") == 11.0


def test_parentheses_change_result():
    assert run("(3 + 4) * 2") == 14.0


def test_exponent_right_associative_value():
    # 2 ^ 3 ^ 2 == 2 ^ (3 ^ 2) == 2 ^ 9 == 512, NOT (2^3)^2 == 64
    assert run("2 ^ 3 ^ 2") == 512.0


def test_division():
    assert run("10 / 4") == 2.5


def test_division_by_zero_raises():
    with pytest.raises(DivisionByZeroError):
        run("5 / (1 - 1)")


def test_complex_expression_from_readme_example():
    # (3 + 4) * 2 - 5 / (1 + 1) == 14 - 2.5 == 11.5
    assert run("(3 + 4) * 2 - 5 / (1 + 1)") == 11.5
