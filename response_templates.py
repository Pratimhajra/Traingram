list_response ={
  "payload": {
    "google": {
      "expectUserResponse": True,
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": "Choose a item"
            }
          }
        ]
      },
      "systemIntent": {
        "intent": "actions.intent.OPTION",
        "data": {
          "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
          "listSelect": {
            "title": "Trains between X & Y",
            "items": []
          }
        }
      }
    }
  }
}


simple_response = {
    "payload": {
      "google": {
        "richResponse": {
          "items": [
            {
              "simpleResponse": {
                "textToSpeech": "sample",
                "displayText": "sample"
              }
            }
          ]
        }
      }
    }
}