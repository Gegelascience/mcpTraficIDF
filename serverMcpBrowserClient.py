import contextlib

from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.middleware.cors import CORSMiddleware

from mcp.server.fastmcp import FastMCP
from services.idf_transport import getLineInfo
from dotenv import dotenv_values

config = dotenv_values(".env")

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)


idf_mcp = FastMCP(name="IDFTransportServer", stateless_http=True)


# get transport line information
@idf_mcp.tool()
def get_transport_info(line: str) -> list:
    """Get information about a transport line in the Paris region. It can be a metro line or a RER line"""
    apikey = config.get("IDF_API_KEY", "")

    logger.info(f"Received STIF data: {line}.")
    
    return getLineInfo(apikey, line)


# Add a dynamic greeting resource
@idf_mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(idf_mcp.session_manager.run())
        yield

starlette_app = Starlette(
    routes=[
        Mount("/idf", idf_mcp.streamable_http_app()),
    ],
    lifespan=lifespan,
)

starlette_app = CORSMiddleware(
        starlette_app,
        allow_origins=["*"],  # Allow all origins - adjust as needed for production
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],  # MCP streamable HTTP methods
        allow_headers=["Content-Type", "Authorization", "Mcp-Session-Id"],
        expose_headers=["Mcp-Session-Id", "X-Request-Id"],

        max_age=3600
    )

import uvicorn

uvicorn.run(starlette_app, host="127.0.0.1", port=8000)


