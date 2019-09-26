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
  <name>Bluetooth_Persist_StartAudio_StreamingOut_Device_Properties</name>
  <primitive_test_id/>
  <primitive_test_name>Bluetooth_GetDeviceProperties</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check the connected device properties are persisting or not</synopsis>
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
    <test_case_id>CT_BLUETOOTH_47</test_case_id>
    <test_objective>To check the connected device properties are persisting or not</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI5</test_setup>
    <pre_requisite>1.Set the values in bluetoothcredential.config
2. Initialize the bluetooth manager
BTRMGR_Init();
3. Deinit the bluetooth manager after test
BTRMGR_DeInit();</pre_requisite>
    <api_or_interface_used>bool Bluetooth_GetAdapterPowerStatus
bool Bluetooth_SetAdapterPowerStatus
bool Bluetooth_StartDeviceDiscovery
bool Bluetooth_StopDeviceDiscovery
bool Bluetooth_GetDiscoveredDevices
bool Bluetooth_PairDevice
bool Bluetooth_GetPairedDevices
Bluetooth_StartAudioStreamingOut
Bluetooth_IsAudioStreamingOut
bool Bluetooth_GetConnectedDevices
bool Bluetooth_GetDeviceProperties
Bluetooth_StopAudioStreamingOut
bool Bluetooth_UnpairDevice</api_or_interface_used>
    <input_parameters>BTRMGR_GetAdapterPowerStatus(0, &amp;powerStatus);
BTRMGR_SetAdapterPowerStatus(0,powerStatus);BTRMGR_StartDeviceDiscovery(0);
BTRMGR_StopDeviceDiscovery(0);
BTRMGR_GetDiscoveredDevices(0, &amp;discoveredDevices);
BTRMGR_PairDevice(0, handle);
BTRMGR_UnpairDevice(0, handle);
BTRMGR_GetPairedDevices(0, &amp;pairedDevices);
BTRMGR_StartAudioStreamingOut(0, handle,BT_DEVICE_TYPE);
 BTRMGR_IsAudioStreamingOut(0,audioStreamingStatus);
BTRMGR_GetConnectedDevices(0, &amp;connectedDevices);
 BTRMGR_StopAudioStreamingOut(0, handle);
BTRMGR_GetDeviceProperties(0, handle, &amp;deviceProperty);</input_parameters>
    <automation_approch>1. TM loads the Bluetooth agent via the test agent.
2  Turn ON the bluetotoh adapter if it is OFF
3.Turn ON the discoverable status of bluetooth emulator
4.Start the device discovery with  the device type as audio output  in DUT
5.Stop the device discovery  with the device type as audio output after 30 seconds
6.Check the discovered devices list in DUT and confirm the bluetooth emulator adapter name is there in the list
7.Pair with the bluetooth emulator
8.Check the paired devices list in DUT and confirm the bluetooth emulator adapter name is there in the list
9.Start the audio out streaming in the device with device type audio output
10. .Check the audio streaming is started out not 
11.Reboot the box if audio streaming is started
12.Check the connected devices list in DUT and confirm the bluetooth emulator adapter name is there in the list
13.Get the device properties of the bluetooth emulator
14.Stop the audio streaming out and check audio streaming out is stopped or not then unpair the bluetooth emulator with the DUT</automation_approch>
    <except_output>Checkpoint 1.Verify the API call return value
Checkpoint 2.The bluetooth emulator name should be there in the discovered devices list of DUT
Checkpoint 3 After pairing the bluetooth emulator name should be there in the paired devices list of DUT
Checkpoint 4 After started audio streaming out and reboot the DUT then check the bluetooth emulator name in the connectedevices list of DUT.After that check connected device propery value is 1 or not
Checkpoint 5 After stopping audio streaming out, the bluetooth emulator name should NOT be there in the connected devices list of DUT
Checkpoint 6 After unpair, the bluetooth emulator name should NOT be there in the paired devices list of DUT</except_output>
    <priority>High</priority>
    <test_stub_interface>libbluetoothstub.so.0</test_stub_interface>
    <test_script>Bluetooth_Persist_StartAudio_StreamingOut_Device_Properties</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import bluetoothlib;
import json;
from time import sleep

#Test component to be tested
bluetoothObj = tdklib.TDKScriptingLibrary("bluetooth","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
bluetoothObj.configureTestCase(ip,port,'Bluetooth_Persist_StartAudio_StreamingOut_Device_Properties');

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

def isAudioStreamingOut():
    tdkTestObj = bluetoothObj.createTestStep('Bluetooth_IsAudioStreamingOut')
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    audioStreamingStatus = tdkTestObj.getResultDetails();
    print "Audio Streaming Status " , audioStreamingStatus
    if actualresult == expectedresult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "Bluetooth_IsAudioStreamingOut call is SUCCESS"
        return audioStreamingStatus
    else:
        print "Bluetooth_IsAudioStreamingOut call is FAILURE"
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
   commandList = ['bt-agent &','bluetoothctl','discoverable on','quit'] 
   output = bluetoothlib.executeBluetoothCtl(bluetoothObj,commandList)
   if "FAILURE" in output:
        tdkTestObj.setResultStatus("FAILURE");
        print "Connecting to client device got failed"
   else:
       tdkTestObj.setResultStatus("SUCCESS");
       print "Discoverable is enabled in Client Device" , bluetoothlib.deviceName
       print "Starting the device discovery in DUT"
       tdkTestObj = bluetoothObj.createTestStep('Bluetooth_StartDeviceDiscovery');
       tdkTestObj.addParameter("devicetype",1)
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
           tdkTestObj.addParameter("devicetype",1)
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
                   deviceHandleList=[]
                   for devices in range(len(discoveredDevicesList)):  
                       deviceNameList.append(discoveredDevicesList[devices].split(':')[0])  
                       deviceHandleList.append(discoveredDevicesList[devices].split(':')[1]) 
                   if str(bluetoothlib.deviceName) in deviceNameList :
                       tdkTestObj.setResultStatus("SUCCESS");
                       print "Client device is successfully discovered in DUT" 
                       deviceNameIndex = deviceNameList.index(str(bluetoothlib.deviceName))
                       handleNumber = deviceHandleList[deviceNameIndex]
                       print "Device Handle Number", handleNumber
                       tdkTestObj = bluetoothObj.createTestStep('Bluetooth_PairDevice')
                       tdkTestObj.addParameter("devicehandle",handleNumber);
                       #Execute the test case in STB
                       tdkTestObj.executeTestCase(expectedresult);
                       actualresult = tdkTestObj.getResult();
                       if actualresult == expectedresult:
                           tdkTestObj.setResultStatus("SUCCESS");
                           print "Bluetooth_PairDevice call is SUCCESS"
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
                               pairedDeviceNameList=[]
                               for devices in range(len(pairedDevicesList)):  
                                   pairedDeviceNameList.append(pairedDevicesList[devices].split(':')[0])
                               if str(bluetoothlib.deviceName) in pairedDeviceNameList :
                                   tdkTestObj.setResultStatus("SUCCESS");
                                   print "Client device is successfully paired with DUT"
                                   print "Start the audio streaming out with device type as audio out"
                                   tdkTestObj = bluetoothObj.createTestStep('Bluetooth_StartAudioStreamingOut')
                                   tdkTestObj.addParameter("devicehandle",handleNumber);
                                   tdkTestObj.addParameter("devicetype",1)
                                   #Execute the test case in STB
                                   tdkTestObj.executeTestCase(expectedresult);
                                   actualresult = tdkTestObj.getResult();
                                   if actualresult == expectedresult:
                                       tdkTestObj.setResultStatus("SUCCESS");
                                       print "Bluetooth_StartAudioStreamingOut call is SUCCESS with device type as audio output"
                                       print "Check the audio stream out is started or not"
                                       audioStreamingStartStatus = isAudioStreamingOut()
                                       if audioStreamingStartStatus == '1':
                                           tdkTestObj.setResultStatus("SUCCESS");
                                           print "Audio Streaming Out Started Successfully with device type as audio output"
                                           #Reboot the STB
                                           bluetoothObj.initiateReboot(); 
                                           sleep(60);
                                           print "Set the client device as discoverable"
                                           commandList = ['bluetoothctl','discoverable on','quit'] 
                                           output = bluetoothlib.executeBluetoothCtl(bluetoothObj,commandList)
                                           if "FAILURE" in output:
                                               tdkTestObj.setResultStatus("FAILURE");
                                               print "Connecting to client device got FAILED"
                                           else:
                                               print "Discoverable is enabled in Client Device" , bluetoothlib.deviceName
                                               tdkTestObj = bluetoothObj.createTestStep('Bluetooth_GetConnectedDevices')
                                               #Execute the test case in STB
                                               tdkTestObj.executeTestCase(expectedresult);
                                               actualresult = tdkTestObj.getResult();
                                               if actualresult == expectedresult:
                                                   tdkTestObj.setResultStatus("SUCCESS");
                                                   print "Bluetooth_GetConnectedDevices call is SUCCESS"
                                                   connectedDevicesList = tdkTestObj.getResultDetails();
                                                   connectedDevicesList = connectedDevicesList.split(';')[:-1]
                                                   print "Connected Devices List" , connectedDevicesList
                                                   connectedDeviceNameList=[]
                                                   for devices in range(len(connectedDevicesList)):  
                                                       connectedDeviceNameList.append(connectedDevicesList[devices].split(':')[0])
                                                   if str(bluetoothlib.deviceName) in connectedDeviceNameList :
                                                       tdkTestObj.setResultStatus("SUCCESS");
                                                       print "Client device is successfully reconnected with DUT"
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
                                                           if "1" in deviceProperties['connected']:
                                                               tdkTestObj.setResultStatus("SUCCESS");
                                                               print"Connected Device properties are persisted"
                                                           else:
                                                               print"Connected Device properties are NOT persisted"
                                                               tdkTestObj.setResultStatus("FAILURE");
                                                       else:
                                                           tdkTestObj.setResultStatus("FAILURE");
                                                   else:
                                                       tdkTestObj.setResultStatus("FAILURE");
                                                       print "Client device is NOT reconnected with DUT"
                                               else:
                                                   tdkTestObj.setResultStatus("FAILURE");
                                                   print "Bluetooth_GetConnectedDevices call is FAILURE"
                                          
                                           print "Stop the Audio streaming out"
                                           tdkTestObj = bluetoothObj.createTestStep('Bluetooth_StopAudioStreamingOut')
                                           tdkTestObj.addParameter("devicehandle",handleNumber);
                                           #Execute the test case in STB
                                           tdkTestObj.executeTestCase(expectedresult);
                                           actualresult = tdkTestObj.getResult();
                                           if actualresult == expectedresult:
                                               tdkTestObj.setResultStatus("SUCCESS");
                                               print "Bluetooth_StopAudioStreamingOut call is SUCCESS"
                                           else:
                                               tdkTestObj.setResultStatus("FAILURE");
                                               print "Bluetooth_StopAudioStreamingOut call is FAILURE"

                                           print "Check the audio stream out is stopped or not"
                                           audioStreamingStopStatus = isAudioStreamingOut()
                                           if(audioStreamingStopStatus == '0'):
                                               tdkTestObj.setResultStatus("SUCCESS");
                                               print "Audio Streaming Out is Stopped Successfully"
                                           else: 
                                               tdkTestObj.setResultStatus("FAILURE");
                                               print "Audio Streaming Out is NOT Stopped"
                                           
                                       else: 
                                           tdkTestObj.setResultStatus("FAILURE"); 
                                           print "Audio Streaming Out is NOT Started with device type as audio output"
                                   else: 
                                       tdkTestObj.setResultStatus("FAILURE");
                                       print "Bluetooth_StartAudioStreamingOut call is FAILURE"      

                                   print "Unpair the client device" 
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
                                           pairedDeviceNameList=[]
                                           for devices in range(len(pairedDevicesList)):  
                                               pairedDeviceNameList.append(pairedDevicesList[devices].split(':')[0])
                                           if str(bluetoothlib.deviceName) not in pairedDeviceNameList :
                                               tdkTestObj.setResultStatus("SUCCESS");
                                               print "Client device is successfully unpaired with DUT" 
                                           else:
                                               tdkTestObj.setResultStatus("FAILURE");
                                               print "Client device is NOT unpaired with DUT"
                                       else:
                                           tdkTestObj.setResultStatus("FAILURE");
                                           print "Bluetooth_GetPairedDevices call is FAILURE"
                                   else: 
                                       tdkTestObj.setResultStatus("FAILURE");
                                       print "Bluetooth_UnpairDevice call is FAILURE" 
                               else:
                                   tdkTestObj.setResultStatus("FAILURE");
                                   print "Client device is NOT paired with DUT"
                           else:
                               tdkTestObj.setResultStatus("FAILURE");
                               print "Bluetooth_GetPairedDevices call is FAILURE"
                       else: 
                           tdkTestObj.setResultStatus("FAILURE");
                           print "Bluetooth_PairDevice call is FAILURE"
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

       tdkTestObj = bluetoothObj.createTestStep('Bluetooth_SendRequest');
       #Execute the test case in STB
       tdkTestObj.executeTestCase(expectedresult);
       print "Stop the bt-agent"
       commandList = ['pkill bt-agent']
       output = bluetoothlib.executeBluetoothCtl(bluetoothObj,commandList)
       if "FAILURE" in output:
            tdkTestObj.setResultStatus("FAILURE");
            print "Connecting to client device got failed"
       else:
           tdkTestObj.setResultStatus("SUCCESS");
           print "BT agent stopped successfully"

   bluetoothObj.unloadModule("bluetooth");

else:
    print "Failed to load bluetooth module\n";
    #Set the module loading status
    bluetoothObj.setLoadModuleStatus("FAILURE");

