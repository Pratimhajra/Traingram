# Traingram

### API Details

|**Host**|https://enquiry.indianrail.gov.in/ntes/|
|--------|:--------:|
|**Protocol**|SSL|

### Required Cookies

|Cookie|Value|
|------|-----|
|`trnTypeColShow`| `y`|
|`JSESSIONID`| Retrieve|

### Required Headers

|Header|Value|
|------|-----|
|Accept-Encoding| `gzip, deflate, br`|
|Accept-Language| `en-US,en;q=0.9,hi;q=0.8,mr;q=0.7`|
|Accept| `*/*`|
|Referer|`https://enquiry.indianrail.gov.in/ntes/index.html`|

### Known Endpoints
Note: All endpoints are concatenated to the host url

### GET METHODS:

|Endpoint|Purpose|Parameters
|--------|--------|--------|
|`SearchTrain?trainNo={TrainNo}`| Search trains by name/number | TrainNo: Integer/String|
|`NTES?action=getTrainData&trainNo={TrainNo}`| train data (stations, delay, destination,etc) | TrainNo: Integer|
|`NTES?action=getTrainsViaStn&viaStn={From}&toStn={To}&withinHrs={Hrs}&trainType={Type}`| All trains coming to/leaving a station. | From: StnCode, To: StnCode, Hrs: Int, Type: See list of types|
|`NTES?action=getTrnBwStns&stn1={Stn1}&stn2={Stn2}&trainType={Type}&viaStn={Via}`| Trains between any two stations. | Stn1, Stn2, Type, [Via]: String|
|`FutureTrain?action=getTrainData&trainNo={TrainNo}&validOnDate={Date}`| Train Schedule | TrainNo, Date (DD/MM/YYYY)|
|`ntes/NTES?action=showAllCancelledTrains`|All Cancelled Trains.|
|`NTES?action=showAllRescheduledTrains`| All rescheduled trains. |
|`NTES?action=showAllDivertedTrains`| All diverted trains.|
|`FutureTrain?action=getTrainDataForAvgDelay&trainNo={TrainNo}`| Average Delay. | TrainNo 
|||

[Station Codes with Station Names](https://enquiry.indianrail.gov.in/ntes/js/stnCodesWithNamesArrayStr.js)


