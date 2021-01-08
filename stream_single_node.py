import convert_html_to_latex
from bs4 import NavigableString, Tag
from convert_html_to_latex import convert_html_to_latex
from stream_blockquote import stream_blockquote
from stream_code import stream_code
from stream_document import stream_document
from stream_em import stream_em
from stream_h1 import stream_h1
from stream_h2 import stream_h2
from stream_h3 import stream_h3
from stream_li import stream_li
from stream_ac_link import stream_ac_link
from stream_p import stream_p
from stream_ul import stream_ul
from stream_unknown import stream_unknown
from write_latex_stream import write_latex_stream
from log_info import log_warning


def stream_single_node(latex_stream, node, depth=0):
    """Stream a single HTML node
    and return the next sibling node"""
    depth += 1
    if node is None:
        return None
    elif isinstance(node, Tag):
        if node.name == "h1":
            stream_h1(latex_stream, node, depth)
            node = None
        elif node.name == "h2":
            node = stream_h2(latex_stream, node, depth)
        elif node.name == "h3":
            node = stream_h3(latex_stream, node, depth)
        elif node.name == "p":
            node = stream_p(latex_stream, node, depth)
        elif node.name == "blockquote":
            node = stream_blockquote(latex_stream, node, depth)
        elif node.name == "em":
            node = stream_em(latex_stream, node, depth)
        elif node.name == "ul":
            node = stream_ul(latex_stream, node, depth)
        elif node.name == "ac:link":
            node = stream_ac_link(latex_stream, node, depth)
        elif node.name == "li":
            node = stream_li(latex_stream, node, depth)
        elif node.name == "code":
            node = stream_code(latex_stream, node, depth)
        elif node.name == "[document]":
            # This is the default root tag
            # used by Beautiful Soup
            # for HTML fragments
            node = stream_document(latex_stream, node, depth)
        else:
            # Other tag, i.e. tag for which we don't
            # have a special implementation.
            # Content will be converted by default pypandoc behavior.
            # You may with to implement a custom handler for this node: {node}.")
            node = stream_unknown(latex_stream, node, depth)
    elif isinstance(node, NavigableString):
        node_as_string = str(node.string)
        node_as_string = node_as_string.replace("\r\n", "")
        node_as_string = node_as_string.replace("\r", "")
        node_as_string = node_as_string.replace("\n", "")
        if node_as_string == "":
            node_as_string = None
        if node_as_string is not None:
            node_latex = convert_html_to_latex(node_as_string)
            write_latex_stream(latex_stream, node_latex)
        # Stream through to the next sibling.
        node = node.next_sibling
    else:
        # Unknown type
        log_warning(f"Unknown type: {type(node)}. Please investigate this node: {node}.")

    # The function stream HTML soup
    # until it reaches the end of the stream.
    # Thus this function should always return None.
    return node
