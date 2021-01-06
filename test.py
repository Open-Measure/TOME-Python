import xml.etree.ElementTree as ET
from save_file import save_file
from convert_confluence_page_json_to_xml import convert_confluence_page_json_to_xml
from download_confluence_page import download_confluence_page
from get_confluence_page_xml import get_confluence_page_xml
from list_confluence_pages import list_confluence_pages


page_id = "1027080193"
space_key = "DIC"
# page_xml = get_confluence_page_xml(space_key=space_key, page_id=page_id)
print(list_confluence_pages(label="iam-dictionary-entry"))
