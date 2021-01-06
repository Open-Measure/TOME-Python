from get_confluence_page_latex_path import get_confluence_page_latex_path
from pathlib import Path
from load_file import load_file
from save_file import save_file
from get_confluence_page_xml import get_confluence_page_xml
from convert_confluence_page_xml_to_latex import convert_confluence_page_xml_to_latex
from convert_confluence_page_xml_to_latex import convert_confluence_page_xml_to_latex


def get_confluence_page_latex(space_key, page_id, force_download=False, template=None):
    page_latex = None
    if not force_download:
        # Check if the page has already been downloaded
        page_latex_path = get_confluence_page_latex_path(space_key=space_key, page_id=page_id)
        page_latex_path_object = Path(page_latex_path)
        if page_latex_path_object.is_file():
            # The file exists
            page_latex = load_file(file_path=page_latex_path, mode="r", encoding="utf-8")
    if page_latex is None:
        # Retrieving a locally cached file failed
        # or force download was required.
        # Retrieve the page XML.
        page_xml = get_confluence_page_xml(space_key=space_key, page_id=page_id, force_download=force_download)
        # Retrieving a locally cached file failed
        # or force download was required.
        # Retrieve the page JSON.
        page_xml = get_confluence_page_xml(space_key=space_key, page_id=page_id, force_download=force_download)
        page_latex = None
        page_latex = convert_confluence_page_xml_to_latex(page_xml)
        page_latex_path = get_confluence_page_latex_path(space_key=space_key, page_id=page_id)
        save_file(content=page_latex, file_path=page_latex_path, mode="w", encoding="utf-8")
    return page_xml
