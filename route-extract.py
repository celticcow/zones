#!/usr/bin/python3 -W ignore::DeprecationWarning

import requests
import json
import sys
import csv
import time
import base64
import getpass
import ipaddress
import apifunctions

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
gregory.dunlap / celtic_cow

zone extract info based on route matches via api

input csv format
fw_name_in_cma,Meta_Data Description, Meta_Data Policy Name,search_subnet
"""

"""
takes fwname and returns route base64 blob
"""
def get_routes(fwname, ip_addr, sid):
    debug = 0

    get_route_json = {
        "script-name" : "script to get route table from fw",
        "script" : "clish -c 'show configuration static-route'",
        "targets" : [fwname]
    }

    route_result = apifunctions.api_call(ip_addr, "run-script", get_route_json, sid)

    if(debug == 1):
        print(json.dumps(route_result))
    
    #get task ID
    task_id = route_result['tasks'][0]['task-id']

    #get task info ... lot of stuff in here
    task_info = apifunctions.api_call(ip_addr, "show-task", {"task-id" : task_id, "details-level" : "full"}, sid)

    #better measure if done or not.   will be int from 0 - 100
    percent = task_info['tasks'][0]['progress-percentage']
    
    while(percent != 100):
        if(debug == 1):
            print("--In progress--")

        time.sleep(1)
        
        task_info = apifunctions.api_call(ip_addr, "show-task", {"task-id" : task_id, "details-level" : "full"}, sid)  #, "details-level" : "full"
        status = task_info['tasks'][0]['status']
        percent = task_info['tasks'][0]['progress-percentage']

        #print(status)
        if(debug == 1):
            print(json.dumps(task_info))
            print(percent)
            print("/////////////////////////////////////")
    #end of while loop

    if(debug == 1):
        print(json.dumps(task_info))

    if(debug == 1):
        print("-----------------------------------------\n\n")
        print(task_info['tasks'][0]['task-details'][0]['responseMessage'])
        print("\n\n\n")

    return(task_info['tasks'][0]['task-details'][0]['responseMessage'])

## end of get_routes()

"""
convert the base64 blob to routes and get the subnet that matches
"""
def convert64(b64, search_str):
    debug = 0

    nets = list()

    a_base64_bytes = b64.encode('ascii')
    a_message_bytes = base64.b64decode(a_base64_bytes)
    a_message = a_message_bytes.decode('ascii')

    routes = a_message.split('\n')

    for route in routes:
               
        if(search_str in route):
            if(debug == 1):
                print(route)
                print("match")
                print("----")

            parts = route.split(" ")
            if(debug == 1):
                print(parts[2])
            nets.append(parts[2])

    return(nets)
#end of convert64()

"""
main function
note : the run-script has to have RW priv 
can't do it with only ROapi user
"""
def main():
    debug = 0

    inputfile = sys.argv[1]

    ip_addr = input("enter IP of MDS : ")
    ip_cma  = input("enter IP of CMA : ")
    user    = input("enter P1 user id : ")
    password = getpass.getpass('Enter P1 Password : ')

    networks = list()

    sid = apifunctions.login(user,password, ip_addr, ip_cma)

    if(debug == 1):
        print("session id : " + sid)

    with open(inputfile) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            grp  = row[0]
            try:
                meta = row[1]
            except:
                #no one put meta data in ... need this to avoid error condition
                meta = "n/a"
            try:
                policy = row[2]
            except:
                #no data to pull
                policy = "n/a"
            try:
                search_str = row[3]
            except:
                search_str = "0.0.0.0"
            #print("*********")
            print(grp)
            print("Meta:" + meta)
            print("Policy:" + policy)
            a_base64_message = get_routes(grp, ip_addr, sid)
            networks = convert64(a_base64_message, search_str)
            for i in range(len(networks)):
                print(networks[i])
            print("****")

    # don't need to publish
    time.sleep(20)

    ### logout
    logout_result = apifunctions.api_call(ip_addr, "logout", {}, sid)
    if(debug == 1):
        print(logout_result)
#endof main()

if __name__ == "__main__":
    main()
### end of program