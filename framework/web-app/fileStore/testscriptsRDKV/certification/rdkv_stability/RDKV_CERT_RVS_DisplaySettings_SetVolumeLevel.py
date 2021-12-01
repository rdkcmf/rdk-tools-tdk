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
  <name>RDKV_CERT_RVS_DisplaySettings_SetVolumeLevel</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateResourceUsage</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to continuously change the volume level for a minimum of 1000 times.</synopsis>
  <groups_id/>
  <execution_time>600</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Emulator-HYB</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>RPI-Client</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_STABILITY_61</test_case_id>
    <test_objective>The objective of this test is to continuously change the volume level for a minimum of 1000 times.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1.wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>set_volumelevel_max_count:integer</input_parameters>
    <automation_approch>1. Activate DisplaySettings and DeviceInfo plugins
2. Get the connected audio ports list
3. Get the current volume level for the first port in the previous list
4. In a loop of min 1000:
a) Set a volume level within 0-100
b) Get the volume level and check
c) Validate resource usage
5. Revert the volume level
6. Revert the status of plugins</automation_approch>
    <expected_output>Device should be stable after each iteration</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_DisplaySettings_SetVolumeLevel</test_script>
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
from random import randrange

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_DisplaySettings_SetVolumeLevel');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}{}_{}_{}_CPUMemoryInfo.json'.format(obj.logpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    status = "SUCCESS"
    revert="NO"
    value = {}
    max_iterations = StabilityTestVariables.set_volumelevel_max_count
    plugins_list = ["org.rdk.DisplaySettings","DeviceInfo"]
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
        tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.getConnectedAudioPorts")
        tdkTestObj.addParameter("reqValue","connectedAudioPorts")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        connected_ports = tdkTestObj.getResultDetails()
        connected_ports = ast.literal_eval(connected_ports)
        if connected_ports and result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
            print "\n Get volume level for ",connected_ports[0]
            value["audioPort"] = connected_ports[0]
            get_params = json.dumps(value)
            tdkTestObj = obj.createTestStep('rdkservice_getValueWithParams')
            tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.getVolumeLevel")
            tdkTestObj.addParameter("params",get_params)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            initial_vol_level = tdkTestObj.getResultDetails()
            initial_vol_level = ast.literal_eval(initial_vol_level)
            initial_vol_level = initial_vol_level["volumeLevel"]
            if result == "SUCCESS":
                print "\n Initial volume level for {} port :{}".format(connected_ports[0],initial_vol_level)
                print "\n Starting set and get volume level test for {} port".format(connected_ports[0])
                for count in range(0,max_iterations):
                    result_dict = {}
                    params = {}
                    #Generate random number between 0 and 100 (inclusive both)
                    volume = randrange(100)
                    params["audioPort"] = connected_ports[0]
                    params["volumeLevel"] = volume
                    input_params = json.dumps(params)
                    print "\n Set volume level to :",volume
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.setVolumeLevel")
                    tdkTestObj.addParameter("value",input_params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if result == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                        time.sleep(5)
                        tdkTestObj = obj.createTestStep('rdkservice_getValueWithParams')
                        tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.getVolumeLevel")
                        tdkTestObj.addParameter("params",get_params)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        volume_info = tdkTestObj.getResultDetails()
                        volume_info = ast.literal_eval(volume_info)
                        volume_level = volume_info["volumeLevel"]
                        if result == "SUCCESS" and  int(float(volume_level)) == volume:
                            print "\n Successfully set volume level to: ",volume_level
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
                                result_dict["iteration"] = count + 1
                                result_dict["cpu_load"] = float(cpuload)
                                result_dict["memory_usage"] = float(memory_usage)
                                result_dict_list.append(result_dict)
                            else:
                                print "\n Error while validating Resource usage"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            print "\n Error while setting volume to: ",volume
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        print "\n Error while muting the {} port".format(connected_ports[0])
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                else:
                    print "\n Successfully completed {} iterations".format(max_iterations)
                cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                json.dump(cpu_mem_info_dict,json_file)
                json_file.close()
                params = {}
                params["audioPort"] = connected_ports[0]
                params["volumeLevel"] = int(float(initial_vol_level))
                input_params = json.dumps(params)
                print "\n Revert volume level to :",initial_vol_level
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.setVolumeLevel")
                tdkTestObj.addParameter("value",input_params)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if result == "SUCCESS":
                    print "\n Successfully reverted volume level"
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print "\n Error while reverting the volume level"
                    tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while checking connected audio ports, details:",connected_ports
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
