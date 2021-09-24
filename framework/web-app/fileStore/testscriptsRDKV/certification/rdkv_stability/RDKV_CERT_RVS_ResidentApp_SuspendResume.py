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
  <name>RDKV_CERT_RVS_ResidentApp_SuspendResume</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateResourceUsage</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to suspend and resume ResidentApp for a minimum of 1000 times</synopsis>
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
    <test_case_id>RDKV_STABILITY_46</test_case_id>
    <test_objective>The objective of this test is to suspend and resume ResidentApp for a minimum of 1000 times</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>suspend_resume_max_count:integer</input_parameters>
    <automation_approch>1. Get the current URL in ResidentApp.
In a loop of 1000:
2. Suspend ResidentApp using org.rdk.RDKShell.1.suspend method
3. Check the status of ResidentApp
4. Resume ResidentApp plugin using org.rdk.RDKShell.1.launch method
5. Check the status of ResidentApp
6. Validate the resource usage using DeviceInfo.1.systemInfo</automation_approch>
    <expected_output>Device should be stable after each iteration and resource usage must be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_ResidentApp_SuspendResume</test_script>
    <skipped>No</skipped>
    <release_version>M93</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
import StabilityTestVariables
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_ResidentApp_SuspendResume');
#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}{}_{}_{}_CPUMemoryInfo.json'.format(obj.logpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}
max_count = StabilityTestVariables.suspend_resume_max_count

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

obj.setLoadModuleStatus(result)

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status = "SUCCESS"
    plugin = "ResidentApp"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo","ResidentApp"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    if curr_plugins_status_dict[plugin] in ("resumed","activated"):
        #Get the ResidentApp url
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","ResidentApp.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        ui_app_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult()
        if ui_app_url and result == "SUCCESS" :
            tdkTestObj.setResultStatus("SUCCESS")
            plugins_list.remove(plugin)
            curr_plugins_status_dict.pop(plugin)
            plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated","DeviceInfo":"activated"}
            if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
                print "\n Error while getting the status of plugins"
                status = "FAILURE"
            elif curr_plugins_status_dict != plugin_status_needed:
                revert = "YES"
                status = set_plugins_status(obj,plugin_status_needed)
                time.sleep(10)
                new_plugins_status = get_plugins_status(obj,plugins_list)
                if new_plugins_status != plugin_status_needed:
                    print "\n Error while setting plugin status"
                    status = "FAILURE"
        else:
            print "\n Error while getting current URL in ResidentApp"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n ResidentApp is not in activated/resumed state"
        status = "FAILURE"
    if status == "SUCCESS":
        print "\nPre conditions for the test are set successfully"
        time.sleep(10)
        for count in range(0,max_count): 
            suspend_status,start_suspend = suspend_plugin(obj,plugin)
            if suspend_status == expectedResult:
                time.sleep(5)
                tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                tdkTestObj.addParameter("plugin",plugin)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                residentapp_status = tdkTestObj.getResultDetails()
                if residentapp_status == 'suspended' and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print "\nResidentApp plugin Suspended Successfully"
                    time.sleep(5)
                    resume_status,start_resume = launch_plugin(obj,plugin,ui_app_url)
                    if resume_status == expectedResult:
                        time.sleep(10)
                        tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                        tdkTestObj.addParameter("plugin",plugin)
                        tdkTestObj.executeTestCase(expectedResult)
                        residentapp_status = tdkTestObj.getResultDetails()
                        result = tdkTestObj.getResult()
                        if residentapp_status == 'resumed' and expectedResult in result:
                            print "\nResidentApp plugin Resumed Successfully\n"
                            tdkTestObj.setResultStatus("SUCCESS")
                            result_dict = {}
                            print "\n ##### Validating CPU load and memory usage #####\n"
                            print "Iteration : ", count + 1
                            tdkTestObj = obj.createTestStep('rdkservice_validateResourceUsage')
                            tdkTestObj.executeTestCase(expectedResult)
                            status = tdkTestObj.getResult()
                            result = tdkTestObj.getResultDetails()
                            if expectedResult in status and result != "ERROR":
                                tdkTestObj.setResultStatus("SUCCESS")
                                cpuload = result.split(',')[0]
                                memory_usage = result.split(',')[1]
                                result_dict["iteration"] = count + 1
                                result_dict["cpu_load"] = float(cpuload)
                                result_dict["memory_usage"] = float(memory_usage)
                                result_dict_list.append(result_dict)
                            else:
                                print "\n Error while validating Resource usage"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            print "ResidentApp plugin is not in Resumed state, current ResidentApp Status: ",residentapp_status
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        print "Unable to set ResidentApp plugin to resumed state"
                        break
                else:
                    print "ResidentApp is not in Suspended state, current ResidentApp Status: ",residentapp_status
                    tdkTestObj.setResultStatus("FAILURE")
                    break
            else:
                print "Unable to set ResidentApp plugin to suspended state"
                break
        else:
            print "\n Successfully completed the {} iterations\n".format(max_count)
        cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
        json.dump(cpu_mem_info_dict,json_file)
        json_file.close()
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
