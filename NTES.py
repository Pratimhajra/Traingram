import requests
from pure_python_parser import parse_json

base_URL = "https://enquiry.indianrail.gov.in/ntes/"

def live_status(TrainNo, stnCode):
    with requests.session() as s:
        r1 = s.get(base_URL+"IamAlive")
        JSESSIONID = str(r1.cookies.get('JSESSIONID'))
        SERVERID = str(r1.cookies.get('SERVERID'))
        print(JSESSIONID,SERVERID)
        s.get(base_URL+f"SearchTrain?trainNo={TrainNo}")
        
        cookies = {
            'JSESSIONID': JSESSIONID,
            'SERVERID': SERVERID,
        }

        r = s.get(f"https://enquiry.indianrail.gov.in/ntes/NTES?action=getTrainData&trainNo={TrainNo}", cookies=cookies)
        json_data = parse_json(r.text, ["runsOnDays", "trnName"])
        # grab everything nested inside first key, i.e. _variable_<unixtimestamp>
        variable = list(json_data.keys())[0]
        stations = json_data[variable][0]["rakes"][0]["stations"]
        for station in stations:
            if(station["stnCode"] == stnCode):
                return station["delayArr"]

def live_station(viaStn, toStn="null", hrs="2", trainType="ALL"):
    r = requests.get(base_URL+f"NTES?action=getTrainsViaStn&viaStn={viaStn}&toStn={toStn}&withinHrs={hrs}&trainType={trainType}")
    json_data = parse_json(r.text, ["runsOnDays", "trnName"])
    variable = list(json_data.keys())[0]
    trains = json_data[variable]["allTrains"]
    print("The Trains available are:")
    for train in trains:
    	print(train["trainName"])

    #TODO: Parse response and return data

def trains_btwn_stations(stn1, stn2, viaStn="null", trainType="ALL"):
    query_url = base_URL+f"NTES?action=getTrnBwStns&stn1={stn1}&stn2={stn2}&trainType={trainType}"
    if(viaStn != "null"):
        query_url = query_url+f"&viaStn={viaStn}"
    r = requests.get(query_url)

    json_data = parse_json(r.text, ["runsOnDays", "trnName"])
    return json_data
    #TODO: Parse response and return parsed data

def train_schedule(TrainNo, validOnDate=""):
    with requests.session() as s:
        r1 = s.get(base_URL+"IamAlive")
        JSESSIONID = str(r1.cookies.get('JSESSIONID'))
        SERVERID = str(r1.cookies.get('SERVERID'))
        print(JSESSIONID,SERVERID)
        s.get(base_URL+f"SearchFutureTrain?trainNo={TrainNo}")
        
        cookies = {
            'JSESSIONID': JSESSIONID,
            'SERVERID': SERVERID,
        }
        r = s.get(base_URL+f"FutureTrain?action=getTrainData&trainNo={TrainNo}&validOnDate={validOnDate}", cookies=cookies)
    #TODO: Parse response and return data

def show_all_cancelled_trains():
    """We'll not be working with this function"""
    r = requests.get(base_URL+"NTES?action=showAllCancelledTrains")
    #print(r.text)
    data = parse_json(r.text, ["runOnDays", "trnName"])
    print(data)
    #TODO: Parse response and return data

def rescheduled_trains():
    """We'll not be working with this function"""
    r = requests.get(base_URL+"NTES?action=showAllRescheduledTrains")
    json_data = parse_json(r.text, ["runsOnDays", "trnName"])
    print(json_data)
    #TODO: Parse response and return data

def diverted_trains():
    """We'll not be working with this function"""
    r = requests.get(base_URL+"NTES?action=showAllDivertedTrains")
    json_data = parse_json(r.text, ["runsOnDays", "trnName"])
    print(json_data)
    
def avg_delay(TrainNo):
    """We'll not be working with this function"""
    with requests.session() as s:
        r1 = s.get(base_URL+"IamAlive")
        JSESSIONID = str(r1.cookies.get('JSESSIONID'))
        SERVERID = str(r1.cookies.get('SERVERID'))
        print(JSESSIONID,SERVERID)
        s.get(base_URL+f"SearchFutureTrain?trainNo={TrainNo}")
        
        cookies = {
            'JSESSIONID': JSESSIONID,
            'SERVERID': SERVERID,
        }
        r = s.get(base_URL+f"FutureTrain?action=getTrainDataForAvgDelay&trainNo={TrainNo}", cookies=cookies)
    #TODO: Parse response and return data

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
    #live_status("19016", "MMCT")
    #live_station('VR', toStn='PLG')
    #trains_btwn_stations('BCT', 'PBR')
    #train_schedule('19016')
    #show_all_cancelled_trains() #too long response
    #diverted_trains() #starts with obj15xxx, gives unknown identifier "function"
    #rescheduled_trains() #starts with obj15xxx, gives unknown identifier "function"
    #avg_delay('19016')
    print(stnName_to_stnCode("Porbandar"))