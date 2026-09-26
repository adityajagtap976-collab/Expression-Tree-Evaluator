import pytest

from expression_tree_evaluator.exceptions import (
    InvalidTokenError,
    MismatchedParenthesesError,
)
from expression_tree_evaluator.infix_to_postfix import infix_to_postfix
from expression_tree_evaluator.tokenizer import tokenize


def convert(expression: str) -> list[str]:
    return infix_to_postfix(tokenize(expression))


def test_simple_addition():
    assert convert("3 + 4") == ["3", "4", "+"]


def test_precedence_multiplication_before_addition():
    assert convert("3 + 4 * 2") == ["3", "4", "2", "*", "+"]


def test_parentheses_override_precedence():
    assert convert("(3 + 4) * 2") == ["3", "4", "+", "2", "*"]


def test_left_associativity_of_subtraction():
    # 10 - 3 - 2 must mean (10 - 3) - 2, not 10 - (3 - 2)
    assert convert("10 - 3 - 2") == ["10", "3", "-", "2", "-"]


def test_right_associativity_of_exponent():
    # 2 ^ 3 ^ 2 must mean 2 ^ (3 ^ 2), so 3 and 2 combine before the
    # outer 2 does.
    assert convert("2 ^ 3 ^ 2") == ["2", "3", "2", "^", "^"]


def test_unmatched_closing_paren():
    with pytest.raises(MismatchedParenthesesError):
        convert("3 + 4)")


def test_unmatched_opening_paren():
    with pytest.raises(MismatchedParenthesesError):
        convert("(3 + 4")


def test_rejects_unknown_token_symbol():
    with pytest.raises(InvalidTokenError):
        infix_to_postfix(["3", "%", "4"])
