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
  <name>RDKV_CERT_PVS_Functional_TimeTo_UserFactory_ResetDevice</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken to reset the DUT using resetDevice method of org.rdk.Warehouse plugin</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_67</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to reset the DUT using resetDevice method of org.rdk.Warehouse plugin</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be up and running
2. Time in Test Manager and DUT should be in sync.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Activate the warehouse plugin and system plugin
2. Create a test file in /opt/ directory in DUT.
3. Execute the resetDevice method of warehouse plugin.
4. Check for resetDone event for getting the time taken for reset.
5. Verify whether reset is happened by checking the test file is deleted and previous reboot info is updated to warehousereset.
6. Validate the time taken for reset.
</automation_approch>
    <expected_output>Reset should happen and time taken to reset should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_UserFactory_ResetDevice</test_script>
    <skipped>No</skipped>
    <release_version>M92</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from StabilityTestUtility import *
from datetime import datetime
from web_socket_util import *
import PerformanceTestVariables
import ast

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_UserFactory_ResetDevice');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    event_listener = None
    reset_done_time = ""
    thunder_port = PerformanceTestVariables.thunder_port
    plugins_list = ["org.rdk.Warehouse","org.rdk.System"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"org.rdk.System":"activated","org.rdk.Warehouse":"activated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        plugins_status_dict = get_plugins_status(obj,plugins_list)
        if plugins_status_dict != plugin_status_needed:
            print "\n Unable to set status of plugins"
            status = "FAILURE"
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    if status == "SUCCESS" and ssh_param_dict != {}:
        tdkTestObj.setResultStatus("SUCCESS")
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 5,"method": "org.rdk.Warehouse.1.register","params": {"event": "resetDone", "id": "client.events.1" }}'],"/jsonrpc",False)
        time.sleep(10)
        #Save a file
        command = 'touch /opt/tdk_test.ini; [ -f /opt/tdk_test.ini ] && echo yes || echo no'
        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
        tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
        tdkTestObj.addParameter("command",command)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        output = tdkTestObj.getResultDetails()
        if output != "EXCEPTION" and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            output = tdkTestObj.getResultDetails()
            if len(output.split('\n')) >= 3 and "yes" in output.split('\n')[1]:
                print "\n Successfully created tdk_test.ini file in /opt/ directory"
                print "\n Reset device"
                params = '{"suppressReboot": false, "resetType": "USERFACTORY"}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue');
                tdkTestObj.addParameter("method","org.rdk.Warehouse.1.resetDevice");
                tdkTestObj.addParameter("value",params)
                reset_start_time = str(datetime.utcnow()).split()[1] 
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult();
                if expectedResult in result:
                    print "\n The resetDevice method executed successfully"
                    tdkTestObj.setResultStatus("SUCCESS")
                    time.sleep(10)
                    continue_count = 0
                    while True:
                        if (continue_count > 60):
                            break
                        if (len(event_listener.getEventsBuffer())== 0):
                            continue_count += 1
                            time.sleep(1)
                            continue
                        event_log = event_listener.getEventsBuffer().pop(0)
                        print "\n Triggered event: ",event_log
                        event = json.loads(event_log.split('$$$')[1])
                        if event["method"] == 'client.events.1.resetDone' and event['params']["success"]:
                            print "\n Device reset is success"
                            reset_done_time = event_log.split('$$$')[0]
                            tdkTestObj.setResultStatus("SUCCESS")
                            break
                        else:
                            print "\n Error while resetting Device using resetDevice method"
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    time.sleep(150)
                    if reset_done_time:
                        print "\n Check reboot info"
                        status = "SUCCESS"
                        new_plugins_status_dict = get_plugins_status(obj,plugins_list)
                        if any(new_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
                            print "\n Error while getting status of plugins"
                            status = "FAILURE"
                        elif new_plugins_status_dict != plugin_status_needed:
                            revert = "YES"
                            status = set_plugins_status(obj,plugin_status_needed)
                            plugins_status_dict_after_set = get_plugins_status(obj,plugins_list)
                            if plugins_status_dict_after_set != plugin_status_needed:
                                print "\n Unable to set status of plugins"
                                status = "FAILURE"
                        if status == "SUCCESS":
                            print "\n Check previous reboot info"
                            tdkTestObj = obj.createTestStep('rdkservice_getValue')
                            tdkTestObj.addParameter("method","org.rdk.System.1.getPreviousRebootInfo2")
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            if expectedResult in result:
                                reboot_info = tdkTestObj.getResultDetails()
                                reboot_info = ast.literal_eval(reboot_info)
                                reboot_source = reboot_info['rebootInfo']['source']
                                if "WarehouseReset" in reboot_source:
                                    print "\n Device is rebooted due to resetDevice method"
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print "\n Check whether device reset is happened"
                                    command = '[ -f /opt/tdk_test.ini ] && echo yes || echo no'
                                    tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                                    tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                                    tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                                    tdkTestObj.addParameter("command",command)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result = tdkTestObj.getResult()
                                    output = tdkTestObj.getResultDetails()
                                    if output != "EXCEPTION" and expectedResult in result:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        if len(output.split('\n')) >= 3 and "no" in output.split('\n')[1]:
                                            print "\n The file /opt/tdk_test.ini is removed as part of reset"
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            conf_file,file_status = getConfigFileName(obj.realpath)
                                            config_status,device_reset_time_threshold = getDeviceConfigKeyValue(conf_file,"DEVICE_RESET_TIME_THRESHOLD_VALUE")
                                            offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                            if all(value != "" for value in (device_reset_time_threshold,offset)):
                                                reset_start_time_in_millisec = getTimeInMilliSec(reset_start_time)
                                                reset_done_time_in_millisec = getTimeInMilliSec(reset_done_time)
                                                print "\n Reset device initiated at: ", reset_start_time
                                                print "\n Reset device completed at : ", reset_done_time 
                                                time_taken_for_reset = reset_done_time_in_millisec - reset_start_time_in_millisec
                                                print "\n Time taken to reset the device: {}(ms)".format(time_taken_for_reset)
                                                print "\n Threshold value for time taken to reset the device: {}(ms)".format(device_reset_time_threshold)
                                                print "\n Validate the time: \n"
                                                if 0 < time_taken_for_reset < (int(device_reset_time_threshold) + int(offset)) :
                                                    print "\n Time taken for resetting the device is within the expected range"
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                else:
                                                    print "\n Time taken for resetting the device is not within the expected range"
                                                    tdkTestObj.setResultStatus("FAILURE")
                                            else:
                                                print "\n Please configure the Threshold value in device configuration file \n"
                                                tdkTestObj.setResultStatus("FAILURE")
                                        else:
                                            print "\n The file /opt/tdk_test.ini is not removed as part of reset"
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print "\n Error while executing a command in DUT"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n The reboot source is not updated as WarehouseReset, current reboot source: ",reboot_source
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Error while executing org.rdk.System.1.getPreviousRebootInfo2 method"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Plugins are not activated"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error while resetting the device"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error while executing org.rdk.Warehouse.1.resetDevice method"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while creating file named tdk_test.ini under /opt directory in DUT"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while executing command in DUT"
            tdkTestObj.setResultStatus("FAILURE")
        event_listener.disconnect()
        time.sleep(10)
    else:
        print "\n Preconditions are not met"
        tdkTestObj.setResultStatus("FAILURE")
     #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
