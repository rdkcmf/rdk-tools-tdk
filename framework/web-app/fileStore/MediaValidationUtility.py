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
import re
from SSHUtility import *
from rdkv_performancelib import *

# Global variable to store all the operations
all_operations = ""
# Global variable to store all the url arguments
all_arguments  = {}

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
    all_arguments[key] = val

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
        url = url + "?" + URLarguments
    url = "\"" + url + "\""
    return url

# Function to parser the web inspect json message and display the
# console log
def dispConsoleLog(log):
   console_methods = ["Console.messagesCleared","Console.messageRepeatCountUpdated"]
   try:
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
       print str(log).replace('\\n','\n')

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

# Function to read the proc validation parameters from device config file
def getProcValidationParams(obj,proc_file):
    validation_dict = {}
    print "\n getting validation params from conf file"
    conf_file,result = getConfigFileName(obj.realpath)
    result, proc_check = getDeviceConfigKeyValue(conf_file,"VALIDATION_REQ")
    if result == "SUCCESS":
        if proc_check == "NO":
            validation_dict["proc_check"] = False
        else:
            validation_dict["proc_check"] = True
            result,validation_dict["ssh_method"] = getDeviceConfigKeyValue(conf_file,"SSH_METHOD")
            if validation_dict["ssh_method"] == "directSSH":
                validation_dict["host_name"] = obj.IP
                result,validation_dict["user_name"] = getDeviceConfigKeyValue(conf_file,"SSH_USERNAME")
                result,validation_dict["password"] = getDeviceConfigKeyValue(conf_file,"SSH_PASSWORD")
            else:
                #TODO
                print "selected ssh method is {}".format(validation_dict["ssh_method"])
                pass
            result,validation_dict["proc_file"] = getDeviceConfigKeyValue(conf_file,proc_file)
    else:
        print "Failed to get the validation parameters from config file, please configure values before test"
    if any(value == "" for value in validation_dict.itervalues()):
        print "please configure values before test"
        validation_dict = {}

    return validation_dict

# Function to check required pattern in proc entry file
def checkProcEntry(sshmethod,credentials,procfile,pattern):
    result_val = "FAILURE"
    if sshmethod == "directSSH":
        credentials_list = credentials.split(',')
        host_name = credentials_list[0]
        user_name = credentials_list[1]
        password = credentials_list[2]
    else:
        #TODO
        print "Secure ssh to CPE"
        pass
    command = "cat " + str(procfile)
    output = ssh_and_execute(sshmethod,host_name,user_name,password,command)
    output_list =  output.split('\n')
    for item in output_list:
        if pattern in item:
            print item
            result_val = "SUCCESS"
    if result_val == "SUCCESS":
        print "Expected data is found in the proc file\n"
    else:
        print "Expected data is not found in the proc file\n"

    return result_val

