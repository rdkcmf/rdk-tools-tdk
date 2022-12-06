#!/usr/bin/python
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

import ConfigParser
import json
from pexpect import pxssh
from time import sleep
import bluetoothhallib;

##################################################################
# Methods
#################################################################
def setAdapterPowerON (bluetoothhalObj, adapterPath):

    try :
        expectedresult = "SUCCESS"
        powerON = 1
        #Set the power status to powerStatusToBeSet
        print "Setting the bluetooth adapter power ON"
        tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_SetAdapterPower');
        #Set the adapter path to the default adapter path
        tdkTestObj.addParameter("adapter_path", adapterPath)
        tdkTestObj.addParameter("power_status", powerON)

        #Execute the test case in DUT
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
                currentPowerStatus = int (tdkTestObj.getResultDetails())
                if (powerON == currentPowerStatus):
                    print "Adapter powered ON successfully"
                    tdkTestObj.setResultStatus("SUCCESS");
                else:
                    print "Adapter could not be powered ON"
                    actualresult = "FAILURE"
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                print "Failed to get adapter power"
                tdkTestObj.setResultStatus("FAILURE");
        else:
            print "Failed to set adapter power"
            tdkTestObj.setResultStatus("FAILURE");

    except Exception, e:
        print e;
        actualresult = "FAILURE"

    return actualresult


##################################################
#
# Method to execute the commands in client device shell
#
##################################################

def executeBluetoothCtl(bluetoothObj,commands):

    try :

        #Get Bluetooth configuration file
        bluetoothConfigFile = bluetoothObj.realpath+'fileStore/bluetoothcredential.config'
        configParser = ConfigParser.ConfigParser()
        configParser.read(r'%s' % bluetoothConfigFile)
        ip = configParser.get('bluetooth-config', 'ip')
        username = configParser.get('bluetooth-config', 'username')
        password = configParser.get('bluetooth-config', 'password')
        global deviceName;
        deviceName = configParser.get('bluetooth-config','devicename')
        BT_Mac =  configParser.get('bluetooth-config','DUT_BT_controller_mac')
        #Executing the commands in device
        print 'Number of commands:', len(commands)
        print 'Commands List:', commands
        print "Connecting to client device"
        global session
        session = pxssh.pxssh(options={
                            "StrictHostKeyChecking": "no",
                            "UserKnownHostsFile": "/dev/null"})
        session.login(ip,username,password,sync_multiplier=3)
        print "Executing the bluetoothctl commands"
        for parameters in range(0,len(commands)):
            if 'scan on' in commands[parameters]:
                session.sendline(commands[parameters])
                print "Scanning started"
                sleep(20);
            elif 'pair' in commands[parameters]:
                commands[parameters] += ' '+ BT_Mac;
                session.sendline(commands[parameters])
                print "Paired with DUT"
                sleep(3);
            elif 'remove' in commands[parameters]:
                commands[parameters] += ' '+ BT_Mac;
                session.sendline(commands[parameters])
                print "Un Paired with DUT"
                sleep(3);
            else:
                session.sendline(commands[parameters])
        session.prompt()
        status = session.before
        print "Successfully Executed bluetoothctl commands in client device"

    except Exception, e:
        print e;
        status = "FAILURE"

    return status

##################################################
#
# Method to close the ssh session in the client device
#
##################################################

def closeSSHSession ():

    if session:
        print "Closing the ssh session with bluetooth client device"
        session.logout()
        session.close()

######################################################
#
# Method to query the device type from the config file
#
######################################################

def DeviceType (bluetoothObj):
    try :

        #Get Bluetooth configuration file
        bluetoothConfigFile = bluetoothObj.realpath+'fileStore/bluetoothcredential.config'
        configParser = ConfigParser.ConfigParser()
        configParser.read(r'%s' % bluetoothConfigFile)
        deviceType = configParser.get('bluetooth-config', 'deviceType')
        if "AudioIn" in deviceType or "AudioOut" in deviceType:
            return "I/O"
        elif "HID" in deviceType:
            return "HID"
        elif "LE" in deviceType:
            return "LE"
        else:
            print "Configuration parameter missing for isDeviceLE in bluetoothcredential.config"
            print "Please configure to execute the script"
            exit()

    except Exception, e:
        print e;
        exit()

###############################################################################################
#
# Method to retrieve the list of paired devices and traverse the list to find the client device
#
###############################################################################################

def checkDeviceInPairedList(bluetoothhalObj,deviceID_check):
    devicePaired = False
    expectedresult = "SUCCESS"
    tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_GetListOfPairedDevices');
    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    actualresult = tdkTestObj.getResult();

    if (actualresult == expectedresult):
        print "BluetoothHal_GetListOfPairedDevices executed successfully"
        tdkTestObj.setResultStatus("SUCCESS")
        pairResult = tdkTestObj.getResultDetails()
        if pairResult and "NO_DEVICES_PAIRED" != pairResult :
            pairedDevices = json.loads(pairResult)
            #Traverse the paired devices list to check if the client device is present
            for device in pairedDevices :
                if (str(device["deviceID"]) == deviceID_check):
                    devicePaired = True
        else:
            print "Paired devices list is empty"
    else:
        print "BluetoothHal_GetListOfPairedDevices: failed"
        tdkTestObj.setResultStatus("FAILURE")

    return devicePaired

#######################################################################################################
#
# Method to unpair emulator from DUT if already paired in order to proceed with next execution properly
#
#######################################################################################################

def Unpair_if_paired(bluetoothhalObj):
    expectedresult = "SUCCESS"
    tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_GetListOfPairedDevices');
    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    actualresult = tdkTestObj.getResult();

    if (actualresult == expectedresult):
        print "BluetoothHal_GetListOfPairedDevices executed successfully"
        tdkTestObj.setResultStatus("SUCCESS")
        pairResult = tdkTestObj.getResultDetails()
        if pairResult and "NO_DEVICES_PAIRED" != pairResult :
            pairedDevices = json.loads(pairResult)
            #Traverse the paired devices list to check if the client device is present
            for device in pairedDevices :
                if str(device["deviceName"]) == bluetoothhallib.deviceName:
                    print "%s device with device Handle %s is Paired, unpairing from DUT"%(str(device["deviceName"]),str(device["deviceID"]))
                    tdkTestObj = bluetoothhalObj.createTestStep('BluetoothHal_UnPairDevice');
                    #Set device ID as the bluetooth client device ID
                    deviceID = str(device["deviceID"])
                    tdkTestObj.addParameter("device_id", deviceID)
                    #Execute the test case in DUT
                    tdkTestObj.executeTestCase(expectedresult);

                    #Get the result of execution
                    actualresult = tdkTestObj.getResult();

                    if (actualresult == expectedresult):
                        print "BluetoothHal_UnPairDevice executed successfully"
                        tdkTestObj.setResultStatus("SUCCESS")
                        #Retrieve the list of paired devices
                        devicePaired = checkDeviceInPairedList(bluetoothhalObj,deviceID)
                        if True == devicePaired:
                            print "Client device is not unpaired from DUT"
                            tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "Client device is successfully unpaired from DUT"
                            tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print "Unpair failed"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "%s device is not paired with the DUT. Proceeding with the execution"%(bluetoothhallib.deviceName)
        else:
            print "Paired devices list is empty"
    else:
        print "BluetoothHal_GetListOfPairedDevices: failed"
        tdkTestObj.setResultStatus("FAILURE")
