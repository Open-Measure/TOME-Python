from write_latex_stream import write_latex_stream
from log_info import log_info
from convert_html_to_latex import convert_html_to_latex
from get_xml_attribute import get_xml_attribute


def stream_br(latex_stream, node, depth):

    # Local module imports to avoid circular dependencies
    from stream_single_node import stream_single_node

    # Source Structure
    # </br>

    # Title
    log_info(f"{chr(32) * depth}br")

    if node is None:
        return None

    # Stream the result
    write_latex_stream(latex_stream, f"\\\\ ")

    # Return the next node to the calling function to facilitate streaming
    return node.next_sibling
