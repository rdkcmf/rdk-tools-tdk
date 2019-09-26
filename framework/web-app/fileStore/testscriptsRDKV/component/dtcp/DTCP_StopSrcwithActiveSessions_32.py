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
'''
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>13</version>
  <name>DTCP_StopSrcwithActiveSessions_32</name>
  <primitive_test_id/>
  <primitive_test_name>DTCP_Comp_Test</primitive_test_name>
  <primitive_test_version>3</primitive_test_version>
  <status>FREE</status>
  <synopsis>To stop DTCP-IP source without deleting active source and sink sessions.
There can be two approach for this (Refer RDKTT-641):
1) Cleanup of in-use sessions in DTCPMgrStopSource(), as done in intel
2) Return error from DTCPMgrStopSource() if there exist any in-use session, as done in broadcom.
TestType: Positive
TestcaseID: CT_DTCP_32</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DTCP_32</test_case_id>
    <test_objective>To stop DTCP-IP source without deleting active source and sink sessions.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>DTCPMgrInitialize</pre_requisite>
    <api_or_interface_used>dtcp_result_t DTCPMgrStartSource(char* ifName, int portNum);
dtcp_result_t DTCPMgrCreateSinkSession(char *srcIpAddress, int srcIpPort, BOOLEAN uniqueKey, int maxPacketSize, DTCP_SESSION_HANDLE *handle);
dtcp_result_t DTCPMgrCreateSourceSession(char *sinkIpAddress, int key_label, int PCPPacketSize, int maxPacketSize, DTCP_SESSION_HANDLE *handle);
dtcp_result_t DTCPMgrDeleteDTCPSession(DTCP_SESSION_HANDLE session);
dtcp_result_t DTCPMgrStopSource(void);</api_or_interface_used>
    <input_parameters>ifName':'lan0','port':5000
'srcIp':ip,'srcPort':5000,'uniqueKey':0,'maxPacketSize':4096
'sinkIp':ip,'keyLabel':0,'pcpPacketSize':0,'maxPacketSize':4096</input_parameters>
    <automation_approch>1.TM loads DTCP_agent via the test agent. 
2.The stub will invokes the RPC method for to stop active session.
3. The stub function will call the API and result will be shared back to TM
4. TM will receive and display the result.</automation_approch>
    <except_output>Checkpoint 1 stub will check for the return value of the function.</except_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_DTCP_Test_Execute</test_stub_interface>
    <test_script>DTCP_StopSrcwithActiveSessions_32</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import dtcp;
from random import randint

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("dtcp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DTCP_StopSrcwithActiveSessions_32');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "DTCP module loading status :  %s" %loadmodulestatus;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus.upper());

if "SUCCESS" in loadmodulestatus.upper():
  #Primitive test case which associated to this Script
  tdkTestObj = obj.createTestStep('DTCP_Comp_Test');

  expectedresult="SUCCESS";
  #Pre-cond: Init,StartSource,CreateSrcSession,CreateSinkSession
  dtcp.init(tdkTestObj,expectedresult);
  dtcp.setLogLevel(tdkTestObj,expectedresult,kwargs={"level":5})
  port = randint(5001, 6000);
  result = dtcp.startSource(tdkTestObj,expectedresult,kwargs={'ifName':'lo','port':port})
  if expectedresult in result:

        print "\nCreate sessions"
        dtcp.createSinkSession(tdkTestObj,expectedresult,kwargs={'srcIp':'127.0.0.1','srcPort':port,'uniqueKey':0,'maxPacketSize':4096})
        dtcp.createSourceSession(tdkTestObj,expectedresult,kwargs={'sinkIp':'127.0.0.1','keyLabel':0,'pcpPacketSize':0,'maxPacketSize':4096})
        dtcp.getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':2})

        #Stop source without deleting active sessions
        print "\n"
        fnName="DTCPMgrStopSource"
        #Add parameters to test object
        tdkTestObj.addParameter("funcName", fnName)
        #Execute the test case in STB
        tdkTestObj.executeTestCase("FAILURE")
        #Get the result of execution
        result = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        print "%s"%(fnName)
        print "Result: [%s]"%(result)
        print "Details: [%s]"%details
        tdkTestObj.setResultStatus("SUCCESS");

        #Return error from DTCPMgrStopSource() if there exist any in-use session
        if "FAILURE" == result:
            #Delete all sessions and Stop source again
            print "\nDelete source sessions"
            srcNum = int(dtcp.getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':0}))
            for index in range (0,srcNum):
                #dtcp.getSessionInfo(tdkTestObj,expectedresult,kwargs={"deviceType":0})
                dtcp.deleteSession(tdkTestObj,expectedresult,kwargs={"deviceType":0})

            print "\nDelete sink sessions"
            sinkNum = int(dtcp.getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':1}))
            for index in range (0,sinkNum):
                #dtcp.getSessionInfo(tdkTestObj,expectedresult,kwargs={"deviceType":1})
                dtcp.deleteSession(tdkTestObj,expectedresult,kwargs={"deviceType":1})

            print "\nGet number of src and sink sessions after deleting sessions"
            dtcp.getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':0})
            dtcp.getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':1})

            print "\nStop source after sessions cleanup"
            dtcp.stopSource(tdkTestObj,expectedresult)
        #Cleanup of in-use sessions in DTCPMgrStopSource()
        else:
            print "\nGet number of src and sink sessions after stop source"

            print "\n"
            fnName="DTCPMgrGetNumSessions";
            #Add parameters to test object
            deviceType=0
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
            if expectedresult in result and "0" in details:
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");

            print "\n"
            fnName="DTCPMgrGetNumSessions";
            #Add parameters to test object
            deviceType=1
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
            if expectedresult in result and "1" in details:
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");

  #Unload the dtcp module
  obj.unloadModule("dtcp");
