from write_latex_stream import write_latex_stream
from log_info import log_info


def stream_ul(latex_stream, node, depth):
    """Stream a <ul> element and return the next node."""

    # Local module imports to avoid circular dependencies
    from stream_single_node import stream_single_node

    log_info(f"{chr(32) * depth}ul")
    write_latex_stream(latex_stream, f"\\begin{{enumerate}}")
    for child_node in node.find_all("li"):
        stream_single_node(latex_stream, child_node, depth)
    write_latex_stream(latex_stream, f"\\end{{enumerate}}")
    # Return the next node
    return node.next_sibling
