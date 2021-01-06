from write_latex_stream import write_latex_stream
from log_info import log_info
from get_first_child import get_first_child


def stream_link(latex_stream, node, depth):
    """Stream a <ac:link> element and return the next node."""

    # Local module imports to avoid circular dependencies
    from stream_single_node import stream_single_node

    log_info(f"{chr(32) * depth}link: {str(node)[:64]}(...)")
    write_latex_stream(latex_stream, f"(link)")
    child_nodes = []
    child_node = get_first_child(node)
    while child_node:
        child_nodes.append(child_node)
        child_node = child_node.next_sibling
    for i in range(len(child_nodes)):
        child_node = child_nodes[i]
        log_info(f"{chr(32) * depth}link child: {str(child_node)[:64]}(...)")
        stream_single_node(latex_stream, child_node, depth)
    # Return the next node
    return node.next_sibling
