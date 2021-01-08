from log_info import log_info, log_warning


def stream_unknown(latex_stream, node, depth):
    """Stream an unknown <???> element and return the next node."""

    log_warning(f"Unknown tag: {node.name}\n{node}\n\n")

    # Local module imports to avoid circular dependencies
    from stream_single_node import stream_single_node

    log_info(f"{chr(32) * depth}unknown")
    for child_node in node.children:
        stream_single_node(latex_stream, child_node, depth)
    # Return the next node
    return node.next_sibling
