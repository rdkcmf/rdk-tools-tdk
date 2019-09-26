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
  <version>5</version>
  <name>Bluetooth_Discoverable_On_List_Discovered_Devices_Unknown</name>
  <primitive_test_id/>
  <primitive_test_name>Bluetooth_GetDiscoveredDevices</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check whether discoverable  devices are listed in the discovered devices list when the decvice type is Unknown</synopsis>
  <groups_id/>
  <execution_time>2</execution_time>
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
    <test_case_id>CT_BLUETOOTH_35</test_case_id>
    <test_objective>To check whether discoverable  devices are listed in the discovered devices list when the decvice type is Unknown</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI5</test_setup>
    <pre_requisite>1.Set the values in bluetoothcredential.config
2. Initialize the bluetooth manager
BTRMGR_Init();
3. Deinit the bluetooth manager after test
BTRMGR_DeInit();</pre_requisite>
    <api_or_interface_used>bool Bluetooth_IsAdapterDiscoverable
bool Bluetooth_SetAdapterDiscoverable
Bluetooth_GetAdapterPowerStatus
Bluetooth_SetAdapterPowerStatus
Bluetooth_StartDeviceDiscovery
Bluetooth_StopDeviceDiscovery
Bluetooth_GetDiscoveredDevices</api_or_interface_used>
    <input_parameters>BTRMGR_IsAdapterDiscoverable(0,&amp;discoverableStatus);
BTRMGR_SetAdapterDiscoverable(0,discoverableStatus,Timeout);
BTRMGR_GetAdapterPowerStatus(0, &amp;powerStatus);
BTRMGR_SetAdapterPowerStatus(0,powerStatus);BTRMGR_StartDeviceDiscovery(0,devicetype);
BTRMGR_StopDeviceDiscovery(0,devicetype);
BTRMGR_GetDiscoveredDevices(0, &amp;discoveredDevices);</input_parameters>
    <automation_approch>1. TM loads the Bluetooth agent via the test agent.
2  Turn On the bluetotoh adapter if it is OFF
3. Turn on the discoverable status of DUT
4.Turn on the discoverable status of bluetooth emulator
5.Start the device discovery in DUT with Unknown as param
6.Stop the device discovery with the decvice type as Unknown after 30 seconds
7.Check the discovered devices list in DUT and confirm the bluetooth emulator adapter name is there in the list</automation_approch>
    <except_output>Checkpoint 1.Verify the API call return value
Checkpoint 2.The bluetooth emulator name should be there in the discovered devices list of DUT</except_output>
    <priority>High</priority>
    <test_stub_interface>libbluetoothstub.so.0</test_stub_interface>
    <test_script>Bluetooth_Discoverable_On_List_Discovered_Devices_Unknown</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import bluetoothlib;
from time import sleep

#Test component to be tested
bluetoothObj = tdklib.TDKScriptingLibrary("bluetooth","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
bluetoothObj.configureTestCase(ip,port,'Bluetooth_Discoverable_On_List_Discovered_Devices_Unknown');

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

   tdkTestObj = bluetoothObj.createTestStep('Bluetooth_SendRequest');
   #Execute the test case in STB
   tdkTestObj.executeTestCase(expectedresult);
   print "Set the client device as discoverable before starting the discovery in DUT"
   commandList = ['bluetoothctl','discoverable on','quit'] 
   output = bluetoothlib.executeBluetoothCtl(bluetoothObj,commandList)
   if "FAILURE" in output:
        print "Connecting to client device got failed"
        tdkTestObj.setResultStatus("FAILURE");
   else:
       tdkTestObj.setResultStatus("SUCCESS");
       print "Discoverable is enabled in Client Device" , bluetoothlib.deviceName
       print "Starting the device discovery in DUT"
       tdkTestObj = bluetoothObj.createTestStep('Bluetooth_StartDeviceDiscovery');
       tdkTestObj.addParameter("devicetype",8)
       #Execute the test case in STB
       tdkTestObj.executeTestCase(expectedresult);
       actualresult = tdkTestObj.getResult();
       if actualresult == expectedresult:
           tdkTestObj.setResultStatus("SUCCESS");
           print "Bluetooth_StartDeviceDiscovery call is SUCCESS"
           print "Wait for 30 seconds to disover the available devices"
           sleep(30);
           print "Stop the device discovery"
           tdkTestObj = bluetoothObj.createTestStep('Bluetooth_StopDeviceDiscovery');
	   tdkTestObj.addParameter("devicetype",8)
           #Execute the test case in STB
           tdkTestObj.executeTestCase(expectedresult);
           actualresult = tdkTestObj.getResult();
           if actualresult == expectedresult:
               tdkTestObj.setResultStatus("SUCCESS");
               print "Bluetooth_StopDeviceDiscovery call is SUCCESS"
               print "Check the discovered device list"
               tdkTestObj = bluetoothObj.createTestStep('Bluetooth_GetDiscoveredDevices');
               #Execute the test case in STB
               tdkTestObj.executeTestCase(expectedresult);
               actualresult = tdkTestObj.getResult();
               discoveredDevicesList = tdkTestObj.getResultDetails();
               discoveredDevicesList = discoveredDevicesList.split(';')[:-1]
               print "Discovered Devices List" , discoveredDevicesList
               if actualresult == expectedresult:
                   tdkTestObj.setResultStatus("SUCCESS");
                   print "Bluetooth_GetDiscoveredDevices call is SUCCESS"
                   deviceNameList=[]
                   for devices in range(len(discoveredDevicesList)):  
                       deviceNameList.append(discoveredDevicesList[devices].split(':')[0])
                   if str(bluetoothlib.deviceName) in deviceNameList :
                       tdkTestObj.setResultStatus("SUCCESS");
                       print "Client device is successfully discovered in DUT" 
                   else:
                       tdkTestObj.setResultStatus("FAILURE");
                       print "Client device is NOT discovered in DUT"
               else:
                   tdkTestObj.setResultStatus("FAILURE");
                   print "Bluetooth_GetDiscoveredDevices call is FAILURE"
           else: 
               tdkTestObj.setResultStatus("FAILURE");
               print "Bluetooth_StopDeviceDiscovery call is FAILURE"
       else:
           tdkTestObj.setResultStatus("FAILURE");
           print "Bluetooth_StartDeviceDiscovery call is FAILURE"


   bluetoothObj.unloadModule("bluetooth");

else:
    print "Failed to load bluetooth module\n";
    #Set the module loading status
    bluetoothObj.setLoadModuleStatus("FAILURE");
