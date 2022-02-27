import itertools
import math
import csv
from datetime import datetime

input_file = {
  "input_trip_id": 101,
  "start_latitude": 27.961307,
  "start_longitude": -82.4493,
  "start_time": "2020-02-04 08:00:00",
  "max_destination_time": "2022-02-06 15:00:00"
}

# Create all possible combinations of trips
x = []
data = []
highest_profit = 0.0
best_combination = []

for i in range(50000):
  x.append(i)
combinations = [p for p in itertools.product(x, repeat=5)]
print("hi")
# store CSV file in an array
reader = csv.DictReader(open("data1.csv"))
for row in reader:
  data.append(row)

# calculate geodesic distance
def long_calc(lat1, lon1, lat2, lon2):
  R = 6371000; #metres
  φ1 = lat1 * math.pi/180 # φ, λ in radians
  φ2 = lat2 * math.pi/180
  Δφ = (lat2-lat1) * math.pi/180
  Δλ = (lon2-lon1) * math.pi/180

  a = math.sin(Δφ/2) * math.sin(Δφ/2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2) * math.sin(Δλ/2);
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  d = R * c # in metres
  d = d/1609
  return d

# update time at the trucker goes through his trip
def update_time(original, added_hours):
  date = datetime.fromisoformat(original)
  time = 2.3
  hours = int(time)
  minutes = int((time*60) % 60)
  seconds = int((time*3600) % 60)
  return date.replace(hour=hours, minute=minutes, second=seconds)

# v = d/t t = d/v

# calculate profit made by following a specific combination of indices
def compute_profit(indices):
  profit = 0
  # find the distance from starting location to first origin
  d_to_first_loc = long_calc(float(input_file["start_latitude"]), float(input_file["start_longitude"]), float(data[0]["origin_latitude"]), float(data[0]["origin_longitude"]))
  profit -= 0.40 * d_to_first_loc

  # update time based on the lenght of trip
  date = input_file["start_time"]
  t_to_first_loc = d_to_first_loc/55.0
  new_date = update_time(date, t_to_first_loc)

  for index in indices:
    # if truck has time to make it to the next location, without being late
    if data[index]["pickup_date_time"] > str(new_date):
      # calculate the distance to the next point
      d_to_next_loc = long_calc(float(data[index]["origin_latitude"]), float(data[index]["origin_longitude"]), float(data[index]["destination_latitude"]), float(data[index]["destination_longitude"]))
      # update profit
      profit += (float(data[index]["amount"])) - (0.40 * float(d_to_next_loc))
      # update time after the destination was reached
      new_date = update_time(data[index]["pickup_date_time"], d_to_next_loc/55.0)
    # else not enough time, combinaison is forgotten
    else:
      return -1
  return profit

# for every possible combinaison
for combination in combinations:
  profit = compute_profit(combination)
  if profit > highest_profit:
    highest_profit = profit
    best_combination = combination
  