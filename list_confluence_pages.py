from get_confluence_connection import get_confluence_connection


def list_confluence_pages(label):
    # References:
    # - https://developer.atlassian.com/cloud/confluence/rest/api-group-content/#api-api-content-get

    # Get Confluence connection
    confluence_connection = get_confluence_connection()

    # Download the Confluence page
    # which comes in a JSON format
    # that includes page properties
    # and wrap page content
    page_json = confluence_connection.get_all_pages_by_label(label=label)
    return page_json
