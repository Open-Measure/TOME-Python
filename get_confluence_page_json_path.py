import settings


def get_confluence_page_json_path(space_key, page_id):
    confluence_page_json_path = \
        f"{settings.LOCAL_CONFLUENCE_PAGE_JSON_FOLDER}/" \
        f"{space_key}_{page_id}.json"
    return confluence_page_json_path
