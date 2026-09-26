"""Infix -> postfix conversion using the shunting-yard algorithm.

This is the "stack" half of the project: a single stack of operators
is used to reorder tokens from infix notation (the way humans write
expressions) into postfix / Reverse Polish Notation (the way the tree
builder below wants to consume them).
"""

from .exceptions import InvalidTokenError, MismatchedParenthesesError
from .tokenizer import is_number_token

# Higher number = binds tighter.
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}

# '^' is right-associative (2^3^2 == 2^(3^2) == 512), everything else
# here is left-associative.
RIGHT_ASSOCIATIVE_OPERATORS = {"^"}


def infix_to_postfix(tokens: list[str]) -> list[str]:
    """Convert a list of infix tokens into postfix order.

    Raises MismatchedParenthesesError if parentheses don't balance,
    InvalidTokenError if a token isn't a number, a known operator, or
    a parenthesis.
    """
    output: list[str] = []
    operator_stack: list[str] = []

    for token in tokens:
        if is_number_token(token):
            output.append(token)

        elif token == "(":
            operator_stack.append(token)

        elif token == ")":
            found_matching_paren = False
            while operator_stack:
                top = operator_stack.pop()
                if top == "(":
                    found_matching_paren = True
                    break
                output.append(top)
            if not found_matching_paren:
                raise MismatchedParenthesesError(
                    "Unmatched closing parenthesis ')'"
                )

        elif token in PRECEDENCE:
            while operator_stack and operator_stack[-1] != "(":
                top = operator_stack[-1]
                top_precedence = PRECEDENCE[top]
                current_precedence = PRECEDENCE[token]
                if top_precedence > current_precedence or (
                    top_precedence == current_precedence
                    and token not in RIGHT_ASSOCIATIVE_OPERATORS
                ):
                    output.append(operator_stack.pop())
                else:
                    break
            operator_stack.append(token)

        else:
            raise InvalidTokenError(f"Unexpected token '{token}'")

    while operator_stack:
        top = operator_stack.pop()
        if top == "(":
            raise MismatchedParenthesesError("Unmatched opening parenthesis '('")
        output.append(top)

    return output
