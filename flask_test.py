import requests
import json

request_json = """{
  "responseId": "6e1e764e-6bbe-4c38-a210-0750540c447e",
  "queryResult": {
    "queryText": "live status for 19016 at Palghar",
    "action": "LIVE_STATUS",
    "parameters": {
      "trainNumber": [
        19016
      ],
      "trainName": "",
      "stnName": "Palghar"
    },
    "allRequiredParamsPresent": true,
    "intent": {
      "name": "projects/traingram-b4327/agent/intents/2eda581d-a287-415f-8b18-52ce6e1c23ae",
      "displayName": "LIVE_STATUS"
    },
    "intentDetectionConfidence": 0.79,
    "languageCode": "en"
  },
  "webhookStatus": {
    "message": "Webhook execution successful"
  }
}"""

payload = json.loads(request_json) # Convert string into an object
headers = {'Content-type':'application/json'} # Add headers since they're required
flask_url = "http://localhost:5000" # URL of the flask server
r = requests.post(flask_url, json=payload)

print(r.text)