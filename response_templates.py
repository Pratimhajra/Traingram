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
            "items": [
              {
                "optionInfo": {
                  "key": "first title key"
                },
                "description": "first description abcdefghijklmnop fuck this shit I'm out, pratim hajra, mihir kulkarni, pranav gharat, kanishk singh",
                "title": "first title"
              },
              {
                "optionInfo": {
                  "key": "second"
                },
                "description": "second description",
                "title": "second title"
              },
							{
                "optionInfo": {
                  "key": "third"
                },
                "description": "third description",
                "title": "third title"
              },
							{
                "optionInfo": {
                  "key": "fourth"
                },
                "description": "fourth description",
                "title": "fourth title"
              },
							{
                "optionInfo": {
                  "key": "fifth"
                },
                "description": "fifth description",
                "title": "fifth title"
              },
							{
                "optionInfo": {
                  "key": "sixth"
                },
                "description": "sixth description",
                "title": "sixth title"
              }
            ]
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