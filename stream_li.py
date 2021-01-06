from write_latex_stream import write_latex_stream
from log_info import log_info


def stream_li(latex_stream, node, depth):
    """Stream a <li> element and return the next node."""

    # Local module imports to avoid circular dependencies
    from stream_single_node import stream_single_node

    log_info(f"{chr(32) * depth}li")
    write_latex_stream(latex_stream, f"\\item ")

    # Confluence embeds a <p> inside <li> items.
    # LaTeX consider that \item elements are
    # equivalent to paragraphs and cannot
    # contain a \paragraph item.
    # Consequently I skip the <p> element
    # and parse directly its content.
    node_children = node.p

    for child_node in node_children:
        stream_single_node(latex_stream, child_node, depth)
    # Return the next node
    return node.next_sibling
