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
  <name>RdkService_PremiumApp_Launch_Cobalt</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this script is to get the CPU and memory when launching Cobalt</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_19</test_case_id>
    <test_objective>The objective of this script is to validate the CPU and memory when launching Cobalt</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework process must be running in the DUT.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. As a prerequisite disable all plugins.
2. launch cobalt using RDKShell
3. Validate CPU load and memory usage.</automation_approch>
    <expected_output>Cobalt should launch and CPU load and memory usage must be within the expected range.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RdkService_PremiumApp_Launch_Cobalt</test_script>
    <skipped>No</skipped>
    <release_version>M84</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *


#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RdkService_PremiumApp_Launch_Cobalt');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated","DeviceInfo":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
    cobal_launch_status = launch_cobalt(obj)
    if status == "SUCCESS" and cobal_launch_status == "SUCCESS":
        time.sleep(10)
        print "\n Cobalt is launched \n "
        #get the cpu load
        tdkTestObj = obj.createTestStep('rdkservice_getCPULoad')
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        cpuload = tdkTestObj.getResultDetails()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
            #validate the cpuload
            tdkTestObj = obj.createTestStep('rdkservice_validateCPULoad')
            tdkTestObj.addParameter('value',float(cpuload))
            tdkTestObj.addParameter('threshold',90.0)
            tdkTestObj.executeTestCase(expectedResult)
            is_high_cpuload = tdkTestObj.getResultDetails()
            if is_high_cpuload == "YES" :
                print "\n cpu load is high :{}%".format(cpuload)
                tdkTestObj.setResultStatus("FAILURE")
            else:
                tdkTestObj.setResultStatus("SUCCESS")
                print "\n cpu load : {}%\n".format(cpuload)
        else:
            print "Unable to get cpuload"
            tdkTestObj.setResultStatus("FAILURE")
        #get the memory usage
        tdkTestObj = obj.createTestStep('rdkservice_getMemoryUsage')
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        memory_usage = tdkTestObj.getResultDetails()
        if (result == "SUCCESS"):
            tdkTestObj.setResultStatus("SUCCESS")
            #validate memory usage
            tdkTestObj = obj.createTestStep('rdkservice_validateMemoryUsage')
            tdkTestObj.addParameter('value',float(memory_usage))
            tdkTestObj.addParameter('threshold',90.0)
            tdkTestObj.executeTestCase(expectedResult)
            is_high_memory_usage = tdkTestObj.getResultDetails()
            if is_high_memory_usage == "YES":
                print "\nmemory usage is high :{}%\n".format(memory_usage)
                tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\nmemory usage :{}%\n".format(memory_usage)
                tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "\n Unable to get the memory usage\n"
            tdkTestObj.setResultStatus("FAILURE")
        #Deactivate cobalt
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
        tdkTestObj.addParameter("plugin","Cobalt")
        tdkTestObj.addParameter("status","deactivate")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "Unable to deactivate Cobalt"
            tdkTestObj.setResultStatus("FAILURE")
    elif cobal_launch_status != "SUCCESS":
        print "Unable to launch cobalt"
        obj.setLoadModuleStatus("FAILURE")
    else:
        print "Preconditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "\n Revert the values before exiting \n"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

