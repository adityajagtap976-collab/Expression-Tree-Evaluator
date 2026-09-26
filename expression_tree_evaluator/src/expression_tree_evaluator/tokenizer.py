"""Turns a raw infix expression string into a list of tokens.

Scope note: this tokenizer accepts non-negative integers and decimals,
the four basic arithmetic operators, '^' for exponentiation, and
parentheses. It does NOT support unary minus (e.g. "-5 + 3") or
variables. That's a deliberate scope cut, not an oversight -- see
README "Known Limitations".
"""

import re

from .exceptions import InvalidTokenError

OPERATORS = set("+-*/^")
PARENTHESES = set("()")

# A valid number token is digits, optionally with a single decimal
# point (leading or trailing digits allowed, e.g. "3", "3.5", ".5",
# "5."). Anything else is not a number, even if it isn't an operator
# or parenthesis either -- that case is an invalid token, not a
# number, and callers must not assume otherwise.
_NUMBER_PATTERN = re.compile(r"^(\d+\.\d+|\d+\.|\.\d+|\d+)$")


def tokenize(expression: str) -> list[str]:
    """Convert an infix expression string into a list of string tokens.

    Numbers (including decimals like "3.14") are kept as single tokens.
    Each operator and parenthesis is its own token. Whitespace is
    ignored. Raises InvalidTokenError on any other character.
    """
    tokens: list[str] = []
    position = 0
    length = len(expression)

    while position < length:
        char = expression[position]

        if char.isspace():
            position += 1
            continue

        if char.isdigit() or char == ".":
            start = position
            seen_decimal_point = False
            while position < length and (
                expression[position].isdigit()
                or (expression[position] == "." and not seen_decimal_point)
            ):
                if expression[position] == ".":
                    seen_decimal_point = True
                position += 1
            number_text = expression[start:position]
            if not _NUMBER_PATTERN.match(number_text):
                raise InvalidTokenError(
                    f"Invalid number '{number_text}' at position {start}"
                )
            # Catch "3..5": the scan above stops cleanly after "3."
            # because a second decimal point isn't allowed, but the
            # leftover ".5" would otherwise be re-scanned as its own
            # valid-looking number token with no operator between
            # them. That's not two numbers, it's one malformed one.
            if position < length and (
                expression[position].isdigit() or expression[position] == "."
            ):
                raise InvalidTokenError(
                    f"Invalid number format starting at position {start}"
                )
            tokens.append(number_text)
            continue

        if char in OPERATORS or char in PARENTHESES:
            tokens.append(char)
            position += 1
            continue

        raise InvalidTokenError(
            f"Invalid character '{char}' at position {position}"
        )

    return tokens


def is_number_token(token: str) -> bool:
    """True only if the token actually looks like a numeric literal.

    This must be a real check, not "anything that isn't an operator
    or parenthesis" -- otherwise a genuinely invalid symbol slips
    through tokenizing/parsing as if it were a number instead of
    being rejected.
    """
    return bool(_NUMBER_PATTERN.match(token))
