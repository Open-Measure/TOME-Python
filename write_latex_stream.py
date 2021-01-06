
def write_latex_stream(latex_stream, latex):
    """Write to the LaTeX stream."""
    # Dirty fix to remove curious CR and CRLF,
    # curiously it seems that pypandoc is adding these,
    # and this leads to syntax errors in TexStudio.
    latex = latex.replace("\r\n", " ")
    latex = latex.replace("\r", " ")
    latex_stream.write(f"{latex} ")
