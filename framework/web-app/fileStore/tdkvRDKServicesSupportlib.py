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
import inspect
import json , ast
import collections
from pexpect import pxssh
import ConfigParser
from base64 import b64encode, b64decode
import codecs
from time import sleep
import re
import subprocess
import requests

# To use the REST API variables
#import CertificationSuiteCommonVariables

#-----------------------------------------------------------------------------------------------
#               ***  RDK SERVICES VALIDATION FRAMEWORK SUPPORTING FUNCTIONS ***
#-----------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------
# CheckAndGenerateTestStepResult
#-----------------------------------------------------------------------------------------------
# Syntax      : CheckAndGenerateTestStepResult(result,methodTag,arguments,expectedValues,otherInfo)
# Description : Method to parse the output JSON response and generate test result
# Parameter   : result - JSON response result value
#             : methodTag - tag used to identify the parser step
#             : arguments - list of arguments used for parsing
#             : expectedValues - list of expected values
#             : otherInfo - list of other response messages like error/message etc
# Return Value: Result Info Dictionary
#-----------------------------------------------------------------------------------------------
def CheckAndGenerateTestStepResult(result,methodTag,arguments,expectedValues,otherInfo={}):
    tag  = methodTag
    arg  = arguments

    # Input Variables:
    # a. result - result from response JSON
    # b. methodTag - string
    # c. arguments - list
    # d. expectedValues - list
    # e. otherInfo - list

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
        if result == {} or result == [] or result == "":
            print "\n[INFO]: Received empty JSON response result"
            info["Test_Step_Status"] = "FAILURE"

        # DeviceInfo Plugin Response result parser steps
        elif tag == "deviceinfo_get_system_info":

            if arg[0] == "check_cpu_load":
                info["cpu_load"] = result.get("cpuload")
                if int(info["cpu_load"]) < 90:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

            elif arg[0] == "get_all_info":
                info = checkAndGetAllResultInfo(result)

        elif tag == "deviceinfo_get_network_info":
            if arg[0] == "get_all_info":
                status = []
                network_info = []
                for interface in result:
                    interface_info = []
                    interface_info.append(interface.get("name"))
                    interface_info.append(interface.get("mac"))
                    interface_details  = "Name :" + interface.get("name") + " - "
                    interface_details += "MAC :"  + interface.get("mac")  + " - "
                    if interface.get("ip") is not None and len(interface.get("ip")):
                        ip_info = [ str(ip) for ip in interface.get("ip") ]
                        interface_info.extend(ip_info)
                        interface_details += "IP :" + str(ip_info)
                    else:
                        interface_details += "IP:"  + str(interface.get("ip"))
                    network_info.append(interface_details)
                    status.append(checkNonEmptyResultData(interface_info))
                info["network_info"] = network_info
                if "FALSE" not in status and len(network_info) != 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "deviceinfo_get_socket_info":
            if arg[0] == "get_all_info":
                info = checkAndGetAllResultInfo(result)


        # LocationSync Plugin Response result parser steps
        elif tag == "locationsync_get_location_info":
            if arg[0] == "get_all_info":
                info = checkAndGetAllResultInfo(result)

        # OCDM Plugin Response result parser steps
        elif tag == "ocdm_get_drm_info":
            if arg[0] == "get_all_info":
                status = []
                drm_info = []
                for drm in result:
                    drm_details = []
                    drm = eval(json.dumps(drm))
                    drm_details.append(drm.get("name"))
                    if drm.get("keysystems") is not None and len(drm.get("keysystems")):
                        key_info = [ str(key) for key in drm.get("keysystems") ]
                        drm_details.extend(key_info)
                    else:
                        status.append("FALSE")
                    drm_info.append(drm)
                    status.append(checkNonEmptyResultData(drm_details))
                info["drm_info"] = drm_info
                if "FALSE" not in status and len(drm_info) != 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "ocdm_get_drm_key_info":
            if arg[0] == "check_drm_key":
                key_info = []
                key_valid_status = "TRUE"
                for key in result:
                    key_info.append(str(key))
                    if key not in expectedValues:
                        key_valid_status = "FALSE"
                info["keysystems"] = key_info
                if key_valid_status == "TRUE":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        # DeviceIdentification Plugin Response result parser steps
        elif tag == "deviceidentification_get_platform_info":
            info = result.copy()
            status = checkNonEmptyResultData(info.values())
            if status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # TraceControl Plugin Response result parser steps
        elif tag == "tracecontrol_get_state":

            info["state"]    = result.get("settings")[0].get("state")
            info["module"]   = result.get("settings")[0].get("module")
            info["category"] = result.get("settings")[0].get("category")
            if arg[0] == "check_state":
                if info["state"] in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"


        # Network Plugin Response result parser steps
        elif tag == "network_get_interface_info":
            status = []
            interfaces_info = result.get("interfaces")
            for interface in interfaces_info:
                status.append(checkNonEmptyResultData(interface.values()))
            if "FALSE" not in status and len(interfaces_info) != 0:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

            if arg[0] == "get_all_info":
                info["interfaces"] = interfaces_info
            elif arg[0] == "get_interface_names":
                interface_names = []
                for interface in interfaces_info:
                    interface_names.append(interface.get("interface"))
                interface_names = [ str(name) for name in interface_names if str(name).strip() ]
                info["interface_names"] = interface_names

        elif tag == "network_get_default_interface":
            default_interface = result.get("interface")
            info["default_interface"] = default_interface
            if len(arg) and arg[0] == "check_interface":
                if default_interface in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"


        elif tag == "network_check_results":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "network_get_named_endpoints":
            result = result.get("endpoints")
            endpoints = [ str(name) for name in result if str(name).strip() ]
            info["endpoints"] = endpoints
            if len(endpoints):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "network_get_ping_response":
            info = result.copy()
            target = result.get("target")
            tx_packets = int(result.get("packetsTransmitted"))
            rx_packets = int(result.get("packetsReceived"))
            packets_loss = result.get("packetLoss")
            if "duplicates" in packets_loss:
                packets_loss = packets_loss.split("duplicates")[0]
            success = str(result.get("success")).lower() == "true"
            if len(arg) and arg[0] == "check_target":
                packets = int(expectedValues[0])
                host_ip = expectedValues[1]
                if success and target == host_ip and tx_packets == packets and rx_packets == packets and int(packets_loss) == 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                packets = int(expectedValues[0])
                if success and target.strip() and tx_packets == packets and rx_packets == packets and int(packets_loss) == 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "network_get_trace_response":
            info = result.copy()
            result_data = result.get("results")
            success = str(result.get("success")).lower() == "true"
            error_status = "FALSE"
            for data in result_data:
                if "ERROR" in data or "error" in data:
                    error_status = "TRUE"
            if len(arg) and arg[0] == "check_target":
                host_ip = expectedValues[0]
                if success and result.get("target") == host_ip and error_status == "FALSE":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if success and error_status == "FALSE":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"


        elif tag == "network_get_ip_settings":
            info = result.copy()
            if result.get("interface") == expectedValues[0]:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        elif tag == "network_get_interface_status":
            info["enabled"] = result.get("enabled")
            if str(result.get("enabled")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        elif tag == "network_check_interface_enable_set_status":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "network_check_connectedto_internet":
            info["ConnectedToInternet"] = result.get("connectedToInternet")
            status = checkNonEmptyResultData(result)
            if status and str(result.get("connectedToInternet")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "network_check_device_ip_changed":
            info["Device_IP"] = result.get("ip")
            if str(result.get("ip")) != str(expectedValues):
                message = "Internally received onIPAddressStatusChanged event and default interface changed"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # Front Panel Response result parser steps
        elif tag == "frontpanel_get_led_info":
            supported_leds = result.get("supportedLights")
            supported_leds_info = []
            for led in supported_leds:
                led_info = result.get("supportedLightsInfo").get(led).copy()
                led_info["index"] = led
                supported_leds_info.append(led_info)
            status = []
            status.append(checkNonEmptyResultData(supported_leds))
            success = str(result.get("success")).lower() == "true"
            for led_info in supported_leds_info:
                status.append(checkNonEmptyResultData(led_info.values()))
            if arg[0] == "get_all_info":
                info["supported_leds"] = supported_leds
                info["supported_leds_info"] = supported_leds_info
            elif arg[0] == "get_power_led_info":
                info = result.get("supportedLightsInfo").get("power_led").copy()
                info["index"] = "power_led"
            elif arg[0] == "get_data_led_info":
                info = result.get("supportedLightsInfo").get("data_led").copy()
                info["index"] = "data_led"
            elif arg[0] == "get_record_led_info":
                info = result.get("supportedLightsInfo").get("record_led").copy()
                info["index"] = "record_led"

            if success and "FALSE" not in status and len(supported_leds):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "frontpanel_get_fp_or_clock_brightness":
            brightness = result.get("brightness")
            status = checkNonEmptyResultData(brightness)
            success = str(result.get("success")).lower() == "true"
            info["brightness"] = brightness
            if len(arg) and arg[0] == "check_brightness_level":
                if success and status == "TRUE" and int(brightness) == int(expectedValues[0]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if success and status == "TRUE":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "frontpanel_get_led_brightness":
            brightness = result.get("brightness")
            status = checkNonEmptyResultData(brightness)
            success = str(result.get("success")).lower() == "true"
            info["brightness"] = brightness
            if len(expectedValues) == 1:
                if success and status == "TRUE" and int(brightness) == int(expectedValues[0]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if success and status == "TRUE" and int(brightness) >= int(expectedValues[0]) and int(brightness) <= int(expectedValues[1]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "frontpanel_get_clock_mode":
            info["is24Hour"] = result.get("is24Hour")
            success = str(result.get("success")).lower() == "true"
            expectedValues = [str(value).lower() for value in expectedValues]
            if success and str(result.get("is24Hour")).lower() in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "frontpanel_set_operation_status":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "frontpanel_get_preferences":
            info["preferences"] = result.get("preferences")
            success = str(result.get("success")).lower() == "true"
            expectedValues = ",".join(expectedValues)
            expectedValues = json.loads(str(expectedValues))
            if success and expectedValues == result.get("preferences"):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # WebKitBrowser Plugin Response result parser steps
        elif tag == "webkitbrowser_get_state":
            info["state"] = result
            if result in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_check_url":
            info["url"] = result
            status = compareURLs(result,expectedValues[0])
            if status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_get_visibility":
            info["visibility"] = result
            if result in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "webkitbrowser_check_fps":
            if int(result) >= 0:
                info["fps"] = result
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        elif tag == "webkitbrowser_get_cookie_policy":
            info["cookie_accept_policy"] = result
            if result in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_get_local_storage_availability":
            info["enabled"] = result
            if str(result) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_check_languages":
            info["languages"] = result
            status = [ "FALSE" for lang in result if lang not in expectedValues ]
            if "FALSE" not in status:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_get_useragent":
            info["useragent"] = result
            status = checkNonEmptyResultData(result)
            if len(arg) and arg[0] == "check_useragent":
                if status == "TRUE" and result in ",".join(expectedValues):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_get_headers":
            info["headers"] = result
            if len(result) > 0:
                status = []
                for data in result:
                    status.append(checkNonEmptyResultData(data.values()))
                if len(arg) and arg[0] == "check_header":
                    if "FAILURE" not in status and data.get("name") in expectedValues and data.get("value") in expectedValues:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                else:
                    if "FAILURE" not in status:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"


        # Cobalt Plugin Response result parser steps
        elif tag == "cobalt_get_state":
            info["state"] = result
            if result in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "cobalt_validate_accessibility_settings":
            status = checkNonEmptyResultData(result)
            closedcaptions = result.get("closedcaptions")
            textdisplay = result.get("textdisplay")
            for key,value in closedcaptions.items():
                info[key] = value
            info["ishighcontrasttextenabled"] = textdisplay.get("ishighcontrasttextenabled")
            if status and str(closedcaptions.get("isenabled")).lower() == str(expectedValues[0]).lower() and closedcaptions.get("backgroundcolor") == expectedValues[1] and closedcaptions.get("backgroundopacity") == expectedValues[2] and closedcaptions.get("characteredgestyle") == expectedValues[3] and closedcaptions.get("fontcolor") == expectedValues[4] and closedcaptions.get("fontfamily") == expectedValues[5] and closedcaptions.get("fontopacity") == expectedValues[6] and closedcaptions.get("fontsize") == expectedValues[7] and closedcaptions.get("windowcolor") == expectedValues[8] and closedcaptions.get("windowopacity") == expectedValues[9] and str(textdisplay.get("ishighcontrasttextenabled")).lower() == str(expectedValues[10]).lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # Device Diagnostics Plugin Response parser steps
        elif tag == "devicediagnostics_get_configurations":
            params_info = result.get("paramList")
            status = []
            params_detail = []
            success = str(result.get("success")).lower() == "true"
            for param in params_info:
                detail = []
                detail.append(param.get("name"))
                detail.append(param.get("value"))
                status.append(checkNonEmptyResultData(detail))
                params_detail.append(str(detail[0]) + " - " + str(detail[1]))
            info["param_list"] = params_detail
            if success and "FALSE" not in status:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # HDCP Profile Plugin Response result parser steps
        elif tag == "hdcpprofile_get_general_info":
            if arg[0] == "get_stb_hdcp_info":
                info = checkAndGetAllResultInfo(result,result.get("success"))
            elif arg[0] == "get_hdcp_status":
                info = checkAndGetAllResultInfo(result.get("HDCPStatus"),result.get("success"))
                if str(info["isConnected"]).lower() == expectedValues[0]:
                    info["Test_Step_Status"] = "SUCCESS"
                    if str(info["isConnected"]).lower() == "false" and str(info["isHDCPCompliant"]).lower() != "false":
                        info["Test_Step_Status"] = "FAILURE"
                else:
                    info["Test_Step_Status"] = "FAILURE"


        # System Plugin Response result parser steps
        elif tag == "system_get_api_info":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "system_get_xconf_info":
            info = checkAndGetAllResultInfo(result.get("xconfParams"),result.get("success"))

        elif tag == "system_get_rfc_info":
            info = checkAndGetAllResultInfo(result.get("RFCConfig"),result.get("success"))
            rfc_values = result.get("RFCConfig").values()
            for rfc_data in rfc_values:
                if "ERROR" in rfc_data or "error" in rfc_data:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_get_gz_enabled_status":
            info["enabled"] = result.get("enabled")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("enabled")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_check_set_operation":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_check_cache":
            if str(result.get("success")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_check_cache_key":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if result.get(expectedValues[0]) == str(expectedValues[1]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_get_power_state":
            powerState = result.get("powerState")
            info["powerState"] = powerState
            success = str(result.get("success")).lower() == "true"
            if success and powerState in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_get_available_standby_modes":
            supportedStandbyModes = result.get("supportedStandbyModes")
            status = checkNonEmptyResultData(supportedStandbyModes)
            success = str(result.get("success")).lower() == "true"
            info["supportedStandbyModes"] = supportedStandbyModes
            if len(arg) and arg[0] == "check_mode":
                if success and status == "TRUE" and all( mode in supportedStandbyModes for mode in expectedValues ):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if success and status == "TRUE":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_get_preferred_standby_mode":
            preferredStandbyMode = result.get("preferredStandbyMode")
            success = str(result.get("success")).lower() == "true"
            info["standbyMode"] = preferredStandbyMode
            if success and preferredStandbyMode in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_get_timezone_dst":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if len(arg) and arg[0] == "check_timezone":
                if info.get("timeZone") in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_get_state_info":
            if len(arg):
                info = checkAndGetAllResultInfo(result.get(arg[0]),result.get("success"))
            else:
                info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "system_validate_core_temperature":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if int(float(result.get("temperature"))) > 0:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_validate_modes":
            mode_info = result.get("modeInfo")
            info = checkAndGetAllResultInfo(mode_info,result.get("success"))
            if str(mode_info.get("mode")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_validate_bool_result":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            status = str(result.get(arg[0])).lower()
            if status in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_verify_thresholds_params":
            success = str(result.get("success")).lower() == "true"
            result = result.get("temperatureThresholds")
            info["WARN"] = result.get("WARN")
            info["MAX"] =  result.get("MAX")
            if len(arg) and arg[0] == "validate_threshold_params":
                if success and float(result.get("WARN")) == float(expectedValues[0]) and float(result.get("MAX")) == float(expectedValues[1]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if success:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag== "system_check_mac_address":
            if arg[0] == "bluetooth_mac":
                info["bluetooth_mac"] = result.get("bluetooth_mac")
                macAddress = result.get("bluetooth_mac")
                success = str(result.get("success")).lower() == "true"
                status = checkNonEmptyResultData(result.get("bluetooth_mac"))
            elif arg[0] == "wifi_mac":
                info["wifi_mac"] = result.get("wifi_mac")
                macAddress = result.get("wifi_mac")
                success = str(result.get("success")).lower() == "true"
                status = checkNonEmptyResultData(result.get("wifi_mac"))
            if success and status == "TRUE":
                if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macAddress.lower()) is None:
                    info["Test_Step_Status"] = "FAILURE"
                else:
                    info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "system_validate_powerstate_before_reboot":
            powerState = result.get("state")
            info["powerState"] = powerState
            success = str(result.get("success")).lower() == "true"
            if success and powerState in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "system_check_telemetry_optout_status":
            success = str(result.get("success")).lower() == "true"
            info["Opt-Out"] = result.get("Opt-Out")
            if success and str(result.get("Opt-Out")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "system_get_downloaded_firmware_info":
            currentFWVersion = result.get("currentFWVersion")
            info["current_FW_version"] = currentFWVersion
            status = checkNonEmptyResultData(result.get("currentFWVersion"))
            success = str(result.get("success")).lower() == "true"
            if len(arg) and arg[0] == "check_image":
                if success and status == "TRUE" and currentFWVersion in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if  success and status == "TRUE":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        elif tag == "system_check_custom_reboot_reason":
            info = checkAndGetAllResultInfo(result.get(arg[0]),result.get("success"))
            result = result.get(arg[0])
            if result.get("customReason") in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # User Preferces Plugin Response result parser steps
        elif tag == "userpreferences_get_ui_language":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if len(arg) and arg[0] == "check_language":
                if result.get("ui_language") == expectedValues[0]:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        elif tag == "userpreferences_check_set_operation":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        #Code for RDK Shell plugin

        elif tag == "rdkshell_get_connected_client_list":
            result = result.get("clients")
            clients = [ str(name) for name in result if str(name).strip() ]
            info["clients"] = clients
            #Minimum two clients have to be running to effectivly perform RDK Shell test cases
            if len(clients) >= 2:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_get_result_status":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_for_results":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            
        elif tag == "rdkshell_check_for_visibility_result":
            if len(expectedValues) > 1 :
                if str(result.get("visible")).lower() in str(expectedValues[0]).lower() or str(result.get("visible")).lower() in str(expectedValues[1]).lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif str(result.get("visible")).lower() in str(expectedValues[0]).lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        # read previously set resolution and compare it
        elif tag == "rdkshell_check_for_resolution_set":
            w = int(result.get("w"))
            h = int(result.get("h"))
            expectedw = int(expectedValues[0])
            expectedh = int(expectedValues[1])
            if w == expectedw and h == expectedh:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_for_bounds":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            result=result.get("bounds")
            info["x"]=str(result.get("x"))
            info["y"]=str(result.get("y"))
            info["w"]=str(result.get("w"))
            info["h"]=str(result.get("h"))
            if len(expectedValues)>0:
                 x = str(result.get("x"))
                 y = str(result.get("y"))
                 w = str(result.get("w"))
                 h = str(result.get("h"))
                 expectedx = expectedValues[0]
                 expectedy = expectedValues[1]
                 expectedw = expectedValues[2]
                 expectedh = expectedValues[3]
                 if x == expectedx and  y == expectedy and  w == expectedw and  h == expectedh:
                     info["Test_Step_Status"] = "SUCCESS"
                 else:
                     info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_validate_opacity":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            status = result.get("opacity")
            if len(expectedValues)>0:
                if int(expectedValues[0]) == int(status):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif int(status) >= 0 and int(status) <=100 :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_verify_scale_params":
            if float(result.get("sx")) == float(expectedValues[0]) and float(result.get("sy")) == float(expectedValues[1]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_application":
            result = result.get("clients")
            clients = [ str(name) for name in result if str(name).strip() ]
            if arg[0] == "check_not_exists":
                if expectedValues[0] not in clients:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

            elif arg[0] == "check_if_exists":
                if expectedValues[0] in clients:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_get_state":
            success = str(result.get("success")).lower() == "true"
            result = result.get("state")
            for data in result:
                if(data.get("callsign")) == str(arg[0]):
                    break;
            if success and data.get("callsign") ==  str(arg[0]) and str(data.get("state")) in expectedValues:
                info["callsign"] = data.get("callsign")
                info["state"] = data.get("state")
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
         
        elif tag == "rdkshell_check_log_level":
            success = str(result.get("success")).lower() == "true"
            info["LogLevel"] = result.get("logLevel")
            if success and str(result.get("logLevel")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_hole_punch":
            success = str(result.get("success")).lower() == "true"
            info["holePunch"] = result.get("holePunch")
            if success and str(result.get("holePunch")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_validate_topmost_client":
            success = str(result.get("success")).lower() == "true"
            TopMostClient = result.get("clients")[0]
            info["TopMostClient"] = result.get("clients")[0]
            if success and TopMostClient in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_key_repeats_status":
            success = str(result.get("success")).lower() == "true"
            info["enable"] = result.get("keyRepeat")
            if success and str(result.get("keyRepeat")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"        

        elif tag == "rdkshell_get_enabled_status":
            success = str(result.get("success")).lower() == "true"
            info["enabled"] = result.get("enabled")
            if success and str(result.get("enabled")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_get_virtual_resolution":
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result)
            info["width"] = result.get("width")
            info["height"] = result.get("height")
            if success and status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
            if len(arg) and  arg[0] == "check_virtual_resolutions":
                if success and str(result.get("width")) == str(expectedValues[0]) and  str(result.get("height")) == str(expectedValues[1]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_error_message":
            success = str(result.get("success")).lower() == "false"
            info["message"] = result.get("message")
            if success and result.get("message") in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        # DisplayInfo Plugin Response result parser steps
        elif tag == "displayinfo_get_general_info":
            if arg[0] == "get_all_info":
                info = checkAndGetAllResultInfo(result)

        elif tag == "displayinfo_check_for_nonempty_result":
            info["Result"] = result
            status = checkNonEmptyResultData(result)
            if status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        
        elif tag == "displayinfo_validate_results":
            info["Result"] = result
            if result > 0:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "displayinfo_validate_boolean_result":
            if str(result) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "displayinfo_validate_width_or_height":
            if arg[0] == "width":
                index = 0
            elif arg[0] == "height":
                index = 1
            SupportingRes=expectedValues
            Resolution_Details = {}
            for values in range(1,len(arg)):
                mapping_details = arg[values].split(":")
                resolution = mapping_details[0]
                width = mapping_details[1].split('|')[0].strip('[]')
                height = mapping_details[1].split('|')[1].strip('[]')
                Resolution_Details[resolution] = [int(width),int(height)]
            search_key = int(result)
            #Create a sub dictionary of width and height pair from the SupportingRes keys.
            subdict=dict([(x,Resolution_Details[x]) for x in SupportingRes])

            #Get matching width_height pair for given width from the SupportingRes.
            width_height_pair = [val for key, val in subdict.items() if search_key in val]
            #List of matching width/height list based on index
            sub_list = [item[index] for item in width_height_pair]
            if search_key in sub_list :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "displayinfo_validate_hdr_formats":
            status = checkNonEmptyResultData(result)
            if status == "TRUE":
                info["Result"] = result
                status = [ "FALSE" for form in result if form not in expectedValues ]
                if "FALSE" not in status:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "displayinfo_validate_expected_results":
            status = checkNonEmptyResultData(result)
            if status == "TRUE":
                info["Result"] = result
                expectedValues = [ value.lower() for value in expectedValues]
                if len(arg) and arg[0] == "check_colorimetry":
                    result = [ value.lower() for value in result]
                    colorimetry_status = [ "FALSE" for value in result if value not in expectedValues ]
                    if "FALSE" not in colorimetry_status:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                else:
                    if str(result).lower() in expectedValues:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "displayinfo_check_edid_result":
            info = checkAndGetAllResultInfo(result)
            EDID = result.get("data")
            if str(EDID) == str(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        # Parser Code for ActivityMonitor plugin
        elif tag == "activitymonitor_check_applications_memory":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            app_list=result.get("applicationMemory")
            status = []
            if len(app_list) > 0:
                for app_info in app_list:
                    status.append(checkNonEmptyResultData(app_info.values))
                if "FALSE" not in status:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "activitymonitor_validate_result":
            if len(arg) > 0:
                info = checkAndGetAllResultInfo(result.get(arg[0]),result.get("success"))
            else:
                info = checkAndGetAllResultInfo(result,result.get("success"))

        # Parser Code for HDMICEC plugin
        elif tag == "hdmicec_get_enabled_status":
            info["enabled"] = result.get("enabled")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("enabled")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "hdmicec_check_result":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "hdmicec_get_cec_addresses":
            cec_addresses = result.get("CECAddresses")
            if arg[0] == "get_logical_address":
                success = str(result.get("success")).lower() == "true"
                logical_address = cec_addresses.get("logicalAddresses")
                info["logicalAddress"] =  logical_address.get("logicalAddress")
                info["deviceType"] =  logical_address.get("deviceType")
                if len(logical_address) > 0:
                    logical_Address_value = logical_address.get("logicalAddress")
                    Device_Type_value = logical_address.get("deviceType")
                    if logical_Address_value  not in [15,255] and logical_Address_value == int(expectedValues[0]) and  Device_Type_value == expectedValues[1] and  success:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                else:
                    info["logicalAddresses"] = logical_address
                    info["Test_Step_Status"] = "FAILURE"

            elif arg[0] == "get_physical_address":
                 physical_address = cec_addresses.get("physicalAddress")
                 status = checkNonEmptyResultData(cec_addresses.get("physicalAddress"))
                 hex_codes = {"\x00":"0","\x01":"1","\x02":"2","\x03":"3","\x04":"4","\x05":"5","\x06":"6","\x07":"7","\x08":"8","\x09":"9","\x0a":"a","\x0b":"b","\x0c":"c","\x0d":"d","\x0e":"e","\x0f":"f"}
                 for code in hex_codes.keys():
                    physical_address = physical_address.replace(code,hex_codes.get(code))
                 info["physicalAddress"] = physical_address
                 if status == "TRUE" and str(result.get("success")).lower() == "true":
                    if expectedValues[0] == "true" and  physical_address != "ffff":
                            info["Test_Step_Status"] = "SUCCESS"

                    elif expectedValues[0] == "false" and  physical_address == "ffff":
                            info["Test_Step_Status"] = "SUCCESS"
                    else:
                            info["Test_Step_Status"] = "FAILURE"
                 else:
                    info["Test_Step_Status"] = "FAILURE"

        #Parser code for State Observer plugin
        elif tag == "StateObserver_validate_result":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "StateObserver_validate_version":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            version=result.get("version")
            if len(arg) and arg[0] == "check_version":
                if int(float(version)) > 0 and int(float(version)) == int(expectedValues[0]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if int(float(version)) > 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "StateObserver_validate_name":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            name=result.get("Name")
            if str(expectedValues[0]).lower() in str(name).lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "StateObserver_get_property_info":
            property_info = result.get("properties")
            status = []
            success = str(result.get("success")).lower() == "true"
            for property_data in property_info:
                status.append(checkNonEmptyResultData(property_data.values()))
            info["properties"] = property_info
            if success and "FALSE" not in status:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "stateobserver_check_registered_property_names":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            property_info = result.get("properties")
            success = str(result.get("success")).lower() == "true"
            status = "TRUE"
            for property_data in property_info:
                if property_data not in expectedValues:
                   status = "FALSE"
            info["properties"] = property_info
            if success and "FALSE" not in status:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # Display Settings Plugin Response result parser steps
        elif tag == "display_is_connected":
            info["video_display"] = result.get('connectedVideoDisplays')
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result.get('connectedVideoDisplays'))
            if success and status == "TRUE":
                info["is_connected"] = "true"
                info["Test_Step_Status"] = "SUCCESS"
            elif success and status == "FALSE":
                info["is_connected"] = "false"
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
            if len(arg) and arg[0] == "check_tv_connected":
                if "true" in info["is_connected"]:
                    info["Test_Step_Status"] = "FAILURE"
                    message = "Please test after disconnecting the TV"
                    info["Test_Step_Message"] = message
                else:
                    info["Test_Step_Status"] = "SUCCESS"
            elif len(arg) and arg[0] == "check_tv_not_connected":
                if "true" in info["is_connected"]:
                    info["Test_Step_Status"] = "FAILURE"
                    message = "Connected video displays list should be empty when TV is not connected"
                    info["Test_Step_Message"] = message
                else:
                    info["Test_Step_Status"] = "SUCCESS"

        elif tag == "display_settings_check_set_operation":
            info["success"] = result.get("success")
            if len(arg) and arg[0] == "check_set_failed":
                if str(result.get("success")).lower() == "false":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

            else:
                if str(result.get("success")).lower() == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "display_connected_status":
            info["video_display"] = result.get('connectedVideoDisplays')
            if json.dumps(result.get('success')) == "true" and  result.get('connectedVideoDisplays'):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_settop_supported_resolutions":
            info["supportedSettopResolutions"] = result.get('supportedSettopResolutions')
            if collections.Counter(result.get('supportedSettopResolutions')) == collections.Counter(expectedValues):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
      
        elif tag == "check_supported_tv_resolutions":
            info["supportedTvResolutions"] = result.get('supportedTvResolutions')
            if json.dumps(result.get("success")) == "true" and any(item not in result.get('supportedTvResolutions') for item in ["none"]) :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "display_supported_resolutions":
            info["supportedResolutions"] = result.get('supportedResolutions')
            if json.dumps(result.get("success")) == "true" :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_current_resolution":
            info["resolution"] = result.get('resolution')
            if json.dumps(result.get("success")) == "true" :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
            if len(arg) and arg[0] == "check_expected_resolution":
                if result.get('resolution') in expectedValues and json.dumps(result.get("success")) == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif len(arg) and arg[0] == "check_resolution_not_persisted":
                defaultResolution = str(expectedValues[0])
                info["defaultResolution"] = defaultResolution
                if defaultResolution == str(expectedValues[1]):
                    if str(result.get('resolution')) and json.dumps(result.get("success")) == "true":
                        info["Test_Step_Status"] = "SUCCESS"
                elif result.get('resolution') != str(expectedValues[1]) and json.dumps(result.get("success")) == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_supported_video_displays":
            info["supportedVideoDisplays"] = result.get('supportedVideoDisplays')
            if json.dumps(result.get('success')) == "true" and collections.Counter((result.get('supportedVideoDisplays'))) == collections.Counter(expectedValues):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_supported_audio_ports":
            info["audio_port"] = result.get('supportedAudioPorts')
            if collections.Counter(result.get('supportedAudioPorts')) == collections.Counter(expectedValues):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_settop_HDR_support":
            info["supportsHDR"] = result.get('supportsHDR')
            if json.dumps(result.get('supportsHDR')).upper()in json.dumps(expectedValues):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
    
        elif tag == "check_TV_HDR_support":
            info["TVsupportsHDR"] = result.get('supportsHDR')
            if json.dumps(result.get('supportsHDR')) == "true" and any(item not in result.get('standards') for item in ["none"]) :
                info["Test_Step_Status"] = "SUCCESS"
            elif json.dumps(result.get('supportsHDR')) == "false" and any(item in result.get('standards') for item in ["none"]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_host_edid":
            info["host_edid"] = result.get('EDID')
            if json.dumps(result.get('EDID')) and json.dumps(result.get("success")) == "true" :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_connected_device_edid":
            if len(arg) and arg[0] == "check_edid_status_for_disconnected_device":
                if str(result.get("success")).lower() == "false":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["connected_device_edid"] = result.get('EDID')
                if json.dumps(result.get('EDID')) and json.dumps(result.get("success")) == "true" :
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        
        elif tag == "check_connected_audio_ports":
            if len(arg) and arg[0] == "check_value":
                info["connected_audio_port"] = result.get('connectedAudioPorts')
                if json.dumps(result.get('success')) == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["connected_audio_port"] = result.get('connectedAudioPorts')
                if json.dumps(result.get('success')) == "true" and str(expectedValues[0]) in result.get('connectedAudioPorts'):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_supported_audio_modes":
            info["supported_audio_modes"] = result.get('supportedAudioModes');
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result.get('supportedAudioModes'))
            if "FALSE" not in status and success:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
            if len(arg) and arg[0] == "check_hdmi0_audio_modes":
                status = "TRUE"
                expectedValues = [ str(mode).lower() for mode in expectedValues ]
                for soundMode in  result.get('supportedAudioModes'):
                    if "AUTO" in soundMode:
                        soundMode = re.search(r"\((.*?)\)",soundMode).group(1)
                    if str(soundMode).lower() not in expectedValues:
                        status = "FALSE"
                        break
                if "FALSE" not in status:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        
        elif tag == "check_sound_mode":
            soundMode = result.get('soundMode')
            if "AUTO" in soundMode:
                message = "Best sound mode of the device %s" %(soundMode)
                info["Test_Step_Message"] = message
                soundMode = re.search(r"\((.*?)\)",soundMode).group(1)
            info["soundMode"] = str(soundMode).lower()
            if len(arg) and arg[0] == "check_expected_sound_mode":
                expectedMode = str(expectedValues[0]).lower()
                if result.get('soundMode').lower() == expectedMode or expectedMode in result.get('soundMode').lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and result.get('soundMode') in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE" 

        elif tag == "check_zoom_settings":
            info["zoomSetting"] = result.get('zoomSetting');
            if str(result.get("success")).lower() == "true" and result.get('zoomSetting') in expectedValues :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_current_output_settings":
            info["colorSpace"] = result.get('colorSpace')
            info["colorDepth"] = result.get('colorDepth')
            info["matrixCoefficients"] = result.get('matrixCoefficients')
            info["videoEOTF"] = result.get('videoEOTF')
            if str(result.get("success")).lower() == "true" and result.get('colorSpace') in [0,1,2,3,4,5] and result.get('matrixCoefficients') in [0,1,2,3,4,5,6,7] :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"    
    
        elif tag == "check_active_input":
            info ["activeInput"] = result.get('activeInput')
            info ["success"] = result.get('success')
            if len(arg) and arg[0] == "check_for_invalid_port":
                if str(result.get("success")).lower() == "false" and str(result.get('activeInput')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and str(result.get('activeInput')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_MS12_audio_compression":
            info["compresionLevel"] = result.get('compressionlevel');
            if str(result.get("success")).lower() == "true" and str(result.get('compressionlevel')) in expectedValues :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_video_port_status_standby":
            if len(arg) and arg[0] == "check_for_invalid_port":
                info = checkAndGetAllResultInfo(result)
                if str(result.get("success")).lower() == "false" and result.get('error_message') in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["enabled"] = result.get('videoPortStatusInStandby');
                if str(result.get("success")).lower() == "true" and str(result.get('videoPortStatusInStandby')) in expectedValues :
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_dolby_volume_mode":
            info["dolbyVolumeMode"] = result.get('dolbyVolumeMode');
            if str(result.get("success")).lower() == "true" and str(result.get('dolbyVolumeMode')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_dialog_enhancement":
            info["enhancerlevel"] = result.get('enhancerlevel');
            if str(result.get("success")).lower() == "true" and str(result.get('enhancerlevel')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_intelligent_equalizer_mode":
            info["intelligentEqualizerMode"] = result.get('mode');
            if str(result.get("success")).lower() == "true" and str(result.get('mode')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_volume_leveller":
            info["level"] = result.get('level');
            if len(arg) and arg[0] == "check_volume_leveller_mode":
                info["mode"] = result.get('mode');
                print expectedValues
                if str(result.get("success")).lower() == "true" and str(result.get('mode')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and str(result.get('level')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_bass_enhancer":
            info["bassBoost"] = result.get('bassBoost');
            if len(arg) and arg[0] == "check_bass_range":
                if 0 <= int(result.get('bassBoost')) <= 100 :
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and str(result.get('bassBoost')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_surround_virtualizer":
            info["boost"] = result.get('boost');
            if len(arg) and arg[0] == "check_surround_virtualizer_range":
                if 0 <= int(result.get('boost')) <= 96 :
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif len(arg) and arg[0] == "check_surround_virtualizer_mode":
                info["mode"] = result.get('mode')
                print  expectedValues
                if str(result.get("success")).lower() == "true" and str(result.get('mode')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and str(result.get('boost')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_mi_steering":
            info["MISteeringEnable"] = result.get('MISteeringEnable');
            if str(result.get("success")).lower() == "true" and str(result.get('MISteeringEnable')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_surround_decoder":
            info["surroundDecoderEnable"] = result.get('surroundDecoderEnable');
            if str(result.get("success")).lower() == "true" and str(result.get('surroundDecoderEnable')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_drc_mode":
            if result.get('DRCMode').lower() == "line":
                DRCMode = 0
                message = "DRCMode => line-0"
            elif result.get('DRCMode').lower() == "rf":
                DRCMode = 1
                message = "DRCMode => RF-1"
            info["DRCMode"] = DRCMode
            info["Test_Step_Message"] = message
            if len(arg) and arg[0] == "validate_drc_mode":
                if str(result.get("success")).lower() == "true" and DRCMode == int(expectedValues[0]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and str(result.get('DRCMode')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_volume_level":
            info["volumeLevel"] = result.get('volumeLevel');
            if len(arg) and arg[0] == "check_volume_level_range":
                if 0 <= int(float(result.get('volumeLevel'))) <= 100 :
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and str(int(float(result.get('volumeLevel')))) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_gain":
            info["gain"] = result.get('gain');
            if len(arg) and arg[0] == "check_gain_range":
                if 0 <= float(result.get('gain')) <= 100 :
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if int(expectedValues[0])== 0 and int(float(result.get('gain')))== 2 and str(result.get("success")).lower() == "true":
                    info["Test_Step_Status"] = "SUCCESS"

                elif str(result.get("success")).lower() == "true" and str(int(float(result.get('gain')))) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_muted":
            info["muted"] = result.get('muted');
            if str(result.get("success")).lower() == "true" and str(result.get('muted')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_audio_delay":
            info["audioDelay"] = result.get('audioDelay');
            if len(arg) and arg[0] == "check_audio_delay_range":
                if 0 <= int(result.get('audioDelay')):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and str(result.get('audioDelay')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_audio_delay_offset":
            info["audioDelayOffset"] = result.get('audioDelayOffset');
            if len(arg) and arg[0] == "check_audio_delay_offset_range":
                if 0 <= int(result.get('audioDelayOffset')):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and str(result.get('audioDelayOffset')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_sink_atmos_capability":
            info["atmos_capability"] = result.get('atmos_capability');
            if str(result.get("success")).lower() == "true" and str(result.get('atmos_capability')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_tv_hdr_capabilities":
            info["capabilities"] = result.get('capabilities')
            if str(result.get("success")).lower() == "true" and int(result.get('capabilities')) >= 0:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_device_repeater":
            info["HdcpRepeater"] = result.get('HdcpRepeater')
            if str(result.get("success")).lower() == "true" and str(result.get('HdcpRepeater')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_default_resolution" :
            info["defaultResolution"] = result.get('defaultResolution')
            if str(result.get("success")).lower() == "true" and str(result.get('defaultResolution')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_supported_MS12_Audio_Profiles":
            info["supportedMS12AudioProfiles"] = result.get('supportedMS12AudioProfiles')
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result.get('supportedMS12AudioProfiles'))
            if success and status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_audio_profile":
            info["ms12AudioProfile"] = result.get('ms12AudioProfile')
            if str(result.get("success")).lower() == "true" and str(result.get('ms12AudioProfile')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "check_audio_port_status":
            info["enable"] = result.get('enable')
            if str(result.get("success")).lower() == "true" and str(result.get('enable')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_graphic_equalizer_mode":
            info["graphicEqualizerMode"] = result.get('mode')
            if str(result.get("success")).lower() == "true" and str(result.get('mode')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_settop_supported_audio_capabilities":
            info["audioCapabilities"] = result.get('AudioCapabilities')
            status = checkNonEmptyResultData(result)
            audioCapabilities = [value.lower() for value in result.get('AudioCapabilities')]
            audioCapabilities_status = [ "FALSE" for value in expectedValues if value.lower() not in audioCapabilities ]
            if status == "TRUE" and "FALSE" not in  audioCapabilities_status:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_settop_supported_ms12_capabilities":
            info["ms12Capabilities"] = result.get('MS12Capabilities')
            status = checkNonEmptyResultData(result)
            ms12Capabilities = [value.lower() for value in result.get('MS12Capabilities')]
            ms12Capabilities_status = [ "FALSE" for value in expectedValues if value.lower() not in ms12Capabilities ]
            if status == "TRUE" and "FALSE" not in  ms12Capabilities_status:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "validate_supported_resolutions":
            supportedResolutions = result.get('supportedResolutions')
            info["supportedResolutions"] = supportedResolutions
            status = all(item in expectedValues for item in supportedResolutions)
            if status is True:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_audio_video_formats":
            if len(arg) and arg[0] == "get_video_format":
                info["supportedVideoFormat"] = supportedFormats = result.get("supportedVideoFormat")
                info["currentVideoFormat"] = currentFormat = result.get("currentVideoFormat")
            elif len(arg) and arg[0] == "get_audio_format":
                info["supportedAudioFormat"] = supportedFormats = result.get("supportedAudioFormat")
                info["currentAudioFormat"] = currentFormat = result.get("currentAudioFormat")
            status = checkNonEmptyResultData(result)
            if status == "TRUE" and currentFormat in supportedFormats:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # Wifi Plugin Response result parser steps
        elif tag == "wifi_check_adapter_state":
            info = result.copy()
            state = int(result.get("state"))
            state_names = ["UNINSTALLED","DISABLED","DISCONNECTED","PAIRING","CONNECTING","CONNECTED","FAILED"]
            success = str(result.get("success")).lower() == "true"
            info["state_name"] = state_names[state]
            info["enable"] = "True" if state not in [0,6,1] else "False"
            if str(result.get("state")) in expectedValues:
                info["Test_Step_Status"] = "FAILURE"
                if arg[0] == "check_state_valid" and state not in [0,6]:
                    info["Test_Step_Status"] = "SUCCESS"
                elif arg[0] == "check_state_enabled" and state not in [0,6,1]:
                    info["Test_Step_Status"] = "SUCCESS"
                elif arg[0] == "check_connection_status" and state == 5:
                    info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "wifi_check_set_operation":
            if str(result.get("success")).lower() == expectedValues[0]:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "wifi_check_save_clear_ssid":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if int(result.get("result")) == int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "wifi_check_signal_threshold_change_status":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if str(result.get("success")).lower() == "true" and str(result.get("result")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "wifi_get_connected_ssid":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if arg[0] == "check_ssid":
                if str(result.get("success")).lower() == "true" and str(result.get("ssid")) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif arg[0] == "check_no_ssid":
                if str(result.get("success")).lower() == "true" and str(result.get("ssid"))=="":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "wifi_check_ssid_pairing":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if int(result.get("result")) == int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "wifi_get_paired_ssid":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if str(result.get("success")).lower() == "true" and str(result.get("ssid")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "wifi_check_supported_security_modes":
            info["supported_security_modes"] = result.get("security_modes")
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result)
            if "FALSE" not in status and success:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # Bluetooth Plugin Response result parser steps
        elif tag == "bluetooth_set_operation":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "bluetooth_get_discoverable_status":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if str(result.get("discoverable")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "bluetooth_get_name":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if len(arg) and arg[0] == "check_name":
                if result.get("name") in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "bluetooth_get_device_info":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            success = str(result.get("success")).lower() == "true"
            deviceInfo = result.get("deviceInfo")
            info["deviceInfo"] = deviceInfo
            status = checkNonEmptyResultData(deviceInfo)
            if "FALSE" not in status and success:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "bluetooth_get_discovered_devices":
            discoveredDevices = result.get("discoveredDevices")
            status = []
            devices = []
            success = str(result.get("success")).lower() == "true"
            if len(arg) and arg[0] == "get_devices_info":
                for device_info in discoveredDevices:
                    status.append(checkNonEmptyResultData(device_info))
                    device_data = {}
                    device_data["deviceID"] = str(device_info.get("deviceID"))
                    device_data["name"] = str(device_info.get("name"))
                    device_data["deviceType"] = str(device_info.get("deviceType"))
                    devices.append(device_data)
                info["devices"] = devices
            elif len(arg) and arg[0] == "get_device_id":
                checkStatus = "FALSE"
                for device_info in discoveredDevices:
                    if str(device_info.get("name")) in expectedValues[0]:
                        info["deviceID"] = str(device_info.get("deviceID"))
                        checkStatus = "TRUE"
                        break
                status.append(checkStatus)
            elif len(arg) and arg[0] == "check_device_not_discovered":
                checkStatus = "TRUE"
                for device_info in discoveredDevices:
                    if str(device_info.get("name")) in expectedValues[0]:
                        checkStatus = "FALSE"
                        break
                status.append(checkStatus)
            if "FALSE" not in status and success:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "bluetooth_get_paired_devices":
            if arg[0] == "check_device_paired":
                info = checkAndGetAllResultInfo(result,result.get("success"))
                status = False
                pairedDevices = result.get("pairedDevices")
                success = str(result.get("success")).lower() == "true"
                for pairedDevice in pairedDevices:
                    if str(pairedDevice.get("name")) in expectedValues[0]:
                        status = True
                        info = pairedDevice
                if success and status:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif arg[0] == "check_paired_device_list_empty":
                if len(result.get("pairedDevices")) == 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"


        elif tag == "bluetooth_get_connected_devices":
            if arg[0] == "check_device_connected":
                info = checkAndGetAllResultInfo(result,result.get("success"))
                status = False
                connectedDevices = result.get("connectedDevices")
                success = str(result.get("success")).lower() == "true"
                for connectedDevice in connectedDevices:
                    if str(connectedDevice.get("name")) in expectedValues[0]:
                        status = True
                        info = connectedDevice
                if success and status:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif arg[0] == "check_connected_device_list_empty":
                if len(result.get("connectedDevices")) == 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_api_version_number":
            info = result
            success = str(result.get("success")).lower() == "true"
            if success and result.get("version") == int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # FirmwareCotrol Plugin Response result parser steps
        elif tag == "fwc_get_status":
            expectedStatuses = ["none", "upgradestarted", "downloadstarted", "downloadaborted", "downloadcompleted", "installinitiated", "installnotstarted", "installaborted", "installstarted", "upgradecompleted", "upgradecancelled"]
            info["status"] = result
            if result in expectedStatuses:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "fwc_get_download_size":
            info["downloadsize"] = int(result)
            if info["downloadsize"] > 200000000:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # FrameRate Plugin Response result parser steps
        elif tag == "framerate_check_set_operation":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        
        elif tag == "framerate_check_auto_framerate_mode":
            success = str(result.get("success")).lower() == "true"
            info["frmmode"] = result.get("auto-frm-mode")
            if success and str(result.get("auto-frm-mode")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "framerate_check_display_framerate":
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result.get("framerate"))
            info["framerate"] = result.get("framerate")
            if success and status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
            if len(arg) and  arg[0] == "check_framerate_values":
                if success and str(result.get("framerate")) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"


        # Warehouse Plugin Response result parser steps
        
        elif tag == "warehouse_get_device_info":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "warehouse_set_operation":
            info = result.copy()
            if len(arg) and arg[0] == "invalid":
                if str(result.get("success")).lower() == "false":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "warehouse_check_isclean":
            info = result.copy()
            isclean = str(result.get("clean")).lower()
            success = str(result.get("success")).lower() == "true"
            if success and len(result.get("files")) > 0 and isclean == "false":
                info["Test_Step_Status"] = "SUCCESS"
            elif success and ( len(result.get("files")) == 0 or result.get("files") is None ) and isclean == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "warehouse_validate_reset":
            info["success"] = result.get("success")
            success = str(result.get("success")).lower() == "true"
            if "error" in result and len(result.get("error")) > 0:
                info["error"] = result.get("error")
                info["Test_Step_Status"] = "FAILURE"
            else:
                if success:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        # LoggingPreferences Plugin Response result parser steps
        elif tag == "loggingpreferences_check_keystroke_mask_state":
            info["keystrokeMaskEnabled"] = result.get("keystrokeMaskEnabled")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("keystrokeMaskEnabled")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "loggingpreferences_check_set_operation":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        # DataCapture Plugin Response result parser steps
        elif tag == "datacapture_enable_audio_capture":
            info =  checkAndGetAllResultInfo (result,result.get("success"))

        elif tag == "datacapture_get_audio_clip":
            info = checkAndGetAllResultInfo (result,result.get("success"))

        # Timer Plugin Response result parser steps
        elif tag == "timer_check_results":
            info = checkAndGetAllResultInfo (result,result.get("success"))

        elif tag == "timer_check_timer_status":
            info["state"] = result.get("state")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("state")) in expectedValues:
                 info["Test_Step_Status"] = "SUCCESS"
            else:
                 info["Test_Step_Status"] = "FAILURE"



        # Messenger Plugin Response result parser steps
        elif tag == "messenger_join_room":
            info["roomid"] = result.get("roomid")
            if not str(result.get("roomid")):
                info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "SUCCESS"

        elif tag == "Messenger_check_leave_response":
            if result== None:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # Monitor Plugin Response result parser steps
        elif tag == "monitor_get_result_data":
            if arg[0] == "get_status":
                measurements =  result[0].get("measurements")
                info["observable"] = result[0].get("observable")
                info["restart_limit"] = result[0].get("restart").get("limit")
                info["restart_window"] = result[0].get("restart").get("window")
            elif arg[0] == "get_reset_statistics":
                measurements =  result.get("measurements")
                info["observable"] = result.get("observable")
                info["restart_limit"] = result.get("restart").get("limit")
                info["restart_window"] = result.get("restart").get("window")
            status = []
            measurement_detail = []
            for key in measurements:
                detail_Values=[]
                detail_Values.append(measurements.get(key))
                status.append(checkNonEmptyResultData(detail_Values))
                measurement_detail.append(str(key)+": "+str(measurements.get(key)))
            info["measurements"] =  measurement_detail
            if "FALSE" not in status:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        # ScreenCapture Plugin Response result parser steps
        elif tag == "screencapture_upload_screen":
            if str(result.get("success")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        
        #AVInput Plugin Response result parser
        elif tag == "avinput_check_inputs":
            info["numberOfInputs"] = result.get("numberOfInputs")
            success = str(result.get("success")).lower() == "true"
            if success and int(result.get("numberOfInputs")) == int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "avinput_get_currentvideomode":
            info["currentVideoMode"] = result.get("currentVideoMode")
            currentVideoMode =  result.get("currentVideoMode")
            status = checkNonEmptyResultData(currentVideoMode)
            VideoMode = re.split('(p|i)',currentVideoMode)
            if status == "TRUE":
                Resolution = VideoMode[0]
                Framerate = VideoMode[2]
                if Resolution == "unknown" and  len(Framerate) == 0 or Resolution in ["480", "576", "720", "1080", "3840x2160", "4096x2160"] and Framerate in ["24", "25", "30", "60", "23.98", "29.97", "50", "59.94"]:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "avinput_is_contentprotected":
            info["isContentProtected"] = result.get("isContentProtected")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("isContentProtected")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # HdmiInput Response result parser steps
        elif tag == "get_hdmiinput_devices":
            success = str(result.get("success")).lower() == "true"
            devices = result.get("devices")
            status = []
            device_details = []
            if len(arg) and arg[0] == "get_data":
                for device_info in devices:
                    status.append(checkNonEmptyResultData(device_info))
                    device_data = {}
                    device_data["id"] = int(device_info.get("id"))
                    device_data["locator"] = str(device_info.get("locator"))
                    device_details.append(device_data)
                info["devices"] = device_details
            else:
                port_id_list = []
                for device_info in devices:
                    status.append(checkNonEmptyResultData(device_info))
                    port_id_list.append(str(device_info.get("id")))
                info["portIds"] = port_id_list
            if "FALSE" not in status and success:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "hdmiinput_check_set_operation":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "hdmiinput_read_edid_value":
            info["name"]  = str(result.get("name"))
            if str(result.get("success")).lower() == "true" and info["name"] in expectedValues[0]:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # PlayerInfo Plugin Response result parser steps
        elif tag == "playerinfo_check_audio_video_codecs":
            info["RESULT"] = result
            status = checkNonEmptyResultData(result)
            codec_status = [ "FALSE" for codec in expectedValues if codec  not in result ]
            if status == "TRUE" and "FALSE" not in codec_status:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "playerinfo_validate_boolean_result":
            info["RESULT"] = result
            if str(result).lower() == "true" or str(result).lower() == "false" :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "playerinfo_check_results":
            info["RESULT"] = result
            if result in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "playerinfo_check_resolution":
            info["resolution"]= result
            fps_data = ""
            resolution = result.replace("Resolution","")
            fps_data = re.split('(p|i)',str(expectedValues[0]))[2]
            if fps_data == "60":
                expectedValues = str(expectedValues[0])[0:-2]
            if str(resolution).lower() in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
     
        # PersistentStore Plugin Response result parser steps
        elif tag == "persistentstore_check_set_operation":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "persistentstore_check_value":
            info["value"] = result.get("value")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("value")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "persistentstore_get_keys":
            keys = result.get("keys")
            info["Keys"] = keys
            if arg[0] == "check_not_exists":
                if expectedValues[0] not in keys:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif arg[0] == "check_if_exists":
                if expectedValues[0] in keys:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        elif tag == "persistentstore_get_namespaces":
            Namespaces = result.get("namespaces")
            info["Namespaces"] = Namespaces
            if arg[0] == "check_not_exists":
                if expectedValues[0] not in Namespaces:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif arg[0] == "check_if_exists":
                if expectedValues[0] in Namespaces:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        elif tag == "persistentstore_get_storage_size":
            status = checkNonEmptyResultData(result)
            if "FALSE" not in status:
                storage_size = []
                for key,value in result.get("namespaceSizes").iteritems():
                    storage_size.append(str(key)+": "+str(value))
                    info["storage_size"] =  storage_size
                    info["Test_Step_Status"] = "SUCCESS"
            else:
                info["storage_size"] = result
                info["Test_Step_Status"] = "FAILURE"

        # TextToSpeech Plugin Response result parser steps
        elif tag == "texttospeech_get_enabled_status":
            info["enabletts"] = result.get("isenabled")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("isenabled")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "texttospeech_check_result":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "texttospeech_check_api_version":
            info["version"] = result.get("version")
            success = str(result.get("success")).lower() == "true"
            if success and result.get("version") == int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # XCast Plugin Response result parser steps
        elif tag == "xcast_get_enabled_status":
            info["enabled"] = result.get("enabled")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("enabled")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "xcast_check_result":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "xcast_check_api_version":
            info["version"] = result.get("version")
            success = str(result.get("success")).lower() == "true"
            if success and result.get("version") == int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "xcast_check_set_operation":
            info["success"] = result.get("success")
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "xcast_check_friendly_name":
            info["friendlyname"] = result.get("friendlyname")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("friendlyname")).lower() in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "xcast_check_standby_behavior":
            info["standbybehavior"] = result.get("standbybehavior")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("standbybehavior")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # Controller Plugin Response result parser steps
        elif tag == "controller_get_plugin_state":
            if arg[0] == "check_status":
                state = ""
                callsign = ""
                for plugin in result:
                    if plugin.get("callsign") == arg[1]:
                        state = plugin.get("state")
                        callsign = plugin.get("callsign")
                        break
                info["state"] = state
                info["callsign"] = callsign

                if info["state"] in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "controller_check_discovery_result":
            info = checkAndGetAllResultInfo (result[0])

        elif tag == "controller_check_environment_variable_value":
            status = checkNonEmptyResultData(result)
            info["RESULT"] = result
            if status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "controller_get_configuration_url":
            info["url"] = result.get("url")
            status = compareURLs(str(result.get("url")),expectedValues[0])
            if status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "controller_check_processinfo":
            info = checkAndGetAllResultInfo (result)

        elif tag == "controller_check_active_connection":
            info = result[0]
            status = checkNonEmptyResultData(result[0])
            if status == "TRUE" and str(result[0].get("state")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "controller_check_subsystems_status":
            info = result[0]
            status = checkNonEmptyResultData(result[0])
            if status == "TRUE" and str(result[0].get("subsystem")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag =="controller_check_error_message":
            info = otherInfo.get("error")
            error = otherInfo.get("error")
            message = error.get("message")
            code = error.get("code")
            if message.lower() == str(expectedValues[0]).lower() and int(code) == int(expectedValues[1]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "controller_check_default_plugin_state":
            if arg[0] == "check_default_state":
                state = ""
                callsign = ""
                for plugin in result:
                    if plugin.get("callsign") == arg[1]:
                        state = plugin.get("state")
                        callsign = plugin.get("callsign")
                        autostart = plugin.get("autostart")
                        break
                info["state"] = state
                info["callsign"] = callsign
                info["autostart"] = autostart
                if autostart == True:
                    expectedState = "activated,activation"
                    if state in expectedState:
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



#-----------------------------------------------------------------------------------------------
# CheckAndGenerateConditionalExecStatus
#-----------------------------------------------------------------------------------------------
# Syntax      : CheckAndGenerateConditionalExecStatus(testStepResults,methodTag,arguments)
# Description : Method to parse the previous test step result to check whether required
#               condition is satisfied to execute the current test step
# Parameter   : testStepResults - list of previous test step results
#             : methodTag - tag used to identify the parser step
#             : arguments - list of arguments used for parsing
# Return Value: Function execution status & Condition status (TRUE/FALSE)
#-----------------------------------------------------------------------------------------------
def CheckAndGenerateConditionalExecStatus(testStepResults,methodTag,arguments):
    tag  = methodTag
    arg  = arguments

    # Input Variables:
    # a. testStepResults - list of dictionaries
    #    Eg [ {1: [{"brightness":100}]} ] // 1-testCaseId
    # b. methodTag - string
    # c. arguments - list

    # Output variables:
    # a.status - (SUCCESS/FAILURE)
    #   1.It means the status of the parsing action
    #   By default is SUCCESS, if any exception occurs
    #   while parsing then status will be FAILURE
    # b.result - (TRUE/FALSE)
    #   1.It is the actual variable which indicates
    #   whether required condition is met or not

    # User can also use testStepId to refer the result
    # data present in testStepResults

    # DO NOT OVERRIDE THE RETURN VARIABLES "RESULT" &
    # "STATUS" WITHIN PARSER STEPS TO STORE SOME OTHER
    # DATA. USER CAN ONLY UPDATE "RESULT" WITH (TRUE/FALSE)
    result = ""
    status = "SUCCESS"

    # USER CAN ADD N NUMBER OF PREVIOUS RESULT PARSER
    # STES BELOW
    try:

        # Controller Plugin Response result parser steps
        if tag == "controller_get_plugin_state":
            state = ""
            testStepResults = testStepResults[0].values()[0]
            for result in testStepResults:
                if result.get("callsign") == arg[1]:
                    state = result.get("state")
                    break;
            if arg[0] == "isDeactivated":
                if state == "deactivated":
                    result = "TRUE"
                elif state == "activated":
                    result = "FALSE"
                elif state == "resumed":
                    result = "FALSE"
                else:
                    result = "TRUE"
            elif arg[0] == "isActivated":
                if state == "activated":
                    result = "TRUE"
                elif state == "resumed":
                    result = "TRUE"
                elif state == "deactivated":
                    result = "FALSE"
                else:
                    result = "FALSE"

        # TraceControl Plugin Response result parser steps
        elif tag == "tracecontrol_get_state":
            testStepResults = testStepResults[0].values()[0]
            state = testStepResults[0].get("state")
            if arg[0] == "isDisabled":
                if state == "disabled":
                    result = "TRUE"
                else:
                    result = "FALSE"
            if arg[0] == "isEnabled":
                if state == "enabled":
                    result = "TRUE"
                else:
                    result = "FALSE"


        # Front Panel Plugin Response result parser steps
        elif tag == "frontpanel_check_led_brightness":
            testStepResults = testStepResults[0].values()[0]
            brightness = testStepResults[0].get("brightness")
            if arg[0] == "isBrigtnessZero":
                if str(brightness) == "0":
                    result = "TRUE"
                else:
                    result = "FALSE"


        # WebKitBrowser Plugin Response result parser steps
        elif tag == "webkitbrowser_check_state":
            testStepResults = testStepResults[0].values()[0]
            state = testStepResults[0].get("state")
            if arg[0] == "isSuspended":
                if state == "suspended":
                    result = "TRUE"
                else:
                    result = "FALSE"



        # Cobalt Plugin Response result parser steps
        elif tag == "cobalt_check_state":
            testStepResults = testStepResults[0].values()[0]
            state = testStepResults[0].get("state")
            if arg[0] == "isSuspended":
                if state == "suspended":
                    result = "TRUE"
                else:
                    result = "FALSE"

        # Wifi Plugin Response result parser steps
        elif tag == "wifi_check_adapter_state":
            testStepResults = testStepResults[0].values()[0]
            state = str(testStepResults[0].get("state"))
            if arg[0] == "isDisabled":
                if state == "1":
                    result = "TRUE"
                else:
                    result = "FALSE"

        # RDKShell Plugin Response result parser steps
        elif tag == "rdkshell_check_app_launch_type1":
            Type_one = ["Cobalt"]
            if arg[0] in Type_one:
                result = "TRUE"
            else:
                result = "FALSE"
        elif tag == "rdkshell_check_app_launch_type2":
            Type_two = ["WebKitBrowser"]
            if arg[0] in Type_two:
                result = "TRUE"
            else:
                result = "FALSE"
        elif tag == "rdkshell_check_application_state":
            testStepResults = testStepResults[0].values()[0]
            clients = testStepResults[0].get("clients")
            if arg[0] not in clients:
                result = "TRUE"
            else:
                result = "FALSE"

        # System Plugin Response result parser steps
        elif tag == "system_check_preferred_standby_mode":
            testStepResults = testStepResults[0].values()[0]
            mode = testStepResults[0].get("preferredStandbyMode")
            if arg[0] == "isNotEqual":
                if mode != arg[1]:
                    result = "TRUE"
                else:
                    result = "FALSE"

        elif tag == "system_check_disk_partition":
            testStepResults = testStepResults[0].values()[0]
            partition_count = testStepResults[0].get("partition_count")
            if int(partition_count) < int(arg[0]):
                result = "TRUE"
            else:
                result = "FALSE"

        else:
            print "\nError Occurred: [%s] No Parser steps available for %s" %(inspect.stack()[0][3],methodTag)
            status = "FAILURE"

    except Exception as e:
        status = "FAILURE"
        print "\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e)
        print "Result: %s" %(result)

    return status,result



#-----------------------------------------------------------------------------------------------
# parsePreviousTestStepResult
#-----------------------------------------------------------------------------------------------
# Syntax      : parsePreviousTestStepResult(testStepResults,methodTag,arguments)
# Description : Method to parse the previous test step results to get the certain
#               required key-value pair(s) based on user's need
# Parameter   : testStepResults - list of previous test step results
#             : methodTag - tag used to identify the parser step
#             : arguments - list of arguments used for parsing
# Return Value: Function execution status & Result Info Dictionary
#-----------------------------------------------------------------------------------------------
def parsePreviousTestStepResult(testStepResults,methodTag,arguments):
    tag  = methodTag
    arg  = arguments

    # Input Variables:
    # a. testStepResults - list of dictionaries
    #    Eg [ {1: [{"brightness":100}]} ] // 1-testCaseId
    # b. methodTag - string
    # c. arguments - list

    # Output variables:
    # a.status - (SUCCESS/FAILURE)
    #   1.It means the status of the parsing action
    #   By default is SUCCESS, it any exception occurs
    #   while parsing then status will be FAILURE
    # b.Info - dictionary
    #   1.It should be updated with the required
    #   key-value pair(s) based on user's need

    # User can also use testStepId to refer the result
    # data present in testStepResults

    # DO NOT OVERRIDE THE RETURN VARIABLES "INFO" &
    # "STATUS" WITHIN PARSER STEPS TO STORE SOME OTHER
    # DATA. USER CAN ONLY UPDATE "INFO" WITH REQUIRED
    # RESULT DETAILS

    info = {}
    status = "SUCCESS"

    # USER CAN ADD N NUMBER OF PREVIOUS RESULT PARSER
    # STES BELOW
    try:
        # TraceControl Plugin Response result parser steps
        if tag == "tracecontrol_toggle_state":
            state = ""
            testStepResults = testStepResults[0].values()[0]
            if len(arg) != 0:
                for result in testStepResults:
                    if arg[0] == result.get("category"):
                        state = result.get("state")
                        break;
            else:
                state = testStepResults[0].get("state")

            if state == "enabled":
                info["state"] = "disabled"
            elif state == "disabled":
                info["state"] = "enabled"

        elif tag == "tracecontrol_get_category":
            testStepResults = testStepResults[0].values()[0]
            info["category"] = testStepResults[0].get("category")


        # OCDM Plugin Response result parser steps
        elif tag == "ocdm_get_all_drms":
            testStepResults = testStepResults[0].values()[0]
            drm_info = testStepResults[0].get("drm_info")
            drms = []
            for drm in drm_info:
                drms.append(drm.get("name"))
            info["drm"] = ",".join(drms)

        elif tag == "ocdm_get_drm_key":
            testStepResults = testStepResults[0].values()[0]
            drm_info = testStepResults[0].get("drm_info")
            drm_key = ""
            for drm in drm_info:
                if arg[0] == drm.get("name"):
                    drm_key = ",".join(drm.get("keysystems"))
                    break;
            info["drm_key"] = drm_key


        # Network Plugin Response result parser steps
        elif tag == "network_get_interface_names":
            testStepResults = testStepResults[0].values()[0]
            interface_names = testStepResults[0].get("interface_names")
            interface_names = [ name for name in interface_names if name.strip() ]
            info["interface_names"] = ",".join(interface_names)

        elif tag == "network_get_endpoint_name":
            testStepResults = testStepResults[0].values()[0]
            endpoints = testStepResults[0].get("endpoints")
            if len(endpoints):
                info["endpointName"] = endpoints[0]
            else:
                info["endpointName"] = ""

        elif tag == "network_get_default_interface_name":
            testStepResults = testStepResults[0].values()[0]
            info["interface"] =  testStepResults[0].get("default_interface")

        elif tag == "network_toggle_interface_status":
            testStepResults = testStepResults[0].values()[0]
            status = testStepResults[0].get("enabled")
            if str(status).lower() == "true":
                info["enabled"] = False
            else:
                info["enabled"] = True

        elif tag == "network_get_stb_ip":
            testStepResults = testStepResults[0].values()[0]
            info["Device_IP"] = testStepResults[0].get("ip")


        # Front Panel Plugin Response result parser steps
        elif tag == "frontpanel_get_brightness_levels":
            testStepResults = testStepResults[0].values()[0]
            range_type = testStepResults[0].get("range")
            step_value = str(testStepResults[0].get("step"))
            min_value  = str(testStepResults[0].get("min"))
            max_value  = str(testStepResults[0].get("max"))
            if len(arg) and arg[0] == "get_min_max":
                info["brightness"] = min_value + "," + max_value
            elif len(arg) and arg[0] == "get_max":
                info["brightness"] = max_value
            else:
                if range_type == "boolean":
                    info["brightness"] = min_value + "," + max_value
                else:
                    if step_value == "10":
                        mid_value = "50"
                    elif step_value == "20":
                        mid_value = "60"
                    else:
                        mid_value = step_value
                    info["brightness"] = min_value + "," + mid_value + "," + max_value

        elif tag == "frontpanel_get_clock_brightness":
            testStepResults = testStepResults[0].values()[0]
            brightness = testStepResults[0].get("brightness")
            if str(brightness) == "100":
                info["brightness"] = "50"
            else:
                info["brightness"] = "100"

        elif tag == "frontpanel_toggle_clock_mode":
            testStepResults = testStepResults[0].values()[0]
            hr24clock_mode = testStepResults[0].get("is24Hour")
            if str(hr24clock_mode).lower() == "false":
                info["is24Hour"] = True
            else:
                info["is24Hour"] = False

        elif tag == "frontpanel_set_led_info":
            testStepResults = testStepResults[0].values()[0]
            info["preferences"] = json.dumps(testStepResults[0].get("supported_leds_info")[0])

        # FrameRate Plugin Response result parser steps
        elif tag == "framerate_set_display_framerate":
            FramerateList = []
            testStepResults = testStepResults[0].values()[0]
            test_list = testStepResults[0].get("DisplayFrameRate")
            for value in test_list:
                if value not in FramerateList:
                    FramerateList.append(value)
            info["framerate"] = FramerateList

        # WebkitBrowser Plugin Response result parser steps
        elif tag == "webkitbrowser_toggle_visibility":
            testStepResults = testStepResults[0].values()[0]
            visibility = testStepResults[0].get("visibility")
            if visibility == "visible":
                info["visibility"] = "hidden"
            else:
                info["visibility"] = "visible"

        elif tag == "webkitbrowser_toggle_local_storage_availability":
            testStepResults = testStepResults[0].values()[0]
            enabled = testStepResults[0].get("enabled")
            if str(enabled).lower() == "false":
                info["enabled"] = True
            else:
                info["enabled"] = False

        elif tag == "webkitbrowser_change_cookie_policy":
            testStepResults = testStepResults[0].values()[0]
            cookie_accept_policy = testStepResults[0].get("cookie_accept_policy")
            if cookie_accept_policy  == "always":
                info["cookie_accept_policy"] = "never"
            else:
                info["cookie_accept_policy"] = "always"

        elif tag == "webkitbrowser_get_useragent_string":
            testStepResults = testStepResults[0].values()[0]
            info["useragent"] = testStepResults[0].get("useragent")

        elif tag == "webkitbrowser_get_header":
            testStepResults = testStepResults[0].values()[0]
            header = testStepResults[0].get("headers")[0]
            if len(arg) and arg[0] == "get_name":
                info["name"] = header.get("name")
            elif len(arg) and arg[0] == "get_value":
                info["value"] = header.get("value")
            else:
                info = header

        elif tag == "webkitbrowser_check_average_fps":
            testStepResults = testStepResults[0].values()[0]
            fpsValues = 0;count = 0
            for result in testStepResults:
                count += 1
                fpsValues += int(result.get("fps"))
            average= fpsValues/count
            info["Average"] = average


        # System plugin result parser steps
        elif tag == "system_toggle_gz_enabled_status":
            testStepResults = testStepResults[0].values()[0]
            enabled = testStepResults[0].get("enabled")
            if str(enabled).lower() == "true":
                info["enabled"] = False
            else:
                info["enabled"] = True

        elif tag == "system_switch_power_state":
            testStepResults = testStepResults[0].values()[0]
            powerState = testStepResults[0].get("powerState")
            if powerState in ("STANDBY","DEEP_SLEEP","LIGHT_SLEEP"):
                info["powerState"] = "ON"
            else:
                info["powerState"] = "STANDBY"

        elif tag == "system_get_available_standby_modes":
            testStepResults = testStepResults[0].values()[0]
            info["standbyMode"] = testStepResults[0].get("supportedStandbyModes")
  
        elif tag == "system_generate_new_temperature_thresholds":
            testStepResults_list = testStepResults[0].values()[0]
            if str(arg[0]) == "warn":
                info["WARN"] = float(testStepResults_list[0].get("WARN")) + 10
            if str(arg[1]) == "max":
                info["MAX"] = float(testStepResults_list[0].get("MAX")) + 10

        elif tag == "system_get_bluetooth_mac":
            testStepResults = testStepResults[0].values()[0]
            info["bluetooth_mac"] = testStepResults[0].get("bluetooth_mac")

        elif tag == "system_get_powerstate_before_reboot":
            testStepResults = testStepResults[0].values()[0]
            info["powerState"] = testStepResults[0].get("powerState")

        elif tag == "system_get_estb_mac":
            testStepResults = testStepResults[0].values()[0]
            info["estb_mac"] = testStepResults[0].get("estb_mac")

        elif tag == "system_get_current_image_name":
            testStepResults = testStepResults[0].values()[0]
            info["image_name"] = testStepResults[0].get("current_FW_version")

        # user Preferences result parser steps
        elif tag == "userpreferences_switch_ui_language":
            testStepResults = testStepResults[0].values()[0]
            language = testStepResults[0].get("language")
            if "en" in str(language):
                info["language"] = "es"
            else:
                info["language"] = "en"


        # RDK Shell plugin result parser steps
        elif tag == "rdkshell_get_connected_client":
            testStepResults = testStepResults[0].values()[0]
            clients = testStepResults[0].get("clients")
            index = int(arg[0])
             
            if len(clients):
                if len(arg) > 1:
                    if arg[1] == "target":
                        info["target"] = clients[index]
                
                else:
                    info["client"] = clients[index]
            else:
                info["client"] = ""
                info["target"] = ""
        elif tag == "rdkshell_get_clients_state":
            testStepResults = testStepResults[0].values()[0]
            result = testStepResults[0].get("state")
            print result
            info["callsign"] = result[int(arg[0])].get("callsign")

        elif tag =="visibility_toggle_status":
            testStepResults = testStepResults[0].values()[0]
            status = testStepResults[0].get("visible")
            if str(status).lower() == "true":
                info["visible"] = False
            else:
                info["visible"] = True

        elif tag =="rdkshell_generate_new_opacity_value":
            testStepResults = testStepResults[0].values()[0]
            opacity = str(testStepResults[0].get("opacity"))
            #Check if the current opacity is set to 75 if not set it to 75 for testing.
            #If curretnt value is 75 then set to 50 for testing.
            if int(opacity) != 75:
                info["opacity"] = 75
            else:
                info["opacity"] = 50

        elif tag =="rdkshell_generate_new_scale_value":
            testStepResults = testStepResults[0].values()[0]
            #Generate a new scaling values by incrementing 1 to the given value
            if len(arg) > 0:
                if str(arg[0]) == "sx":
                    info["sx"] = float(testStepResults[0].get("sx")) + 1
                if str(arg[0]) == "sy":
                    info["sy"] = float(testStepResults[0].get("sy")) + 1
            else:
                info["sx"] = float(testStepResults[0].get("sx")) + 1
                info["sy"] = float(testStepResults[0].get("sy")) + 1

        elif tag =="rdkshell_get_last_client_zorder":
            testStepResults = testStepResults[0].values()[0]
            clients = testStepResults[0].get("clients")
            info["client"] = str(clients[(len(clients)-1)])
  
        elif tag == "rdkshell_get_zorder":
            testStepResults = testStepResults[0].values()[0]
            clients = testStepResults[0].get("clients")
            index = int(arg[0])
            if len(clients):
                info["client"] = clients[index]
            else:
                info["client"] = ""

        elif tag == "rdkshell_toggle_enabled_status":
            testStepResults = testStepResults[0].values()[0]
            enabled = testStepResults[0].get("enabled")
            if str(enabled).lower() == "true":
                info["enable"] = False
            else:
                info["enable"] = True

        elif tag == "rdkshell_set_virtual_resolution":
            testStepResults = testStepResults[0].values()[0]
            width = testStepResults[0].get("width")
            height = testStepResults[0].get("height")
            info["width"] = width
            info["height"] = height

        #Display info plugin result parser steps
        elif tag == "display_info_get_supported_resolution_list":
            testStepResults = testStepResults[0].values()[0]
            SupportingRes = testStepResults[0].get("supportedResolutions")
            info["resolution"] = ",".join(SupportingRes)

        elif tag == "displayinfo_get_connected_device_edid":
            testStepResults = testStepResults[0].values()[0]
            info["connected_device_edid"] = testStepResults[0].get('connected_device_edid')

        # Parser Code for ActivityMonitor plugin
        elif tag == "activitymonitor_get_appPid":
            testStepResults = testStepResults[0].values()[0]
            app_list=testStepResults[0].get("applicationMemory")
            if len(app_list) > 0:
                pid=app_list[0].get("appPid")
                if pid and int(pid) > 0:
                    info["pid"] = pid
                else:
                    info["pid"] = ""
            else:
                info["pid"] = ""

        # HDMI CEC plugin result parser steps
        elif tag == "hdmicec_toggle_enabled_status":
            testStepResults = testStepResults[0].values()[0]
            enabled = testStepResults[0].get("enabled")
            if str(enabled).lower() == "true":
                info["enabled"] = False
            else:
                info["enabled"] = True

        elif tag == "hdmicec_get_base64_data":
            testStepResults = testStepResults[0].values()[0]
            message  = testStepResults[0].get("message")
            info["message"] = message


        #Parser code for State Observer plugin
        elif tag == "StateObserver_change_version":
            testStepResults = testStepResults[0].values()[0]
            version = testStepResults[0].get("version")
            if int(float(version)) == 1:
                info["version"] = 2
            else:
                info["version"] = 1
        
        #Parser code for FirmwareController plugin
        elif tag == "change_image_version":
            testStepResults = testStepResults[0].values()[0]
            info["image"] = testStepResults[0].get("image")

        # Display Settings Plugin result parser steps
        elif tag == "display_get_isconnected_status":
            testStepResults = testStepResults[0].values()[0]
            is_connected = testStepResults[0].get("is_connected")
            info["is_connected"] = is_connected

        elif tag =="set_video_display":
            testStepResults = testStepResults[0].values()[0]
            video_display = testStepResults[0].get("video_display")       
            info["videoDisplay"] = video_display[0]
            info["portName"] = video_display[0] 

        elif tag =="get_supported_sound_modes":
            testStepResults = testStepResults[0].values()[0]
            supported_sound_modes = testStepResults[0].get("supported_audio_modes")
            info["soundMode"] = ",".join(supported_sound_modes)

        elif tag =="get_supported_resolutions":
            testStepResults = testStepResults[0].values()[0]
            supportedResolutions = testStepResults[0].get("supportedResolutions")
            info["resolution"] = ",".join(supportedResolutions)

        elif tag =="get_supported_audio_profiles":
            testStepResults = testStepResults[0].values()[0]
            audioProfiles = testStepResults[0].get("supportedMS12AudioProfiles")
            info["ms12AudioProfile"] = ",".join(audioProfiles)

        elif tag == "get_connected_audio_port":
            testStepResults = testStepResults[0].values()[0]
            audioPorts = testStepResults[0].get("connected_audio_port")
            if "HDMI0" in audioPorts:
                info["audioPort"] = "HDMI0"
            else:
                info["audioPort"] = audioPorts[0]

        elif tag =="get_formatted_sound_modes":
            testStepResults = testStepResults[0].values()[0]
            supported_sound_modes = testStepResults[0].get("supported_audio_modes")
            soundModes = []
            for mode in supported_sound_modes:
                if "AUTO" in mode:
                    value = re.search(r"\((.*?)\)",mode).group(1)
                    soundModes.append(value)
                else:
                    soundModes.append(mode)
            info["soundMode"] = ",".join(soundModes)
            
        elif tag =="get_settop_and_tv_resolutions":
            testStepResults1 = testStepResults[0].values()[0]
            testStepResults2 = testStepResults[1].values()[0]
            supportedTvResolutions = testStepResults1[0].get("supportedTvResolutions")
            supportedSettopResolutions = testStepResults2[0].get("supportedSettopResolutions")
            commonResolutions = list(set(supportedTvResolutions) & set(supportedSettopResolutions))
            info["commonResolutions"] = ",".join(commonResolutions)
        
        elif tag =="get_selected_resolutions":
            resolutionsList = []
            testStepResults = testStepResults[0].values()[0]
            supportedResolutions = testStepResults[0].get("supportedResolutions")
            resolutionsList.append(supportedResolutions[0])
            resolutionsList.append(supportedResolutions[len(supportedResolutions)/2])
            resolutionsList.append(supportedResolutions[len(supportedResolutions)-1])
            info["resolution"] = resolutionsList

        elif tag == "get_default_resolution":
            testStepResults = testStepResults[0].values()[0]
            info["defaultResolution"] = testStepResults[0].get("defaultResolution")

        elif tag == "get_audio_delay":
            testStepResults = testStepResults[0].values()[0]
            info["audioDelay"] = testStepResults[0].get("audioDelay")

        # Wifi Plugin Response result parser steps
        elif tag == "wifi_toggle_adapter_state":
            testStepResults = testStepResults[0].values()[0]
            state = str(testStepResults[0].get("state"))
            if len(arg) and arg[0] == "get_state_no":
                if state == "1":
                    info["state"] = "2"
                else:
                    info["state"] = "1"
            else:
                if state == "1":
                    info["enable"] = True
                else:
                    info["enable"] = False

        elif tag == "wifi_toggle_signal_threshold_status":
            testStepResults = testStepResults[0].values()[0]
            status = testStepResults[0].get("result")
            if len(arg) and arg[0] == "get_toggle_value":
                if int(status) == 1:
                    info["enabled"] = True
                else:
                    info["enabled"] = False
            else:
                if int(status) == 1:
                    info["result"] = 0
                else:
                    info["result"] = 1

        # Bluetooth Plugin Response result parser steps
        elif tag == "bluetooth_toggle_discoverable_status":
            testStepResults = testStepResults[0].values()[0]
            status = testStepResults[0].get("discoverable")
            if str(status).lower() == "true":
                info["discoverable"] = False
            else:
                info["discoverable"] = True

        elif tag == "bluetooth_get_device_id":
            testStepResults = testStepResults[0].values()[0]
            info["deviceID"] = testStepResults[0].get("deviceID")

        # Logging Preferences Plugin Response result parser steps
        elif tag == "loggingpreferences_toggle_keystroke_mask_state":
            testStepResults = testStepResults[0].values()[0]
            status = testStepResults[0].get("keystrokeMaskEnabled")
            if str(status).lower()== "false":
                  info["keystrokeMaskEnabled"] = True
            else:
                  info["keystrokeMaskEnabled"] = False

        #Timer Plugin Response result parser steps
        elif tag == "timer_start_timer_result":
            testStepResults = testStepResults[0].values()[0]
            info["timerId"] = testStepResults[0].get("timerId")


        # Messenger Plugin Response result parser steps
        elif tag == "messenger_get_roomid":
            testStepResults = testStepResults[0].values()[0]
            info["roomid"] = testStepResults[0].get("roomid")

        # HdmiInput plugin result parser steps
        elif tag == "hdmiinput_get_portids":
            testStepResults = testStepResults[0].values()[0]
            port_id_list = testStepResults[0].get("portIds")
            portIds = []
            for portId in port_id_list:
                portIds.append(portId)
            info["portId"] = ",".join(portIds)

        #PlayerInfo Plugin Response result parser steps
        elif tag == "player_info_get_resolutions":
            testStepResults = testStepResults[0].values()[0]
            SupportingRes = testStepResults[0].get("supportedResolutions")
            info["resolution"] = ",".join(SupportingRes)
        
        # TextToSpeech Plugin Response result parser steps
        elif tag == "texttospeech_toggle_enabled_status":
            testStepResults = testStepResults[0].values()[0]
            enabled_status = testStepResults[0].get("enabletts")
            if str(enabled_status).lower() == "true":
                info["enabletts"] = False
            else:
                info["enabletts"] = True

        # XCast Plugin Response result parser steps
        elif tag == "xcast_toggle_enabled_status":
            testStepResults = testStepResults[0].values()[0]
            enabled_status = testStepResults[0].get("enabled")
            if str(enabled_status).lower() == "true":
                info["enabled"] = False
            else:
                info["enabled"] = True
        elif tag == "xcast_toggle_standby_behavior_status":
            testStepResults = testStepResults[0].values()[0]
            standbyBehavior = testStepResults[0].get("standbybehavior")
            if str(standbyBehavior).lower() == "active":
                info["standbybehavior"] = "inactive"
            else:
                info["standbybehavior"] = "active"

        # Controller Plugin Response result parser steps
        elif tag == "controller_get_plugin_name":
            testStepResults = testStepResults[0].values()[0]
            info["callsign"] = testStepResults[0].get("callsign")
        else:
            print "\nError Occurred: [%s] No Parser steps available for %s" %(inspect.stack()[0][3],methodTag)
            status = "FAILURE"

    except Exception as e:
        status = "FAILURE"
        print "\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e)

    return status,info



#-----------------------------------------------------------------------------------------------
# checkTestCaseApplicability
#-----------------------------------------------------------------------------------------------
# Syntax      : checkTestCaseApplicability(methodTag,configKeyData,arguments)
# Description : Method to check whether the current test is applicable for the device or not
# Parameter   : configKeyData - Key data from the device/platform config file
#             : methodTag - tag used to identify the parser step
#             : arguments - list of arguments used for parsing
# Return Value: Function execution status & Applicability Status (TRUE/FALSE)
#-----------------------------------------------------------------------------------------------

def checkTestCaseApplicability(methodTag,configKeyData,arguments):
    tag  = methodTag
    arg  = arguments
    keyData  = configKeyData

    # Input Variables:
    # a. configKeyData - list
    # b. methodTag - string
    # c. arguments - list

    # Output variables:
    # a.status - (SUCCESS/FAILURE)
    #   1.It means the status of the parsing action
    #   By default is SUCCESS, it any exception occurs
    #   while parsing then status will be FAILURE
    # b.result - (TRUE/FALSE)
    #   1.It is the actual variable which indicates
    #   test case applicability

    # DO NOT OVERRIDE THE RETURN VARIABLES "RESULT" &
    # "STATUS" WITHIN PARSER STEPS TO STORE SOME OTHER
    # DATA. USER CAN ONLY UPDATE "RESULT" WITH (TRUE/FALSE)

    result = "TRUE"
    status = "SUCCESS"

    # USER CAN ADD N NUMBER OF PREVIOUS RESULT PARSER
    # STES BELOW
    try:
        if tag == "is_plugin_applicable":
            if arg[0] not in keyData:
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "displaysetting_check_feature_applicability":
            if all(item in keyData for item in arg):
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "is_led_supported":
            if arg[0] in keyData:
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "warehouse_na_tests":
            if arg[0] not in keyData:
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "bt_na_tests":
            if arg[0] not in str(keyData).lower():
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "network_check_feature_applicability":
            if arg[0] in keyData:
                result = "TRUE"
            else:
                result = "FALSE"
        elif tag == "wifi_check_feature_applicability":
            if arg[0] in keyData:
                result = "TRUE"
            else:
                result = "FALSE"
        elif tag == "controller_check_feature_applicability":
            if arg[0] in str(keyData).lower():
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "rdkshell_check_feature_applicability":
            if arg[0] in str(keyData).lower():
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "firmwarecontrol_check_feature_applicability":
            if arg[0] in keyData:
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "system_check_feature_applicability":
            if arg[0] in keyData:
                result = "TRUE"
            else:
                result = "FALSE"

        else:
            print "\nError Occurred: [%s] No Parser steps available for %s" %(inspect.stack()[0][3],methodTag)
            status = "FAILURE"

    except Exception as e:
        status = "FAILURE"
        print "\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e)

    return status,result


#-----------------------------------------------------------------------------------------------
# generateComplexTestInputParam
#-----------------------------------------------------------------------------------------------
# Syntax      : generateComplexTestInputParam(methodTag,testParams)
# Description : Method to generate complex test input parameters which cannot be generated
#               by the framework
# Parameter   : testParams - test params collected by the framework
#             : methodTag - tag used to identify the parser step
# Return Value: Function execution status & User Generated param Dictionary
#-----------------------------------------------------------------------------------------------
def generateComplexTestInputParam(methodTag,testParams):
    tag = methodTag

    # Input Variables:
    # a. testParams - test params to be re-formed
    # b. methodTag - string

    # Output variables:
    # a.status - (SUCCESS/FAILURE)
    #   1.It means the status of the parsing action
    #   By default is SUCCESS, it any exception occurs
    #   while parsing then status will be FAILURE
    # b.userGeneratedParam - dictionary/str/list
    #   1.Test params can be reformed in anyway
    #   and any data type.By default its dict

    # DO NOT OVERRIDE THE RETURN VARIABLE "STATUS"
    # WITHIN PARSER STEPS TO STORE SOME OTHER DATA.
    # USER CAN OVERRIDE "USERGENERATEDPARAM" WITH
    # RE-FORMED TEST INPUT PARAM

    status = "SUCCESS"
    userGeneratedParam = {}

    # USER CAN ADD N NUMBER OF PARAM REFORMING
    # STES BELOW
    try:

        if tag == "get_same_param":
            userGeneratedParam = testParams
        elif tag == "webkitbrowser_get_header_params":
            userGeneratedParam = [testParams]
        elif tag == "monitor_get_restart_params":
            userGeneratedParam = { "callsign": testParams.get("callsign"), "restart": { "limit": testParams.get("limit") ,  "window": testParams.get("window") }}
        elif tag == "rdkshell_set_keys_params":
            newtestParams = []
            for value in testParams.get("keyCode"):
                keysValue = {"keyCode" : int(value),"modifiers": testParams.get("modifiers"),"delay": testParams.get("delay")}
                newtestParams.append(keysValue)
            userGeneratedParam = {"keys":newtestParams}
        elif tag == "rdkshell_set_launch_params":
            userGeneratedParam = { "callsign": testParams.get("callsign"), "configuration": { "closurepolicy": testParams.get("closurepolicy") } }
        elif tag == "rdkshell_set_keylistener_params":
            newtestParams = testParams.copy()
            newtestParams.pop("client")
            userGeneratedParam = {"keys": [newtestParams],"client": testParams.get("client") }
        elif tag == "rdkshell_set_animations_params":
            userGeneratedParam = {"animations":[testParams]}
        elif tag == "cobalt_set_accessibility_params":
            newtestParams = testParams.copy()
            newtestParams.pop("ishighcontrasttextenabled")
            userGeneratedParam = {"closedcaptions": newtestParams, "textdisplay": { "ishighcontrasttextenabled": testParams.get("ishighcontrasttextenabled") } }
        elif tag == "system_set_thresholds_params":
            userGeneratedParam = {"thresholds":testParams}

        else:
            print "\nError Occurred: [%s] No Parser steps available for %s" %(inspect.stack()[0][3],methodTag)
            status = "FAILURE"

    except Exception as e:
        status = "FAILURE"
        print "\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e)

    return status,userGeneratedParam


#-----------------------------------------------------------------------------------------------
# ExecExternalFnAndGenerateResult
#-----------------------------------------------------------------------------------------------
# Syntax      : ExecExternalFnAndGenerateResult(methodTag,arguments,expectedValues,execInfo)
# Description : Method to execute other user defined functions by the framework
# Parameter   : methodTag - tag used to identify the function ti be called
#             : arguments - arguments to be passed to the function
#             : expectedValues - expected values to be checked
#             : execInfo - list of execution details like TM path, device IP, MAC, exec method
# Return Value: Result Info Dictionary
#-----------------------------------------------------------------------------------------------
def ExecExternalFnAndGenerateResult(methodTag,arguments,expectedValues,execInfo):
    tag  = methodTag
    arg  = arguments
    basePath = execInfo[0]
    deviceConfigFile = execInfo[1]
    deviceIP = execInfo[2]

    # Input Variables:
    # a. methodTag - string
    # b. arguments - list
    # c. expectedValues - list
    # d. execInfo - list

    # Output Variable:
    # a.info - dictionary
    #   1.info can have N different result key-value
    #    pairs based on user's need
    #   2.info must have "Test_Step_Status" key to
    #   update the status. By default its SUCCESS

    # USER MUST GENERATE THE TEST STEP RESULT FROM THE
    # EXTERNAL FUNCTION TO BE INVOKED AND UPDATE INFO
    # WITH THOSE RESULTS

    info = {}
    info["Test_Step_Status"] = "SUCCESS"

    # USER CAN ADD N NUMBER OF FUNCTION CALL STEPS BELOW

    try:
        print "\n\n---------- Executing Function ------------"
        print "FUNCTION TAG     :", tag
        if tag == "executeBluetoothCtl":
            info["Test_Step_Status"] = executeBluetoothCtl(deviceConfigFile,arg)
        elif tag == "broadcastIARMEventTuneReady":
            command = "IARM_event_sender TuneReadyEvent 1"
            info["details"] = executeCommand(execInfo, command)
            info["Test_Step_Status"] =  "SUCCESS"
        elif tag == "broadcastIARMEventChannelMap":
            command = "IARM_event_sender ChannelMapEvent 1"
            info["deatils"] = executeCommand(execInfo, command)
            info["Test_Step_Status"] =  "SUCCESS"
        elif tag == "Trust_MAC":
            deviceType = arguments[0]
            command = "bluetoothctl <<< 'trust "+arguments[1]+"'"
            executeCommand(execInfo, command, deviceType)
        elif tag == "Enable_TR181_Parameter":
            command = arguments[0]
            output = executeCommand(execInfo, command)
            if "set operation success" in output.lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "network_check_stb_ip_family":
            info["STB_IP_Family"] = expectedValues
            if str(expectedValues[0]) == str(deviceIP):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "EncodeHexToBase64":
            arguments[1] = arguments[1]+"0"
            hex_code  = "".join((arguments[1],arguments[0]))
            base64_data = hex_code.decode("hex").encode("base64")
            info["Hex_Data"] = hex_code
            info["message"] = base64_data.strip()

        elif tag == "Check_Version_File":
            command = '[ -f "/version.txt" ] && echo 1 || echo 0'
            output = executeCommand(execInfo, command)
            output = str(output).split("\n")
            if int(output[1]) == 1:
                print "Version.txt File Exists"
                command = '[ -s "/version.txt" ] && echo 1 ||  echo 0'
                output = executeCommand(execInfo, command)
                output = str(output).split("\n")
                if int(output[1]) == 1:
                    print "Version.txt File Is not Empty"
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    print "Version.txt File Is Empty"
                    info["Test_Step_Status"] = "FAILURE"
            else:
                print "Version.txt File doesn't Exists"
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_include.properties_file":
            xconfurl = arg[0]
            print "include.properties file exist,checking whether xconf url is updated"
            command = 'grep -q '+xconfurl+' /etc/include.properties  && echo 1 || echo 0'
            output = executeCommand(execInfo, command)
            output = str(output).split("\n")
            if int(output[1]) == 1:
                print "File is updated with xconf url"
                info["Test_Step_Status"] = "SUCCESS"
            else:
                print "File is not updated with xconf url,Updating file with xconf url"
                command = 'sed -i \'s~^CLOUDURL=.*$~CLOUDURL='+xconfurl+'~g\' /etc/include.properties;grep -q '+xconfurl+' /etc/include.properties  && echo 1 || echo 0'
                output = executeCommand(execInfo, command)
                output = str(output).split("\n")
                if int(output[1]) == 1:
                    print "Successfully updated file with xconf url"
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    print "File is not updated with xconf url"
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_swupdate_file":
            xconfurl = arg[0]
            command = '[ -f "/opt/swupdate.conf" ] && echo 1 || echo 0'
            output = executeCommand(execInfo, command)
            output = str(output).split("\n")
            if int(output[1]) == 1:
                print "swupdate.conf file exist,checking whether xconf url is updated"
                command = 'grep -q '+xconfurl+' /opt/swupdate.conf  && echo 1 || echo 0'
                output = executeCommand(execInfo, command)
                output = str(output).split("\n")
                if int(output[1]) == 1:
                    print "File is updated with xconf url"
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    print "File is not updated with xconf url,Updating file with xconf url"
                    command = 'echo '+xconfurl+' >> /opt/swupdate.conf;grep -q '+xconfurl+' /opt/swupdate.conf  && echo 1 || echo 0'
                    output = executeCommand(execInfo, command)
                    output = str(output).split("\n")
                    if int(output[1]) == 1:
                        print "Successfully updated file with xconf url"
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        print "File is not updated with xconf url"
                        info["Test_Step_Status"] = "FAILURE"
            else:
                print "swupdate.conf file does not exist. Creating the file...."
                command = 'touch /opt/swupdate.conf;[ -f "/opt/swupdate.conf" ] && echo 1 || echo 0'
                output = executeCommand(execInfo, command)
                output = str(output).split("\n")
                if int(output[1]) == 1:
                    print "File created"
                    command = 'echo '+xconfurl+' >> /opt/swupdate.conf;grep -q '+xconfurl+' /opt/swupdate.conf  && echo 1 || echo 0'
                    output = executeCommand(execInfo, command)
                    output = str(output).split("\n")
                    if int(output[1]) == 1:
                        print "Successfully updated file with xconf url"
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        print "File is not updated with xconf url"
                        info["Test_Step_Status"] = "FAILURE"

                else:
                    print "File doesn't created"
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "Check_disk_partition":
            command = 'ls /dev/mmcblk0*'
            output = executeCommand(execInfo, command)
            output = output.splitlines()
            partition_list = output[1].split()
            partition_count = len(partition_list)-1
            info["partition_count"] = partition_count
            if len(arg) and arg[0] == "after_reboot":
                if str(partition_count) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "Set_xconfServerConfigurations":
            configParser = ConfigParser.ConfigParser()
            configParser.read(r'%s' % deviceConfigFile)
            firmwareDownloadProtocol = configParser.get('device.config', 'FIRMWARE_DOWNLOAD_PROTOCOL')
            firmwareLocation = configParser.get('device.config', 'FIRMWARE_LOCATION')
            xconfurl = configParser.get('device.config', 'XCONF_SERVER_URL')
            if len(arg) and arg[0]=="upgrade_image":
                firmwareFilename = configParser.get('device.config', 'FIRMWARE_FILENAME')
            elif len(arg) and arg[0]=="revert_image":
                firmwareFilename = configParser.get('device.config', 'EXISTING_FIRMWARE_FILENAME')
            command = 'curl -X PUT -H \'Content-Type: application/json\' -d \'{"eStbMac": "'+arg[1]+'","xconfServerConfig": {"firmwareDownloadProtocol": "'+firmwareDownloadProtocol+'","firmwareFilename": "'+firmwareFilename+'","firmwareVersion": "'+firmwareFilename+'","firmwareLocation": "'+firmwareLocation+'","rebootImmediately": false}}\' '+xconfurl
            output = executeCommandInTM(command)
            info["RESULT"] = output
            if "Successfully added configuration" in output:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "Create_File":
            command = "mkdir "+arguments[0]+"/Controller;[ -d "+arguments[0]+"/Controller ] && echo 1 || echo 0"
            status = executeCommand(execInfo, command)
            status = str(status).split("\n")
            result = 1
            if int(status[1]) == result:
                info["RESULT"] = "Controller directory created"
                command = "touch "+arguments[0]+"/Controller/TDK_TEST_FILE.txt;[ -f "+arguments[0]+"/Controller/TDK_TEST_FILE.txt ] && echo 1 || echo 0"
                status = executeCommand(execInfo, command)
                status = str(status).split("\n")
                result = 1
                if int(status[1]) == result:
                    info["RESULT"] = "File created"
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["RESULT"] = "File not created"
                    info["Test_Step_Status"] = "FAILURE"

            else:
                info["RESULT"] = "Controller directory not created"
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "Check_WPE_Process":
            processesRunning = []
            processesNotRunning = []
            command = "ps -ef | awk '{print $8}' ; ps -eo comm"
            output = executeCommand(execInfo, command)
            for value in expectedValues:
                if ":" in str(value):
                    value = value.split(":")[1]
                if value.lower() in str(output).lower():
                    status = True
                    processesRunning.append(value)
                else:
                    status = False
                    processesNotRunning.append(value)
            if status:
                info["Running_Processes"] = processesRunning
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Running_Processes"] = processesRunning
                info["processes_Not_Running"] = processesNotRunning
                info["Test_Step_Status"] = "FAILURE" 
        elif tag == "check_fps_value":
            expectedFPS = (int(expectedValues[0])-int(expectedValues[1]))
            info["AVERAGE_FPS"] = arguments[0]
            if int(arguments[0]) >= expectedFPS:
                message = "FPS should be >= %d & it is as expected" %(expectedFPS)
                info["Test_Step_Status"] = "SUCCESS"
            else:
                message = "FPS should be >= %d & it is not as expected" %(expectedFPS)
                info["Test_Step_Status"] = "FAILURE"
            info["Test_Step_Message"] = message

        elif tag == "Check_If_File_Exists":
            command = "[ -f "+arguments[0]+"/Controller/TDK_TEST_FILE.txt ] && echo 1 || echo 0"
            status = executeCommand(execInfo, command)
            status = str(status).split("\n")
            result = 0
            if int(status[1]) == result:
                info["RESULT"] = "File does not exist"
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["RESULT"] = "File exist"
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "Delete_Test_File":
            command = "[ -d "+arguments[0]+"/Controller ] && echo 1 || echo 0"
            status = executeCommand(execInfo, command)
            status = str(status).split("\n")
            if int(status[1]) == 0:
                info["RESULT"] = "File does not exist"
                info["Test_Step_Status"] = "SUCCESS"
            else:
                command = "rm -rf "+arguments[0]+"/Controller ; [ -d "+arguments[0]+"/Controller ] && echo 1 || echo 0"
                status = executeCommand(execInfo, command)
                status = str(status).split("\n")
                if int(status[1]) == 0:
                    info["Message"] = "Test file deleted"
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Message"] = "Test file not deleted"
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "Framerate_Get_Width_And_Height":
            DisplayFrameRate_values = []
            for values in range(1,len(arg)):
                mapping_details = arg[values].split(":")
                width = mapping_details[1].split('|')[0].strip('[]')
                height = mapping_details[1].split('|')[1].strip('[]')
                DisplayFrameRate = width+'x'+height+'x40'
                DisplayFrameRate_values.append(DisplayFrameRate)
            info["DisplayFrameRate"] = DisplayFrameRate_values
        
        elif tag == "RDKShell_Get_Width_And_Height":
            mapping_details = arg[len(arg)-1].split(":")
            info["width"] = mapping_details[1].split('|')[0].strip('[]')
            info["height"] = mapping_details[1].split('|')[1].strip('[]')

        elif tag == "Check_Environment_Variable_In_Service_File":
            command = 'grep -q '+str(expectedValues[0])+' /lib/systemd/system/wpeframework.service && echo 1 || echo 0'
            output = executeCommand(execInfo, command)
            output = str(output).split("\n")
            if int(output[1]) == 1:
                message = "\"RDKSHELL_SPLASH_IMAGE_JPEG\" Environment variable is present in the  wpeframework.service file"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "SUCCESS"
            else:
                message = "\"RDKSHELL_SPLASH_IMAGE_JPEG\" Environment variable is not present in the wpeframework.service file but \"Splash Screen\" feature configured as supported feature in config file"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "executeRebootCmd":
            command = "reboot"
            info["deatils"] = executeCommand(execInfo, command)
            info["Test_Step_Status"] =  "SUCCESS"
        elif tag == "getImageVersion":
            command = "cat /version.txt | grep imagename | cut -d ':' -f2"
            details = executeCommand(execInfo, command)
            info["image"] = str(details).split("\n")[1]
            if len(arg) and arg[0] == "get":
                if str(info["image"]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if expectedValues[0] in info["image"] :
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        elif tag == "toggleMemoryBank":
            command = "/bin/sh /usr/bin/swap_bank.sh"
            info["deatils"] = executeCommand(execInfo, command)
            info["Test_Step_Status"] =  "SUCCESS"

        else:
            print "\nError Occurred: [%s] No function call available for %s" %(inspect.stack()[0][3],methodTag)
            info["Test_Step_Status"] = "FAILURE"

    except Exception as e:
        print "\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e)
        info["Test_Step_Status"] = "FAILURE"
    return info


#-----------------------------------------------------------------------------------------------
#                    ***  USER CAN ADD SUPPORTING FUNCTIONS BELOW ***
#-----------------------------------------------------------------------------------------------
def checkAndGetAllResultInfo(result,success="null"):
    info = {}
    info = result.copy()
    status = checkNonEmptyResultData(info.values())
    success = str(success).lower() == "true" if success != "null" else True
    if success and status == "TRUE":
        info["Test_Step_Status"] = "SUCCESS"
    else:
        info["Test_Step_Status"] = "FAILURE"

    return info


def checkNonEmptyResultData(resultData):
    status = "TRUE"
    if resultData is None:
        status = "FALSE"
    elif type(resultData) is list:
        for data in resultData:
            if str(data).strip() == "":
                status = "FALSE"
                break;
        if len(resultData) == 0:
            status = "FALSE"
    elif str(resultData).strip() == "":
        status = "FALSE"

    return status

def compareURLs(actualURL,expectedURL):
    if expectedURL in actualURL:
        status = "TRUE"
    else:
        url_data = []
        url_data_split = [ data for data in expectedURL.split("/") if data.strip() ]
        for data in url_data_split:
            if "?" in data:
                url_data.extend(data.split("?"))
            else:
                url_data.append(data)
        status = "TRUE"
        for data in url_data:
            if data not in actualURL:
                status = "FALSE"

    return status

def DecodeBase64ToHex(base64):
    if len(base64) % 4 != 0:
        while len(base64) % 4 != 0:
            base64 = base64 + "="
    decoded = b64decode(base64)
    hex_code = codecs.encode(decoded, 'hex').decode("utf-8")
    return hex_code


# Other External Functions can be added below

def executeBluetoothCtl(deviceConfigFile,commands):
    try :
        #Get Bluetooth configuration file
        configParser = ConfigParser.ConfigParser()
        configParser.read(r'%s' % deviceConfigFile)
        ip = configParser.get('device.config', 'BT_EMU_IP')
        username = configParser.get('device.config', 'BT_EMU_USER_NAME')
        password = configParser.get('device.config', 'BT_EMU_PWD')
        deviceName = configParser.get('device.config','BT_EMU_DEVICE_NAME')
        #Executing the commands in device
        print 'Number of commands:', len(commands)
        print 'Commands List:', commands
        print "Connecting to client device"
        global session
        session = pxssh.pxssh(options={
                            "StrictHostKeyChecking": "no",
                            "UserKnownHostsFile": "/dev/null"})
        session.login(ip,username,password,sync_multiplier=5)
        print "Executing the bluetoothctl commands"
        for parameters in range(0,len(commands)):
            session.sendline(commands[parameters])
        session.prompt()
        status=session.before
        status=status.strip()
        #session.logout()
        status = "SUCCESS"
        #session.close()
        print "Successfully Executed bluetoothctl commands in client device"
    except Exception, e:
        print e;
        status = "FAILURE"

    return status

def executeCommand(execInfo, command, device="test-device"):
    deviceConfigFile = execInfo[1]
    deviceIP         = execInfo[2]
    deviceMAC        = execInfo[3]
    execMethod       = execInfo[4]

    configParser = ConfigParser.ConfigParser()
    configParser.read(r'%s' % deviceConfigFile)
    sshMethod = configParser.get('device.config', 'SSH_METHOD')
    if device == "test-device":
        username = configParser.get('device.config', 'SSH_USERNAME')
        password = configParser.get('device.config', 'SSH_PASSWORD')
    elif device == "bt-emu":
        deviceIP = configParser.get('device.config', 'BT_EMU_IP')
        username = configParser.get('device.config', 'BT_EMU_USER_NAME')
        password = configParser.get('device.config', 'BT_EMU_PWD')
        deviceName = configParser.get('device.config','BT_EMU_DEVICE_NAME')
    if password == "None":
        password = ''

    output = ""
    if sshMethod.upper() == "DIRECTSSH":
        try:
            session = pxssh.pxssh(options={
                                "StrictHostKeyChecking": "no",
                                "UserKnownHostsFile": "/dev/null"})
            print "\nCreating ssh session"
            session.login(deviceIP,username,password,sync_multiplier=5)
            sleep(2)
            print "Executing command: ",command
            session.sendline(command)
            if command == "reboot":
                sleep(2);
                output = "reboot"
            else:
                session.prompt()
                output = session.before
                print"Closing session"
                session.logout()
        except pxssh.ExceptionPxssh as e:
            print "Login to device failed"
            print e
    elif sshMethod.upper() == "REST":
        auth_token= ""
        rest_url = ""
        try:
            print "\nFetching config file values for REST api call"
            rest_url = CertificationSuiteCommonVariables.rest_url
            auth_method = CertificationSuiteCommonVariables.auth_method
            if auth_method == "TOKEN":
                auth_token = CertificationSuiteCommonVariables.auth_token
                if auth_token =="" or rest_url == "":
                    print "\n[ERROR]: Missing REST API configurations"
                else:
                    headers = {'Content-Type': 'application/json', 'authToken': auth_token,}
                    url = str(rest_url.replace("mac",deviceMAC))
                    command = command.replace(" grep","grep").replace("|grep",'\|grep').replace("\"","\\\"")
                    if "awk" in command:
                        command = command.replace("$","\$")
                    command = "\"" + command + "\"";
                    print "Executing command: ",command
                    response = requests.post(url, headers=headers, data=command, timeout=20)
                    #print response.content
                    output = response.content
                    #output = command + '\n' + output;
        except Exception as e:
            print "Login to device failed"
            print e
    else:
        print "\n[ERROR]: Invalid SSH Method"

    return output


def executeCommandInTM(command):
    output = ""
    try:
        if "" == command:
            status = "FAILURE"
            print "[ERROR]: Command to be executed cannot be empty"
        else:
            print "Going to execute %s..." %(command)
            output = subprocess.check_output (command, shell=True)
    except Exception, e:
        print e
        status = "FAILURE"
        print "Unable to execute %s successfully" %(command)
    return output
