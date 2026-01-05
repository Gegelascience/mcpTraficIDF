# MCP Trafic IDF

MCP with PRIM API implementation of Paris metro lines trafic informations (https://prim.iledefrance-mobilites.fr/fr/apis/idfm-ivtr-info_trafic).
It use Gemini as a LLM.


## Setup

Install dependencies
````sh
python3 -m pip install -r requirements.txt
````

Create a .env with api keys

````.env
IDF_API_KEY=<PRIM APIKEY>
GEMINI_API_KEY=<GEMINI APIKEY>
````




## Run App (http streamable server)

First launch the server

````sh
python3 mcpServer.py
````
The server will run on localhost on port 8000.

Once done, on another terminal, launch the client.

````sh
python3 mcpClientHttp.py
````


