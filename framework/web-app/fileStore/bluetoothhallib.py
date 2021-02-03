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
        
