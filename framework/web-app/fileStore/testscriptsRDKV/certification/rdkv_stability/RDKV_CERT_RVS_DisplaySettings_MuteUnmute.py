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
  <version>2</version>
  <name>RDKV_CERT_RVS_DisplaySettings_MuteUnmute</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateResourceUsage</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to mute and unmute the DUT for a minimum of 1000 times.</synopsis>
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
    <test_case_id>RDKV_STABILITY_59</test_case_id>
    <test_objective>The objective of this test is to mute and unmute the DUT for a minimum of 1000 times.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1.wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>mute_unmute_max_count: integer</input_parameters>
    <automation_approch>1. Activate DisplaySettings and DeviceInfo plugins
2. In a loop of min 1000,
a) Mute the DUT using setMuted method
b) Verify using getMuted method
c) Unmute the DUT using setMuted method
d) Verify using getMuted method
3) Validate the resource usage using DeviceInfo plugin
4) Revert the status of plugins</automation_approch>
    <expected_output>Mute and unmute should be success in all iterations</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_DisplaySettings_MuteUnmute</test_script>
    <skipped>No</skipped>
    <release_version>M95</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
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
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_DisplaySettings_MuteUnmute')

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
    error_in_loop = False
    max_iterations = StabilityTestVariables.mute_unmute_max_count
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
            print "\n Starting mute and unmute operations for audioport: ",connected_ports[0]
            for count in range(0,max_iterations):
                result_dict = {}
                params = {}
                value = {}
                for muted in [True,False]:
                    params["audioPort"] = connected_ports[0]
                    params["muted"] = muted
                    input_params = json.dumps(params)
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.setMuted")
                    tdkTestObj.addParameter("value",input_params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if result == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                        time.sleep(5)
                        value["audioPort"] = connected_ports[0]
                        get_params = json.dumps(value)
                        tdkTestObj = obj.createTestStep('rdkservice_getValueWithParams')
                        tdkTestObj.addParameter("method","org.rdk.DisplaySettings.1.getMuted")
                        tdkTestObj.addParameter("params",get_params)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        muted_info = tdkTestObj.getResultDetails()
                        muted_info = ast.literal_eval(muted_info)
                        muted_val = muted_info["muted"]
                        if result == "SUCCESS" and  muted_val == muted:
                            print "\n Successfully set muted: ",muted_val
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\n Error while setting muted: ",muted
                            tdkTestObj.setResultStatus("FAILURE")
                            error_in_loop = True
                            break
                    else:
                        print "\n Error while muting the HDMI0 port"
                        tdkTestObj.setResultStatus("FAILURE")
                        error_in_loop = True
                        break
                else:
                    print "\n Successfully muted and unmuted {} port".format(connected_ports[0])
                    #Validate resource usage
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
                if error_in_loop:
                    print "\n Stopping the test"
                    break
            else:
                print "\n Successfully completed {} iterations".format(max_iterations)
            cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
            json.dump(cpu_mem_info_dict,json_file)
            json_file.close()
        else:
            print "\n Error while checking connected audio ports, list of connected auidoports: ",connected_ports
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
