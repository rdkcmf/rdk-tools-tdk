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
  <version>1</version>
  <name>IARMBus_Verify_after_UnRegister_Multiple_EventHandler_124</name>
  <primitive_test_id/>
  <primitive_test_name>IARMBUSPERF_UnRegisterEventHandler</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>IARMBUS-After IARM_Bus_UnRegisterEventHandler() all registered event handlers for the given event are removed, and the handlers are not invoked.</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_IARMBUS_124</test_case_id>
    <test_objective>IARMBUS-After IARM_Bus_UnRegisterEventHandler() all registered event handlers for the given event are removed, and the handlers are not invoked.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>All</test_setup>
    <pre_requisite>“IARMDaemonMain” process should be running.</pre_requisite>
    <api_or_interface_used>IARM_Bus_Init(char *)
IARM_Bus_Connect()
IARM_Bus_BroadcastEvent(const char *, IARM_EventId_t , void *, size_t )
IARM_Bus_Disconnect()
IARM_Bus_Term()</api_or_interface_used>
    <input_parameters>IARM_Bus_Init : 
char *  - (test agent process_name)
IARM_Bus_Connect : None
IARM_Bus_IsConnected : 
Char - *memberName, int * - isRegistered
IARMBUS_GetLastReceivedEventPerformanceDetails: Average of response time.
IARM_Bus_Disconnect : None
IARM_Bus_Term : None</input_parameters>
    <automation_approch>1.TM loads the IARMBUS_Agent via the test agent.
2.The IARMBUS_Agent initializes and registers with IARM Bus Daemon. 
3.IARMBUS_Agent checks for Registration of process with IARMDaemon Manager. 
4.IARMBUS_Agent will register for “IARM_BUS_IREVENT” event and waits on event using a  event handler
5.IARMBUS_Agent will register for “IARM_BUS_IREVENT” event and waits on event using another event handler
6.IARMBUS_Agent will register for “IARM_BUS_IREVENT” event and waits on event using another event handler
7. Broadcast the event from another application and check whether all the event handlers are called
8. IARMBUS_Agent unregisters all event handler
9.Broadcast the event from another application and check whether all the event handlers are not called
10.IARMBUS_Agent deregisters from the IARM Bus Daemon.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API.
Checkpoint 2. Check for the print message.</except_output>
    <priority>libiarmbusstub.so
1.TestMgr_IARMBUS_Init
2.TestMgr_IARMBUS_Term
3.TestMgr_IARMBUS_Connect
4.TestMgr_IARMBUS_Disconnect
5.TestMgr_IARMBUS_BroadcastEvent
6.TestMgr_IARMBUS_RegisterEventHandler
7.TestMgr_IARMBUS_UnRegisterEventHandler
8.TestMgr_IARMBUS_GetLastReceivedEventPerformanceDetails
9.TestMgr_IARMBUS_RegisterMultipleEventHandler</priority>
    <test_stub_interface>IARMBus_Verify_after_UnRegister_Multiple_EventHandler_124.py</test_stub_interface>
    <test_script>IARMBus_Verify_after_UnRegister_Multiple_EventHandler_124</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks>M23</remarks>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import time;
#from resetAgent import resetAgent;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'IARMBus_Verify_after_UnRegister_Multiple_EventHandler_124');

loadmodulestatus =obj.getLoadModuleResult();
print "Iarmbus module loading status :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS"); 

	#Prmitive test case which associated to this Script
	tdkTestObj = obj.createTestStep('IARMBUS_Init');
        #tdkTestObj.addParameter("Process_name","Bus Client");
        expectedresult="SUCCESS/FAILURE"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details=tdkTestObj.getResultDetails();
        #Check for SUCCESS/FAILURE return value of IARMBUS_Init
        if ("SUCCESS" in actualresult or ("FAILURE" in actualresult and "INVALID_PARAM" in details)):
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
	
			#Prmitive test case which associated to this Script
			tdkTestObj = obj.createTestStep('IARMBUS_RegisterMultipleEventHandlers');
			#registering event handler for IR Key events
			tdkTestObj.addParameter("owner_name","IRMgr");
			tdkTestObj.addParameter("event_id",0);
			expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Event Handler registered for IR key events";
                                #sleep for 3 sec to receive IR key event that is broadcasted from second app.
                                #time.sleep(3);
				#Prmitive test case which associated to this Script
				tdkTestObj = obj.createTestStep('IARMBUS_InvokeEventTransmitterApp');
				#registering event handler for IR Key events
				tdkTestObj.addParameter("owner_name","IRMgr");
				tdkTestObj.addParameter("event_id",0);
				tdkTestObj.addParameter("evttxappname","gen_single_event");
				tdkTestObj.addParameter("keyType",32768);
				tdkTestObj.addParameter("keyCode",301);
				expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                #details=tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Second application Invoked successfully";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Second application failed to execute";
                                time.sleep(2);
				#Prmitive test case which associated to this Script
				tdkTestObj = obj.createTestStep('IARMBUS_GetLastReceivedEventPerformanceDetails');
				expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
                                print details;
                                #Check for SUCCESS/FAILURE return value of IARMBUS_GetLastReceivedEventDetails
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: GetLastReceivedEventDetails executed successfully";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: GetLastReceivedEventDetails failed";
	
				tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
				#Transmit IR Key events
				tdkTestObj.addParameter("owner_name","IRMgr");
				tdkTestObj.addParameter("event_id",0);
				expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: UnRegister Event Handler for IR key events";

                                        #Prmitive test case which associated to this Script
                                        tdkTestObj = obj.createTestStep('IARMBUS_InvokeEventTransmitterApp');
                                        #registering event handler for IR Key events
                                        tdkTestObj.addParameter("owner_name","IRMgr");
                                        tdkTestObj.addParameter("event_id",0);
                                        tdkTestObj.addParameter("evttxappname","gen_single_event");
                                        tdkTestObj.addParameter("keyType",32768);
                                        tdkTestObj.addParameter("keyCode",301);
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        #details=tdkTestObj.getResultDetails();
                                        #Check for SUCCESS/FAILURE return value
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Second application Invoked successfully";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: Second application failed to execute";
                                        time.sleep(2);
                                        #Prmitive test case which associated to this Script
                                        tdkTestObj = obj.createTestStep('IARMBUS_GetLastReceivedEventPerformanceDetails');
                                        expectedresult="FAILURE"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details=tdkTestObj.getResultDetails();
                                        print details;
                                        #Check for SUCCESS/FAILURE return value of IARMBUS_GetLastReceivedEventDetails
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: GetLastReceivedEventDetails failed";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: GetLastReceivedEventDetails executed successfully";

                                        
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE : IARM_Bus_UnRegisterEventHanlder failed. %s " %details;
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE : IARM_Bus_RegisterEventHandler failed. %s " %details;
                        #calling IARMBUS API "IARM_Bus_DisConnect"
                        tdkTestObj = obj.createTestStep('IARMBUS_DisConnect');
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of IARMBUS_DisConnect
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Application successfully disconnected from IARMBus";
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
        
	obj.unloadModule("iarmbus");
	#resetAgent(ip,8090,"true");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
