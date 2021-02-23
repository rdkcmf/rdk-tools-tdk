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
  <name>BluetoothHAL_Set_Get_AdapterPowerStatus_ON_Persist</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>BluetoothHal_SetAdapterPower</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check that bluetooth adapter power status in reset  to ON after reboot</synopsis>
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
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_BLUETOOTH_HAL_16</test_case_id>
    <test_objective>To check that bluetooth adapter power status in reset  to ON after reboot</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Accelerator</test_setup>
    <pre_requisite>1. Initialize the BTRCore module using BTRCore_Init()</pre_requisite>
    <api_or_interface_used>1. enBTRCoreRet BTRCore_GetAdapter (tBTRCoreHandle hBTRCore, stBTRCoreAdapter* apstBTRCoreAdapter);
2. enBTRCoreRet BTRCore_GetAdapterPower (tBTRCoreHandle hBTRCore, const char* pAdapterPath, unsigned char* pAdapterPower);
3. enBTRCoreRet BTRCore_SetAdapterPower (tBTRCoreHandle hBTRCore, const char* pAdapterPath, unsigned char powerStatus);</api_or_interface_used>
    <input_parameters>1. pAdapterPath - retrieved using BTRCore_GetAdapter() API
2. powerStatus - 0 (OFF)</input_parameters>
    <automation_approch>1. TM loads the BluetoothHal agent via the test agent.
2 . BluetoothHal agent will invoke the api BTRCore_GetAdapter() to get the adapterPath for the default adapter
3. Set the bluetooth adapter power status to 0 (OFF) using BTRCore_SetAdapterPower () API
4. Read back the power value with BTRCore_GetAdapterPower() again and verify that the power value is OFF.
5. Reboot the DUT
6. Get the power value with BTRCore_GetAdapterPower() again and verify that the power value is ON
6. Reset the bluetooth adapter power to ON if it fails to reset power to ON after reboot</automation_approch>
    <expected_output>Checkpoint 1. Verify the API call is success
Checkpoint 2. Verify that the adapter power value is reset to ON after DUT reboots</expected_output>
    <priority>High</priority>
    <test_stub_interface>libbluetoothhalstub.so.0</test_stub_interface>
    <test_script>BluetoothHAL_Set_Get_AdapterPowerStatus_ON_Persist</test_script>
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
from bluetoothhallib import *;
import bluetoothhallib;

#Test component to be tested
bluetoothhalObj = tdklib.TDKScriptingLibrary("bluetoothhal","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
bluetoothhalObj.configureTestCase(ip,port,'BluetoothHAL_Set_Get_AdapterPowerStatus_ON_Persist');

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
	    #Set the power status to OFF
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
		    print ("BluetoothHal_GetAdapterPower : Current power status of default adapter(%s) is : %d" %(adapterPath, currentPowerStatus))
				   
		    if (powerOFF == currentPowerStatus):
	                print ("%s adapter powered OFF successfully" %(adapterPath))
			tdkTestObj.setResultStatus("SUCCESS");
		        
                        #Reboot the DUT
                        bluetoothhalObj.initiateReboot()
                        time.sleep(120)

                        #Check the bluetooth adapter power is reset to ON after reboot
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
                            #Verify that bluetooth adapter power is 1 (ON) after reboot
			    if (1 == currentPowerStatus):
			        print ("%s adapter powered ON successfully after reboot" %(adapterPath))
			        tdkTestObj.setResultStatus("SUCCESS");
                            else:
			        print "Adapter not powered ON correctly after reboot"
			        tdkTestObj.setResultStatus("FAILURE");
				#Reset the bluetooth adapter power to ON state
                                actualresult = setAdapterPowerON (bluetoothhalObj, adapterPath)

                                if (actualresult == expectedresult):
                                    print "Successfully reset adapter power"							  
                                else:
				    print "Failed to power ON adapter"
				    tdkTestObj.setResultStatus("FAILURE");
                        else:
		            print "BluetoothHal_GetAdapterPower: failed"
			    tdkTestObj.setResultStatus("FAILURE");
                    else:
		        print "Adapter not powered OFF correctly"
			tdkTestObj.setResultStatus("FAILURE");
		else:
		    print "BluetoothHal_GetAdapterPower: failed"
		    tdkTestObj.setResultStatus("FAILURE");
	    else:
		print "BluetoothHal_SetAdapterPower: failed"
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
