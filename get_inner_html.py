from bs4 import BeautifulSoup, NavigableString, Tag
import io
from log_info import log_info

XXX?
def get_inner_html(node):
    """The node.children iterator and node.next_sibling property
    of BeautifulSoup nodes have apparently a "voluntary" bug
    that is especially problematic when parsing composite strings
    of text and tags:
    :param node:
    :return:
    """
    # References:
    # - https://www.crummy.com/software/BeautifulSoup/bs4/doc/#string
    # - https://stackoverflow.com/questions/37997702/how-to-convert-a-string-into-a-beautifulsoup-object
    xml_stream = io.StringIO(newline="")
    sibling = node
    while True:
        sibling = sibling.nextSibling
        if sibling is None:
            break
        if isinstance(sibling, Tag) and sibling.name in closing_tags:
            break
        if isinstance(sibling, Tag):
            xml_stream.write(str(sibling))
        else:
            xml_stream.write(sibling)
    xml_string = xml_stream.getvalue()
    # CR and LF are useless entities in HTML
    # and produce a lot of useless parsing.
    xml_string = xml_string.replace("\n", "")
    xml_string = xml_string.replace("\r", "")
    if xml_string == "":
        # If no writes were done on the stream,
        # it will end up as an empty string.
        # To make it clear that there was no
        # content, we rather return None.
        log_info(f"get_adjacent_html(node, {closing_tags}) = None")
        return None
    else:
        return BeautifulSoup(xml_stream.getvalue(), "html.parser")
