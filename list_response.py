list_response ={
	"payload": {
		"google": {
			"messages": [{
				"items": [{
						"simpleResponse": {
							"textToSpeech": "sample",
							"displayText": "sample"
						}
					},
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
				]
			}]
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