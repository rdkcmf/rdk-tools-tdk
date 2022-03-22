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
import sys

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
        print "\n---------------------------------------------------------------------------------------------------"
        print "Json command : ", data
        print "\n Response : ", json_response, "\n"
        print "----------------------------------------------------------------------------------------------------\n"
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

#---------------------------------------------------------------------
#GET THE RESOURCE USAGE AND VALIDATE 
#---------------------------------------------------------------------
def rdkservice_validateResourceUsage():
    resource_usage = ""
    high_cpu = False
    high_memory = False
    data = '"method": "DeviceInfo.1.systeminfo"'
    result = execute_step(data)
    if result != "EXCEPTION OCCURRED":
        cpuload = result["cpuload"]

        if float(cpuload) > float(90):
            high_cpu = True
            high_resource = "CPU"
            #Command to get the top 5 processes with high CPU usage
            command = 'top -o %CPU -bn 1 -w 512 | grep "^ " | awk \'{ printf("%s:%s,\\n",$12, $9); }\' | head -n 6 | tail -n +2 | tr -d \'\\n \''
            print "\n CPU load is high : {}".format(float(cpuload))

        else:
            print "\n CPU load : {}".format(float(cpuload))

        totalram = result["totalram"]
        freeram = result["freeram"]
        memory_usage = round(float(totalram-freeram)/float(totalram)* 100,2)

        if memory_usage > float(90):
            high_memory = True
            high_resource = "MEM"
            #Command to get the top 5 processes with high MEM usage
            command = 'top -o %MEM -bn 1 -w 512 | grep "^ " | awk \'{ printf("%s:%s,\\n",$12, $10); }\' | head -n 6 | tail -n +2 | tr -d \'\\n \''
            print "\n Memory usage is high: {}".format(memory_usage)

        else:
            print "\n Memory usage : {}".format(memory_usage)

        if high_cpu and high_memory:
            high_resource = "CPU and MEM"
            command = 'top -bn 1 -w 512 | grep "^ " | awk \'{ printf("%s : [cpu-%s][mem-%s],\\n",$12, $10, $9); }\' | head -n 6 | tail -n +2 | tr -d \'\\n \''

        if high_cpu or high_memory:
            resource_usage = "ERROR"

            #List top 5 processes with high resource usage
            rdkv_performancelib.deviceName = deviceName
            rdkv_performancelib.deviceType = deviceType
            ssh_param = rdkv_performancelib.rdkservice_getSSHParams(libObj.realpath,deviceIP)
            ssh_param = json.loads(ssh_param)
            output = rdkv_performancelib.rdkservice_getRequiredLog(ssh_param["ssh_method"],ssh_param["credentials"],command)
            print "\n<b>Top 5 process with high {} usage:</b>\n".format(high_resource)
            output = output.split("\n")[1]
            print '\n\n'.join(output.split(","))

        else:
            resource_usage = cpuload +","+str(memory_usage)

        return resource_usage

    else:
        return result

#-------------------------------------------------------------------
#EXECUTE COMPLETE LIFECYCLE METHODS OF A PLUGIN
#-------------------------------------------------------------------
def rdkservice_executeLifeCycle(plugin,operations,validation_details):
    result = "FAILURE"
    #Dictionary to store the method and parameter to be passed for that method
    suspend_resume_dict = {"suspend":{"method":"org.rdk.RDKShell.1.suspend","param":'{"callsign":"'+plugin+'"}'},"resume":{"method":"org.rdk.RDKShell.1.launch","param":'{"callsign":"'+plugin+'", "type":"", "uri":""}'}}
    #Dictionary to store the expected values for suspend and resume operations
    expected_status_dict = {"suspend":["suspended"],"resume":["activated","resumed"]}
    #Parameter used for move to front and move to back
    param_val = '{"client": "'+plugin+'"}'
    #Dictionary to store the index values to be checked in move to back and front operations
    check_zorder_dict = {"moveToBack":-1,"moveToFront":0}
    status = rdkv_performancelib.rdkservice_validatePluginFunctionality(plugin,operations,validation_details)
    sys.stdout.flush()
    if status == "SUCCESS":
        #Suspend and resume operations
        for operation in ["suspend","resume"]:
            method = suspend_resume_dict[operation]["method"]
            value = suspend_resume_dict[operation]["param"]
            operation_status = rdkservice_setValue(method,value)
            if operation_status != "EXCEPTION OCCURRED":
                time.sleep(5)
                curr_status = rdkv_performancelib.rdkservice_getPluginStatus(plugin)
                sys.stdout.flush()
                if curr_status in expected_status_dict[operation]:
                    print "\n Successfully set {} plugin to {} status".format(plugin,curr_status)
                else:
                    print "\n Error while setting {} plugin to {} status, current status: {}".format(plugin,operation,curr_status)
                    break
            else:
                print "\n Error while setting {} plugin to {}".format(plugin,operation)
                break
        #On successfull completion of the loop for suspend and resume, below block will get executed
        else:
            print "\n Successfully completed suspend and resume for {} plugin".format(plugin)
            #Do move to front and back operations
            for move_to_method in ["moveToBack","moveToFront"]:
                move_to_status = rdkv_performancelib.rdkservice_setValue("org.rdk.RDKShell.1."+move_to_method,param_val)
                if move_to_status != "EXCEPTION OCCURRED":
                    time.sleep(5)
                    zorder_result = rdkv_performancelib.rdkservice_getValue("org.rdk.RDKShell.1.getZOrder")
                    sys.stdout.flush()
                    if zorder_result != "EXCEPTION OCCURRED":
                        print zorder_result
                        zorder = zorder_result["clients"]
                        zorder = rdkv_performancelib.exclude_from_zorder(zorder)
                        if zorder[check_zorder_dict[move_to_method]].lower() == plugin.lower():
                            print "\n {} operation is success ".format(move_to_method)
                        else:
                            print "\n Error while doing {} operation ".format(move_to_method)
                            break
                    else:
                        print "\n Error while getting the zorder"
                        break
                else:
                    print "\n Error while doing {} operation ".format(move_to_method)
                    break
            else:
                print "\n Successfully completed move to back and move to front for the {} plugin".format(plugin)
                result = "SUCCESS"
    else:
        print "\n Error occurred while lauching and checking the plugin functionality"
    #Destroy the plugin
    print "\n Deactivate {} plugin".format(plugin)
    status = rdkv_performancelib.rdkservice_setPluginStatus(plugin,"deactivate")
    if status != "EXCEPTION OCCURRED":
        #Get the status
        time.sleep(10)
        plugin_status = rdkv_performancelib.rdkservice_getPluginStatus(plugin)
        if plugin_status != 'deactivated':
            print "\n {} plugin is not in deactivated state, current status:{}".format(plugin,plugin_status)
            result = "FAILURE"
        else:
            print "\n Successfully deactivated {} plugin".format(plugin)
    else:
        print "\n Error while deactivating {} plugin".format(plugin)
        result = "FAILURE"
    return result

#-------------------------------------------------------------------
#LAUNCH AND DESTROY A GIVEN GRAPHICAL PLUGIN
#-------------------------------------------------------------------
def rdkservice_launchAndDestroy(plugin,uri=""):
    result = "FAILURE"
    print "\n Launching {} plugin".format(plugin)
    launch_status = rdkv_performancelib.rdkservice_setPluginStatus(plugin,"activate",uri)
    time.sleep(5)
    if launch_status != "EXCEPTION OCCURRED":
        curr_status = rdkv_performancelib.rdkservice_getPluginStatus(plugin)
        if curr_status in ("activated","resumed"):
            print "\n Successfully launched {} plugin".format(plugin)
            time.sleep(5)
            print "\n Destroying {} plugin".format(plugin)
            destroy_status = rdkv_performancelib.rdkservice_setPluginStatus(plugin,"deactivate")
            if destroy_status != "EXCEPTION OCCURRED":
                time.sleep(5)
                new_status = rdkv_performancelib.rdkservice_getPluginStatus(plugin)
                if new_status == "deactivated":
                    print "\n Destroyed {} plugin".format(plugin)
                    result = "SUCCESS"
                else:
                    print "\n Unable to destroy {} plugin, current status".format(plugin,new_status)
            else:
                print "\n Error while destroying {} plugin".format(plugin)
        else:
            print "\n Unable to launch {} plugin, current status".format(plugin,curr_status)
    else:
        print "\n Error while launching {} plugin".format(plugin)
    return result
