from bs4 import BeautifulSoup, NavigableString, Tag
import io
from log_info import log_info, log_warning
import pypandoc
from get_adjacent_html import get_adjacent_html


def get_next_html_node(starting_node, tags):
    """Find the next HTML node
    that matches one of the tags.
    Useful to stream through nodes."""
    if starting_node is None:
        # EOF
        return None
    for current_node in starting_node.next_elements:
        if isinstance(current_node, Tag) and current_node.name == tags:
            return current_node
    # EOF
    return None


def convert_html_to_latex(node):
    """Apply default pypandoc behavior
    to convert HTML to LaTeX.
    In general, call it on text content
    or HTML elements for which no
    non-default representations are
    needed."""
    node_as_string = str(node)
    #if isinstance(node, Tag):
    #    node_as_string = str(node)
    #elif isinstance(node, NavigableString):
    #    node_as_string = str(node.string)
    if node_as_string is not None:
        latex = pypandoc.convert_text(node_as_string, 'tex', format='html')
        latex = latex.replace("\r\n", " ")
        latex = latex.replace("\r", " ")
        return latex
    else:
        return None


def write_latex_stream(latex_stream, latex):
    """Write to the LaTeX stream."""
    # Dirty fix to remove curious CR and CRLF,
    # curiously it seems that pypandoc is adding these,
    # and this leads to syntax errors in TexStudio.
    latex = latex.replace("\r\n", " ")
    latex = latex.replace("\r", " ")
    latex_stream.write(latex)


def stream_from(latex_stream, node, depth=0):
    """Stream arbitrary HTML
    from one node
    until it reaches the end of the parent document"""
    while node is not None:
        node = stream_single_node(latex_stream, node, depth)
    return None


def stream_single_node(latex_stream, node, depth=0):
    """Stream a single HTML node
    and return the next sibling node"""
    depth += 1
    if isinstance(node, Tag):
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
            log_warning(f"Unknown tag: {node.name}")
            # Content will be converted by default pypandoc behavior. You may with to implement a custom handler for this node: {node}.")
            node = stream_unknown(latex_stream, node, depth)
            # Stream through to the next sibling.
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


def stream_h1(latex_stream, node, depth):
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


def stream_h2(latex_stream, node, depth):
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


def stream_h3(latex_stream, node, depth):
    # Source Structure
    # <h3>[Title]</h3>
    # [Adjacent Content]
    # <h1>|<h2>|<h3>|EOF

    # Title
    title = node.get_text("", strip=True)
    log_info(f"{chr(32) * depth}h3: {title}")
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


def stream_blockquote(latex_stream, node, depth):
    """Stream a blockquote element,
    and return the next node."""
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


def stream_p(latex_stream, node, depth):
    """Stream a <p> element and return the next node."""
    log_info(f"{chr(32) * depth}p: {str(node)[:64]}(...)")
    write_latex_stream(latex_stream, f"\\paragraph{{}}")
    child_nodes = []
    child_node = get_first_child(node)
    while child_node:
        child_nodes.append(child_node)
        child_node = child_node.next_sibling
    for i in range(len(child_nodes)):
        child_node = child_nodes[i]
        log_info(f"{chr(32) * depth}p child: {str(child_node)[:64]}(...)")
        if isinstance(child_node, NavigableString):
            pass # XXX
        stream_single_node(latex_stream, child_node, depth)
    # Return the next node
    return node.next_sibling


def get_first_child(node):
    first_child = node.contents[0]
    # log_info(f"First child: {str(first_child)[:64]}")
    return first_child


def stream_document(latex_stream, node, depth):
    """When Beautiful Soup parses an HTML fragment,
    by default it wraps it in a root tag named <[document]>.
    Thus. whenever we extract (e.g. adjacent) HTML fragments,
    we then need to first parse the parent <[document]>
    and only then can we parse its children."""
    log_info(f"{chr(32) * depth}[document]: {str(node)[:64]}(...)")
    child_nodes = []
    child_node = get_first_child(node)
    while child_node:
        child_nodes.append(child_node)
        child_node = child_node.next_sibling
    for i in range(len(child_nodes)):
        child_node = child_nodes[i]
        log_info(f"{chr(32) * depth}[document] child: {str(child_node)[:64]}")
        stream_single_node(latex_stream, child_node, depth)
        child_node = child_node.next_sibling
    # Return the next node
    return node.next_sibling


def stream_em(latex_stream, node, depth):
    """Stream a <em> element and return the next node."""
    log_info(f"{chr(32) * depth}em: {str(node)[:24]}(...)")
    write_latex_stream(latex_stream, f"\\emph{{")
    child_nodes = []
    child_node = get_first_child(node)
    while child_node:
        child_nodes.append(child_node)
        child_node = child_node.next_sibling
    for i in range(len(child_nodes)):
        child_node = child_nodes[i]
        log_info(f"{chr(32) * depth}em child: {str(child_node)[:64]}")
        stream_single_node(latex_stream, child_node, depth)
    write_latex_stream(latex_stream, f"}}")
    # Return the next node
    return node.next_sibling


def stream_ul(latex_stream, node, depth):
    """Stream a <ul> element and return the next node."""
    log_info(f"{chr(32) * depth}ul")
    write_latex_stream(latex_stream, f"\\begin{{itemize}}")
    for child_node in node.find_all("li"):
        stream_single_node(latex_stream, child_node, depth)
    write_latex_stream(latex_stream, f"\\end{{itemize}}")
    # Return the next node
    return node.next_sibling


def stream_li(latex_stream, node, depth):
    """Stream a <li> element and return the next node."""
    log_info(f"{chr(32) * depth}li")
    write_latex_stream(latex_stream, f"\\item ")
    for child_node in node.children:
        stream_single_node(latex_stream, child_node, depth)
    # Return the next node
    return node.next_sibling


def stream_code(latex_stream, node, depth):
    """Stream a <code> element and return the next node."""
    log_info(f"{chr(32) * depth}code")
    write_latex_stream(latex_stream, f"\\texttt{{")
    for child_node in node.children:
        stream_single_node(latex_stream, child_node, depth)
    write_latex_stream(latex_stream, f"}}")
    # Return the next node
    return node.next_sibling


def stream_unknown(latex_stream, node, depth):
    """Stream an unknown <???> element and return the next node."""
    log_info(f"{chr(32) * depth}unknown")
    for child_node in node.children:
        stream_single_node(latex_stream, child_node, depth)
    # Return the next node
    return node.next_sibling


def convert_confluence_page_xml_to_latex(page_xml):
    latex_stream = io.StringIO()
    page_soup = BeautifulSoup(page_xml, "html.parser")
    h1 = page_soup.html.body.h1
    stream_from(latex_stream, h1)
    return latex_stream.getvalue()


