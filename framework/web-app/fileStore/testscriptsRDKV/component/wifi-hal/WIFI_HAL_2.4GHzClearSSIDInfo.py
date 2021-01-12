##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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
  <name>WIFI_HAL_2.4GHzClearSSIDInfo</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>WIFI_HAL_ClearSSIDInfo</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To invoke wifi_clearSSIDInfo() api with radio Index 0 to clear the last connected AP info from wpa_supplicant.conf</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <box_type>IPClient-Wifi</box_type>
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_WIFI_HAL_40</test_case_id>
    <test_objective>To invoke wifi_clearSSIDInfo() api with radioIndex 0 to clear the last connected AP info from wpa_supplicant.conf</test_objective>
    <test_type>Positive</test_type>
    <test_setup>IPClient-Wifi</test_setup>
    <pre_requisite>1.TDK Agent should be in running state or invoke it through StartTdk.sh script.</pre_requisite>
    <api_or_interface_used>wifi_clearSSIDInfo()
wifi_lastConnected_Endpoint()
wifi_disconnectEndpoint()</api_or_interface_used>
    <input_parameters>radioIndex:0
ssid : 2ghz ssid name
</input_parameters>
    <automation_approch>1.Load the module.
2.Check if the DUT is connected to the required SSID, using wifi utility method isConnectedtoSSID.
3.If connected to end point, invoke wifi_clearSSIDInfo() to clear the conf file
4.Invoke wifi_lastConnected_Endpoint() to get the details of the last connected station
5. lastConnected_Endpoint results should be empty, since conf file is cleared
6.Unload the module.</automation_approch>
    <expected_output>lastConnected_Endpoint results should be empty after conf file clear operation</expected_output>
    <priority>High</priority>
    <test_stub_interface>WIFI_HAL</test_stub_interface>
    <test_script>WIFI_HAL_2.4GHzClearSSIDInfo</test_script>
    <skipped>No</skipped>
    <release_version>M74</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkvWifiUtility;
from tdkvWifiUtility import *;
import time;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("wifihal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'WIFI_HAL_2.4GHzClearSSIDInfo');

#Get the result of connection with test component and DUT
loadmodulestatus =obj.getLoadModuleResult();

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    radioIndex = 0
    connectresult = isConnectedtoSSID(obj,radioIndex);
    ssid = tdkvWifiUtility.ssid_2ghz_name;
    if "TRUE" in connectresult:
        print "TEST STEP 1 : To invoke wifi_clearSSIDInfo api to clear configuration";
        print "EXPECTED RESULT : Should clear ssid info from wpa_supplicant.conf";
        tdkTestObj = obj.createTestStep("WIFI_HAL_ClearSSIDInfo");
        tdkTestObj.addParameter("radioIndex",0);
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");
            print "ACTUAL RESULT  : wpa_supplicant.conf file cleared successfully"
            print "Value Returned : %s\n" %(details)

            print "TEST STEP 2 : To invoke wifi_lastConnected_Endpoint to get the Access point details";
            print "EXPECTED RESULT : Should return end point details";
            tdkTestObj = obj.createTestStep("WIFI_HAL_LastConnected_Endpoint");
            #Expected to get FIALURE since last cnnected ssid info is cleared.
            expectedresult = "FAILURE";
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "ACTUAL RESULT  : last connected end point info received"
                print "Value Returned : %s\n" %(details)

                print "TEST STEP 3 : Check wifi_lastConnected_Endpoint results"
                print "EXPECTED RESULT : wifi_lastConnected_Endpoint results should not have connected ssid info"
                if ssid not in details:
                    print "ACTUAL RESULT : clearSSIDInfo cleared configuration successfully"
                    print "[TEST EXECUTION RESULT] : SUCCESS\n"
                    tdkTestObj.setResultStatus("SUCCESS");
                else:
                    print "ACTUAL RESULT : clearSSIDInfo failed to clear configuration"
                    print "[TEST EXECUTION RESULT] : FAILURE\n"
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                print "ACTUAL RESULT : ",details
                print "[TEST EXECUTION RESULT] : FAILURE"
                tdkTestObj.setResultStatus("FAILURE");
        else:
            print "ACTUAL RESULT : ",details
            print "[TEST EXECUTION RESULT] : FAILURE"
            tdkTestObj.setResultStatus("FAILURE");

        # Disconnecting from the connected End Point, since conf file is cleared as
        # part of this test
        print "Disconnect from the End Point : SSID : ",ssid
        tdkTestObj = obj.createTestStep("WIFI_HAL_DisconnectEndpoint")
        tdkTestObj.addParameter("radioIndex",0);
        tdkTestObj.addParameter("ssid",ssid);
        expectedresult = "SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print details
        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            tdkTestObj.setResultStatus("FAILURE");

    else:
        print "Connecting to SSID operation failed"
        print "[TEST EXECUTION RESULT] : FAILURE"

    obj.unloadModule("wifihal");
else:
    print "Failed to load the module";
    obj.setLoadModuleStatus("FAILURE");
    print "Module loading failed";


