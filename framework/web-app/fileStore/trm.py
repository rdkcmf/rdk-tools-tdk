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

# To fetch max tuners supported by gateway box.
#
# Syntax       : getMaxTuner(obj)
#
# Parameters   : obj
#
# Return Value : maxValue on success and 0 on failure

def getMaxTuner(obj,expectedresult):

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TRM_GetMaxTuners');

    print "\n"
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
    maxTuner = int(details)

    #Set the result status of execution
    if "SUCCESS" in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

    print "Max tuners supported: ",maxTuner
    print "\n"
    return maxTuner

#######################################################

# To initiate reserve tuner for live.
#
# Syntax       : reserveForLive(obj,expectedresult,kwargs={})
#
# Parameters   : deviceNo,duration,streamId,startTime
#
# Return Value : NONE

def reserveForLive(obj,expectedresult,kwargs={}):

    #Primitive test case associated to the function
    tdkTestObj = obj.createTestStep('TRM_TunerReserveForLive');

    deviceNo = int(kwargs["deviceNo"])
    duration = int(kwargs["duration"])
    streamId = str(kwargs["streamId"])
    startTime = int(kwargs["startTime"])
    locator = "ocap://"+tdkTestObj.getStreamDetails(streamId).getOCAPID()

    tdkTestObj.addParameter("deviceNo",deviceNo);
    tdkTestObj.addParameter("duration",duration);
    tdkTestObj.addParameter("locator",locator);
    tdkTestObj.addParameter("startTime", startTime);

    print "\nDeviceNo:%d locator:%s duration:%d startTime:%d"%(deviceNo,locator,duration,startTime),

    if 'token' in kwargs:
        token = str(kwargs["token"])
        tdkTestObj.addParameter("token", token);
        print " token:%s"%token,

    if 'selectOnConflict' in kwargs:
        conflict = int(kwargs["selectOnConflict"])
        tdkTestObj.addParameter("selectOnConflict", conflict);
        print " SelectOnConflict:%d"%conflict

    print "\n"
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result/details of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
    print "Details: ",details

    #Set the result status of execution
    if expectedresult in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

    print "\n"
    return details

#######################################################

# To initiate reserve tuner for record.
#
# Syntax       : reserveForRecord(obj,expectedresult,kwargs={})
#
# Parameters   : deviceNo,duration,streamId,startTime,recordingId,hot
#
# Return Value : NONE

def reserveForRecord(obj,expectedresult,kwargs={}):

    #Primitive test case associated to the function
    tdkTestObj = obj.createTestStep('TRM_TunerReserveForRecord');

    deviceNo = int(kwargs["deviceNo"])
    duration = int(kwargs["duration"])
    streamId = str(kwargs["streamId"])
    startTime = int(kwargs["startTime"])
    recordingId = str(kwargs["recordingId"])
    hot = int(kwargs["hot"])
    locator = "ocap://"+tdkTestObj.getStreamDetails(streamId).getOCAPID()

    tdkTestObj.addParameter("deviceNo",deviceNo);
    tdkTestObj.addParameter("duration",duration);
    tdkTestObj.addParameter("locator",locator);
    tdkTestObj.addParameter("startTime", startTime);
    tdkTestObj.addParameter("recordingId",recordingId);
    tdkTestObj.addParameter("hot",hot);

    print "\nDeviceNo:%d locator:%s duration:%d startTime:%d recordingId:%s hot:%d"%(deviceNo,locator,duration,startTime,recordingId,hot),

    if 'token' in kwargs:
        token = str(kwargs["token"])
        tdkTestObj.addParameter("token", token);
        print " token:%s"%token,

    if 'selectOnConflict' in kwargs:
        conflict = int(kwargs["selectOnConflict"])
        tdkTestObj.addParameter("selectOnConflict", conflict);
        print " SelectOnConflict:%d"%conflict

    print "\n"

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result/details of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
    print "Details: ",details

    #Set the result status of execution
    if expectedresult in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

    print "\n"
    return details

#######################################################

def cancelRecording(obj,expectedresult,kwargs={}):

    #Primitive test case associated to the function
    tdkTestObj = obj.createTestStep('TRM_CancelRecording');

    streamId = str(kwargs["streamId"])
    locator = "ocap://"+tdkTestObj.getStreamDetails(streamId).getOCAPID()

    tdkTestObj.addParameter("locator",locator);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result/details of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "Locator: %s"%(locator)
    print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
    print "Details: [%s]"%details

    #Set the result status of execution
    if expectedresult in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

    print "\n"

#######################################################

def releaseReservation(obj,expectedresult,kwargs={}):

    #Primitive test case associated to the function
    tdkTestObj = obj.createTestStep('TRM_ReleaseTunerReservation');

    deviceNo = int(kwargs["deviceNo"])
    activity = int(kwargs["activity"])
    streamId = str(kwargs["streamId"])
    locator = "ocap://"+tdkTestObj.getStreamDetails(streamId).getOCAPID()

    tdkTestObj.addParameter("deviceNo",deviceNo);
    tdkTestObj.addParameter("activity",activity);
    tdkTestObj.addParameter("locator",locator);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    if (1 == activity):
        Activity = 'Live'
    else:
        Activity = 'Record'

    #Get the result/details of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "activity:%s deviceNo:%d locator:%s"%(Activity,deviceNo,locator)
    print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
    print "Details: [%s]"%details

    #Set the result status of execution
    if expectedresult in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

    print "\n"

#######################################################
def validateReservation(obj,expectedresult,kwargs={}):

    #Primitive test case associated to the function
    tdkTestObj = obj.createTestStep('TRM_ValidateTunerReservation');

    deviceNo = int(kwargs["deviceNo"])
    activity = int(kwargs["activity"])
    streamId = str(kwargs["streamId"])
    locator = "ocap://"+tdkTestObj.getStreamDetails(streamId).getOCAPID()

    tdkTestObj.addParameter("deviceNo",deviceNo);
    tdkTestObj.addParameter("activity",activity);
    tdkTestObj.addParameter("locator",locator);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    if (1 == activity):
        Activity = 'Live'
    else:
        Activity = 'Record'

    #Get the result/details of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "activity:%s deviceNo:%d locator:%s"%(Activity,deviceNo,locator)
    print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
    print "Details: [%s]"%details

    #Set the result status of execution
    if expectedresult in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

    print "\n"

#######################################################

def getAllTunerStates(obj,expectedresult):

    #Primitive test case associated to the function
    tdkTestObj = obj.createTestStep('TRM_GetAllTunerStates');

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
    print "Details: [%s]"%details

    #Set the result status of execution
    if expectedresult in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

    print "\n"
    return details

#######################################################

def getAllReservations(obj,expectedresult,kwargs={}):

    #Primitive test case associated to the function
    tdkTestObj = obj.createTestStep('TRM_GetAllReservations');

    if 'deviceNo' in kwargs:
        deviceNo = int(kwargs["deviceNo"])
        tdkTestObj.addParameter("deviceNo",deviceNo);
        print "Fetching reservation info for deviceNo: ",deviceNo
    else:
        print "Fetching all reservations"

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
    print "Details: [%s]"%details

    #Set the result status of execution
    if expectedresult in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

    print "\n"

#######################################################

def getAllTunerIds(obj,expectedresult):

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TRM_GetAllTunerIds');

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
    print "Details: [%s]"%details

    #Set the result status of execution
    if expectedresult in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

    print "\n"

#######################################################

def getVersion(obj,expectedresult):

    #Primitive test case associated to the function
    tdkTestObj = obj.createTestStep('TRM_GetVersion');

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
    print "Details: [%s]"%details

    #Set the result status of execution
    if expectedresult in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

    print "\n"
    return details

#######################################################
