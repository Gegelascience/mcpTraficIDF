import requests

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

hostUrl = "https://prim.iledefrance-mobilites.fr/marketplace"


def formatMsgIdf(listMsg:list) -> list:
    if len(listMsg) == 0:
        return []
    else:
        return [{"type":msg.get("InfoChannelRef", {}).get("value", {}),"message":msg.get("Content", {}).get("Message", [])[0].get("MessageText",{}).get("value","") } for msg in listMsg]


def getLineStif(line: str) -> str:

    if line == "1":
        return "C01371"
    elif line == "2":
        return "C01372"
    elif line == "3":
        return "C01373"
    elif line == "3bis" or line == "3 bis":
        return "C01386"
    elif line == "4":
        return "C01374"
    elif line == "5":
        return "C01375"
    elif line == "6":
        return "C01376"
    elif line == "7":
        return "C01377"
    elif line == "7bis" or line == "7 bis":
        return "C01387"
    elif line == "8":
        return "C01378"
    elif line == "9":
        return "C01379"
    elif line == "10":
        return "C01380"
    elif line == "11":
        return "C01381"
    elif line == "12":
        return "C01382"
    elif line == "13":
        return "C01383"
    elif line == "14":
        return "C01384"
    elif line == "R":
        return "C01731"
    elif line == "H":
        return "C01737"
    elif line == "A" or line == "RER A":
        return "C01742"
    elif line == "B" or line == "RER B":
        return "C01743"
    elif line == "C" or line == "RER C":
        return "C01727"
    elif line == "D" or line == "RER D":
        return "C01728"
    elif line == "E" or line == "RER E":
        return "C01729"
    else:
        return ""




def getLineInfo(apiKey,humainLine:str):
    logger.info(f"Using API Key: {apiKey}")

    selected_line = getLineStif(humainLine)

    if(len(selected_line) <= 0) :
      return "Désolé, nous ne connaissons pas la ligne" + humainLine

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

            listGeneralMsg = result.json().get("Siri", {}).get("ServiceDelivery", {}).get("GeneralMessageDelivery", {})

            listInfos = [formatMsgIdf(msg.get("InfoMessage", [])) for msg in listGeneralMsg]

            #return f"Information about transport line: {line} {result.text}"
            return listInfos
        except ValueError:
            return f"Error parsing JSON response for line {humainLine}"