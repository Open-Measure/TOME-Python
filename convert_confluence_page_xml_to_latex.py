import io
from bs4 import BeautifulSoup
from stream_from import stream_from


def convert_confluence_page_xml_to_latex(page_xml):
    latex_stream = io.StringIO()
    page_soup = BeautifulSoup(page_xml, "html.parser")
    h1 = page_soup.html.body.h1
    stream_from(latex_stream, h1)
    return latex_stream.getvalue()


