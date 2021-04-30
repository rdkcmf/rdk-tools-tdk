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
  <name>RDKV_CERT_PACS_AmazonPrime_TimeTo_Launch</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken to launch Amazon Prime</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_39</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to launch Amazon Prime</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Listen for onLaunched event of RDKShell
2. Save current system time and launch Amazon plugin
3. Parse the time stamp from event print and calculate output by comparing the value with initial system time
4. Validate the time with threshold time.</automation_approch>
    <expected_output>The time taken to launch must be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_AmazonPrime_TimeTo_Launch</test_script>
    <skipped>No</skipped>
    <release_version>M88</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
from web_socket_util import *
from rdkv_performancelib import *
import PerformanceTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_AmazonPrime_TimeTo_Launch');

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
    plugin = "Amazon"
    revert = "NO"
    plugins_list = ["Amazon","WebKitBrowser","Cobalt"]
    plugin_status_needed = {"Amazon":"deactivated","WebKitBrowser":"deactivated","Cobalt":"deactivated"}
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
        launch_status,launch_start_time = launch_plugin(obj,"Amazon")
        if launch_status == expectedResult:
            time.sleep(5)
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","Amazon")
            tdkTestObj.executeTestCase(expectedResult)
            amazon_status = tdkTestObj.getResultDetails()
            result = tdkTestObj.getResult()
            if amazon_status == 'resumed' and expectedResult in result:
                print "\nAmazon Resumed Successfully\n"
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
                    if ("Amazon" in event_log):
                        print "\n Event :onLaunched is triggered during Amazon launch \n"
                        launched_time = event_log.split('$$$')[0]
                        break
                if launched_time:
                    conf_file,file_status = getConfigFileName(obj.realpath)
                    config_status,amazon_launch_threshold = getDeviceConfigKeyValue(conf_file,"AMAZON_LAUNCH_THRESHOLD_VALUE")
                    offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                    if all(value != "" for value in (amazon_launch_threshold,offset)):
                        launch_start_time_in_millisec = getTimeInMilliSec(launch_start_time)
                        launched_time_in_millisec = getTimeInMilliSec(launched_time)
                        print "\n Amazon launch initiated at: " + launch_start_time + "(UTC)"
                        print "\n Amazon launched at : "+ launched_time + "(UTC)"
                        time_taken_for_launch = launched_time_in_millisec - launch_start_time_in_millisec
                        print "\n Time taken to launch Amazon: {}(ms)".format(time_taken_for_launch)
                        print "\n Validate the time: \n"
                        if 0 < time_taken_for_launch < (int(amazon_launch_threshold) + int(offset)) :
                            print "\n Time taken for launching Amazon is within the expected range \n"
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\n Time taken for launching Amazon is not within the expected range \n"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Please configure the Threshold value in device configuration file \n"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n onLaunched event not triggered for during Amazon launch\n"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while checking Amazon status \n"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while launching Amazon \n"
        #Deactivate amazon
        print "\n Exiting from Amazon \n"
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
        tdkTestObj.addParameter("plugin",plugin)
        tdkTestObj.addParameter("status","Amazon")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "Unable to deactivate Amazon"
            tdkTestObj.setResultStatus("FAILURE")
        event_listener.disconnect()
        time.sleep(5)
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
