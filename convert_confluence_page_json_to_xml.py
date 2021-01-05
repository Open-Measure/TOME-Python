def convert_confluence_page_json_to_xml(page_json):
    """Receive a Confluence page body.storage property value,
    as an XML fragment,
    and wraps it properly in a well-formed XML document.
    REFERENCES:
        - http://www.amnet.net.au/~ghannington/confluence/readme.html
        - https://www.w3.org/TR/xhtml1/dtds.html#a_dtd_Latin-1_characters
        - https://stackoverflow.com/questions/7237466/python-elementtree-support-for-parsing-unknown-xml-entities"""
    #
    # DOC TYPE AND DOCUMENT STRUCTURE
    # I choose to wrap the XML in an XHTML doc type,
    # an alternative would be to wrap it in a Confluence doc type.
    # It is unclear to me which approach is "right", here.
    # Alternative XML:
    # <ac:confluence
    #   xmlns:ac="http://www.atlassian.com/schema/confluence/4/ac/"
    #   xmlns:ri="http://www.atlassian.com/schema/confluence/4/ri/"
    #   xmlns="http://www.atlassian.com/schema/confluence/4/">
    # </ac:confluence>
    #
    # HTML ENTITIES
    # Unfortunately, the Python XML library
    # does not support the importation of external entities.
    # I thus revert to include them one by one expressly.
    # " <!ENTITY % HTMLlat1 PUBLIC" \
    # " \"-//W3C//ENTITIES Latin 1 for XHTML//EN\"" \
    # " \"http://www.w3.org/TR/xhtml1/DTD/xhtml-lat1.ent\">" \
    # " %HTMLlat1;" \
    # " <!ENTITY % HTMLspecial PUBLIC" \
    # " \"-//W3C//ENTITIES Special for XHTML//EN\"" \
    # " \"http://www.w3.org/TR/xhtml1/DTD/xhtml-special.ent\" >" \
    # " %HTMLspecial;" \

    # Retrieve the page title from the JSON.
    page_title = page_json["title"]

    # Retrieve the page content XML fragment in the JSON.
    body_storage_value = page_json["body"]["storage"]["value"]

    # Convert XML fragment to well-formed XML document
    page_xml = \
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
        "<!DOCTYPE html" \
        " PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\"" \
        " \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"" \
        " [" \
        " <!ENTITY rsquo \"’\">" \
        " <!ENTITY ndash \"–\">" \
        " ]" \
        " >" \
        "<html " \
        " xmlns=\"http://www.w3.org/1999/xhtml\"" \
        " xmlns:ac=\"http://www.atlassian.com/schema/confluence/4/ac/\"" \
        " xmlns:ri=\"http://www.atlassian.com/schema/confluence/4/ri/\"" \
        " xml:lang=\"en\" lang=\"en\">" \
        "<head>" \
        f"<title>{page_title}</title>" \
        "</head>" \
        "<body>" \
        f"{body_storage_value}" \
        "</body>" \
        "</html>"

    return page_xml
