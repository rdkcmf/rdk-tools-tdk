##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>BluetoothHAL_Get_ListOf_ScannedDevices_For_DeviceType_HeadSet</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>BluetoothHal_GetListOfScannedDevices</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check whether discoverable devices are listed in the discovered devices list when the device type is HeadSet</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_BLUETOOTH_HAL_21</test_case_id>
    <test_objective>To check whether discoverable devices are listed in the discovered devices list when the device type is HeadSet</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator</test_setup>
    <pre_requisite>1. Initialize the BTRCore module using BTRCore_Init()</pre_requisite>
    <api_or_interface_used>1. enBTRCoreRet BTRCore_GetAdapter (tBTRCoreHandle hBTRCore, stBTRCoreAdapter* apstBTRCoreAdapter);
2. enBTRCoreRet BTRCore_GetAdapterPower (tBTRCoreHandle hBTRCore, const char* pAdapterPath, unsigned char* pAdapterPower);
3. enBTRCoreRet BTRCore_SetAdapterPower (tBTRCoreHandle hBTRCore, const char* pAdapterPath, unsigned char powerStatus);
4. enBTRCoreRet BTRCore_StartDiscovery (tBTRCoreHandle hBTRCore, const char* pAdapterPath, enBTRCoreDeviceType aenBTRCoreDevType, unsigned int aui32DiscDuration);
5. enBTRCoreRet BTRCore_StopDiscovery (tBTRCoreHandle hBTRCore, const char* pAdapterPath, enBTRCoreDeviceType aenBTRCoreDevType);
6. enBTRCoreRet BTRCore_GetListOfScannedDevices (tBTRCoreHandle hBTRCore, stBTRCoreScannedDevicesCount *pListOfScannedDevices);</api_or_interface_used>
    <input_parameters>1. adapter_path - retrieved using BTRCore_GetAdapter()
2. power_status - 1 (ON)
3. device_type - 1, for enBTRCoreHeadSet
4. timeout - 0 , for no device discovery timeout</input_parameters>
    <automation_approch>1. TM loads the BluetoothHal agent via the test agent.
2 . BluetoothHal agent will invoke the api BTRCore_GetAdapter to get the adapter path for default bluetooth adapters.
3. Set the bluetooth adapter power to 1 (ON) before starting the discovery
4. Set the bluetooth client device as discoverable using executeBluetoothCtl() utility from bluetoothhallib.
5. Start device discovery in adapter using BTRCore_StartDiscovery api
6. After 30 seconds stop the device discovery using BTRCore_StopDiscovery api
7. Get the list of discovered devices using BTRCore_GetListOfScannedDevices api
8. Ensure that the bluetooth client device is present in the scanned devices list.
9. Based on the API call return code, TM return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1. Verify the API call is success
Checkpoint 2. Verify that the bluetooth client device  is present in the discovered devices list</expected_output>
    <priority>High</priority>
    <test_stub_interface>libbluetoothhalstub.so.0</test_stub_interface>
    <test_script>BluetoothHAL_Get_ListOf_ScannedDevices_For_DeviceType_HeadSet</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import json;
from bluetoothhallib import *;
import bluetoothhallib;

#Test component to be tested
bluetoothhalObj = tdklib.TDKScriptingLibrary("bluetoothhal","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
bluetoothhalObj.configureTestCase(ip,port,'BluetoothHAL_Get_ListOf_ScannedDevices_For_DeviceType_HeadSet');

#Get the result of connection with test component and DUT
result =bluetoothhalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
bluetoothhalObj.setLoadModuleStatus(result.upper());

if "SUCCESS" in result.upper():
    expectedresult="SUCCESS"
    #Primitive test case which associated to this Script
    tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_GetAdapter');

    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    actualresult = tdkTestObj.getResult();
	
    #Check the result of execution
    if (actualresult == expectedresult):
        print "BluetoothHal_GetAdapter executed successfully"
        adapterPath = tdkTestObj.getResultDetails();
	print "BluetoothHal_GetAdapter : Default adapter path : ", adapterPath
	if (adapterPath):
            tdkTestObj.setResultStatus("SUCCESS");
     
            #Set the bluetooth adapter power to ON state
            actualresult = setAdapterPowerON (bluetoothhalObj, adapterPath)
            if (actualresult == expectedresult):
                print "Successfully powered ON bluetooth adapter"
          
                #Set the bluetooth client device as discoverable prior to starting device discovery in DUT
                print "Setting client device as discoverable before starting device discovery in DUT"
                commandList = ['bluetoothctl','discoverable on','quit'] 
                bluetoothctlResult = executeBluetoothCtl(bluetoothhalObj,commandList)
                if "FAILURE" not in bluetoothctlResult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Client Device %s set as discoverable" %(bluetoothhallib.deviceName)
                    #Start device discovery in DUT
                    print "Starting the device discovery in DUT"
                    tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_StartDiscovery');
	            #Set the adapter path to the default adapter path
	            tdkTestObj.addParameter("adapter_path", adapterPath)
                    #Set the discovery timeout as 0, for no timeout
	            tdkTestObj.addParameter("timeout", 0)
                    #Set the device type as 1 - HeadSet
                    tdkTestObj.addParameter("device_type", 1)

                    #Execute the test case in DUT
                    tdkTestObj.executeTestCase(expectedresult);
			
	            #Get the result of execution
                    actualresult = tdkTestObj.getResult();
			   
	            if (actualresult == expectedresult):
	                print "BluetoothHal_StartDiscovery executed successfully"
	                tdkTestObj.setResultStatus("SUCCESS")

                        #Waiting for 30 seconds to scan available devices
                        time.sleep (30)
                        
                        #Stop device discovery in DUT
                        print "Stoping the device discovery in DUT"
                        tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_StopDiscovery');
	                #Set the adapter path to the default adapter path
	                tdkTestObj.addParameter("adapter_path", adapterPath)
                        #Set the device type as 1 - HeadSet
                        tdkTestObj.addParameter("device_type", 1)

                        #Execute the test case in DUT
                        tdkTestObj.executeTestCase(expectedresult);
			
	                #Get the result of execution
                        actualresult = tdkTestObj.getResult();
			   
	                if (actualresult == expectedresult):
	                    print "BluetoothHal_StopDiscovery executed successfully"
                            tdkTestObj.setResultStatus("SUCCESS")

                            #Retrieve the list of scanned devices
                            tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_GetListOfScannedDevices');
                            #Execute the test case in DUT
                            tdkTestObj.executeTestCase(expectedresult);
			
	                    #Get the result of execution
                            actualresult = tdkTestObj.getResult();
			  
	                    if (actualresult == expectedresult):
	                        print "BluetoothHal_GetListOfScannedDevices executed successfully"
                                tdkTestObj.setResultStatus("SUCCESS")
                                result = tdkTestObj.getResultDetails()
                                deviceDiscovered = False
                                if result and "NO_DEVICES_FOUND" != result:
                                    scannedDevices = json.loads(result)
                                    #Traverse the scanned devices list to check if the client device is present
                                    for device in scannedDevices:
                                        if (device["deviceName"] == bluetoothhallib.deviceName):
                                            print "Client device of type HeadSet is successfully discovered in DUT"
                                            print "Client device details: \n", device
                                            deviceDiscovered = True
                                    if True == deviceDiscovered:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print "Client device NOT discovered in DUT"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "Client device NOT discovered in DUT"
                                    tdkTestObj.setResultStatus("FAILURE")   
                            else:
                                print "BluetoothHal_GetListOfScannedDevices: failed"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "BluetoothHal_StopDiscovery: failed"
                            tdkTestObj.setResultStatus("FAILURE")
		    else:
	                print "BluetoothHal_StartDiscovery: failed"
	                tdkTestObj.setResultStatus("FAILURE")
  
                    #Close the client device session after use
                    closeSSHSession()
                else:
                    print "Failed to connect to client device"
                    tdkTestObj.setResultStatus("FAILURE");
            else:
		print "Failed to power ON bluetooth adapter"
		tdkTestObj.setResultStatus("FAILURE");
        else:
            print "Default adapter path is empty"
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print "BluetoothHal_GetAdapter: failed"
        tdkTestObj.setResultStatus("FAILURE");

    #Unload the module
    bluetoothhalObj.unloadModule("bluetoothhal");
        
else:
    print "Failed to load bluetoothhal module\n";
    #Set the module loading status
    bluetoothhalObj.setLoadModuleStatus("FAILURE");
