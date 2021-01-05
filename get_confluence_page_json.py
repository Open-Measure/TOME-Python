from get_confluence_page_json_path import get_confluence_page_json_path
from pathlib import Path
from load_file import load_file
from download_confluence_page import download_confluence_page
from save_file import save_file


def get_confluence_page_json(space_key, page_id, force_download=False):
    page_json = None
    page_json_path = get_confluence_page_json_path(space_key=space_key, page_id=page_id)
    if not force_download:
        # Check if the page has already been downloaded
        page_json_path_object = Path(page_json_path)
        if page_json_path_object.is_file():
            # The file exists, use it
            page_json = load_file(file_path=page_json_path, mode="r", encoding="utf-8")
    if page_json is None:
        # Retrieving a locally cached file failed
        # or force download was required.
        page_json = download_confluence_page(space_key=space_key, page_id=page_id)
        # Cache the JSON file locally.
        save_file(content=str(page_json), file_path=page_json_path)
    return page_json
