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
  <name>WIFI_HAL_DisconnectEndPoint_WithoutSaveSSID</name>
  <primitive_test_id/>
  <primitive_test_name>WIFI_HAL_DisconnectEndpoint</primitive_test_name>
  <primitive_test_version>3</primitive_test_version>
  <status>FREE</status>
  <synopsis>To connected the endpoint without saving the SSID, disconnect the connected endpoint and check if the last connected end point is updated or not</synopsis>
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
    <test_case_id>TC_WIFI_HAL_30</test_case_id>
    <test_objective>To connect the end point with saveSSID flag as false, disconnect the endpoint and verify that the details about the end point are not saved in the lastConnected endpoint details</test_objective>
    <test_type>Positive</test_type>
    <test_setup>IPClient-Wifi,Video_Accelerator</test_setup>
    <pre_requisite>"1.TDK Agent should be in running state or invoke it through StartTdk.sh script"</pre_requisite>
    <api_or_interface_used>wifi_connectEndpoint
wifi_disconnectEndpoint
wifi_lastConnected_Endpoint</api_or_interface_used>
    <input_parameters>radioIndex,ssid,security_mode,WEPKey,PreSharedKey,KeyPassphrase,
saveSSID = 0</input_parameters>
    <automation_approch>"1.Load the module.
2.Using WIFI_HAL_ConnectEndpoint, invoke wifi_connectEndpoint() api and connect to the default access point with saveSSID = 1
3. Using WIFI_HAL_ConnectEndpoint, invoke wifi_connectEndpoint() api and connect to a new access point with saveSSID = 0
4.Using WIFI_HAL_DisconnectEndpoint, invoke wifi_disconnectEndpoint() api
5.Using WIFI_HAL_LastConnected_Endpoint, invoke wifi_lastConnected_Endpoint() and get the last connected end point details
6.If the ssid details returned wifi_lastConnected_Endpoint() and the connected SSID details are different, then return SUCCESS,else FAILURE.
7.Unload the module."</automation_approch>
    <except_output>ssid details returned from wifi_lastConnected_Endpoint() and the connected SSID details should be different</except_output>
    <priority>High</priority>
    <test_stub_interface>WIFIHAL</test_stub_interface>
    <test_script>WIFI_HAL_DisconnectEndPoint_WithoutSaveSSID</test_script>
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
obj.configureTestCase(ip,port,'WIFI_HAL_DisconnectEndPoint_WithoutSaveSSID');

#Get the result of connection with test component and DUT
loadmodulestatus =obj.getLoadModuleResult();

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");

    parseStatus = parseDeviceConfig(obj);

    #Script to load the configuration file of the component
    #Connect ans save the SSID details
    print "TEST STEP 1 : Initiate connection to Access Point A using wifi_connectEndpoint()"
    print "EXPECTED RESULT : Connection initiation should be success"
    tdkTestObj = obj.createTestStep("WIFI_HAL_ConnectEndpoint");
    tdkTestObj.addParameter("radioIndex",1);
    tdkTestObj.addParameter("ssid",tdkvWifiUtility.ssid_5ghz_name);
    tdkTestObj.addParameter("security_mode",int(tdkvWifiUtility.ap_5ghz_security_mode));
    tdkTestObj.addParameter("WEPKey",tdkvWifiUtility.ap_5ghz_wep_key);
    tdkTestObj.addParameter("PreSharedKey",tdkvWifiUtility.ap_5ghz_preshared_key);
    tdkTestObj.addParameter("KeyPassphrase",tdkvWifiUtility.ap_5ghz_key_passphrase);
    tdkTestObj.addParameter("saveSSID",1);
    expectedresult = "SUCCESS";
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "Connecting to an AP by saving the SSID details"
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "ACTUAL RESULT  : Connection to %s initiated successfully" %(tdkvWifiUtility.ssid_5ghz_name)
        print "Value Returned : %s\n" %(details)

        # Getting current station connection status after 15 seconds
        sleep(15);
        print "TEST STEP 2 : Invoke wifi_getStats to get the connection status"
        print "EXPECTED RESULT : Should get the details of connected station"
        tdkTestObj = obj.createTestStep("WIFI_HAL_GetStats");
        tdkTestObj.addParameter("radioIndex",1);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedresult in actualresult:
            SSID_GET = details.split(":")[1].split(",")[0].split("=")[1];
            if SSID_GET == tdkvWifiUtility.ssid_5ghz_name:
                tdkTestObj.setResultStatus("SUCCESS");
                print "ACTUAL RESULT  : Connected to %s successfully" %(tdkvWifiUtility.ssid_5ghz_name)
                print "Value Returned : %s\n" %(details)

                print "TEST STEP 3 : Initiate connection to Access Point B using wifi_connectEndpoint()"
                print "EXPECTED RESULT : Connection initiation should be success"
                tdkTestObj = obj.createTestStep("WIFI_HAL_ConnectEndpoint");
                tdkTestObj.addParameter("radioIndex",1);
                tdkTestObj.addParameter("ssid",tdkvWifiUtility.ssid_5ghz_name_new);
                tdkTestObj.addParameter("security_mode",int(tdkvWifiUtility.ap_5ghz_security_mode_new));
                tdkTestObj.addParameter("WEPKey",tdkvWifiUtility.ap_5ghz_wep_key_new);
                tdkTestObj.addParameter("PreSharedKey",tdkvWifiUtility.ap_5ghz_preshared_key_new);
                tdkTestObj.addParameter("KeyPassphrase",tdkvWifiUtility.ap_5ghz_key_passphrase_new);
                tdkTestObj.addParameter("saveSSID",0);
                expectedresult = "SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                print "Connecting to an AP without saving the SSID details"
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "ACTUAL RESULT  : Connection to %s initiated successfully" %(tdkvWifiUtility.ssid_5ghz_name_new)
                    print "Value Returned : %s\n" %(details)

                    # Getting current station connection status after 15 seconds
                    sleep(15);
                    print "TEST STEP 4 : Invoke wifi_getStats to get the connection status"
                    print "EXPECTED RESULT : Should get the details of connected station"
                    tdkTestObj = obj.createTestStep("WIFI_HAL_GetStats");
                    tdkTestObj.addParameter("radioIndex",1);
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    if expectedresult in actualresult:
                        SSID_GET = details.split(":")[1].split(",")[0].split("=")[1];
                        if SSID_GET == tdkvWifiUtility.ssid_5ghz_name_new:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "ACTUAL RESULT  : Connected to %s successfully" %(tdkvWifiUtility.ssid_5ghz_name_new)
                            print "Value Returned : %s\n" %(details)

                            print "TEST STEP 5 : Invoke wifi_disconnectEndpoint to diconnect Access Point A"
                            print "EXPECTED RESULT : Should get disconnected from the end-point"
                            tdkTestObj = obj.createTestStep("WIFI_HAL_DisconnectEndpoint")
                            tdkTestObj.addParameter("radioIndex",1);
                            tdkTestObj.addParameter("ssid",tdkvWifiUtility.ssid_5ghz_name);
                            expectedresult = "SUCCESS";
                            tdkTestObj.executeTestCase(expectedresult);
                            actualresult = tdkTestObj.getResult();
                            details = tdkTestObj.getResultDetails();
                            if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "ACTUAL RESULT  : Disconnected from End Point: SSID: %s" %(tdkvWifiUtility.ssid_5ghz_name)
                                print "Value Returned : %s\n" %(details)

                                print "TEST STEP 6 : Check wifi_lastConnected_Endpoint results"
                                print "EXPECTED RESULT : wifi_lastConnected_Endpoint results should not have details of Access Point B"
                                tdkTestObj = obj.createTestStep("WIFI_HAL_LastConnected_Endpoint");
                                expectedresult = "SUCCESS";
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details = tdkTestObj.getResultDetails();
                                if expectedresult in actualresult:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    details = details.split(":",1)[1].strip().split(",");
                                    detailsList = [i.split('=', 1)[1] for i in details]
                                    print "Last connected details: ", details
                                    if tdkvWifiUtility.ssid_5ghz_name_new not in detailsList and tdkvWifiUtility.ap_5ghz_key_passphrase_new not in detailsList:
                                        print "ACTUAL RESULT : The SSID details are not the same"
                                        print "Value Returned : %s" %(details)
                                        print "[TEST EXECUTION RESULT] : SUCCESS\n"
                                        tdkTestObj.setResultStatus("SUCCESS");
                                    else:
                                        print "ACTUAL RESULT : The SSID details are the same"
                                        print "Value Returned : %s" %(details)
                                        print "[TEST EXECUTION RESULT] : FAILURE\n"
                                        tdkTestObj.setResultStatus("FAILURE");
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "ACTUAL RESULT : ",details
                                    print "[TEST EXECUTION RESULT] : FAILURE"
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "ACTUAL RESULT : ",details
                                print "[TEST EXECUTION RESULT] : FAILURE"
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "ACTUAL RESULT  : Connection to %s Failed" %(tdkvWifiUtility.ssid_5ghz_name_new)
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
                print "ACTUAL RESULT  : Connection to %s Failed" %(tdkvWifiUtility.ssid_5ghz_name)
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

    obj.unloadModule("wifihal");
else:
    print "Failed to load the module";
    obj.setLoadModuleStatus("FAILURE");
    print "Module loading failed";


