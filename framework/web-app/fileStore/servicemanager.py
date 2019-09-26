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

def registerService(obj,service_name):

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('SM_RegisterService')

    expectedresult = "SUCCESS"

    #Execute the test case in STB
    tdkTestObj.addParameter("service_name",service_name)
    tdkTestObj.executeTestCase(expectedresult)

    #Get the result of execution
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails()
    print "Details: ", details

    #Set the result status of execution
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS")
        retValue = "SUCCESS"
    else:
        tdkTestObj.setResultStatus("FAILURE")
        retValue = "FAILURE"

    return retValue


def unRegisterService(obj,service_name):

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('SM_UnRegisterService')

    expectedresult = "SUCCESS"

    #Execute the test case in STB
    tdkTestObj.addParameter("service_name",service_name)
    tdkTestObj.executeTestCase(expectedresult)

    #Get the result of execution
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails()
    print "Details: ", details

    #Set the result status of execution
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS")
        retValue = "SUCCESS"
    else:
        tdkTestObj.setResultStatus("FAILURE")
        retValue = "FAILURE"

    return retValue


def doesServiceExists(obj,service_name):

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('SM_DoesServiceExist')

    expectedresult = "SUCCESS"

    #Execute the test case in STB
    tdkTestObj.addParameter("service_name",service_name)
    tdkTestObj.executeTestCase(expectedresult)

    #Get the result of execution
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails()
    print "Details: ", details

    #Set the result status of execution
    if expectedresult in actualresult:
        if "PRESENT" in details:
		tdkTestObj.setResultStatus("SUCCESS")
		retValue = "SUCCESS"
	else:
		tdkTestObj.setResultStatus("FAILURE")
        	retValue = "FAILURE"
    else:
        tdkTestObj.setResultStatus("FAILURE")
        retValue = "FAILURE"

    return retValue


def DS_getSoundMode(obj,portName):

        tdkTestObj = obj.createTestStep('SM_DisplaySetting_GetSoundMode');
        expectedresult="SUCCESS"

        tdkTestObj.addParameter("portName", portName);
        tdkTestObj.executeTestCase(expectedresult);

        actualresult = tdkTestObj.getResult();
        serviceDetail = tdkTestObj.getResultDetails();
        ret_list = [actualresult, serviceDetail];

        print "[TEST EXECUTION DETAILS] sound mode is: %s"%serviceDetail;

        #Check for SUCCESS/FAILURE
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
        else:
                tdkTestObj.setResultStatus("FAILURE");

        return ret_list


def RunSMEvent(obj, service_name, event_name, event_param):

        tdkTestObj = obj.createTestStep('SM_RunSMEvent_QtApp');

        tdkTestObj.addParameter("service_name",service_name);
        tdkTestObj.addParameter("event_name",event_name);
        tdkTestObj.addParameter("event_param",event_param);

        expectedresult = "SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);

        actualresult= tdkTestObj.getResult();
        serviceDetail = tdkTestObj.getResultDetails();
        print "Details: ", serviceDetail

        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue
