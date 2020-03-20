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
def get_group_contents(grp,ip_addr,sid):
    show_group_json = {"name" : grp}

    check_group = apifunctions.api_call(ip_addr, "show-group", show_group_json, sid)

    #print(json.dumps(check_group))

    grp_size = len(check_group['members'])  # oh wow this worked.

    #print(grp_size)

    for x in range(grp_size):
        #print(check_group['members'][x]['name'])
        if(check_group['members'][x]['type'] == "host"):
            print(check_group['members'][x]['ipv4-address'] + "/32")
        elif(check_group['members'][x]['type'] == "network"):
            print(check_group['members'][x]['subnet4'] + "/" + str(check_group['members'][x]['mask-length4']))
        elif(check_group['members'][x]['type'] == "group"):
            get_group_contents(check_group['members'][x]['name'],ip_addr,sid)
        elif(check_group['members'][x]['type'] == "address-range"):
            #print(json.dumps(check_group['members'][x]))
            startip = check_group['members'][x]['ipv4-address-first']
            endip   = check_group['members'][x]['ipv4-address-last']

            sparts = startip.split('.')
            eparts = endip.split('.')

            if((sparts[0] == eparts[0]) and (sparts[1] == eparts[1]) and (sparts[2] == eparts[2])):
                #we have a < /24 thing
                for i in range(int(sparts[3]), int(eparts[3])+1):
                    print(sparts[0] + "." + sparts[1] + "." + sparts[2] + "." + str(i) + "/32")
            if((sparts[0] == eparts[0]) and (sparts[1] == eparts[1]) and (sparts[2] != eparts[2])):
                #we have a > 24 but < 16
                start3 = int(sparts[2])
                end3   = int(eparts[2])
                start4 = int(sparts[3])
                end4   = int(eparts[3])

                for i in range(int(sparts[2]), int(eparts[2])+1):
                    if(i == start3):
                        #we're in the first 3rd octet we need to start and start4 and go through 255
                        for j in range(start4,256):
                            print(sparts[0] + "." + sparts[1] + "." + str(i) + "." + str(j) + "/32")
                    elif((i != start3) and (i != end3)):
                        #in the middle
                        print(sparts[0] + "." + sparts[1] + "." + str(i) + ".0/24")
                        #for j in range(0,256):
                        #    print(sparts[0] + "." + sparts[1] + "." + str(i) + "." + str(j)+ "/32")
                    elif((i != start3) and (i == end3)):
                        #at the end
                        for j in range(0,end4+1):
                            print(sparts[0] + "." + sparts[1] + "." + str(i) + "." + str(j)+ "/32")
                    else:
                        print("hit else")
            if((sparts[0] == eparts[0]) and (sparts[1] != eparts[1])):
                #we have a > 16 but < 8
                # if some one does this ... find them and distroy them
                start2 = int(sparts[1])
                end2   = int(eparts[1])
                start3 = int(sparts[2])
                end3   = int(eparts[2])
                start4 = int(sparts[3])
                end4   = int(eparts[3])

                for k in range(start2,end2+1):
                    if(k == start2):
                        #first 2nd octet 
                        for j in range(start3,256):
                            #print(sparts[0] + "." + str(k) + "." + str(j) + ".")
                            if(j == start3):
                                #beginning
                                for q in range(start4,256):
                                    print(sparts[0] + "." + str(k) + "." + str(j) + "." + str(q) + "/32")
                            else:
                                #do a /24 we're not at end
                                print(sparts[0] + "." + str(k) + "." + str(j) + ".0/24")
                    elif((k != start2) and (k != end2)):
                        #middle 2nd octet 
                        #possible for /16 here  ****
                        print(sparts[0] + "." + str(k) + ".0.0/16")
                    elif((k != start2) and (k == end2)):
                        #at the end of the road
                        for j in range(0,end3+1):
                            if((j != start3) and (j != end3)):
                                print(sparts[0] + "." + str(k) + "." + str(j) + ".0/24")
                            else:
                                for q in range(0,end4+1):
                                    print(sparts[0] + "." + str(k) + "." + str(j) + "." + str(q) + "/32")
        #end of elif(check_group['members'][x]['type'] == "address-range"):  
        else:
            #unknown type of group content
            print(check_group['members'][x]['name'])
            print(check_group['members'][x]['type'])

# end of get_group_contents

if __name__ == "__main__":
    
    debug = 1

    if(debug == 1):
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
            #print("*********")
            print(grp)
            get_group_contents(grp,ip_addr,sid)
            print("****")
  
    # don't need to publish
    time.sleep(20)

    ### logout
    logout_result = apifunctions.api_call(ip_addr, "logout", {}, sid)
    if(debug == 1):
        print(logout_result)
#endof main()