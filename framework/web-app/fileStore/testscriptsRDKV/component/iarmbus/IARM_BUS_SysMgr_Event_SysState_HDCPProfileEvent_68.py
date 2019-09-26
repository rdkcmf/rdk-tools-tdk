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
  <id>1414</id>
  <version>2</version>
  <name>IARM_BUS_SysMgr_Event_SysState_HDCPProfileEvent_68</name>
  <primitive_test_id>8</primitive_test_id>
  <primitive_test_name>IARMBUS_BusCall</primitive_test_name>
  <primitive_test_version>8</primitive_test_version>
  <status>FREE</status>
  <synopsis>IARMBUS –Receiving event IARM_BUS_SYSMGR_EVENT_HDCP_PROFILE_UPDATE upon changing the HDCP profile 
Test case Id - CT_IARMBUS_68</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_IARMBUS_68</test_case_id>
    <test_objective>IARMBUS –Receiving event IARM_BUS_SYSMGR_EVENT_HDCP_PROFILE_UPDATE upon changing the HDCP profile</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1 / XG1-1</test_setup>
    <pre_requisite>“IARMDaemonMain” and "sysMgrMain" process should be running.</pre_requisite>
    <api_or_interface_used>IARM_Bus_Init(char *)
IARM_Bus_Connect()
IARM_Bus_RegisterEventHandler(const char* , IARM_EventId_t , IARM_EventHandler_t )
IARM_Bus_Call(const char *,  const char *, void *, size_t )
IARM_Bus_UnRegisterEventHandler(const char*, IARM_EventId_t )
IARM_Bus_Disconnect()
IARM_Bus_Term()</api_or_interface_used>
    <input_parameters>IARM_Bus_Init : 
char *  - (test agent process_name)
IARM_Bus_Connect : None
IARM_Bus_RegisterEventHandler : 
const char * - IARM_BUS_SYSMGR_NAME , IARM_EventId_t - IARM_BUS_SYSMGR_EVENT_HDCP_PROFILE_UPDATE, IARM_EventHandler_t - _evthandler 
IARM_Bus_Call : const char * - IARM_BUS_SYSMGR_NAME, const char * - IARM_BUS_SYSMGR_API_GetHDCPProfile
(&amp;IARM_BUS_SYSMGR_API_SetHDCPProfile) void * - param, size_t -sizeof(param)
IARM_Bus_UnRegisterEventHandler : 
const char* – IARM_BUS_SYSMGR_NAME , IARM_EventId_t – IARM_BUS_SYSMGR_EVENT_HDCP_PROFILE_UPDATE
IARM_Bus_Disconnect : None
IARM_Bus_Term : None</input_parameters>
    <automation_approch>1.TM loads the IARMBUS_Agent via the test agent
2.The IARMBUS_Agent initializes and registers with IARM Bus Daemon (First Application).
3..IARMBUS_Agent will register for “IARM_BUS_SYSMGR_EVENT_HDCP_PROFILE_UPDATE” event and waits on event.
4.IARMBUS_Agent calls an RPC call(IARM_BUS_SYSMGR_API_GetHDCPProfile), to get the HDCP profile value.
5.Get the HDCP profile value and set it to the other HDCP profile value using IARM_BUS_SYSMGR_API_SetHDCPProfile.
6.IARMBUS_Agent should check the last received event for IARM_BUS_SYSMGR_EVENT_HDCP_PROFILE_UPDATE.
7.IARMBUS_Agent deregisters from the IARM Bus Daemon.
8.For each API called in the script, IARMBUS_Agent will send SUCCESS or FAILURE status to Test Agent by comparing the return vale of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.

Checkpoint 2. Check for the last received event for HDCP profile update event.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>libiarmbusstub.so
1.TestMgr_IARMBUS_Init
2.TestMgr_IARMBUS_Term
3.TestMgr_IARMBUS_Connect
4.TestMgr_IARMBUS_Disconnect
5.TestMgr_IARMBUS_Bus Call
6.TestMgr_IARMBUS_RegisterEventHandler
7.TestMgr_IARMBUS_UnRegisterEventHandler
8.TestMgr_IARMBUS_GetLastReceivedEventDetails</test_stub_interface>
    <test_script>IARM_BUS_SysMgr_Event_SysState_HDCPProfileEvent_68</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_IARMBUS_68');
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
                        print "Application is successfully connected with IARM-BUS Daemon";                        
                        #calling IARMBUS API "IARM_Bus_RegisterEventHandler"
                        tdkTestObj = obj.createTestStep('IARMBUS_RegisterEventHandler');
                        #passing parameter for receving POWER_MODE_CHANGEDevent
                        tdkTestObj.addParameter("owner_name","SYSMgr");
                        tdkTestObj.addParameter("event_id",5);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS :SYSMgr Event Handler registered successfully";
                                #calling IARMBUS API "IARM_Bus_Call"
                                tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                #passing parameter for querying STB HDCP profile state
                                tdkTestObj.addParameter("method_name","GetHDCPProfile");
                                tdkTestObj.addParameter("owner_name","SYSMgr");
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
                                print "current HDCP profile state: %s" %details;
                                curstate=details;
                                #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Querying STB HDCP profile state -RPC method invoked successfully";
                                        #Setting the HDCP profile state
                                        tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                        tdkTestObj.addParameter("method_name","SetHDCPProfile");
                                        tdkTestObj.addParameter("owner_name","SYSMgr");
                                        # setting state to 1
                                        if curstate == "1" :
                                                #change to 0
                                                tdkTestObj.addParameter("newState",0);
                                        else :
                                                #change to 1
                                                tdkTestObj.addParameter("newState",1);
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details=tdkTestObj.getResultDetails();
                                        print "set HDCP profile state: %s" %details;
                                        #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Setting STB HDCP_profile state -RPC method invoked successfully";
                                                tdkTestObj = obj.createTestStep('IARMBUS_GetLastReceivedEventDetails');
                                                expectedresult="SUCCESS"
                                                tdkTestObj.executeTestCase(expectedresult);
                                                actualresult = tdkTestObj.getResult();
                                                details=tdkTestObj.getResultDetails();
                                                #checking for event received status
                                                if expectedresult in actualresult:
                                                        print details;
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print "SUCCESS: Event Received";
                                                else:
                                                        print details;
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "FAILURE: Event is not received";
                                                #calling IARMBUS API "IARM_Bus_UnRegisterEventHandler"
                                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                                tdkTestObj.addParameter("owner_name","SYSMgr");
                                                tdkTestObj.addParameter("event_id",5);
                                                expectedresult="SUCCESS"
                                                tdkTestObj.executeTestCase(expectedresult);
                                                actualresult = tdkTestObj.getResult();
                                                details=tdkTestObj.getResultDetails();
                                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                                if expectedresult in actualresult:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print "SUCCESS :Event Handler unregistered successfully";
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "unregister event handler failed. %s" %details;
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: Set STB HDCP_profile state - IARM_Bus_Call failed. %s " %details;
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Querying STB HDCP_profile state - IARM_Bus_Call failed. %s " %details;
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Register Event Handler failed. %s " %details;
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
