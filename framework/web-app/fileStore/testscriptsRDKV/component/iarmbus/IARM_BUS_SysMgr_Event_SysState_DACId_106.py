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
  <id>1409</id>
  <version>1</version>
  <name>IARM_BUS_SysMgr_Event_SysState_DACId_106</name>
  <primitive_test_id>18</primitive_test_id>
  <primitive_test_name>IARMBUS_BroadcastEvent</primitive_test_name>
  <primitive_test_version>6</primitive_test_version>
  <status>FREE</status>
  <synopsis>IARMBUS – Broadcasting and Receiving “IARM_BUS_SYSMGR_EVENT_SYSTEMSTATE” event and setting data for IARM_BUS_SYSMGR_SYSSTATE_DAC_ID and getting back using IARM_BUS_SYSMGR_API_GetSystemStates RPC call.
Test case Id - CT_IARMBUS_106</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_IARMBUS_106</test_case_id>
    <test_objective>IARMBUS – Broadcasting and Receiving “IARM_BUS_SYSMGR_EVENT_SYSTEMSTATE” event and setting data for IARM_BUS_SYSMGR_SYSSTATE_DAC_ID and getting back using IARM_BUS_SYSMGR_API_GetSystemStates RPC call.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1 / XG1-1</test_setup>
    <pre_requisite>“IARMDaemonMain” and "sysMgrMain" process should be running.</pre_requisite>
    <api_or_interface_used>IARM_Bus_Init(char *)
IARM_Bus_Connect()
IARM_Bus_BroadcastEvent(const char *, IARM_EventId_t , void *, size_t )
IARM_Bus_Call(const char *,  const char *, void *, size_t )
IARM_Bus_Disconnect()
IARM_Bus_Term()</api_or_interface_used>
    <input_parameters>IARM_Bus_Init : 
char *  - (test agent process_name)
IARM_Bus_Connect : None
IARM_Bus_BroadcastEvent :
Const char* - IARM_BUS_SYSMGR_NAME,
IARM_EventId_t – IARM_BUS_SYSMGR_EVENT_SYSTEMSTATE ,
Void * - eventdata(IARM_BUS_SYSMGR_SYSSTATE_DAC_ID), size_t – sizeof (eventdata)
IARM_Bus_Call : const char * - IARM_BUS_SYSMGR_NAME, const char * - IARM_BUS_SYSMGR_API_GetSystemStates
void * - param, size_t -sizeof(param)
IARM_Bus_Disconnect : None
IARM_Bus_Term : None</input_parameters>
    <automation_approch>1.TM loads the IARMBUS_Agent via the test agent
2.The IARMBUS_Agent initializes and registers with IARM Bus Daemon (First Application).
3.IARMBUS_Agent broadcast the event IARM_BUS_SYSMGR_EVENT_SYSTEMSTATE to the bus and sysmgr sets the data sent.
5.IARMBUS_Agent calls an RPC call(IARM_BUS_SYSMGR_API_GetSystemStates), to get the data passed using Broadcast Event
6.IARMBUS_Agent deregisters from the IARM Bus Daemon.
7.For each API called in the script, IARMBUS_Agent will send SUCCESS or FAILURE status to Test Agent by comparing the return vale of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.

Checkpoint 2. Check for the data set from the RPC call with the data passed through Broadcast Event</except_output>
    <priority>Medium</priority>
    <test_stub_interface>libiarmbusstub.so
1.TestMgr_IARMBUS_Init
2.TestMgr_IARMBUS_Term
3.TestMgr_IARMBUS_Connect
4.TestMgr_IARMBUS_Disconnect
5.TestMgr_IARMBUS_BroadcastEvent
6.TestMgr_IARMBUS_BusCall</test_stub_interface>
    <test_script>IARM_BUS_SysMgr_Event_SysState_DACId_106</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
from tdklib import TDKScriptingLibrary;
import time;
#Test component to be tested
obj = TDKScriptingLibrary("iarmbus","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_IARMBUS_106');
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
                        #calling IARMBUS API "IARM_Bus_RegisterEventHandler"
                        tdkTestObj = obj.createTestStep('IARMBUS_RegisterEventHandler');
                        #passing parameter for receiving SYSMgr event sys state DAC ID
                        tdkTestObj.addParameter("owner_name","SYSMgr");
                        tdkTestObj.addParameter("event_id",0);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS :Event Handler registered successfully";
                                #invoking application to broadcast event
                                tdkTestObj = obj.createTestStep('IARMBUS_BroadcastEvent');
                                tdkTestObj.addParameter("owner_name","SYSMgr");
                                tdkTestObj.addParameter("event_id",0);
                                tdkTestObj.addParameter("newState",31);
                                setstate=11;
                                seterror=22;
                                setpayload="DAC ID";
                                tdkTestObj.addParameter("state",setstate);
                                tdkTestObj.addParameter("error",seterror);
                                tdkTestObj.addParameter("payload",setpayload);

                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
				print "set state:%d "%setstate, "error:%d "%seterror, "payload:%s "%setpayload;
                                actualresult = tdkTestObj.getResult();
                                #checking for Broadcast event invokation status
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS:Broadcast event success";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE:Broadcast event fails";

				#Wait for SystemStates values to change
                                time.sleep(2);

                                #calling IARMBUS API "IARM_Bus_Call"
                                tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                tdkTestObj.addParameter("owner_name","SYSMgr");
                                tdkTestObj.addParameter("method_name","GetSystemStates");
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
				print details;
                                #checking for event received status
                                if expectedresult in actualresult:
                                        if str(setstate) in details and str(seterror) in details and str(setpayload) in details:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: RPC method invoked and DAC ID value for state, error and payload properly set";
                                        else :
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: RPC method invoked and DAC ID value for state and error has not been set";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: IARMBUS call failed";
                                #calling IARM_Bus_UnRegisterEventHandler API
                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                tdkTestObj.addParameter("owner_name","SYSMgr");
                                #Register for Broadcast event
                                tdkTestObj.addParameter("event_id",0);
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS:UnRegister Event Handler registered successfully";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: IARM_Bus_UnRegisterEventHandler failed %s" %details;
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: IARM_Bus_RegisterEventHandler %s" %details;
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
