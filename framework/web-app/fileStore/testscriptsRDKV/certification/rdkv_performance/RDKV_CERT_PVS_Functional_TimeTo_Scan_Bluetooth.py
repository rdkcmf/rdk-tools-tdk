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
  <name>RDKV_CERT_PVS_Functional_TimeTo_Scan_Bluetooth</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken to scan Bluetooth devices.</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-HYB</box_type>
    <box_type>RPI-Client</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_65</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to scan Bluetooth devices.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Bluetooth emulator should be available 
2. wpeframework should be up and running
3. Time in DUT and TM should be in sync</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Enable discovery on in Bluetooth emulator device.
2. Enable Bluetooth in DUT.
3. Listen for onDiscoveredDevice event
4. Start scanning for Bluetooth devices.
5. Stop scanning after few seconds
6. Check for the event logs
7. Validate the time taken using the triggered event.
</automation_approch>
    <expected_output>Time taken to scan for Bluetooth devices should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_Scan_Bluetooth</test_script>
    <skipped>No</skipped>
    <release_version>M92</release_version>
    <remarks/>
  </test_cases>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
</xml>

'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
from tdkvRDKServicesSupportlib import executeBluetoothCtl
from StabilityTestUtility import *
import rdkv_performancelib
from rdkv_performancelib import *
from PerformanceTestVariables import *
from web_socket_util import *
from datetime import datetime

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_Scan_Bluetooth')

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Execution summary variable 
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    revert="NO"
    event_listener = None
    plugins_list = ["org.rdk.Bluetooth"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    plugin_status = "SUCCESS"
    plugin_status_needed = {"org.rdk.Bluetooth":"activated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting plugin status"
        plugin_status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        plugin_status = set_plugins_status(obj,plugin_status_needed)
        new_plugins_status_dict = get_plugins_status(obj,plugins_list)
        if new_plugins_status_dict != plugin_status_needed:
            plugin_status = "FAILURE"
    bluetooth_commands = ["bluetoothctl","agent NoInputNoOutput","default-agent","discoverable on"]
    conf_file,conf_status = getConfigFileName(obj.realpath)
    bluetooth_emu_status = executeBluetoothCtl(conf_file,bluetooth_commands)
    if all(status == "SUCCESS" for status in ( plugin_status,conf_status,bluetooth_emu_status)):
        thunder_port = rdkv_performancelib.devicePort
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 6,"method": "org.rdk.Bluetooth.1.register","params": {"event": "onDiscoveredDevice", "id": "client.events.1" }}'],"/jsonrpc",False)
        time.sleep(10)
        tdkTestObj = obj.createTestStep('rdkservice_getValue')
        tdkTestObj.addParameter("method","org.rdk.Bluetooth.1.enable")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            print "\n Bluetooth enabled sucessfully"
            tdkTestObj.setResultStatus("SUCCESS")
            time.sleep(10)
            params = '{"timeout": "30", "profile": "DEFAULT"}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","org.rdk.Bluetooth.1.startScan")
            tdkTestObj.addParameter("value",params)
            scan_start_time = str(datetime.utcnow()).split()[1]
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            details = tdkTestObj.getResultDetails()
            if result == "SUCCESS":
                print "\n Bluetooth startScan executed sucessfully \n"
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(30)
                tdkTestObj = obj.createTestStep('rdkservice_getValue')
                tdkTestObj.addParameter("method","org.rdk.Bluetooth.1.stopScan")
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if result == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                    if [True for event in event_listener.getEventsBuffer() if "onDiscoveredDevice" in str(event) and "DISCOVERED" in str(event)]:
                        event_log = [event for event in event_listener.getEventsBuffer() if "onDiscoveredDevice" in str(event) and "DISCOVERED" in str(event)][0]
                        print "\n Triggered event: ",event_log,"\n"
                        event_time = event_log.split('$$$')[0]
                        config_status,bluetooth_scan_threshold = getDeviceConfigKeyValue(conf_file,"BLUETOOTH_SCAN_TIME_THRESHOLD_VALUE")
                        Summ_list.append('BLUETOOTH_SCAN_TIME_THRESHOLD_VALUE :{}ms'.format(bluetooth_scan_threshold))
                        offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                        Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
                        if all(value != "" for value in (bluetooth_scan_threshold,offset)):
                            scan_start_time_in_millisec = getTimeInMilliSec(scan_start_time)
                            scan_end_time_in_millisec = getTimeInMilliSec(event_time)
                            print "\n BLUETOOTH scan initiated at: ",scan_start_time
                            Summ_list.append('BLUETOOTH scan initiated at :{}'.format(scan_start_time))
                            print "\n BLUETOOTH scan completed at : ", event_time
                            Summ_list.append('BLUETOOTH scan completed at :{}'.format(event_time))
                            time_taken_for_wifiscan = scan_end_time_in_millisec - scan_start_time_in_millisec
                            print "\n Time taken to scan BLUETOOTH details: {}(ms)".format(time_taken_for_wifiscan)
                            Summ_list.append('Time taken to scan BLUETOOTH details :{}ms'.format(time_taken_for_wifiscan))
                            print "\n Threshold value for time taken to scan Bluetooth details : {} ms".format(bluetooth_scan_threshold)
                            print "\n Validate the time: \n"
                            if 0 < time_taken_for_wifiscan < (int(bluetooth_scan_threshold) + int(offset)) :
                                print "\n Time taken for scanning the Bluetooth details is within the expected range"
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print "\n Time taken for scanning the Bluetooth details is not within the expected range"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Please configure the Threshold value in device configuration file"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n onDiscoveredDevice event is not triggered"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error while executing stopscan"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while executing startscan"
                tdkTestObj.setResultStatus("FAILURE")
            event_listener.disconnect()
            time.sleep(10)
        else:
            print "\n Error while enabling Bluetooth"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Preconditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "\n Revert the values before exiting \n"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
    getSummary(Summ_list,obj)
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
