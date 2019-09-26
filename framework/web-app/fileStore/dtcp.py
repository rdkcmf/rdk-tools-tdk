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
import time;

# Description  : To initialize DTCP Manager
#
# Parameters   : tdkTestObj (Instance of dtcp common primitive testcase)
#              : expectedresult
#
# Return Value : "SUCCESS"/"FAILURE"
#
def init(tdkTestObj,expectedresult):

        print "\n"
	fnName="DTCPMgrInitialize";
	#Add parameters to test object
	tdkTestObj.addParameter("funcName", fnName); 
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);
        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
	print "%s"%(fnName)
	print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
 	print "Details: [%s]"%details

        #Set the result status of execution
        if expectedresult in result:
        	tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
		retValue = "FAILURE"

        return retValue

########## End of dtcpMgrInitialize Function ##########

def startSource(tdkTestObj,expectedresult,kwargs={}):

        print "\n"
        fnName="DTCPMgrStartSource";
        #Add parameters to test object
	ifName=str(kwargs["ifName"])
        port=int(kwargs["port"])
        tdkTestObj.addParameter("funcName", fnName);
	tdkTestObj.addParameter("strParam1", ifName);
	tdkTestObj.addParameter("intParam2", port);
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);
        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
	print "%s [ifName:%s port:%d]"%(fnName,ifName,port);
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details

        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue


def stopSource(tdkTestObj,expectedresult):

        print "\n"
        fnName="DTCPMgrStopSource"
        #Add parameters to test object
        tdkTestObj.addParameter("funcName", fnName)
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult)
        #Get the result of execution
        result = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        print "%s"%(fnName)
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details

        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue


def createSourceSession(tdkTestObj,expectedresult,kwargs={}):

        print "\n"
        fnName="DTCPMgrCreateSourceSession";

        #Add parameters to test object
        sinkIp=str(kwargs["sinkIp"])
        keyLabel=int(kwargs["keyLabel"])
	pcpPacketSize=int(kwargs["pcpPacketSize"])
	maxPacketSize=int(kwargs["maxPacketSize"])

  	tdkTestObj.addParameter("funcName", fnName);
  	tdkTestObj.addParameter("strParam1", sinkIp);
  	tdkTestObj.addParameter("intParam2", keyLabel);
  	tdkTestObj.addParameter("intParam3", pcpPacketSize);
  	tdkTestObj.addParameter("intParam4", maxPacketSize);

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);
        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
	print "%s [sinkIp:%s keyLabel:%d pcpPacketSize:%d maxPacketSize:%d]"%(fnName,sinkIp,keyLabel,pcpPacketSize,maxPacketSize);
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details

        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue


def createSinkSession(tdkTestObj,expectedresult,kwargs={}):

        print "\n"
        fnName="DTCPMgrCreateSinkSession";

        #Add parameters to test object
        srcIp=str(kwargs["srcIp"])
        srcPort=int(kwargs["srcPort"])
        uniqueKey=int(kwargs["uniqueKey"])
        maxPacketSize=int(kwargs["maxPacketSize"])

        tdkTestObj.addParameter("funcName", fnName);
        tdkTestObj.addParameter("strParam1", srcIp);
        tdkTestObj.addParameter("intParam2", srcPort);
        tdkTestObj.addParameter("intParam3", uniqueKey);
        tdkTestObj.addParameter("intParam4", maxPacketSize);

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);
        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
	print "%s [srcIp:%s srcPort:%d uniqueKey:%d maxPacketSize:%d]"%(fnName,srcIp,srcPort,uniqueKey,maxPacketSize)
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details

        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue


def processPacket(tdkTestObj,expectedresult,kwargs={}):

        print "\n"
        fnName="DTCPMgrProcessPacket"

        #Add parameters to test object
        tdkTestObj.addParameter("funcName", fnName)
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult)
        #Get the result of execution
        result = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
	print "%s"%(fnName)
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details
	time.sleep(10);
        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue


def releasePacket(tdkTestObj,expectedresult,kwargs={}):

        print "\n"
        fnName="DTCPMgrReleasePacket"
        #Add parameters to test object
        tdkTestObj.addParameter("funcName", fnName)
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult)
        #Get the result of execution
        result = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        print "%s"%(fnName)
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details
        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue


def deleteSession(tdkTestObj,expectedresult,kwargs={}):

        print "\n"
        fnName="DTCPMgrDeleteDTCPSession"
        #Add parameters to test object
        deviceType=int(kwargs["deviceType"])
        tdkTestObj.addParameter("funcName", fnName)
        tdkTestObj.addParameter("intParam3", deviceType);
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult)
        #Get the result of execution
        result = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        print "%s [deviceType:%d (0-source 1-sink 2-all) ]"%(fnName,deviceType)
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details
        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue

def getSessionInfo(tdkTestObj,expectedresult,kwargs={}):

        print "\n"
        fnName="DTCPMgrGetSessionInfo"

        #Add parameters to test object
        deviceType=int(kwargs["deviceType"])
        tdkTestObj.addParameter("funcName", fnName)
        tdkTestObj.addParameter("intParam3", deviceType);
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult)
        #Get the result of execution
        result = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        print "%s [deviceType:%d (0-source 1-sink 2-all) ]"%(fnName,deviceType)
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details
        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = details
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue

def getNumSessions(tdkTestObj,expectedresult,kwargs={}):

        print "\n"
        fnName="DTCPMgrGetNumSessions";
        #Add parameters to test object
        deviceType=int(kwargs["deviceType"])
        tdkTestObj.addParameter("funcName", fnName);
        tdkTestObj.addParameter("intParam2", deviceType);
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);
        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "%s [deviceType:%d (0-source 1-sink 2-all) ]"%(fnName,deviceType);
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Num of type(%d) sessions: [%s]"%(deviceType,details)

        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
        else:
                tdkTestObj.setResultStatus("FAILURE");

        return details


def setLogLevel(tdkTestObj,expectedresult,kwargs={}):

        print "\n"
        fnName="DTCPMgrSetLogLevel";
        #Add parameters to test object
        level=int(kwargs["level"])
        tdkTestObj.addParameter("funcName", fnName);
        tdkTestObj.addParameter("intParam2", level);
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);
        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "%s [level:%d]"%(fnName,level);
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details

        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
		retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
		retValue = "FAILURE"

        return retValue
