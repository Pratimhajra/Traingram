# coding: utf-8
# Work in Progress

from flask import Flask
from flask import request	
from flask import make_response, jsonify

import os

from RailRider import *

# Flask app should start in global layout
app = Flask(__name__)
DEVELOPER_ACCESS_TOKEN = os.getenv("DEVELOPER_ACCESS_TOKEN")

@app.route('/', methods=['POST'])
def webhook():
    start_time = time.time()
    req = request.get_json(silent=True, force=True)
    
    getIntent = req.get("queryResult").get("intent").get("displayName")
    if(getIntent == "LIVE_STATUS"):
        getParams = req.get("queryResult").get("parameters")
        TrainNo = int(getParams.get("trainNumber"))
        StnName = getParams.get("stnName")
        getQuery = req.get("queryResult").get("queryText")
        message = live_status(TrainNo, StnName)
    #elif(getIntent == "TRAINS_BETWEEN_STATIONS"):
    response_dict = {'fulfillmentText': message,
    "messages": [
        {
            "displayText": message,
            "platform": "google",
            "textToSpeech": message,
            "type": "simple_response"
        }
    ]
    }


    r = make_response((jsonify(response_dict)))
    r.headers['Authorization'] = 'Bearer ' + DEVELOPER_ACCESS_TOKEN
    r.headers['Content-Type'] = 'application/json'
    return r
    

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5002))

	print("Starting app on port %d" % port)

	app.run(debug=False, port=port, host='0.0.0.0')
