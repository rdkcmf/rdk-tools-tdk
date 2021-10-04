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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_RVS_Bluetooth_PairUnpair</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_validateResourceUsage</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to do pair and unpair Bluetooth emulator for a minimum of 1000 times.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2400</execution_time>
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
    <test_case_id>RDKV_STABILITY_48</test_case_id>
    <test_objective>The objective of this test is to do pair and unpair Bluetooth emulator for a minimum of 1000 times.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Bluetooth emulator should be available
2. wpeframework should be up and running in the DUT.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>pair_unpair_max_count:integer</input_parameters>
    <automation_approch>1. Bluetooth and Device info plugins should be activated.
In a loop of 1000:
2. SSH to the Bluetooth emulator and make the device discoverable.
3. Start scanning in DUT for the emulator.
4. Stop scanning and check for emulator details in the discoveredDevices.
5. Pair the Bluetooth device and check the pairedDevices list
6. Unpair the device and check the pairedDevices list
7. Validate the CPU and memory details from DeviceInfo Plugin.
8. Revert the status of plugins </automation_approch>
    <expected_output>Pair and Unpair should be working. Device must be stable after each iteration, CPU load and memory usage must be with in the expected limit.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_Bluetooth_PairUnpair</test_script>
    <skipped>No</skipped>
    <release_version>M93</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib 
from tdkvRDKServicesSupportlib import executeBluetoothCtl
from StabilityTestUtility import *
from rdkv_performancelib import *
import StabilityTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Bluetooth_PairUnpair');

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
    error_in_loop = False
    plugin_status_needed = {"DeviceInfo":"activated","org.rdk.Bluetooth":"activated","org.rdk.System":"activated"}
    max_count = StabilityTestVariables.pair_unpair_max_count
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
    name_status,device_name = getDeviceConfigKeyValue(conf_file,"BT_EMU_DEVICE_NAME")
    if all(status == "SUCCESS" for status in (plugin_status,conf_status)) and device_name != "":
        for count in range(0,max_count):
            print "\n########## Iteration :{} ##########\n".format(count+1)
            result_dict = {}
            bluetooth_emu_status = executeBluetoothCtl(conf_file,bluetooth_commands)
            tdkTestObj = obj.createTestStep('rdkservice_getValue')
            tdkTestObj.addParameter("method","org.rdk.Bluetooth.1.enable")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if (result and bluetooth_emu_status) == "SUCCESS":
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
                    print "\n Bluetooth startScan executed sucessfully"
                    tdkTestObj.setResultStatus("SUCCESS")
                    time.sleep(20)
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method","org.rdk.Bluetooth.1.stopScan")
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if result == "SUCCESS":
                        print "\n Bluetooth stopScan executed sucessfully"
                        tdkTestObj.setResultStatus("SUCCESS")
                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                        tdkTestObj.addParameter("method","org.rdk.Bluetooth.1.getDiscoveredDevices")
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        details = tdkTestObj.getResultDetails()
                        if result == "SUCCESS":
                            print "\n Bluetooth getDiscoveredDevices executed sucessfully"
                            device_id = ""
                            devices_list = ast.literal_eval(details)["discoveredDevices"]
                            for device in devices_list:
                                if device["name"] == device_name:
                                    device_id = device["deviceID"]
                            if device_id != "" :
                                print "\n Device found in the getDiscoveredDevices list"
                                tdkTestObj.setResultStatus("SUCCESS")
                                for method in ["pair","unpair"]:
                                    print "\n Executing {} method".format(method)
                                    params = '{"deviceID": "' + device_id + '"}'
                                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                    tdkTestObj.addParameter("method","org.rdk.Bluetooth.1."+method)
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
                                            print "\n Bluetooth getPairedDevices executed sucessfully"
                                            devices_list = ast.literal_eval(details)["pairedDevices"]
                                            print "\n Paired Devices list: ",devices_list
                                            paired_condition = devices_list != [] and any(device["name"] == device_name for device in devices_list)
                                            proceeding_condition = paired_condition if method == 'pair' else not paired_condition
                                            if proceeding_condition:
                                                print "\n Device {}ed successfully".format(method)
                                                tdkTestObj.setResultStatus("SUCCESS")
                                            else:
                                                print "\n Device is not {}ed successfully".format(method)
                                                tdkTestObj.setResultStatus("FAILURE")
                                                error_in_loop = True
                                                break
                                        else:
                                            print "\n Error while executing getPairedDevices method \n"
                                            tdkTestObj.setResultStatus("FAILURE")
                                            error_in_loop = True
                                            break
                                    else:
                                        print "\n Error while executing {} method ".format(method)
                                        tdkTestObj.setResultStatus("FAILURE")
                                        error_in_loop = True
                                        break
                                else:
                                    print "\n #### Successfully completed pair and unpair operations #### \n"
                                    print "\n ##### Validating CPU load and memory usage ##### \n"
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
                                    result_dict["iteration"] = count+1
                                    result_dict["cpu_load"] = float(cpuload)
                                    result_dict["memory_usage"] = float(memory_usage)
                                    result_dict_list.append(result_dict)
                                if error_in_loop:
                                    print "\n Stopping the test !!\n"
                                    break
                            else:
                                print "\n Device not found in the getDiscoveredDevices list"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            print "\n Error while executing getDiscoveredDevices method"
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        print "\n StopScan is not working"
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                else:
                    print "\n StartScan is not working"
                    tdkTestObj.setResultStatus("FAILURE")
                    break
            else:
                print "\n Bluetooth is not enabled"
                tdkTestObj.setResultStatus("FAILURE")
                break
        else:
            print "\n Successfully completed {} pair and unpair operations \n".format(max_count)
        cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
        json.dump(cpu_mem_info_dict,json_file)
        json_file.close()
    else:
        print "\n Preconditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
