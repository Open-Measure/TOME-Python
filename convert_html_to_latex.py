import pypandoc


def convert_html_to_latex(node):
    """Apply default pypandoc behavior
    to convert HTML to LaTeX.
    In general, call it on text content
    or HTML elements for which no
    non-default representations are
    needed."""
    node_as_string = str(node)
    if node_as_string is not None:
        latex = pypandoc.convert_text(node_as_string, 'tex', format='html')
        latex = latex.replace("\r\n", " ")
        latex = latex.replace("\r", " ")
        return latex
    else:
        return None
