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
  <name>BluetoothHAL_Enable_Disable_Adapter</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>BluetoothHal_EnableAdapter</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To disable the bluetooth adapter and then enable it</synopsis>
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
    <test_case_id>CT_BLUETOOTH_HAL_07</test_case_id>
    <test_objective>To disable the bluetooth adapter and then enable it	</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Accelerator</test_setup>
    <pre_requisite>1. Initialize the BTRCore module using BTRCore_Init()</pre_requisite>
    <api_or_interface_used>1. enBTRCoreRet BTRCore_GetAdapter (tBTRCoreHandle hBTRCore, stBTRCoreAdapter* apstBTRCoreAdapter);
2. enBTRCoreRet BTRCore_EnableAdapter (tBTRCoreHandle hBTRCore, stBTRCoreAdapter* apstBTRCoreAdapter);
3. enBTRCoreRet BTRCore_DisableAdapter (tBTRCoreHandle hBTRCore, stBTRCoreAdapter* apstBTRCoreAdapter);</api_or_interface_used>
    <input_parameters>adapter handle - retrieved using BTRCore_GetAdapter() API</input_parameters>
    <automation_approch>1. TM loads the BluetoothHal agent via the test agent.
2 . BluetoothHal agent will invoke the api BTRCore_GetAdapter() to get the handle for the default adapter
3. Disable the adapter using BTRCore_DisableAdapter() and check for the enable flag status to be 0
4. Enabel the adapter using BTRCore_EnableAdapter() and check for the enable flag status to be 1</automation_approch>
    <expected_output>Checkpoint 1. Verify the API call is success
Checkpoint 2. Verify that the adapter enable flag value is 0 when BTRCore_DisableAdapter() is executed and enable flag value is 1 when BTRCore_EnableAdapter() is executed </expected_output>
    <priority>High</priority>
    <test_stub_interface>libbluetoothhalstub.so.0</test_stub_interface>
    <test_script>BluetoothHAL_Enable_Disable_Adapter</test_script>
    <skipped>No</skipped>
    <release_version>M85</release_version>
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
bluetoothhalObj.configureTestCase(ip,port,'BluetoothHAL_Enable_Disable_Adapter');

#Get the result of connection with test component and DUT
result =bluetoothhalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
bluetoothhalObj.setLoadModuleStatus(result.upper());

if "SUCCESS" in result.upper():
    expectedresult="SUCCESS"
    #Retrieve the adapter handle using BluetoothHal_GetAdapter, before executing Enable/Disable adapter api
    tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_GetAdapter');

    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    actualresult = tdkTestObj.getResult();
	
    #Check the result of execution
    if (actualresult == expectedresult):
        print "BluetoothHal_GetAdapter executed successfully"
        tdkTestObj.setResultStatus("SUCCESS");

        #Disable the bluetooth adapter
        tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_DisableAdapter');

        #Execute the test case in DUT
        tdkTestObj.executeTestCase(expectedresult);

        #Get the result of execution
        actualresult = tdkTestObj.getResult();
	
        #Check the result of execution
        if (actualresult == expectedresult):
            adapterStatus = int(tdkTestObj.getResultDetails())
            if (0 == adapterStatus):
                print "BluetoothHal_DisableAdapter executed successfully.\nAdapter Status : %d" %(adapterStatus)
                tdkTestObj.setResultStatus("SUCCESS");
                
                #Enable the bluetooth adapter
                tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_EnableAdapter');

                #Execute the test case in DUT
                tdkTestObj.executeTestCase(expectedresult);

                #Get the result of execution
                actualresult = tdkTestObj.getResult();
	        
                #Check the result of execution
                if (actualresult == expectedresult):
                    adapterStatus = int(tdkTestObj.getResultDetails())
                    if (1 == adapterStatus):
                        print "BluetoothHal_EnableAdapter executed successfully.\nAdapter Status : %d" %(adapterStatus)
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        print "Failed to enable bluetooth adapter"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "BluetoothHal_EnableAdapter: failed"
                    tdkTestObj.setResultStatus("FAILURE")     
            else:
                print "Failed to disable bluetooth adapter"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "BluetoothHal_DisableAdapter: failed"
            tdkTestObj.setResultStatus("FAILURE")
    else:
	print "BluetoothHal_GetAdapter: failed"
	tdkTestObj.setResultStatus("FAILURE");

    #Unload the module
    bluetoothhalObj.unloadModule("bluetoothhal");
	
else:
    print "Failed to load bluetoothhal module\n";
    #Set the module loading status
    bluetoothhalObj.setLoadModuleStatus("FAILURE");
