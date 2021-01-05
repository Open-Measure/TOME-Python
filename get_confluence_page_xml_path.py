import settings


def get_confluence_page_xml_path(space_key, page_id):
    confluence_page_xml_path = \
        f"{settings.LOCAL_CONFLUENCE_PAGE_XML_FOLDER}/" \
        f"{space_key}_{page_id}.xml"
    return confluence_page_xml_path
