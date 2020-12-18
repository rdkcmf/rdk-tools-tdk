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
<?xml version="1.0" encoding="UTF-8"?>
<xml>
  <id/>
  <version>1</version>
  <name>WIFI_HAL_GetDualBandSupport</name>
  <primitive_test_id/>
  <primitive_test_name>WIFI_HAL_GetDualBandSupport</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To invoke wif_getDualBandSupport() api and check whether device supports dual band or not</synopsis>
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
    <test_case_id>TC_WIFI_HAL_34</test_case_id>
    <test_objective>To invoke wif_getDualBandSupport() api and check  whether the device supports dual band or not</test_objective>
    <test_type>Positive</test_type>
    <test_setup>IPClient-Wifi</test_setup>
    <pre_requisite>1.TDK Agent should be in running state or invoke it through StartTdk.sh script.</pre_requisite>
    <api_or_interface_used>wif_getDualBandSupport()
wifi_getRadioSupportedFrequencyBands()</api_or_interface_used>
    <input_parameters>methodName : getDualBandSupport</input_parameters>
    <automation_approch>1.Load the module.
2.Invoke wif_getDualBandSupport() api to get dual band support status.
3.API returns 1 if device supports dual band or 0 if the device does not dual band
4.Invoke wifi_getRadioSupportedFrequencyBands() to get the supported bands
5.Supported bands should be both 2.4 and 5 GHz if dual band support is true else either one frequency band
6.Update test results
7.Unload the module.</automation_approch>
    <expected_output>Dual band support status of the device</expected_output>
    <priority>High</priority>
    <test_stub_interface>WIFI_HAL</test_stub_interface>
    <test_script>WIFI_HAL_GetDualBandSupport</test_script>
    <skipped>No</skipped>
    <release_version>M74</release_version>
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
obj.configureTestCase(ip,port,'WIFI_HAL_GetDualBandSupport');

#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();

if "SUCCESS" in loadmodulestatus.upper():
    expectedresult="SUCCESS";
    obj.setLoadModuleStatus("SUCCESS");
    print "\nTEST STEP 1: To invoke the api wif_getDualBandSupport() to check whether device supports dual band";
    print "EXPECTED RESULT : Should get dual band support status";
    tdkTestObj = obj.createTestStep("WIFI_HAL_GetDualBandSupport");
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if ":" in details and details.split(":")[1].strip(" "):
        tdkTestObj.setResultStatus("SUCCESS");
        dualBandSupport = details.split(":")[1].strip(" ");
        if int(dualBandSupport) == 1:
            print "ACTUAL RESULT  : TRUE";
            print "Value returned : ",details;
            print "[TEST EXECUTION RESULT] : SUCCESS"
        else:
            print "ACTUAL RESULT  : FALSE";
            print "Value returned : ",details;
            print "[TEST EXECUTION RESULT] : SUCCESS"

        #Getting Supported Frequency Bands
        print "\nTEST STEP 2: To invoke the wifi_getRadioSupportedFrequencyBands() to get frequency bands";
        print "EXPECTED RESULT : Should get details of supported frequency bands";
        tdkTestObj = obj.createTestStep("WIFI_HAL_GetOrSetParamStringValue");
        tdkTestObj.addParameter("methodName","getRadioSupportedFrequencyBands");
        tdkTestObj.addParameter("radioIndex",0);
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");
            SupportedFrequencyBands = details.split(":")[1].strip(" ");
            print "ACTUAL RESULT : Supported Frequency Bands = ",SupportedFrequencyBands;

            print "\nTEST STEP 3: Validate getDualBandSupport using getRadioSupportedFrequencyBands";
            print "EXPECTED RESULT : supported bands should be both 2.4 & 5 GHz if dual band or either 2.4 or 5 GHz"
            if int(dualBandSupport) == 1 and "2.4GHz" in SupportedFrequencyBands and "5GHz" in SupportedFrequencyBands:
                print "ACTUAL RESULT : DUAL BAND : Supported Bands : ",SupportedFrequencyBands
                print "[TEST EXECUTION RESULT] : SUCCESS"
                tdkTestObj.setResultStatus("SUCCESS");
            elif int(dualBandSupport) == 0 and ("2.4GHz" in SupportedFrequencyBands or "5GHz" in SupportedFrequencyBands):
                print "ACTUAL RESULT : NO DUAL BAND : Supported Band : ",SupportedFrequencyBands
                print "[TEST EXECUTION RESULT] : SUCCESS"
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                print "ACTUAL RESULT : Dual Band Support validation failed"
                print "[TEST EXECUTION RESULT] : FAILURE"
                tdkTestObj.setResultStatus("FAILURE");
        else:
            print "wifi_getRadioSupportedFrequencyBands() operation failed"
            print "[TEST EXECUTION RESULT] : FAILURE"
            tdkTestObj.setResultStatus("FAILURE");
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "wif_getDualBandSupport() operation failed";
        print "[TEST EXECUTION RESULT] : FAILURE"

    obj.unloadModule("wifihal");
else:
    print "Failed to load the module";
    obj.setLoadModuleStatus("FAILURE");
    print "Module loading failed";

