# coding: utf-8

# Not ready!
# Finish NTES.py functions before moving to this part.

from flask import Flask
from flask import request	
from flask import make_response

import fileinput
import sys

import os.path
import requests
import json

# Move NTES.py to flask-webhook/ after completing NTES functions
#from NTES import live_status

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    
    req = request.get_json(silent=True, force=True)
    #print("Request:")
    
    getIntent = req.get("queryResult").get("intent").get("displayName")
    if(getIntent == "LIVE_STATUS"):
        getParams = req.get("queryResult").get("parameters")
        TrainNo = getParams[0][0] #trainNumber returned as a list
        StnName = getParams[1]
        getQuery = req.get("queryResult").get("queryText")
        print(getQuery)
        message = live_status(TrainNo, StnName)
    elif(getIntent == "TRAINS_BETWEEN_STATIONS"):
        
    
    
    my_result =  {
        "fulfillmentText": message,
        "source": "Traingram-Dialogflow-Webhook",
        "payload": {
            "telegram":{
                "text": message
            }
        }
    }
    res = json.dumps(my_result, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
    

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5002))

	print("Starting app on port %d" % port)

	app.run(debug=True, port=port, host='0.0.0.0')
