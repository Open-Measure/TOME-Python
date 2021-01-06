from bs4 import BeautifulSoup, NavigableString, Tag


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
