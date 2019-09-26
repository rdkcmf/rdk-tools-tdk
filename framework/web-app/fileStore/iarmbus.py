#!/usr/bin/python
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
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

#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import tdklib;

def IARMBUS_Init(obj,expectedresult):

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('IARMBUS_Init')

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult)

    #Get the result of execution
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails()
    print "Result: IARMBus Init [%s]"%(actualresult)

    #Set the result status of execution
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS")
        retValue = "SUCCESS"
    else:
        print "Failure Details: [%s]"%(details)
        tdkTestObj.setResultStatus("FAILURE")
        retValue = "FAILURE"

    return retValue


def IARMBUS_Connect(obj,expectedresult):

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('IARMBUS_Connect')

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult)

    #Get the result of execution
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails()
    print "Result: IARMBus Connect [%s]"%(actualresult)

    #Set the result status of execution
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS")
        retValue = "SUCCESS"
    else:
        print "Failure Details: [%s]"%(details)
        tdkTestObj.setResultStatus("FAILURE")
        retValue = "FAILURE"

    return retValue


def IARMBUS_DisConnect(obj,expectedresult):

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('IARMBUS_DisConnect')

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult)

    #Get the result of execution
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails()
    print "Result: IARMBus DisConnect [%s]"%(actualresult)

    #Set the result status of execution
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS")
        retValue = "SUCCESS"
    else:
        print "Failure Details: [%s]"%(details)
        tdkTestObj.setResultStatus("FAILURE")
        retValue = "FAILURE"

    return retValue


def IARMBUS_Term(obj,expectedresult):

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('IARMBUS_Term')

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult)

    #Get the result of execution
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails()
    print "Result: IARMBus Term [%s]"%(actualresult)

    #Set the result status of execution
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS")
        retValue = "SUCCESS"
    else:
        print "Failure Details: [%s]"%(details)
        tdkTestObj.setResultStatus("FAILURE")
        retValue = "FAILURE"

    return retValue


def change_powermode(obj,mode):

    #Setting the POWER state
    tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
    tdkTestObj.addParameter("method_name","SetPowerState");
    tdkTestObj.addParameter("owner_name","PWRMgr");               
    tdkTestObj.addParameter("newState",mode);        
    expectedresult="SUCCESS"
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details=tdkTestObj.getResultDetails();
    print "set power state: %s" %details;
    #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
    before_set_powerstate = details;
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS");
        retValue = "SUCCESS";
        print "SUCCESS: Setting STB power state -RPC method invoked successfully";
        #Querying the STB power state
        tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
        tdkTestObj.addParameter("method_name","GetPowerState");
        tdkTestObj.addParameter("owner_name","PWRMgr");
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details=tdkTestObj.getResultDetails();
        print "current power state: %s" %details;
        #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
        after_set_powerset=details;
        if expectedresult in actualresult:                      
            print "SUCCESS: Querying STB power state -RPC method invoked successfully";
            if before_set_powerstate == after_set_powerset :
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS";
                print "SUCCESS: Both the Power states are equal";
            else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"
                print "FAILURE: Both power states are different";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            retValue = "FAILURE"
            print "FAILURE: Querying STB power state - IARM_Bus_Call failed. %s " %details;
    else:
        tdkTestObj.setResultStatus("FAILURE");
        retValue = "FAILURE"
        print "FAILURE: Set STB power state - IARM_Bus_Call failed. %s " %details;
            
    return retValue;
