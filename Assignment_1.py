# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 22:23:29 2015

@author: Oisin
"""

import math
import sqlite3

def lat_long_distance(long1, lat1, long2, lat2):
    # Convert latitude and longitude to spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0     
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
 
    # Multiply arc by radius of the earth in kms to get distance in kms
    distance = 6373 * arc
    return distance


conn = sqlite3.connect('renewable.db') # create a "connection"
c = conn.cursor() # create a "cursor" 
c.execute("SELECT * FROM ports;") # execute a SQL command
ports = []
for item in c:
    ports.append(item)


c.execute("SELECT * FROM location;") # execute a SQL command
location = []
for item in c:
    location.append(item)
print location
    
def distance_between_plants(plant_num):
    proposed_plant_data = location[plant_num]
    print proposed_plant_data
    distance_between_plants = []
    for alternative_plant_data in location:
        if proposed_plant_data != alternative_plant_data:
            test = lat_long_distance(alternative_plant_data[0], alternative_plant_data[1], proposed_plant_data[0], proposed_plant_data[1])
            distance_between_plants.append(test)
    print distance_between_plants
    
#print(len(location))
for i in range(len(location)):
    print i
    distance_between_plants(i)

def distance_plants_to_ports(plant_num):
    proposed_plant_data = location[plant_num]
    print proposed_plant_data
    distance_plants_to_ports = []
    for port_data in ports:
        test = lat_long_distance(port_data[0], port_data[1], proposed_plant_data[0], proposed_plant_data[1])
        distance_plants_to_ports.append(test)
    print distance_plants_to_ports
    
for i in range(len(location)):
    print i
    distance_plants_to_ports(i)
  