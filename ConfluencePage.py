from get_confluence_page_json import get_confluence_page_json
from get_confluence_page_xml import get_confluence_page_xml
from get_confluence_page_latex import get_confluence_page_latex


class ConfluencePage:
    def __init__(self, space_key, page_id, force_download=False):
        self.space_key = space_key
        self.page_id = page_id
        # Retrieve first the output of the last pipeline step
        self.page_latex = get_confluence_page_latex(space_key=space_key, page_id=page_id, force_download=force_download)
        # Benefit from local cache to retrieve precedent pipeline steps.
        # Force Download option is no longer necessary.
        self.page_xml = get_confluence_page_xml(space_key=space_key, page_id=page_id, force_download=False)
        self.page_json = get_confluence_page_json(space_key=space_key, page_id=page_id, force_download=False)
