from get_confluence_page_latex import get_confluence_page_latex
from log_info import log_info


log_info("Pipeline started")
space_key = "DIC"
page_id_array = ["TEST", "998244645", "822345754", "1027080193"]
# page_id_array = ["822345754"]
force_download = False

for page_id in page_id_array:
    log_info(f"space_key: {space_key}, page_id: {page_id}")

    # page_json = get_confluence_page_json(space_key=space_key, page_id=page_id, force_download=force_download)
    # page_xml = get_confluence_page_xml(space_key=space_key, page_id=page_id, force_download=force_download)
    page_latex = get_confluence_page_latex(
        space_key=space_key, page_id=page_id,
        force_download=force_download, template="DIC Entry")
    # page = ConfluencePage(space_key=space_key, page_id=page_id, force_download=force_download)
    print(page_latex)


log_info("Pipeline completed")
