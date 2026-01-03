from typing import Any
import requests
from enum import Enum
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

hostUrl = "https://prim.iledefrance-mobilites.fr/marketplace"


class LineIDF(Enum):
    LINE_1 = "1"
    LINE_2 = "2"
    LINE_3 = "3"
    LINE_3BIS = "3 bis"
    LINE_4 = "4"
    LINE_5 = "5"
    LINE_6 = "6"
    LINE_7 = "7"
    LINE_7BIS = "7 bis"
    LINE_8 = "8"
    LINE_9 = "9"
    LINE_10 = "10"
    LINE_11 = "11"
    LINE_12 = "12"
    LINE_13 = "13"
    LINE_14 = "14"
    TRANSILIEN_R = "R"
    TRANSILIEN_H = "H"
    RER_A = "A"
    RER_B = "B"
    RER_C = "C"
    RER_D = "D"
    RER_E = "E"
    TRANSILIEN_P = "P"
    TRANSILIEN_J = "J"
    TRANSILIEN_N = "N"
    TRANSILIEN_L = "L"
    TRANSILIEN_K = "K"
    TRANSILIEN_V = "V"
    TRANSILIEN_U = "U"

def formatMsgIdf(listMsg:list[dict[str,Any]]) -> list[dict[str,Any]]:
    if len(listMsg) == 0:
        return []
    else:
        return [{"type":dict(msg.get("InfoChannelRef", {})).get("value", {}),"message":dict(msg.get("Content", {})).get("Message", [])[0].get("MessageText",{}).get("value","") } for msg in listMsg]


def getLineStif(line: str) -> str:

    mappingLineToStif = {
        "1": "C01371",
        "2": "C01372",
        "3": "C01373",
        "3 bis": "C01386",
        "4": "C01374",
        "5": "C01375",
        "6": "C01376",
        "7": "C01377",
        "7 bis": "C01387",
        "8": "C01378",
        "9": "C01379",
        "10": "C01380",
        "11": "C01381",
        "12": "C01382",
        "13": "C01383",
        "14": "C01384",
        "R": "C01731",
        "H": "C01737",
        "A": "C01742",
        "B": "C01743",
        "C": "C01727",
        "D": "C01728",
        "E": "C01729",
        "P": "C01730",
        "J": "C01739",
        "N": "C01736",
        "L": "C01740",
        "K": "C01738",
        "V": "C02711",
        "U": "C01741",
    }

    return mappingLineToStif.get(line, "")




def getLineInfo(apiKey:str,humainLine:LineIDF) -> list[list[dict[str,object]]] | str:
    logger.info(f"Using API Key: {apiKey}")

    selected_line = getLineStif(humainLine.value)

    if(len(selected_line) <= 0) :
      return "Désolé, nous ne connaissons pas la ligne" + humainLine.name

    header = {
        "Accept": "application/json",
        "apikey": f"{apiKey}",
        "Accept-Encoding": "gzip, deflate",
    }

    

    queryParams = {
        "LineRef": "STIF:Line::" +selected_line + ":",
    }

    url = hostUrl+"/general-message"

    try:
        result = requests.get(url,params=queryParams, headers=header)

    except requests.RequestException as e:
        return f"Error fetching data for line {humainLine}: {str(e)}"
    
    if result.status_code != 200:
        return f"Error fetching data for line {humainLine}: {result.status_code} - {result.text}"
    else:
        try:
            jsonResult: dict[str, Any] = result.json()    

            siriData:dict[str,Any] = jsonResult.get("Siri",{})

            if not isinstance(jsonResult.get("Siri"), dict):
                return f"Invalid JSON response for line {humainLine}"

            listGeneralMsg: list[dict[str,Any]] = dict(siriData.get("ServiceDelivery", {})).get("GeneralMessageDelivery", {})

            listInfos = [formatMsgIdf(msg.get("InfoMessage", [])) for msg in listGeneralMsg]

            #return f"Information about transport line: {line} {result.text}"
            return listInfos
        except ValueError:
            return f"Error parsing JSON response for line {humainLine}"