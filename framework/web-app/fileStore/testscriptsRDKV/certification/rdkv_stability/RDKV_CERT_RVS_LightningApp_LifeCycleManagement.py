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
  <name>RDKV_CERT_RVS_LightningApp_LifeCycleManagement</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_executeLifeCycle</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to launch LightningApp plugin then set URL, suspend, resume, move behind and front then destroy. The script will repeat this for a minimum of 1000 times.</synopsis>
  <groups_id/>
  <execution_time>5000</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_STABILITY_39</test_case_id>
    <test_objective>The objective of this test is to launch LightningApp plugin then set URL, suspend, resume, move behind and front then destroy. The script will repeat this for a minimum of 1000 times.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>lifecycle_max_iterations: integer</input_parameters>
    <automation_approch>In a loop of 1000 :
1. Launch plugin using launch method of RDKShell.
2. Set given URL using LightningApp.1.url method.
3.  Validate whether URL is set using above method itself.
4. Suspend the plugin using suspend method of RDKShell
5. Resume the plugin using resume method of RDKShell
6. Move the plugin to back using moveToBack method of RDKShell
7. Move the plugin to front using moveToFront method of RDKShell
8. Deactivate the plugin using destroy method of RDKShell.
9. Validate the CPU load and memory usage using DeviceInfo.1.systeminfo method
</automation_approch>
    <expected_output>Device should be stable after completing a lifecycle. CPU load and memory usage must be within the limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_LightningApp_LifeCycleManagement</test_script>
    <skipped>No</skipped>
    <release_version>M90</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import StabilityTestVariables
import json
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_LightningApp_LifeCycleManagement');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
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
if expectedResult in (result.upper() and pre_condition_status) :
    status = "SUCCESS"
    revert="NO"
    max_iterations = StabilityTestVariables.lifecycle_max_count
    lightning_app_test_url = obj.url+'/fileStore/lightning-apps/VideoResizeTest.html'
    if lightning_app_test_url == "":
        print "\n Please configure the lightning_app_test_url in Config file"
    plugins_list = ["LightningApp","DeviceInfo"]
    print "\n Check Pre conditions"
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    plugin_status_needed = {"LightningApp":"deactivated","DeviceInfo":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS":
        plugin = "LightningApp"
        print "\n Preconditions are set successfully"
        plugin_operations_list = []
        plugin_validation_details = ["LightningApp.1.url",lightning_app_test_url]
        plugin_operations_list.append({plugin_validation_details[0]:plugin_validation_details[1]})
        plugin_validation_details = json.dumps(plugin_validation_details)
        plugin_operations = json.dumps(plugin_operations_list)
        for count in range(0,max_iterations):
            result_dict = {}
            tdkTestObj = obj.createTestStep('rdkservice_executeLifeCycle')
            tdkTestObj.addParameter("plugin",plugin)
            tdkTestObj.addParameter("operations",plugin_operations)
            tdkTestObj.addParameter("validation_details",plugin_validation_details)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            details = tdkTestObj.getResultDetails();
            if expectedResult in result and details == "SUCCESS" :
                print "\n Successfully completed lifecycle"
                tdkTestObj.setResultStatus("SUCCESS")
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
            else:
                print "\n Error while executing life cycle methods"
                tdkTestObj.setResultStatus("FAILURE")
                break
        else:
            print "\n Successfully Completed {} iterations".format(max_iterations)
        cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
        json.dump(cpu_mem_info_dict,json_file)
        json_file.close()
    else:
        print "\n Preconditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
