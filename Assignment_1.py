# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 22:23:29 2015

@author: Oisin
"""
import math
import sqlite3

# Function to calculate distance between two points in lat long format
def lat_long_distance(long1, lat1, long2, lat2):
    # Convert latitude and longitude to spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0     
    # phi = 90 - latitude
    phi1 = (90.0 - lat1) * degrees_to_radians
    phi2 = (90.0 - lat2) * degrees_to_radians
    # theta = longitude
    theta1 = long1 * degrees_to_radians
    theta2 = long2 * degrees_to_radians
    # Compute spherical distance from spherical coordinates
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    # Multiply arc by radius of the earth in kms to get distance in kms
    distance = 6373 * arc
    return distance
# Function complete, returning distance

# Function to calculate the distance from one site to others
# Takes in index number of plant that distance is being calculated from
# And the list that contains the sites that distance is being calculated to
# Returns list containing distance from required site to each of the others
def distance_between_sites(plant_num, L):
    plant_num_data = Location[plant_num]
    Distance_List = []
    for data in L:
        if data == plant_num_data: # ensure distance is 0 between one site and itself
            d = 0.0
        else:
            d = lat_long_distance(data[0], data[1], plant_num_data[0], plant_num_data[1])
        Distance_List.append(d)
    return Distance_List

# Function to determine nearest port to each site
# Returns list with distance to nearest port for each site
def nearest_port():
    L = []
    for i in range(len(Location)):
        L1 = distance_between_sites(i, Ports)
        m = min(L1)
        L.append(m)
    return L
        
# Function to calculate transport cost from one site to others
# Takes in distance list for site that cost is being evaluated for
# And the list that contains the sites that cost is being calculated to
# Returns list containing transport cost from required site
# to all others in the input list
def transport_cost(D, L):
    Cost_List = []
    for i in range(len(Location)):
        plant_data = L[i]
        plant_tonnage = plant_data[2]
        cost = plant_tonnage * D[i]
        Cost_List.append(cost)
    return Cost_List
 
# Function to sum values in a list
# Takes in list (in this program list contains transport cost to other sites)
# Returns the sum
def sum_costs(L):
    sum = 0.0
    for i in L:
        sum += i
    return sum
    
# Function to calculate total tonnage that will be transported to the ports
# Takes in Location list
# Returns the sum of the tonnage at every site
def total_tonnage(L):
    sum = 0.0
    for data in L:
        sum += data[2]
    return sum
    
def index_of_nearest_port(i):
    L = []
    L = distance_between_sites(i, Ports)
    index = L.index(min(L))
    return index
    
   
# Import data from "ports" table into Python using SQL command
conn = sqlite3.connect('renewable.db') # create a "connection"
c = conn.cursor() # create a "cursor" 
c.execute("SELECT * FROM ports;") # execute SQL command
Ports = []
for item in c:
    Ports.append(item)
# Finished importing "ports" table. Data is stored in a list called Ports

# Import data from "location" table into Python using SQL command
c.execute("SELECT * FROM location;") # execute SQL command
Location = []
for item in c:
    Location.append(item)
# Finished importing "location" table. Data is stored in a list called Location

Total_Cost_List = []
for i in range(len(Location)):
    D = distance_between_sites(i, Location)
    TC = transport_cost(D, Location)
    sum = sum_costs(TC)
    Total_Cost_List.append(sum)

Cost_To_Port = [x * total_tonnage(Location) for x in nearest_port()]
Total_Cost_Port_And_Sites = [a + b for a, b in zip(Total_Cost_List, Cost_To_Port)]
print "\nThe list below shows the total transportation cost for each location being used as the processing plant:\n"
print Total_Cost_Port_And_Sites

min_cost = min(Total_Cost_Port_And_Sites)
print "\nThe minimum transportation cost from this list is:", min_cost, "tkm/year (tonne-kilometre/year)"
location_index = Total_Cost_Port_And_Sites.index(min_cost)
print "\nDetails of the location chosen for the processing plant (%dth in the list of %d) are:" % ((location_index+1), len(Location)) 
print "(long, lat, production)", Location[location_index]
port_index = index_of_nearest_port(location_index)
print "\nDetails of the chosen port (%drd in the list of %d) are:" % ((port_index+1), len(Ports))
print "(long, lat)", Ports[port_index]
