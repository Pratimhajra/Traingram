import json
import requests
import time
from time import gmtime, strftime
from datetime import date, datetime
import calendar
from json.decoder import JSONDecodeError
import textwrap

def live_status(TrainNo, stnName):
    stnCode = stnName_to_stnCode(stnName)
    today=datetime.now()
    date=today.strftime("%d-%m-%Y")
    delay = 9999 # Default value of delay
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
    #print(len(response.text))
    if len(response.text) == 0: # Response empty
        message = "Your PNR number is invalid. Please verify it or try again later."
        return message

    data = response.json() #json.loads(data)
    doj = data.get('doj')
    trainname=data.get('train_name')
    clas = data.get('class1')
    total_passengers = data.get('total_passengers')
    from_station = data.get('from_station').get('name')
    to_station = data.get('to_station').get('name')
    total_fare = str(data.get('total_fare'))
    cnf = data.get('passengers')
    message = ""
    for i in cnf:
    	Passenger_no,booking_status,current_status = i['no'],i['booking_status'],i['booking_status']
    	message += f"NO.{Passenger_no}\nBooking_status:{booking_status}\nCurrent_status:{current_status}\n"
    #message = f"Date of journey: {doj}\nTrain Name: {trainname}\nClass: {clas}\nTotal Passengers: {total_passengers}\nFrom Station: {from_station}\nTo Station: {to_station}\nTotal Fare: {total_fare}" 
    return(message)
    

def stnName_to_stnCode(stnName):
    """
    Returns Station Code for input Station Name
    """
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


def trains_btwn_stations(stn1, stn2):
    today=datetime.now()
    date=today.strftime("%d-%b-%y")
    stnc1 = stnName_to_stnCode(stn1)
    stnc2 = stnName_to_stnCode(stn2)
    dayc = day_in_short()
    response=requests.get(f"https://api.railrider.in/api_rr_v3_test.php?page_type=train_between_station&from={stn1}+-+{stnc1}&to={stn2}+-+{stnc2}&day={dayc}")
    try:
        data=response.json()
    except JSONDecodeError:
        return "Multiple Stations exist!"

    num = data['total_results']
    #train_list = []
    message =""
    i=0
    while i < num:
        var=data['result'][i]['train_name']
        message += var + "\n"
        #print(var)
        i=i+1
    return message


def live_station(stnName, hrs=2):
    date = strftime("%d", gmtime())
    curr = datetime.now().strftime("%H:%M")
    tim = curr.split(":")
    timh = int(tim[0])
    time_till = timh + hrs
    stnCode = stnName_to_stnCode(stnName)
    response = requests.get(f"http://whereismytrain.in/cache/live_station?hrs={hrs}&station_code={stnCode}")
    data = response.json()
    message = f"Trains at {stnName} within next {hrs} hours are :\n"
    message_template = textwrap.dedent("""
    Train: {name}
    Train Number:{number}
    Departure Time:{Dtime}
    Platform Number: {platform}
    Delay: {delay}
    """)
    for train in data.get('live_station_info', []):
        train_no = train.get('train_no')
        platform = train.get('platform')
        dep = train.get('actDep')
        dept = dep.split(",")
        dep_hr = dep.split(":")
        deph = int(dep_hr[0])
        if deph <= time_till:
            delay = train.get('delay_in_arrival') # "Right time" or "XX:XX"
            if delay == "RIGHT TIME":
                delay = "On time"
            else:
                hrs, mins = delay.split(':')
                if hrs == '00':
                    delay = f"{mins} mins late"
                else:
                    delay = f"{hrs} hours and {mins} mins late"
            Dep_time = time.strftime( "%I:%M %p",time.strptime(dept[0], "%H:%M"))
            name = train.get('train_name')
            message += message_template.format(name=name, number=train_no,Dtime=Dep_time, platform=platform, delay=delay)
    return message

def day_in_short():
    my_date = date.today()
    day = calendar.day_name[my_date.weekday()]
    #If the initials of day are not repeating then return first letter
    #e.g    Tuesday and Thursday starts with so we return Tu for Tuesday and Th for Thurday
    #   and for Monday we return M 
    if(day =='Monday' or day == 'Wednesday' or day == 'Friday'):
        day_code = day[0]
    else:
        day_code = day[0:2]
    return day_code

if __name__ == '__main__':
    live_status(19016, 'Palghar')
    PNR_status('8108432697') #RAC 2612829606
    trains_btwn_stations('VIRAR','PALGHAR')
    live_station('Palghar')
