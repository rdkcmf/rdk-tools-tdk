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
  <name>RDKV_CERT_RVS_Toggle_2.4GHz_5GHz</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to switch between 2.4ghz and 5ghz SSID continuously for 1000 times</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3000</execution_time>
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
    <test_case_id>RDKV_STABILITY_37</test_case_id>
    <test_objective>The objective of this test is to switch between 2.4ghz and 5ghz SSID continuously for 1000 times</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Both 2.4GHZ and 5GHZ Access points should be available to connect.
2. If DUT is connected to Ethernet, the WiFi access point should be in same IP address range
3. Lightning application for ip change detection should be already hosted.
4. Wpeframework process should be up and running in the device.
5.4. If DUT is RPI, the version must be RPI 3B+ for detecting  5GHZ SSID.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>max_ssid_changes: int
ip_change_app_url: string
tm_username : string
tm_password : string
device_ip_address_type : string
webinspect port : string</input_parameters>
    <automation_approch>1. Load the Lightning application in WebKitBrowser to detect IP address change of DUT.
2a). If current active interface is ETHERNET, enable the WIFI interface.
b) Connect to SSID
c) Set WIFI as default interface
3. In a loop of minimum 1000 switch between 2.4GHZ SSID and 5GHZ SSID.
4. Validate CPU load and memory usage in each iteration.</automation_approch>
    <expected_output>DUT should connect to corresponding SSID in each iteration. 
CPU load and memory usage must be within the expected range.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_Toggle_2.4GHz_5GHz</test_script>
    <skipped>No</skipped>
    <release_version>M89</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from StabilityTestUtility import *
from ip_change_detection_utility import *
import StabilityTestVariables
import rdkv_stabilitylib

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Toggle_2.4GHz_5GHz');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    status = "SUCCESS"
    completed = True
    revert_if = ""
    max_iterations = StabilityTestVariables.max_ssid_changes
    revert_plugins_dict = {}
    plugins_list = ["WebKitBrowser","org.rdk.Wifi","DeviceInfo"]
    plugin_status_needed = {"WebKitBrowser":"resumed","org.rdk.Wifi":"activated","DeviceInfo":"activated"}
    print "\n Get plugins status \n"
    current_plugin_status_dict = get_plugins_status(obj,plugins_list)
    if plugin_status_needed != current_plugin_status_dict:
        print "\n Set plugins status \n"
        status = set_plugins_status(obj,plugin_status_needed)
    #Check current interface
    current_interface,revert_nw = check_current_interface(obj)
    initial_interface = current_interface
    url_status,complete_url = get_lightning_app_url(obj)
    if revert_nw == "YES":
        revert_plugins_dict["org.rdk.Network"] = "deactivated"
    if current_interface == "ETHERNET":
        revert_if = "YES"
        wifi_connect_status,plugins_status_dict,revert_plugins = switch_to_wifi(obj)
        if wifi_connect_status == "SUCCESS":
            current_interface = "WIFI"
        else:
            status = "FAILURE"
    if current_interface != "EMPTY" and current_plugin_status_dict != {} and all(value =="SUCCESS" for value in (url_status,status)):
        revert_plugins_dict.update(current_plugin_status_dict)
        status = launch_lightning_app(obj,complete_url)
        time.sleep(30)
        print "\n Check frequency of Connected SSID"
        ssid_freq = initial_ssid_freq = check_cur_ssid_freq(obj)
        if ssid_freq != "FAILURE" and status == "SUCCESS":
            for count in range(0,max_iterations):
                result_dict = {}
                if ssid_freq == "2.4":
                    new_ssid_freq = "5"
                else:
                    new_ssid_freq = "2.4"
                print "\n Connecting to {}GHZ SSID".format(new_ssid_freq)
                connect_wifi_status = connect_wifi(obj,new_ssid_freq)
                if connect_wifi_status == "SUCCESS":
                    ssid_freq = new_ssid_freq
                    time.sleep(10)
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
                        result_dict["iteration"] = count+1
                        result_dict["cpu_load"] = float(cpuload)
                        result_dict["memory_usage"] = float(memory_usage)
                        result_dict_list.append(result_dict)
		    else:
			print "\n Error while validating Resource usage"
               		tdkTestObj.setResultStatus("FAILURE")
                	break
                else:
                    print "\n Error happened while connecting to SSID"
                    completed = False
                    break
            else:
                print "\nSuccessfully completed the {} iterations ".format(max_iterations)
            cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
            json.dump(cpu_mem_info_dict,json_file)
            json_file.close()
        else:
            print "\n Preconditions are not met"
            completed = False
        if revert_if == "YES" and status == "SUCCESS":
            time.sleep(40)
            interface_status = set_default_interface(obj,"ETHERNET")
            if interface_status == "SUCCESS":
                print "\n Successfully reverted to ETHERNET \n"
                status = close_lightning_app(obj)
            else:
                print "\n Error while reverting to ETHERNET \n"
        if not completed:
            obj.setLoadModuleStatus("FAILURE")
    else:
        print "\n Preconditions are not met "
        obj.setLoadModuleStatus("FAILURE")
    if revert_plugins_dict != {}:
        status = set_plugins_status(obj,revert_plugins_dict)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
