from convert_html_to_latex import convert_html_to_latex
from get_adjacent_html import get_adjacent_html
from get_next_html_node import get_next_html_node
from log_info import log_info
from write_latex_stream import write_latex_stream


def stream_h2(latex_stream, node, depth):

    # Local module imports to avoid circular dependencies
    from stream_single_node import stream_single_node

    # Source Structure
    # <h2>[Title]</h2>
    # [Adjacent Content]
    # <h1>|<h2>|<h3>|EOF
    # [<h3> Sub Headers]
    # [<h3> Sub Headers Content]

    # Title
    title = node.get_text("", strip=True)
    log_info(f"{chr(32) * depth}h2: {title}")
    title_latex = convert_html_to_latex(title)
    write_latex_stream(latex_stream, f"\\subsection*{{{title_latex}}}")

    # Adjacent Content
    # This is the HTML after the <h2>
    # but (before the first <h3> or before the next <h2>)
    adjacent_nodes = get_adjacent_html(node, ["h3", "h2"])
    stream_single_node(latex_stream, adjacent_nodes, depth)

    # Sub headings
    adjacent_nodes = get_adjacent_html(node, ["h2"])
    if adjacent_nodes is not None:
        h3_nodes = adjacent_nodes.find_all("h3")
        for h3 in h3_nodes:
            stream_single_node(latex_stream, h3, depth)

    # Return the next node
    next_node = get_next_html_node(node, ["h2"])
    return next_node
