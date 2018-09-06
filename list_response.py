list_response ={
    "messages": [
  {
    "items": [
      {
        "description": "Item One Description",
        "image": {
          "url": "http://imageOneUrl.com",
          "accessibilityText": "Image description for screen readers"
        },
        "optionInfo": {
          "key": "itemOne",
          "synonyms": [
            "thing one",
            "object one"
          ]
        },
        "title": "Item One"
      },
      {
        "description": "Item Two Description",
        "image": {
          "url": "http://imageTwoUrl.com",
          "accessibilityText": "Image description for screen readers"
        },
        "optionInfo": {
          "key": "itemTwo",
          "synonyms": [
            "thing two",
            "object two"
          ]
        },
        "title": "Item Two"
      }
    ],
    "platform": "google",
    "title": "Title",
    "type": "list_card"
  }
]
}

simple_response = {
    "messages": [
  {
    "displayText": "Text response",
    "platform": "google",
    "textToSpeech": "Audio response",
    "type": "simple_response"
  }
]
}