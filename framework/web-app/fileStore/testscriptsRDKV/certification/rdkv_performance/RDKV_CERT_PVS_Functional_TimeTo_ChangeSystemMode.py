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
  <version>3</version>
  <name>RDKV_CERT_PVS_Functional_TimeTo_ChangeSystemMode</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate  the time to change system mode of the device.</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_95</test_case_id>
    <test_objective>The objective of this test is to validate  the time to change system mode of the device.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>thunder_port: string</input_parameters>
    <automation_approch>1. Activate the System plugin
2. Get the current system mode using getMode
3. Register for "onSystemModeChanged" event
4. Set the mode to WAREHOUSE
5.Validate the time taken to change the mode using event log
6. Revert the plugin status</automation_approch>
    <expected_output>The time taken for mode change should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_ChangeSystemMode</test_script>
    <skipped>No</skipped>
    <release_version>M96</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib 
from rdkv_performancelib import *
from datetime import datetime
from StabilityTestUtility import *
from web_socket_util import *
import PerformanceTestVariables
import ast

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_ChangeSystemMode')
#Execution summary variable 
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "\n Check Pre conditions"
    event_listener = None
    continue_count = 0
    mode_change_start_time = ""
    mode_changed_time = ""
    thunder_port = PerformanceTestVariables.thunder_port
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["org.rdk.System"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    inverse_dict = {"NORMAL":"WAREHOUSE","WAREHOUSE":"NORMAL"}
    plugin_status_needed = {"org.rdk.System":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        plugins_status_dict = get_plugins_status(obj,plugins_list)
        if plugins_status_dict != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS":
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 5,"method": "org.rdk.System.1.register","params": {"event": "onSystemModeChanged", "id": "client.events.1" }}'],"/jsonrpc",False)
        time.sleep(10)
        print "\nPre conditions for the test are set successfully"
        print "\n Get the current mode"
        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
        tdkTestObj.addParameter("method","org.rdk.System.1.getMode")
        tdkTestObj.addParameter("reqValue","modeInfo")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        current_mode = tdkTestObj.getResultDetails()
        current_mode = ast.literal_eval(current_mode)["mode"]
        if expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            print "\n Current system mode : ",current_mode
            print "\n Set system mode to :",inverse_dict[current_mode]
            params = '{"modeInfo":{"mode":"'+inverse_dict[current_mode]+'","duration":120}}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","org.rdk.System.1.setMode")
            tdkTestObj.addParameter("value",params)
            mode_change_start_time = str(datetime.utcnow()).split()[1]
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if expectedResult in result:
                print "\n setMode is executed successfully"
                tdkTestObj.setResultStatus("SUCCESS")
                while not(mode_changed_time):
                    if (continue_count > 60):
                        print "\n onSystemModeChanged event is not triggered"
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                    if (len(event_listener.getEventsBuffer())== 0):
                        continue_count += 1
                        time.sleep(1)
                        continue
                    event_log = event_listener.getEventsBuffer().pop(0)
                    print "\n Triggered event: ",event_log
                    if ("onSystemModeChanged" in str(event_log) and inverse_dict[current_mode] in str(event_log)):
                        print "\n Event :onSystemModeChanged is triggered during mode change"
                        mode_changed_time = event_log.split('$$$')[0]
                else:
                    tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
                    tdkTestObj.addParameter("method","org.rdk.System.1.getMode")
                    tdkTestObj.addParameter("reqValue","modeInfo")
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult();
                    new_mode = tdkTestObj.getResultDetails()
                    new_mode = ast.literal_eval(new_mode)["mode"]
                    if expectedResult in result and new_mode == inverse_dict[current_mode]:
                        print "\n New system mode is: ",inverse_dict[current_mode]
                        tdkTestObj.setResultStatus("SUCCESS")
                        conf_file,file_status = getConfigFileName(obj.realpath)
                        config_status,modechange_time_threshold = getDeviceConfigKeyValue(conf_file,"SYS_MODECHANGE_THRESHOLD_VALUE")
                        Summ_list.append('SYS_MODECHANGE_THRESHOLD_VALUE :{}ms'.format(modechange_time_threshold))
                        offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                        Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
                        if all(value != "" for value in (modechange_time_threshold,offset)):
                            mode_change_start_time_in_millisec = getTimeInMilliSec(mode_change_start_time)
                            mode_changed_time_in_millisec = getTimeInMilliSec(mode_changed_time)
                            print "\n Set system mode initiated at: " + mode_change_start_time + "(UTC)"
                            Summ_list.append('Set system mode initiated at :{}'.format(mode_change_start_time))
                            print "\n System mode changed at : "+ mode_changed_time + "(UTC)"
                            Summ_list.append('System mode changed at :{}'.format(mode_changed_time))
                            time_taken_for_modechange = mode_changed_time_in_millisec - mode_change_start_time_in_millisec
                            print "\n Time taken for system mode change : {}(ms)".format(time_taken_for_modechange)
                            Summ_list.append('Time taken for system mode change :{}ms'.format(time_taken_for_modechange))
                            print "\n Threshold value for system mode change: {} ms".format(modechange_time_threshold)
                            print "\n Validate the time: \n"
                            if 0 < time_taken_for_modechange < (int(modechange_time_threshold) + int(offset)) :
                                print "\n Time taken for system mode change is within the expected range \n"
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print "\n Time taken for system mode change is not within the expected range \n"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Failed to get the threshold value from config file"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Unable to set system mode to :{}, current system mode: {}".format(inverse_dict[current_mode],new_mode)
                        tdkTestObj.setResultStatus("FAILURE")
                print "\n Revert system mode to:",current_mode
                params = '{"modeInfo":{"mode":"'+current_mode+'","duration":10}}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.System.1.setMode")
                tdkTestObj.addParameter("value",params)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult();
                if expectedResult in result:
                    print "\n setMode is executed successfully"
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print "\n Error while executing setMode method"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while executing setMode method"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while executing getMode method"
            tdkTestObj.setResultStatus("FAILURE")
        event_listener.disconnect()
        time.sleep(10)
    else:
        print "\n Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance")
    getSummary(Summ_list)
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
