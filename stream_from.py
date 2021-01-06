from stream_single_node import stream_single_node


def stream_from(latex_stream, node, depth=0):
    """Stream arbitrary HTML
    from one node
    until it reaches the end of the parent document"""
    while node is not None:
        node = stream_single_node(latex_stream, node, depth)
    return None
