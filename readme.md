# MCP Trafic IDF

MCP with PRIM API implementation of Paris metro lines trafic informations (https://prim.iledefrance-mobilites.fr/fr/apis/idfm-ivtr-info_trafic).
It use Gemini as a LLM.


## Setup

Install dependencies
````bash
python3 -m pip install -r requirements.txt
````

Create a .env with api keys

````.env
IDF_API_KEY=<PRIM APIKEY>
GEMINI_API_KEY=<GEMINI APIKEY>
````


## Run App (stdio)

````bash
python3 mcpClientStdio.py
````

The mcp server run in stdio mode so it is a subprocess of client process.


