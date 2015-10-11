# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 22:23:29 2015

MIS40750: Python Programming, Databases, and Version Control Assignment 

@author: Oisin Mangan
Student Number: 15201541
"""
import math
import sqlite3

# Function to calculate distance between two points in long lat format
# Takes in two sets of coordinates in long lat format
# Returns distance between the points
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


# Function to calculate the distance from one location to all others
# Takes in index number of location that distance is being calculated from
# And the list that contains the sites that distance is being calculated to
# Returns list containing distance from required site to each of the others
def distance_between_sites(location_i, L):
    # Location is list of location data imported from database
    location_i_data = Location[location_i] 
    Distance_List = []
    for data in L:
        # ensure distance is 0 between one location and itself
        if data == location_i_data:
            d = 0.0
        else:
            d = lat_long_distance(data[0], data[1], location_i_data[0], location_i_data[1])
        Distance_List.append(d)
    return Distance_List

# Function to determine nearest port to each location
# No input required
# Returns list with distance to nearest port for each location
def nearest_port():
    L = []
    # Location is list of location data imported from database
    for i in range(len(Location)):
        # Ports is list of port data imported from database
        L1 = distance_between_sites(i, Ports)
        m = min(L1)
        L.append(m)
    return L
        
# Function to calculate transport cost from one location to all others
# Takes in distance list for location that cost is being evaluated for
# Returns list containing transport cost from required location
# to all others in the input list
def transport_cost(D):
    Cost_List = []
     # Location is list of location data imported from database
    for i in range(len(Location)):
        location_i_data = Location[i]
        location_i_tonnage = location_i_data[2]
        cost = location_i_tonnage * D[i]
        Cost_List.append(cost)
    return Cost_List
 
# Function to sum values in a list
# Takes in list (in this program list contains transport cost to other locations)
# Returns the sum
def sum_costs(L):
    sum = 0.0
    for i in L:
        sum += i
    return sum
    
# Function to calculate total tonnage that will be transported to the ports
# No input required
# Returns the sum of the tonnage at every site
def total_tonnage():
    sum = 0.0
    # Location is list of location data imported from database
    for data in Location:
        sum += data[2]
    return sum

# Function to provide index of nearest port to a given location
# Takes in index of required location
# Returns index of nearest port to that location   
def index_of_nearest_port(i):
    # Ports is list of port data imported from database
    L = distance_between_sites(i, Ports)
    index = L.index(min(L))
    return index
    
# This is the beginning of the main code
   
# Import data from "ports" table in database into Python using SQL command
conn = sqlite3.connect('renewable.db') # create a "connection"
c = conn.cursor() # create a "cursor" 
c.execute("SELECT * FROM ports;") # execute SQL command
Ports = []
for item in c:
    Ports.append(item)
# Finished importing "ports" table. Data is stored in a list called Ports

# Import data from "location" table in databse into Python using SQL command
c.execute("SELECT * FROM location;") # execute SQL command
Location = []
for item in c:
    Location.append(item)
# Finished importing "location" table. Data is stored in a list called Location

# Generate the total transportation cost for each location to all other locations
# Ports are not included at this point
Cost_To_Site = []
for i in range(len(Location)):
    D = distance_between_sites(i, Location)
    TC = transport_cost(D)
    sum = sum_costs(TC)
    Cost_To_Site.append(sum)

# Generate List of transportation cost from each location to it's nearest port
Cost_To_Port = [x * total_tonnage() for x in nearest_port()]

# Generate List of total transporation cost from each location including
# Transportation from other locations and transportation to nearest port
Total_Cost_Port_And_Sites = [a + b for a, b in zip(Cost_To_Site, Cost_To_Port)]
print "\nThe list below shows the total transportation cost for each location being used as the processing plant:"
print "(based on nearest port being used in each case)\n"
print Total_Cost_Port_And_Sites

# Calculate the minimum transportation cost and print out details of selected location and port
min_cost = min(Total_Cost_Port_And_Sites)
print "\nThe minimum transportation cost from this list is:", min_cost, "tkm/year (tonne-kilometre/year)"
location_index = Total_Cost_Port_And_Sites.index(min_cost)
print "\nDetails of the location chosen for the processing plant (%dth in the list of %d) are:" % ((location_index+1), len(Location)) 
print "(long, lat, production)", Location[location_index]
port_index = index_of_nearest_port(location_index)
print "\nDetails of the chosen port (%drd in the list of %d) are:" % ((port_index+1), len(Ports))
print "(long, lat)", Ports[port_index]
