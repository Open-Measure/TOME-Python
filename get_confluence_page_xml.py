from get_confluence_page_xml_path import get_confluence_page_xml_path
from pathlib import Path
from load_file import load_file
from get_confluence_page_json import get_confluence_page_json
from convert_confluence_page_json_to_xml import convert_confluence_page_json_to_xml
from save_file import save_file


def get_confluence_page_xml(space_key, page_id, force_download=False):
    page_xml = None
    if not force_download:
        # Check if the page has already been downloaded
        page_xml_path = get_confluence_page_xml_path(space_key=space_key, page_id=page_id)
        page_xml_path_object = Path(page_xml_path)
        if page_xml_path_object.is_file():
            # The file exists
            page_xml = load_file(file_path=page_xml_path, mode="r", encoding="utf-8")
    if page_xml is None:
        # Retrieving a locally cached file failed
        # or force download was required.
        # Retrieve the page JSON.
        page_json = get_confluence_page_json(space_key=space_key, page_id=page_id, force_download=force_download)
        page_xml = convert_confluence_page_json_to_xml(page_json)
        page_xml_path = get_confluence_page_xml_path(space_key=space_key, page_id=page_id)
        save_file(content=page_xml, file_path=page_xml_path, mode="w", encoding="utf-8")
    return page_xml
