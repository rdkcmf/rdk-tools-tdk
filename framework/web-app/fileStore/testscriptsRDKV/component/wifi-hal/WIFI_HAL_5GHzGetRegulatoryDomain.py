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
  <version>2</version>
  <name>WIFI_HAL_5GHzGetRegulatoryDomain</name>
  <primitive_test_id/>
  <primitive_test_name>WIFI_HAL_GetOrSetParamStringValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To get the Access Point Regulatory domain.</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-Wifi</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_WIFI_HAL_10</test_case_id>
    <test_objective>To get the Access Point Regulatory domain and check that it does not return a NULL value.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>IPClient-Wifi,Video_Accelerator</test_setup>
    <pre_requisite>1.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>wifi_getRegulatoryDomain()
</api_or_interface_used>
    <input_parameters>methodName : getRegulatoryDomain
radioIndex : 1</input_parameters>
    <automation_approch>1.Load the module.
2.Invoke the api wifi_getRegulatoryDomain() and get the Access Point Regulatory Domain.
3.If the api returns a non empty regulatory domain value,return SUCCESS.
4.If it returns a NULL value,return FAILURE.
5.Unload the module.</automation_approch>
    <except_output>wifi_getRegulatoryDomain() api should return the Access Point Regulatory Domain.</except_output>
    <priority>High</priority>
    <test_stub_interface>WIFI_HAL</test_stub_interface>
    <test_script>WIFI_HAL_5GHzGetRegulatoryDomain</test_script>
    <skipped>No</skipped>
    <release_version>M61</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkvWifiUtility;
from tdkvWifiUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("wifihal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'WIFI_HAL_5GHzGetRegulatoryDomain');

#Get the result of connection with test component and DUT
loadmodulestatus =obj.getLoadModuleResult();

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult="SUCCESS";
    radioIndex = 1;
    #Script to load the configuration file of the component
    tdkTestObj = obj.createTestStep("WIFI_HAL_GetOrSetParamStringValue");
    #Giving the method name to invoke the api for getting the Access Point regulatory domain. ie,wifi_getRegulatoryDomain()
    tdkTestObj.addParameter("methodName","getRegulatoryDomain");
    #Radio index is 0 for 2.4GHz and 1 for 5GHz
    tdkTestObj.addParameter("radioIndex",1);
    expectedresult="SUCCESS";
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedresult in actualresult:
        RegulatoryDomain = details.split(":")[1].strip(" ");
        if RegulatoryDomain !="":
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS");
            print "TEST STEP 1 : Get the Access Point regulatory domain";
            print "EXPECTED RESULT 1 : Should get the Access Point regulatory domain";
            print "Access Point Regulatory Domain = ",RegulatoryDomain;
            #Get the result of execution
            print "[TEST EXECUTION RESULT] : SUCCESS";
        else:
            #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE");
            print "TEST STEP 1 : Get the Access Point regulatory domain";
            print "EXPECTED RESULT 1 : Should get the Access Point regulatory domain";
            print "Access Point Regulatory Domain = ",RegulatoryDomain;
            #Get the result of execution
            print "[TEST EXECUTION RESULT] : FAILURE";
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "wifi_getRegulatoryDomain() operation failed";

    obj.unloadModule("wifihal");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load wifi-hal module";
