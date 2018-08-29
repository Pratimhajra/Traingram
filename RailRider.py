import requests
import time
import datetime


def live_status(TrainNo, stnName):
    stnCode = stnName_to_stnCode(stnName)
    today=datetime.datetime.now()
    date=today.strftime("%d-%b-%y")
    response=requests.get(f"https://api.railrider.in/api_rr_v3_test.php?page_type=live_train_status&train_num={TrainNo}&journey_station={stnCode}&journey_date={date}")
    data=response.json()
    var=data.get('delay_arr')
    return var


#def trains_btwn_stations(stn1, stn2, viaStn="null", trainType="ALL"):
    # WIP

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