import json
import requests
import time
from time import gmtime, strftime
from datetime import date, datetime
import calendar
from json.decoder import JSONDecodeError
from database import session, StationInfo


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
            station_list.append(station.station_code)
        return station_list # Return list of similar named stations
    return stations[0].station_code # Return the single station's station code
        


def trains_btwn_stations(stn1, stn2,trainTypeA=None,trainTypeB=None,trainTypeC=None):
    date = strftime("%d", gmtime())
    stnc1 = stnName_to_stnCode(stn1)
    stnc2 = stnName_to_stnCode(stn2)
    dayInShort = day_in_short()                             #Calculating short names for week days
    CurrentTime = datetime.now().strftime('%H:%M')          #Taking the time when user call the function
    TimeSplit = CurrentTime.split(":")                      #spliting the time to get hour
    HourTime = int(TimeSplit[0])                            #Converting to integer value
    time_till = HourTime + 4                                #Calculating the maximum search limit that is 4 hours
    noFilter=0
    if(trainTypeA==trainTypeB and trainTypeB==trainTypeC and trainTypeC==None):
        noFilter=1
    response=requests.get(f"https://api.railrider.in/api_rr_v3_test.php?page_type=train_between_station&from={stn1}+-+{stnc1}&to={stn2}+-+{stnc2}&day=Sa")
    try:
        data=response.json()
    except JSONDecodeError:
        return "Multiple Stations exist!"

    TotalResults = data['total_results']
    FirstTrain = data['result'][0]['trainno']
    train_numbers = []
    ActualTrains = 1
    i = 0
    #Calculating the number of trains in a day between station 1  and  station 2
    while i<TotalResults:
        if i == 0:
            i += 1
        if FirstTrain != data['result'][i]['trainno']:
            ActualTrains+=1
            i += 1
        if FirstTrain == data['result'][i]['trainno']:  
            break
    i = 0
    message = []
    while i < ActualTrains:
        AreTrainsAvail = 0
        TrainName = data['result'][i]['train_name']
        if(data['result'][i]['train_type']==trainTypeA or data['result'][i]['train_type']==trainTypeB or data['result'][i]['train_type']==trainTypeC or noFilter):
            
            DepartTime1 = data['result'][i]['from_dep_time']            #Train's departure time from station 1
            ArriveTime2 = data['result'][i]['to_dep_time']              #Train's arrival time at station 2
            time24 = time.strptime(DepartTime1, "%H:%M")                #Time in 24 hour fashion
            DepartureTime = time.strftime( "%H:%M", time24 )
            DepartHour = str(DepartureTime)                             #Converting tuple to string
            TimeSplitList = DepartHour.split(":")   
            TimeInHours = int(TimeSplitList[0])                         #Converting string into integer
            DepartTime1 = time.strftime( "%I:%M %p", time24 )           #Conversion from 24 hr. fashion to 12 hr. fashion for Departure time from station 1
            ArriveTime2 = time.strftime( "%I:%M %p",time.strptime(ArriveTime2, "%H:%M")) #Conversion from 24 hr. fashion to 12 hr. fashion for Arrival time at station 2
            TrainNumber = data['result'][i]['trainno']
            if time_till >= TimeInHours and TimeInHours>=HourTime:  
                AllTrainDetails = {"optionInfo": {"key": f"{TrainNumber}"},
                                    "description": f"Departsa from {stn1} at {DepartTime1}\nWill arrive in {stn2} by {ArriveTime2}",
                                    "title": f"{TrainName}"}
                message.append(AllTrainDetails)                         #Concatinating the dictionaries
                AreTrainsAvail +=1                                 
        i+=1
    if  AreTrainsAvail == 0:                                            #Checking for NULL directionary
        message = "No trains available in next 4 hours"
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
    trains_btwn_stations('VIRAR','PALGHAR')
    live_station('Palghar')