#File will contain the algorithm

# Import Statements
import math
import csv
from datetime import datetime

#Global variables
loadDataset = dict()

pathIdList = [] #list of available ids

"""
loadedPathWeights = [] #Represents path weights for delivery trips

inBetweenPathWeights = []
"""

#TODO: Temp data used to test algorithm
TripPlan = {
      "input_trip_id": 101,
      "start_latitude": 27.961307,
      "start_longitude": -82.4493,
      "start_time": "2022-02-04 08:00:00",
      "max_destination_time": "2022-02-06 15:00:00"
   }

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
    inBetweenPathWeights = [[[float('inf'), 0]] * len(loadDataset) for i in range(len(loadDataset))]
    
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

# Returns the profit from going through a list of deliveries in series; returns none if exceeding time limit or if paths are repeated
def evalRoute(listOfIds, tripInput):
    if len(listOfIds) != len(set(listOfIds)):
        return None
    
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
            return None
        
        #Actual delivery route
        dist = dCalc(float(row["origin_latitude"]),float(row["destination_latitude"]), float(row["origin_longitude"]), float(row["destination_longitude"]))
        profit += profitCalc(dist, float(row["amount"]))
        currTime += timeCalc(dist)
        
        #set new positions
        lat = float(row["destination_latitude"])
        long = float(row["destination_longitude"])
        
        if (currTime > maxTime): 
            return None
    return profit

def routePlan(tripInput):
    id = tripInput["input_trip_id"] 
    loadIdList = []
    initialDistanceList = []
    
    timeLimit = timeConverter(tripInput["max_destination_time"]) - timeConverter(tripInput["start_time"])
    for row in loadDataset:
        #distances from starting point to end 
        dist = dCalc(float(tripInput["start_latitude"]), float(row["origin_latitude"]), float(tripInput["start_longitude"]), float(row["origin_longitude"]))
        profit = profitCalc(dist, float(row["amount"]))
        time = timeCalc(dist)
        initialDistanceList.append([profit, time])
    
    maxIndex = 0;
    maxProfit = 0;
    
    for i, row in enumerate(initialDistanceList):
        if (row[0] > maxProfit and row[1] < timeLimit):
            maxProfit = row[0]
            maxIndex = i
    loadIdList.append(loadDataset[i]["load_id"])
    
    return {"input_trip_id": id, "load_ids": loadIdList}  


def main():
    print("Welcome to the TruckMatchr System\n")
    print("Now fetching data; please be patient...\n")
    dataFetch()
    print("Data fetching completed! Commencing calculations...")
    print (evalRoute([434057843,434076692,434077295], TripPlan))

if __name__ == '__main__':
    main()