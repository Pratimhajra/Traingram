import json
import requests
import time
from time import gmtime, strftime
from datetime import date, datetime
import calendar
from json.decoder import JSONDecodeError
from database import session, StationInfo,TrainInfo
from pure_python_parser import parse_json


def live_status(TrainNo, stnName):
    stnCode = stnName_to_stnCode(stnName)
    today=datetime.now()
    date=today.strftime("%d-%m-%Y")
    delay = 9999         # Default value of delay
    delay = from_day(TrainNo,stnCode,date,1)
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
        return station_list # Return list of similar named stations
    return stations[0].station_code # Return the single station's station code
        


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
                            "title": f"{TrainName} ({TrainNumber})"}
        message.append(AllTrainDetails)

    if(len(trains) == 1):
        message = "\nName: "+ TrainName+"\nTrain number:"+TrainNumber+"\nDeparts from: "+Source_Stn+"\nwill arrive in"+Destination_Stn
    return message


def live_station(stnName, hrs=2):
    CurrentHour = int(datetime.now().strftime('%H')) #Converting to integer value
    time_till = CurrentHour + hrs                       #Calculating the maximum search limit that is 4 hours
    stnCode = stnName_to_stnCode(stnName)               
    response = requests.get(f"http://whereismytrain.in/cache/live_station?hrs={hrs}&station_code={stnCode}")
    data = response.json()
    message = []
    
    for train in data.get('live_station_info', []):
        train_no = train.get('train_no')
        platform = train.get('platform')
        DepartTime = train.get('actDep').split(',') # HH:MM
        DepartHour = int(DepartTime[0].split(':')[0]) # HH
        if DepartHour <= time_till and DepartHour >= CurrentHour: #Generating the list of trains within user specified time
            delay = train.get('delay_in_arrival') # "Right time" or "XX:XX"
            print(delay)
            if delay == "RIGHT TIME" or delay is None:                   
                delay = "On time"
            else:
                hrs, mins = delay.split(':')
                if hrs == '00':
                    delay = f"{mins} mins late"
                else:
                    delay = f"{hrs} hours and {mins} mins late"
            DepartTimeFinal = time.strftime("%I:%M %p", time.strptime(DepartTime[0], "%H:%M"))
            name = train.get('train_name')
            print("Name:")
            All_train_details = {"optionInfo": {"key": f"{train_no}"},
                                "description": f"Will arrive on platform : {platform} at {DepartTimeFinal}",
                                "title": f"{name}"}
            print("All_train_details: ", All_train_details)
            message.append(All_train_details)
    return message


def from_day(TrainNo,stnCode,date,from_day_value):
    formattedDate = int(date.split("-")[0])
    response=requests.get(f"http://whereismytrain.in/cache/live_status?date={date}&from_day={from_day_value}&train_no={TrainNo}")
    data=response.json()
    for station in data.get('days_schedule'):
        if(station.get('station_code') == stnCode):
            arrival_date = station.get('actual_arrival_date')
            arrival_date = int(arrival_date.split(" ")[0])
            if(arrival_date == formattedDate):
                return station.get('delay_in_arrival')
            else:
                from_day_value+=1
                return from_day(stnName,trainNo,from_day_value)


def trainName_to_trainCode(trainName):      
    trainList=[]  
    trains = session.query(TrainInfo).filter(TrainInfo.train_name.like(f"%{trainName}%")).all()  
    if(len(trains)==1): #Returns train no if list contains one item 
        return trains[0].train_no      
    else:  
        for train in trains:  
            trainNo=train.train_no  
            trainName=train.train_name  
            trainDict={"optionInfo" : {"key" : f"{trainNo}"},  
                       "description" : f"{trainNo}",  
                       "title" : f"{trainName}"}  
            trainList.append(trainDict)  
        return trainList  


if __name__ == '__main__':
    print(live_status(19016, 'Palghar'))
    #PNR_status('8108432697')     #RAC 2612829606
    #trains_btwn_stations('BORIVALI','PALGHAR')
    #live_station('Palghar')