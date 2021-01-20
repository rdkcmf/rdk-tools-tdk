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
  <version>4</version>
  <name>RdkService_FunctionalPerformance_BluetoothConnection</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to get the CPU and memory usage after connecting to  a Bluetooth device</synopsis>
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
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_18</test_case_id>
    <test_objective>The objective of this test is to connect to a Bluetooth device and validate the CPU and memory usage</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Need to set up a Bluetooth emulator .
2. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Bluetooth and Device info plugins should be activated.
2. SSH to the Bluetooth emulator and make the device discoverable.
3. Start scanning in DUT for the emulator.
4. Stop scanning and check for emulator details in the discoveredDevices.
5. Connect to the device 
6. Validate the CPU and memory details from DeviceInfo Plugin.
7. Revert the status of plugins </automation_approch>
    <expected_output>Bluetooth emulator should be connected and cpu load and memory usage must with within the expected range.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RdkService_FunctionalPerformance_BluetoothConnection</test_script>
    <skipped>No</skipped>
    <release_version>M84</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from tdkvRDKServicesSupportlib import executeBluetoothCtl
from StabilityTestUtility import *
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RdkService_FunctionalPerformance_BluetoothConnection');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    revert="NO"
    plugins_list = ["DeviceInfo","org.rdk.Bluetooth"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    plugin_status = "SUCCESS"
    plugin_status_needed = {"DeviceInfo":"activated","org.rdk.Bluetooth":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        plugin_status = set_plugins_status(obj,plugin_status_needed)
    bluetooth_commands = ["bluetoothctl","agent NoInputNoOutput","default-agent","discoverable on"]
    conf_file,conf_status = getConfigFileName(obj.realpath)
    bluetooth_emu_status = executeBluetoothCtl(conf_file,bluetooth_commands)
    if all(status == "SUCCESS" for status in ( plugin_status,conf_status,bluetooth_emu_status)):
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
                    print "\n Bluetooth stopScan executed sucessfully \n"
                    tdkTestObj.setResultStatus("SUCCESS")
                    status,device_name = getDeviceConfigKeyValue(conf_file,"BT_EMU_DEVICE_NAME")
                    print "Devicename :",device_name
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method","org.rdk.Bluetooth.1.getDiscoveredDevices")
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    details = tdkTestObj.getResultDetails()
                    if result == "SUCCESS":
                        print "\n Bluetooth getDiscoveredDevices executed sucessfully \n"
                        device_id = ""
                        devices_list = ast.literal_eval(details)["discoveredDevices"]
                        for device in devices_list:
                            if device["name"] == device_name:
                                device_id = device["deviceID"]
                        if device_id != "" :
                            print "\n Device found in the getDiscoveredDevices list \n"
                            tdkTestObj.setResultStatus("SUCCESS")
                            params = '{"deviceID": "' + device_id + '"}'
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method","org.rdk.Bluetooth.1.pair")
                            tdkTestObj.addParameter("value",params)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            if result == "SUCCESS":
                                tdkTestObj.setResultStatus("SUCCESS")
                                time.sleep(15)
                                tdkTestObj = obj.createTestStep('rdkservice_getValue')
                                tdkTestObj.addParameter("method","org.rdk.Bluetooth.1.getPairedDevices")
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                details = tdkTestObj.getResultDetails()
                                if result == "SUCCESS":
                                    print "\n Bluetooth getPairedDevices executed sucessfully \n"
                                    paired = False
                                    devices_list = ast.literal_eval(details)["pairedDevices"]
                                    for device in devices_list:
                                        if device["name"] == device_name:
                                            paired = True
                                    if paired:
                                        print "Device paired successfully"
                                        tdkTestObj.setResultStatus("SUCCESS")
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
                                            result = tdkTestObj.getResult()
                                            is_high_cpuload = tdkTestObj.getResultDetails()
                                            if is_high_cpuload == "YES"  or expectedResult not in result:
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
                                            result = tdkTestObj.getResult()
                                            is_high_memory_usage = tdkTestObj.getResultDetails()
                                            if is_high_memory_usage == "YES" or expectedResult not in result:
                                                print "\nmemory usage is high :{}%\n".format(memory_usage)
                                                tdkTestObj.setResultStatus("FAILURE")
                                            else:
                                                print "\nmemory usage :{}%\n".format(memory_usage)
                                                tdkTestObj.setResultStatus("SUCCESS")
                                        else:
                                            print "\n Unable to get the memory usage\n"
                                            tdkTestObj.setResultStatus("FAILURE")
                                        #Unpair device
                                        params = '{"deviceID": "' +device_id + '"}'
                                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                        tdkTestObj.addParameter("method","org.rdk.Bluetooth.1.unpair")
                                        tdkTestObj.addParameter("value",params)
                                        tdkTestObj.executeTestCase(expectedResult)
                                        result = tdkTestObj.getResult()
                                        if result == "SUCCESS":
                                            print "Device is unpaired \n"
                                            tdkTestObj.setResultStatus("SUCCESS")
                                        else:
                                            print "\n Error in unpair method \n"
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print "\n Device is not paired \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n Error while executing getPairedDevices method \n"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Error while executing pair method \n"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Device not found in the getDiscoveredDevices list \n"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error while executing getDiscoveredDevices method \n"
                        tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n startScan is not working \n"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Bluetooth is not enabled \n"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Preconditions are not met \n"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "\n Revert the values before exiting \n"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
