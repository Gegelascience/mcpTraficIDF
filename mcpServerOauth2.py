# server.py

import os


from services.idf_transport import LineIDF, getLineInfo
from typing import Any

import logging
from fastmcp import FastMCP
from fastmcp.server.auth.providers.google import GoogleProvider
from fastmcp.server.dependencies import get_access_token

logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

from dotenv import load_dotenv

load_dotenv(".env")

auth_provider = GoogleProvider(
    client_id=os.environ.get("GOOGLE_CLIENT_ID", "VOTRE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", "VOTRE_CLIENT_SECRET"),
    #required_scopes=["https://www.googleapis.com/auth/calendar.readonly"]
    base_url="http://localhost:8000",
    required_scopes=[                                  # Request user information
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
    ],
)



# Create an MCP server
mcp = FastMCP(
    "IDFTrafficInfo", 
    "Get traffic information for the Paris region transport lines (Metro, RER, Transilien)",
    auth=auth_provider,
    
    )



# get transport line information
@mcp.tool()
def get_transport_info(line: LineIDF) -> list[list[dict[str,Any]]] | str:
    """
        Get information about a transport line in the Paris region. It can be a metro line or a RER line or transilien line.
        Args:
            line (LineIDF): The line to get information about. It should be one of the values from the LineIDF enum.
    """
    token = get_access_token()
    if token:
        logger.info(f"User email: {token.claims.get('email')}")
    apikey = os.environ.get("IDF_API_KEY", "")
    logger.info(f"API key: {apikey}")
    
    return getLineInfo(apikey, line)






if __name__ == "__main__":
    
    #mcp.settings.port = 8000
    #mcp.settings.host = "0.0.0.0"

    mcp.run(transport="streamable-http")

