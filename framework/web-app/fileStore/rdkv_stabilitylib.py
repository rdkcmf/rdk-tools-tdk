##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#########################################################################
import requests
import json
import time
import os
from SSHUtility import *

deviceIP=""
devicePort=""
deviceName=""
deviceType=""
#METHODS
#---------------------------------------------------------------
#INITIALIZE THE MODULE
#---------------------------------------------------------------
def init_module(libobj,port,deviceInfo):
    global deviceIP
    global devicePort
    global deviceName
    global deviceType
    deviceIP = libobj.ip;
    devicePort = port
    deviceName = deviceInfo["devicename"]
    deviceType = deviceInfo["boxtype"]

#---------------------------------------------------------------
#EXECUTE CURL REQUESTS
#---------------------------------------------------------------
def execute_step(data):
    data = '{"jsonrpc": "2.0", "id": 1234567890, '+data+'}'
    headers = {'content-type': 'text/plain;',}
    url = 'http://'+str(deviceIP)+':'+str(devicePort)+'/jsonrpc'
    try:
        response = requests.post(url, headers=headers, data=data, timeout=20)
        json_response = json.loads(response.content)
        return json_response.get("result");
    except requests.exceptions.RequestException as e:
        print "ERROR!! \nEXCEPTION OCCURRED WHILE EXECUTING CURL COMMANDS!!"
        print "Error message received :\n",e;
        return "EXCEPTION OCCURRED"

#------------------------------------------------------------------
#REBOOT THE DEVICE
#------------------------------------------------------------------
def rdkservice_rebootDevice(waitTime):
    try:
        cmd = "curl --silent --data-binary '{\"jsonrpc\": \"2.0\", \"id\": 1234567890, \"method\": \"Controller.1.harakiri\" }' -H 'content-type:text/plain;' http://"+ str(deviceIP)+":"+str(devicePort)+ "/jsonrpc"
        os.system(cmd)

        print "WAIT TO COMPLETE THE REBOOT PROCESS"
        time.sleep(waitTime)
        return "SUCCESS"
    except Exception as e:
        print "ERROR!! \nEXCEPTION OCCURRED WHILE REBOOTING DEVICE!!"
        print "Error message received :\n",e;
        return "EXCEPTION OCCURRED"


#-------------------------------------------------------------------
#GET THE CPU LOAD VALUE FROM DEVICEINFO PLUGIN
#-------------------------------------------------------------------
def rdkservice_getCPULoad():
    data = '"method": "DeviceInfo.1.systeminfo"'
    result = execute_step(data)
    if result != "EXCEPTION OCCURRED":
        value = result["cpuload"]
        return value
    else:
        return result 

#-------------------------------------------------------------------
#GET THE MEMORY USAGE VALUE IN BYTES FROM DEVICEINFO PLUGIN
#-------------------------------------------------------------------
def rdkservice_getMemoryUsage():
    data = '"method": "DeviceInfo.1.systeminfo"'
    result = execute_step(data)
    if result != "EXCEPTION OCCURRED":
        totalram = result["totalram"]
        freeram = result["freeram"]
        value = float(totalram-freeram)/float(totalram)* 100
        return round(value,2)
    else:
        return result

#-------------------------------------------------------------------
#CHECK WHETHER CHANNEL CHANGE TEXT IS PRESENT IN THE CONSOLE LOG
#-------------------------------------------------------------------
def rdkservice_checkChannelChangeLog(log,text):
    remarks = "proceed"
    found = "FAILURE"
    console_methods = ["Console.messagesCleared","Console.messageRepeatCountUpdated"]
    channel_change_log = json.loads(log)
    if (channel_change_log.get("method") not in console_methods):
        text_from_message = channel_change_log.get("params").get("message").get("text")
        if (text in text_from_message):
            found = "SUCCESS"
    return found

#-------------------------------------------------------------------
#VALIDATE WHETHER THE CPU LOAD VALUE IS GREATER THAN THE THRESHOLD VALUE
#-------------------------------------------------------------------
def rdkservice_validateCPULoad(value,threshold):
    if (value > threshold ):
        return "YES"
    else:
        return "NO"

#-------------------------------------------------------------------
#CHECK WHETHER THE MEMORY USAGE VALUE IS GREATER THAN THE THRESHOLD VALUE
#-------------------------------------------------------------------
def rdkservice_validateMemoryUsage(value,threshold):
    if (value > threshold ):
        return "YES"
    else:
        return "NO"

#-------------------------------------------------------------------
#VALIDATE PROC ENTRY TO FIND WHETHER PLAYBACK IS HAPPENING
#-------------------------------------------------------------------
def rdkservice_validateProcEntry(sshmethod,credentials,procfile,mincdb):
    result_val = "SUCCESS"
    if sshmethod == "directSSH":
        credentials_list = credentials.split(',')
        host_name = credentials_list[0]
        user_name = credentials_list[1]
        password = credentials_list[2]
    else:
        #TODO
        print "Secure ssh to CPE"
        pass
    command = "cat " +procfile
    counter = 0
    decoded_val_list =[]
    while counter < 2 :
        output = ssh_and_execute(sshmethod,host_name,user_name,password,command)
        output_list =  output.split('\n')
        cdb_data = ""
        decoded = ""
        started = ""
        for item in output_list:
            if "started:" in item:
                started = item
            elif "CDB:" in item:
                cdb_data = item
            elif "Decode:" in item:
                decoded = item
            else:
                continue
        if any(value == "" for value in [started,cdb_data,decoded]):
            result_val = "FAILURE"
            break
        else:
            decoded_val = ""
            for item in decoded.split():
                if "decoded" in item:
                    decoded_val = int(item.split("=")[1])
            if decoded_val == "":
                print "decoded value is empty"
                result_val = "FAILURE"
                break
            else:
                decoded_val_list.append(decoded_val)
                cdb_data = cdb_data.split(',')[0].split()[-2]
                value_1 = cdb_data.split('/')[0]
                value_2 = cdb_data.split('/')[1]
                cdb_percent1 = float(value_1) / float(value_2)
                cdb_percent = cdb_percent1*100
                if cdb_percent < float(mincdb) :
                    print "cdb_percent is {} which is less than min cdb:{}".format(cdb_percent,mincdb)
                    result_val = "FAILURE"
                    break
                counter += 1
                time.sleep(2)
    if(counter == 2):
        if decoded_val_list[0] >= decoded_val_list[1]:
            print "decoded value is not increasing"
            result_val = "FAILURE"
    return result_val
