from write_latex_stream import write_latex_stream
from log_info import log_info
from get_adjacent_html import get_adjacent_html
from convert_html_to_latex import convert_html_to_latex


def stream_h1(latex_stream, node, depth):

    # Local module imports to avoid circular dependencies
    from stream_single_node import stream_single_node

    # Source Structure
    # <h1>[Title]</h1>
    # [Adjacent Content]
    # Loop:
    #   <h2>|EOF
    #   With <h2> =
    #       <h2>[Title]</h2>
    #       [Adjacent Content]

    # Title
    title = node.get_text("", strip=True)
    log_info(f"{chr(32) * depth}h1: {title}")
    write_latex_stream(latex_stream, f"\\newpage")
    title_latex = convert_html_to_latex(title)
    write_latex_stream(latex_stream, f"\\subsection*{{{title_latex}}}")

    # Adjacent content
    # This is the HTML after <h1> and before the first <h2>
    adjacent_nodes = get_adjacent_html(node, ["h2"])
    stream_single_node(latex_stream, adjacent_nodes, depth)

    # Sub headers
    adjacent_nodes = get_adjacent_html(node, [])
    if adjacent_nodes is not None:
        h2_nodes = adjacent_nodes.find_all("h2")
        for h2 in h2_nodes:
            stream_single_node(latex_stream, h2, depth)

    # Return the next node
    # to the calling function
    # to facilitate streaming.
    # But by definition,
    # after <h1> and its adjacent content
    # there is no more content.
    # In consequence this function should
    # always return None.
    return None