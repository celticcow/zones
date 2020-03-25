#!/usr/bin/python3

import cgi, cgitb
import csv
import sys

from zone import Zone
from network import Network

"""
Greg Dunlap / celtic_cow
cgi search function
"""

if __name__ == "__main__":
    
    debug = 1
 
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
            elif("Meta" in data):
                list_of_zones[csvindex].set_meta(data)
            elif(data == "****"):
                #end of zone section
                startZ = 1
                csvindex = csvindex + 1
            else:
                tmp_net = Network(data)
                list_of_zones[csvindex].add_network(tmp_net)
        #end of for row
    #end of csv file

    #create instance of Field Storage
    form = cgi.FieldStorage()
    ip2find = form.getvalue('ip2find')
    #ipx = input("enter IP to search for : ")

    ipx = "172.29.28.3"

    ## html header and config data dump
    print ("Content-type:text/html\r\n\r\n")
    print ("<html>")
    print ("<head>")
    print ("<title>Zone_Search</title>")
    print ("</head>")
    print ("<body>")
    print ("<br><br>")
    print("search zones 0.1<br><br>")

    print("You Searched for : " + ip2find + "<br>")

    for z in list_of_zones:
        if(z.compare(ip2find)):
            print("Match in zone<br>")
            print(z.get_name() + "<br>")
            print(z.get_meta() + "<br>")
            print("**********<br>")
    
    print("--------end of program-------")

    print("<br><br>")
    print("</body>")
    print("</html>")
