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
  <name>IARMBus_UnRegister_After_Remove_EventHandler_128</name>
  <primitive_test_id/>
  <primitive_test_name>IARMBUS_RemoveEventHandler</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>IARMBUS – IARM_Bus_UnRegisterEventHanlder() should fail after removing the event handler using IARM_Bus_RemoveEventHandler()</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
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
    <test_case_id>CT_IARMBUS_128</test_case_id>
    <test_objective>IARMBUS – IARM_Bus_UnRegisterEventHanlder() should fail after removing the event handler using IARM_Bus_RemoveEventHandler()</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XI3-1 / XG1-1</test_setup>
    <pre_requisite>“IARMDaemonMain” process should be running.</pre_requisite>
    <api_or_interface_used>IARM_Bus_Init(char *)
IARM_Bus_Connect()
IARM_Bus_RegisterEventHandler(const char* , IARM_EventId_t , IARM_EventHandler_t )
IARM_Bus_RemoveEventHandler(const char* , IARM_EventId_t , IARM_EventHandler_t )
IARM_Bus_UnRegisterEventHandler(const char*, IARM_EventId_t )
IARM_Bus_Disconnect()
IARM_Bus_Term()</api_or_interface_used>
    <input_parameters>IARM_Bus_Init : 
char *  - (test agent process_name)
IARM_Bus_Connect : None
IARM_Bus_RegisterEventHandler : 
const char * - IARM_BUS_DAEMONMGR , IARM_EventId_t - 0, IARM_EventHandler_t - eventhandler
IARM_Bus_RemoveEventHandler : 
const char * - IARM_BUS_DAEMONMGR , IARM_EventId_t - 0, IARM_EventHandler_t - eventhandler
IARM_Bus_UnRegisterEventHandler : 
const char* – IARM_BUS_DAEMONMGR , IARM_EventId_t – 0
IARM_Bus_Disconnect : None
IARM_Bus_Term : None</input_parameters>
    <automation_approch>1.TM loads the IARMBUS_Agent via the test agent
2.The IARMBUS_Agent initializes and registers with IARM Bus Daemon (First Application).
3.TM loads(initializes and registers) another application with IARM Daemon(second application which broadcasts the Dummy events) .
4.IARMBUS_Agent will register for “IARM_BUS_EVENT_RESOLUTIONCHANGE” event and waits on event using a  event handler.(should pass)
5.IARMBUS_Agent will unregister the event handler for “IARM_BUS_EVENT_RESOLUTIONCHANGE” event .
6.IARMBUS_Agent should not be able to remove a NULL event handler 
7.IARMBUS_Agent deregisters from the IARM Bus Daemon.
8.For each API called in the script, IARMBUS_Agent will send SUCCESS or FAILURE status to Test Agent by comparing the return vale of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.

Checkpoint 2. Check for  the print  message.</except_output>
    <priority>libiarmbusstub.so
1.TestMgr_IARMBUS_Init
2.TestMgr_IARMBUS_Term
3.TestMgr_IARMBUS_Connect
4.TestMgr_IARMBUS_Disconnect
5.TestMgr_IARMBUS_BroadcastEvent
6.TestMgr_IARMBUS_RegisterEventHandler
7.TestMgr_IARMBUS_UnRegisterEventHandler
8.TestMgr_IARMBUS_InvokeSecondApplication
9.TestMgr_IARMBUS_RemoveEventHandler</priority>
    <test_stub_interface>IARMBus_UnRegister_After_Remove_EventHandler_128.py</test_stub_interface>
    <test_script>IARMBus_UnRegister_After_Remove_EventHandler_128</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks>M35</remarks>
  </test_cases>
  <script_tags/>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
from tdklib import TDKScriptingLibrary;
from time import sleep;
#Test component to be tested
obj = TDKScriptingLibrary("iarmbus","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'IARMBus_UnRegister_After_Remove_EventHandler_128');
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
                print "SUCCESS :Application successfully initialized with IARMBUS library";
                #calling IARMBUS API "IARM_Bus_Connect"
                tdkTestObj = obj.createTestStep('IARMBUS_Connect');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details=tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of IARMBUS_Connect
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully connected with IARMBUS ";
                        #calling IARMBUS API "IARM_BusDaemon_RequestOwnership"
                        tdkTestObj = obj.createTestStep('IARMBUS_RequestResource');
                        tdkTestObj.addParameter("resource_type",1);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of IARMBUS_RequestResource
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS :Requested resource is allocated successfully for the application";
                                #calling IARMBUS API "IARM_Bus_RegisterEventHandler"
                                tdkTestObj = obj.createTestStep('IARMBUS_RegisterEventHandler');
                                #passing parameter for receving RESOURCE_AVAILABLE event
                                tdkTestObj.addParameter("owner_name","Daemon");
                                tdkTestObj.addParameter("event_id",0);
                                tdkTestObj.addParameter("evt_handler","evtHandler");
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS :Event Handler registered successfully";
                                        #Call second application to check for resource available event
                                        tdkTestObj = obj.createTestStep('IARMBUS_InvokeSecondApplication');
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS:InvokeSecondApplication success";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE:InvokeSecondApplication fails";

                                        #wait for 2 sec to receive event that is broadcasted from second app
                                        sleep(2);

                                        #Get last received event details
                                        tdkTestObj = obj.createTestStep('IARMBUS_GetLastReceivedEventDetails');
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details=tdkTestObj.getResultDetails();
                                        #checking for event receiving status
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print details;
                                                print "SUCCESS: Event is Received";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: Event is not Received";
                                        #calling IARMBUS API "IARM_Bus_RemoveEventHandler"
                                        tdkTestObj = obj.createTestStep('IARMBUS_RemoveEventHandler');
                                        tdkTestObj.addParameter("owner_name","Daemon");
                                        tdkTestObj.addParameter("event_id",0);
                                        tdkTestObj.addParameter("evt_handler","evtHandler");
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details=tdkTestObj.getResultDetails();
                                        #Check for SUCCESS/FAILURE return value of IARMBUS_RemoveEventHandler
                                        if expectedresult in actualresult:
                                                print "SUCCESS :Event Handler Removed successfully";
                                                #calling IARMBUS API "IARM_Bus_UnRegisterEventHandler"
                                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                                tdkTestObj.addParameter("owner_name","Daemon");
                                                tdkTestObj.addParameter("event_id",0);
                                                expectedresult="FAILURE"
                                                tdkTestObj.executeTestCase(expectedresult);
                                                actualresult = tdkTestObj.getResult();
                                                details=tdkTestObj.getResultDetails();
                                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                                if expectedresult in actualresult:
                                                    if "INVALID_PARAM" in details.upper():
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print "SUCCESS :UnRegister Event Handler failed %s" %details;
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "FAILURE: IARM_Bus_UnRegisterEventHandler failed with %s error" %details;                                                    
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "FAILURE: IARM_Bus_UnRegisterEventHandler Success. %s" %details;
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: IARM_Bus_RemoveEventHandler failed. %s" %details;

                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: IARM_Bus_RegisterEventHandler failed. %s" %details;
                                #calling IARMBUS API "IARM_BusDaemon_ReleaseOwnership"
                                tdkTestObj = obj.createTestStep('IARMBUS_ReleaseResource');
                                tdkTestObj.addParameter("resource_type",1);
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value of IARMBUS_ReleaseResource
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: IARM_BusDaemon_ReleaseOwnership success";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: IARM_BusDaemon_ReleaseOwnership failed. %s" %details;

                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: IARM_BusDaemon_RequestOwnership failed %s" %details;

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
