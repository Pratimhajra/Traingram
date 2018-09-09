import requests
from pure_python_parser import parse_json
import time
import json
from database import session, StationInfo

base_URL = "https://enquiry.indianrail.gov.in/ntes/"

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
    """
    Returns Station Code for input Station Name
    """
    station_list = []
    stations = session.query(StationInfo).filter(StationInfo.title.like(f"%{stnName}%")).all()
    print(stations)
    if len(stations) > 1:
        for station in stations:
            stnCode = station.station_code
            stnTitle = station.title
            station_dict = {"optionInfo": {"key": f"{stnCode}"},
                            "description": f"{stnCode}",
                            "title": f"{stnTitle}"}
            station_list.append(station_dict)
        return station_list # Return list of similar named stations
    return stations[0].station_code # Return the single station's station code

if __name__ == "__main__":
    print(trains_btwn_stations('palghar', 'borivali'))