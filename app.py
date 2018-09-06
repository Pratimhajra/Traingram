# coding: utf-8
# Work in Progress

from flask import Flask
from flask import request	
from flask import make_response, jsonify

import os

from RailRider import *
from list_response import list_response, simple_response

# Flask app should start in global layout
app = Flask(__name__)
DEVELOPER_ACCESS_TOKEN = os.getenv("DEVELOPER_ACCESS_TOKEN")

@app.route('/', methods=['POST'])
def webhook():
    start_time = time.time()
    req = request.get_json(silent=True, force=True)
    message = ""
    displayText = ""
    getIntent = req.get("queryResult").get("intent").get("displayName")
    if(getIntent == "LIVE_STATUS"):
        getParams = req.get("queryResult").get("parameters")
        TrainNo = int(getParams.get("trainNumber"))
        StnName = getParams.get("stnName")
        getQuery = req.get("queryResult").get("queryText")
        message = live_status(TrainNo, StnName)
        displayText = message
        my_response = simple_response
        simple_response['payload']['google']['richResponse']['items'][0]['textToSpeech'] = message
        simple_response['payload']['google']['richResponse']['items'][0]['displayText'] = message
        
        print(my_response)
    elif(getIntent == "TRAINS_BETWEEN_STATIONS"):
        getParams = req.get("queryResult").get("parameters")
        sourceStation = getParams.get("sourceStation")
        destinationStation = getParams.get("destinationStation")
        getQuery = req.get("queryResult").get("queryText")
        message = f"Here are trains from {sourceStation} to {destinationStation}"
        displayText = trains_btwn_stations(sourceStation, destinationStation)
        my_response = list_response
    elif(getIntent == "PNR_STATUS"):
        getParams = req.get("queryResult").get("parameters")
        pnr = getParams.get("pnr")
        message = "Here's the PNR information: "
        displayText = PNR_status(pnr)
        my_response = simple_response
        simple_response['payload']['google']['richResponse']['items'][0]['textToSpeech'] = message
        simple_response['payload']['google']['richResponse']['items'][0]['displayText'] = displayText
        

    r = make_response((jsonify(my_response)))
    r.headers['Authorization'] = 'Bearer ' + DEVELOPER_ACCESS_TOKEN
    r.headers['Content-Type'] = 'application/json'
    return r
    

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5002))

	print("Starting app on port %d" % port)

	app.run(debug=False, port=port, host='0.0.0.0')
