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
import json,ast,re
import inspect
from tdkvRDKServicesSupportlib import checkAndGetAllResultInfo
from tdkvRDKServicesSupportlib import checkNonEmptyResultData
from tdkvRDKServicesSupportlib import compareURLs
from tdkvRDKServicesSupportlib import DecodeBase64ToHex
#-----------------------------------------------------------------------------------------------
#               ***  RDK SERVICES VALIDATION FRAMEWORK SUPPORTING FUNCTIONS ***
#-----------------------------------------------------------------------------------------------

class createEventListener(object):
    def __init__(self,deviceIP,devicePort,eventsInfo,trace):
        self.ip = deviceIP
        self.port = devicePort
        self.eventsregistercmds   = eventsInfo.get("eventsRegisterJsonCmds")
        self.eventsunregistercmds = eventsInfo.get("eventsUnRegisterJsonCmds")
        self.trace = trace
        self.access_token = str(eventsInfo.get("token"))
        thread = threading.Thread(target=self.connect, args=())
        thread.daemon = True
        thread.start()
        self.listen = True
        self.listenflag = False
        self.eventsbuffer = []
        self.neweventflag = False
        self.neweventaction   = None
        self.neweventcommand  = None
        self.neweventresponse = None
        self.eventsregisterstatus   = []
        self.eventsunregisterstatus = []
        self.eventsregisterinfo   = []
        self.eventsunregisterinfo = []
    def getEventsRegisterInfo(self):
        return self.eventsregisterinfo
    def getEventsUnRegisterInfo(self):
        return self.eventsunregisterinfo
    def setNewEventDetails(self,cmd,action):
        self.neweventcommand = cmd
        self.neweventaction = action
        self.neweventflag = True
    def getNewEventResponse(self):
        return self.neweventresponse
    def getEventsBuffer(self):
        return self.eventsbuffer
    def clearEventsBuffer(self):
        self.eventsbuffer = []
    def getListenerFlag(self):
        return self.listenflag
    def setListenerFlag(self):
        self.listenflag = True
    def resetListenerFlag(self):
        self.listenflag = False

    def connect(self):
        try:
            print "[INFO]: Opening websocket Connection"
            websocket.enableTrace(self.trace)
            auth = "Authorization: Bearer " + str(self.access_token)
            # # # With Thunder Security Token
            if self.access_token != None:
                websocketConnection = "ws://" + self.ip + ":" + str(self.port) + "/jsonrpc?token="+str(self.access_token)
            # # # Without Thunder Security Token
            else:
                websocketConnection = "ws://" + self.ip + ":" + str(self.port) + "/jsonrpc"
            self.ws = websocket.WebSocketApp(websocketConnection, header=[auth],
                                             on_message = self.on_message,
                                             on_error   = self.on_error,
                                             on_close   = self.on_close,
                                             on_open    = self.on_open)
            self.ws.keep_running = True
            print "[INFO]: Start Event Handler..."
            self.ws.run_forever()
        except Exception as e:
            print e
            print "\nException Occurred while connecting to target device\n"

    def on_open(self):
        def run(*args):
            try:
                print("[INFO]: Registering Events...")
                self.eventsRegisterAndUnRegister("register")
                if "FAILURE" not in self.eventsregisterstatus:
                    print("[INFO]: Events Registration success")
                    print("[INFO]: Starting Event listener...")
                    self.setListenerFlag()
                    while self.listen:
                        time.sleep(1)
                        if self.neweventflag:
                            self.handleNewEvent()
                    print ("[INFO]: Stopped Event listener...")
                    print ("[INFO]: UnRegistering Events...")
                    self.eventsRegisterAndUnRegister("unregister")
                    self.resetListenerFlag()
                    if "FAILURE" not in self.eventsunregisterstatus:
                        print("[INFO]: Events UnRegistration success")
                    else:
                        print("[ERROR]: Events UnRegistration failed")
                    self.ws.close()
                else:
                    print("[ERROR]: Events Registration failed")
            except Exception as e:
                print "\nException Occurred in EventListener thread: [%s] %s" %(inspect.stack()[0][3],e)
        thread.start_new_thread(run, ())


    def eventsRegisterAndUnRegister(self,action):
        if action == "register":
            eventsjsoncmds = self.eventsregistercmds
        elif action == "unregister":
            eventsjsoncmds = self.eventsunregistercmds

        for event in eventsjsoncmds:
            if self.trace:
                if action == "register":
                    print "\n Register Event %s" %(event)
                elif action == "unregister":
                    print "\n UnRegister Event %s" %(event)
            self.clearEventsBuffer()
            self.ws.send(event)
            time.sleep(2)
            response = json.loads(self.getEventsBuffer()[0])
            try:
                if response.get("error") is not None:
                    if "Duplicate registration" in response.get("error").get("message"):
                        status = "SUCCESS"
                    else:
                        status = "FAILURE"
                elif int(response.get("result")) == 0:
                    status = "SUCCESS"
                else:
                    status = "FAILURE"
            except Exception as e:
                status = "FAILURE"
                print "\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e)

            eventinfo = {}
            eventinfo["event"]  = json.loads(event).get("params").get("event")
            eventinfo["status"] = status
            eventinfo["response"] = response
            if action == "register":
                self.eventsregisterstatus.append(status)
                self.eventsregisterinfo.append(eventinfo)
            elif action == "unregister":
                self.eventsunregisterstatus.append(status)
                self.eventsunregisterinfo.append(eventinfo)

    def handleNewEvent(self):
        event = self.neweventcommand
        if self.trace:
            if self.neweventaction== "register":
                print "\n Register Event %s" %(event)
            elif self.neweventaction == "unregister":
                print "\n UnRegister Event %s" %(event)
        self.clearEventsBuffer()
        self.ws.send(event)
        time.sleep(2)
        response = json.loads(self.getEventsBuffer()[0])
        self.neweventresponse = response
        self.neweventflag = False


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
        #self.listenflag = False


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
        # Check whether the response result is empty
        if result == []:
            if len(arg) and arg[0] == "check_empty_event":
                print "\n[INFO]: Not Received the event(s)"
                info["Test_Step_Status"] = "SUCCESS"
            else:
                print "\n[INFO]: Not Received the expected event(s)"
                info["Test_Step_Status"] = "FAILURE"

        # WebKitBrowser Events response result parser steps
        elif tag == "webkitbrowser_check_load_finished_event":
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

        # Controller Events response result parser steps
        elif tag == "controller_check_state_change_event":
            info["Test_Step_Status"] = "FAILURE"
            for eventResult in result:
                if str(eventResult.get("callsign")).lower() == expectedValues[0] and str(eventResult.get("state")).lower() == expectedValues[1] and str(eventResult.get("reason")).lower() == expectedValues[2]:
                    info = eventResult
                    info["Test_Step_Status"] = "SUCCESS"
                    break;
        elif tag == "controller_check_all_event":
            info["Test_Step_Status"] = "FAILURE"
            for eventResult in result:
                if str(eventResult.get("callsign")).lower() == expectedValues[0] and str(eventResult.get("data")["state"]).lower() == expectedValues[1] and str(eventResult.get("data")["reason"]).lower() == expectedValues[2]:
                    info["callsign"] = eventResult.get("callsign")
                    info["state"] = eventResult.get("data")["state"]
                    info["reason"] = eventResult.get("data")["reason"]
                    info["Test_Step_Status"] = "SUCCESS"
                    break;

        # Wifi Events response result parser steps
        elif tag == "wifi_check_state_change_event":
            info["Test_Step_Status"] = "FAILURE"
            for eventResult in result:
                if str(eventResult.get("state")) in str(expectedValues[0]):
                    info = eventResult
                    info["Test_Step_Status"] = "SUCCESS"
                    break;

        elif tag == "wifi_check_available_ssids_event":
            ssids = []
            frequencies = []
            status = []
            for ssid_info in result:
                if ssid_info.get("ssids"):
                    status.append("TRUE")
                else:
                    status.append("FALSE")
            if "TRUE" in status:
                for ssid_info in result:
                    for ssid_data in ssid_info.get("ssids"):
                        if "\\x00" not in str(ssid_data.get("ssid")):
                            ssids.append(str(ssid_data.get("ssid")))
                            frequencies.append(str(ssid_data.get("frequency")))
            else:
                message = "Available ssids list is empty"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "FAILURE"
            if len(arg) and arg[0] == "get_ssid_names":
                if not ssids and "TRUE" not in status:
                    info["Test_Step_Status"] = "FAILURE"
                else:
                    info["ssids"] = ssids
                    info["Test_Step_Status"] = "SUCCESS"
            elif len(arg) and arg[0] == "check_scanned_ssid_name":
                if not ssids and "TRUE" not in status:
                    info["Test_Step_Status"] = "FAILURE"
                else:
                    ssid_found = 0
                    for ssid in ssids:
                        if ssid in expectedValues:
                            info["ssid"] = ssid
                            ssid_found = 1
                            break
                    if ssid_found == 1:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
            elif len(arg) and arg[0] == "check_scanned_ssid_frequency":
                if not ssids and "TRUE" not in status:
                    info["Test_Step_Status"] = "FAILURE"
                else:
                    info["result"] =  dict(zip(ssids,frequencies))
                    resultStatus = "TRUE"
                    for frequency in frequencies:
                        if frequency not in expectedValues:
                            resultStatus = "FALSE"
                            break
                    if "FALSE" not in resultStatus:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
 
        elif tag == "wifi_check_on_error_event":
            result = result[0]
            info = result
            if int(result.get("code")) == int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # FrameRate Events response result parser steps
        elif tag == "framerate_check_fps_event":
            fps_info = []
            flag = 0
            for fps_data in result:
                fps_info.append(fps_data)
                if fps_data.get("average") <= 0 and fps_data.get("min") <= 0 and fps_data.get("max") <= 0:
                    flag = 1
            info["fps_info"] = fps_info
            if flag==1:
                info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "SUCCESS"

        elif tag == "framerate_check_display_framerate_changed_event":
            result = result[0]
            info = result
            if result:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

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

        elif tag == "bluetooth_check_status_changed_event":
            info["Test_Step_Status"] = "FAILURE"
            for eventResult in result:
                if str(eventResult.get("newStatus")) == str(expectedValues[0]):
                    info = eventResult
                    info["Test_Step_Status"] = "SUCCESS"
                    break;

        elif tag == "bluetooth_check_request_failed_event":
            result=result[0]
            info = result
            if str(result.get("newStatus")) == str(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

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
            powerState = str(result.get("powerState"))
            if str(expectedValues[0]) == "STANDBY" and powerState == "LIGHT_SLEEP" or powerState == "STANDBY" or str(expectedValues[0]) == "ON" and powerState == "ON":
                info["Test_Step_Status"] = "SUCCESS"

        elif tag == "system_check_temperature_threshold_change_event":
            result=result[0]
            info["Test_Step_Status"] = "FAILURE"
            if str(result.get("exceeded")) == "true":
                info["Test_Step_Status"] = "SUCCESS"

        elif tag == "system_check_system_mode_change_event":
            result = result[0]
            info = result
            if str(result.get("mode")) in  expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_check_reboot_reason_event":
             result=result[0]
             info = result
             info["Test_Step_Status"] = "FAILURE"
             if str(result.get("rebootReason")) == str(expectedValues[0]) and str(result.get("requestedApp")).lower() == str(expectedValues[1]).lower():
                info["Test_Step_Status"] = "SUCCESS"

        elif tag == "system_check_network_standby_mode_changed_event":
            result = result[0]
            info = result
            if str(result.get("nwStandby")) in  expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        # LoggerPreferences Events response result parser steps
        elif tag == "loggingpreferences_check_onkeystroke_mask_enabled_change_event":
            result = result[0]
            info = result
            if str(result.get("keystrokeMaskEnabled")) in  expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # DisplaySettings Events response result parser steps
        elif tag == "displaysettings_check_zoom_settings_updated_event":
            result = result[0]
            info = result
            if str(result.get("zoomSetting")) in  expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "displaysettings_check_resolution_changed_event":
            result = result[0]
            info = result
            if str(result.get("resolution")) in  expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "displaysettings_check_resolution_prechange_event":
            result = result[0]
            if not result:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # Timer Events response result parser steps
        elif tag == "timer_check_timer_expired_event":
            result = result[0]
            info = result
            if int(result.get("status")) ==  int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "timer_check_timer_expiry_reminder_event":
            result = result[0]
            info = result
            if int(result.get("timeRemaining")) <= int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # Network Events response result parser steps
        elif tag == "network_check_interface_status_change_event":
            result = result[0]
            info = result
            if str(result.get("enabled")) in expectedValues and str(result.get("interface")).lower() == str(expectedValues[0]).lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "network_connection_status_change_event":
            info["Test_Step_Status"] = "FAILURE"
            for eventResult in result:
                if str(eventResult.get("interface")) == "WIFI" and str(eventResult.get("status")) in  expectedValues:
                    info = eventResult
                    info["Test_Step_Status"] = "SUCCESS"
                    break; 
        # DataCapture Events response result parser steps
        elif tag == "datacapture_check_on_audioclip_ready_event":
            result = result[0]
            info = result
            if str(result.get("status")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # ScreenCapture Events response result parser steps
        elif tag == "screencapture_check_upload_complete_event":
            if arg[0] == "check_upload_status":
                info["Test_Step_Status"] = "FAILURE"
                for eventResult in result:
                    if str(eventResult.get("status")) in  expectedValues:
                        info = eventResult
                        info["Test_Step_Status"] = "SUCCESS"
                        break;
            elif arg[0] == "check_status_and_callguid":
                info["Test_Step_Status"] = "FAILURE"
                for eventResult in result:
                    if str(eventResult.get("status")) in  expectedValues and str(eventResult.get("call_guid")) in  expectedValues:
                        info = eventResult
                        info["Test_Step_Status"] = "SUCCESS"
                        break;

        # HdmiCec Events response result parser steps
        elif tag == "hdmicec_check_on_message_event":
            Src_Dest_Address = {"0":"TV","1":"Recording Device 1","2":"Recording Device 2","3":"Tuner 1","4":"Playback Device 1","5":"Audio System","6":"Tuner 2","7":"Tuner 3","8":"Playback Device 2","9":"Recording Device 3","a":"Tuner 4","b":"Playback Device 3","c":"Reserved 12","d":"Reserved 13","e":"Specific Use","f":"Broadcast/Unregistered"}
            info["Test_Step_Status"] = "FAILURE"
            for eventResult in result:
                if len(str(eventResult.get("message"))) > 0:
                    hex_code = DecodeBase64ToHex(str(eventResult.get("message")))
                    if arg[0] == "check_power_status":
                       if "90" in str(hex_code):
                           info["Hex_Code"] = hex_code
                           Power_Status = {"00":"On","01":"Standby","10":"In transition Standby to On","11":"In transition On to Standby"}
                           Oprand  = hex_code[-2:]
                           Address = hex_code[0:2]
                           info["From"] = Src_Dest_Address[Address[0]]
                           info["To"] =  Src_Dest_Address[Address[1]]
                           info["Power_Status"] = Power_Status[Oprand]
                           info["Test_Step_Status"] = "SUCCESS"

                    elif arg[0] == "check_cec_version":
                      if "9e" in str(hex_code).lower():
                          Version = {"01":"Reserved","02":"Reserved","03":"Reserved","04":"Reserved","05":"Version 1.3a","06":"Version 1.4" }
                          Oprand  = hex_code[-2:]
                          Address = hex_code[0:2]
                          info["From"] = Src_Dest_Address[Address[0]]
                          info["To"] =  Src_Dest_Address[Address[1]]
                          info["Version"] = Version[Oprand]
                          info["Test_Step_Status"] = "SUCCESS"

                    elif arg[0] == "check_menu_language":
                      if "32" in str(hex_code):
                          MenuLanguage  = hex_code[2:4]
                          Address = hex_code[0:2]
                          info["From"] = Src_Dest_Address[Address[0]]
                          info["To"] =  Src_Dest_Address[Address[1]]
                          info["Menu_Language"] = MenuLanguage
                          info["Test_Step_Status"] = "SUCCESS"

                    elif arg[0] == "check_device_vendor_id":
                      if "87" in str(hex_code):
                          VendorID  = hex_code[2:4]
                          Address = hex_code[0:2]
                          info["From"] = Src_Dest_Address[Address[0]]
                          info["To"] =  Src_Dest_Address[Address[1]]
                          info["Device_Vendor_ID"] = VendorID
                          info["Test_Step_Status"] = "SUCCESS"

                else:
                    info["Test_Step_Status"] = "FAILURE"
        # Warehouse Events response result parser steps
        elif tag == "warehouse_check_device_reset_event":
            result=result[0]
            info = result
            if str(result.get("success")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # StateObserver Events response result parser steps
        elif tag == "stateobserver_check_property_changed_event":
            result=result[0]
            info = result
            if str(result.get("value")) in expectedValues and int(result.get("error"))==0:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # RDKShell Events response result parser steps
        elif tag == "rdkshell_check_on_launched_event":
            result=result[0]
            info = result
            if str(result.get("client")) ==  str(expectedValues[0]) and str(result.get("launchType"))== str(expectedValues[1]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_application_state_event":
            info["Test_Step_Status"] = "FAILURE"
            for eventResult in result:
                if str(eventResult.get("client")) in expectedValues:
                    info["client"] = eventResult.get("client")
                    info["Test_Step_Status"] = "SUCCESS"

        elif tag == "rdkshell_check_on_userinactivity_event":
            if len(arg) and arg[0] == "check_user_inactive":
                result1=result[0]
                result2=result[1]
                difference = int(float(result2.get("minutes"))) - int(float(result1.get("minutes")))
                if difference == int(expectedValues[0]):
                    info["User_Inactivity_Minutes"] = difference
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif len(arg) and arg[0] == "check_reset_inactivity_interval":
                info["Test_Step_Status"] = "FAILURE"
                for eventResult in result:
                    if int(float(eventResult.get("minutes"))) == int(expectedValues[0]):
                        info["User_Inactivity_Minutes"] = eventResult.get("minutes")
                        info["Test_Step_Status"] = "SUCCESS"
            elif len(arg) and arg[0] == "check_empty_event":
                if result:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                result = result[0]
                info = result
                if result.get("minutes"):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_on_will_destroy_event":
            result=result[0]
            info = result
            if str(result.get("callsign")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # TextToSpeech Events response result parser steps
        elif tag == "texttospeech_check_tts_state_changed_event":
            result = result[0]
            info = result
            if str(result.get("state")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
     
        # Cobalt Events response result parser steps
        elif tag == "cobalt_check_state_change_event":
            result = result[0]
            info = result
            if str(result.get("suspended")).lower() in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        
        elif tag == "cobalt_check_closure_event":
            result = result[0]
            if result == "":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
                
        # DisplayInfo Events response result parser steps
        elif tag == "displayinfo_check_pre_post_resolution_change_event":
            info["Test_Step_Status"] = "FAILURE"
            for eventResult in result:
                if str(eventResult.get("event")).lower() in expectedValues:
                    info = eventResult
                    info["Test_Step_Status"] = "SUCCESS"
                    break;

        # Messenger Events response result parser steps
        elif tag == "messenger_check_room_updated_event":
            result = result[0]
            info = result
            if str(result.get("room")).lower() == str(expectedValues[0]) and str(result.get("action")).lower() == str(expectedValues[1]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "messenger_check_user_update_event":
            info["Test_Step_Status"] = "FAILURE"
            for eventResult in result:
                if str(eventResult.get("user")).lower() == str(expectedValues[0]) and str(eventResult.get("action")).lower() == str(expectedValues[1]):
                    info = eventResult
                    info["Test_Step_Status"] = "SUCCESS"
                    break;

        elif tag == "check_event_registration":
            if len(arg) and arg[0] == "check_user_update_event":
                if str(result.get("user")).lower() == str(expectedValues[0]) and str(result.get("action")).lower() == str(expectedValues[1]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["result"] = result
                if int(result) == int(expectedValues[0]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "messenger_check_message_event":
            result = result[0]
            info = result
            if str(result.get("user")).lower() == str(expectedValues[0]) and str(result.get("message")).lower() == str(expectedValues[1]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # HdmiCecSink Events response result parser steps
        elif tag == "hdmicecsink_check_on_active_source_change_event":
            info["Test_Step_Status"] = "FAILURE"
            for eventResult in result:
                if int(eventResult.get("logicalAddress")) == int(expectedValues[0]) and str(eventResult.get("physicalAddress")).lower() == str(expectedValues[1]).lower():
                    info = eventResult
                    info["Test_Step_Status"] = "SUCCESS"
                    break;

        # PlayerInfo Events response result parser steps
        elif tag == "playerinfo_check_dolby_audiomode_changed_event":
            result = result[0]
            info = result
            if "AUTO" in expectedValues:
                for Mode in arg:
                    if "auto" in Mode.lower():
                        if "dolby" in Mode.lower():
                            expectedMode = "surround"
                            break
                        else:
                            expectedMode = Mode.lower()
            else:
                expectedMode = str(expectedValues[0]).lower()
            if result.get('mode').lower() == expectedMode or result.get('mode').lower() in expectedMode:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # DTV Events response result parser steps
        elif tag == "dtv_check_search_status_event":
            info["Test_Step_Status"] = "FAILURE"
            for eventResult in result:
                if str(eventResult.get("eventtype")).lower() == expectedValues[0] and str(eventResult.get("finished")).lower() == expectedValues[1] and str(eventResult.get("progress")).lower() == expectedValues[2]:
                    info = eventResult
                    info["Test_Step_Status"] = "SUCCESS"
                    break;

        # PersistentStore Events response result parser steps
        elif tag == "persistentstore_check_on_value_changed_event":
            result = result[0]
            info = result
            if str(result.get("namespace")).lower() == expectedValues[0] and str(result.get("key")).lower() == expectedValues[1] and str(result.get("value")).lower() == str(expectedValues[2]).lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # CompositeInput Events response result parser steps
        elif tag == "compositeinput_check_input_status_changed_event":
            info["Test_Step_Status"] = "FAILURE"
            for eventResult in result:
                if str(eventResult.get("status")).lower() in expectedValues:
                    info = eventResult
                    info["Test_Step_Status"] = "SUCCESS"
                    break;

        # HdmiCecSink Events response result parser steps
        elif tag == "hdmicecsink_check_report_cec_enabled_event":
            result = result[0]
            info = result
            if str(result.get("cecEnable")).lower() == str(expectedValues[0]).lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # FirmwareControl Events response result parser steps
        elif tag == "fwc_check_upgrade_progress_event":
            print "Events list :",result
            expectedStatusList = ["none", "upgradestarted", "downloadstarted", "downloadaborted", "downloadcompleted", "installinitiated", "installnotstarted", "installaborted", "installstarted", "upgradecompleted", "upgradecancelled"]
            status = True
            for event in result:
                info = event
                if str(event.get("status")) not in expectedStatusList: 
                    status = False
            if status:
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
