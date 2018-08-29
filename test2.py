import requests
import time
import datetime
import json
def live_status(TrainNo, stnCode):
	today=datetime.datetime.now()
	date=today.strftime("%d-%b-%y")
	response=requests.get(f"https://api.railrider.in/api_rr_v3_test.php?page_type=live_train_status&train_num={TrainNo}&journey_station={stnCode}&journey_date={date}")
	data=response.json()
	var=data['delay_arr']
	print(var)
#def trains_btwn_stations(stn1, stn2, viaStn="null", trainType="ALL"):

if __name__ == '__main__':
	live_status(19016,'PLG')