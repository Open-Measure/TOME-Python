from write_latex_stream import write_latex_stream
from log_info import log_info, log_warning
from get_first_child import get_first_child
from convert_html_to_latex import convert_html_to_latex


def stream_ac_link(latex_stream, node, depth):
    """Stream a <ac:link> element and return the next node.

    The structure of Concluence links is documented here:
    https://confluence.atlassian.com/doc/confluence-storage-format-790796544.html#ConfluenceStorageFormat-Links

    LaTeX format for hyperlinks:
    \href{http://[URL]}{[TITLE]}
    """

    # Local module imports to avoid circular dependencies
    from stream_single_node import stream_single_node

    log_info(f"{chr(32) * depth}ac:link: {str(node)[:256]}(...)")
    write_latex_stream(latex_stream, f"(link)")
    target_title = node.find("ri:page")
    if target_title is not None:
        target_title = target_title.text
    else:
        target_title = "???"
        log_warning(f"No <ri:page> found in <ac:link>!")
    target_url = node.find("ac:link-body")
    if target_url is not None:
        # This is a link to a Confluence page
        target_url = target_url.text
    else:
        target_url = "???"
        log_warning(f"No <ac:link-body> found in <ac:link>!")

    target_title_latex = convert_html_to_latex(target_title)
    title_url_latex = convert_html_to_latex(target_url)
    write_latex_stream(latex_stream, f"\\href{{{title_url_latex}}}{{{target_title_latex}}}")

    #child_nodes = []
    #child_node = get_first_child(node)
    #while child_node:
    #    child_nodes.append(child_node)
    #    child_node = child_node.next_sibling
    #for i in range(len(child_nodes)):
    #    child_node = child_nodes[i]
    #    log_info(f"{chr(32) * depth}link child: {str(child_node)[:64]}(...)")
    #    stream_single_node(latex_stream, child_node, depth)
    # Return the next node
    return node.next_sibling
