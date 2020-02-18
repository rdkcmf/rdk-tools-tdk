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
  <name>WIFI_HAL_CheckEndPointReassociation</name>
  <primitive_test_id/>
  <primitive_test_name>WIFI_HAL_ConnectEndpoint</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Invoke wifi_connectEndpoint() to connect to End point A , check the connection status using wifi_getStats. Then try to connect to same End point A and verify re-association</synopsis>
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
    <test_case_id>TC_WIFI_HAL_42</test_case_id>
    <test_objective>Invoke wifi_connectEndpoint() to connect to End point A , check the connection status using wifi_getStats. Then try to connect to same End point A and verify re-association</test_objective>
    <test_type>Positive</test_type>
    <test_setup>IPClient-Wifi</test_setup>
    <pre_requisite>"1.TDK Agent should be in running state or invoke it through StartTdk.sh script"</pre_requisite>
    <api_or_interface_used>wifi_getRadioSupportedFrequencyBands
wifi_connectEndpoint
wifi_getStats</api_or_interface_used>
    <input_parameters>radioIndex,ssid,security_mode,WEPKey,PreSharedKey,KeyPassphrase,
saveSSID = 1</input_parameters>
    <automation_approch>"1.Load the module.
2.Using getRadioSupportedFrequencyBands identify the End-Point to be connected (2.4GHz/5GHz)
3.Using WIFI_HAL_ConnectEndpoint, invoke wifi_connectEndpoint() api and connect to the default access point with saveSSID = 1
4. Using WIFI_HAL_GetStats check the connection status
5.If connected to End-Point, try to connect to same End Point using WIFI_HAL_ConnectEndpoint
6. Check the WIFI_HAL_GetStats to verify whether re-association is completed.
7.Update the verification status
8.Unload the module."</automation_approch>
    <expected_output>Re-association should be successful</expected_output>
    <priority>High</priority>
    <test_stub_interface>WIFIHAL</test_stub_interface>
    <test_script>WIFI_HAL_CheckEndPointReassociation</test_script>
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
obj.configureTestCase(ip,port,'WIFI_HAL_CheckEndPointReassociation');

#Get the result of connection with test component and DUT
loadmodulestatus =obj.getLoadModuleResult();

if "SUCCESS" in loadmodulestatus.upper():
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
            ssid = tdkvWifiUtility.ssid_5ghz_name;
            radioIndex = 1;
            securityMode = int(tdkvWifiUtility.ap_5ghz_security_mode);
            WEPKey = tdkvWifiUtility.ap_5ghz_wep_key;
            preSharedKey = tdkvWifiUtility.ap_5ghz_preshared_key;
            keyPassPhrase = tdkvWifiUtility.ap_5ghz_key_passphrase;
        else:
            ssid = tdkvWifiUtility.ssid_2ghz_name;
            radioIndex = 0;
            securityMode = int(tdkvWifiUtility.ap_2ghz_security_mode);
            WEPKey = tdkvWifiUtility.ap_2ghz_wep_key;
            preSharedKey = tdkvWifiUtility.ap_2ghz_preshared_key;
            keyPassPhrase = tdkvWifiUtility.ap_2ghz_key_passphrase;

        print "End Point Chosen based on Frequency Band : %s\n" %(ssid)

        #Connect ans save the SSID details
        print "TEST STEP 2 : Initiate connection to Access Point A using wifi_connectEndpoint()"
        print "EXPECTED RESULT : Connection initiation should be success"
        tdkTestObj = obj.createTestStep("WIFI_HAL_ConnectEndpoint");
        tdkTestObj.addParameter("radioIndex",radioIndex);
        tdkTestObj.addParameter("ssid",ssid);
        tdkTestObj.addParameter("security_mode",securityMode);
        tdkTestObj.addParameter("WEPKey",WEPKey);
        tdkTestObj.addParameter("PreSharedKey",preSharedKey);
        tdkTestObj.addParameter("KeyPassphrase",keyPassPhrase);
        tdkTestObj.addParameter("saveSSID",1);
        expectedresult = "SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");
            print "ACTUAL RESULT  : Connection to %s initiated successfully" %(ssid)
            print "Value Returned : %s\n" %(details)

            # Getting current station connection status after 15 seconds
            sleep(15);
            print "TEST STEP 3 : Invoke wifi_getStats to get the connection status"
            print "EXPECTED RESULT : Should get the details of connected station"
            tdkTestObj = obj.createTestStep("WIFI_HAL_GetStats");
            tdkTestObj.addParameter("radioIndex",radioIndex);
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            if expectedresult in actualresult:
                SSID_GET = details.split(":")[1].split(",")[0].split("=")[1];
                if SSID_GET == ssid:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "ACTUAL RESULT  : Connected to %s successfully" %(ssid)
                    print "Value Returned : %s\n" %(details)

                    print "TEST STEP 4 : Initiate connection to Access Point A using wifi_connectEndpoint()"
                    print "EXPECTED RESULT : Connection initiation should be success"
                    tdkTestObj = obj.createTestStep("WIFI_HAL_ConnectEndpoint");
                    tdkTestObj.addParameter("radioIndex",radioIndex);
                    tdkTestObj.addParameter("ssid",ssid);
                    tdkTestObj.addParameter("security_mode",securityMode);
                    tdkTestObj.addParameter("WEPKey",WEPKey);
                    tdkTestObj.addParameter("PreSharedKey",preSharedKey);
                    tdkTestObj.addParameter("KeyPassphrase",keyPassPhrase);
                    tdkTestObj.addParameter("saveSSID",1);
                    expectedresult = "SUCCESS";
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "ACTUAL RESULT  : Connection to %s initiated successfully" %(ssid)
                        print "Value Returned : %s\n" %(details)

                        # Getting current station connection status after 15 seconds
                        sleep(15);
                        print "TEST STEP 5 : Invoke wifi_getStats to get the connection status"
                        print "EXPECTED RESULT : Should get the details of connected station"
                        tdkTestObj = obj.createTestStep("WIFI_HAL_GetStats");
                        tdkTestObj.addParameter("radioIndex",radioIndex);
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details = tdkTestObj.getResultDetails();
                        if expectedresult in actualresult:
                            SSID_GET = details.split(":")[1].split(",")[0].split("=")[1];
                            if SSID_GET == ssid:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "ACTUAL RESULT  : Re-associated to %s successfully" %(ssid)
                                print "Value Returned : %s\n" %(details)
                                print "[TEST EXECUTION RESULT] : SUCCESS"

                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "ACTUAL RESULT  : Re-association to %s Failed" %(ssid)
                                print "Value Returned : %s\n" %(details)
                                print "[TEST EXECUTION RESULT] : FAILURE"
                        else:
                           tdkTestObj.setResultStatus("FAILURE");
                           print "ACTUAL RESULT : wifi_getStats operation failed"
                           print "[TEST EXECUTION RESULT] : FAILURE"
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "ACTUAL RESULT : ",details
                        print "[TEST EXECUTION RESULT] : FAILURE"
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "ACTUAL RESULT  : Connection to %s Failed" %(ssid)
                    print "Value Returned : %s\n" %(details)
                    print "[TEST EXECUTION RESULT] : FAILURE"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "ACTUAL RESULT : wifi_getStats operation failed"
                print "[TEST EXECUTION RESULT] : FAILURE"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "ACTUAL RESULT : ",details
            print "[TEST EXECUTION RESULT] : FAILURE"
    else:
        print "wifi_getRadioSupportedFrequencyBands() operation failed"
        print "[TEST EXECUTION RESULT] : FAILURE"
        tdkTestObj.setResultStatus("FAILURE");

    obj.unloadModule("wifihal");
else:
    print "Failed to load the module";
    obj.setLoadModuleStatus("FAILURE");
    print "Module loading failed";

