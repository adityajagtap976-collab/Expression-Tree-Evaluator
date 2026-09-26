"""The interactive CLI. Pure input() / print() -- no files, no
database, no network, no GUI. This is the only module that talks to
the terminal; every other module is a plain function library so it
can be unit tested without touching stdin/stdout.
"""

from .display import render_tree
from .evaluator import evaluate
from .exceptions import ExpressionError
from .infix_to_postfix import infix_to_postfix
from .traversal import inorder_with_parentheses
from .tree import build_expression_tree
from .tokenizer import tokenize

BANNER = """\
==================================================
 Expression Tree Evaluator
 Infix -> Postfix (stack) -> Binary Tree -> Result
==================================================
Enter an arithmetic expression using + - * / ^ and parentheses.
Examples:  (3 + 4) * 2        3 + 4 * 2       2 ^ 3 ^ 2
Type 'quit' or 'exit' to leave.
"""

EXIT_COMMANDS = {"quit", "exit"}


def evaluate_expression(expression: str) -> tuple[list[str], str, str, float]:
    """Run one expression through the full pipeline.

    Returns (postfix_tokens, tree_diagram, inorder_check, result).
    Raises ExpressionError subclasses on bad input -- the caller
    decides how to display those.
    """
    tokens = tokenize(expression)
    postfix_tokens = infix_to_postfix(tokens)
    tree_root = build_expression_tree(postfix_tokens)
    result = evaluate(tree_root)
    tree_diagram = render_tree(tree_root)
    inorder_check = inorder_with_parentheses(tree_root)
    return postfix_tokens, tree_diagram, inorder_check, result


def run() -> None:
    print(BANNER)
    while True:
        try:
            raw_input_text = input("expr> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not raw_input_text:
            continue
        if raw_input_text.lower() in EXIT_COMMANDS:
            print("Exiting.")
            break

        try:
            postfix_tokens, tree_diagram, inorder_check, result = evaluate_expression(
                raw_input_text
            )
        except ExpressionError as error:
            print(f"Error: {error}")
            continue

        print(f"Postfix          : {' '.join(postfix_tokens)}")
        print("Expression Tree  :")
        print(tree_diagram)
        print(f"Inorder check    : {inorder_check}")
        print(f"Result           : {result}")
        print()


def main() -> None:
    run()
