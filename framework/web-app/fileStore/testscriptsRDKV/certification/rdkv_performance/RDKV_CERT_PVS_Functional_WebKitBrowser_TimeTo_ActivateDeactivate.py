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
  <version>6</version>
  <name>RDKV_CERT_PVS_Functional_WebKitBrowser_TimeTo_ActivateDeactivate</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to find the time taken for activating and deactivating WebKitPlugin.</synopsis>
  <groups_id/>
  <execution_time>4</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_13</test_case_id>
    <test_objective>The objective of this test is to find the time taken for activating and deactivating the Plugin and check whether the time taken is within the expected range.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. The time in Test Manager should be in sync with UTC </pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Threshold value of activating time.
Threshold value of deactivating time,
</input_parameters>
    <automation_approch>1. Check the current status of plugin
2.a) If it is deactivated, store the current time as start_activate time and activate the plugin.
Verify the status, store the current time as start_deactivate and deactivate the plugin.
b) If it is activated store the current time as start_deactivate time and deactivate the plugin.
Verify the status, store the current time as start_activate and activate the plugin.
3. Find the related logs from wpeframework.log and get the timestamp corresponding to activate and deactivate
4. Find the time taken to activate by finding the difference between timestamp from log and start_activate
5.   Find the time taken to deactivate by finding the difference between timestamp from log and start_deactivate.
6. Verify the time values are within the expected range</automation_approch>
    <expected_output>The time taken should be within expected range of ms.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_WebKitBrowser_TimeTo_ActivateDeactivate</test_script>
    <skipped>No</skipped>
    <release_version>M84</release_version>
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
import PerformanceTestVariables
from web_socket_util import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_WebKitBrowser_TimeTo_ActivateDeactivate')

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
    plugins_list = ["WebKitBrowser"]
    activated_time = ""
    deactivated_time = ""
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugin"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        plugins_status_dict = get_plugins_status(obj,plugins_list)
        if plugins_status_dict != plugin_status_needed:
            print "\n Error while deactivating WebKitBrowser"
            status = "FAILURE"
    if status == "SUCCESS" :
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 5,"method": "org.rdk.RDKShell.1.register","params": {"event": "onLaunched", "id": "client.events.1" }}','{"jsonrpc": "2.0","id": 6,"method": "org.rdk.RDKShell.1.register","params": {"event": "onDestroyed", "id": "client.events.1" }}'],"/jsonrpc",False)
        time.sleep(30)
        print "\nPre conditions for the test are set successfully"
        plugin = "WebKitBrowser"
        launch_status,start_activate = launch_plugin(obj,plugin)
        time.sleep(10)
        if launch_status == expectedResult:
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","WebKitBrowser")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            webkit_status = tdkTestObj.getResultDetails()
            if webkit_status == 'resumed' and expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                print "\nWebKitbrowser resumed successfully\n"
                time.sleep(10)
                tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
                tdkTestObj.addParameter("plugin",plugin)
                tdkTestObj.addParameter("status","deactivate")
                start_deactivate = str(datetime.utcnow()).split()[1]
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if result == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                    tdkTestObj.addParameter("plugin",plugin)
                    tdkTestObj.executeTestCase(expectedResult)
                    webkit_status = tdkTestObj.getResultDetails()
                    result = tdkTestObj.getResult()
                    if webkit_status == 'deactivated' and expectedResult in result:
                        print "\nWebKitbrowser deactivated successfully\n"
                        print "\n Check events triggered \n"
                        time.sleep(30)
                        if (len(event_listener.getEventsBuffer())!= 0):
                            for event_log in event_listener.getEventsBuffer():
                                json_msg = json.loads(event_log.split('$$$')[1])
                                if json_msg["params"]["client"] == plugin:
                                    if "onLaunched" in json_msg["method"] and not activated_time:
                                        activated_time = event_log.split('$$$')[0]
                                    elif "onDestroyed" in json_msg["method"] and not deactivated_time :
                                        deactivated_time = event_log.split('$$$')[0]
                            if activated_time and deactivated_time:
                                tdkTestObj.setResultStatus("SUCCESS")
                                conf_file,file_status = getConfigFileName(obj.realpath)
                                activate_config_status,activate_threshold = getDeviceConfigKeyValue(conf_file,"ACTIVATE_TIME_THRESHOLD_VALUE")
                                deactivate_config_status,deactivate_threshold = getDeviceConfigKeyValue(conf_file,"DEACTIVATE_TIME_THRESHOLD_VALUE")
                                offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                if all(value != "" for value in (activate_threshold,deactivate_threshold,offset)):
                                    start_activate_in_millisec = getTimeInMilliSec(start_activate)
                                    activated_time_in_millisec = getTimeInMilliSec(activated_time)
                                    print "\n Activate initiated at: " +start_activate + "(UTC)"
                                    print "\n Activated at : "+activated_time+ "(UTC)"
                                    time_taken_for_activate = activated_time_in_millisec - start_activate_in_millisec
                                    print "\n Time taken to activate {} plugin: {} (ms)".format(plugin,time_taken_for_activate)
                                    print "\n Threshold value for time taken to activate {} plugin: {} (ms)".format(plugin,activate_threshold)
                                    print "\n Validate the time taken for activation \n"
                                    if 0 < time_taken_for_activate < (int(activate_threshold) + int(offset)) :
                                        print "\n Time taken for activating {} plugin is within the expected range \n".format(plugin)
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print "\n Time taken for activating {} plugin is greater than the expected range \n".format(plugin)
                                        tdkTestObj.setResultStatus("FAILURE")
                                    start_deactivate_in_millisec = getTimeInMilliSec(start_deactivate)
                                    deactivated_time_in_millisec =  getTimeInMilliSec(deactivated_time)
                                    print "\n Deactivate initiated at: " + start_deactivate + "(UTC)"
                                    print "\n Deactivated at: " + deactivated_time + "(UTC)"
                                    time_taken_for_deactivate = deactivated_time_in_millisec - start_deactivate_in_millisec
                                    print "\n Time taken to deactivate {} plugin: {} (ms) \n".format(plugin,time_taken_for_deactivate)
                                    print "\n Threshold value for time taken to deactivate {} plugin: {} (ms)".format(plugin,deactivate_threshold)
                                    print "\n Validate the time taken for deactivation: \n"
                                    if 0 < time_taken_for_deactivate < (int(deactivate_threshold)+int(offset)) :
                                        print "\n Time taken for deactivating {} plugin is within the expected range \n".format(plugin)
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print "\n Time taken for deactivating {} plugin is greater than the expected range \n".format(plugin)
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "Threshold values are not configured in Device configuration file"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n onLaunched and onDestroyed events are not triggered"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n No events are triggered"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error while deactivating the plugin, current status: ",webkit_status
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Unable to deactivate the plugin"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while checking the status of plugin, current status: ",webkit_status
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while launching the plugin"
            obj.setLoadModuleStatus("FAILURE")
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
