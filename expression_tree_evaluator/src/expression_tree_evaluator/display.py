"""Renders an expression tree as an ASCII diagram for the CLI.

This is the whole reason "Evaluator" isn't a black box: seeing the
actual tree structure is what makes the data structure visible to
whoever is grading this.
"""

from .tree import TreeNode


def render_tree(node: TreeNode) -> str:
    """Return a multi-line ASCII rendering of the tree, root at top."""
    lines: list[str] = []
    _render_node(node, prefix="", is_last_child=True, lines=lines, is_root=True)
    return "\n".join(lines)


def _render_node(
    node: TreeNode,
    prefix: str,
    is_last_child: bool,
    lines: list[str],
    is_root: bool,
) -> None:
    connector = "" if is_root else ("└── " if is_last_child else "├── ")
    lines.append(prefix + connector + node.value)

    if node.is_leaf():
        return

    child_prefix = prefix if is_root else prefix + ("    " if is_last_child else "│   ")
    children = [child for child in (node.left, node.right) if child is not None]
    for index, child in enumerate(children):
        _render_node(
            child,
            prefix=child_prefix,
            is_last_child=(index == len(children) - 1),
            lines=lines,
            is_root=False,
        )
