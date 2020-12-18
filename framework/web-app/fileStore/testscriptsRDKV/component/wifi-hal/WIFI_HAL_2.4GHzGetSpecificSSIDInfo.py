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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>WIFI_HAL_2.4GHzGetSpecificSSIDInfo</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>WIFI_HAL_GetSpecificSSIDInfo</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To invoke wifi_getSpecificSSIDInfo()  with frequency band 1 [ 2.4 GHz ] to get the details of the Neighboring AP whose SSID matches with the provided SSID</synopsis>
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
    <test_case_id>TC_WIFI_HAL_36</test_case_id>
    <test_objective>To invoke wifi_getSpecificSSIDInfo()  with frequency band 1 [ 2.4 GHz ] to get the details of the Neighboring APs if its  SSID matches with the provided SSID</test_objective>
    <test_type>Positive</test_type>
    <test_setup>IPClient-Wifi</test_setup>
    <pre_requisite>1.TDK Agent should be in running state or invoke it through StartTdk.sh script.</pre_requisite>
    <api_or_interface_used>wifi_getNeighboringWiFiDiagnosticResult()
wifi_getRadioSupportedFrequencyBands()
wifi_getSpecificSSIDInfo()</api_or_interface_used>
    <input_parameters>ssid : ssid of the neighbor
band: frequency band</input_parameters>
    <automation_approch>1.Load the module.
2.Get the supported frequency bands using wifi_getRadioSupportedFrequencyBands()
2.If 2.4GHz is supported, Get the list of Neighboring APs using wifi_getNeighboringWiFiDiagnosticResult()
3.Invoke wifi_getSpecificSSIDInfo() api with frequency band 1 [ 2.4 GHz ] for all the ssid listed by wifi_getNeighboringWiFiDiagnosticResult()
5.wifi_getSpecificSSIDInfo() should provide  the info of all the Neighboring ssid
6.Update test results based on validation
7.Unload the module.</automation_approch>
    <expected_output>Neighboring AP details</expected_output>
    <priority>High</priority>
    <test_stub_interface>WIFI_HAL</test_stub_interface>
    <test_script>WIFI_HAL_2.4GHzGetSpecificSSIDInfo</test_script>
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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("wifihal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'WIFI_HAL_2.4GHzGetSpecificSSIDInfo');

#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();

if "SUCCESS" in loadmodulestatus.upper():
    expectedresult="SUCCESS";
    obj.setLoadModuleStatus("SUCCESS");
    #Getting Supported Frequency Bands
    print "\nTEST STEP 1: To invoke the wifi_getRadioSupportedFrequencyBands() to get frequency bands";
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
        #If 2.4GHz is supported, Getting the info of all the Neighboring Access Points
        if "2.4GHz" in SupportedFrequencyBands:
            #Getting the list of Access Points
            print "\nTEST STEP 2: To invoke the api wifi_getNeighboringWiFiDiagnosticResult() to get list of Neighboring AP";
            print "EXPECTED RESULT : Should get the list of neighboring ssid";
            tdkTestObj = obj.createTestStep('WIFI_HAL_GetNeighboringWiFiDiagnosticResult');
            tdkTestObj.addParameter("radioIndex",0);
            expectedresult="SUCCESS";
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                neighborAPInfo = details.split("|")
                neighborSSID = [ neighbor.split(",")[0].split("=")[1] for neighbor in neighborAPInfo]
                neighborSSID = [ ssid for ssid in neighborSSID if str(ssid).strip()]
                print "ACTUAL RESULT : No of Neighboring SSIDs  : ",len(neighborSSID)
                print "List of Neighboring SSID : ",neighborSSID
                print "\nTEST STEP 3: To invoke the api wifi_getSpecificSSIDInfo() to get info for all the neighbor ssid";
                print "EXPECTED RESULT : Should get details of Neighbor AP whose ssid matches with provided ssid";
                ssidCount = 0
                for ssid in neighborSSID:
                    tdkTestObj = obj.createTestStep("WIFI_HAL_GetSpecificSSIDInfo");
                    tdkTestObj.addParameter("ssid",ssid);
                    tdkTestObj.addParameter("band",1);
                    tdkTestObj.executeTestCase(expectedresult);
                    sleep(3);
                    actualresult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    ssidCount += 1
                    if expectedresult in actualresult:
                        if ssid in details:
                            print "SSID COUNT : ",ssidCount
                            print "ACTUAL RESULT  : SSID match for ",ssid;
                            print "Value returned : ",details;
                            print "[TEST EXECUTION RESULT] : SUCCESS\n"
                            tdkTestObj.setResultStatus("SUCCESS");
                        else:
                            print "SSID COUNT : ",ssidCount
                            print "ACTUAL RESULT  : No SSID match for ",ssid;
                            print "Value returned : ",details;
                            print "[TEST EXECUTION RESULT] : FAILURE\n"
                            tdkTestObj.setResultStatus("FAILURE");
                            break;
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "wifi_getSpecificSSIDInfo() operation failed";
                        print "[TEST EXECUTION RESULT] : FAILURE\n"
                        break;
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "wifi_getNeighboringWiFiDiagnosticResult() operation failed"
                print "[TEST EXECUTION RESULT] : FAILURE\n"
        else:
            print "Frequency band 2.4GHz not supported : Skipping wifi_getSpecificSSIDInfo() validation"
            print "[TEST EXECUTION RESULT] : SUCCESS\n"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "wifi_getRadioSupportedFrequencyBands() operation failed"
        print "[TEST EXECUTION RESULT] : FAILURE\n"

    obj.unloadModule("wifihal");
else:
    print "Failed to load the module";
    obj.setLoadModuleStatus("FAILURE");
    print "Module loading failed";


