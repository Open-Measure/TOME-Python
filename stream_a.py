from write_latex_stream import write_latex_stream
from log_info import log_info
from convert_html_to_latex import convert_html_to_latex
from get_xml_attribute import get_xml_attribute


def stream_a(latex_stream, node, depth):

    # Local module imports to avoid circular dependencies
    from stream_single_node import stream_single_node

    # Source Structure
    # <a href="[URL]>[Title]</a>

    # Title
    log_info(f"{chr(32) * depth}a: {node}")

    if node is None:
        return None

    # Retrieve the components
    title = node.get_text("", strip=True)
    href = get_xml_attribute(node=node, attribute_name="href")

    # Convert to LaTeX
    title_latex = convert_html_to_latex(title)
    href_latex = convert_html_to_latex(href)

    # Stream the result
    write_latex_stream(latex_stream, f"\\href{{{href_latex}}}{{{title_latex}}}")

    # Return the next node to the calling function to facilitate streaming
    return node.next_sibling
