from get_confluence_page_xml import get_confluence_page_xml
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup, NavigableString, Tag
import io
import logging
from log_info import log_info
import pypandoc


def get_adjacent_html_soup(element, closing_tags):
    """Retrieve the adjacent HTML from an element,
    until any closing tag is reached,
    or the document is reached.
    This is practical to retrieve the content
    of pseudo-hierarchical constructs such as
    HTML headers (<h1>, <h2>, <h3>, ...)."""
    # References:
    # - https://www.crummy.com/software/BeautifulSoup/bs4/doc/#string
    # - https://stackoverflow.com/questions/37997702/how-to-convert-a-string-into-a-beautifulsoup-object
    xml_stream = io.StringIO()
    sibling = element
    while True:
        sibling = sibling.nextSibling
        if sibling is None:
            break
        if isinstance(sibling, Tag) and sibling.name in closing_tags:
            break
        if isinstance(sibling, Tag):
            xml_stream.write(sibling.prettify())
        else:
            xml_stream.write(sibling)
    return BeautifulSoup(xml_stream.getvalue(), "html.parser")


def convert_html_to_latex(fragment):
    if type(fragment) == BeautifulSoup:
        fragment = fragment.prettify()
    latex = pypandoc.convert_text(fragment, 'tex', format='html')
    # pypandoc automatically adds a trailing CRLF (\r\n) to the string.
    # Remove it.
    # latex = latex[:-2]
    # latex.replace("\r\n", " ")
    # latex.replace("\r", " ")
    # ???
    return latex


def stream_latex(latex_stream, latex):
    latex = latex.replace("\r\n", " ")
    latex = latex.replace("\r", " ")
    latex_stream.write(latex)


def stream_h2_to_latex(latex_stream, h2):
    # Header
    log_info(f"h2: {h2.text}")
    title_latex = convert_html_to_latex(h2.text)
    stream_latex(latex_stream, f"\\subsection*{{{title_latex}}}")
    # Adjacent text (before any other header)
    adjacent_html_soup = get_adjacent_html_soup(h2, ["h3", "h2", "h1"])
    adjacent_latex = convert_html_to_latex(adjacent_html_soup)
    stream_latex(latex_stream, adjacent_latex)
    # Sub headers
    for h3 in get_adjacent_html_soup(h2, ["h2", "h1"]).find_all("h3"):
        stream_h3_to_latex(latex_stream, h3)


def stream_h3_to_latex(latex_stream, h3):
    # Header
    log_info(f"h3: {h3.text}")
    title_latex = convert_html_to_latex(h3.text)
    # Adjacent text (before any other header)
    adjacent_html_soup = get_adjacent_html_soup(h3, ["h3", "h2", "h1"])
    adjacent_latex = convert_html_to_latex(adjacent_html_soup)
    if h3.get_text("", strip=True)[:10] == "Definition":
        # Dictionary definitions
        log_info(f"definition")
        stream_latex(latex_stream, f"\\begin{{DIC_Def}}{{{title_latex}}}{{}}")
        stream_latex(latex_stream, f"{adjacent_latex}")
        stream_latex(latex_stream, f"\\end{{DIC_Def}}")
    else:
        # Default style
        stream_latex(latex_stream, f"\\subsubsection*{{{title_latex}}}")
        stream_latex(latex_stream, f"{adjacent_latex}")


def convert_confluence_page_xml_to_latex_dic_entry(page_xml):
    latex_stream = io.StringIO()
    page_soup = BeautifulSoup(page_xml, "html.parser")
    # Header
    h1 = page_soup.html.h1
    log_info(f"h1: {h1.text}")
    title_latex = convert_html_to_latex(h1.text)
    stream_latex(latex_stream, f"\\section*{{{title_latex}}}")
    for h2 in get_adjacent_html_soup(h1, ["h1"]).find_all("h2"):
        stream_h2_to_latex(latex_stream, h2)
    return latex_stream.getvalue()


