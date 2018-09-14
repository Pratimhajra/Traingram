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
    print(req)
    getIntent = req.get("queryResult").get("intent").get("displayName")
    if(getIntent == "LIVE_STATUS"):
        my_response = _process_live_status(req)
    elif(getIntent == "TRAINS_BETWEEN_STATIONS"):
        my_response = _process_trains_btwn_stations(req)
    elif(getIntent == "PNR_STATUS"):
        my_response = _process_pnr_station(req)
    elif(getIntent == "LIVE_STATIONS"):
        my_response = _process_live_station(req)
    elif(getIntent == "OPTIONS_LIVE_STATUS"):
        my_response = _process_options_live_status(req)
    elif(getIntent == "OPTIONS_LIVE_STATIONS"):
        my_response = _process_options_live_stations(req)
    elif(getIntent == "OPTIONS_TRAINS_BETWEEN_STATIONS"):
        my_response == _process_options_trains_btwn_stations(req)

    r = make_response((jsonify(my_response)))
    r.headers['Authorization'] = 'Bearer ' + DEVELOPER_ACCESS_TOKEN
    r.headers['Content-Type'] = 'application/json'
    return r
    

def _process_live_status(req):
    getParams = req.get("queryResult").get("parameters")
    TrainNo = int(getParams.get("trainNumber"))
    stnName = getParams.get("stnName")
    stations = stnName_to_stnCode(stnName)
    if(isinstance(stations, list)): # Check if response from the function is a list of dicts
        list_response['payload']['google']['systemIntent']['data']['listSelect']['title'] = "Stations"
        list_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Select station"
        list_response['payload']['google']['systemIntent']['data']['listSelect']['items'] = stations
        return list_response
    else:
        message = live_status(TrainNo, stnName=stnName)
        simple_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = message
        simple_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['displayText'] = message
        return simple_response

def _process_trains_btwn_stations(req):
    #NOTE: WE CANNOT PASS STATION CODES AND GET RESULTS.
    #FIGURE OUT HOW TO DIFFERENTIATE STN_CODES FROM STN_NAMES
    #OR CHANGE OptionInfo{"key": <value>}
    getParams = req.get("queryResult").get("parameters")
    sourceStation = getParams.get("sourceStation")
    destinationStation = getParams.get("destinationStation")
    title = f"Trains from {sourceStation} to {destinationStation}"
    textToSpeech = f"Here are trains going from {sourceStation} to {destinationStation}"
    source_station = stnName_to_stnCode(sourceStation)
    destination_station = stnName_to_stnCode(destinationStation)
    if(isinstance(source_station, list)):
        list_response['payload']['google']['systemIntent']['data']['listSelect']['title'] = "Stations"
        list_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = f"Here are the stations I found"
        list_response['payload']['google']['systemIntent']['data']['listSelect']['items'] = source_station
        return list_response
    if(isinstance(destination_station, list)):   
        list_response['payload']['google']['systemIntent']['data']['listSelect']['title'] = "Stations"
        list_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = f"Here are the stations I found"
        list_response['payload']['google']['systemIntent']['data']['listSelect']['items'] = destination_station
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
    stations = stnName_to_stnCode(stnName)
    print(stations, "\n", stnName)
    title = f"Trains at {stnName}"
    textToSpeech = f"Here are trains at {stnName}"
    live_station_output = live_station(stnName=stnName)
    print(live_station_output)
    print(len(live_station_output))
    if(isinstance(stations, list)): # Check if response from stationName to Code is a list
        list_response['payload']['google']['systemIntent']['data']['listSelect']['title'] = "Stations"
        list_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Please select a Station"
        list_response['payload']['google']['systemIntent']['data']['listSelect']['items'] = stations
        return list_response
    else:
        if isinstance(live_station_output, list):
            list_response['payload']['google']['systemIntent']['data']['listSelect']['title'] = title
            list_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = textToSpeech
            list_response['payload']['google']['systemIntent']['data']['listSelect']['items'] = live_station_output
            return list_response
        else:
            simple_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = live_station_output
            simple_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['displayText'] = live_station_output
            return simple_response

def _process_options_live_status(req):
    outputContexts = req.get("queryResult").get("outputContexts")
    stnCode = ""
    trainNumber = ""
    for context in outputContexts:
        # projects/${PROJECT_ID}/agent/sessions/${SESSION_ID}/contexts/actions_intent_option
        name = context.get('name')

        if name.endswith('actions_intent_option'):
            stnCode = context.get('parameters').get('OPTION')
        if name.endswith('session-vars'):
            trainNumber = int(context.get('parameters').get('trainNumber'))

    message = live_status(trainNumber, actualStationCode=stnCode)
    simple_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = message
    simple_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['displayText'] = message
    return simple_response
    
def _process_options_live_stations(req):
    outputContexts = req.get("queryResult").get("outputContexts")
    stnCode = ""

    for context in outputContexts:
        # projects/${PROJECT_ID}/agent/sessions/${SESSION_ID}/contexts/actions_intent_option
        name = context.get('name')

        if name.endswith('actions_intent_option'):
            stnCode = context.get('parameters').get('OPTION')

    stnName = stnCode_to_stnName(stnCode)
    title = f"Trains at {stnName}"
    textToSpeech = f"Here are trains at {stnName}"

    live_station_output = live_station(actualStationCode=stnCode)
    if isinstance(live_station_output, list):
        list_response['payload']['google']['systemIntent']['data']['listSelect']['title'] = title
        list_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = textToSpeech
        list_response['payload']['google']['systemIntent']['data']['listSelect']['items'] = live_station_output
        return list_response
    else:
        simple_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = live_station_output
        simple_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['displayText'] = live_station_output
        return simple_response


def _process_options_trains_btwn_stations(req):
    outputContexts = req.get("queryResult").get("outputContexts")
    for context in outputContexts:
        # projects/${PROJECT_ID}/agent/sessions/${SESSION_ID}/contexts/actions_intent_option
        name = context.get('name')
        # Four Cases:
        # sourceStation is Unique & destinationStation is non-unique (destination_station_list is a list)
        # sourceStation is non-unique & destinationStation is unique (source_station_list is a list)
        # sourceStation & destinationStation both are non-unique (both are lists) (station_code will be sourceStation 
        # which is a STATION_CODE)
        # sourceStation & destinationStation both are unique (already handled by _process_trains_btwn_station)
        # Get STATION_CODE of source_station and STATION_NAME of destination_station
        if name.endswith('actions_intent_option'):
            station_code = context.get('parameters').get('OPTION')
        if name.endswith('session-vars'):
            source_station = context.get('parameters').get('sourceStation')
            destination_station = context.get('parameters').get('destinationStation')

    source_station_list = stnName_to_stnCode(source_station)
    destination_station_list = stnName_to_stnCode(destination_station)
    if isinstance(source_station_list, list): # station_code is sourceStation's STATION_CODE
        #list_of_trains = trains_btwn_stations()
        list_response['payload']['google']['systemIntent']['data']['listSelect']['title'] = "Source Stations"
        list_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Please select source station"
        list_response['payload']['google']['systemIntent']['data']['listSelect']['items'] = source_station_list
        return list_response
    elif isinstance(destination_station_list, list):
        list_response['payload']['google']['systemIntent']['data']['listSelect']['title'] = "Source Stations"
        list_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Please select destination station"
        list_response['payload']['google']['systemIntent']['data']['listSelect']['items'] = destination_station_list
        return list_response

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5002))

	print("Starting app on port %d" % port)

	app.run(debug=False, port=port, host='0.0.0.0')
