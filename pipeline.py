from get_confluence_page_latex import get_confluence_page_latex
from log_info import log_info, set_log_warning
from list_confluence_pages import list_confluence_pages
import io
import datetime
import time
from write_latex_stream import write_latex_stream
from save_file import save_file
import settings
from convert_html_to_latex import convert_html_to_latex


log_info("Pipeline started")
space_key = "DIC"
page_id_array = ["998244645", "822345754", "1027080193"]
# page_id_array = ["822345754"]
# page_id_array = ["TEST"]
force_download = True

# DIC Terms

latex_stream = io.StringIO()

# f = '%Y-%m-%d %H:%M:%S'
now_as_string = datetime.datetime.now().isoformat()
write_latex_stream(latex_stream, f"% Generation time: {now_as_string} \n")
write_latex_stream(latex_stream, f"% Title: DICTIONARY TERMS INCLUSION LIST \n")
write_latex_stream(latex_stream, f"% Description: This file references all the dictionary term files with an \\input command \n")

confluence_pages = list_confluence_pages(label="iam-dictionary-entry")

# TODO: Sort terms alphabetically

max_iterations = 10000
i = 0
set_log_warning()

for confluence_page in confluence_pages:

    i += 1
    if i > max_iterations:
        break

    page_id = confluence_page["id"]
    page_title = confluence_page["title"]
    # The space attribute is stored under the _expandable node.
    # The format of the space key is: "/rest/api/space/[SPACE_KEY]",
    # e.g.: "/rest/api/space/DIC".
    # We thus need to split the string and get the last segment.
    space_key = confluence_page["_expandable"]["space"].split("/")[-1]
    log_info(f"space_key: {space_key}, page_id: {page_id}")

    file_tex_name = f"{space_key}_{page_id}"
    write_latex_stream(latex_stream, f"\n")
    write_latex_stream(latex_stream, f"% Page Space: {space_key} \n")
    write_latex_stream(latex_stream, f"% Page ID: {page_id} \n")
    write_latex_stream(latex_stream, f"% Page Title: {page_title} \n")
    write_latex_stream(latex_stream, f"\\input{{confluence-page-latex/{file_tex_name}}} \n")

    # page_json = get_confluence_page_json(space_key=space_key, page_id=page_id, force_download=force_download)
    # page_xml = get_confluence_page_xml(space_key=space_key, page_id=page_id, force_download=force_download)
    page_latex = get_confluence_page_latex(
        space_key=space_key, page_id=page_id,
        force_download=force_download, template="DIC Entry")
    # page = ConfluencePage(space_key=space_key, page_id=page_id, force_download=force_download)
    # print(page_latex)

page_latex = latex_stream.getvalue()
page_latex_path = \
    f"{settings.LOCAL_CONFLUENCE_PAGE_LATEX_FOLDER}/" \
    f"DIC_Term_Inclusion_List.tex"

save_file(content=page_latex, file_path=page_latex_path, mode="w", encoding="utf-8")


log_info("Pipeline completed")
