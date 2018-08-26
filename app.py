# coding: utf-8

# Not ready!
# Finish NTES.py functions before moving to this part.

from flask import Flask
from flask import request	
from flask import make_response

import os
import requests
import json

#from NTES import live_status
from NTES import *

# Move NTES.py to flask-webhook/ after completing NTES functions


# Flask app should start in global layout
app = Flask(__name__)
DEVELOPER_ACCESS_TOKEN = os.getenv("DEVELOPER_ACCESS_TOKEN")

@app.route('/', methods=['POST'])
def webhook():
    
    req = request.get_json(silent=True, force=True)
    
    getIntent = req.get("queryResult").get("intent").get("displayName")
    if(getIntent == "LIVE_STATUS"):
        getParams = req.get("queryResult").get("parameters")
        TrainNo = int(getParams.get("trainNumber"))
        StnName = getParams.get("stnName")
        getQuery = req.get("queryResult").get("queryText")
        print(getQuery, "\n", "TrainNo: ",TrainNo, "\n", "StnName: ",StnName)
        #message = live_status(TrainNo, StnName)
        #print("Message: ", message)
    #elif(getIntent == "TRAINS_BETWEEN_STATIONS"):

    my_result = {
  "fulfillmentText": "Train is on time",
  "fulfillmentMessages": [
    {
      "card": {
        "title": "card title",
        "subtitle": "card text",
        "imageUri": "https://assistant.google.com/static/images/molecule/Molecule-Formation-stop.png",
        "buttons": [
          {
            "text": "button text",
            "postback": "https://assistant.google.com/"
          }
        ]
      }
    }
  ],
  "source": "https://traingram.herokuapp.com/",
  "payload": {
    "google": {
      "expectUserResponse": "true",
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": "The train is on time"
            }
          }
        ]
      }
    },
    "facebook": {
      "text": "Hello, Facebook!"
    },
    "slack": {
      "text": "This is a text response for Slack."
    }
  },
  "outputContexts": [
    {
      "name": "projects/${PROJECT_ID}/agent/sessions/${SESSION_ID}/contexts/context name",
      "lifespanCount": 5,
      "parameters": {
        "param": "param value"
      }
    }
  ],
  "followupEventInput": {
    "name": "event name",
    "languageCode": "en-US",
    "parameters": {
      "param": "param value"
    }
  }
}


    """my_result =  {
        "fulfillmentText": message,
        "source": "Traingram-Dialogflow-Webhook",
        "payload": {
            "google":{
                "textToSpeech": message
            }
        },
        "status":200,
        "errorType":"success"
    }
    """
    res = json.dumps(my_result, indent=4)
    r = make_response(res)
    r.headers['Authorization'] = 'Bearer ' + DEVELOPER_ACCESS_TOKEN
    r.headers['Content-Type'] = 'application/json'
    return r
    

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5002))

	print("Starting app on port %d" % port)

	app.run(debug=False, port=port, host='0.0.0.0')
