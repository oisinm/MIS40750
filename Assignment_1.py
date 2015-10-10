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

# Function to calculate the distance from one site to others
# Takes in index number of plant that distance is being calculated from
# And the list that contains the sites that distance is being calculated to
# Returns list containing distance from required site to each of the others
def distance_between_sites(plant_num, L):
    plant_num_data = Location[plant_num]
    #print "this is tuple of data for locations"
    #print plant_num_data
    Distance_List = []
    for data in L:
        if data == plant_num_data: # ensure distance is 0 between one site and itself
            d = 0.0
        else:
            d = lat_long_distance(data[0], data[1], plant_num_data[0], plant_num_data[1])
        Distance_List.append(d)
    #print "this is the list of distances between sites"
    #print Distance_List
    return Distance_List


# Calculate the distance between site i and all other locations
for i in range(len(Location)):
    #print i
    distance_between_sites(i, Location)

# Calculate the distance between site i and all ports

# Function to determine nearest port to each site
# Returns list with distance to nearest port for each site
def nearest_port():
    L = []
    for i in range(len(Location)):
        L1 = distance_between_sites(i, Ports)
        m = min(L1)
        L.append(m)
    return L
    
    
    
for i in range(len(Location)):
#   print i
    distance_between_sites(i, Ports)

      
# Function to calculate transport cost from one site to others
# Takes in distance list for site that cost is being evaluated for
# And the list that contains the sites that cost is being calculated to
# Returns list containing distance from required site to each of the others
def transport_cost(D, L):
    Cost_List = []
    for i in range(len(Location)):
        #print i
        proposed_plant_data = L[i]
        proposed_plant_tonnage = proposed_plant_data[2]
        #print "this is tonnage at site we are calculating cost to"
        #print proposed_plant_tonnage
        cost = proposed_plant_tonnage * D[i]
        #print "this is cost of transport"
        #print cost
        Cost_List.append(cost)
    #print "this is the list of transport costs to all other sites"
    #print Cost_List
    return Cost_List
 
for i in range(len(Location)):
    #print i
    transport_cost(distance_between_sites(i,Location), Location)
    

# Function to sum values in a list
# Takes in list (in this program list contains transport cost to other sites)
# Returns the sum
def sum_costs(L):
    sum = 0.0
    for i in L:
        sum += i
    #print "this is the sum of transport costs"
    #print sum
    return sum

Total_Cost_List = []
for i in range(len(Location)):
    #print i
    x = distance_between_sites(i, Location)
    y = transport_cost(x, Location)
    z = sum_costs(y)
    Total_Cost_List.append(z)
print Total_Cost_List


# Function to calculate total tonnage that will be transported to the ports
# Takes in Location list
# Returns the sum of the tonnage at every site
def total_tonnage(L):
    sum = 0.0
    for data in L:
        sum += data[2]
    print sum
    return sum

total_tonnage(Location)
        
 
#print "This is the Location information as it was originally imported"     
print Location
print Ports

print(nearest_port())
  