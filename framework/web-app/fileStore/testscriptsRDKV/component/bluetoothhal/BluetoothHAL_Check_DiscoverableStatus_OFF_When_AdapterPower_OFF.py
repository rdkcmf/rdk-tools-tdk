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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>BluetoothHAL_Check_DiscoverableStatus_OFF_When_AdapterPower_OFF</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>BluetoothHal_SetAdapterDiscoverable</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check that discoverable status is reset to off when the bluetooth adapter power is turned off</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2</execution_time>
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
    <test_case_id>CT_BLUETOOTH_HAL_19</test_case_id>
    <test_objective>To check that discoverable status is reset to off when the bluetooth adapter power is turned off</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Accelerator</test_setup>
    <pre_requisite>1. Initialize the BTRCore module using BTRCore_Init()</pre_requisite>
    <api_or_interface_used>1. enBTRCoreRet BTRCore_GetAdapter (tBTRCoreHandle hBTRCore, stBTRCoreAdapter* apstBTRCoreAdapter);
2. enBTRCoreRet BTRCore_SetAdapterPower (tBTRCoreHandle hBTRCore, const char* pAdapterPath, unsigned char powerStatus);
3. enBTRCoreRet BTRCore_GetAdapterPower (tBTRCoreHandle hBTRCore, const char* pAdapterPath, unsigned char* pAdapterPower);
4. enBTRCoreRet BTRCore_SetAdapterDiscoverable (tBTRCoreHandle hBTRCore, const char* pAdapterPath, unsigned char discoverable);
5. enBTRCoreRet BTRCore_GetAdapterDiscoverableStatus (tBTRCoreHandle hBTRCore, const char* pAdapterPath, unsigned char* pDiscoverable);</api_or_interface_used>
    <input_parameters>1. adapter_path - retrieved using BTRCore_GetAdapter()
2. discoverable_status - 1 , to set the device as discoverable
3. power_status - 0 (OFF)</input_parameters>
    <automation_approch>1. TM loads the BluetoothHal agent via the test agent.
2 . BluetoothHal agent will invoke the api BTRCore_GetAdapter to get the adapter path for default bluetooth adapters.
3. Set the discoverable status for the adapter as 1(discoverable)
4. Get the discoverable status for the adapter and check if its 1
5. BluetoothHal agent will invoke the api BTRCore_SetAdapterPower to set the power status of bluetooth adapter to 0 (OFF).
6. Read back the power value with BTRCore_GetAdapterPower() again and verify that the adapter is powered OFF correctly.
7. Get the discoverable status for the adapter and check if it is reset to 0.
8. Bluetooth adapter power is reset to 1 (ON).
9. Based on the API call return code, TM return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1. Verify the API call is success
Checkpoint 2. Verify the discoverable status for the bluetooth adapter which was set to 1 (discoverable )  is reset to 0 (undiscoverable) when adapter power was set to 0 (OFF).</expected_output>
    <priority>High</priority>
    <test_stub_interface>libbluetoothhalstub.so.0</test_stub_interface>
    <test_script>BluetoothHAL_Check_DiscoverableStatus_OFF_When_AdapterPower_OFF</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from bluetoothhallib import *;
import bluetoothhallib;

#Test component to be tested
bluetoothhalObj = tdklib.TDKScriptingLibrary("bluetoothhal","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
bluetoothhalObj.configureTestCase(ip,port,'BluetoothHAL_Check_DiscoverableStatus_OFF_When_AdapterPower_OFF');

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
            #Set the adapter to be discoverable
	    tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_SetAdapterDiscoverable');
	    #Set the adapter path to the default adapter path
	    tdkTestObj.addParameter("adapter_path", adapterPath)
            #Set the discoverable status to be 1(discoverable)
	    tdkTestObj.addParameter("discoverable_status", 1)
				
	    #Execute the test case in DUT
            tdkTestObj.executeTestCase(expectedresult);
			
	    #Get the result of execution
            actualresult = tdkTestObj.getResult();
			   
	    if (actualresult == expectedresult):
	        print "BluetoothHal_SetAdapterDiscoverable executed successfully"
	        tdkTestObj.setResultStatus("SUCCESS");
                    
                #Check if the adapter is discoverable by retrieving the discoverable status
		#Primitive to get the discoverable status
                tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_GetAdapterDiscoverableStatus');
		#Set the adapter path to the default adapter path
		tdkTestObj.addParameter("adapter_path", adapterPath)
			
		#Execute the test case in DUT
                tdkTestObj.executeTestCase(expectedresult);
			
		#Get the result of execution
                actualresult = tdkTestObj.getResult();
			
		if (actualresult == expectedresult):
                    print "BluetoothHal_GetAdapterDiscoverableStatus executed successfully"
                    discoverableStatus = int(tdkTestObj.getResultDetails())
				   
		    if (1 == discoverableStatus):
		        print ("Adapter %s is discoverable" %(adapterPath))
			tdkTestObj.setResultStatus("SUCCESS");

                        #Set the adapter power status to OFF
                        powerOFF = 0
	                tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_SetAdapterPower');
	                #Set the adapter path to the default adapter path
	                tdkTestObj.addParameter("adapter_path", adapterPath)
	                tdkTestObj.addParameter("power_status", powerOFF)
				
	                #Execute the test case in DUT
                        print "Setting bluetooth adapter power OFF"
                        tdkTestObj.executeTestCase(expectedresult);
			
	                #Get the result of execution
                        actualresult = tdkTestObj.getResult();
			   
	                if (actualresult == expectedresult):
	                    print "BluetoothHal_SetAdapterPower executed successfully"
	                    tdkTestObj.setResultStatus("SUCCESS");	   
	                    #Check if the value is powered OFF by retrieving the power
                            #Primitive to get the adapter power
                            tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_GetAdapterPower');
		            #Set the adapter path to the default adapter path
		            tdkTestObj.addParameter("adapter_path", adapterPath)
			
		            #Execute the test case in DUT
                            tdkTestObj.executeTestCase(expectedresult);
			
		            #Get the result of execution
                            actualresult = tdkTestObj.getResult();
			
		            if (actualresult == expectedresult):
                                print "BluetoothHal_GetAdapterPower executed successfully"
                                currentPowerStatus = int(tdkTestObj.getResultDetails())
				   
		                if (powerOFF == currentPowerStatus):
	                            print ("%s adapter powered OFF successfully" %(adapterPath))
			            tdkTestObj.setResultStatus("SUCCESS");

                                    #Check the adapter discoverable status to verify that its reset to 0
                                    #Primitive to get the discoverable status
                                    tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_GetAdapterDiscoverableStatus');
		                    #Set the adapter path to the default adapter path
		                    tdkTestObj.addParameter("adapter_path", adapterPath)
		                
		                    #Execute the test case in DUT
                                    tdkTestObj.executeTestCase(expectedresult);
		                
		                    #Get the result of execution
                                    actualresult = tdkTestObj.getResult();
		                
		                    if (actualresult == expectedresult):
                                        print "BluetoothHal_GetAdapterDiscoverableStatus executed successfully"
                                        discoverableStatus = int(tdkTestObj.getResultDetails())		                	   
		                        if (0 == discoverableStatus):
		                            print ("Adapter %s is not discoverable when power status is OFF" %(adapterPath))
		                            tdkTestObj.setResultStatus("SUCCESS");
                                        else:
                                            print ("Adapter %s is discoverable even when power status is OFF" %(adapterPath))
                                            tdkTestObj.setResultStatus("FAILURE");
                                    else:
                                        print "BluetoothHal_GetAdapterDiscoverableStatus: failed"
                                        tdkTestObj.setResultStatus("FAILURE");

                                    #Reset the bluetooth adapter power to ON state
                                    print "Resetting the bluetooth adapter power to ON after testing"
                                    actualresult = setAdapterPowerON (bluetoothhalObj, adapterPath)
                                    if (actualresult == expectedresult):
                                        print "Successfully reset adapter power"							  
                                    else:
			                print "Failed to power ON adapter"
			                tdkTestObj.setResultStatus("FAILURE");
                                else:
                                    print "Adapter is not powered OFF correctly"
                                    tdkTestObj.setResultStatus("FAILURE");
                            else:
		                print "BluetoothHal_GetAdapterPower: failed"
		                tdkTestObj.setResultStatus("FAILURE");
	                else:
		            print "BluetoothHal_SetAdapterPower: failed"
		            tdkTestObj.setResultStatus("FAILURE");
                    else:
                        print ("Adapter %s is not discoverable" %(adapterPath))
                        tdkTestObj.setResultStatus("FAILURE");
                else:
                    print "BluetoothHal_GetAdapterDiscoverableStatus: failed"
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                print "BluetoothHal_SetAdapterDiscoverable: failed"
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
