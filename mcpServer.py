# server.py
from mcp.server.fastmcp import FastMCP
import os
import argparse
from services.idf_transport import getLineInfo

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

from dotenv import load_dotenv




# Create an MCP server
mcp = FastMCP("IDFTrafficInfo")


# Add an addition tool
@mcp.tool()
def sum(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# get transport line information
@mcp.tool()
def get_transport_info(line: str) -> list[list[dict]] | str:
    """Get information about a transport line in the Paris region. It can be a metro line or a RER line"""
    apikey = os.environ.get("IDF_API_KEY", "")
    logger.info(f"API key: {apikey}")
    
    return getLineInfo(apikey, line)


@mcp.prompt()
def get_transport_info_prompt(stifData: str) -> str:
    """Prompt for transport line information."""
    if not stifData:
        return "Aucune information disponible pour cette ligne de transport."
    
    logger.info(f"Received STIF data: {stifData}.")

    return f"Voici les informations sur la ligne de transport : {stifData}. La réponse est formatée en chaine de caractères."

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


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
