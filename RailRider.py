import json
import requests
import time
import datetime
from json.decoder import JSONDecodeError

def live_status(TrainNo, stnName):
    stnCode = stnName_to_stnCode(stnName)
    today=datetime.datetime.now()
    date=today.strftime("%d-%b-%y")
    response=requests.get(f"https://api.railrider.in/api_rr_v3_test.php?page_type=live_train_status&train_num={TrainNo}&journey_station={stnCode}&journey_date={date}")
    data=response.json()
    var=data.get('delay_arr')
    return var


def PNR_status(pnr):
    payload = {'pnr_post':pnr}
    response=requests.post("https://www.railrider.in/api/ajax_pnr_check.php", data=payload)
    count = 1
    if(count<=2):
        try:
            data = response.json()
        except JSONDecodeError:
            print("JSONDecodeError... Retrying... Attempt: ", count)
            data = response.json()
    #data = response.json() #json.loads(data)
    doj = data.get('doj')
    trainname=data.get('train_name')
    clas = data.get('class1')
    total_passengers = data.get('total_passengers')
    from_station = data.get('from_station').get('name')
    to_station = data.get('to_station').get('name')
    total_fare = str(data.get('total_fare'))
    #message = "The PNR status is:\n"+"Date of journey: "+doj+"\nTrain_name: "+trainname+"\nclass: "+clas+"\nTotal_passengers: "+total_passengers+"\nFrom_station:"+from_station+"\n To_station: "+to_station#+"\nTotal_fare: "+total_fFRare
    message = f"The PNR status is:\nDate of journey: {doj}\nTrain Name: {trainname}\nClass: {clas}\nTotal Passengers: {total_passengers}\nFrom Station: {from_station}\nTo Station: {to_station}\nTotal Fare: {total_fare}" 
    print(message)
    #return(message)
    

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


if __name__ == '__main__':
    live_status(19016, 'Palghar')
    PNR_status('8108432697')
    #print(x)