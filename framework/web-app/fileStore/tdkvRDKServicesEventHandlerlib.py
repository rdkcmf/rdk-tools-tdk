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
##########################################################################
#


#-----------------------------------------------------------------------------------------------
# module imports
#-----------------------------------------------------------------------------------------------
import time
import websocket
import threading
import thread
import requests
import json,ast
import inspect
from tdkvRDKServicesSupportlib import checkAndGetAllResultInfo
from tdkvRDKServicesSupportlib import checkNonEmptyResultData
from tdkvRDKServicesSupportlib import compareURLs
#-----------------------------------------------------------------------------------------------
#               ***  RDK SERVICES VALIDATION FRAMEWORK SUPPORTING FUNCTIONS ***
#-----------------------------------------------------------------------------------------------

class createEventListener(object):
    def __init__(self,deviceIP,devicePort,events,trace):
        self.ip = deviceIP
        self.port = devicePort
        self.events = events
        self.trace = trace
        thread = threading.Thread(target=self.connect, args=())
        thread.daemon = True
        thread.start()
        self.listen = True
        self.listenflag = False
        self.eventsbuffer = []
        self.eventsregisterinfo = []
    def getEventsRegisterInfo(self):
        return self.eventsregisterinfo
    def getEventsBuffer(self):
        return self.eventsbuffer
    def clearEventsBuffer(self):
        self.eventsbuffer = []
    def getListenerFlag(self):
        return self.listenflag
    def setListenerFlag(self):
        self.listenflag = True

    def connect(self):
        try:
            print "[INFO]: Opening websocket Connection"
            websocket.enableTrace(self.trace)
            websocketConnection = "ws://" + self.ip + ":" + str(self.port) + "/jsonrpc"
            self.ws = websocket.WebSocketApp(websocketConnection,
                                             on_message = self.on_message,
                                             on_error   = self.on_error,
                                             on_close   = self.on_close,
                                             on_open    = self.on_open)
            self.ws.keep_running = True
            print "[INFO]: Start Event Handler..."
            self.ws.run_forever()
        except Exception as e:
            print "\nException Occurred while connecting to target device\n"

    def on_open(self):
        def run(*args):
            print("[INFO]: Registering Events...")
            for event in self.events:
                if self.trace:
                    print "\n Register Event %s" %(event)
                self.clearEventsBuffer()
                self.ws.send(event)
                time.sleep(2)
                registerResponse = json.loads(self.getEventsBuffer()[0])
                if int(registerResponse.get("result")) == 0:
                    status = "SUCCESS"
                else:
                    status = "FAILURE"
                eventinfo = {}
                eventinfo["event"]  = json.loads(event).get("params").get("event")
                eventinfo["status"] = status
                eventinfo["response"] = registerResponse
                self.eventsregisterinfo.append(eventinfo)
            print("[INFO]: Starting Event listener...")
            self.setListenerFlag()
            while self.listen:
                time.sleep(1)
            print ("[INFO]: Stopped Event listener...")
            self.ws.close()
        thread.start_new_thread(run, ())


    def on_message(self,message):
        if self.trace:
            print "\n Received Event Response: %s" %(message)
        if "\\" in message:
            message = message.replace("\\","\\\\")
        self.eventsbuffer.append(message)
    def on_error(self,error):
        print(error)
    def on_close(self):
        print("[INFO]: Closed websocket Connection")

    def disconnect(self):
        self.listen = False
        self.listenflag = False


#-----------------------------------------------------------------------------------------------
# CheckAndGenerateEventResult
#-----------------------------------------------------------------------------------------------
# Syntax      : CheckAndGenerateEventResult(result,methodTag,arguments,expectedValues)
# Description : Method to parse the event output JSON response and generate test result
# Parameter   : result - JSON response results
#             : methodTag - tag used to identify the parser step
#             : arguments - list of arguments used for parsing
#             : expectedValues - list of expected values
# Return Value: Result Info Dictionary
#-----------------------------------------------------------------------------------------------
def CheckAndGenerateEventResult(result,methodTag,arguments,expectedValues):
    tag  = methodTag
    arg  = arguments

    # Input Variables:
    # a. result - list of event response results
    # b. methodTag - string
    # c. arguments - list
    # d. expectedValues - list

    # Output Variable:
    # a.info - dictionary
    #   1.info can have N different result key-value
    #    pairs based on user's need
    #   2.info must have "Test_Step_Status" key to
    #   update the status. By default its SUCCESS

    # DO NOT OVERRIDE THE RETURN VARIABLE "INFO" WITHIN
    # PARSER STEPS TO STORE SOME OTHER DATA. USER CAN
    # ONLY UPDATE "INFO" WITH RESULT DETAILS & STATUS
    info = {}
    info["Test_Step_Status"] = "SUCCESS"

    # USER CAN ADD N NUMBER OF RESPONSE RESULT PARSER
    # STES BELOW
    try:
        # WebKitBrowser Events response result parser steps
        if tag == "webkitbrowser_check_load_finished_event":
            url_load = "FALSE"
            for url_data in result:
                status = compareURLs(url_data.get("url"),expectedValues[1])
                if int(url_data.get("httpstatus")) == int(expectedValues[0]) and status == "TRUE":
                    info = url_data
                    url_load = "TRUE"
                    break;
            if url_load == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_check_load_failed_event":
            result = result[0]
            info = result
            status = compareURLs(result.get("url"),expectedValues[0])
            if status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_check_url_change_event":
            url_change = "FALSE"
            for eventResult in result:
                status = compareURLs(eventResult.get("url"),expectedValues[0])
                if str(eventResult.get("loaded")).lower() == "true" and status == "TRUE":
                    info = eventResult
                    url_change = "TRUE"
                    break;
            if url_change == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_check_visibility_change_event":
            result = result[0]
            info = result
            if str(result.get("hidden")).lower() == "false" and expectedValues[0] == "visible":
                info["Test_Step_Status"] = "SUCCESS"
            elif str(result.get("hidden")).lower() == "true" and expectedValues[0] == "hidden":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_check_statechange_event":
            result = result[0]
            info = result
            if str(result.get("suspended")).lower() in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # Wifi Events response result parser steps
        elif tag == "wifi_check_state_change_event":
            result = result[0]
            info = result
            if int(result.get(state)) == int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "wifi_check_available_ssids_event":
            ssids = []
            for ssid_info in result:
                for ssid_data in ssid_info.get("ssids"):
                    if "\\x00" not in str(ssid_data.get("ssid")):
                        ssids.append(str(ssid_data.get("ssid")))
            if len(arg) and arg[0] == "get_ssid_names":
                info["ssids"] = ssids
                info["Test_Step_Status"] = "SUCCESS"


        # FrameRate Events response result parser steps
        elif tag == "framerate_check_fps_event":
            fps_info = []
            for fps_data in result:
                fps_info.append(fps_data)
            info["fps_info"] = fps_info


        # Bluetooth Events response result parser steps
        elif tag == "bluetooth_check_discovered_device_event":
            devices = []
            if len(arg) and arg[0] == "get_devices_info":
                for device_info in result:
                    device_data = {}
                    device_data["deviceID"] = str(device_info.get("deviceID"))
                    device_data["name"] = str(device_info.get("name"))
                    device_data["deviceType"] = str(device_info.get("deviceType"))
                    devices.append(device_data)
            info["devices"] = devices

        # System plugin Events response result parser steps
        elif tag == "system_check_macaddress_event":
            result=result[0]
            info = result
            info["Test_Step_Status"] = "SUCCESS"

            for mac in arg:
                if result.get(mac):
                    if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", result.get(mac).lower()) is None:
                        info["Test_Step_Status"] = "FAILURE"
                        break

        elif tag == "system_validate_power_mode":
            result=result[0]
            info["Test_Step_Status"] = "FAILURE"
            if str(result.get("powerState")) == str(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"

        # LoggerPreferences Events response result parser steps
        elif tag == "loggingpreferences_check_onkeystroke_mask_enabled_change_event":
            result = result[0]
            info = result
            if str(result.get("keystrokeMaskEnabled")) in  expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # DataCapture Events response result parser steps
        elif tag == "datacapture_check_on_audioclip_ready_event":
            result = result[0]
            info = result
            if str(result.get("status")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        else:
            print "\nError Occurred: [%s] No Parser steps available for %s" %(inspect.stack()[0][3],methodTag)
            info["Test_Step_Status"] = "FAILURE"

    except Exception as e:
        print "\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e)
        info["Test_Step_Status"] = "FAILURE"

    return info

