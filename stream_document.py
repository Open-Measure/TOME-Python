from log_info import log_info
from get_first_child import get_first_child


def stream_document(latex_stream, node, depth):
    """When Beautiful Soup parses an HTML fragment,
    by default it wraps it in a root tag named <[document]>.
    Thus. whenever we extract (e.g. adjacent) HTML fragments,
    we then need to first parse the parent <[document]>
    and only then can we parse its children."""

    # Local module imports to avoid circular dependencies
    from stream_single_node import stream_single_node

    log_info(f"{chr(32) * depth}[document]: {str(node)[:64]}(...)")
    child_nodes = []
    child_node = get_first_child(node)
    while child_node:
        child_nodes.append(child_node)
        child_node = child_node.next_sibling
    for i in range(len(child_nodes)):
        child_node = child_nodes[i]
        log_info(f"{chr(32) * depth}[document] child: {str(child_node)[:64]}")
        stream_single_node(latex_stream, child_node, depth)
        child_node = child_node.next_sibling
    # Return the next node
    return node.next_sibling
