#!/usr/bin/python3 -W ignore::DeprecationWarning

import requests
import json
import sys
import csv
import time
import argparse
import ipaddress
import apifunctions

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
gregory.dunlap / celtic_cow

"""

def main():
    debug = 1

    ip_addr  = "146.18.96.16"
    ip_cma   = "146.18.96.25"
    user     = "gdunlap"
    password = "1qazxsw2"

    sid = apifunctions.login(user,password, ip_addr, ip_cma)

    if(debug == 1):
        print("session id : " + sid)

    get_route_json = {
        "script-name" : "script to get route table from fw",
        "script" : "clish -c 'show configuration static-route'",
        "targets" : ["hublab1"]
    }

    route_result = apifunctions.api_call(ip_addr, "run-script", get_route_json, sid)

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

    task_len = len(task_info['tasks'][0]['task-details'])
    
    if(debug == 1):
        print(task_len)

    print("-----------------------------------------\n\n")
    print(task_info['tasks'][0]['task-details'][0]['responseMessage'])
    print("\n\n\n")
    #for x in range(task_len):
    #    if(task_info['tasks'][0]['task-details'][x]['cluster'] == True):
    #        print("*^*^*^*^*^")
    #        print(task_info['tasks'][0]['task-details'][x]['stagesInfo'])

    print(json.dumps(task_info))

    # don't need to publish
    time.sleep(20)

    ### logout
    logout_result = apifunctions.api_call(ip_addr, "logout", {}, sid)
    if(debug == 1):
        print(logout_result)
#endof main()

if __name__ == "__main__":
    main()