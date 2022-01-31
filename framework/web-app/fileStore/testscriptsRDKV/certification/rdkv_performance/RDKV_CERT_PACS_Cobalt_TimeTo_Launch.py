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
  <name>RDKV_CERT_PACS_Cobalt_TimeTo_Launch</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken to launch Cobalt</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_36</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to launch Cobalt</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. Time in Test Manager and DUT should be in sync with UTC</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Register for onLaunch event of RDKShell.
2. Save current system time and launch Cobalt using RDKShell.
3. Get the time from triggered event
4. Validate the output with threshold value</automation_approch>
    <expected_output>Cobalt should be launched and time taken to launch Cobalt should be within the expected limit.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_TimeTo_Launch</test_script>
    <skipped>No</skipped>
    <release_version>M88</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import PerformanceTestVariables
from StabilityTestUtility import * 
from web_socket_util import *
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_TimeTo_Launch');
#Execution summary variable 
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    event_listener = None
    thunder_port = PerformanceTestVariables.thunder_port
    status = "SUCCESS"
    revert = "NO"
    plugins_list = ["Cobalt","WebKitBrowser"]
    plugin_status_needed = {"Cobalt":"deactivated","WebKitBrowser":"deactivated"}
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        new_status_dict = get_plugins_status(obj,plugins_list)
        if new_status_dict != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS":
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 6,"method": "org.rdk.RDKShell.1.register","params": {"event": "onLaunched", "id": "client.events.1" }}'],"/jsonrpc",False)
        time.sleep(5)
        launch_status,launch_start_time = launch_plugin(obj,"Cobalt")
        if launch_status == expectedResult:
            time.sleep(5)
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","Cobalt")
            tdkTestObj.executeTestCase(expectedResult)
            cobalt_status = tdkTestObj.getResultDetails()
            result = tdkTestObj.getResult()
            if cobalt_status == 'resumed' and expectedResult in result:
                print "\nCobalt Resumed Successfully\n"
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(10)
                continue_count = 0
                launched_time = ""
                while True:
                    if (continue_count > 60):
                        break
                    if (len(event_listener.getEventsBuffer())== 0):
                        continue_count += 1
                        time.sleep(1)
                        continue
                    event_log = event_listener.getEventsBuffer().pop(0)
                    print "\n Triggered event: ",event_log,"\n"
                    if ("Cobalt" in event_log and "onLaunched" in str(event_log)):
                        print "\n Event :onLaunched is triggered during Cobalt launch \n"
                        launched_time = event_log.split('$$$')[0]
                        break
                if launched_time:
                    conf_file,file_status = getConfigFileName(obj.realpath)
                    config_status,cobalt_launch_threshold = getDeviceConfigKeyValue(conf_file,"COBALT_LAUNCH_THRESHOLD_VALUE")
                    Summ_list.append('COBALT_LAUNCH_THRESHOLD_VALUE :{}ms'.format(cobalt_launch_threshold))
                    offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                    Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
                    if all(value != "" for value in (cobalt_launch_threshold,offset)):
                        launch_start_time_in_millisec = getTimeInMilliSec(launch_start_time)
                        launched_time_in_millisec = getTimeInMilliSec(launched_time)
                        print "\n Cobalt launch initiated at: ",launch_start_time
                        Summ_list.append('Cobalt launch initiated at :{}'.format(launch_start_time))
                        print "\n Cobalt launched at : ",launched_time
                        Summ_list.append('Cobalt launched at :{}'.format(launched_time))
                        time_taken_for_launch = launched_time_in_millisec - launch_start_time_in_millisec
                        print "\n Time taken to launch Cobalt: {}(ms)".format(time_taken_for_launch)
                        Summ_list.append(' Time taken to launch Cobalt:{}ms'.format(time_taken_for_launch))
                        print "\n Threshold value for time taken to launch Cobalt: {} ms".format(cobalt_launch_threshold)
                        print "\n Validate the time: \n"
                        if 0 < time_taken_for_launch < (int(cobalt_launch_threshold) + int(offset)) :
                            print "\n Time taken for launching Cobalt is within the expected range \n"
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\n Time taken for launching Cobalt is not within the expected range \n"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Please configure the Threshold value in device configuration file \n"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n onLaunched event not triggered for during Cobalt launch\n"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while checking Cobalt status \n"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while launching Cobalt \n"
            obj.setLoadModuleStatus("FAILURE")
         #Deactivate cobalt
        print "\n Exiting from Cobalt \n"
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

        event_listener.disconnect()
        getSummary(Summ_list)
        time.sleep(10)
    else:
        print "\n Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
