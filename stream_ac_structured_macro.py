from log_info import log_info, log_warning


def stream_ac_structured_macro(latex_stream, node, depth):
    """Stream a <ac:structured-macro> element and return the next node.

    The structure of Confluence macros is documented here:
    https://confluence.atlassian.com/doc/confluence-storage-format-790796544.html#ConfluenceStorageFormat-Links

    LaTeX format for hyperlinks:
    N/A
    """

    # Local module imports to avoid circular dependencies
    from stream_single_node import stream_single_node

    log_info(f"{chr(32) * depth}ac:structured-macro: {str(node)[:256]}(...)")

    if node is None:
        return None

    # TODO: Extract the CQL query from the macro, execute the CQL and substitute the result.

    return node.next_sibling
