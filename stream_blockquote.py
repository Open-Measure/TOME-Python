from log_info import log_info
from convert_html_to_latex import convert_html_to_latex
from write_latex_stream import write_latex_stream


def stream_blockquote(latex_stream, node, depth):
    """Stream a blockquote element,
    and return the next node."""

    # Local module imports to avoid circular dependencies
    # N/A

    log_info(f"{chr(32) * depth}blockquote")
    # Source Structure
    # <blockquote>[Quote]</blockquote>
    # <p><a>[Citation]</a></p>
    #
    # Quote
    quote_latex = convert_html_to_latex(node.text)
    write_latex_stream(latex_stream, f"\\begin{{DIC_BlockQuote}}")
    write_latex_stream(latex_stream, quote_latex)
    write_latex_stream(latex_stream, f"\\end{{DIC_BlockQuote}}")
    # Citation
    p = node.next_sibling
    if p.name == "p":
        citation = convert_html_to_latex(p)
        write_latex_stream(latex_stream, citation)
    # Return the next node
    # to the calling function
    # to facilitate streaming.
    if p.name != "p":
        log_warning("Blockquote is not followed by <p>")
        return node.next_sibling
    else:
        return p.next_sibling
