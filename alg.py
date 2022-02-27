#File will contain the algorithm

# Import Statements
import math
import random
import csv
from datetime import datetime

#Global variables
loadDataset = dict()

truckers = dict()

pathIdList = [] #list of available ids

"""
loadedPathWeights = [] #Represents path weights for delivery trips

inBetweenPathWeights = []
"""

#TODO: Temp data used to test algorithm
TripPlan = [
   {
      "input_trip_id": 401,
      "start_latitude": 33.522594,
      "start_longitude": -86.811318,
      "start_time": "2022-02-28 08:00:00",
      "max_destination_time": "2022-03-01 15:00:00"
   },
   {
      "input_trip_id": 402,
      "start_latitude": 45.507460,
      "start_longitude": -73.578565,
      "start_time": "2022-02-28 12:00:00",
      "max_destination_time": "2022-03-01 12:00:00"
   },
   {
      "input_trip_id": 403,
      "start_latitude": 42.836208,
      "start_longitude": -78.793257,
      "start_time": "2022-03-01 08:00:00",
      "max_destination_time": "2022-03-02 15:00:00"
   },
   {
      "input_trip_id": 404,
      "start_latitude": 35.047637,
      "start_longitude": -90.025120,
      "start_time": "2022-03-01 15:00:00",
      "max_destination_time": "2022-03-03 10:00:00"
   },
   {
      "input_trip_id": 405,
      "start_latitude": 39.328294,
      "start_longitude": -76.640924,
      "start_time": "2022-03-01 12:00:00",
      "max_destination_time": "2022-03-02 16:00:00"
   },
   {
      "input_trip_id": 406,
      "start_latitude": 32.296628,
      "start_longitude": -87.774006,
      "start_time": "2022-03-02 16:00:00",
      "max_destination_time": "2022-03-04 10:00:00"
   },
   {
      "input_trip_id": 407,
      "start_latitude": 44.036950,
      "start_longitude": -103.200021,
      "start_time": "2022-03-02 08:00:00",
      "max_destination_time": "2022-03-03 15:00:00"
   },
   {
      "input_trip_id": 408,
      "start_latitude": 33.448375,
      "start_longitude": -112.066077,
      "start_time": "2022-03-04 11:00:00",
      "max_destination_time": "2022-03-06 16:00:00"
   },
   {
      "input_trip_id": 409,
      "start_latitude": 41.106195,
      "start_longitude": -112.018256,
      "start_time": "2022-03-05 09:00:00",
      "max_destination_time": "2022-03-06 17:00:00"
   },
   {
      "input_trip_id": 410,
      "start_latitude": 41.608842,
      "start_longitude": -84.555735,
      "start_time": "2022-03-04 10:00:00",
      "max_destination_time": "2022-03-05 16:00:00"
   }
]

#Returns time in hours since linux epoch
def timeConverter(dataTimeStamp):

    return (datetime.strptime(dataTimeStamp, "%Y-%m-%d %H:%M:%S")).timestamp() / 3600


# Function that converts meters to miles
def meterToMile(meters):
    return(0.0006213712*meters)


def dCalc(lat1, lat2, lon1, lon2):
    R = 6371000 # metres
    φ1 = lat1 * math.pi/180 # φ, λ in radians
    φ2 = lat2 * math.pi/180
    Δφ = (lat2-lat1) * math.pi/180
    Δλ = (lon2-lon1) * math.pi/180

    a = math.sin(Δφ/2) * math.sin(Δφ/2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2) * math.sin(Δλ/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    d = R * c # in metres!!! NOT MILES

    return(meterToMile(d))


#Calculates the profite made from doing a route with a given distance in miles and pickup amount in dollars
def profitCalc(distance, amount):
    return (amount - distance * 0.4)

#Returns time needed to travel a certain distance, in miles
def timeCalc(distance):
    return (distance / 55.0)

# Function to fetch data from the dataset csv file
def dataFetch():
    global loadDataset 
    global pathIdList
    file = open("./dataset.csv", "r")
    loadDataset = list(csv.DictReader(file))
    for i in loadDataset:
        pathIdList.append(int(i["load_id"]))
"""    
#Populates graph with distances
def populateGraph():
    global loadDataset
    global pathWeights
    global inBetweenPathWeights
    #initialize multidimensional list
    inBetweenPathWeights = [[[float("inf"), 0]] * len(loadDataset) for i in range(len(loadDataset))]
    
    for i, row in enumerate(loadDataset):
        dist = dCalc(float(row["origin_latitude"]), float(row["destination_latitude"]), float(row["origin_longitude"]), float(row["destination_longitude"]))
        profit = profitCalc(dist, float(row["amount"]))
        time = timeCalc(dist)
        loadedPathWeights.append([profit, dist])
        for j, otherRow in enumerate(loadDataset):
            unloadedDist = dCalc(float(row["destination_latitude"]), float(otherRow["origin_latitude"]), float(row["destination_longitude"]), float(otherRow["origin_latitude"]))
            unloadedProfit = profitCalc(unloadedDist, 0)
            unloadedTime = timeCalc(unloadedDist)
            inBetweenPathWeights[i][j] = [unloadedProfit, unloadedTime]
"""

# Returns the profit from going through a list of deliveries in series; returns negative infinity if exceeding time limit or if paths are repeated
def evalRoute(listOfIds, tripInput):
    if (listOfIds == None):
        return float("-inf")
    
    if len(listOfIds) != len(set(listOfIds)):
        return float("-inf")
    
    global loadDataset
    profit = 0
    lat = float(tripInput["start_latitude"])
    long = float(tripInput["start_longitude"])
    maxTime = timeConverter(tripInput["max_destination_time"])
    currTime = timeConverter(tripInput["start_time"])
    for i in listOfIds:
        index = pathIdList.index(i)
        row = loadDataset[index]
        #Calculate first stretch to pickup
        dist = dCalc(lat, float(row["origin_latitude"]), long, float(row["origin_longitude"]))
        profit += profitCalc(dist, 0)
        currTime += timeCalc(dist)
        
        if (currTime > timeConverter(row["pickup_date_time"])):
            return float("-inf")
        
        #Actual delivery route
        dist = dCalc(float(row["origin_latitude"]),float(row["destination_latitude"]), float(row["origin_longitude"]), float(row["destination_longitude"]))
        profit += profitCalc(dist, float(row["amount"]))
        currTime += timeCalc(dist)
        
        #set new positions
        lat = float(row["destination_latitude"])
        long = float(row["destination_longitude"])
        
        if (currTime > maxTime): 
            return float("-inf")
    return profit

def randomFillList(idList, tripInput):
    
    trialsPermitted = 10
    
    for _ in range(trialsPermitted):
        proposed = pathIdList[random.randint(0, len(pathIdList) - 1)]
        testList = idList.copy()
        testList.append(proposed)
        newEval = evalRoute(testList, tripInput)
        if newEval > 0:
            idList = testList
            break
        
        
    return idList

"""
def randomFillList(idList, tripInput):
    eval = evalRoute(idList, tripInput)
    
    trialsPermitted = 10
    
    for _ in range(trialsPermitted):
        proposed = pathIdList[random.randint(0, len(pathIdList))]
        testList = idList.copy()
        testList.append(proposed)
        newEval = evalRoute(testList, tripInput)
        if (not eval == null) and (newEval > eval):
            idList = testList
        
        
    return idList
"""
"""
def naturalSelect(idLists, tripInput):
    newLists = idLists.copy().sort(key=lambda x: evalRoute(x, tripInput))
    newLists = newLists[0:len(newLists) / 2]
    newLists = newLists * 2
    return newLists
"""
    
def mutateList(idList, tripInput):
    newList = idList.copy()[:random.randint(int(len(idList) / 1.5),len(idList))]
    newList = randomFillList(newList, tripInput)
    return newList

def routePlan(tripInput):
    id = tripInput["input_trip_id"] 
    idList = []
    
    #Initial approximation
    maxProfit = 0
    maxEntry = None
    for entry in pathIdList:
        eval = evalRoute([entry], tripInput)
        if (eval > maxProfit):
            maxProfit = eval
            maxEntry = entry
    if (not maxEntry == None):
        idList.append(maxEntry)
    
    temperature = 2000
    annealList = idList[:]
    while temperature > 0:
        fitness = evalRoute(annealList, tripInput)
        newList = mutateList(annealList, tripInput)
        if (evalRoute(newList, tripInput) > fitness or random.randint(0,2000) < temperature):
            fitness = evalRoute(newList, tripInput)
            annealList = newList
        temperature -= 1
    
    print("Profit: "+ str(evalRoute(annealList, tripInput))+"$")
    return {"input_trip_id": id, "load_ids": annealList}  


        
        

def main():
    print("\nWelcome to the TruckMatchr System!\n")
    print("Now fetching data; please be patient...\n")
    dataFetch()
    print("Data fetching completed! Commencing calculations...\n")
    outArray=[]
    for i in range  (len(TripPlan)) :
        print("Trip "+str(i+1)+":\n")
        # sometimes this outputs an error for an out of range, this makes sure the program does not terminate because of it
        try:
            out = routePlan(TripPlan[i])
        except:
            print("Failed!\n\n")
            out = {"input_trip_id": "N/A", "load_ids": ["N/A"]}
        strOut = str(out)
        strOut = strOut.replace("\'","\"")
        print(strOut+"\n\n")
        outArray.append(strOut)
    strOutArray = str(outArray)
    strOutArray = strOutArray.replace("\'","")
    print(outArray)
    with open("json_data.json", "w") as outfile:
        outfile.write(str(strOutArray))
if __name__ == "__main__":
    main()