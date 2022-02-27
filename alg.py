#File will contain the algorithm

# Import Statements
import math
import csv

#Global variables
global loadDataset

# Function that converts meters to miles
def meterToMile(meters):
    return(0.0006213712*meters)


def dCalc(lat1, lat2, lon1, lon2):
    R = 6371000 # metres
    φ1 = lat1 * math.PI/180 # φ, λ in radians
    φ2 = lat2 * math.PI/180
    Δφ = (lat2-lat1) * math.PI/180
    Δλ = (lon2-lon1) * math.PI/180

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
    file = open("./dataset.csv", "r")
    loadDataset = csv.DictReader(file)
    



def main():
    print("Hello world!")

if __name__ == '__main__':
    main()