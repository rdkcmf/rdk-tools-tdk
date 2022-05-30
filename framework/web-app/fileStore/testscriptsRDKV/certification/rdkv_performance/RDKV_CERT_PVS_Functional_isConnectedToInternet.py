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
  <name>RDKV_CERT_PVS_Functional_isConnectedToInternet</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getValue</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to check org.rdk.Network.1.isConnectedToInternet method with Ethernet, 2.4GHz and 5GHz Wi-Fi.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>20</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_55</test_case_id>
    <test_objective>The objective of this test is to check org.rdk.Network.1.isConnectedToInternet method with Ethernet, 2.4GHz and 5GHz Wi-Fi.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Lightning application for ip change detection should be already hosted.
2. Wpeframework process should be up and running in the device.
3. RPI 3B+ is needed to detect 5GHz SSID</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>ip_change_app_url: string
tm_username : string
tm_password : string
device_ip_address_type : string</input_parameters>
    <automation_approch>1. Activate org.rdk.Network plugin  Check the current interface of DUT.
2. Launch the Lightning app to detect ip address change in webkitbrowser.
3. In a loop of for 3 different connections :- (Ethernet, 2.4GHZ WIFI, 5GHZ WIFI) :
3a) Check org.rdk.Network.1.isConnectedToInternet for the current interface. Set the next connection.
4. Revert the connection after the test.</automation_approch>
    <expected_output>The method should return True for all connections.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_isConnectedToInternet</test_script>
    <skipped>No</skipped>
    <release_version>M90</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
from ip_change_detection_utility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_isConnectedToInternet');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    validation_dict = {}
    initial_connection = ""
    revert_plugins_dict = {}
    connections_list = ["WIFI","WIFI_5GHZ","ETHERNET"]
    for connection in connections_list:
        connect_status, revert_dict, revert_plugin_status = connect_to_interface(obj, connection)
        if connect_status == "SUCCESS":
            if initial_connection == "":
                initial_connection = revert_dict.pop("current_if")
                revert_if  = revert_dict.pop("revert_if")
                if revert_plugin_status == "YES":
                    revert_plugins_dict.update(revert_dict)
            tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
            tdkTestObj.addParameter("method","org.rdk.Network.1.isConnectedToInternet")
            tdkTestObj.addParameter("reqValue","connectedToInternet")
            tdkTestObj.executeTestCase(expectedResult)
            connected = tdkTestObj.getResultDetails()
            connected_status = tdkTestObj.getResult()
            if expectedResult in connected_status :
                print "\n Successfully executed isConnectedToInternet method"
                print "\n Result of isConnectedToInternet method for {} connection:{}".format(connection,connected)
                if connected:
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while executing isConnectedToInternet method"
                tdkTestObj.setResultStatus("FAILURE")
                break
        else:
            print "\n Error while setting {} as default interface".format(connection)
            obj.setLoadModuleStatus("FAILURE")
            break
    if initial_connection != "":
        reconnect_status, revert_dict, revert_plugin_status = connect_to_interface(obj,initial_connection )
    if revert_plugins_dict != {}:
        status = set_plugins_status(obj,revert_plugins_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
