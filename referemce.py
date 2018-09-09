import requests
from pure_python_parser import parse_json
import time
import json

def trains_btwn_stations(stn1, stn2, viaStn="null", trainType="ALL"):
    stn1 = stnName_to_stnCode(stn1)
    stn2 = stnName_to_stnCode(stn2)
    query_url = base_URL+f"NTES?action=getTrnBwStns&stn1={stn1}&stn2={stn2}&trainType={trainType}"
    if(viaStn != "null"):
        viaStn = stnName_to_stnCode(viaStn)
        query_url = query_url+f"&viaStn={viaStn}"
    r = requests.get(query_url)
    json_data = parse_json(r.text, ["runsOnDays", "trnName"])
    variable = list(json_data.keys())[0]
    trains=json_data[variable]["trains"]["direct"]
    message="Trains going from  "+stn1+" to "+stn2+" are: \n"
    for train in trains:
        message+="\nName: "+ train["trainName"]+"\nTrain number:"+train["trainNo"]+"\nOperational: "+train["runsFromStn"]
    return message

def stnName_to_stnCode(stnName):
    stnName = stnName.upper()
    with open("stnCodeswithStnNames.txt", "r", encoding='utf8') as f:
        data_stream = f.read()
        list_of_elems = []
        
        # Load every comma separated string into list
        for elem in data_stream.strip(';').split(','):
            list_of_elems.append(elem)
        for elem in list_of_elems:
            if stnName == elem:
                stnName_index = list_of_elems.index(stnName)
                stnCode = list_of_elems[stnName_index-1]
                return stnCode

if __name__ == "__main__":
    print(trains_btwn_stations('VR', 'PLG'))