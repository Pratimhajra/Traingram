# coding: utf-8
# Work in Progress

from flask import Flask
from flask import request	
from flask import make_response, jsonify

import os

from RailRider import *
from response_templates import list_response, simple_response

# Flask app should start in global layout
app = Flask(__name__)
DEVELOPER_ACCESS_TOKEN = os.getenv("DEVELOPER_ACCESS_TOKEN")

@app.route('/', methods=['POST'])
def webhook():
    start_time = time.time()
    req = request.get_json(silent=True, force=True)
    getIntent = req.get("queryResult").get("intent").get("displayName")
    if(getIntent == "LIVE_STATUS"):
        my_response = _process_live_status(req)
    elif(getIntent == "TRAINS_BETWEEN_STATIONS"):
        my_response = _process_trains_btwn_stations(req)
    elif(getIntent == "PNR_STATUS"):
        my_response = _process_pnr_station(req)
    elif(getIntent == "LIVE_STATION"):
        my_response = _process_live_station(req)

    r = make_response((jsonify(my_response)))
    r.headers['Authorization'] = 'Bearer ' + DEVELOPER_ACCESS_TOKEN
    r.headers['Content-Type'] = 'application/json'
    return r
    

def _process_live_status(req):
    getParams = req.get("queryResult").get("parameters")
    TrainNo = int(getParams.get("trainNumber"))
    StnName = getParams.get("stnName")
    stations = stnName_to_stnCode(StnName)
    if(isinstance(stations, list)): # Check if response from the function is a list of dicts
        list_response['payload']['google']['systemIntent']['data']['listSelect']['title'] = "Stations"
        list_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Select station"
        list_response['payload']['google']['systemIntent']['data']['listSelect']['items'] = stations
        return list_response
    else:
        message = live_status(TrainNo, StnName)
        simple_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = message
        simple_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['displayText'] = message
        return simple_response

def _process_trains_btwn_stations(req):
    getParams = req.get("queryResult").get("parameters")
    sourceStation = getParams.get("sourceStation")
    destinationStation = getParams.get("destinationStation")
    title = f"Trains from {sourceStation} to {destinationStation}"
    textToSpeech = f"Here are trains going from {sourceStation} to {destinationStation}"
    source_station = stnName_to_stnCode(sourceStation)
    destination_station = stnName_to_stnCode(destinationStation)
    if(isinstance(list_of_stnCode_src, list)):
        list_response['payload']['google']['systemIntent']['data']['listSelect']['title'] = "Stations"
        list_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = f"Here are the stations I found"
        list_response['payload']['google']['systemIntent']['data']['listSelect']['items'] = list_of_stnCode_src
        return list_response
    if(isinstance(list_of_stnCode_destn, list)):   
        list_response['payload']['google']['systemIntent']['data']['listSelect']['title'] = "Stations"
        list_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = f"Here are the stations I found"
        list_response['payload']['google']['systemIntent']['data']['listSelect']['items'] = list_of_stnCode_dest
        return list_response
    else:
        list_of_trains = trains_btwn_stations(sourceStation, destinationStation)
        if(isinstance(list_of_trains, list)): # Check if response from the function is a list of dicts
            list_response['payload']['google']['systemIntent']['data']['listSelect']['title'] = title
            list_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = textToSpeech
            list_response['payload']['google']['systemIntent']['data']['listSelect']['items'] = list_of_trains
            return list_response
        else:
            simple_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = list_of_trains
            simple_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['displayText'] = list_of_trains
            return simple_response

def _process_pnr_station(req):
    getParams = req.get("queryResult").get("parameters")
    pnr = getParams.get("pnr")
    message = "Here's the PNR information: "
    displayText = PNR_status(pnr)
    simple_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = message
    simple_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['displayText'] = displayText
    return simple_response

def _process_live_station(req):
    getParams = req.get("queryResult").get('parameters')
    stnName = getParams.get("stnName")
    title = f"Trains at {stnName}"
    textToSpeech = f"Here are trains at {stnName}"
    displayText = live_station(stnName)
    if(isinstance(list_of_trains, list)): # Check if response from the function is a list of dicts
        list_response['payload']['google']['systemIntent']['data']['listSelect']['title'] = title
        list_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = textToSpeech
        list_response['payload']['google']['systemIntent']['data']['listSelect']['items'] = list_of_trains
        return list_response
    else:
        simple_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = list_of_trains
        simple_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['displayText'] = list_of_trains
        return simple_response

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5002))

	print("Starting app on port %d" % port)

	app.run(debug=False, port=port, host='0.0.0.0')
