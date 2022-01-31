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
  <name>RDKV_CERT_PACS_Cobalt_TimeTo_SuspendResume</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The script is to find the time taken to suspend and resume Cobalt</synopsis>
  <groups_id/>
  <execution_time>8</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_22</test_case_id>
    <test_objective>The script is to find the time taken to suspend and resume Cobalt</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. The time in Test Manager should be in sync with UTC </pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Threshold value of suspending time.
Threshold value of resuming time,</input_parameters>
    <automation_approch>1. Resume the Cobalt plugin.
2. Store the current time in start_resume variable and suspend the plugin using RDKShell.
3. Verify the status.
4. Store the current time in start_resume variable and resume the plugin using RDKShell.
5. Verify the status.
6. Find the corresponding logs and get the timestamps for suspending and resuming the pluginfrom wpeframework log.
7. Calculate the time taken to suspend by finding the difference between start_suspend and timestamp
8. Calculate the time taken to resume by  finding the difference between start_resume and timestamp
9. Verify the time values are within the expected range</automation_approch>
    <expected_output>The time taken should be within expected range of ms.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_TimeTo_SuspendResume</test_script>
    <skipped>No</skipped>
    <release_version>M85</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from rdkv_performancelib import *
from datetime import datetime
from StabilityTestUtility import *
from web_socket_util import *
import PerformanceTestVariables
import json

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_TimeTo_SuspendResume');
#Execution summary variable 
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    event_listener = None
    thunder_port = PerformanceTestVariables.thunder_port
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["Cobalt"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"Cobalt":"resumed"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        plugins_status_dict = get_plugins_status(obj,plugins_list)
        if plugins_status_dict != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS":
        time.sleep(10)
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 5,"method": "org.rdk.RDKShell.1.register","params": {"event": "onSuspended", "id": "client.events.1" }}','{"jsonrpc": "2.0","id": 6,"method": "org.rdk.RDKShell.1.register","params": {"event": "onLaunched", "id": "client.events.1" }}'],"/jsonrpc",False)
        time.sleep(30)
        print "\nPre conditions for the test are set successfully"
        suspended_time = resumed_time = ""
        suspend_status,start_suspend = suspend_plugin(obj,"Cobalt")
        if suspend_status == expectedResult:
            time.sleep(5)
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","Cobalt")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            cobalt_status = tdkTestObj.getResultDetails()
            if cobalt_status == 'suspended' and expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(10)
                print "\nCobalt Suspended Successfully\n"
                resume_status,start_resume = launch_plugin(obj,"Cobalt")
                if resume_status == expectedResult:
                    time.sleep(5)
                    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                    tdkTestObj.addParameter("plugin","Cobalt")
                    tdkTestObj.executeTestCase(expectedResult)
                    cobalt_status = tdkTestObj.getResultDetails()
                    result = tdkTestObj.getResult()
                    if cobalt_status == 'resumed' and expectedResult in result:
                        print "\nCobalt Resumed Successfully\n"
                        tdkTestObj.setResultStatus("SUCCESS")
                        time.sleep(30)
                        if (len(event_listener.getEventsBuffer())!= 0):
                            for event_log in event_listener.getEventsBuffer():
                                json_msg = json.loads(event_log.split('$$$')[1])
                                print json_msg
                                if json_msg["params"]["client"] == "Cobalt":
                                    if "onSuspended" in json_msg["method"] and not suspended_time:
                                        suspended_time = event_log.split('$$$')[0]
                                    elif "onLaunched" in json_msg["method"] and not resumed_time:
                                        resumed_time = event_log.split('$$$')[0]
                            if suspended_time and resumed_time:
                                conf_file,file_status = getConfigFileName(obj.realpath)
                                suspend_config_status,suspend_threshold = getDeviceConfigKeyValue(conf_file,"COBALT_SUSPEND_TIME_THRESHOLD_VALUE")
                                Summ_list.append('COBALT_SUSPEND_TIME_THRESHOLD_VALUE :{}ms'.format(suspend_threshold))
                                resume_config_status,resume_threshold = getDeviceConfigKeyValue(conf_file,"COBALT_RESUME_TIME_THRESHOLD_VALUE")
                                Summ_list.append('COBALT_RESUME_TIME_THRESHOLD_VALUE :{}ms'.format(resume_threshold))
                                offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
                                if all(value != "" for value in (suspend_threshold,resume_threshold,offset)):
                                    start_suspend_in_millisec = getTimeInMilliSec(start_suspend)
                                    suspended_time_in_millisec = getTimeInMilliSec(suspended_time)
                                    print "\n Suspended initiated at: " +start_suspend + "(UTC)"
                                    Summ_list.append('Suspended initiated at :{}'.format(start_suspend))
                                    print "\n Suspended at : "+suspended_time+ "(UTC)"
                                    Summ_list.append('Suspended at :{}'.format(suspended_time))
                                    time_taken_for_suspend = suspended_time_in_millisec - start_suspend_in_millisec
                                    print "\n Time taken to Suspend Cobalt Plugin: " + str(time_taken_for_suspend) + "(ms)"
                                    Summ_list.append('Time taken to Suspend Cobalt Plugin :{}ms'.format(time_taken_for_suspend))
                                    print "\n Threshold value for time taken to suspend Cobalt plugin: " + str(suspend_threshold) + "(ms)"
                                    print "\n Validate the time taken for suspending the plugin \n"
                                    if 0 < time_taken_for_suspend < (int(suspend_threshold) + int(offset)) :
                                        print "\n Time taken for suspending Cobalt plugin is within the expected range \n"
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print "\n Time taken for suspending Cobalt plugin not within the expected range \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                    start_resume_in_millisec = getTimeInMilliSec(start_resume)
                                    resumed_time_in_millisec =  getTimeInMilliSec(resumed_time)
                                    print "\n Resume initiated at: " + start_resume + "(UTC)"
                                    Summ_list.append('Resume initiated at :{}'.format(start_resume))
                                    print "\n Resumed at: " + resumed_time + "(UTC)"
                                    Summ_list.append('Resumed at :{}'.format(resumed_time))
                                    time_taken_for_resume = resumed_time_in_millisec - start_resume_in_millisec
                                    print "\n Time taken to Resume Cobalt Plugin: " + str(time_taken_for_resume) + "(ms)"
                                    Summ_list.append('Time taken to Resume Cobalt Plugin :{}ms'.format(time_taken_for_resume))
                                    print "\n Threshold value for time taken to resume Cobalt plugin: " + str(resume_threshold) + "(ms)"
                                    print "\n Validate the time taken for resuming the plugin \n"
                                    if 0 < time_taken_for_resume < (int(resume_threshold) + int(offset)) :
                                        print "\n Time taken for resuming Cobalt plugin is within the expected range \n"
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print "\n Time taken for resuming Cobalt plugin is not within the expected range \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n Threshold values are not configured in Device configuration file \n"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Suspend and resume related events are not available \n"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n State change events are not triggered \n"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Cobalt is not in Resumed state, current Cobalt Status: ",cobalt_status
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Unable to set Cobalt plugin to resumed state \n"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Cobalt is not in Suspended state, current Cobalt Status: ",cobalt_status
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Unable to set Cobalt plugin to suspended state"
            obj.setLoadModuleStatus("FAILURE")
        event_listener.disconnect()
        time.sleep(30)
    else:
        print "\n Pre conditions are not met \n"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
    getSummary(Summ_list)
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
