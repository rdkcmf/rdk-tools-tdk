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
  <version>2</version>
  <name>IARMBUS_DummyEvt_Persistent_test_LD</name>
  <primitive_test_id>22</primitive_test_id>
  <primitive_test_name>IARMBUS_RegisterEventHandler</primitive_test_name>
  <primitive_test_version>15</primitive_test_version>
  <status>FREE</status>
  <synopsis>As per RDKTT-620</synopsis>
  <groups_id/>
  <execution_time>300</execution_time>
  <long_duration>true</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_IARMBUS_121</test_case_id>
    <test_objective>IARMBUS – Broadcasting and Receiving of Dummy Event for 'x' times</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1 / XG1-1</test_setup>
    <pre_requisite>“IARMDaemonMain” process should be running.</pre_requisite>
    <api_or_interface_used>IARM_Bus_Init(char *)
IARM_Bus_Connect()
IARM_Bus_RegisterEventHandler(const char* , IARM_EventId_t , IARM_EventHandler_t )
IARM_Bus_BroadcastEvent(const char *, IARM_EventId_t , void *, size_t )
IARM_Bus_UnRegisterEventHandler(const char*, IARM_EventId_t )
IARM_Bus_Disconnect()
IARM_Bus_Term()</api_or_interface_used>
    <input_parameters>IARM_Bus_Init : 
char *  - (test agent process_name)
IARM_Bus_Connect : None
IARM_Bus_RegisterEventHandler : 
const char * - IARM_BUS_DUMMYMGR_NAME , IARM_EventId_t - IARM_BUS_DUMMYMGR_EVENT_DUMMYX, IARM_EventHandler_t - _handler_ResolutionChange 
IARM_Bus_BroadcastEvent :
Const char* - IARM_BUS_DUMMYMGR_NAME,
IARM_EventId_t – IARM_BUS_DUMMYMGR_EVENT_DUMMYX ,
Void * - eventdata, size_t – sizeof (eventdata)
IARM_Bus_UnRegisterEventHandler : 
const char* – IARM_BUS_DUMMYMGR_NAME , IARM_EventId_t – IARM_BUS_DUMMYMGR_EVENT_DUMMYX
IARM_Bus_Disconnect : None
IARM_Bus_Term : None</input_parameters>
    <automation_approch>1.TM loads the IARMBUS_Agent via the test agent
2.The IARMBUS_Agent initializes and registers with IARM Bus Daemon (First Application).
3.TM loads(initializes and registers) another application with IARM Daemon(second application which broadcasts the Dummy events) .
4.IARMBUS_Agent will register for “IARM_BUS_EVENT_RESOLUTIONCHANGE” event and waits on event.
5.Second application will broadcast the event to the bus.
6.IARMBUS_Agent should receive the event and event handler should handle the event(printing some log message) .
7. Repeat steps3 to 6 for 'x' times .
8.IARMBUS_Agent deregisters from the IARM Bus Daemon.
9.For each API called in the script, IARMBUS_Agent will send SUCCESS or FAILURE status to Test Agent by comparing the return vale of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.

Checkpoint 2. Check for  the print  message.</except_output>
    <priority>High</priority>
    <test_stub_interface>libiarmbusstub.so
1.TestMgr_IARMBUS_Init
2.TestMgr_IARMBUS_Term
3.TestMgr_IARMBUS_Connect
4.TestMgr_IARMBUS_Disconnect
5.TestMgr_IARMBUS_BroadcastEvent
6.TestMgr_IARMBUS_RegisterEventHandler
7.TestMgr_IARMBUS_UnRegisterEventHandler
8.TestMgr_IARMBUS_InvokeSecondApplication</test_stub_interface>
    <test_script>IARMBUS_DummyEvt_Persistent_test_LD</test_script>
    <skipped>No</skipped>
    <release_version>M33</release_version>
    <remarks>Developed on request through RDKTT-620</remarks>
  </test_cases>
  <script_tags/>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import re
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'IARMBUS_DummyEvt_Persistent_test_LD');
loadmodulestatus =obj.getLoadModuleResult();
print "Iarmbus module loading status :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        #calling IARMBUS API "IARM_Bus_Init"
        tdkTestObj = obj.createTestStep('IARMBUS_Init');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details=tdkTestObj.getResultDetails();
        #Check for SUCCESS/FAILURE return value of IARMBUS_Init
        if ("SUCCESS" in actualresult):
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: Application successfully initialized with IARMBUS library";
                #calling IARMBUS API "IARM_Bus_Connect"
                tdkTestObj = obj.createTestStep('IARMBUS_Connect');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details=tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of IARMBUS_Connect
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: Application successfully connected with IARM-Bus Daemon";
                        i=0;
                        for i in range(0,100000):
                                				
                                print "**************** Iteration ", (i+1), " ****************";
                                tdkTestObj = obj.createTestStep('IARMBUS_InvokeSecondApplication');
                                tdkTestObj.addParameter("appname","DUMMYMgr");
                                tdkTestObj.addParameter("argv1","");
                                tdkTestObj.addParameter("apptype","background");
                                tdkTestObj.addParameter("iterationcount",i);
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                #details=tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Second application Invoked successfully";

                                        time.sleep(2)			
                                        #calling IARMBUS API "IARM_Bus_RegisterEventHandler"
                                        tdkTestObj = obj.createTestStep('IARMBUS_RegisterEventHandler');
                                        tdkTestObj.addParameter("owner_name","DUMMYMgr");
                                        tdkTestObj.addParameter("event_id",0);
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details=tdkTestObj.getResultDetails();
                                        #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Event Handler registered for Event-X";
                                                #calling IARMBUS API "IARM_Bus_RegisterEventHandler"
                                                tdkTestObj = obj.createTestStep('IARMBUS_RegisterEventHandler');
                                                tdkTestObj.addParameter("owner_name","DUMMYMgr");
                                                tdkTestObj.addParameter("event_id",1);
                                                expectedresult="SUCCESS"
                                                tdkTestObj.executeTestCase(expectedresult);
                                                actualresult = tdkTestObj.getResult();
                                                details=tdkTestObj.getResultDetails();
                                                #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                                                if expectedresult in actualresult:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print "SUCCESS: Event Handler registered for Event-Y";
                                                        #calling IARMBUS API "IARM_Bus_RegisterEventHandler"
                                                        tdkTestObj = obj.createTestStep('IARMBUS_RegisterEventHandler');
                                                        tdkTestObj.addParameter("owner_name","DUMMYMgr");
                                                        tdkTestObj.addParameter("event_id",2);
                                                        expectedresult="SUCCESS"
                                                        tdkTestObj.executeTestCase(expectedresult);
                                                        actualresult = tdkTestObj.getResult();
                                                        details=tdkTestObj.getResultDetails();
                                                        #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                                                        if expectedresult in actualresult:
                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                print "SUCCESS: Event Handler registered for Event-Z";
                                     
				        			#Syncing Second Application
                                                                tdkTestObj = obj.createTestStep('IARMBUS_SyncSecondApplication');
                                                                tdkTestObj.addParameter("lockenabled","false");
                                                                expectedresult="SUCCESS"
                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                actualresult = tdkTestObj.getResult();
                                                                #Check for SUCCESS/FAILURE for syncing second application
                                                                if expectedresult in actualresult:
                                                                       tdkTestObj.setResultStatus("SUCCESS");
                                                                       print "SUCCESS: Second application synced successfully";
                                                                else:
                                                                       tdkTestObj.setResultStatus("FAILURE");
                                                                       print "FAILURE: Failed to sync second application";
                                     
                                                                time.sleep(1.2);
                                                                tdkTestObj = obj.createTestStep('IARMBUS_GetLastReceivedEventDetails');
                                                                expectedresult="SUCCESS"
                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                actualresult = tdkTestObj.getResult();
                                                                details=tdkTestObj.getResultDetails();
                                                                #Check for SUCCESS/FAILURE return value of IARMBUS_GetLastReceivedEventDetails
                                                                if "SUCCESS" in expectedresult:
                                                                        print "SUCCESS: GetLastReceivedEventDetails executed Successfully"
                                                                        line = details;
                                                                        matchObj = re.match( r'(.*)X(.*)Y(.*)Z.*',line)
                                                                        if matchObj:
                                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                                print "SUCCESS: All events are received successfully in order";
                                                                        else:
                                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                                print "FAILURE: Events are not received in order";
                                                                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                                                                #deregistering event handler for event-X
                                                                                tdkTestObj.addParameter("owner_name","DUMMYMgr");
                                                                                tdkTestObj.addParameter("event_id",0);
                                                                                expectedresult="SUCCESS"
                                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                                actualresult = tdkTestObj.getResult();
                                                                                details=tdkTestObj.getResultDetails();
                                                                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                                                                if expectedresult in actualresult:
                                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                                        print "SUCCESS: UnRegister Event Handler for Event-X";
                                                                                else:
                                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                                        print "FAILURE : IARM_Bus_UnRegisterEventHanlder failed. %s " %details;
                                                                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                                                                #deregistering event handler for event-Y
                                                                                tdkTestObj.addParameter("owner_name","DUMMYMgr");
                                                                                tdkTestObj.addParameter("event_id",1);
                                                                                expectedresult="SUCCESS"
                                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                                actualresult = tdkTestObj.getResult();
                                                                                details=tdkTestObj.getResultDetails();
                                                                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                                                                if expectedresult in actualresult:
                                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                                        print "SUCCESS: UnRegister Event Handler for Event-Y";
                                                                                else:
                                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                                        print "FAILURE : IARM_Bus_UnRegisterEventHanlder failed. %s " %details;
                                                                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                                                                #deregistering event handler for event-Z
                                                                                tdkTestObj.addParameter("owner_name","DUMMYMgr");
                                                                                tdkTestObj.addParameter("event_id",2);
                                                                                expectedresult="SUCCESS"
                                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                                actualresult = tdkTestObj.getResult();
                                                                                details=tdkTestObj.getResultDetails();
                                                                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                                                                if expectedresult in actualresult:
                                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                                        print "SUCCESS: UnRegister Event Handler Event-Z";
                                                                                else:
                                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                                        print "FAILURE : IARM_Bus_UnRegisterEventHanlder failed. %s " %details;
                                                                                break;
                                                                else:
                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                        print "FAILURE: GetLastReceivedEventDetails failed and all the events are not received";
                                                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                                                #deregistering event handler for event-X
                                                                tdkTestObj.addParameter("owner_name","DUMMYMgr");
                                                                tdkTestObj.addParameter("event_id",0);
                                                                expectedresult="SUCCESS"
                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                actualresult = tdkTestObj.getResult();
                                                                details=tdkTestObj.getResultDetails();
                                                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                                                if expectedresult in actualresult:
                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                        print "SUCCESS: UnRegister Event Handler for Event-X";
                                                                else:
                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                        print "FAILURE : IARM_Bus_UnRegisterEventHanlder failed. %s " %details;
                                                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                                                #deregistering event handler for event-Y
                                                                tdkTestObj.addParameter("owner_name","DUMMYMgr");
                                                                tdkTestObj.addParameter("event_id",1);
                                                                expectedresult="SUCCESS"
                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                actualresult = tdkTestObj.getResult();
                                                                details=tdkTestObj.getResultDetails();
                                                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                                                if expectedresult in actualresult:
                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                        print "SUCCESS: UnRegister Event Handler for Event-Y";
                                                                else:
                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                        print "FAILURE : IARM_Bus_UnRegisterEventHanlder failed. %s " %details;
                                                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                                                #deregistering event handler for event-Z
                                                                tdkTestObj.addParameter("owner_name","DUMMYMgr");
                                                                tdkTestObj.addParameter("event_id",2);
                                                                expectedresult="SUCCESS"
                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                actualresult = tdkTestObj.getResult();
                                                                details=tdkTestObj.getResultDetails();
                                                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                                                if expectedresult in actualresult:
                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                        print "SUCCESS: UnRegister Event Handler Event-Z";
                                                                else:
                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                        print "FAILURE : IARM_Bus_UnRegisterEventHanlder failed. %s " %details;
                                                        else:
                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                print "FAILURE : IARM_Bus_RegisterEventHandler failed. %s " %details;
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "FAILURE : IARM_Bus_RegisterEventHandler failed. %s " %details;
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE : IARM_Bus_RegisterEventHandler failed. %s " %details;
				        	
				        	
				        time.sleep(2)
                                        #Syncing Second Application
                                        tdkTestObj = obj.createTestStep('IARMBUS_SyncSecondApplication');
                                        tdkTestObj.addParameter("lockenabled","false");
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        #Check for SUCCESS/FAILURE for syncing second application
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Second application synced successfully";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: Failed to sync second application";				
                                
                                else:
				        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Failed to invoke Second application"
					
                        # Calling IARM_Bus_DisConnect API
                        tdkTestObj = obj.createTestStep('IARMBUS_DisConnect');
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of IARMBUS_DisConnect
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS :Application successfully disconnected from IARMBus";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: IARM_Bus_Disconnect failed. %s " %details;                                        
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: IARM_Bus_Connect failed. %s" %details;
                #calling IARMBUS API "IARM_Bus_Term"
                tdkTestObj = obj.createTestStep('IARMBUS_Term');
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details=tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of IARMBUS_Term
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: IARM_Bus term success";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: IARM_Bus Term failed";                        
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: IARM_Bus_Init failed. %s " %details;
 
        print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Unload the iarmbus module
        obj.unloadModule("iarmbus");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
