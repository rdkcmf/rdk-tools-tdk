##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2018 RDK Management
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
<?xml version="1.0" encoding="UTF-8"?>
<xml>
  <id/>
  <version>1</version>
  <name>WIFI_HAL_2.4GHzGetSSIDMACAddress</name>
  <primitive_test_id/>
  <primitive_test_name>WIFI_HAL_GetOrSetParamStringValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To get the SSID Mac Address and verify using BSSID.</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-Wifi</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_WIFI_HAL_24</test_case_id>
    <test_objective>To get the SSID Mac Address and verify using BSSID.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>IPClient-Wifi</test_setup>
    <pre_requisite>1.TDK Agent should be in running state or invoke it through StartTdk.sh script.</pre_requisite>
    <api_or_interface_used>wifi_getSSIDMACAddress()
wifi_getBaseBSSID()
wifi_connectEndpoint()</api_or_interface_used>
    <input_parameters>methodName : getSSIDMACAddress
methodName : getBaseBSSID
radioIndex : 0</input_parameters>
    <automation_approch>1.Load the module.
2.Check if the DUT is connected to the required SSID, if not do the connection using wifi_connectEndpoint().
3.Invoke the api wifi_getSSIDMACAddress() to get the SSID Mac Address.
4.Invoke the api wifi_getBaseBSSID() api to get the BSSID.
5.Check whether the values of SSID Mac Address and BSSID are same.
6.If same,return SUCCESS,else FAILURE.
7.Unload the module.</automation_approch>
    <except_output>The SSID Mac Address and BSSID values should be the same.</except_output>
    <priority>High</priority>
    <test_stub_interface>WIFI_HAL</test_stub_interface>
    <test_script>WIFI_HAL_2.4GHzGetSSIDMACAddress</test_script>
    <skipped>No</skipped>
    <release_version>M61</release_version>
    <remarks/>
  </test_cases>
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
obj.configureTestCase(ip,port,'WIFI_HAL_2.4GHzGetSSIDMACAddress');

#Get the result of connection with test component and DUT
loadmodulestatus =obj.getLoadModuleResult();

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    radioIndex = 0
    connectresult = isConnectedtoSSID(obj,radioIndex);
    if "TRUE" in connectresult:
        #Script to load the configuration file of the component
        tdkTestObj = obj.createTestStep("WIFI_HAL_GetOrSetParamStringValue");
        #Giving the method name to invoke the api for getting SSIDMAC Address ie,wifi_getSSIDMACAddress()
        tdkTestObj.addParameter("methodName","getSSIDMACAddress");
        #Radio index is 0 for 2.4GHz and 1 for 5GHz
        tdkTestObj.addParameter("radioIndex",0);
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "details:",details

        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");
            MacAddress = details.split(": ")[1].strip(" ");
            print "TEST STEP 1: Get the SSIDMACAddress"
            print "EXPECTED RESULT 1: Should get the SSIDMACAddress"
            print "ACTUAL RESULT 1: SSIDMACAddress = ",MacAddress
            print "TEST EXECUTION RESULT : SUCCESS"
            #Script to load the configuration file of the component
            tdkTestObj = obj.createTestStep("WIFI_HAL_GetOrSetParamStringValue");
            #Giving the method name to invoke the api for getting Base BSSID ie,wifi_getBaseBSSID()
            tdkTestObj.addParameter("methodName","getBaseBSSID");
            #Radio index is 0 for 2.4GHz and 1 for 5GHz
            tdkTestObj.addParameter("radioIndex",0);
            expectedresult="SUCCESS";
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            print "details:",details

            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                BSSID = details.split(": ")[1].strip(" ");
                print "TEST STEP 2: Get the BaseBSSID"
                print "EXPECTED RESULT 2: Should get the BaseBSSID"
                print "ACTUAL RESULT 2: BaseBSSID = ",BSSID
                if BSSID == MacAddress:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "TEST STEP: Comparing the values of SSID Mac Address and BSSID";
                    print "EXECUTION RESULT : SSID Mac Address and BSSID values should be the same";
                    print "ACTUAL RESULT : SSID Mac Address and BSSID values are the same";
                    print "SSID Mac Address is :%s"%MacAddress;
                    print "BSSID is :%s"%BSSID
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "TEST STEP: Comparing the values of SSID Mac Address and BSSID";
                    print "EXECUTION RESULT : SSID Mac Address and BSSID values should be the same";
                    print "ACTUAL RESULT : SSID Mac Address and BSSID values are NOT the same";
                    print "SSID Mac Address is :%s"%MacAddress;
                    print "BSSID is :%s"%BSSID
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "TEST STEP 2: Get the BaseBSSID"
                print "EXPECTED RESULT 2: Should get the BaseBSSID"
                print "ACTUAL RESULT 2: ",details
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "TEST STEP 1: Get the SSIDMACAddress"
            print "EXPECTED RESULT 1: Should get the SSIDMACAddress"
            print "ACTUAL RESULT 1: ",details
            print "TEST EXECUTION RESULT : FAILED"
    else:
        print "Connecting to SSID operation failed"

    obj.unloadModule("wifihal");
else:
    print "Failed to load the module";
    obj.setLoadModuleStatus("FAILURE");
    print "Module loading failed";
