import keyring
from atlassian import Confluence

# KEYRING CONFIGURATION:
# To set the configuration in keyring storage, use the following commands.
# Confluence username:
#   keyring.set_password("open_measure", "confluence_username", "[USER_NAME]")
# Confluence base URL:
#   keyring.set_password("open_measure", "confluence_base_url", "https://[SITE_NAME].atlassian.net/")
# Confluence API token:
#   keyring.set_password("open_measure", "confluence_api_token", "[SECRET_PASSWORD]")

# GLOBAL VARIABLES
__confluence = None


def get_confluence_connection():
    global __confluence
    # Retrieve the Confluence base URL from keyring storage:
    confluence_base_url = keyring.get_password("open_measure", "confluence_base_url")
    if __confluence is None:
        # API TOKEN AUTH
        # To create an API token in Confluence:
        #   1) Login to Confluence
        #   2) Go to Account Settings > API Tokens
        # Retrieve the API token from keyring storage:
        confluence_username = keyring.get_password("open_measure", "confluence_username")
        # Retrieve the API token from keyring storage:
        confluence_api_token = keyring.get_password("open_measure", "confluence_api_token")
        __confluence = Confluence(
            url=confluence_base_url,
            username=confluence_username,
            password=confluence_api_token)
        # CERT AUTH
        # confluence = Confluence(
        #    url='http://localhost:8090',
        #    key='/path/to/key',
        #    cert='/path/to/cert')
        # OAUTH
        # confluence = Confluence(
        #    url='http://localhost:8090',
        #    oauth=oauth_dict)
    return __confluence
