import xml.etree.ElementTree as ET
from save_file import save_file
from convert_confluence_page_json_to_xml import convert_confluence_page_json_to_xml
from download_confluence_page import download_confluence_page
from get_confluence_page_json import get_confluence_page_json
from get_confluence_page_xml import get_confluence_page_xml
from get_confluence_page_latex import get_confluence_page_latex
from convert_confluence_page_xml_to_latex_dic_entry import convert_confluence_page_xml_to_latex_dic_entry
from ConfluencePage import ConfluencePage
from log_info import log_info


log_info("Pipeline started")

page_id_array = ["822345754", "998244645", "1027080193"]
for page_id in page_id_array:
    space_key = "DIC"
    force_download = True
    # page_json = get_confluence_page_json(space_key=space_key, page_id=page_id, force_download=force_download)
    # page_xml = get_confluence_page_xml(space_key=space_key, page_id=page_id, force_download=force_download)
    page_latex = get_confluence_page_latex(
        space_key=space_key, page_id=page_id,
        force_download=force_download, template="DIC Entry")
    # page = ConfluencePage(space_key=space_key, page_id=page_id, force_download=force_download)
    print(page_latex)

# >>> for elem in tree.iter():
# ...     print elem
# print(page.page_xml)

log_info("Pipeline completed")
