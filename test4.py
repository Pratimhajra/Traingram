from database import session,TrainInfo 
 
def live_status(trainName):     
    trainList=[] 
    trains = session.query(TrainInfo).filter(TrainInfo.train_name.like(f"%{trainName}%")).all() 
    if(len(trains)<=1): 
        return trains[0].train_no     
    else: 
        for train in trains: 
            trainNo=train.train_no 
            trainName=train.train_name 
            trainDict={"optionInfo" : {"key" : f"{trainNo}"}, 
                       "description" : f"{trainNo}", 
                       "title" : f"{trainName}"} 
            trainList.append(trainDict) 
        return trainList 
 
if __name__ == "__main__": 
    live_status("saurashtra")