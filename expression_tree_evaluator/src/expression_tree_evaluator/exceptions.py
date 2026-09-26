"""Custom exceptions for the expression tree evaluator.

Keeping these separate from generic Python exceptions (ValueError,
ZeroDivisionError, etc.) is deliberate: it lets the CLI layer catch
*only* the errors that come from malformed user input, and treat any
other exception as a real bug in the program rather than bad input.
"""


class ExpressionError(Exception):
    """Base class for every error this package raises on bad input."""


class InvalidTokenError(ExpressionError):
    """Raised when the input contains a character that isn't a digit,
    a decimal point, an operator (+ - * / ^), or a parenthesis."""


class MismatchedParenthesesError(ExpressionError):
    """Raised when parentheses in the input don't balance."""


class InvalidExpressionError(ExpressionError):
    """Raised when the token stream doesn't form a valid expression
    (e.g. an operator with too few operands, or leftover operands)."""


class DivisionByZeroError(ExpressionError):
    """Raised when evaluating the tree would divide by zero."""
