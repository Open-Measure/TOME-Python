from log_info import log_info
from get_first_child import get_first_child
from write_latex_stream import write_latex_stream


def stream_em(latex_stream, node, depth):
    """Stream a <em> element and return the next node."""

    # Local module imports to avoid circular dependencies
    from stream_single_node import stream_single_node

    log_info(f"{chr(32) * depth}em: {str(node)[:24]}(...)")
    write_latex_stream(latex_stream, f"\\emph{{")
    child_nodes = []
    child_node = get_first_child(node)
    while child_node:
        child_nodes.append(child_node)
        child_node = child_node.next_sibling
    for i in range(len(child_nodes)):
        child_node = child_nodes[i]
        log_info(f"{chr(32) * depth}em child: {str(child_node)[:64]}")
        stream_single_node(latex_stream, child_node, depth)
    write_latex_stream(latex_stream, f"}}")
    # Return the next node
    return node.next_sibling
