##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2017 RDK Management
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
  <version>4</version>
  <name>Bluetooth_Persist_Set_Get_Discoverable_Timeout</name>
  <primitive_test_id/>
  <primitive_test_name>Bluetooth_IsAdapterDiscoverable</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check whether discoverable staus ON is  persisting or not after reboot</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
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
    <test_case_id>CT_BLUETOOTH_13</test_case_id>
    <test_objective>To check whether discoverable staus ON is  persisting or not after reboot</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI5</test_setup>
    <pre_requisite>1. Initialize the bluetooth manager
BTRMGR_Init();
2. Deinit the bluetooth manager after test
BTRMGR_DeInit();</pre_requisite>
    <api_or_interface_used>bool Bluetooth_IsAdapterDiscoverable
bool Bluetooth_SetAdapterDiscoverable</api_or_interface_used>
    <input_parameters>BTRMGR_IsAdapterDiscoverable(0,&amp;discoverableStatus);
BTRMGR_SetAdapterDiscoverable(0,discoverableStatus,Timeout);</input_parameters>
    <automation_approch>1. TM loads the Bluetooth agent via the test agent.
2  Bluetooth agent will invoke the api   BTRMGR_SetAdapterDiscoverable with discoverable status as ON and timeout as 300
3.Reboot the box
3.Check whether the discoverable status is set as OFF after reboot using BTRMGR_IsAdapterDiscoverable API</automation_approch>
    <except_output>Checkpoint 1.Verify the API call return value
Checkpoint 2.The adapter discoverable status should change to OFF after reboot</except_output>
    <priority>High</priority>
    <test_stub_interface>libbluetoothstub.so.0</test_stub_interface>
    <test_script>Bluetooth_Persist_Set_Get_Discoverable_Timeout</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from time import sleep

#Test component to be tested
bluetoothObj = tdklib.TDKScriptingLibrary("bluetooth","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
bluetoothObj.configureTestCase(ip,port,'Bluetooth_Persist_Set_Get_Discoverable_Timeout');

#Get the result of connection with test component and STB
bluetoothLoadStatus =bluetoothObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %bluetoothLoadStatus;
bluetoothObj.setLoadModuleStatus(bluetoothLoadStatus.upper());

if "SUCCESS" in bluetoothLoadStatus.upper():
 
    expectedresult="SUCCESS"
    print "Set the Bluetooth Discoverable status to ON (1)"
    discoverableStatus = "1"
    tdkTestObj = bluetoothObj.createTestStep('Bluetooth_SetAdapterDiscoverable');
    timeout = "300"
    tdkTestObj.addParameter("discoverablestatus",int(discoverableStatus))
    tdkTestObj.addParameter("timeout",int(timeout))
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    if actualresult == expectedresult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "Bluetooth_SetAdapterDiscoverable API Call is Successfull with status value as " , discoverableStatus ,"and timeout is " ,timeout

        print "Check whether the Discoverable status is set to ON (1)" 
        tdkTestObj = bluetoothObj.createTestStep('Bluetooth_IsAdapterDiscoverable')
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        discoverable = tdkTestObj.getResultDetails();
        print "RESULT : Bluetooth_IsAdapterDiscoverable : " , actualresult
        print "DETAILS : Bluetooth_IsAdapterDiscoverable : " , discoverable
        if actualresult == expectedresult:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Bluetooth_IsAdapterDiscoverable API Call is Success"
            if discoverable == discoverableStatus:
                tdkTestObj.setResultStatus("SUCCESS");
                print "Discoverable status changed to " , discoverable , "successfully"
                print "Reboot the box and check whether the discoverable status persists or not"
                #Reboot the STB
                bluetoothObj.initiateReboot();
                sleep(60);
                tdkTestObj = bluetoothObj.createTestStep('Bluetooth_IsAdapterDiscoverable')
                #Execute the test case in STB
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                discoverable = tdkTestObj.getResultDetails();
                print "RESULT : Bluetooth_IsAdapterDiscoverable : " , actualresult
                print "DETAILS : Bluetooth_IsAdapterDiscoverable : " , discoverable
                if actualresult == expectedresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Bluetooth_IsAdapterDiscoverable API Call after reboot is success"
                    if discoverable == "0":
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "After reboot discoverable status changed to " , discoverable , "successfully"
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "After reboot discoverable status NOT changed to " , discoverable , "successfully"
                else:
                    print "Bluetooth_IsAdapterDiscoverable API Call after reboot is Failure"
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Discoverable status NOT changed to " , discoverable , "successfully"
        else:
            print "Bluetooth_IsAdapterDiscoverable API Call is Failure"
            tdkTestObj.setResultStatus("FAILURE");
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "Bluetooth_SetAdapterDiscoverable API Call is NOT Successfull with status value as " , discoverableStatus , "and timeout is " ,timeout

    bluetoothObj.unloadModule("bluetooth");

else:
    print "Failed to load bluetooth module\n";
    #Set the module loading status
    bluetoothObj.setLoadModuleStatus("FAILURE");
