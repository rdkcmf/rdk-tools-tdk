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
  <name>WIFI_HAL_5GHzSetRadioScanningFreqList</name>
  <primitive_test_id/>
  <primitive_test_name>WIFI_HAL_SetRadioScanningFreqList</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To invoke wifi_setRadioScanningFreqList() api with radio index 1 to set the radio scanning frequency list</synopsis>
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
    <test_case_id>TC_WIFI_HAL_39</test_case_id>
    <test_objective>To invoke wifi_setRadioScanningFreqList() api with radio index 1 to set the radio scanning frequency list</test_objective>
    <test_type>Positive</test_type>
    <test_setup>IPClient-Wifi</test_setup>
    <pre_requisite>1.TDK Agent should be in running state or invoke it through StartTdk.sh script.</pre_requisite>
    <api_or_interface_used>wifi_getRadioSupportedFrequencyBands()
wifi_setRadioScanningFreqList()
wifi_getNeighboringWiFiDiagnosticResult()</api_or_interface_used>
    <input_parameters>radioIndex : 1
freqList : list of frequency to be set</input_parameters>
    <automation_approch>1.Load the module.
2.Invoke wifi_getRadioSupportedFrequencyBands() to check whether 5GHz frequency band is supported.
3.If 5GHz is supported, invoke wifi_setRadioScanningFreqList() api with radio index 1 and list of frequency to be set
4. Invoke wifi_getNeighboringWiFiDiagnosticResult() to get the list of APs with those channels
5.Update test results based on validation
6.Unload the module.</automation_approch>
    <expected_output>Neighboring AP details with the channels set</expected_output>
    <priority>High</priority>
    <test_stub_interface>WIFI_HAL</test_stub_interface>
    <test_script>WIFI_HAL_5GHzSetRadioScanningFreqList</test_script>
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
obj.configureTestCase(ip,port,'WIFI_HAL_5GHzSetRadioScanningFreqList');

#Get the result of connection with test component and DUT
loadmodulestatus =obj.getLoadModuleResult();

if "SUCCESS" in loadmodulestatus.upper():
    expectedresult="SUCCESS";
    obj.setLoadModuleStatus("SUCCESS");
    parseStatus = parseDeviceConfig(obj);
    #Getting Supported Frequency Bands
    print "\nTEST STEP 1: To invoke the wifi_getRadioSupportedFrequencyBands() to get frequency bands";
    print "EXPECTED RESULT : Should get details of supported frequency bands";
    tdkTestObj = obj.createTestStep("WIFI_HAL_GetOrSetParamStringValue");
    tdkTestObj.addParameter("methodName","getRadioSupportedFrequencyBands");
    tdkTestObj.addParameter("radioIndex",1);
    expectedresult="SUCCESS";
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS");
        SupportedFrequencyBands = details.split(":")[1].strip(" ");
        print "ACTUAL RESULT : Supported Frequency Bands = ",SupportedFrequencyBands;
        if "5GHz" in SupportedFrequencyBands:
            #Setting the radio scanning frequency list
            print "\nTEST STEP 2: To invoke the api wifi_setRadioScanningFreqList() to set the radio scanning frequency list";
            print "EXPECTED RESULT : Should set the radio scanning frequency list successfully";
            tdkTestObj = obj.createTestStep("WIFI_HAL_SetRadioScanningFreqList");
            tdkTestObj.addParameter("radioIndex",1);
            tdkTestObj.addParameter("freqList",tdkvWifiUtility.set_5ghz_freq_list);
            expectedresult="SUCCESS";
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            print "FREQ LIST TO BE SET : ",tdkvWifiUtility.set_5ghz_freq_list
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "ACTUAL RESULT : ",details
                print "[TEST EXECUTION RESULT]: SUCCESS"
                #Getting Neighboring Access Points with the channel set
                print "\nTEST STEP 3: To invoke the api wifi_getNeighboringWiFiDiagnosticResult() to get Neighboring APs";
                print "EXPECTED RESULT : Should get the neighbor wifi diagnostic";
                tdkTestObj = obj.createTestStep('WIFI_HAL_GetNeighboringWiFiDiagnosticResult');
                tdkTestObj.addParameter("radioIndex",1);
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "ACTUAL RESULT : Gets the neighbor wifi diagnostic successfully"
                    if "SSID" in details and "Band" in details:
                        neighborAPInfo = details.split("|")
                        print "Neighboring AP Info:"
                        for AP in neighborAPInfo:
                            print AP
                    else:
                        print "Neighboring AP Info : %s" %details;
                    print "[TEST EXECUTION RESULT] : SUCCESS";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "ACTUAL RESULT : ",details
                    print "[TEST EXECUTION RESULT] : FAILURE";
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "ACTUAL RESULT : ",details
                print "[TEST EXECUTION RESULT]: FAILURE"
        else:
            print "Frequency band 5GHz not supported : Skipping setRadioScanningFreqList validation"
            print "[TEST EXECUTION RESULT] : SUCCESS";
            tdkTestObj.setResultStatus("SUCCESS");
    else:
        print "wifi_getRadioSupportedFrequencyBands() operation failed"
        print "[TEST EXECUTION RESULT] : FAILURE"
        tdkTestObj.setResultStatus("FAILURE");

    obj.unloadModule("wifihal");
else:
    print "Failed to load the module";
    obj.setLoadModuleStatus("FAILURE");
    print "Module loading failed";


