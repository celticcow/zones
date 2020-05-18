#!/usr/bin/python3 -W ignore::DeprecationWarning

import requests
import json
import sys
import csv
import time
import base64
import argparse
import ipaddress
import apifunctions

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
gregory.dunlap / celtic_cow

"""

"""
takes fwname and returns route base64 blob
"""
def get_routes(fwname, ip_addr, sid):
    debug = 1

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
    print(percent)
    
    while(percent != 100):
        print("--In progress--")

        time.sleep(1)
        
        task_info = apifunctions.api_call(ip_addr, "show-task", {"task-id" : task_id, "details-level" : "full"}, sid)  #, "details-level" : "full"
        status = task_info['tasks'][0]['status']
        percent = task_info['tasks'][0]['progress-percentage']

        print(status)
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

def convert64(b64, search_str):
    debug = 1

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

def main():
    debug = 1

    ip_addr  = "146.18.96.16"
    ip_cma   = "146.18.96.25"
    user     = "gdunlap"
    password = "1qazxsw2"

    networks = list()

    sid = apifunctions.login(user,password, ip_addr, ip_cma)

    if(debug == 1):
        print("session id : " + sid)

    a_base64_message = get_routes("hublab1", ip_addr, sid)

    networks = convert64(a_base64_message, "161.135.150.129")

    print(len(networks))

    for i in range(len(networks)):
        print(str(i) + " " + networks[i])

    # don't need to publish
    time.sleep(20)

    ### logout
    logout_result = apifunctions.api_call(ip_addr, "logout", {}, sid)
    if(debug == 1):
        print(logout_result)
#endof main()

if __name__ == "__main__":
    main()