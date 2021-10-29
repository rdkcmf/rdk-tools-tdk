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
  <name>RDKV_CERT_RVS_Cobalt_Video_Navigation</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateResourceUsage</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to launch Cobalt and Navigate through the tiles for a minimum of 1000 times.</synopsis>
  <groups_id/>
  <execution_time>60</execution_time>
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
    <test_case_id>RDKV_STABILITY_56</test_case_id>
    <test_objective>The objective of this test is to launch Cobalt and Navigate through the tiles for a minimum of 1000 times.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_max_navigations:string</input_parameters>
    <automation_approch>1. Launch Cobalt using RDKShell
2. In a loop of 100:
a) Do 10 key navigations through videos using generateKey method
b) Validate resource usage using DeviceInfo plugin
3. Destroy Cobalt plugin
 </automation_approch>
    <expected_output>Navigations should happen and resource usage must be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_Cobalt_Video_Navigation</test_script>
    <skipped>No</skipped>
    <release_version>M94</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
import StabilityTestVariables
import json
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Cobalt_Video_Navigation')

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}{}_{}_{}_CPUMemoryInfo.json'.format(obj.logpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    status = "SUCCESS"
    revert="NO"
    navigation_key_dictionary = {"ArrowLeft":37,"ArrowUp":38,"ArrowRight":39,"ArrowDown":40}
    keys_list = ["ArrowDown","ArrowRight","ArrowLeft","ArrowDown","ArrowRight","ArrowLeft","ArrowDown","ArrowUp","ArrowUp","ArrowUp"]
    max_navigations = StabilityTestVariables.cobalt_max_navigations
    plugins_list = ["Cobalt","WebKitBrowser","DeviceInfo"]
    print "\n Check Pre conditions"
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    plugin_status_needed = {"Cobalt":"deactivated","WebKitBrowser":"deactivated","DeviceInfo":"activated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            print "\n Error while setting status of plugins"
            status = "FAILURE"
    if status == "SUCCESS":
        plugin = "Cobalt"
        print "\n Preconditions are set successfully"
        generatekey_method = 'org.rdk.RDKShell.1.generateKey'
        cobalt_launch_status = launch_cobalt(obj)
        time.sleep(30)
        if cobalt_launch_status == "SUCCESS":
            print "Set focus to Cobalt"
            client = '{"client": "Cobalt"}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.setFocus")
            tdkTestObj.addParameter("value",client)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                error_in_loop = False
                for count in range(0,max_navigations):
                    result_dict = {}
                    for key in keys_list:
                        params = '{"keys":[ {"keyCode": '+str(navigation_key_dictionary[key])+',"modifiers": [],"delay":1.0}]}'
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method",generatekey_method)
                        tdkTestObj.addParameter("value",params)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        if expectedResult in result:
                            print "\n Pressed {} key".format(key)
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\n Error while pressing {} key ".format(key)
                            tdkTestObj.setResultStatus("FAILURE")
                            error_in_lopp = True
                            break
                    else:
                        print "\n ##### Validating CPU load and memory usage #####\n"
                        print "Iteration : ", count+1
                        tdkTestObj = obj.createTestStep('rdkservice_validateResourceUsage')
                        tdkTestObj.executeTestCase(expectedResult)
                        status = tdkTestObj.getResult()
                        result = tdkTestObj.getResultDetails()
                        if expectedResult in status and result != "ERROR":
                            tdkTestObj.setResultStatus("SUCCESS")
                            cpuload = result.split(',')[0]
                            memory_usage = result.split(',')[1]
                            result_dict["iteration"] = count+1
                            result_dict["cpu_load"] = float(cpuload)
                            result_dict["memory_usage"] = float(memory_usage)
                            result_dict_list.append(result_dict)
                        else:
                            print "\n Error while validating Resource usage"
                            tdkTestObj.setResultStatus("FAILURE")
                            error_in_loop = True
                            break
                    if error_in_loop:
                        print "\n Stopping the test"
                        break
                else:
                    print "\n Successfully completed {} iterations".format(max_navigations)
                cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                json.dump(cpu_mem_info_dict,json_file)
                json_file.close()
            else:
                print "\n Unable to set focus to Cobalt"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Unable to launch Cobalt"
            obj.setLoadModuleStatus("FAILURE")
        #Deactivate cobalt
        print "\n Exiting from Cobalt"
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
        tdkTestObj.addParameter("plugin","Cobalt")
        tdkTestObj.addParameter("status","deactivate")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "\n Unable to deactivate Cobalt"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Preconditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
