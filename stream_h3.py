from write_latex_stream import write_latex_stream
from log_info import log_info
from get_adjacent_html import get_adjacent_html
from convert_html_to_latex import convert_html_to_latex
from get_next_html_node import get_next_html_node


def stream_h3(latex_stream, node, depth):

    # Local module imports to avoid circular dependencies
    from stream_single_node import stream_single_node

    # Source Structure
    # <h3>[Title]</h3>
    # [Adjacent Content]
    # <h1>|<h2>|<h3>|EOF

    # Title
    title = node.get_text("", strip=True)
    log_info(f"{chr(32) * depth}h3: {title}")
    write_latex_stream(latex_stream, f"\\clearpage")
    title_latex = convert_html_to_latex(title)
    if title[:10] == "Definition":
        # Dictionary definitions
        log_info(f"{chr(32) * depth}definition")
        write_latex_stream(latex_stream, f"\\begin{{DIC_Def}}{{{title_latex}}}{{}}")
    else:
        # Default style
        write_latex_stream(latex_stream, f"\\subsubsection*{{{title_latex}}}")

    # Adjacent content
    # This is the HTML after the <h3>
    # and (before the next <h3> or <h2> or EOF)
    # It is necessary to retrieve it like this
    # because sometimes we need to append a
    # closing element to encapsulate the content.
    adjacent_html_soup = get_adjacent_html(node, ["h3", "h2"])
    stream_single_node(latex_stream, adjacent_html_soup, depth)

    # Closing element
    if title[:10] == "Definition":
        # Dictionary definitions
        write_latex_stream(latex_stream, f"\\end{{DIC_Def}}")

    # Return the next node
    next_node = get_next_html_node(node, ["h2", "h3"])
    return next_node
