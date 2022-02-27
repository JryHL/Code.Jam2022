#File will contain the algorithm
print("hello world")


# Function to fetch data from the dataset csv file
def dataFetch():
    dataset = open("./dataset.csv", "r")
    dataset = dataset.readlines()
    #print(dataset) #test for data collection, should print file in console