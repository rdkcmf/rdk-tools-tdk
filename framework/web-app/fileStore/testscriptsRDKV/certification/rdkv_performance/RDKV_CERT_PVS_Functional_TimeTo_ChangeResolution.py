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
##########################################################################
'''
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>1</version>
  <name>RDKV_CERT_PVS_Functional_TimeTo_ChangeResolution</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken to change resolution using DisplaySettings plugin.</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-HYB</box_type>
    <box_type>RPI-Client</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_97</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to change resolution using DisplaySettings plugin.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. CHANGE_RESOLUTION_VALUE should be configured in device config file
2. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>CHANGE_RESOLUTION_VALUE</input_parameters>
    <automation_approch>1. Activate Displaysettings plugin
2. Get the connected video displays list
3. Check the current resolution of first display in the above list
4. Set a given resolution which is different from the current resolution
5. Check the resolutionChanged event and validate the time taken to change resolution</automation_approch>
    <expected_output>The time taken to change resolution should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_ChangeResolution</test_script>
    <skipped>No</skipped>
    <release_version>M96</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib 
import PerformanceTestVariables
import json
import ast
from StabilityTestUtility import *
from web_socket_util import *
import rdkv_performancelib
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_ChangeResolution')

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Execution summary variable 
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    status = "SUCCESS"
    revert="NO"
    value = {}
    params = {}
    event_listener = None
    plugins_list = ["org.rdk.DisplaySettings"]
    print "\n Check Pre conditions"
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    plugin_status_needed = {"org.rdk.DisplaySettings":"activated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            print "\n Error while setting status of plugins, current status: ",new_plugins_status
            status = "FAILURE"
    conf_file,file_status = get_configfile_name(obj)
    result1, resolution = getDeviceConfigKeyValue(conf_file,"CHANGE_RESOLUTION_VALUE")
    if resolution == "":
        print "\n Configure the CHANGE_RESOLUTION_VALUE in device config file"
    if status == "SUCCESS" and resolution != "":
        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
        tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.getConnectedVideoDisplays")
        tdkTestObj.addParameter("reqValue","connectedVideoDisplays")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        connected_displays = tdkTestObj.getResultDetails()
        connected_displays = ast.literal_eval(connected_displays)
        if connected_displays and result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
            print "\n Get current resolution for ",connected_displays[0]
            value["videoDisplay"] = connected_displays[0]
            input_value = json.dumps(value)
            tdkTestObj = obj.createTestStep('rdkservice_getValueWithParams')
            tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.getCurrentResolution")
            tdkTestObj.addParameter("params",input_value)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            initial_resolution = tdkTestObj.getResultDetails()
            initial_resolution = ast.literal_eval(initial_resolution)
            initial_resolution = initial_resolution["resolution"]
            if result == "SUCCESS":
                print "\n Current resolution for {} port :{}".format(connected_displays[0],initial_resolution)
                tdkTestObj.setResultStatus("SUCCESS")
                print "\n Get supported resolutions for :",connected_displays[0]
                tdkTestObj = obj.createTestStep('rdkservice_getValueWithParams')
                tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.getSupportedResolutions")
                tdkTestObj.addParameter("params",input_value)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if result == "SUCCESS":
                    supported_resolutions = tdkTestObj.getResultDetails()
                    supported_resolutions = ast.literal_eval(supported_resolutions)
                    supported_resolutions = supported_resolutions["supportedResolutions"]
                    print "\n Supported resolutions for {} display: {}".format(connected_displays[0],supported_resolutions)
                    if len(supported_resolutions) > 1:
                        tdkTestObj.setResultStatus("SUCCESS")
                        thunder_port = rdkv_performancelib.devicePort
                        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 6,"method": "org.rdk.DisplaySettings.1.register","params": {"event": "resolutionChanged", "id": "client.events.1" }}'],"/jsonrpc",False)
                        time.sleep(10)
                        supported_resolutions.remove(initial_resolution)
                        if resolution in supported_resolutions:
                            params["videoDisplay"] = connected_displays[0]
                            params["resolution"] = resolution
                            params["persist"] = True
                            input_params = json.dumps(params)
                            print "\n Set resolution to :",resolution
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.setCurrentResolution")
                            tdkTestObj.addParameter("value",input_params)
                            resol_change_start_time = str(datetime.utcnow()).split()[1]
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            if result == "SUCCESS":
                                tdkTestObj.setResultStatus("SUCCESS")
                                time.sleep(10)
                                continue_count = 0
                                resolution_changed_time = ""
                                while True:
                                    if (continue_count > 60):
                                        break
                                    if (len(event_listener.getEventsBuffer())== 0):
                                        continue_count += 1
                                        time.sleep(1)
                                        continue
                                    event_log = event_listener.getEventsBuffer().pop(0)
                                    print "\n Triggered event: ",event_log,"\n"
                                    if (resolution in event_log and "resolutionChanged" in str(event_log)):
                                        print "\n Event :resolutionChanged is triggered during resolution change"
                                        resolution_changed_time = event_log.split('$$$')[0]
                                        break
                                if resolution_changed_time:
                                    tdkTestObj = obj.createTestStep('rdkservice_getValueWithParams')
                                    tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.getCurrentResolution")
                                    tdkTestObj.addParameter("params",input_value)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result = tdkTestObj.getResult()
                                    current_resolution = tdkTestObj.getResultDetails()
                                    current_resolution = ast.literal_eval(current_resolution)
                                    current_resolution = current_resolution["resolution"]
                                    if result == "SUCCESS" and  current_resolution == resolution:
                                        print "\n Successfully set current resolution to: ",resolution
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        config_status,resol_change_threshold = getDeviceConfigKeyValue(conf_file,"RESOLUTION_CHANGE_THRESHOLD_VALUE")
                                        Summ_list.append('RESOLUTION_CHANGE_THRESHOLD_VALUE :{}ms'.format(resol_change_threshold))
                                        offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                        Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
                                        if all(value != "" for value in (resol_change_threshold,offset)):
                                            resol_change_start_time_in_millisec = getTimeInMilliSec(resol_change_start_time)
                                            resolution_changed_time_in_millisec = getTimeInMilliSec(resolution_changed_time)
                                            print "\n Resolution change initiated at: " ,resol_change_start_time
                                            Summ_list.append('Resolution change initiated at :{}'.format(resol_change_start_time))
                                            print "\n Resolution changed at : ",resolution_changed_time
                                            Summ_list.append('Resolution changed at  :{}'.format(resolution_changed_time))
                                            time_taken_for_resol_change = resolution_changed_time_in_millisec - resol_change_start_time_in_millisec
                                            Summ_list.append('Time taken to change resolution :{}ms'.format(time_taken_for_resol_change))
                                            print "\n Time taken to change resolution: {}(ms)".format(time_taken_for_resol_change)
                                            print "\n Threshold value for time taken to change resolution plugin : {} ms".format(resol_change_threshold)
                                            print "\n Validate the time:"
                                            if 0 < time_taken_for_resol_change < (int(resol_change_threshold) + int(offset)) :
                                                print "\n Time taken for changing resolution is within the expected range"
                                                tdkTestObj.setResultStatus("SUCCESS")
                                            else:
                                                print "\n Time taken for changing resolution is not within the expected range"
                                                tdkTestObj.setResultStatus("FAILURE")
                                        else:
                                            print "\n Please configure the Threshold value in device configuration file"
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print "\n Unable to set the resolution to : {}, current resolution: {}".format(resolution,current_resolution)
                                else:
                                    print "\n resolutionChanged event not triggered for during Resolution change"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Error while setting resolution"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n The resolution {} is not supported, please configure CHANGE_RESOLUTION_VALUE from : {}".format(resolution,supported_resolutions)
                            tdkTestObj.setResultStatus("FAILURE")
                        event_listener.disconnect()
                        time.sleep(10)
                        #Revert resolution
                        params = {}
                        params["videoDisplay"] = connected_displays[0]
                        params["resolution"] = initial_resolution
                        params["persist"] = True
                        input_params = json.dumps(params)
                        print "\n Revert resolution to :",initial_resolution
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.setCurrentResolution")
                        tdkTestObj.addParameter("value",input_params)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        if result == "SUCCESS":
                            print "\n Successfully reverted the resolution"
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\n Error while reverting the resolution to : ",initial_resolution
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Only one resolution is supported"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error while getting the supported resolutions"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while getting the initial resolution"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Unable to find connected displays, connected displays list:",connected_displays
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Pre conditions are not met \n"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
    getSummary(Summ_list)
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
