import json
import requests
import time
from time import gmtime, strftime
from datetime import date, datetime
import calendar
from json.decoder import JSONDecodeError
from database import session, StationInfo
from pure_python_parser import parse_json


def live_status(TrainNo, stnName):
    stnCode = stnName_to_stnCode(stnName)
    today=datetime.now()
    date=today.strftime("%d-%m-%Y")
    delay = 9999         # Default value of delay
    response=requests.get(f"http://whereismytrain.in/cache/live_status?date={date}&train_no={TrainNo}")
    data=response.json()
    for station in data.get('days_schedule'):
        if(station.get('station_code') == stnCode):
            delay = station.get('delay_in_arrival')
    if delay is None or delay == 0:
        return "The train is on time!"
    elif delay != 9999:
        message = f"The train is {delay} mins late"
        return message
    else:
        return f"The given train doesn't run through {stnName}"


def PNR_status(pnr):
    payload = {'pnr_post':pnr}
    response=requests.post("https://www.railrider.in/api/ajax_pnr_check.php", data=payload)
    count = 1
    
    if len(response.text) == 0:       # Response empty
        message = "Your PNR number is invalid. Please verify it or try again later."
        return message
    
    data = response.json()
    passengers = data.get('passengers')
    message = ""
    for passenger in passengers:
    	Passenger_no, booking_status, current_status = passenger['no'], passenger['booking_status'], passenger['current_status']
    	message += f"Passenger {Passenger_no}\nBooking_status:{booking_status}\nCurrent_status:{current_status}\n"
    return(message)
    

def stnName_to_stnCode(stnName):
    """
    Returns Station Code for input Station Name
    """
    station_list = []
    stations = session.query(StationInfo).filter(StationInfo.title.like(f"%{stnName}%")).all()
    if len(stations) > 1:
        for station in stations:
            stnCode = station.station_code
            stnTitle = station.title
            station_dict = {"optionInfo": {"key": f"{stnCode}"},
                            "description": f"{stnCode}",
                            "title": f"{stnTitle}"}
            station_list.append(station_dict)
    if len(stations) == 1:
        station_list = f"{stnCode}"
    return station_list # Return list of similar named stations
    #return stations[0].station_code # Return the single station's station code
        


def trains_btwn_stations(stn1, stn2, viaStn="null", trainType="ALL"):
    base_URL = "https://enquiry.indianrail.gov.in/ntes/"
    message = []
    stn1 = stnName_to_stnCode(stn1)
    stn2 = stnName_to_stnCode(stn2)
    query_url = base_URL+f"NTES?action=getTrnBwStns&stn1={stn1}&stn2={stn2}&trainType={trainType}"
    
    if(viaStn != "null"):
        viaStn = stnName_to_stnCode(viaStn)
        query_url = query_url+f"&viaStn={viaStn}"
    
    r = requests.get(query_url)
    json_data = parse_json(r.text, ["runsOnDays", "trnName"])
    variable = list(json_data.keys())[0]
    trains = json_data[variable]["trains"]["direct"]
    
    for train in trains:
        TrainNumber = train["trainNo"]
        TrainName = train["trainName"]
        Source_Stn = train["fromStn"]
        Destination_Stn = train["toStn"]
        AllTrainDetails = {"optionInfo": {"key": f"{TrainNumber}"},
                            "description": f"{stn1} → {stn2}",
                            "title": f"{TrainName} ({TrainNumber})"}
        message.append(AllTrainDetails)

    if(len(trains) == 1):
        message = "\nName: "+ TrainName+"\nTrain number:"+TrainNumber+"\nDeparts from: "+Source_Stn+"\nwill arrive in"+Destination_Stn
    return message


def live_station(stnName, hrs=2):
    date = strftime("%d", gmtime())
    CurrentTime = datetime.now().strftime('%H:%M')      #Taking the time when user call the function
    TimeSplit = CurrentTime.split(":")                  #spliting the time to get hour
    HourTime = int(TimeSplit[0])                        #Converting to integer value
    time_till = HourTime + hrs                          #Calculating the maximum search limit that is 4 hours
    stnCode = stnName_to_stnCode(stnName)               
    response = requests.get(f"http://whereismytrain.in/cache/live_station?hrs={hrs}&station_code={stnCode}")
    data = response.json()
    message = []
    for train in data.get('live_station_info', []):
        train_no = train.get('train_no')
        platform = train.get('platform')
        DepartDateTime = train.get('actDep')
        DepartTime = DepartDateTime.split(",")
        DepartHourMin = DepartDateTime.split(":")
        DepartHour = int(DepartHourMin[0])
        if DepartHour <= time_till and DepartHour >= HourTime:      #Generating the list of trains within user specified time
            delay = train.get('delay_in_arrival')                   # "Right time" or "XX:XX"
            if delay == "RIGHT TIME":                   
                delay = "On time"
            else:
                hrs, mins = delay.split(':')
                if hrs == '00':
                    delay = f"{mins} mins late"
                else:
                    delay = f"{hrs} hours and {mins} mins late"
            DepartTimeFinal = time.strftime( "%I:%M %p",time.strptime(DepartTime[0], "%H:%M"))
            name = train.get('train_name')
            All_train_details = {"optionInfo": {"key": f"{train_no}"},
                                "description": f"Will arrive on platform : {platform} at {DepartTimeFinal}\n Delay : {delay}",
                                "title": f"{name}"}
            message.append(All_train_details)
    return message


def day_in_short():
    my_date = date.today()
    day = calendar.day_name[my_date.weekday()]
    '''
    If the initials of day are not repeating then return first letter
    e.g    Tuesday and Thursday starts with so we return Tu for Tuesday and Th for Thurday
           and for Monday we return M 
    '''
    if(day =='Monday' or day == 'Wednesday' or day == 'Friday'):
        day_code = day[0]
    else:
        day_code = day[0:2]
    return day_code


if __name__ == '__main__':
    live_status(19016, 'Palghar')
    PNR_status('8108432697')     #RAC 2612829606
    stnName_to_stnCode('BORIVALI')
    trains_btwn_stations('BORIVALI','PALGHAR')
    live_station('Palghar')