##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
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
import subprocess
import inspect
import ConfigParser
from SSHUtility import *

deviceIP=""
devicePort=""
deviceName=""
deviceType=""

#METHODS
#---------------------------------------------------------------
#INITIALIZE THE MODULE
#---------------------------------------------------------------
def init_module (libobj, port, deviceInfo):
    global deviceIP
    global devicePort
    global deviceName
    global deviceType
    deviceIP = libobj.ip;
    devicePort = port
    deviceName = deviceInfo["devicename"]
    deviceType = deviceInfo["boxtype"]

#---------------------------------------------------------------
#EXECUTE A COMMAND IN TM AND GET THE OUTPUT
# Description  : Execute a command in the Test Manager and get the output back
# Parameters   : command - a string to specify the
# Return Value : console output of the 'command' in case of successful execution or "FAILURE" in case of failure
#---------------------------------------------------------------
def rdkvsecurity_executeInTM (command):
    outdata = ""
    try:
        if "" == command:
            outdata = "FAILURE"
            print "[ERROR]: Command to be executed cannot be empty"
        else:
            print "Going to execute %s..." %(command)
            outdata = subprocess.check_output (command, shell=True)
    except:
        outdata = "FAILURE"
        print "#TDK_@error-ERROR : Unable to execute %s successfully" %(command)
    return outdata

#-------------------------------------------------------------------
#EXECUTE A COMMAND IN DUT SHELL AND GET THE OUTPUT
# Description  : Execute a command in DUT through ssh_and_execute() from SSHUtility library and get the output
# Parameters   : 1. sshMethod -  string to specify the SSH method to be used
#                2. credentials - a coma ceparated string to specify the parameters for ssh_and_execute() method. Values are retrieved from <device>.config
#                       a. credentials[0] - string to specify the DUT IP
#                       b. credentials[1] - string to specify the username to ssh to DUT
#                       c. credentials[2] - string to specify the password to ssh to DUT
#                3. command - string to specify the command to be executed in DUT
# Return Value : console output of the command executed on DUT
#-------------------------------------------------------------------
def rdkvsecurity_executeInDUT (sshMethod, credentials, command):
    output = ""
    if sshMethod == "directSSH":
        credentialsList = credentials.split(',')
        host_name = credentialsList[0]
        user_name = credentialsList[1]
        password = credentialsList[2]
    else:
        #TODO
        print "Secure ssh to CPE"
        pass
    try:
        output = ssh_and_execute (sshMethod, host_name, user_name, password, command)
    except Exception as e:
        print "Exception occured during ssh session"
        print e
    return output

#----------------------------------------------------------------------
#GET DEVICE CONFIGURATION FROM THE DEVICE CONFIG FILE
# Description  : Read the value of device configuration from the <device>.config file
# Parameters   : basePath - a string to specify the path of the TM
#                configKey - a string to specify the configuration whose value needs to be retrieved from the <device>.config file
# Return Value : value of device configuration or error log in case of failure
#----------------------------------------------------------------------
def rdkvsecurity_getDeviceConfig (basePath, configKey):
    deviceConfigFile=""
    configValue = ""
    output = ""
    configPath = basePath + "/"   + "fileStore/tdkvRDKServiceConfig"
    deviceNameConfigFile = configPath + "/" + deviceName + ".config"
    deviceTypeConfigFile = configPath + "/" + deviceType + ".config"
    # Check whether device / platform config files required for
    # executing the test are present
    if os.path.exists (deviceNameConfigFile) == True:
        deviceConfigFile = deviceNameConfigFile
    elif os.path.exists (deviceTypeConfigFile) == True:
        deviceConfigFile = deviceTypeConfigFile
    else:
        output = "FAILURE : No Device config file found : " + deviceNameConfigFile + " or " + deviceTypeConfigFile
        print output
        #print "[ERROR]: No Device config file found : %s or %s" %(deviceNameConfigFile,deviceTypeConfigFile)
    try:
        if (len (deviceConfigFile) != 0) and (len (configKey) != 0):
            config = ConfigParser.ConfigParser ()
            config.read (deviceConfigFile)
            deviceConfig = config.sections ()[0]
            configValue =  config.get (deviceConfig, configKey)
            output = configValue
        else:
            output = "FAILURE : DeviceConfig file or key cannot be empty"
            print output
    except Exception as e:
        output = "FAILURE : Exception Occurred: [" + inspect.stack()[0][3] + "] " + e.message
        print output
    return output;
#---------------------------------------------------------------
#EXECUTE CURL REQUESTS
# Description  : Execute curl request in DUT
# Parameters   : Data - a string which contains actual curl request
# Return Value : contains response of the curl request sent
#---------------------------------------------------------------
def execute_step(Data):
    data = '{"jsonrpc": "2.0", "id": 1234567890, '+Data+'}'
    headers = {'content-type': 'text/plain;',}
    url = 'http://'+str(deviceIP)+':'+str(devicePort)+'/jsonrpc'
    try:
        response = requests.post(url, headers=headers, data=data, timeout=20)
        json_response = json.loads(response.content)
        result = json_response.get("result")
        if result != None and "'success': False" in str(result):
            result = "EXCEPTION OCCURRED"
        return result;
    except requests.exceptions.RequestException as e:
        print "ERROR!! \nEXCEPTION OCCURRED WHILE EXECUTING CURL COMMANDS!!"
        print "Error message received :\n",e;
        return "EXCEPTION OCCURRED"

#-------------------------------------------------------------------
#GET THE VALUE OF A METHOD
#-------------------------------------------------------------------
def rdkvsecurity_getValue(method):
    data = '"method": "'+method+'"'
    result = execute_step(data)
    return result

#------------------------------------------------------------------
#SET VALUE FOR A METHOD
#------------------------------------------------------------------
def rdkvsecurity_setValue(method,value):
    data = '"method": "'+method+'","params": '+value
    result = execute_step(data)
    return result

#-----------------------------------------------------------------
#GET PLUGIN STATUS
#-----------------------------------------------------------------
def rdkvsecurity_getPluginStatus(plugin):
    data = '"method": "Controller.1.status@'+plugin+'"'
    result = execute_step(data)
    if result != None and result != "EXCEPTION OCCURRED":
        for x in result:
            PluginStatus=x["state"]
        return PluginStatus
    else:
        return result;

#-------------------------------------------------------------------
#GET THE REQUIRED VALUE FROM A RESULT
#-------------------------------------------------------------------
def rdkvsecurity_getReqValueFromResult(method,reqValue):
    data = '"method": "'+method+'"'
    result = execute_step(data)
    if result != "EXCEPTION OCCURRED":
        value = result[reqValue]
        return value
    else:
        return result
                              
