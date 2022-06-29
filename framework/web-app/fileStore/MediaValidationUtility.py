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

import json
import sys
import re,time,ast
from SSHUtility import *
from rdkv_performancelib import *
from rdkv_medialib import *
from web_socket_util import *
from MediaValidationVariables import *

# Device specific config file
deviceConfigFile = ""
# Global variable to store all the operations
all_operations = ""
# Global variable to store all the url arguments
all_arguments  = {}

# Global variable to store the monotoring mechanism
logging_method = None

# Global variable to store websocket conn feature
webkit_socket_conn = True
# Global variable to store default webinspect port
webkit_socket_port = webinspect_port

expectedResult = "SUCCESS"
# Global variable to store client with high z-order
next_z_order_client = None

# Global variables to store default AV port
video_port = None
audio_port = None
# Global variables to store resolution info
current_resolution = None
resolution_revert = False
# Global variables to store sound modes
current_mode = None
mode_revert = False
# Global variable to store proc validation mode
proc_check_mode = None
# Global variable to store process to be excluded
excluded_process_list = PerformanceTestVariables.excluded_process_list

# Function to set the operation and interval
def setOperation(operation,intervalOrCount):
    global all_operations
    if all_operations != "":
        all_operations += ","
    all_operations += operation + "(" + str(intervalOrCount) + ")"

# Function to get all the operations set
def getOperations():
    return all_operations

# Function to set the url argument and its value
def setURLArgument(key,val):
    if key == "options":
        updateOptions(val)
    elif key == "url" or (key == "drmconfigs" and val.strip() != ""):
        val = val.replace("&",":and:").replace("=",":eq:")
        if key == "drmconfigs":
            drm_config = ""
            for drm_info in val.split("|"):
                print drm_info
                drm_tag = drm_info.split("[",1)[0]
                drm_val = drm_info.split("[",1)[1].rsplit("]",1)[0]
                drm_val = drm_val.replace("(",":ob:").replace(")",":cb:").replace(",",":comma:")
                if drm_config != "":
                    drm_config += ","
                drm_config += drm_tag + "(" + drm_val + ")"
            all_arguments[key] = drm_config
        else:
            all_arguments[key] = val
    else:
        all_arguments[key] = val
    if key == "type":
        updateLibOptions(val)

# Function to get all the url arguments
def getURLArguments():
    url_arguments = ""
    for args in all_arguments:
        if url_arguments != "":
            url_arguments += "&"
        url_arguments += args + "=" + str(all_arguments[args])
    return url_arguments


# Function to form the complete test app url
def getTestURL(appURL,URLarguments):
    url = appURL
    if URLarguments != "" and URLarguments != None:
        if "?" not in url:
            url = url + "?" + URLarguments
        else:
            url = url + "&" + URLarguments
    url = "\"" + url + "\""
    return url

def setDeviceConfigFile(conf_file):
     global deviceConfigFile
     deviceConfigFile = conf_file

def setProcCheckMode(mode):
     global proc_check_mode
     proc_check_mode = mode

def setLoggingMethod(obj):
    global logging_method
    config_file,result = getDeviceConfigFile(obj.realpath)
    result,logging_method = getDeviceConfigKeyValue(config_file,"LOGGING_METHOD")

def updateOptions(val):
    if all_arguments.get("options") != None:
        options = all_arguments.get("options") + "," + val
    else:
        options = val
    all_arguments["options"] = options

def updateLibOptions(val):
    if val == "dash":
        lib_key = "useDashlib"
        result,uselib = getDeviceConfigKeyValue(deviceConfigFile,"LOAD_USING_DASHLIB")
        updateOptions(lib_key+"("+uselib+")")
    elif val == "hls":
        lib_key = "useHlslib"
        uselib = "yes"
        # By default yes, if required it can be made configurable
        #result,uselib = getDeviceConfigKeyValue(deviceConfigFile,"LOAD_USING_HLSLIB")
        updateOptions(lib_key+"("+uselib+")")


# Function to parser the web inspect json message and display the
# console log
def dispConsoleMessage(log):
    try:
       log_info = log.split(",")
       for data in log_info:
          if "\"text\"" in data:
            print(data.split("\"text\":")[1].replace("\"",""))
    except:
       print("An exception occurred")
       print str(log).replace('\\n','\n').replace("\\","")

def dispConsoleLog(log):
   console_methods = ["Console.messagesCleared","Console.messageRepeatCountUpdated"]
   try:

       #if "Console.messageAdded" in log:
       #    dispConsoleMessage(log)
       if "%" not in log:
           log_data = json.loads(log)
           if log_data.get("method") not in console_methods:
                if log_data.get("params") is not None:
                    text_from_message = log_data.get("params").get("message")
                    if text_from_message is not None:
                        text_from_message = text_from_message.get("text")
                        print str(text_from_message).replace('\\n','\n').decode("unicode-escape")
                        sys.stdout.flush()
   except:
       print("An exception occurred")
       print str(log).replace('\\n','\n').replace("\\","")

# Function to get the text message from web inspect json message
def getConsoleMessage(log):
    log_data = json.loads(log)
    text_from_message = log_data.get("params").get("message").get("text")
    return text_from_message

# Function to get the time string from the console message
def getTimeFromMsg(message):
    match = re.search(r"\[\s([0-9:]+)\s\]", message)
    return match.group(1)

# Function to get the time in milliseconds if the input is in HH:MM:SS:sss
def getTimeInMilliSeconds(time_str):
    hours, minutes, seconds, millisec = time_str.split(':')
    time_in_millisec = int(hours) * 3600000 + int(minutes) * 60000 + int(seconds)*1000 + int(millisec)
    return time_in_millisec

# Function read the key value from device config file
def readDeviceConfigKeyValue(conf_file,key):
    result,value = getDeviceConfigKeyValue(conf_file,key)
    return result,value

# Function to enable/disable websocket conn
def socketConnectionEnableDisable(flag):
    global webkit_socket_conn
    webkit_socket_conn = flag

# Function to update webnspect port
def setWebKitSocketPort(port):
    global webkit_socket_port
    webkit_socket_port = port

# Function to create websocket connection to webki webinspect page
def createWebKitSocket(obj):
    print "\nInitiate Connection to Webinspect page (port:%s)..." %(webkit_socket_port)
    socket = createEventListener(obj.IP,webkit_socket_port,[],"/devtools/page/1",False)
    time.sleep(10)
    status = socket.getConnectionStatus()
    return status,socket


# Function to set Pre/Post requisites for executing media tests

def checkPluginStatus(obj,plugin):
    print "\nChecking %s Plugin Status..." %(plugin)
    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus');
    tdkTestObj.addParameter("plugin",plugin);
    tdkTestObj.executeTestCase("SUCCESS");
    result = tdkTestObj.getResult();
    status = tdkTestObj.getResultDetails();
    print "%s Plugin Status: %s" %(plugin,status)
    return result,status

def setPluginState(obj,plugin,state):
    print "\nActivating %s Plugin" %(plugin)
    tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus');
    tdkTestObj.addParameter("plugin",plugin);
    tdkTestObj.addParameter("status",state);
    tdkTestObj.executeTestCase("SUCESS");
    result = tdkTestObj.getResult();
    if "SUCCESS" in result:
        print "%s plugin %sed" %(plugin,state)
        tdkTestObj.setResultStatus("SUCCESS");
        return "SUCCESS"
    else:
        print "Unable to %s %s plugin" %(state,plugin)
        tdkTestObj.setResultStatus("FAILURE");
        return "FAILURE"

def launchPlugin(obj,plugin,url):
    print "\nLaunching %s using RDKShell..." %(plugin)
    url = url.replace('\"',"")
    tdkTestObj = obj.createTestStep('rdkservice_setValue')
    params = '{"callsign":"'+plugin+'", "type":"'+plugin+'", "uri":"'+url+'"}'
    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.launch")
    tdkTestObj.addParameter("value",params)
    tdkTestObj.executeTestCase(expectedResult);
    result = tdkTestObj.getResult();
    info = tdkTestObj.getResultDetails();
    if "SUCCESS" in result:
        print "Resumed %s plugin " %(plugin)
        tdkTestObj.setResultStatus("SUCCESS")
        time.sleep(3)
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method",plugin+".1.url");
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult()
        new_url = tdkTestObj.getResultDetails();
        print "%s Plugin current url: %s" %(plugin,new_url)
        if "SUCCESS" in result and (new_url in url or url in new_url):
            tdkTestObj.setResultStatus("SUCCESS")
            return "SUCCESS"
        else:
            tdkTestObj.setResultStatus("FAILURE")
            return "FAILURE"
    else:
        print "Unable to Resume %s plugin " %(plugin)
        tdkTestObj.setResultStatus("FAILURE")
        return result

def checkRDKShellClients(obj,plugin):
    print "\nChecking RDKShell Clients..."
    tdkTestObj = obj.createTestStep('rdkservice_getValue');
    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getClients");
    tdkTestObj.executeTestCase("SUCCESS");
    result  = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    check_client = ""
    if "SUCCESS" in result:
        clients_list = ast.literal_eval(details)["clients"]
        print "RDKShell Clients: %s" %(clients_list)
        for client in clients_list:
            if client.lower() == plugin.lower():
                check_client = client
                break;
        if check_client != "":
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Unable to get RDKShell Clients"
        tdkTestObj.setResultStatus("FAILURE")

    return result,check_client

def checkClientZOrder(obj,client):
    print "\nChecking Clients Z-Order..."
    tdkTestObj = obj.createTestStep('rdkservice_getValue');
    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder");
    tdkTestObj.executeTestCase("SUCCESS");
    result  = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    client_z_order_status = None
    global next_z_order_client
    next_z_order_client   = None
    if "SUCCESS" in result:
        clients_list = ast.literal_eval(details)["clients"]
        # remove unwanted process from z-order list
        clients_list = exclude_from_zorder(clients_list)
        print "Clients Z-Order: %s" %(clients_list)
        if len(clients_list) > 0:
            tdkTestObj.setResultStatus("SUCCESS")
            if clients_list[0] == client:
                client_z_order_status = True
                if len(clients_list) > 1:
                    next_z_order_client = clients_list[1]
            else:
                client_z_order_status = False
        else:
            print "Clients Z-Order list is empty"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Unable to get Clients Z-Order"
        tdkTestObj.setResultStatus("FAILURE")

    return result,client_z_order_status

#remove unwanted processes from z-order list
def exclude_from_zorder(zorder):
   new_zorder = [ element for element in zorder if element not in excluded_process_list ]
   return new_zorder

def checkWebkitReadyState(obj,result,webkit_client,webkit_z_order_status):
    if "SUCCESS" in result and not webkit_z_order_status:
        move_status = moveToFrontClient(obj,webkit_client)
        if "SUCCESS" in move_status:
            result,webkit_z_order_status = checkClientZOrder(obj,webkit_client)
            if "SUCCESS" in result and webkit_z_order_status:
                webkit_ready = True
            else:
                webkit_ready = False
        else:
            webkit_ready = False
    elif "SUCCESS" in result and webkit_z_order_status:
        webkit_ready = True
    else:
        webkit_ready = False

    return webkit_ready

def checkProcEntry(obj,validation_dict):
    tdkTestObj = obj.createTestStep('rdkv_media_checkProcEntry')
    tdkTestObj.addParameter("sshMethod",validation_dict["ssh_method"])
    tdkTestObj.addParameter("credentials",validation_dict["credentials"])
    tdkTestObj.addParameter("validation_script",validation_dict["validation_script"])
    global proc_check_mode
    if proc_check_mode == None:
        result,mode = getDeviceConfigKeyValue(deviceConfigFile,"PROC_CHECK_MODE")
        if mode.strip() != "":
            tdkTestObj.addParameter("mode",mode)
        else:
            tdkTestObj.addParameter("mode","AV")
    else:
        tdkTestObj.addParameter("mode",proc_check_mode)

    tdkTestObj.executeTestCase(expectedResult);
    result = tdkTestObj.getResult();
    info = tdkTestObj.getResultDetails();
    tdkTestObj.setResultStatus(result);
    return info

def moveToFrontClient(obj,client):
    print "\nMoving %s to front..." %(client)
    tdkTestObj = obj.createTestStep('rdkservice_setValue')
    params = '{"client":"'+client+'"}'
    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.moveToFront")
    tdkTestObj.addParameter("value",params)
    tdkTestObj.executeTestCase(expectedResult);
    result = tdkTestObj.getResult();
    info = tdkTestObj.getResultDetails();
    time.sleep(3)
    if "SUCCESS" in result:
        print "%s plugin moved to front" %(client)
        tdkTestObj.setResultStatus("SUCCESS");
        return "SUCCESS"
    else:
        print "Unable to move %s plugin to front" %(client)
        tdkTestObj.setResultStatus("FAILURE");
        return "FAILURE"

# Function to send key code inputs to the RDKShell client
# Values must follow the pattern KeyName:KeyCode seperated by comma. Eg [ArrowLeft:37,ArrowDown:40]
def sendKeysToClient(obj,client,key_sequence):
    status = "SUCCESS"
    for key_info in key_sequence.split(","):
        key_name = key_info.split(":")[0]
        key_code = key_info.split(":")[1]
        time.sleep(10)
        tdkTestObj = obj.createTestStep('rdkservice_setValue')
        params = '{"keys":[{"keyCode":'+key_code+',"modifiers": ["'+key_name+'"],"delay": 1.0,"callsign": "'+client+'"}]}'
        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
        tdkTestObj.addParameter("value",params)
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult();
        if "SUCCESS" in result:
            print "Key: %s KeyCode: %s sent successfully" %(key_name,key_code)
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            print "Key: %s KeyCode: %s sending failed" %(key_name,key_code)
            tdkTestObj.setResultStatus("FAILURE");
            status = "FAILURE"
    return status


def checkDRMSupported(obj,drm):
    result,ocdm_status = checkPluginStatus(obj,"OCDM");
    if str(ocdm_status) != "None":
        if "FAILURE" in result or ocdm_status != "activated":
            setPluginState(obj,"OCDM","activate");
            time.sleep(3)
            result,ocdm_status = checkPluginStatus(obj,"OCDM");
        if "SUCCESS" in result and "activated" in ocdm_status:
            print "\nChecking Supported DRMs..."
            tdkTestObj = obj.createTestStep('rdkservice_getValue');
            tdkTestObj.addParameter("method","OCDM.1.drms");
            tdkTestObj.executeTestCase("SUCCESS");
            result  = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            details = ast.literal_eval(details)
            drm_list = []
            for drm_info in details:
                drm_list.append(drm_info.get("name"))
            print "Supported DRMs : %s" %(drm_list)
            drm_list = [ drm_name.lower() for drm_name in drm_list ]
            if drm.lower() in drm_list:
                print "%s DRM is supported" %(drm)
                return "TRUE"
            else:
                print "%s DRM not supported" %(drm)
                return "NA"
        else:
            print "Unable to activate OCDM plugin to check DRM info"
            return "FALSE"
    else:
        print "OCDM plugin not available. DRM not supported"
        return "NA"


def getConnectedVideoDisplay(obj):
    global video_port
    print "\nChecking Connected video displays..."
    tdkTestObj = obj.createTestStep('rdkservice_getValue');
    tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.getConnectedVideoDisplays");
    tdkTestObj.executeTestCase("SUCCESS");
    result  = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if "SUCCESS" in result:
        disp_list = ast.literal_eval(details)["connectedVideoDisplays"]
        print "Connected displays: %s" %(disp_list)
        if "HDMI0" in disp_list:
            video_port  = "HDMI0"
            conn_status = "SUCCESS"
        # For TV platform devices
        elif "Internal0" in disp_list:
            video_port  = "Internal0"
            conn_status = "SUCCESS"
        else:
            print "Please test with TV connected setup"
            conn_status =  "FAILURE"
    else:
        conn_status =  "FAILURE"
        print "Unable to get connected displays"

    tdkTestObj.setResultStatus(conn_status)
    return conn_status

def getConnectedAudioPorts(obj):
    global audio_port
    print "\nChecking Connected audio ports..."
    tdkTestObj = obj.createTestStep('rdkservice_getValue');
    tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.getConnectedAudioPorts");
    tdkTestObj.executeTestCase("SUCCESS");
    result  = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if "SUCCESS" in result:
        disp_list = ast.literal_eval(details)["connectedAudioPorts"]
        print "Connected audio ports: %s" %(disp_list)
        if "HDMI0" in disp_list:
            audio_port  = "HDMI0"
            conn_status = "SUCCESS"
        # For TV platform devices
        elif "SPDIF0" in disp_list:
            audio_port  = "SPDIF0"
            conn_status = "SUCCESS"
        else:
            print "Please test with TV connected setup"
            conn_status =  "FAILURE"
    else:
        conn_status =  "FAILURE"
        print "Unable to get connected audio ports"

    tdkTestObj.setResultStatus(conn_status)
    return conn_status

def checkSupportedAudioModes(obj,mode):
    print "\nChecking Supported Audio modes..."
    tdkTestObj = obj.createTestStep('rdkservice_setValue');
    params = '{"audioPort":"'+audio_port+'"}'
    tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.getSupportedAudioModes");
    tdkTestObj.addParameter("value",params)
    tdkTestObj.executeTestCase("SUCCESS");
    result  = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    check_status = ""
    if "SUCCESS" in result:
        mode_list = ast.literal_eval(details)["supportedAudioModes"]
        print "Supported Audio modes: %s" %(mode_list)
        mode_match = False
        for mode_value in mode_list:
            if mode.lower() in mode_value.lower():
                mode_match = True
                if "AUTO" in mode_value:
                    mode = mode_value.split("(")[1].split(")")[0]
                else:
                    mode = mode_value;
                break;
        if mode_match:
            check_status = "SUCCESS"
        else:
            print "%s audio mode is not supported" %(mode)
            check_status = "FAILURE"
    else:
        check_status = "FAILURE"
        print "Unable to get supported audio modes"

    tdkTestObj.setResultStatus(check_status)
    return mode,check_status


def checkSupportedAudioCapabilities(obj,mode):
    print "\nChecking Supported Audio capabilities..."
    tdkTestObj = obj.createTestStep('rdkservice_setValue');
    params = '{"audioPort":"'+audio_port+'"}'
    tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.getSettopAudioCapabilities");
    tdkTestObj.addParameter("value",params)
    tdkTestObj.executeTestCase("SUCCESS");
    result  = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    check_status = ""
    if "SUCCESS" in result:
        mode_list = ast.literal_eval(details)["AudioCapabilities"]
        print "Supported Audio capabilities: %s" %(mode_list)
        mode_match = False
        for mode_value in mode_list:
            if mode.lower() in mode_value.lower():
                mode_match = True
                break;
        if mode_match:
            check_status = "SUCCESS"
        else:
            print "%s audio capability is not supported" %(mode)
            check_status = "FAILURE"
    else:
        check_status = "FAILURE"
        print "Unable to get supported audio capabilities"

    tdkTestObj.setResultStatus(check_status)
    return check_status


def checkSupportedResolution(obj,res):
    print "\nChecking Supported Resolutions..."
    tdkTestObj = obj.createTestStep('rdkservice_setValue');
    params = '{"videoDisplay":"'+video_port+'"}'
    tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.getSupportedResolutions");
    tdkTestObj.addParameter("value",params)
    tdkTestObj.executeTestCase("SUCCESS");
    result  = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    check_status = ""
    if "SUCCESS" in result:
        res_list = ast.literal_eval(details)["supportedResolutions"]
        print "Supported Resolutions: %s" %(res_list)
        if res in res_list:
            check_status = "SUCCESS"
        else:
            res_match = False
            for res_value in res_list:
                if res in res_value:
                    res_match = True
                    res = res_value;
                    break;
            if res_match:
                check_status = "SUCCESS"
            else:
                print "%s resolution is not supported" %(res)
                check_status = "FAILURE"
    else:
        check_status = "FAILURE"
        print "Unable to get supported resolutions"

    tdkTestObj.setResultStatus(check_status)
    return res,check_status

def getCurrentSoundMode(obj):
    print "\nGet Current Sound Mode..."
    tdkTestObj = obj.createTestStep('rdkservice_setValue');
    params = '{"audioPort":"'+audio_port+'"}'
    tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.getSoundMode");
    tdkTestObj.addParameter("value",params)
    tdkTestObj.executeTestCase("SUCCESS");
    result  = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if "SUCCESS" in result:
        curr_mode = ast.literal_eval(details)["soundMode"]
        print "Current sound mode: %s" %(curr_mode)
        tdkTestObj.setResultStatus("SUCCESS")
        return "SUCCESS",curr_mode
    else:
        print "Unable to get current sound mode"
        tdkTestObj.setResultStatus("FAILURE")
        return "FAILURE",None

def getCurrentResolution(obj):
    print "\nGet Current Resolution..."
    tdkTestObj = obj.createTestStep('rdkservice_setValue');
    params = '{"videoDisplay":"'+video_port+'"}'
    tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.getCurrentResolution");
    tdkTestObj.addParameter("value",params)
    tdkTestObj.executeTestCase("SUCCESS");
    result  = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if "SUCCESS" in result:
        curr_res = ast.literal_eval(details)["resolution"]
        print "Current Resolution: %s" %(curr_res)
        tdkTestObj.setResultStatus("SUCCESS")
        return "SUCCESS",curr_res
    else:
        print "Unable to get current resolution"
        tdkTestObj.setResultStatus("FAILURE")
        return "FAILURE",None

def setCurrentSoundMode(obj,mode):
    status,curr_mode = getCurrentSoundMode(obj)
    if "FAILURE" in status:
        return status
    global current_mode
    global mode_revert
    if "AUTO" in curr_mode:
        current_mode = curr_mode.split("(")[1].split(")")[0]
    else:
        current_mode = curr_mode
    set_status = ""
    if mode.lower() in curr_mode.lower():
        set_status = "SUCCESS"
        print "Required sound mode is set already"
    else:
        print "\nSetting %s sound mode...." %(mode)
        tdkTestObj = obj.createTestStep('rdkservice_setValue');
        params = '{"audioPort":"'+audio_port+'","soundMode":"'+mode+'", "persist":false}'
        tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.setSoundMode");
        tdkTestObj.addParameter("value",params)
        tdkTestObj.executeTestCase("SUCCESS");
        result  = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if "SUCCESS" in result:
            status,new_mode = getCurrentSoundMode(obj)
            if mode.lower() in new_mode.lower():
                mode_revert = True
                set_status = "SUCCESS"
                tdkTestObj.setResultStatus("SUCCESS")
                print "Sound Mode %s set successfully" %(mode)
            else:
                set_status = "FAILURE"
                tdkTestObj.setResultStatus("FAILURE")
                print "Sound Mode %s not set properly" %(mode)
        else:
            set_status = "FAILURE"
            tdkTestObj.setResultStatus("FAILURE")
            print "Unable to set the sound mode"

    return set_status

def setCurrentResolution(obj,res):
    status,curr_res = getCurrentResolution(obj)
    if "FAILURE" in status:
        return status
    global current_resolution
    global resolution_revert
    current_resolution = curr_res
    set_status = ""
    if res == curr_res:
        set_status = "SUCCESS"
        print "Required resolution is set already"
    else:
        print "\nSetting %s Resolution...." %(res)
        tdkTestObj = obj.createTestStep('rdkservice_setValue');
        params = '{"videoDisplay":"'+video_port+'","resolution":"'+res+'", "persist":false}'
        tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.setCurrentResolution");
        tdkTestObj.addParameter("value",params)
        tdkTestObj.executeTestCase("SUCCESS");
        result  = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if "SUCCESS" in result:
            status,new_res = getCurrentResolution(obj)
            # handling res value with framerate also (eg.1080p60)
            if new_res == res or res in str(new_res):
                resolution_revert = True
                set_status = "SUCCESS"
                tdkTestObj.setResultStatus("SUCCESS")
                print "Resolution %s set successfully" %(res)
            else:
                set_status = "FAILURE"
                tdkTestObj.setResultStatus("FAILURE")
                print "Resolution %s not set properly" %(res)
        else:
            set_status = "FAILURE"
            tdkTestObj.setResultStatus("FAILURE")
            print "Unable to set the resolution"

    return set_status

def setAudioAtmosOutputMode(obj,enable):
    print "\nSetting Audio Atmos o/p mode %s" %(enable)
    tdkTestObj = obj.createTestStep('rdkservice_setValue');
    params = '{"enable":"'+str(enable)+'"}'
    tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.setAudioAtmosOutputMode");
    tdkTestObj.addParameter("value",params);
    tdkTestObj.executeTestCase("SUCESS");
    result = tdkTestObj.getResult();
    if "SUCCESS" in result:
        print "Audio Atmos o/p mode enable %s" %(enable)
        tdkTestObj.setResultStatus("SUCCESS");
        return "SUCCESS"
    else:
        print "Unable to set audio atmos o/p enable as %s" %(enable)
        tdkTestObj.setResultStatus("FAILURE");
        return "FAILURE"


# Function to set the resolution pre-requisites
def setResolutionPreRequisites(obj,res):
    result,ds_status = checkPluginStatus(obj,"org.rdk.DisplaySettings");
    if "FAILURE" in result or ds_status != "activated":
        setPluginState(obj,"org.rdk.DisplaySettings","activate");
        time.sleep(3)
        result,ds_status = checkPluginStatus(obj,"org.rdk.DisplaySettings");
    if "SUCCESS" in result and "activated" in ds_status:
        hdmi_connected = getConnectedVideoDisplay(obj)
        if "SUCCESS" in hdmi_connected:
            res,res_supported = checkSupportedResolution(obj,res)
            if "SUCCESS" in res_supported:
                res_set_status = setCurrentResolution(obj,res)
                if "SUCCESS" in res_set_status:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

# Function to set the resolution post-requisites
def setResolutionPostRequisites(obj):
    if resolution_revert:
        res_set_status = setCurrentResolution(obj,current_resolution)
        if "SUCCESS" in res_set_status:
            return True
        else:
            return False
    else:
        return True

# Function to set the sound mode pre-requisites
def setSoundModePreRequisites(obj,mode):
    result,ds_status = checkPluginStatus(obj,"org.rdk.DisplaySettings");
    if "FAILURE" in result or ds_status != "activated":
        setPluginState(obj,"org.rdk.DisplaySettings","activate");
        time.sleep(3)
        result,ds_status = checkPluginStatus(obj,"org.rdk.DisplaySettings");
    if "SUCCESS" in result and "activated" in ds_status:
        hdmi_connected = getConnectedVideoDisplay(obj)
        hdmi_audioport = getConnectedAudioPorts(obj)
        if "SUCCESS" in hdmi_connected and "SUCCESS" in hdmi_audioport:
            mode,mode_supported = checkSupportedAudioModes(obj,mode)
            if "SUCCESS" in mode_supported:
                mode_set_status = setCurrentSoundMode(obj,mode)
                if "SUCCESS" in mode_set_status:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

# Function to set the sound mode post-requisites
def setSoundModePostRequisites(obj):
    if mode_revert:
        mode_set_status = setCurrentSoundMode(obj,current_mode)
        if "SUCCESS" in mode_set_status:
            return True
        else:
            return False
    else:
        return True


# Function to set the atmos o/p mode pre-requisites
def setAudioAtmosOutputModePreRequisites(obj,mode):
    result,ds_status = checkPluginStatus(obj,"org.rdk.DisplaySettings");
    if "FAILURE" in result or ds_status != "activated":
        setPluginState(obj,"org.rdk.DisplaySettings","activate");
        time.sleep(3)
        result,ds_status = checkPluginStatus(obj,"org.rdk.DisplaySettings");
    if "SUCCESS" in result and "activated" in ds_status:
        hdmi_connected = getConnectedVideoDisplay(obj)
        hdmi_audioport = getConnectedAudioPorts(obj)
        if "SUCCESS" in hdmi_connected and "SUCCESS" in hdmi_audioport:
            mode_supported = checkSupportedAudioCapabilities(obj,mode)
            if "SUCCESS" in mode_supported:
                atmos_set_status = setAudioAtmosOutputMode(obj,True)
                if "SUCCESS" in atmos_set_status:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


# function to set the primary pre-requisites
def setMediaTestPreRequisites(obj,webkit_browser_instance,get_proc_info=True):
    pre_requisite_status = "SUCCESS"
    webkit_console_socket = None
    setURLArgument("execID",str(obj.execID))
    setURLArgument("execDevId",str(obj.execDevId))
    setURLArgument("resultId",str(obj.resultId))
    setLoggingMethod(obj)
    setURLArgument("logging",logging_method)
    #print obj.logpath
    if get_proc_info:
        tdkTestObj = obj.createTestStep('rdkv_media_getProcCheckInfo')
        tdkTestObj.addParameter("realpath",obj.realpath)
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult();
        validation_dict = tdkTestObj.getResultDetails();
        validation_dict = ast.literal_eval(validation_dict)
    else:
        result = "SUCCESS"
        validation_dict = {}
        validation_dict["proc_check"] = False

    if "SUCCESS" in result and validation_dict != {}:
        config_status = "SUCCESS"
        if validation_dict["proc_check"]:
            print "PROC entry validation for video player test: Enabled"
        else:
            print "PROC entry validation for video player test: Skipped"
        if get_proc_info:
            tdkTestObj.setResultStatus("SUCCESS");
    else:
        config_status = "FAILURE"
        tdkTestObj.setResultStatus("FAILURE");

    if "SUCCESS" in config_status:
        result,rdkshell_status = checkPluginStatus(obj,"org.rdk.RDKShell");
        if "FAILURE" in result or rdkshell_status != "activated":
            setPluginState(obj,"org.rdk.RDKShell","activate");
            time.sleep(3)
            result,rdkshell_status = checkPluginStatus(obj,"org.rdk.RDKShell");

        if "SUCCESS" in result and "activated" in rdkshell_status:
            launch_status = launchPlugin(obj,webkit_browser_instance,"about:blank")
            if "SUCCESS" in launch_status:
                client_status,webkit_client = checkRDKShellClients(obj,webkit_browser_instance)
                if "SUCCESS" in client_status and webkit_client != "":
                    result,webkit_z_order_status = checkClientZOrder(obj,webkit_client)
                    webkit_ready_state = checkWebkitReadyState(obj,result,webkit_client,webkit_z_order_status)
                    if webkit_ready_state:
                          if webkit_socket_conn and logging_method == "WEB_INSPECT":
                              websocket_conn_status,webkit_console_socket = createWebKitSocket(obj)
                              if not websocket_conn_status:
                                  print "Connection to web-inspect page failed. cannot proceed test"
                                  pre_requisite_status = "FAILURE"
                              else:
                                  pre_requisite_status = "SUCCESS"
                          elif webkit_socket_conn and logging_method == "REST_API":
                              setURLArgument("tmUrl",str(obj.url)+"/")
                              print "App logs are monitored and collected using REST API"
                              pre_requisite_status = "SUCCESS"
                    else:
                        pre_requisite_status = "FAILURE"
                else:
                    pre_requisite_status = "FAILURE"
            else:
                pre_requisite_status = "FAILURE"
        else:
            pre_requisite_status = "FAILURE"
    else:
        pre_requisite_status = "FAILURE"

    return pre_requisite_status,webkit_console_socket,validation_dict


def monitorVideoTest(obj,webkit_console_socket,validation_dict,check_pattern,timeout=60):
    video_test_result = ""
    proc_check_list  = []
    if logging_method == "WEB_INSPECT":
        video_test_result,proc_check_list = monitorVideoTestUsingWebInspect(obj,webkit_console_socket,validation_dict,check_pattern,timeout)
    elif logging_method == "REST_API":
        video_test_result,proc_check_list = monitorVideoTestUsingRestAPI(obj,validation_dict,check_pattern,timeout)

    return video_test_result,proc_check_list


def monitorVideoTestUsingRestAPI(obj,validation_dict,check_pattern,timeout):
    wait_time = timeout/60
    continue_count = 0
    file_check_count = 0
    logging_flag = 0
    hang_detected = 0
    test_result = ""
    proc_check_list = []
    play_status = "FAILURE"
    video_test_result = ""
    last_line = None
    last_index = 0
    skip_proc_check_events = ["Video Player Paused", "Video Player seeking","Video Player Rate Change to 0"]
    app_log_file = obj.logpath+"/"+str(obj.execID)+"/"+str(obj.execID)+"_"+str(obj.execDevId)+"_"+str(obj.resultId)+"_mvs_applog.txt"

    while True:
        if file_check_count > 60:
            print "\nREST API Logging is not happening properly. Exiting..."
            break;
        if os.path.exists(app_log_file):
            logging_flag = 1
            break;
        else:
            file_check_count += 1
            time.sleep(1);


    while logging_flag:
        if continue_count > timeout:
            hang_detected = 1
            print "\nApp not proceeding for %d min. Exiting..." %(wait_time)
            break;

        with open(app_log_file,'r') as f:
            lines = f.readlines()
        if lines:
            if len(lines) != last_index:
                continue_count = 0
                #print(last_index,len(lines))
                for i in range(last_index,len(lines)):
                    print(lines[i])
                    if "Video Player Playing" in lines[i]:
                        play_status = "SUCCESS"
                    if  check_pattern in lines[i] and validation_dict["proc_check"] and (all(skip_events not in lines[i] for skip_events in skip_proc_check_events)):
                        time.sleep(1);
                        info = checkProcEntry(obj,validation_dict)
                        proc_check_list.append(info)
                    if "TEST RESULT" in lines[i]:
                        test_result = lines[i]

                #last_line  = lines[-1]
                last_index = len(lines)
                if test_result != "":
                    break;
            else:
                continue_count += 1
        else:
            continue_count += 1

        time.sleep(1)

    if "SUCCESS" in test_result and "SUCCESS" in play_status and hang_detected == 0:
        video_test_result = "SUCCESS"
    else:
        video_test_result = "FAILURE"

    return video_test_result,proc_check_list


# Function to monitor video test app progress and get the result
def monitorVideoTestUsingWebInspect(obj,webkit_console_socket,validation_dict,check_pattern,timeout=60):
    wait_time = timeout/60
    continue_count = 0
    hang_detected = 0
    test_result = ""
    proc_check_list = []
    play_status = "FAILURE"
    video_test_result = ""
    # Decoder value will not be increasing suring paused state and we check
    # the proc details after getting seeeked event not during the seek operation
    # While doing FF, in between rate may change to 0 and set back to original rate
    skip_proc_check_events = ["Video Player Paused", "Video Player seeking","Video Player Rate Change to 0"]
    while True:
        if continue_count > timeout:
            hang_detected = 1
            print "\nApp not proceeding for %d min. Exiting..." %(wait_time)
            break
        if (len(webkit_console_socket.getEventsBuffer())== 0):
            time.sleep(1)
            continue_count += 1
            continue
        else:
            continue_count = 0
        console_log = webkit_console_socket.getEventsBuffer().pop(0)
        dispConsoleLog(console_log)
        if "Video Player Playing" in console_log:
            play_status = "SUCCESS"
        if  check_pattern in console_log and validation_dict["proc_check"] and (all(skip_events not in console_log for skip_events in skip_proc_check_events)):
            time.sleep(1);
            info = checkProcEntry(obj,validation_dict)
            proc_check_list.append(info)
        if "TEST RESULT:" in console_log or "Connection refused" in console_log:
            test_result = getConsoleMessage(console_log)
            break;
    webkit_console_socket.disconnect();
    time.sleep(3);

    if "SUCCESS" in test_result and "SUCCESS" in play_status and hang_detected == 0:
        video_test_result = "SUCCESS"
    else:
        video_test_result = "FAILURE"

    return video_test_result,proc_check_list



# Function to monitor animation test app progress and get the result
def monitorAnimationTest(obj,webkit_console_socket,check_pattern,timeout=60):
    animation_test_result = ""
    diagnosis_info = ""
    if logging_method == "WEB_INSPECT":
        animation_test_result,diagnosis_info = monitorAnimationTestUsingWebInspect(obj,webkit_console_socket,check_pattern,timeout)
    elif logging_method == "REST_API":
        animation_test_result,diagnosis_info = monitorAnimationTestUsingRestAPI(obj,check_pattern,timeout)
    return animation_test_result,diagnosis_info


def monitorAnimationTestUsingRestAPI(obj,check_pattern,timeout):
    wait_time = timeout/60
    continue_count = 0
    file_check_count = 0
    logging_flag = 0
    hang_detected = 0
    test_result = ""
    diagnosis_info = ""
    animation_test_result = ""
    lastLine = None
    lastIndex = 0
    app_log_file = obj.logpath+"/"+str(obj.execID)+"/"+str(obj.execID)+"_"+str(obj.execDevId)+"_"+str(obj.resultId)+"_mvs_applog.txt"

    while True:
        if file_check_count > 60:
            print "\nREST API Logging is not happening properly. Exiting..."
            break;
        if os.path.exists(app_log_file):
            logging_flag = 1
            break;
        else:
            file_check_count += 1
            time.sleep(1);

    while logging_flag:
        if continue_count > timeout:
            hang_detected = 1
            print "\nApp not proceeding for %d min. Exiting..." %(wait_time)
            break;

        with open(app_log_file,'r') as f:
            lines = f.readlines()
        if lines:
            if len(lines) != lastIndex:
                continue_count = 0
                #print(lastIndex,len(lines))
                for i in range(lastIndex,len(lines)):
                    print(lines[i])
                    if  check_pattern is not None and check_pattern in lines[i]:
                        diagnosis_info = lines[i].split("[DiagnosticInfo]:")[1].split(":")[1]
                    if "TEST RESULT" in lines[i]:
                        test_result = lines[i]
                    if "TEST COMPLETED" in lines[i]:
                        test_result = "SUCCESS"

                #lastLine  = lines[-1]
                lastIndex = len(lines)
                if test_result != "":
                    break;
            else:
                continue_count += 1
        else:
            continue_count += 1

        time.sleep(1)

    if "SUCCESS" in test_result and hang_detected == 0:
        animation_test_result = "SUCCESS"
    else:
        animation_test_result = "FAILURE"

    return animation_test_result,diagnosis_info



# Function to monitor animation test app progress and get the result
def monitorAnimationTestUsingWebInspect(obj,webkit_console_socket,check_pattern,timeout=60):
    wait_time = timeout/60
    continue_count = 0
    hang_detected = 0
    diagnosis_info = ""
    test_result = ""
    animation_test_result = ""
    while True:
        if continue_count > timeout:
            hang_detected = 1
            print "\nApp not proceeding for %d min. Exiting..." %(wait_time)
            break
        if (len(webkit_console_socket.getEventsBuffer())== 0):
            time.sleep(1)
            continue_count += 1
            continue
        else:
            continue_count = 0
        console_log = webkit_console_socket.getEventsBuffer().pop(0)
        dispConsoleLog(console_log)
        if  check_pattern is not None and check_pattern in console_log:
            diagnosis_info = getConsoleMessage(console_log).split("[DiagnosticInfo]:")[1].split(":")[1]
        if "TEST COMPLETED" in console_log:
            test_result = "SUCCESS"
            break;
        if "TEST RESULT:" in console_log or "Connection refused" in console_log:
            test_result = getConsoleMessage(console_log)
            break;
    webkit_console_socket.disconnect();
    time.sleep(3);

    if "SUCCESS" in test_result and hang_detected == 0:
        animation_test_result = "SUCCESS"
    else:
        animation_test_result = "FAILURE"

    return animation_test_result,diagnosis_info




# Function to monitor conformance test app progress and get the result
def monitorConformanceTest(obj,webkit_console_socket,timeout=60):
    wait_time = timeout/60
    continue_count = 0
    hang_detected = 0
    test_result = "SUCCESS"
    total_test_count = 0
    test_completed_flag = 0
    failed_test_list = []
    passed_test_list = []
    timeout_test_list = []
    optional_failed_test_list = []
    conformance_test_result = ""
    while True:
        if continue_count > timeout:
            hang_detected = 1
            print "\nApp not proceeding for %d min. Exiting..." %(wait_time)
            break
        if (len(webkit_console_socket.getEventsBuffer())== 0):
            time.sleep(1)
            continue_count += 1
            continue
        else:
            continue_count = 0
        console_log = webkit_console_socket.getEventsBuffer().pop(0)
        if "Console.messageAdded" in console_log:
            dispConsoleMessage(console_log)
        else:
            dispConsoleLog(console_log)
        if "All tests are completed" in console_log:
            test_completed_flag = 1
        if "STARTED" in console_log and test_completed_flag != 1:
            total_test_count += 1
        if "PASSED" in console_log and test_completed_flag != 1:
            passed_test_list.append(console_log)
        if "FAILED" in console_log and test_completed_flag == 1:
            if "TIMED OUT" not in console_log and "OPTIONAL_FAILED" not in console_log:
                failed_test_list.append(console_log)
        if "OPTIONAL_FAILED" in console_log and test_completed_flag == 1:
            optional_failed_test_list.append(console_log)
        if "TIMED OUT" in console_log and "OPTIONAL_FAILED" not in console_log and test_completed_flag == 1:
            timeout_test_list.append(console_log)
        if "Device Status:" in console_log or "Connection refused" in console_log:
            break;
    webkit_console_socket.disconnect();
    time.sleep(3);
    if len(failed_test_list) != 0:
        print "\n\n====================== FAILED TESTS =========================="
        dispTestCaseInfo(failed_test_list)
        test_result = "FAILURE"
    if len(timeout_test_list) != 0:
        print "\n\n====================== TIME OUT TESTS =========================="
        dispTestCaseInfo(timeout_test_list)
        test_result = "FAILURE"
    if len(optional_failed_test_list) != 0:
        print "\n\n====================== OPTIONAL FAILED TESTS =========================="
        dispTestCaseInfo(optional_failed_test_list)

    if "SUCCESS" in test_result and hang_detected == 0:
        conformance_test_result = "SUCCESS"
    else:
        conformance_test_result = "FAILURE"
    print "\n\n====================== SUMMARY  =========================="
    print "Summary format is generated based on latest version MSE/EME (2021) test results"
    print "TOTAL TESTS: %d"             %(total_test_count)
    print "PASSED TEST(S): %d"          %(len(passed_test_list))
    print "FAILED TEST(S): %d"          %(len(failed_test_list))
    print "OPTIONAL FAILED TEST(S): %d" %(len(optional_failed_test_list))
    print "TIMEOUT TEST(S): %d"         %(len(timeout_test_list))
    print "TEST STATUS: %s\n"           %(conformance_test_result)
    return conformance_test_result,failed_test_list

# Function to display the EME/MSE list of failed test details
def dispTestCaseInfo(test_list):
    for test_info in test_list:
        if "Console.messageAdded" in test_info:
            dispConsoleMessage(test_info)
        else:
            print test_info


# Function to set the primary post-requisites
def setMediaTestPostRequisites(obj,webkit_browser_instance):
    post_requisite_status = "SUCCESS"
    launch_status = launchPlugin(obj,webkit_browser_instance,"about:blank")
    # TODO webkit browser has to be killed, but when launched again it is not
    # listed as clients after killing. This can be handled when the issues are fixed
    if "SUCCESS" in launch_status:
        if next_z_order_client != None:
            move_status = moveToFrontClient(obj,next_z_order_client)
            if "SUCCESS" not in move_status:
                post_requisite_status = "FAILURE"
    else:
        post_requisite_status = "FAILURE"

    return post_requisite_status






