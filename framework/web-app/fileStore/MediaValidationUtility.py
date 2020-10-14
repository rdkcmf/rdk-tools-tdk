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

# Global variable to store all the operations
all_operations = ""

# Function to set the operation and interval
def setOperation(operation,intervalOrCount):
    global all_operations
    if all_operations != "":
        all_operations += ","
    all_operations += operation + "(" + str(intervalOrCount) + ")"

# Function to get all the operations set
def getOperations():
    return all_operations

# Function to form the complete test app url
def getTestURL(appURL,videoURL,operations,autotest="true"):
    url = appURL + "?" + "url=" + videoURL
    if operations != "" or operations == None:
        url = url + "&operations=" + operations
    url = url + "&autotest=" + autotest
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
                        print str(text_from_message).replace('\\n','\n')
                        sys.stdout.flush()
   except:
       print("An exception occurred")
       print str(log).replace('\\n','\n')

# Function to get the text message from web inspect json message
def getConsoleMessage(log):
    log_data = json.loads(log)
    text_from_message = log_data.get("params").get("message").get("text")
    return text_from_message


