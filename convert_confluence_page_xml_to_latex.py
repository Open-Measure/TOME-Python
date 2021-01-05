import pypandoc
import xml.etree.ElementTree as ET

# pylatexenc
# The pylatexenc.latexencode module provides a function unicode_to_latex() which converts a unicode string
# into LaTeX text and escape sequences. It should recognize accented characters and most math symbols. A couple of
# switches allow you to alter how this function behaves.
# https://pypi.org/project/pylatexenc/

def convert_confluence_page_xml_to_latex(page_xml):
    # Parse raw XML to enable DOM manipulations
    # self.page_xml_parsed = ET.fromstring(self.page_xml)
    # Convert HTML to LaTeX
    page_latex = pypandoc.convert_text(page_xml, 'tex', format='html')
    return page_latex
