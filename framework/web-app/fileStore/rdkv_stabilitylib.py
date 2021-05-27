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
from PIL import Image
import numpy as np
from itertools import combinations
from ip_change_detection_utility import *
import importlib

deviceIP=""
devicePort=""
deviceName=""
deviceType=""
global test_obj

#METHODS
#---------------------------------------------------------------
#INITIALIZE THE MODULE
#---------------------------------------------------------------
def init_module(libobj,port,deviceInfo):
    global deviceIP
    global devicePort
    global deviceName
    global deviceType
    global libObj
    deviceIP = libobj.ip;
    devicePort = port
    deviceName = deviceInfo["devicename"]
    deviceType = deviceInfo["boxtype"]
    libObj = libobj
    

#---------------------------------------------------------------
#EXECUTE CURL REQUESTS
#---------------------------------------------------------------
def execute_step(Data):
    data = '{"jsonrpc": "2.0", "id": 1234567890, '+Data+'}'
    headers = {'content-type': 'text/plain;',}
    url = 'http://'+str(deviceIP)+':'+str(devicePort)+'/jsonrpc'
    try:
        response = requests.post(url, headers=headers, data=data, timeout=20)
        IsPerformanceSelected = libObj.parentTestCase.performanceBenchMarkingEnabled
        if IsPerformanceSelected == "true":
            conf_file,result = getConfigFileName(libObj.realpath)
            result, max_response_time = getDeviceConfigKeyValue(conf_file,"MAX_RESPONSE_TIME")
            time_taken = response.elapsed.total_seconds()
            print "Time Taken for",Data,"is :", time_taken
            if (float(time_taken) <= 0 or float(time_taken) > float(max_response_time)):
                print "Device took more than usual to respond."
                print "Exiting the script"
                result = "EXCEPTION OCCURRED"
                return result;
        json_response = json.loads(response.content)
	result = json_response.get("result")
        if result != None and "'success': False" in str(result):
            result = "EXCEPTION OCCURRED"
        return result;
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
def rdkservice_validateProcEntry(sshmethod,credentials,video_validation_script):
    result = "SUCCESS"
    video_validation_script = video_validation_script.split('.py')[0] 
    try:
        lib = importlib.import_module(video_validation_script)
        method = "check_video_status"
        method_to_call = getattr(lib, method)
        result = method_to_call(sshmethod,credentials)
    except Exception as e:
        print "\n ERROR OCCURRED WHILE IMPORTING THE VIDEO VALIDATION SCRIPT FILE, PLEASE CHECK THE CONFIGURATION \n"
        result = "FAILURE"
    finally:
        return result

#-------------------------------------------------------------------------
#COMPARE IMAGES IN THE GIVEN LIST AND CHECK ANY TWO IMAGES IN THE LIST ARE SAME
#------------------------------------------------------------------------
def compare_images(images_list):
    images = []
    status = "SAME"
    result_list = []
    for image in images_list:
        images.append(np.array(Image.open(image)))
    for image_a,image_b in combinations(images, 2):
        difference = image_a - image_b
        if np.all(difference == 0):
            result_list.append("same")
        else:
            result_list.append("different")
    if all(result == "different" for result in result_list):
        status = "DIFFERENT"
    return status

#-------------------------------------------------------------------
#SET DEFAULT NETWORK INTERFACE OF THE DEVICE
#-------------------------------------------------------------------
def rdkservice_setDefaultInterface(new_interface):
    result_status = status = "SUCCESS"
    if new_interface == "WIFI":
        wifi_connect_status,plugins_status_dict,revert_plugins = switch_to_wifi(test_obj)
        if wifi_connect_status != "SUCCESS":
            result_status = "FAILURE"
        else:
            status = close_lightning_app(test_obj)
    else:
        interface_status = set_default_interface(test_obj,"ETHERNET")
        if interface_status  == "SUCCESS":
            print "\n Successfully Set ETHERNET as default interface \n"
            status = close_lightning_app(test_obj)
        else:
            print "\n Error while setting to ETHERNET \n"
            result_status = "FAILURE"
    if status == "FAILURE":
        result_status = "FAILURE"
    return result_status

#-------------------------------------------------------------------
#SEND KEYCODES TO DUT CORRESPONDING TO THE KEYWORD INPUT
#-------------------------------------------------------------------
def rdkservice_sendKeyCodes(keyword):
    key_codes_dict = {"a":"65","b":"66","c":"67","d":"68","e":"69","f":"70","g":"71","h":"72","i":"73","j":"74","k":"75","l":"76","m":"77","n":"78","o":"79","p":"80","q":"81","r":"82","s":"83","t":"84","u":"85","v":"86","w":"87","x":"88","y":"89","z":"90","@":"shift,50",".":"190"," ":"32","0":"48","2":"50","3":"51","4":"52","5":"53","6":"54","7":"55","8":"56","9":"57"}
    for key in keyword:
        if "shift" in key_codes_dict[key]:
            key = key_codes_dict[key].split(",")[-1]
            data = '"method":"org.rdk.RDKShell.1.generateKey", "params":{"keys":[ {"keyCode": '+key+',"modifiers": ["shift"],"delay":1.0}]}'
        else:
            data = '"method":"org.rdk.RDKShell.1.generateKey", "params":{"keys":[ {"keyCode": '+key_codes_dict[key]+',"modifiers": [],"delay":1.0}]}'
        result = execute_step(data)
        if result == "EXCEPTION OCCURRED":
            break
    return result
