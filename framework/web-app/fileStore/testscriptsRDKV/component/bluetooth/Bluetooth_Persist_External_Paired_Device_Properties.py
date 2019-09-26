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
  <name>Bluetooth_Persist_External_Paired_Device_Properties</name>
  <primitive_test_id/>
  <primitive_test_name>Bluetooth_GetDeviceProperties</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check whether the paired device properties persists or not when the pair request came from external device</synopsis>
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
    <test_case_id>CT_BLUETOOTH_57</test_case_id>
    <test_objective>To check whether the paired device properties persists or not when the pair request came from external device</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI5</test_setup>
    <pre_requisite>1.Set the values in bluetoothcredential.config
2. Initialize the bluetooth manager
BTRMGR_Init();
3. Deinit the bluetooth manager after test
BTRMGR_DeInit();</pre_requisite>
    <api_or_interface_used>bool Bluetooth_GetAdapterPowerStatus
bool Bluetooth_SetAdapterPowerStatus
bool Bluetooth_GetPairedDevices
bool Bluetooth_UnpairDevice
bool Bluetooth_GetDeviceProperties</api_or_interface_used>
    <input_parameters>BTRMGR_IsAdapterDiscoverable(0,&amp;discoverableStatus);
BTRMGR_SetAdapterDiscoverable(0,discoverableStatus,Timeout);
BTRMGR_GetAdapterPowerStatus(0, &amp;powerStatus);
BTRMGR_SetAdapterPowerStatus(0,powerStatus);BTRMGR_StartDeviceDiscovery(0);
BTRMGR_PairDevice(0, handle);
BTRMGR_UnpairDevice(0, handle);
BTRMGR_GetPairedDevices(0, &amp;pairedDevices);
</input_parameters>
    <automation_approch>1. TM loads the Bluetooth agent via the test agent.
2  Turn ON the bluetotoh adapter if it is OFF
3.Turn ON the discoverable status of bluetooth emulator
4. Trigger the pairing request from Bluetooth emulator
5.Check the paired devices list in DUT and confirm the bluetooth emulator adapter name is there in the list
6.Get the paired device properties
7. Reboot and get paired device properties 
8.Unpair the bluetooth emulator
</automation_approch>
    <except_output>Checkpoint 1.After pairing the bluetooth emulator name should be there in the paired devices list of DUT
Checkpoint 2 Check the paired device properties values . value of paired should be equal to 1
Checkpoint 3 After reboot also Check the paired device properties values . value of paired should be equal to 1
Checkpoint 4 After Unpair the bluetooth emulator  should be removed from the paired devices list of DUT</except_output>
    <priority>High</priority>
    <test_stub_interface>libbluetoothstub.so.0</test_stub_interface>
    <test_script>Bluetooth_Persist_External_Paired_Device_Properties</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import bluetoothlib;
import json
from time import sleep

#Test component to be tested
bluetoothObj = tdklib.TDKScriptingLibrary("bluetooth","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
bluetoothObj.configureTestCase(ip,port,'Bluetooth_Persist_External_Paired_Device_Properties');

def getPowerStatus():
   tdkTestObj = bluetoothObj.createTestStep('Bluetooth_GetAdapterPowerStatus');
   #Execute the test case in STB
   tdkTestObj.executeTestCase(expectedresult);
   actualresult = tdkTestObj.getResult();
   powerStatusBefore = tdkTestObj.getResultDetails();
   if actualresult == expectedresult:
       tdkTestObj.setResultStatus("SUCCESS");
       print "Bluetooth_GetAdapterPowerStatus call is SUCCESS"
       return powerStatusBefore
   else:
       print "Bluetooth_GetAdapterPowerStatus call is FAILURE"
       tdkTestObj.setResultStatus("FAILURE");

#Get the result of connection with test component and STB
bluetoothLoadStatus =bluetoothObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %bluetoothLoadStatus;
bluetoothObj.setLoadModuleStatus(bluetoothLoadStatus.upper());

if "SUCCESS" in bluetoothLoadStatus.upper():
 
    expectedresult="SUCCESS"
    print "Get the Bluetooth Adapter Power Status"
    powerStatusBefore = getPowerStatus()
    if powerStatusBefore !="1":
        print "Bluetooth Adapter is OFF"
        print  "Turn ON the Bluetooth Adapter"
        tdkTestObj = bluetoothObj.createTestStep('Bluetooth_SetAdapterPowerStatus');
        tdkTestObj.addParameter("powerstatus",1);
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        if actualresult == expectedresult:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Bluetooth_SetAdapterPowerStatus call is SUCCESS"
            powerStatusAfter = getPowerStatus()
            if powerStatusAfter == "1":
                tdkTestObj.setResultStatus("SUCCESS");
                print "Bluetooth Adapter Turned ON successfully"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Unable to Turn ON the Bluetooth Adapter"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Bluetooth_SetAdapterPowerStatus call is FAILURE"
    else:
        print "Bluetooth adapter is already ON"

    print "Set the Bluetooth Discoverable status to ON (1)"
    discoverableStatus = "1"
    tdkTestObj = bluetoothObj.createTestStep('Bluetooth_SetAdapterDiscoverable');
    timeout = "100"
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
                tdkTestObj = bluetoothObj.createTestStep('Bluetooth_SendRequest');
                #Execute the test case in STB
                tdkTestObj.executeTestCase(expectedresult);
                print "Executing the following bluetoothctl commands in the client device "
                commandList = ['bluetoothctl','scan on','scan off' ,'pair ','remove ','quit']
                print commandList
                output = bluetoothlib.executeBluetoothCtl(bluetoothObj,commandList)
                if "FAILURE" in output:
                     tdkTestObj.setResultStatus("FAILURE");
                     print "Connecting to client device got failed"
                else:
                    tdkTestObj.setResultStatus("SUCCESS"); 
                    tdkTestObj = bluetoothObj.createTestStep('Bluetooth_GetPairedDevices')
                    #Execute the test case in STB
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    pairedDevicesList = tdkTestObj.getResultDetails();
                    print "PAIR" , pairedDevicesList
                    pairedDevicesList = pairedDevicesList.split(';')[:-1]
                    print "Paired Devices List" , pairedDevicesList
                    if actualresult == expectedresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Bluetooth_GetPairedDevices call is SUCCESS"
                        pairedDeviceNameList=[]
                        pairedDeviceHandleList=[]
                        for devices in range(len(pairedDevicesList)):  
                            pairedDeviceNameList.append(pairedDevicesList[devices].split(':')[0])
                            pairedDeviceHandleList.append(pairedDevicesList[devices].split(':')[1])
                        if str(bluetoothlib.deviceName) in pairedDeviceNameList :
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "DUT is successfully paired with Client device"
                            pairedDeviceNameIndex = pairedDeviceNameList.index(str(bluetoothlib.deviceName))
                            handleNumber = pairedDeviceHandleList[pairedDeviceNameIndex]
                            tdkTestObj = bluetoothObj.createTestStep('Bluetooth_GetDeviceProperties');
                            tdkTestObj.addParameter("devicehandle",handleNumber);
                            #Execute the test case in STB
                            tdkTestObj.executeTestCase(expectedresult);
                            actualresult = tdkTestObj.getResult();
                            if actualresult == expectedresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "Bluetooth_GetDeviceProperties call is SUCCESS"
                                deviceProperties = tdkTestObj.getResultDetails();
                                print "Device Properties " , deviceProperties
                                json_acceptable_string = deviceProperties.replace("'", "\"")
                                deviceProperties =json.loads(json_acceptable_string)
                                if "1" in deviceProperties['paired']:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print"Externally Paired device property has valid value"
                                    #Reboot the STB
                                    bluetoothObj.initiateReboot();
                                    sleep(60);
                                    tdkTestObj = bluetoothObj.createTestStep('Bluetooth_GetPairedDevices')
                                    #Execute the test case in STB
                                    tdkTestObj.executeTestCase(expectedresult);
                                    actualresult = tdkTestObj.getResult();
                                    pairedDevicesList = tdkTestObj.getResultDetails();
                                    pairedDevicesList = pairedDevicesList.split(';')[:-1]
                                    print "Paired Devices List After Reboot" , pairedDevicesList
                                    if actualresult == expectedresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Bluetooth_GetPairedDevices call After Reboot is SUCCESS"
                                        pairedDeviceNameList=[]
                                        for devices in range(len(pairedDevicesList)):  
                                            pairedDeviceNameList.append(pairedDevicesList[devices].split(':')[0])
                                        if str(bluetoothlib.deviceName) in pairedDeviceNameList :
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print "Client device is automatically paired with DUT After Reboot"
                                            tdkTestObj = bluetoothObj.createTestStep('Bluetooth_GetDeviceProperties');
                                            tdkTestObj.addParameter("devicehandle",handleNumber);
                                            #Execute the test case in STB
                                            tdkTestObj.executeTestCase(expectedresult);
                                            actualresult = tdkTestObj.getResult();
                                            if actualresult == expectedresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "Bluetooth_GetDeviceProperties call is SUCCESS"
                                                deviceProperties = tdkTestObj.getResultDetails();
                                                print "Device Properties " , deviceProperties
                                                json_acceptable_string = deviceProperties.replace("'", "\"")
                                                deviceProperties =json.loads(json_acceptable_string)
                                                if "1" in deviceProperties['paired']:
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print"Externally Paired device property value has persisted"
                                                else:
                                                    print"Externally Paired device property value has INVALID has not persisted"
                                                    tdkTestObj.setResultStatus("FAILURE");
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Bluetooth_GetDeviceProperties call is FAILURE" 

                                            print "Unpair the client device from DUT" 
                                            tdkTestObj = bluetoothObj.createTestStep('Bluetooth_UnpairDevice')
                                            tdkTestObj.addParameter("devicehandle",handleNumber);
                                            #Execute the test case in STB
                                            tdkTestObj.executeTestCase(expectedresult);
                                            actualresult = tdkTestObj.getResult();
                                            if actualresult == expectedresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "Bluetooth_UnpairDevice call is SUCCESS"
                                                tdkTestObj = bluetoothObj.createTestStep('Bluetooth_GetPairedDevices')
                                                #Execute the test case in STB
                                                tdkTestObj.executeTestCase(expectedresult);
                                                actualresult = tdkTestObj.getResult();
                                                pairedDevicesList = tdkTestObj.getResultDetails();
                                                pairedDevicesList = pairedDevicesList.split(';')[:-1]
                                                print "Paired Devices List" , pairedDevicesList
                                                if actualresult == expectedresult:
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print "Bluetooth_GetPairedDevices call is SUCCESS"
                                                    for devices in range(len(pairedDevicesList)):  
                                                        pairedDeviceNameList.append(pairedDevicesList[devices].split(':')[0])
                                                    if str(bluetoothlib.deviceName) not in pairedDeviceNameList :
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print "DUT is successfully unpaired with Client device"
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "DUT is NOT unpaired with Client device"
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print "Bluetooth_GetPairedDevices call is FAILURE"
                                            else: 
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Bluetooth_UnpairDevice call is FAILURE" 
                                else:
                                    print"Externally Paired device property has INVALID value"
                                    tdkTestObj.setResultStatus("FAILURE");
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Bluetooth_GetDeviceProperties call is FAILURE"

                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Client device is NOT paired with DUT"
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Bluetooth_GetPairedDevices call is FAILURE"
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
