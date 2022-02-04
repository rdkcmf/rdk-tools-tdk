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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>BluetoothHAL_Set_Get_AdapterName</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>BluetoothHal_SetAdapterName</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To set and get the Bluetooth adapter name</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>1</execution_time>
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
    <test_case_id>CT_BLUETOOTH_HAL_12</test_case_id>
    <test_objective>To set and get the Bluetooth adapter name</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator</test_setup>
    <pre_requisite>1. Initialize the BTRCore module using BTRCore_Init()</pre_requisite>
    <api_or_interface_used>1. enBTRCoreRet BTRCore_SetAdapterName (tBTRCoreHandle hBTRCore, const char* pAdapterPath, const char* pAdapterName);
2. enBTRCoreRet BTRCore_GetAdapterName (tBTRCoreHandle hBTRCore, const char* pAdapterPath, char* pAdapterName);</api_or_interface_used>
    <input_parameters>1. adapter_path - retrieved using BTRCore_GetAdapter()
2. adapter_name - the name string</input_parameters>
    <automation_approch>1. TM loads the BluetoothHal agent via the test agent.
2. BluetoothHal agent will invoke the api BTRCore_GetAdapter to get the adapter path for default bluetooth adapter.
3 . BluetoothHal agent will invoke the api BTRCore_GetAdapterName to get the default bluetooth adapter name.
4. BluetoothHal agent will invoke the api BTRCore_SetAdapterName to set the  bluetooth adapter name.
5. The default adapter name is read back using api BTRCore_GetAdapterName. 
6. TM checks if the API call is success and checks if the bluetooth adapter name is set correctly.
7. BluetoothHal agent will invoke the api BTRCore_SetAdapterName to set the  bluetooth adapter name to the previous value and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1. Verify all API calls are success
Checkpoint 2. Verify that the adapter name is updated correctly.</expected_output>
    <priority>High</priority>
    <test_stub_interface>libbluetoothhalstub.so.0</test_stub_interface>
    <test_script>BluetoothHAL_Set_Get_AdapterName</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
bluetoothhalObj = tdklib.TDKScriptingLibrary("bluetoothhal","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
bluetoothhalObj.configureTestCase(ip,port,'BluetoothHAL_Set_Get_AdapterName');

#Get the result of connection with test component and DUT
result =bluetoothhalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
bluetoothhalObj.setLoadModuleStatus(result.upper());

if "SUCCESS" in result.upper():
    expectedresult="SUCCESS"
    #Primitive test case to get the default adapter path
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
	    #Primitive to get the adapter name
            tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_GetAdapterName');
	    #Set the adapter path to the default adapter path
	    tdkTestObj.addParameter("adapter_path", adapterPath)
			
	    #Execute the test case in DUT
            tdkTestObj.executeTestCase(expectedresult);
			
	    #Get the result of execution
            actualresult = tdkTestObj.getResult();
			
            if (actualresult == expectedresult):
                print "BluetoothHal_GetAdapterName executed successfully"
                tdkTestObj.setResultStatus("SUCCESS");
	        previousName = tdkTestObj.getResultDetails()
		print ("BluetoothHal_GetAdapterName: Initial name of default adapter (%s) is : %s" %(adapterPath, previousName))
                #Set the adapter name
                nameToBeSet = "TDKAdapter"
				
		#Set the adapter name to nameToBeSet
		tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_SetAdapterName');
		#Set the adapter path to the default adapter path
		tdkTestObj.addParameter("adapter_path", adapterPath)
		tdkTestObj.addParameter("adapter_name", nameToBeSet)
				
		#Execute the test case in DUT
                print ("Setting bluetooth adapter name to %s" %(nameToBeSet))
                tdkTestObj.executeTestCase(expectedresult);
			
		#Get the result of execution
                actualresult = tdkTestObj.getResult();
			   
		if (actualresult == expectedresult):
	            print "BluetoothHal_SetAdapterName executed successfully"
		    tdkTestObj.setResultStatus("SUCCESS");	   
		    #Check if the value is set by retrieving the name
		    #Primitive to get the adapter name
                    tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_GetAdapterName');
		    #Set the adapter path to the default adapter path
		    tdkTestObj.addParameter("adapter_path", adapterPath)
			
		    #Execute the test case in DUT
                    tdkTestObj.executeTestCase(expectedresult);
			
		    #Get the result of execution
                    actualresult = tdkTestObj.getResult();
			
		    if (actualresult == expectedresult):
                        print "BluetoothHal_GetAdapterName executed successfully"
                        currentName = tdkTestObj.getResultDetails()
			print ("BluetoothHal_GetAdapterName : Current name of default adapter(%s) is : %s" %(adapterPath, currentName))
				   
			if (currentName == nameToBeSet):
                            print ("Adapter Name Set successfully for %s" %(adapterPath))
			    tdkTestObj.setResultStatus("SUCCESS");
                            #Set the adapter name back to the previous one
                            tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_SetAdapterName');
		            #Set the adapter path to the default adapter path
		            tdkTestObj.addParameter("adapter_path", adapterPath)
		            tdkTestObj.addParameter("adapter_name", previousName)
				
		            #Execute the test case in DUT
                            print ("Setting bluetooth adapter name back to %s" %(previousName))
                            tdkTestObj.executeTestCase(expectedresult);
			
		            #Get the result of execution
                            actualresult = tdkTestObj.getResult();
			   
		            if (actualresult == expectedresult):
	                        print "BluetoothHal_SetAdapterName executed successfully"
                                print "Adapter name reset successfully"
		                tdkTestObj.setResultStatus("SUCCESS");
                            else:
				print "BluetoothHal_SetAdapterName : failed"
                                print "Failed to reset adapter name"
				tdkTestObj.setResultStatus("FAILURE");
                        else:
			    print "Adapter name not set correctly, retrieved value does not match with the value set"
			    tdkTestObj.setResultStatus("FAILURE");
		    else:
		        print "BluetoothHal_GetAdapterName : failed"
			tdkTestObj.setResultStatus("FAILURE");
		else:
		    print "BluetoothHal_SetAdapterName : failed"
		    tdkTestObj.setResultStatus("FAILURE");
	    else:
                print "BluetoothHal_GetAdapterName : failed"
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
