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
  <name>RDKV_CERT_PACS_Cobalt_TimeTo_Destroy</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to validate the time taken to destroy Cobalt plugin</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2</execution_time>
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
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_71</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to destroy Cobalt plugin</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. Time in Test Manager and DUT should be in sync with UTC</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Register for onDestroyed event of RDKShell.
2. Launch Cobalt using RDKShell
3. Save current system time and destroy Cobalt using destroy method of RDKShell plugin
4. Get the time from triggered event
5. Validate the output with threshold value</automation_approch>
    <expected_output>The time taken should be within the expected limit.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_TimeTo_Destroy</test_script>
    <skipped>No</skipped>
    <release_version>M94</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
import PerformanceTestVariables
from StabilityTestUtility import *
from web_socket_util import *
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_TimeTo_Destroy')

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

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
    time.sleep(10)
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_status_dict = get_plugins_status(obj,plugins_list)
        if new_status_dict != plugin_status_needed:
            print "\n Unable to deactivate the plugins"
            status = "FAILURE"
    if status == "SUCCESS":
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 6,"method": "org.rdk.RDKShell.1.register","params": {"event": "onDestroyed", "id": "client.events.1" }}'],"/jsonrpc",False)
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
                print "\n Cobalt resumed successfully "
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(10)
                #Deactivate cobalt
                print "\n Destroying Cobalt \n"
                tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
                tdkTestObj.addParameter("plugin","Cobalt")
                tdkTestObj.addParameter("status","deactivate")
                destroy_start_time = str(datetime.utcnow()).split()[1]
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if result == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                    tdkTestObj.addParameter("plugin","Cobalt")
                    tdkTestObj.executeTestCase(expectedResult)
                    cobalt_status = tdkTestObj.getResultDetails()
                    result = tdkTestObj.getResult()
                    if cobalt_status == 'deactivated' and expectedResult in result:
                        print "\n Cobalt destroyed successfully"
                        tdkTestObj.setResultStatus("SUCCESS")
                        destroyed_time = ""
                        continue_count = 0
                        while True:
                            if (continue_count > 60):
                                break
                            if (len(event_listener.getEventsBuffer())== 0):
                                continue_count += 1
                                time.sleep(1)
                                continue
                            event_log = event_listener.getEventsBuffer().pop(0)
                            print "\n Triggered event: ",event_log,"\n"
                            if ("Cobalt" in event_log):
                                print "\n Event :onDestroyed is triggered during Cobalt destroy"
                                destroyed_time = event_log.split('$$$')[0]
                                break
                        if destroyed_time:
                            conf_file,file_status = getConfigFileName(obj.realpath)
                            config_status,cobalt_destroy_threshold = getDeviceConfigKeyValue(conf_file,"COBALT_DESTROY_THRESHOLD_VALUE")
                            offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                            if all(value != "" for value in (cobalt_destroy_threshold,offset)):
                                destroy_start_time_in_millisec = getTimeInMilliSec(destroy_start_time)
                                destroyed_time_in_millisec = getTimeInMilliSec(destroyed_time)
                                print "\n Cobalt destroy initiated at: ",destroy_start_time
                                print "\n Cobalt destroyed at : ",destroyed_time
                                time_taken_for_destroy = destroyed_time_in_millisec - destroy_start_time_in_millisec
                                print "\n Time taken to destroy Cobalt: {}(ms)".format(time_taken_for_destroy)
                                print "\n Validate the time:"
                                if 0 < time_taken_for_destroy < (int(cobalt_destroy_threshold) + int(offset)) :
                                    print "\n Time taken for destroying Cobalt is within the expected range"
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print "\n Time taken for destroying Cobalt is not within the expected range"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Please configure the Threshold value in device configuration file"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n onDestroyed event not triggered for during Cobalt destroy"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Unable to destroy Cobalt, current status: ",cobalt_status
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error while destroying Cobalt"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Unable to launch Cobalt, current status: ",cobalt_status
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while launching Cobalt"
        event_listener.disconnect()
        time.sleep(5)
    else:
        print "\n Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
