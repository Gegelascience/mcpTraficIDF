# server.py
from mcp.server.fastmcp import FastMCP
import os
import argparse
from services.idf_transport import LineIDF, getLineInfo
from typing import Any

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

from dotenv import load_dotenv




# Create an MCP server
mcp = FastMCP("IDFTrafficInfo", "Get traffic information for the Paris region transport lines (Metro, RER, Transilien)")



# get transport line information
@mcp.tool()
def get_transport_info(line: LineIDF) -> list[list[dict[str,Any]]] | str:
    """
        Get information about a transport line in the Paris region. It can be a metro line or a RER line or transilien line.
        Args:
            line (LineIDF): The line to get information about. It should be one of the values from the LineIDF enum.
    """
    apikey = os.environ.get("IDF_API_KEY", "")
    logger.info(f"API key: {apikey}")
    
    return getLineInfo(apikey, line)



if __name__ == "__main__":
    #print("Starting MCP server…")
    #mcp.run(transport="stdio")

    parser = argparse.ArgumentParser()
    parser.add_argument("-m","--mode", choices=["stdio", "http"], type=str, default="stdio")
    args =parser.parse_args()

    if args.mode == "stdio":
        mcp.run(transport="stdio")
    elif args.mode == "http":
        mcp.settings.port = 8000
        mcp.settings.host = "0.0.0.0"
        load_dotenv(".env")
        mcp.run(transport="streamable-http")
