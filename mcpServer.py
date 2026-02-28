# server.py
from mcp.server.fastmcp import FastMCP
import os

from services.idf_transport import LineIDF, getLineInfo
from typing import Any
import contextlib
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.requests import HTTPConnection
import logging
import uvicorn
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser
)

logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

from dotenv import load_dotenv

load_dotenv(".env")






# Create an MCP server
mcp = FastMCP(
    "IDFTrafficInfo", 
    "Get traffic information for the Paris region transport lines (Metro, RER, Transilien)",
    )



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

# Create a lifespan context manager to run the session manager
@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with mcp.session_manager.run():
        yield

class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection):
        logger.info("Starting authentication")
        logger.info(f"Authorization header: {conn.headers}")
        try:
            tokenBearer = conn.headers.get("Authorization")
            if tokenBearer is None:
                raise AuthenticationError('Invalid token auth credentials')
            token = tokenBearer.split(" ")[1]
            token_ref = os.environ.get("API_BEARER_TOKEN", "Test")
            if token != token_ref:
                raise AuthenticationError('Invalid token auth credentials')
        except (Exception) as exc:
            logger.error(f"Authentication error: {exc}")
            raise AuthenticationError('Invalid token auth credentials')

        logger.info("Authorization OK")
        return AuthCredentials(["authenticated"]), SimpleUser("user123")


if __name__ == "__main__":
    
    mcp.settings.port = 8000
    mcp.settings.host = "0.0.0.0"

    app = Starlette(
        routes=[
            Mount("/", app=mcp.streamable_http_app()),
        ],
        lifespan=lifespan,
    )

    app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())

    

    uvicorn.run(app, host=mcp.settings.host, port=mcp.settings.port)


