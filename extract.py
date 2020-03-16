#!/usr/bin/python3 -W ignore::DeprecationWarning

import requests
import json
import sys
import csv
import time
import getpass
import ipaddress
import apifunctions

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
gregory.dunlap / celtic_cow

"""
def get_group_contents(grp):
    show_group_json = {"name" : grp}

    check_group = apifunctions.api_call(ip_addr, "show-group", show_group_json, sid)

    print(json.dumps(check_group))

    grp_size = len(check_group['members'])

    print(grp_size)

    for x in range(grp_size):
        print(check_group['members'][x]['name'])
        if(check_group['members'][x]['type'] == "host"):
            print(check_group['members'][x]['ipv4-address'])
        if(check_group['members'][x]['type'] == "network"):
            print(check_group['members'][x]['subnet4'])
            print(check_group['members'][x]['mask-length4'])

# end of get_group_contents

if __name__ == "__main__":
    
    debug = 1

    print("extract zones  : version 0.1")

    ip_addr  = "146.18.96.16"
    ip_cma   = "146.18.96.25"
    user     = "gdunlap"
    password = "1qazxsw2"

    sid = apifunctions.login(user,password, ip_addr, ip_cma)

    if(debug == 1):
        print("session id : " + sid)


    with open('grp.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            grp = row[0]
            print("*********")
            print(grp)
            get_group_contents(grp)
            print("---------")

    """
    grp_2_extract = "NPIT150-VRF105"

    show_group_json = {"name" : grp_2_extract}

    check_group = apifunctions.api_call(ip_addr, "show-group", show_group_json, sid)

    print(json.dumps(check_group))

    grp_size = len(check_group)

    print(grp_size)

    for x in range(grp_size-1):
        print(check_group['members'][x]['name'])
        if(check_group['members'][x]['type'] == "host"):
            print(check_group['members'][x]['ipv4-address'])
        if(check_group['members'][x]['type'] == "network"):
            print(check_group['members'][x]['subnet4'])
            print(check_group['members'][x]['mask-length4'])
    """

    # don't need to publish
    time.sleep(20)

    ### logout
    logout_result = apifunctions.api_call(ip_addr, "logout", {}, sid)
    if(debug == 1):
        print(logout_result)
#endof main()