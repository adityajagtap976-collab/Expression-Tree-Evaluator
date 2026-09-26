import pytest

from expression_tree_evaluator.exceptions import InvalidTokenError
from expression_tree_evaluator.tokenizer import tokenize


def test_simple_expression():
    assert tokenize("3 + 4") == ["3", "+", "4"]


def test_no_spaces():
    assert tokenize("3+4*2") == ["3", "+", "4", "*", "2"]


def test_decimals():
    assert tokenize("3.5 + 2.25") == ["3.5", "+", "2.25"]


def test_parentheses():
    assert tokenize("(3 + 4) * 2") == ["(", "3", "+", "4", ")", "*", "2"]


def test_exponent_operator():
    assert tokenize("2 ^ 3 ^ 2") == ["2", "^", "3", "^", "2"]


def test_rejects_invalid_character():
    with pytest.raises(InvalidTokenError):
        tokenize("3 + x")


def test_rejects_malformed_decimal():
    with pytest.raises(InvalidTokenError):
        tokenize("3..5 + 1")
