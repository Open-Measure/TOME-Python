import settings


def get_confluence_page_latex_path(space_key, page_id):
    confluence_page_latex_path = \
        f"{settings.LOCAL_CONFLUENCE_PAGE_LATEX_FOLDER}/" \
        f"{space_key}_{page_id}.tex"
    return confluence_page_latex_path
