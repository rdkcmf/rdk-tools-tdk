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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_RVS_RDKShell_ActivateDeactivate</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to activate and deactivate RDKShell plugin for given number of times and validate CPU load and memory usage in each iteration.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>660</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_STABILITY_16</test_case_id>
    <test_objective>The objective of this test is to activate and deactivate RDKShell plugin for given number of times and validate CPU load and memory usage in each iteration.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>activate_deactivate_max_count:integer</input_parameters>
    <automation_approch>1. Activate and deactivate RDKShell using controller plugin for given number of times.
2. Get the CPU and memory usage and validate the same.
3. Revert everything.</automation_approch>
    <expected_output>The device must be stable after the complete execution.
CPU load and memory usage must be within the expected limit.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_RDKShell_ActivateDeactivate</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from rdkv_performancelib import *
from StabilityTestUtility import *
import StabilityTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_RDKShell_ActivateDeactivate');

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
    activate_deactivate_max_count = StabilityTestVariables.activate_deactivate_max_count
    plugin = "org.rdk.RDKShell"
    revert = "NO"
    status = "SUCCESS"
    plugins_list = ["org.rdk.RDKShell","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    if all(curr_plugins_status_dict[plugin] != "FAILURE" for plugin in plugins_list):
        if curr_plugins_status_dict["DeviceInfo"] != "activated":
            revert = "YES"
            device_info_plugin = "DeviceInfo"
            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus');
            tdkTestObj.addParameter("plugin",device_info_plugin);
            tdkTestObj.addParameter("status","activate");
            tdkTestObj.executeTestCase(expectedResult);
            result1 = tdkTestObj.getResult();
            if expectedResult in result1:
                print "\n Deviceinfo is activated \n"
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "\n Error while activating DeviceInfo\n"
                tdkTestObj.setResultStatus("FAILURE")
                status = "FAILURE"
        else:
            print "\n DeviceInfo is activated"
    else:
        print "\n Unable to get plugins status"
        status = "FAILURE"
    if status == "SUCCESS":
        error_in_loop = False
        plugin_status = curr_plugins_status_dict[plugin]
        for count in range(0,activate_deactivate_max_count):
            print "\n########## Iteration :{} ##########\n".format(count+1)
            result_dict = {}
            for inner_count in range (0,2):
                if plugin_status == "activated":
                    new_status = "deactivate"
                    expected_status = "deactivated"
                else:
                    new_status = "activate"
                    expected_status = "activated"
                print "\n Setting {} plugin to {} \n".format(plugin,new_status)
                tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
                tdkTestObj.addParameter("plugin",plugin)
                tdkTestObj.addParameter("status",new_status)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if result == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                    time.sleep(5)
                    #check status
                    print "\n Checking current status of {} plugin \n".format(plugin)
                    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                    tdkTestObj.addParameter("plugin",plugin)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if result == "SUCCESS":
                        plugin_status = tdkTestObj.getResultDetails()
                        print "\n Current status of {} plugin : {}\n".format(plugin,plugin_status)
                        if plugin_status in expected_status:
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "{} Status not set to {} , current status: {}".format(plugin,new_status,plugin_status)
                            tdkTestObj.setResultStatus("FAILURE")
                            error_in_loop = True
                            break
                    else:
                        print "Error while getting {} plugin status".format(plugin)
                        tdkTestObj.setResultStatus("FAILURE")
                        error_in_loop = True
                        break
                else:
                    print "Error while setting {} plugin status to {}".format(plugin,new_status)
                    tdkTestObj.setResultStatus("FAILURE")
                    error_in_loop = True
                    break
            if error_in_loop:
                print "\n Stopping the test !!!"
                break
            print "\n##### Inner iterations for  activation and deactivation of plugin completed ##### \n"
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
                break
        else:
            print "\nSuccessfully completed the {} iterations \n".format(activate_deactivate_max_count)
        cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
        json.dump(cpu_mem_info_dict,json_file)
        json_file.close()
    else:
        print "\n Preconditions are not met\n"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES" or plugin_status != curr_plugins_status_dict[plugin] :
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    print "Failed to load module"
    obj.setLoadModuleStatus("FAILURE");
