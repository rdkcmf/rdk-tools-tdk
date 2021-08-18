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
  <name>RDKV_CERT_RVS_Bluetooth_ConnectDisconnect</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to connect and disconnect Bluetooth for given number of times</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2000</execution_time>
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
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_STABILITY_25</test_case_id>
    <test_objective>The objective of this test is to connect and disconnect Bluetooth for given number of times</test_objective>
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
5. Pair the Bluetooth device, then in a loop 
a).Connect to the device. 
b) disconnect the device.
c) Validate the CPU and memory details from DeviceInfo Plugin.
6. unpair the device
7. Revert the status of plugins </automation_approch>
    <expected_output>Connect and disconnect should be working. Device must be stable after each iteration, CPU load and memory usage must be with in the expected limit.
 </expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_Bluetooth_ConnectDisconnect</test_script>
    <skipped>No</skipped>
    <release_version>M87</release_version>
    <remarks>None</remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from tdkvRDKServicesSupportlib import executeBluetoothCtl
from StabilityTestUtility import *
from rdkv_performancelib import *
import StabilityTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Bluetooth_ConnectDisconnect');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}{}_{}_{}_CPUMemoryInfo.json'.format(obj.logpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    revert="NO"
    plugins_list = ["DeviceInfo","org.rdk.Bluetooth","org.rdk.System"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    plugin_status = "SUCCESS"
    plugin_status_needed = {"DeviceInfo":"activated","org.rdk.Bluetooth":"activated","org.rdk.System":"activated"}
    connect_disconnect_max_count = StabilityTestVariables.connect_disconnect_max_count
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
        plugin_status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        plugin_status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_plugins_status_dict = get_plugins_status(obj,plugins_list)
        if new_plugins_status_dict != plugin_status_needed:
            plugin_status = "FAILURE"
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
                                    devices_list = []
                                    print "\n Bluetooth getPairedDevices executed sucessfully \n"
                                    paired = False
                                    devices_list = ast.literal_eval(details)["pairedDevices"]
                                    print "\n Paired Devices :",devices_list
                                    if devices_list and  any(device["name"] == device_name for device in devices_list):
                                        print "\n Device paired successfully \n"
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        #Get bluetooth_mac of DUT
                                        tdkTestObj = obj.createTestStep('rdkservice_getBluetoothMac')
                                        tdkTestObj.executeTestCase(expectedResult)
                                        result = tdkTestObj.getResult()
                                        bluetooth_mac = tdkTestObj.getResultDetails()
                                        if result == "SUCCESS":
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print "\n Bluetooth_mac:",bluetooth_mac
                                            #execute trust command in bluetooth emulator
                                            ip_result,ip = getDeviceConfigKeyValue(conf_file,'BT_EMU_IP')
                                            username_result,username = getDeviceConfigKeyValue(conf_file,'BT_EMU_USER_NAME')
                                            password_result, password = getDeviceConfigKeyValue(conf_file,'BT_EMU_PWD')
                                            credentials = ip +','+username+','+password
                                            command = "bluetoothctl <<< 'trust "+bluetooth_mac+"'"
                                            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                                            tdkTestObj.addParameter("ssh_method","directSSH")
                                            tdkTestObj.addParameter("credentials",credentials)
                                            tdkTestObj.addParameter("command",command)
                                            tdkTestObj.executeTestCase(expectedResult)
                                            result = tdkTestObj.getResult()
                                            output = tdkTestObj.getResultDetails()
                                            if output != "EXCEPTION" and expectedResult in result:
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                for count in range(0,connect_disconnect_max_count):
                                                    print "\n########## Iteration :{} ##########\n".format(count+1)
                                                    result_dict = {}
                                                    print "\n Executing connect method \n"
                                                    params = '{"deviceID": "' + device_id + '","deviceType":"HUMAN INTERFACE DEVICE","profile": "DEFAULT"}'
                                                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                                    tdkTestObj.addParameter("method","org.rdk.Bluetooth.1.connect")
                                                    tdkTestObj.addParameter("value",params)
                                                    tdkTestObj.executeTestCase(expectedResult)
                                                    result = tdkTestObj.getResult()
                                                    if result == "SUCCESS":
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        time.sleep(10)
                                                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                                                        tdkTestObj.addParameter("method","org.rdk.Bluetooth.1.getConnectedDevices")
                                                        tdkTestObj.executeTestCase(expectedResult)
                                                        result = tdkTestObj.getResult()
                                                        details = tdkTestObj.getResultDetails()
                                                        if result == "SUCCESS":
                                                            devices_list = []
                                                            print "\n Bluetooth getConnectedDevices executed sucessfully \n"
                                                            devices_list = ast.literal_eval(details)["connectedDevices"]
                                                            print "Devices_list",devices_list
                                                            if devices_list and  any(device["name"] == device_name for device in devices_list):
                                                                print "Bluetooth Device is present in connected list\n"
                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                #Disconnect Bluetooth device
                                                                print "\n Disconnecting from Bluetooth device \n" 
                                                                params = '{"deviceID": "' +device_id + '","deviceType":"HUMAN INTERFACE DEVICE"}'
                                                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                                                tdkTestObj.addParameter("method","org.rdk.Bluetooth.1.disconnect")
                                                                tdkTestObj.addParameter("value",params)
                                                                tdkTestObj.executeTestCase(expectedResult)
                                                                time.sleep(10)
                                                                result = tdkTestObj.getResult()
                                                                if result == "SUCCESS":
                                                                    print "disconnect method is success \n"
                                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                                    print "\n Check Bluetooth Device is disconnected :\n"
                                                                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                                                                    tdkTestObj.addParameter("method","org.rdk.Bluetooth.1.getConnectedDevices")
                                                                    tdkTestObj.executeTestCase(expectedResult)
                                                                    result = tdkTestObj.getResult()
                                                                    details = tdkTestObj.getResultDetails()
                                                                    if result == "SUCCESS":
                                                                        devices_list = []
                                                                        devices_list = ast.literal_eval(details)["connectedDevices"]
                                                                        print "Devices_list",devices_list
                                                                        if not (devices_list and any(device["name"] == device_name for device in devices_list)):
                                                                            print "\n Bluetooth Device is disconnected properly \n"
                                                                            print "\n ##### Validating CPU load and memory usage #####\n"
									    print "Iteration : ", count+1
                                                                            tdkTestObj = obj.createTestStep('rdkservice_validateResourceUsage')
                                                                            tdkTestObj.executeTestCase(expectedResult)
                                                                            status = tdkTestObj.getResult()
                                                                            result = tdkTestObj.getResultDetails()
                                                                            if expectedResult in status and result != "ERROR":
                                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                                cpuload = result.split(',')[0]
                                                                                memory_usage = result.split(',')[1]
									    else:
										print "\n Error while validating Resource usage"
               								        tdkTestObj.setResultStatus("FAILURE")
               								        break
                                                                        else:
                                                                            print "\n Bluetooth device is not properly disconnected \n"
                                                                            tdkTestObj.setResultStatus("FAILURE")
                                                                            break
                                                                    else:
                                                                        print "\n Error while executing getConnectedDevices method \n"
                                                                        tdkTestObj.setResultStatus("FAILURE")
                                                                        break
                                                                else:
                                                                    print "\n Error in disconnect method \n"
                                                                    tdkTestObj.setResultStatus("FAILURE")
                                                                    break
                                                            else:
                                                                print "\n Bluetooth device is not present in connected list \n"
                                                                tdkTestObj.setResultStatus("FAILURE")
                                                                break
                                                        else:
                                                            print "\n Error while executing getConnectedDevices method \n"
                                                            tdkTestObj.setResultStatus("FAILURE")
                                                            break
                                                    else:
                                                        print "\n Error while executing connect method \n"
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        break
                                                    result_dict["iteration"] = count+1
                                                    result_dict["cpu_load"] = float(cpuload)
                                                    result_dict["memory_usage"] = float(memory_usage)
                                                    result_dict_list.append(result_dict)
                                                else:
                                                    print "\n Successfully completed {} connect and disconnect operations \n".format(connect_disconnect_max_count)
                                                cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                                                json.dump(cpu_mem_info_dict,json_file)
                                                json_file.close()
                                            else:
                                                print "\n Error while executing trust command in Bluetooth device \n"
                                                tdkTestObj.setResultStatus("FAILURE")
                                        else:
                                            print "\n Error while getting Bluetooth MAC of DUT \n"
                                            tdkTestObj.setResultStatus("FAILURE")
                                        #Unpair device
                                        params = '{"deviceID": "' +device_id + '"}'
                                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                        tdkTestObj.addParameter("method","org.rdk.Bluetooth.1.unpair")
                                        tdkTestObj.addParameter("value",params)
                                        tdkTestObj.executeTestCase(expectedResult)
                                        result = tdkTestObj.getResult()
                                        if result == "SUCCESS":
                                            print "\n Unpair method is executed successfully \n"
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            tdkTestObj = obj.createTestStep('rdkservice_getValue')
                                            tdkTestObj.addParameter("method","org.rdk.Bluetooth.1.getPairedDevices")
                                            tdkTestObj.executeTestCase(expectedResult)
                                            result = tdkTestObj.getResult()
                                            details = tdkTestObj.getResultDetails()
                                            if result == "SUCCESS":
                                                devices_list = []
                                                print "\n Bluetooth getPairedDevices executed sucessfully \n"
                                                paired = False
                                                devices_list = ast.literal_eval(details)["pairedDevices"]
                                                print "\n Paired Devices :",devices_list
                                                if not (devices_list and any(device["name"] == device_name for device in devices_list)):
                                                    print "Bluetooth Device unpaired successfully"
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                else:
                                                    print "\n Bluetooth Device is not unpaired \n"
                                                    tdkTestObj.setResultStatus("FAILURE")
                                            else:
                                                print "\n Error while executing getPairedDevices method \n"
                                                tdkTestObj.setResultStatus("FAILURE")
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
                    print "\n StopScan is not working \n"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n StartScan is not working \n"
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
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
