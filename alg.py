#File will contain the algorithm

# Import Statements
import math




# Function to fetch data from the dataset csv file
def dataFetch():
    dataset = open("./dataset.csv", "r")
    dataset = dataset.readlines()
    #print(dataset) #test for data collection, should print file in console

def dCalc(lat1, lat2, lon1, lon2):
    R = 6371000 # metres
    φ1 = lat1 * math.PI/180 # φ, λ in radians
    φ2 = lat2 * math.PI/180
    Δφ = (lat2-lat1) * math.PI/180
    Δλ = (lon2-lon1) * math.PI/180

    a = math.sin(Δφ/2) * math.sin(Δφ/2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2) * math.sin(Δλ/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    d = R * c # in metres!!! NOT MILES

    return(meter2mile(d))


# Function that converts meters to miles
def meter2mile(meters):
    return(0.0006213712*meters)