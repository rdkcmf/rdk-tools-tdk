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
  <name>WIFI_HAL_2.4GHzGetRadioStandard</name>
  <primitive_test_id/>
  <primitive_test_name>WIFI_HAL_GetOrSetRadioStandard</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To get the radio standard for 2.4GHz and check if the values are present in supported radio standards</synopsis>
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
    <test_case_id>TC_WIFI_HAL_33</test_case_id>
    <test_objective>To get the radio standard for 2.4GHz and check if the values are present in supported radio standards</test_objective>
    <test_type>Positive</test_type>
    <test_setup>IPClient-Wifi</test_setup>
    <pre_requisite>1.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>wifi_getRadioSupportedStandards
wifi_getRadioStandard
</api_or_interface_used>
    <input_parameters>radioIndex : 0
methodName : getRadioStandard
methodName : getRadioSupportedStandards
</input_parameters>
    <automation_approch>1.Load the module
2.Check if the DUT is connected to the required SSID, if not do the connection using wifi_connectEndpoint().
3.Invoke wifi_getRadioStandard() api to get the radio standards
4. Invoke wifi_getRadioSupportedStandards() api to get the supported radio standards
5. Compare the values returned
6. If the radio standards are present in supported radio standards, return SUCCESS,else FAILURE.
7.Unload the module,</automation_approch>
    <except_output>Radio standards should be present in supported radio standards</except_output>
    <priority>High</priority>
    <test_stub_interface>WIFIHAL</test_stub_interface>
    <test_script>WIFI_HAL_2.4GHzGetRadioStandard</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
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
obj.configureTestCase(ip,port,'WIFI_HAL_2.4GHzGetRadioStandard');

#Get the result of connection with test component and DUT
loadmodulestatus =obj.getLoadModuleResult();

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    radioIndex = 0
    connectresult = isConnectedtoSSID(obj,radioIndex);
    if "TRUE" in connectresult:
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('WIFI_HAL_GetOrSetRadioStandard');
        #Giving the method name to invoke the api for getting radio standards ie,wifi_getRadioStandards()
        tdkTestObj.addParameter("methodName","getRadioStandard");
        #Radio index is 0 for 2.4GHz and 1 for 5GHz
        tdkTestObj.addParameter("radioIndex",0);
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedresult in actualresult:
            print details
            output = details.split(":")[1].split(",gOnly")[0].split("=")[1].split(",");
            radioStds = [s.strip() for s in output];
            tdkTestObj.setResultStatus("SUCCESS");
            print "TEST STEP 1: Get the Radio Standards for 5GHz";
            print "EXPECTED RESULT 1: Should get the Radio Standards for 5GHz";
            print "ACTUAL RESULT 1: %s" %output
            #Get the result of execution
            print "[TEST EXECUTION RESULT] : SUCCESS";

            #Script to load the configuration file of the component
            tdkTestObj = obj.createTestStep("WIFI_HAL_GetOrSetParamStringValue");
            #Giving the method name to invoke the api for getting radio supported standards ie,wifi_getRadioSupportedStandards()
            tdkTestObj.addParameter("methodName","getRadioSupportedStandards");
            #Radio index is 0 for 2.4GHz and 1 for 5GHz
            tdkTestObj.addParameter("radioIndex",0);
            expectedresult="SUCCESS";
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            print "details:",details
            if expectedresult in actualresult:
                List = details.split(":")[1].split(",");
                SupportedStds = [s.strip() for s in List];
                #Set the result status of execution
                tdkTestObj.setResultStatus("SUCCESS");
                print "TEST STEP 2: Get the Radio Supported Standards for 5GHz";
                print "EXPECTED RESULT 2: Should get the Radio Supported Standards for 5GHz";
                print "ACTUAL RESULT 2: %s" %SupportedStds;
                #Get the result of execution
                print "[TEST EXECUTION RESULT] : SUCCESS";

                if set(radioStds).issubset(SupportedStds):
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "TEST STEP 3: Check if the current radio standard is present in supported radio standard list"
                    print "EXPECTED RESULT 3 :The current radio standard should be present in supported standard list"
                    print "ACTUAL RESULT 3 : Radio standard is present in supported standard list"
                    print "Radio Standards: %s"%radioStds
                    print"Supported Radio Standards :%s"%SupportedStds
                    #Get the result of execution
                    print "[TEST EXECUTION RESULT] : SUCCESS";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "TEST STEP 3: Check if the current radio standard is present in supported radio standard list"
                    print "EXPECTED RESULT 3 :The current radio standard should be present in supported standard list"
                    print "ACTUAL RESULT 3 : Radio standard is not present in supported standard list"
                    print "Radio Standards: %s"%radioStds
                    print"Supported Radio Standards :%s"%SupportedStds
                    #Get the result of execution
                    print "[TEST EXECUTION RESULT] : FAILURE";
            else:
                #Set the result status of execution
                tdkTestObj.setResultStatus("FAILURE");
                print "TEST STEP 1: Get the Radio Supported Standards for 5GHz";
                print "EXPECTED RESULT 1: Should get the Radio Supported Standards for 5GHz";
                print "ACTUAL RESULT 1: %s" %SupportedStds;
                #Get the result of execution
                print "[TEST EXECUTION RESULT] : FAILURE";
        else:
            print "wifi_getRadioStandards() api call failed"
            #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print "Connecting to SSID operation failed"

    obj.unloadModule("wifihal");
else:
    print "Failed to load the module";
    obj.setLoadModuleStatus("FAILURE");
    print "Module loading failed";

