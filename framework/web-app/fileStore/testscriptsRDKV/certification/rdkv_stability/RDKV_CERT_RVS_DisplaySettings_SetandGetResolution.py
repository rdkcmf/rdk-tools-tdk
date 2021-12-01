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
  <name>RDKV_CERT_RVS_DisplaySettings_SetandGetResolution</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateResourceUsage</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to set different resolutions using setCurrentResolution api from DisplaySettings and verify it with getCurrentResolutions for a minimum of 1000 times</synopsis>
  <groups_id/>
  <execution_time>600</execution_time>
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
    <test_case_id>RDKV_STABILITY_60</test_case_id>
    <test_objective>The objective of this test is to set different resolutions using setCurrentResolution api from DisplaySettings and verify it with getCurrentResolutions for a minimum of 1000 times</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1.wpeframework should be up and running
2. Display should be connected</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>set_resolution_max_count:integer</input_parameters>
    <automation_approch>1. Activate DisplaySettings and DeviceInfo plugins
2. Get the connected video displays list
3. Get the current resolution for the first display in the previous list
4. Get the supported resolutions for the display
5. In a loop of min 1000:
a) Set and get each supported resolution
b) Validate resource usage
6. Revert the resolution
7. Revert the status of plugins</automation_approch>
    <expected_output>Device should be stable after each iteration</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_DisplaySettings_SetandGetResolution</test_script>
    <skipped>No</skipped>
    <release_version>M95</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
import StabilityTestVariables
import json
import ast
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_DisplaySettings_SetandGetResolution')

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}{}_{}_{}_CPUMemoryInfo.json'.format(obj.logpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    status = "SUCCESS"
    revert="NO"
    value = {}
    plugins_list = ["org.rdk.DisplaySettings","DeviceInfo"]
    sleep_time = StabilityTestVariables.set_resolution_sleep_time
    max_iterations = StabilityTestVariables.set_resolution_max_count
    print "\n Check Pre conditions"
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    plugin_status_needed = {"org.rdk.DisplaySettings":"activated","DeviceInfo":"activated"}
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
    if status == "SUCCESS":
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
                supported_resolutions = tdkTestObj.getResultDetails()
                supported_resolutions = ast.literal_eval(supported_resolutions)
                supported_resolutions = supported_resolutions["supportedResolutions"]
                print "\n Supported resolutions for {} display: {}".format(connected_displays[0],supported_resolutions)
                for count in range(0,max_iterations):
                    result_dict = {}
                    params = {}
                    params["videoDisplay"] = connected_displays[0]
                    resolution = supported_resolutions[count % len(supported_resolutions)]
                    params["resolution"] = resolution
                    params["persist"] = False
                    input_params = json.dumps(params)
                    print "\n Set resolution to :",resolution
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.setCurrentResolution")
                    tdkTestObj.addParameter("value",input_params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if result == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                        time.sleep(sleep_time)
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
                            print "\n Validate Resource usage for iteration: {}".format(count+1)
                            tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                            tdkTestObj.executeTestCase(expectedResult)
                            resource_usage = tdkTestObj.getResultDetails()
                            result = tdkTestObj.getResult()
                            if expectedResult in result and resource_usage != "ERROR":
                                tdkTestObj.setResultStatus("SUCCESS")
                                cpuload = resource_usage.split(',')[0]
                                memory_usage = resource_usage.split(',')[1]
                                result_dict["iteration"] = count+1
                                result_dict["cpu_load"] = float(cpuload)
                                result_dict["memory_usage"] = float(memory_usage)
                                result_dict_list.append(result_dict)
                            else:
                                print "\n Error while validating Resource usage"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            print "\n Unable to set current resolution to: ",resolution
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        print "\n Error while setting the current resolution for videodisplay: ",connected_displays[0]
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                else:
                    print "\n Successfully completed {} iterations".format(max_iterations)
                cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                json.dump(cpu_mem_info_dict,json_file)
                json_file.close()
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
                print "\n Error while checking current resolution"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while checking connected video displays, details:",connected_displays
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Preconditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
