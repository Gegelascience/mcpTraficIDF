import requests

hostUrl = "https://prim.iledefrance-mobilites.fr/marketplace"


def formatMsgIdf(listMsg:list) -> list:
    if len(listMsg) == 0:
        return []
    else:
        return [{"type":msg.get("InfoChannelRef", {}).get("value", {}),"message":msg.get("Content", {}).get("Message", [])[0].get("MessageText",{}).get("value","") } for msg in listMsg]


def getLineStif(line: str) -> str:

    lineMapping = [
        {
        "human":"1",
        "stif":"C01371"
        },
        {
        "human":"2",
        "stif":"C01372"
        },
        {
        "human":"3",
        "stif":"C01373"
        },
        {
        "human":"3bis",
        "stif":"C01386"
        },
        {
        "human":"3 bis",
        "stif":"C01386"
        },
        {
        "human":"4",
        "stif":"C01374"
        },
        {
        "human":"5",
        "stif":"C01375"
        },
        {
        "human":"6",
        "stif":"C01376"
        },
        {
        "human":"7",
        "stif":"C01377"
        },
        {
        "human":"7bis",
        "stif":"C01387"
        },
        {
        "human":"8",
        "stif":"C01378"
        },
        {
        "human":"9",
        "stif":"C01379"
        },
        {
        "human":"10",
        "stif":"C01380"
        },
        {
        "human":"11",
        "stif":"C01381"
        },
        {
        "human":"12",
        "stif":"C01382"
        },
        {
        "human":"13",
        "stif":"C01383"
        },
        {
        "human":"14",
        "stif":"C01384"
        },
        {
        "human":"R",
        "stif":"C01731"
        },
        {
        "human":"H",
        "stif":"C01737"
        },
        {
        "human":"A",
        "stif":"C01742"
        },
        {
        "human":"B",
        "stif":"C01743"
        },
        {
        "human":"C",
        "stif":"C01727"
        },
        {
        "human":"D",
        "stif":"C01728"
        },
        {
        "human":"E",
        "stif":"C01729"
        },
    ]

    selected_line = [lineM for lineM in lineMapping if lineM["human"].upper() == line.upper()]

    return selected_line



def getLineInfo(apiKey:str, humainLine:str):

    selected_line = getLineStif(humainLine)

    if(len(selected_line) <= 0) :
      return "Désolé, nous ne connaissons pas la ligne" + humainLine

    header = {
        "Accept": "application/json",
        "apikey": f"{apiKey}",
        "Accept-Encoding": "gzip, deflate",
    }

    

    queryParams = {
        "LineRef": "STIF:Line::" +selected_line[0]["stif"] + ":",
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