#!/usr/bin/python3

import csv
import sys

from zone import Zone
from network import Network

"""
"""

if __name__ == "__main__":
    
    debug = 1

    print("search zones 0.1")

    startZ = 1
    csvindex = 0
    list_of_zones = list()

    #build list of zones from file
    with open('zonedata.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            data = row[0]

            if(startZ == 1):
                #zone title
                ztemp = Zone(data)
                list_of_zones.append(ztemp)
                startZ = 0
            elif(data == "****"):
                #end of zone section
                startZ = 1
                csvindex = csvindex + 1
            else:
                tmp_net = Network(data)
                list_of_zones[csvindex].add_network(tmp_net)
        #end of for row
    #end of csv file


    ipx = "10.81.237.99"

    for z in list_of_zones:
        if(z.compare(ipx)):
            print("Match in zone")
            print(z.get_name())
    
    print("--------end of program-------")



