# coding: utf-8

# Not ready!
# Finish NTES.py functions before moving to this part.
import time
from flask import Flask
from flask import request	
from flask import make_response, jsonify

import fileinput
import sys

import os.path
import requests
from requests.exceptions import ReadTimeout, ConnectTimeout
import json

#from NTES import live_status
#from NTES import *
from test2 import *
# Move NTES.py to flask-webhook/ after completing NTES functions


# Flask app should start in global layout
app = Flask(__name__)
#DEVELOPER_ACCESS_TOKEN = os.getenv("DEVELOPER_ACCESS_TOKEN")
#session = requests.Session()
#session.get("https://enquiry.indianrail.gov.in/ntes/IamAlive")



@app.route('/', methods=['POST'])
def webhook():
    start_time = time.time()
    req = request.get_json(silent=True, force=True)
    #print("Request:")
    
    getIntent = req.get("queryResult").get("intent").get("displayName")
    if(getIntent == "LIVE_STATUS"):
        getParams = req.get("queryResult").get("parameters")
        TrainNo = getParams.get("trainNumber") # trainNumber returned as a list
        StnName = getParams.get("stnName")
        getQuery = req.get("queryResult").get("queryText")

        print(getQuery, "\n", TrainNo, "\n", StnName)
        message = live_status(TrainNo, StnName)
    #elif(getIntent == "TRAINS_BETWEEN_STATIONS"):


    r = make_response((jsonify({'fulfillmentText': message})))
    #r.headers['Authorization'] = 'Bearer ' + DEVELOPER_ACCESS_TOKEN
    r.headers['Content-Type'] = 'application/json'
    return r
    

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5002))

	print("Starting app on port %d" % port)

	app.run(debug=True, port=port, host='0.0.0.0')
