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
  <version>1</version>
  <name>Bluetooth_Persist_Set_Get_Adapter_Name</name>
  <primitive_test_id/>
  <primitive_test_name>Bluetooth_SetAdapterName</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check whether Bluetooth adapter name persists or not</synopsis>
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
    <test_case_id>CT_BLUETOOTH_09</test_case_id>
    <test_objective>To check whether Bluetooth adapter name persists or not</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI5</test_setup>
    <pre_requisite>1. Initialize the bluetooth manager
BTRMGR_Init();
2. Deinit the bluetooth manager after test
BTRMGR_DeInit();</pre_requisite>
    <api_or_interface_used>bool Bluetooth_GetAdapterName
bool Bluetooth_SetAdapterName</api_or_interface_used>
    <input_parameters>BTRMGR_GetAdapterName(0, adapterName);
BTRMGR_SetAdapterName(0, nameAdapter);</input_parameters>
    <automation_approch>1. TM loads the Bluetooth agent via the test agent.
2  Bluetooth agent will invoke the api   BTRMGR_GetAdapterName and store the existing adapter name.
3.Bluetooth agent will invoke the api BTRMGR_SetAdapterName with adapter name as "tdk".
4.Reboot the box and Check whether the new adapter name "tdk" is persists or not
5.Set the previous adapter name again</automation_approch>
    <except_output>Checkpoint 1.Verify the API call return value
Checkpoint 2.The new adapter name "tdk" should persists successfully .</except_output>
    <priority>High</priority>
    <test_stub_interface>libbluetoothstub.so.0</test_stub_interface>
    <test_script>Bluetooth_Persist_Set_Get_Adapter_Name</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
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
bluetoothObj.configureTestCase(ip,port,'Bluetooth_Persist_Set_Get_Adapter_Name');

def setAdapterName(adapterName):
    tdkTestObj = bluetoothObj.createTestStep('Bluetooth_SetAdapterName');
    tdkTestObj.addParameter("name",adapterName);
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    if actualresult == expectedresult:
        tdkTestObj.setResultStatus("SUCCESS");
        return "SUCCESS"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        return "FAILURE"

def checkAdapterName(adapterName):
    tdkTestObj = bluetoothObj.createTestStep('Bluetooth_GetAdapterName');
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    adapterNameAfter = tdkTestObj.getResultDetails();
    if actualresult == expectedresult:
        print "Bluetooth_GetAdapterName API Call is Successfull"
        print "Adapter name after changing is " , adapterNameAfter
        tdkTestObj.setResultStatus("SUCCESS");
        if adapterName == adapterNameAfter:
            tdkTestObj.setResultStatus("SUCCESS");
            return "SUCCESS"
        else:   
            tdkTestObj.setResultStatus("FAILURE");
            return "FAILURE"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "Bluetooth_GetAdapterName API Call is NOT Successfull"
        return "FAILURE"

#Get the result of connection with test component and STB
bluetoothLoadStatus =bluetoothObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %bluetoothLoadStatus;
bluetoothObj.setLoadModuleStatus(bluetoothLoadStatus.upper());

if "SUCCESS" in bluetoothLoadStatus.upper():

   #Prmitive test case which associated to this Script
   expectedresult="SUCCESS"
   tdkTestObj = bluetoothObj.createTestStep('Bluetooth_GetAdapterName');
   #Execute the test case in STB
   tdkTestObj.executeTestCase(expectedresult);
   actualresult = tdkTestObj.getResult();
   adapterNameBefore = tdkTestObj.getResultDetails();
   if actualresult == expectedresult:
       tdkTestObj.setResultStatus("SUCCESS");
       print "RESULT : Bluetooth_GetAdapterName : " , actualresult
       print "DETAILS : Bluetooth_GetAdapterName : " , adapterNameBefore
       print "Adapter name before changing is " , adapterNameBefore

       print "Set the adapter name to tdk"
       adapterName = "tdk"
       returnValue = setAdapterName(adapterName)
       if returnValue in expectedresult:
           print "Bluetooth_SetAdapterName API Call is Successfull with name as " , adapterName
           print "Check the adapter name " ,adapterName, " is set successfully or not"
           returnValue = checkAdapterName(adapterName) 
           if returnValue in expectedresult:
               print "Adapter name successfully set to " , adapterName
               #Reboot the STB
               bluetoothObj.initiateReboot();
               sleep(120); 
               tdkTestObj = bluetoothObj.createTestStep('Bluetooth_GetAdapterName');
               #Execute the test case in STB
               tdkTestObj.executeTestCase(expectedresult);
               actualresult = tdkTestObj.getResult();
               adapterNameAfter = tdkTestObj.getResultDetails();
               print "RESULT : Bluetooth_GetAdapterName after reboot : " , actualresult
               print "DETAILS : Bluetooth_GetAdapterName after reboot: " , adapterNameAfter
               if actualresult == expectedresult:
                   print "Bluetooth_GetAdapterName API Call is Successfull"      
                   if adapterName == adapterNameAfter:
                       tdkTestObj.setResultStatus("SUCCESS");
                       print "Adapter name " ,adapterName ,"successfully persisted "
                   else:   
                       tdkTestObj.setResultStatus("FAILURE");
                       print "Adapter name " ,adapterName , "NOT Persisted"
               else:
                   tdkTestObj.setResultStatus("FAILURE");
                   print "Bluetooth_GetAdapterName API Call is NOT Successfull"
           else:
               print "Adapter name NOT set to " , adapterName
       else:
           print "Bluetooth_SetAdapterName API Call is NOT Successfull with name as " ,adapterName
   else:
       tdkTestObj.setResultStatus("FAILURE");
       print "Bluetooth_GetAdapterName call is FAILURE"
  
   bluetoothObj.unloadModule("bluetooth");

else:
    print "Failed to load bluetooth module\n";
    #Set the module loading status
    bluetoothObj.setLoadModuleStatus("FAILURE");
