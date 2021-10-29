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
  <name>RDKV_CERT_RVS_HtmlApp_LoadURL_OnStressLaunch</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateResourceUsage</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to launch and exit HtmlApp for 99 times. On 100th time load HtmlApp and verify if the load URL is happening properly.</synopsis>
  <groups_id/>
  <execution_time>120</execution_time>
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
    <test_case_id>RDKV_STABILITY_54</test_case_id>
    <test_objective>The objective of this test is to launch and exit HtmlApp for 99 times. On 100th time load HtmlApp and verify if the load URL is happening properly.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>html_page_url:string</input_parameters>
    <automation_approch>In a loop of 99 :
1. Launch HtmlApp using RDKShell.
2. Check the status
3. Destroy the plugin using RDKShell
4. Check the status
5. Validate the resource usage DeviceInfo.1.systeminfo method
After successful completion of above steps for 99 times, do below steps:
6. Launch HtmlApp using RDKShell.
7. Check the status
8. Set a URL
9. Validate whether the URL is set
10. Destroy the plugin
</automation_approch>
    <expected_output>DUT should be stable after each iteration and resource usage must be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_HtmlApp_LoadURL_OnStressLaunch</test_script>
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
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_HtmlApp_LoadURL_OnStressLaunch')

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
    max_iterations = 99
    htmlapp_test_url = StabilityTestVariables.html_page_url
    if htmlapp_test_url == "":
        print "\n Please configure the htmlapp_test_url in StabilityTestVariables file"
    plugins_list = ["HtmlApp","Cobalt","DeviceInfo","WebKitBrowser"]
    htmlapp_post_condition = {"HtmlApp":"deactivated"}
    print "\n Check Pre conditions"
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    plugin_status_needed = {"HtmlApp":"deactivated","Cobalt":"deactivated","DeviceInfo":"activated","WebKitBrowser":"deactivated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS" and htmlapp_test_url != "":
        print "\n Preconditions are set successfully"
        plugin = "HtmlApp"
        plugin_operations_list = []
        plugin_validation_details = ["HtmlApp.1.url",htmlapp_test_url]
        plugin_operations_list.append({plugin_validation_details[0]:plugin_validation_details[1]})
        plugin_validation_details = json.dumps(plugin_validation_details)
        plugin_operations = json.dumps(plugin_operations_list)
        for count in range(0,max_iterations):
            result_dict = {}
            tdkTestObj = obj.createTestStep('rdkservice_launchAndDestroy')
            tdkTestObj.addParameter("plugin",plugin)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            details = tdkTestObj.getResultDetails();
            if expectedResult in result and details == "SUCCESS" :
                print "\n Successfully completed launch and destroy of {}".format(plugin)
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
                print "\n Error while doing launch and destroy of {} plugin".format(plugin)
                tdkTestObj.setResultStatus("FAILURE")
                break
        else:
            print "\n Successfully Completed {} iterations".format(max_iterations)
            tdkTestObj = obj.createTestStep('rdkservice_validatePluginFunctionality')
            tdkTestObj.addParameter("plugin",plugin)
            tdkTestObj.addParameter("operations",plugin_operations)
            tdkTestObj.addParameter("validation_details",plugin_validation_details)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            details = tdkTestObj.getResultDetails();
            if expectedResult in result and details == "SUCCESS" :
                print "\n Successfully verified load URL"
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "\n Error while validating load URL in HtmlApp"
                tdkTestObj.setResultStatus("FAILURE")
        cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
        json.dump(cpu_mem_info_dict,json_file)
        json_file.close()
        status = set_plugins_status(obj,htmlapp_post_condition)
        time.sleep(10)
        status_dict = get_plugins_status(obj,[plugin])
        if status_dict and status_dict[plugin] in 'deactivated':
            print "\n Successfully deactivated HtmlApp"
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "\n Unable to deactivate HtmlApp, current status: ",status_dict[plugin]
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
