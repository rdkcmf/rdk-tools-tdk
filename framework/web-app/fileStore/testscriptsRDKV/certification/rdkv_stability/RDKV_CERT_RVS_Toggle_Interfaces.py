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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_RVS_Toggle_Interfaces</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to toggle between Ethernet and Wi-Fi interfaces for given number of times.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>4000</execution_time>
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
    <test_case_id>RDKV_STABILITY_17</test_case_id>
    <test_objective>The objective of this test is to toggle between Ethernet and Wi-Fi interfaces for given number of times.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Both Ethernet and WiFi connection are required and WiFi connection should provide same IP address range of Ethernet
2. Lightning application for IP address change detection should be already hosted.
3. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>ip_change_app_url: string
tm_username : string
tm_password : string
device_ip_address_type : string
max_interface_changes: integer</input_parameters>
    <automation_approch>1. Check the current default network interface.
2. In a loop of minimum 1000 iterations,
a) If the current default interface is Ethernet set default interface as Wi-Fi otherwise set Ethernet as default interface.
b) Toggle Default Interface as Wi-Fi and Ethernet.
c)Validate CPU load and memory usage
3. Revert everything back</automation_approch>
    <expected_output>1. Network interface toggling should work fine.
2. CPU load and memory usage must be within the expected limit.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_Toggle_Interfaces</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
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
rdkv_stabilitylib.test_obj = obj

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Toggle_Interfaces');

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
    max_iterations = StabilityTestVariables.max_interface_changes
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
    if current_interface != "EMPTY" and current_plugin_status_dict != {} and url_status == status == "SUCCESS":
        revert_plugins_dict.update(current_plugin_status_dict)
        for count in range(0,max_iterations):
            result_dict = {}
            if current_interface == "ETHERNET":
                new_interface = "WIFI"
            else:
                new_interface = "ETHERNET"
                status = launch_lightning_app(obj,complete_url)
                time.sleep(30)
            if status == "SUCCESS":
                print "\n Setting Default interface as {}\n".format(new_interface)
                tdkTestObj = obj.createTestStep('rdkservice_setDefaultInterface')
                tdkTestObj.addParameter("new_interface",new_interface)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                details = tdkTestObj.getResultDetails()
                if details == "SUCCESS" and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS")
                    current_interface = new_interface
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
                    print "\n Error while setting Default interface \n"
                    tdkTestObj.setResultStatus("FAILURE")
                    break
            else:
                print "Error while lauching application \n"
                break
        else:
            print "\nSuccessfully completed the {} iterations \n".format(max_iterations)
        cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
        json.dump(cpu_mem_info_dict,json_file)
        json_file.close()
        #Revert interface
        if current_interface != initial_interface:
            print "\n Revert network interface to {}\n".format(initial_interface)
            if initial_interface == "ETHERNET":
                status = launch_lightning_app(obj,complete_url)
                time.sleep(30)
            tdkTestObj = obj.createTestStep('rdkservice_setDefaultInterface')
            tdkTestObj.addParameter("new_interface",initial_interface)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            details = tdkTestObj.getResultDetails()
            if details == "SUCCESS" and expectedResult in result:
                print "\n Successfully reverted the interface\n"
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "\n Error while reverting the network interface \n"
                tdkTestObj.setResultStatus("FAILURE")
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
