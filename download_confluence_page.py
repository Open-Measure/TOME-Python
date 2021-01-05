from get_confluence_connection import get_confluence_connection


def download_confluence_page(space_key, page_id):
    """Download a confluence page and return the JSON"""
    # Get Confluence connection
    confluence_connection = get_confluence_connection()
    # Download the Confluence page
    # which comes in a JSON format
    # that includes page properties
    # and wrap page content
    page_json = confluence_connection.get_page_by_id(page_id=page_id, expand="body.storage")
    return page_json
