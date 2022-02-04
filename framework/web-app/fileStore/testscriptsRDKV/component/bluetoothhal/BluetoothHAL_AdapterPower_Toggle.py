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
  <version>15</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>BluetoothHAL_AdapterPower_Toggle</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>BluetoothHal_SetAdapterPower</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To toggle the power value of bluetooth adapter</synopsis>
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
    <test_case_id>CT_BLUETOOTH_HAL_04</test_case_id>
    <test_objective>To toggle the bluetooth adapter power status in DUT</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator</test_setup>
    <pre_requisite>1. Initialize the BTRCore module using BTRCore_Init()</pre_requisite>
    <api_or_interface_used>1. enBTRCoreRet BTRCore_GetAdapter (tBTRCoreHandle hBTRCore, stBTRCoreAdapter* apstBTRCoreAdapter);
2. enBTRCoreRet BTRCore_GetAdapterPower (tBTRCoreHandle hBTRCore, const char* pAdapterPath, unsigned char* pAdapterPower);
3. enBTRCoreRet BTRCore_SetAdapterPower (tBTRCoreHandle hBTRCore, const char* pAdapterPath, unsigned char powerStatus);</api_or_interface_used>
    <input_parameters>pAdapterPath - retrieved using BTRCore_GetAdapter() API</input_parameters>
    <automation_approch>1. TM loads the BluetoothHal agent via the test agent.
2 . BluetoothHal agent will invoke the api BTRCore_GetAdapter() to get the adapterPath for the default adapter
3. Retrieve the current power value of adapter using BTRCore_GetAdapterPower()
4. Toggle the power of adapter using BTRCore_SetAdapterPower () API
5. Read back the power value with BTRCore_GetAdapterPower() again and verify that the power value is set correctly.
6. Reset the bluetooth adapter power to ON again</automation_approch>
    <expected_output>Checkpoint 1. Verify the API call is success
Checkpoint 2. Verify that the adapter power value is set successfully by reading back the value using BTRCore_GetAdapterPower()</expected_output>
    <priority>High</priority>
    <test_stub_interface>libbluetoothhalstub.so.0</test_stub_interface>
    <test_script>BluetoothHAL_AdapterPower_Toggle</test_script>
    <skipped>No</skipped>
    <release_version>M85</release_version>
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
bluetoothhalObj.configureTestCase(ip,port,'BluetoothHAL_AdapterPower_Toggle');

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
                tdkTestObj.setResultStatus("SUCCESS");
	        currentPowerStatus = int(tdkTestObj.getResultDetails())
		print ("BluetoothHal_GetAdapterPower : Initial power status of default adapter (%s) is : %d" %(adapterPath, currentPowerStatus))
                if (1 == currentPowerStatus):
		    powerStatusToBeSet = 0  
                else:
                    powerStatusToBeSet = 1
				
		#Set the power status to powerStatusToBeSet
		tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_SetAdapterPower');
		#Set the adapter path to the default adapter path
		tdkTestObj.addParameter("adapter_path", adapterPath)
		tdkTestObj.addParameter("power_status", powerStatusToBeSet)
				
		#Execute the test case in DUT
                print ("Setting bluetooth adapter power to %d" %(powerStatusToBeSet))
                tdkTestObj.executeTestCase(expectedresult);
			
		#Get the result of execution
                actualresult = tdkTestObj.getResult();
			   
		if (actualresult == expectedresult):
	            print "BluetoothHal_SetAdapterPower executed successfully"
		    tdkTestObj.setResultStatus("SUCCESS");	   
		    #Check if the value is set by retrieving the power
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
				   
			if (powerStatusToBeSet == currentPowerStatus):
			    print ("Power Value Set successfully for adapter %s" %(adapterPath))
			    tdkTestObj.setResultStatus("SUCCESS");
		        				
                            #Reset the bluetooth adapter power to ON state
                            actualresult = setAdapterPowerON (bluetoothhalObj, adapterPath)

                            if (actualresult == expectedresult):
                                print "Successfully reset adapter power"							  
                            else:
				print "Failed to power ON adapter"
				tdkTestObj.setResultStatus("FAILURE");
                        else:
			    print "Adapter power not set correctly, retrieved value does not match with the value set"
			    tdkTestObj.setResultStatus("FAILURE");
		    else:
		        print "BluetoothHal_GetAdapterPower: failed"
			tdkTestObj.setResultStatus("FAILURE");
		else:
		    print "BluetoothHal_SetAdapterPower: failed"
		    tdkTestObj.setResultStatus("FAILURE");
	    else:
                print "BluetoothHal_GetAdapterPower: failed"
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
