from log_info import log_info
from write_latex_stream import write_latex_stream


def stream_code(latex_stream, node, depth):
    """Stream a <code> element and return the next node."""

    # Local module imports to avoid circular dependencies
    from stream_single_node import stream_single_node

    log_info(f"{chr(32) * depth}code")
    write_latex_stream(latex_stream, f"\\texttt{{")
    for child_node in node.children:
        stream_single_node(latex_stream, child_node, depth)
    write_latex_stream(latex_stream, f"}}")
    # Return the next node
    return node.next_sibling
