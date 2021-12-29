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
  <name>RDKV_CERT_PVS_Functional_LightningApp_TimeTo_SuspendResume</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken to suspend and resume LightningApp plugin.</synopsis>
  <groups_id/>
  <execution_time>4</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_80</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to suspend and resume LightningApp plugin.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. The time in Test Manager should be in sync with UTC </pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Resume the LightningApp plugin.
2. Register for onSuspended and OnLaunched events of RDKShell
3. Store the current time in start_suspend variable and suspend the plugin using RDKShell.
4. Verify the status.
5. Store the current time in start_resume variable and resume the plugin using RDKShell.
6. Verify the status.
7. Find the corresponding events 
8. Calculate the time taken to suspend by finding the difference between start_suspend and timestamp from onSuspended event
9. Calculate the time taken to resume by  finding the difference between start_resume and timestamp from onLaunched event
10. Verify the time values are within the expected range</automation_approch>
    <expected_output>The time taken should be within expected range of ms.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_LightningApp_TimeTo_SuspendResume</test_script>
    <skipped>No</skipped>
    <release_version>M94</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
from rdkv_performancelib import *
from datetime import datetime
from StabilityTestUtility import *
from web_socket_util import *
import PerformanceTestVariables
import json

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_LightningApp_TimeTo_SuspendResume')

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    event_listener = None
    thunder_port = PerformanceTestVariables.thunder_port
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["LightningApp","Cobalt","WebKitBrowser"]
    suspended_time = resumed_time = ""
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    status = "SUCCESS"
    plugin_status_needed = {"LightningApp":"resumed","Cobalt":"deactivated","WebKitBrowser":"deactivated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        plugins_status_dict = get_plugins_status(obj,plugins_list)
        if plugins_status_dict != plugin_status_needed:
            print "\n Unable to set status of plugins"
            status = "FAILURE"
    if status == "SUCCESS" :
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 5,"method": "org.rdk.RDKShell.1.register","params": {"event": "onSuspended", "id": "client.events.1" }}','{"jsonrpc": "2.0","id": 6,"method": "org.rdk.RDKShell.1.register","params": {"event": "onLaunched", "id": "client.events.1" }}'],"/jsonrpc",False)
        time.sleep(30)
        print "\n Pre conditions for the test are set successfully"
        suspend_status,start_suspend = suspend_plugin(obj,"LightningApp")
        time.sleep(10)
        if suspend_status == expectedResult:
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","LightningApp")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            lightningapp_status = tdkTestObj.getResultDetails()
            if lightningapp_status == 'suspended' and expectedResult in result:
                print "\n LightningApp suspended successfully"
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(10)
                resume_status,start_resume = launch_plugin(obj,"LightningApp")
                if resume_status == expectedResult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                    tdkTestObj.addParameter("plugin","LightningApp")
                    tdkTestObj.executeTestCase(expectedResult)
                    lightningapp_status = tdkTestObj.getResultDetails()
                    result = tdkTestObj.getResult()
                    if lightningapp_status == 'resumed' and expectedResult in result:
                        print "\n LightningApp resumed successfully"
                        print "\n Check events triggered "
                        time.sleep(30)
                        if (len(event_listener.getEventsBuffer())!= 0):
                            for event_log in event_listener.getEventsBuffer():
                                json_msg = json.loads(event_log.split('$$$')[1])
                                if json_msg["params"]["client"] == "LightningApp":
                                    if "onSuspended" in json_msg["method"] and not suspended_time:
                                        suspended_time = event_log.split('$$$')[0]
                                    elif "onLaunched" in json_msg["method"] and not resumed_time:
                                        resumed_time = event_log.split('$$$')[0]
                                    print "\n Event: ",event_log.split('$$$')[1]
                            if suspended_time and resumed_time:
                                tdkTestObj.setResultStatus("SUCCESS")
                                conf_file,file_status = getConfigFileName(obj.realpath)
                                suspend_config_status,suspend_threshold = getDeviceConfigKeyValue(conf_file,"LIGHTNINGAPP_SUSPEND_TIME_THRESHOLD_VALUE")
                                resume_config_status,resume_threshold = getDeviceConfigKeyValue(conf_file,"LIGHTNINGAPP_RESUME_TIME_THRESHOLD_VALUE")
                                offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                if all(value != "" for value in (suspend_threshold,resume_threshold,offset)):
                                    start_suspend_in_millisec = getTimeInMilliSec(start_suspend)
                                    suspended_time_in_millisec = getTimeInMilliSec(suspended_time)
                                    print "\n Suspended initiated at: ",start_suspend
                                    print "\n Suspended at : ",suspended_time
                                    time_taken_for_suspend = suspended_time_in_millisec - start_suspend_in_millisec
                                    print "\n Time taken to suspend LightningApp Plugin: " + str(time_taken_for_suspend) + "(ms)"
                                    print "\n Threshold value for time taken to suspend LightningApp plugin: {} ms".format(suspend_threshold)
                                    print "\n Validate the time taken for suspending the plugin"
                                    if 0 < time_taken_for_suspend < (int(suspend_threshold) + int(offset)) :
                                        print "\n Time taken for suspending LightningApp plugin is within the expected range"
                                    else:
                                        print "\n Time taken for suspending LightningApp plugin is greater than the expected range"
                                        tdkTestObj.setResultStatus("FAILURE")
                                    start_resume_in_millisec = getTimeInMilliSec(start_resume)
                                    resumed_time_in_millisec =  getTimeInMilliSec(resumed_time)
                                    print "\n Resume initiated at: ",start_resume
                                    print "\n Resumed at: ",resumed_time
                                    time_taken_for_resume = resumed_time_in_millisec - start_resume_in_millisec
                                    print "\n Time taken to resume LightningApp Plugin: " + str(time_taken_for_resume) + "(ms)"
                                    print "\n Threshold value for time taken to resume LightningApp plugin: {} ms".format(resume_threshold)
                                    print "\n Validate the time taken for resuming the plugin"
                                    if 0 < time_taken_for_resume < (int(resume_threshold) + int(offset)) :
                                        print "\n Time taken for resuming LightningApp plugin is within the expected range"
                                    else:
                                        print "\n Time taken for resuming LightningApp plugin is greater than the expected range"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n Threshold values are not configured in Device configuration file"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Error in suspend and resume events"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n State changed events are not triggered"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n LightningApp is not in resumed state, current LightningApp status: ",lightningapp_status
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Unable to set LightningApp plugin to resumed state"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n LightningApp is not in suspended state, current LightningApp status: ",lightningapp_status
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Unable to set LightningApp plugin to suspended state"
            obj.setLoadModuleStatus("FAILURE")
        event_listener.disconnect()
        time.sleep(30)
    else:
        print "\n Pre conditions are not met \n"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
