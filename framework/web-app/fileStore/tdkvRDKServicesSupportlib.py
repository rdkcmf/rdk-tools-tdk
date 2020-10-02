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


#-----------------------------------------------------------------------------------------------
#               ***  RDK SERVICES VALIDATION FRAMEWORK SUPPORTING FUNCTIONS ***
#-----------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------
# CheckAndGenerateTestStepResult
#-----------------------------------------------------------------------------------------------
# Syntax      : CheckAndGenerateTestStepResult(result,methodTag,arguments,expectedValues)
# Description : Method to parse the output JSON response and generate test result
# Parameter   : result - JSON response result value
#             : methodTag - tag used to identify the parser step
#             : arguments - list of arguments used for parsing
#             : expectedValues - list of expected values
# Return Value: Result Info Dictionary
#-----------------------------------------------------------------------------------------------
def CheckAndGenerateTestStepResult(result,methodTag,arguments,expectedValues):
    tag  = methodTag
    arg  = arguments

    # Input Variables:
    # a. result - result from response JSON
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
        # DeviceInfo Plugin Response result parser steps
        if tag == "deviceinfo_get_system_info":

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


        elif tag == "network_get_stb_ip":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "network_get_named_endpoints":
            result = result.get("endpoints")
            endpoints = [ name.get("endpoint") for name in result ]
            endpoints = [ str(name) for name in endpoints if str(name).strip() ]
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
            packets_loss = int(result.get("packetLoss"))
            success = str(result.get("success")).lower() == "true"
            if len(arg) and arg[0] == "check_target":
                packets = int(expectedValues[0])
                host_ip = expectedValues[1]
                if success and target == host_ip and tx_packets == packets and rx_packets == packets and packets_loss == 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                packets = int(expectedValues[0])
                if success and target.strip() and tx_packets == packets and rx_packets == packets and packets_loss == 0:
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


        # WebKitBrowser Plugin Response result parser steps
        elif tag == "webkitbrowser_get_state":
            info["state"] = result
            if result in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_check_url":
            info["url"] = result
            if expectedValues[0] in result:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                url_data = [ data for data in expectedValues[0].split("/") if data.strip() ]
                status = "TRUE"
                for data in url_data:
                    if data not in result:
                        status = "FALSE"
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
            info["fps"] = result
            if int(result) >= int(expectedValues[0]):
                message = "FPS should be > %s & it is as expected" %(expectedValues[0])
                info["Test_Step_Status"] = "SUCCESS"
            else:
                message = "FPS should be > %s & it is not as expected" %(expectedValues[0])
                info["Test_Step_Status"] = "FAILURE"
            info["Test_Step_Message"] = message

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


        # Cobalt Plugin Response result parser steps
        elif tag == "cobalt_get_state":
            info["state"] = result
            if result in expectedValues:
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
            if success and status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_get_preferred_standby_mode":
            preferredStandbyMode = result.get("preferredStandbyMode")
            success = str(result.get("success")).lower() == "true"
            info["preferredStandbyMode"] = preferredStandbyMode
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
            info = checkAndGetAllResultInfo(result,result.get("success"))

        # User Preferces Plugin Response result parser steps
        elif tag == "userpreferences_get_ui_language":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if len(arg) and arg[0] == "check_language":
                if result.get("language") in expectedValues:
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

        elif tag == "rdkshell_check_for_nonempty_result":
            info = checkAndGetAllResultInfo(result)

        elif tag == "rdkshell_check_for_visibility_result":
            if result.get("visible") in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # read previously set resolution and compare it
        elif tag == "rdkshell_check_for_resolution_set":
            if str(result.get("w")) == "1080" and str(result.get("h")) == "720":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_for_bounds":
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
            status = result.get("opacity")
            if expectedValues is not None:
                if int(expectedValues) is int(status):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif int(status) >= 0 and int(status) <=100 :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_verify_scale_params":
            if int(result.get("sx")) is int(expectedValues[0]) and int(result.get("sy")) is int(expectedValues[1]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_if_application_killed":
            result = result.get("clients")
            clients = [ str(name) for name in result if str(name).strip() ]
            if expectedValues not in clients:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # DisplayInfo Plugin Response result parser steps
        elif tag == "displayinfo_get_general_info":
            if arg[0] == "get_all_info":
                info = checkAndGetAllResultInfo(result)

        elif tag == "displayinfo_check_for_nonempty_result":
            info = checkAndGetAllResultInfo(result)

        elif tag == "displayinfo_validate_boolean_result":
            if str(result.lower()) == "true" or str(result.lower()) == "false" :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "displayinfo_validate_width_or_height":
            if arg[0] is "width":
                index = 0
            elif arg[0] is "height":
                index = 1
            SupportingRes=expectedValues
            search_key = int(result)
            Resolution_Details = {"480i":[720,480],"480p":[720,480],"576p50":[720,576],"720p":[1280,720],"720p50":[1280,720],"1080p24":[1920,1080],"1080i":[1920,1080],"1080p60":[1920,1080],"1080i50":[1920,1080],"2160p30":[3840,2160],"2160p60":[3840,2160]}
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



        # Display Settings Plugin Response result parser steps
        elif tag == "display_is_connected":
            info["video_display"] = result.get('connectedVideoDisplays')
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result.get('connectedVideoDisplays'))
            if success and status == "TRUE":
                info["is_connected"] = "true"
            elif success and status == "FALSE":
                info["is_connected"] = "false"
            info["Test_Step_Status"] = "SUCCESS"

        elif tag == "display_settings_check_set_operation":
            info["success"] = result.get("success")
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "display_connected_status":
            info["video_display"] = result.get('connectedVideoDisplays')
            if json.dumps(result.get('success')) == "true" and any(item in result.get('connectedVideoDisplays') for item in ["HDMI0"]):
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
            info["connected_device_edid"] = result.get('EDID')
            if json.dumps(result.get('EDID')) and json.dumps(result.get("success")) == "true" :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_connected_audio_ports":
            info["connected_audio_port"] = result.get('connectedAudioPorts')
            if json.dumps(result.get('success')) == "true" and any(item in result.get('connectedAudioPorts') for item in ["HDMI0"]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_supported_audio_modes":
            info["supported_audio_modes"] = result.get('supportedAudioModes');
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_sound_mode":
            info["soundMode"] = result.get('soundMode');
            if str(result.get("success")).lower() == "true":
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
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_active_input":
            info ["activeInput"] = result.get('activeInput')
            if str(result.get("success")).lower() == "true" and any(str(result.get('activeInput')) in item for item in expectedValues):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_MS12_audio_compression":
            info["compressionlevel"] = result.get('compressionlevel');
            if str(result.get("success")).lower() == "true" and result.get('compressionlevel') in expectedValues :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_video_port_status_standby":
            info["enabled"] = result.get('videoPortStatusInStandby');
            if str(result.get("success")).lower() == "true" and any(str(result.get('videoPortStatusInStandby')) in item for item in expectedValues) :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_dolby_volume_mode":
            info["dolbyVolumeMode"] = result.get('dolbyVolumeMode');
            if str(result.get("success")).lower() == "true" and any(str(result.get('dolbyVolumeMode')) in item for item in expectedValues):
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
            if powerState == "ON":
                info["powerState"] = "STANDBY"
            else:
                info["powerState"] = "ON"
        elif tag == "system_get_available_standby_modes":
            testStepResults = testStepResults[0].values()[0]
            info["standbyMode"] = testStepResults[0].get("supportedStandbyModes")
        elif tag == "system_switct_timezone_dst":
            testStepResults = testStepResults[0].values()[0]
            timeZone = testStepResults[0].get("timeZone")
            if timeZone == "UTC-5":
                info["timeZone"] == "UTC-7"
            else:
                info["timeZone"] == "UTC-5"

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
            param = arg[1]

            if len(clients):
                if param is "target":
                    info["target"] = clients[index]
                else:
                    info["client"] = clients[index]
            else:
                info["client"] = ""
                info["target"] = ""

        elif tag =="visibility_toggle_status":
            testStepResults = testStepResults[1].values()[0]
            status = testStepResults[0].get("visible")
            if str(status).lower() == "true":
                info["visible"] = False
            else:
                info["visible"] = True

        elif tag =="rdkshell_generate_new_opacity_value":
            testStepResults = testStepResults[0].values()[0]
            opacity = testStepResults[0].get("opacity")
            #Check if the current opacity is set to 75 if not set it to 75 for testing.
            #If curretnt value is 75 then set to 50 for testing.
            if int(opacity) != 75:
                info["opacity"] = 75
            else:
                info["opacity"] = 50

        elif tag =="rdkshell_generate_new_scale_value":
            testStepResults = testStepResults[0].values()[0]
            #Generate a new scaling values by incrementing 1 to the given value
            if arg[0] == "sx":
                info["sx"] = int(testStepResults[0].get("sx")) + 1
            if arg[0] == "sy":
                info["sy"] = int(testStepResults[0].get("sy")) + 1

        #Display info plugin result parser steps
        elif tag == "display_info_get_supported_resolution_list":
            testStepResults = testStepResults[0].values()[0]
            SupportingRes = testStepResults[0].get("supportedResolutions")
            info["resolutions"] = ",".join(SupportingRes)


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

        elif tag =="get_audio_port":
            testStepResults = testStepResults[0].values()[0]
            connected_audio_port = testStepResults[0].get("connected_audio_port")
            info["audioPort"] = connected_audio_port[0]

        elif tag =="get_supported_sound_modes":
            testStepResults = testStepResults[0].values()[0]
            supported_sound_modes = testStepResults[0].get("supported_audio_modes")
            info["soundMode"] = ",".join(supported_sound_modes)

        elif tag =="get_supported_resolutions":
            testStepResults = testStepResults[0].values()[0]
            supportedResolutions = testStepResults[0].get("supportedResolutions")
            info["resolution"] = ",".join(supportedResolutions)


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

        elif tag == "is_led_supported":
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

        else:
            print "\nError Occurred: [%s] No Parser steps available for %s" %(inspect.stack()[0][3],methodTag)
            status = "FAILURE"

    except Exception as e:
        status = "FAILURE"
        print "\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e)

    return status,userGeneratedParam




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



