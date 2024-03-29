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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>5</version>
  <name>BluetoothHAL_Get_AdapterAddress</name>
  <primitive_test_id/>
  <primitive_test_name>BluetoothHal_GetAdapterAddr</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To get the address of bluetooth adapter</synopsis>
  <groups_id/>
  <execution_time>1</execution_time>
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
    <test_case_id>CT_BLUETOOTH_HAL_08</test_case_id>
    <test_objective>To get the address of bluetooth adapter</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator</test_setup>
    <pre_requisite>1. Initialize the BTRCore module using BTRCore_Init()</pre_requisite>
    <api_or_interface_used>1. enBTRCoreRet BTRCore_GetListOfAdapters (tBTRCoreHandle hBTRCore, stBTRCoreListAdapters* pstListAdapters);
2. enBTRCoreRet BTRCore_GetAdapterAddr (tBTRCoreHandle hBTRCore, unsigned char aui8adapterIdx, char* apui8adapterAddr);</api_or_interface_used>
    <input_parameters>adapter_number - using the default adapter 0</input_parameters>
    <automation_approch>1. TM loads the BluetoothHal agent via the test agent.
2 . BluetoothHal agent will invoke the api BTRCore_GetListOfAdapters which fetches and saves the number of bluetooth adapters available in the DUT inside HAL.
3. BluetoothHal agent will invoke the api BTRCore_GetAdapterAddr to get the address of bluetooth adapter specified using the adapter number 0(for default adapter).
4. TM checks if the API call is success and checks if the bluetooth adapter address retrieved is not empty and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1. Verify the API calls are success
Checkpoint 2. Verify that atleast one bluetooth adapter is available in the DUT.
Checkpoint 3. Verify that the bluetooth adapter address retrieved is not empty </expected_output>
    <priority>High</priority>
    <test_stub_interface>libbluetoothhalstub.so.0</test_stub_interface>
    <test_script>BluetoothHAL_Get_AdapterAddress</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
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
bluetoothhalObj.configureTestCase(ip,port,'BluetoothHAL_Get_AdapterAddress');

#Get the result of connection with test component and DUT
result =bluetoothhalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
bluetoothhalObj.setLoadModuleStatus(result.upper());

if "SUCCESS" in result.upper():
    expectedresult="SUCCESS"
    tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_GetListOfAdapters');

    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    actualresult = tdkTestObj.getResult();

    #Set the result status of execution
    if (actualresult == expectedresult):
        print "Successfully executed BluetoothHal_GetListOfAdapters"
        numOfAdapters = tdkTestObj.getResultDetails();
        print "BluetoothHal_GetListOfAdapters: Number of adapters : ", numOfAdapters
        if (0 < numOfAdapters):
            tdkTestObj.setResultStatus("SUCCESS");
            #Primitive test case which associated to this Script
            tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_GetAdapterAddr');
            #Set the adapter number to '0' the default adapter number
            tdkTestObj.addParameter("adapter_number", 0)

            #Execute the test case in DUT
            tdkTestObj.executeTestCase(expectedresult);

            #Get the result of execution
            actualresult = tdkTestObj.getResult();

            if (actualresult == expectedresult) :
                print "BluetoothHal_GetAdapterAddr executed succesfully"
                adapterAddress = tdkTestObj.getResultDetails();
	        if (adapterAddress):
                    print "Deafult adapter address : ", adapterAddress
                    tdkTestObj.setResultStatus("SUCCESS");
                else:
                    print "Adapter address should not be empty"
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                print "BluetoothHal_GetAdapterAddr : failed"
                tdkTestObj.setResultStatus("FAILURE");
        else:
            print "Atleast default adapter should be present in the device"
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print "Failed to execute BluetoothHal_GetListOfAdapters"
        tdkTestObj.setResultStatus("FAILURE");
	        
    #Unload the module
    bluetoothhalObj.unloadModule("bluetoothhal");
	
else:
    print "Failed to load bluetoothhal module\n";
    #Set the module loading status
    bluetoothhalObj.setLoadModuleStatus("FAILURE");
