# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 22:23:29 2015

@author: Oisin
"""

import math
import sqlite3

conn = sqlite3.connect('renewable.db') # create a "connection"
c = conn.cursor() # create a "cursor" 
c.execute("SELECT * FROM ports;") # execute a SQL command
for item in c:
    print item

c.execute("SELECT * FROM location;") # execute a SQL command
for item in c:
    print item[2]
    print (type(item))
 
def calculate_distance(lat1, long1, lat2, long2):
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

distance = calculate_distance(6.25, 53.33, 6.39, 52.27)
print distance