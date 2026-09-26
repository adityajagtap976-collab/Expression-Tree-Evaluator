# Expression Tree Evaluator

A CLI tool that takes an infix arithmetic expression, converts it to
postfix using a **stack**, builds a **binary expression tree** from
the postfix form, and evaluates it using **recursive post-order
traversal**. Every step of the pipeline is visible on screen: the
postfix form, an ASCII diagram of the tree, and an inorder
reconstruction used as a correctness check.

No database. No frontend. No files written to disk. Pure CLI,
pure data structures and algorithms.

## Why this project

Real DSA content, not a CRUD app wearing a costume: this is the same
technique used inside calculators and compiler parsers to turn
human-readable arithmetic into something a machine can walk and
evaluate directly. It demonstrates, on purpose:

- **Stack** — shunting-yard infix-to-postfix conversion
- **Binary tree** — building an expression tree from postfix
- **Recursion / traversals** — preorder, inorder, postorder, and
  post-order evaluation

## Installation

```bash
pip install -e ".[dev]"
```

## Usage

```bash
expression-tree-evaluator
```

```
expr> (3 + 4) * 2 - 5 / (1 + 1)
Postfix          : 3 4 + 2 * 5 1 1 + / -
Expression Tree  :
-
├── *
│   ├── +
│   │   ├── 3
│   │   └── 4
│   └── 2
└── /
    ├── 5
    └── +
        ├── 1
        └── 1
Inorder check    : (((3 + 4) * 2) - (5 / (1 + 1)))
Result           : 11.5
```

Type `quit` or `exit` to leave.

## Supported syntax

- Non-negative integers and decimals: `3`, `3.5`, `.5`
- Operators: `+  -  *  /  ^`
- Parentheses for grouping
- `^` is right-associative (`2 ^ 3 ^ 2` = `2 ^ (3 ^ 2)` = `512`, not `64`)

## Error handling

The tool explicitly detects and reports, without crashing:
- Mismatched parentheses (extra `(` or extra `)`)
- Division by zero
- Invalid characters/tokens
- Malformed expressions (missing operator or missing operand)

## Known limitations (deliberate scope cuts)

- **No unary minus / negative literals** (`-5 + 3` is not supported).
  Supporting it correctly would require either a separate unary-node
  type in the tree or a preprocessing pass that rewrites unary minus
  as `0 - x`, both of which add real complexity for a 2-day, solo,
  CLI-only project. Results can still be negative (e.g.
  `5 / (1 + 1) - 10` evaluates fine) — only negative *input literals*
  are unsupported.
- **No variables** (`x`, `y`). This is an expression evaluator, not a
  symbolic algebra system.
- **No functions** (`sin`, `sqrt`, etc.).

## Project structure

```
src/expression_tree_evaluator/
├── tokenizer.py          # string -> tokens
├── infix_to_postfix.py   # stack-based shunting-yard
├── tree.py                # TreeNode + stack-based tree builder
├── evaluator.py            # recursive post-order evaluation
├── traversal.py            # preorder / inorder / postorder
├── display.py               # ASCII tree rendering
├── cli.py                    # interactive menu loop (the only I/O module)
└── exceptions.py             # custom exception hierarchy
tests/                          # pytest suite, one file per module
```

## Running the tests

```bash
pip install -e ".[dev]"
pytest -v
```

32 tests covering: tokenizing, precedence, associativity (including
`^`'s right-associativity), tree shape, all four documented error
conditions, and traversal correctness.
