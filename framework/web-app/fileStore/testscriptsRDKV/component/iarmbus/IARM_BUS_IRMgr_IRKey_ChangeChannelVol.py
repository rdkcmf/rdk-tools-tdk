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
  <id>1603</id>
  <version>2</version>
  <name>IARM_BUS_IRMgr_IRKey_ChangeChannelVol</name>
  <primitive_test_id>18</primitive_test_id>
  <primitive_test_name>IARMBUS_BroadcastEvent</primitive_test_name>
  <primitive_test_version>6</primitive_test_version>
  <status>FREE</status>
  <synopsis>Check if multiple IR event notification is received for repeated key press/release for keys: channel up, channel down, Volume Up, Volume Down.
Testcase ID: CT_IARMBUS_109</synopsis>
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
    <test_case_id>CT_IARMBUS_109</test_case_id>
    <test_objective>Check if multiple IR event notification is received for repeated key press/release for keys: channel up, channel down, Volume Up, Volume Down</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1/XI3-1</test_setup>
    <pre_requisite>“IARMDaemonMain” process should be running.</pre_requisite>
    <api_or_interface_used>IARM_Bus_Init(char *)
IARM_Bus_Connect()
IARM_Bus_BroadcastEvent(const char *, IARM_EventId_t , void *, size_t )
IARM_Bus_Disconnect()
IARM_Bus_Term()</api_or_interface_used>
    <input_parameters>IARM_Bus_Init : 
char * - (test agent process_name)
IARM_Bus_Connect : None
ARM_Bus_RegisterEventHandler :
const char * - IARM_BUS_IRMGR_NAME, IARM_EventId_t - IARM_BUS_IRMGR_EVENT_IRKEY, IARM_EventHandler_t - IR_event_callback
IARM_Bus_BroadcastEvent :
const char *- IARM_BUS_IRMGR_NAME, IARM_EventId_t - IARM_BUS_IRMGR_EVENT_IRKEY, 
Void *- eventData, size_t- sizeof(eventData) 
IARM_Bus_UnRegisterEventHandler :
const char* - IARM_BUS_IRMGR_NAME,
IARM_EventId_t - IARM_BUS_IRMGR_EVENT_IRKEY
IARM_Bus_Disconnect : None
IARM_Bus_Term : None</input_parameters>
    <automation_approch>1.TM loads the IARMBUS_Agent via the test agent
2.The IARMBUS_Agent initializes and registers with IARM Bus Daemon.
3.TM loads(initializes and registers) another application with IARM Daemon(second application) .
4.IARMBUS_Agent will register for “IARM_BUS_IRMGR_EVENT_IRKEY” event and waits on event.
5.IARMBUS_Agent will broadcast CHANNELUP/CHANNELDOWN/VOLUMEUP/VOLUMEDOWN key press and key release event 5 times to the bus.
6.IARMBUS_Agent should receive the event and event handler should handle the event(printing some log message) .
7.IARMBUS_Agent deregisters from the IARM Bus Daemon.
8.For each API called in the script, IARMBUS_Agent will send SUCCESS or FAILURE status to Test Agent by comparing the return vale of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.
Checkpoint 2. Check for the print message.</except_output>
    <priority>High</priority>
    <test_stub_interface>libiarmbusstub.so
1.TestMgr_IARMBUS_Init
2.TestMgr_IARMBUS_Term
3.TestMgr_IARMBUS_Connect
4.TestMgr_IARMBUS_Disconnect
5.TestMgr_IARMBUS_BroadcastEvent
6.TestMgr_IARMBUS_RegisterEventHandler
7.TestMgr_IARMBUS_UnRegisterEventHandler
8.TestMgr_IARMBUS_GetLastReceivedEventDetails</test_stub_interface>
    <test_script>IARM_BUS_IRMgr_IRKey_ChangeChannelVol</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'IARM_BUS_IRMgr_IRKey_ChangeChannelVol');
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
                        #set owner to IRMgr
                        ownerName="IRMgr"
                        # IR KEY Event
                        eventId=0
                        #passing parameter for receiving IRMgr events
                        tdkTestObj.addParameter("owner_name",ownerName);
                        tdkTestObj.addParameter("event_id",eventId);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS :Event Handler registered successfully";
                                #Broadcast IR Key event (CHANNELUP/CHANNELDOWN/VOLUMEUP/VOLUMEDOWN) from IR Mgr
                                for keyCode in range(0x00000088,0x0000008C):
                                    if keyCode == 0x00000088:
					keyCodeStr = "CHANNELUP"
                                    elif keyCode == 0x00000089:
					keyCodeStr = "CHANNELDOWN"
                                    elif keyCode == 0x0000008A:
					keyCodeStr = "VOLUMEUP"
                                    elif keyCode == 0x0000008B:
					keyCodeStr = "VOLUMEDOWN"
                                    # Repeat Key Press/Release for 6 times
                                    for x in range(0,6):
					print '\n******** Iteration %d **********' % x ;
					tdkTestObj = obj.createTestStep('IARMBUS_InvokeEventTransmitterApp',0);
                                        if (x % 2 == 0):
                                                # Key Press
                                                keyType=0x00008000
						keyTypeStr="PRESS"
                                        else:
                                                # Key Release
                                                keyType=0x00008100
						keyTypeStr="RELEASE"

                                        tdkTestObj.addParameter("owner_name",ownerName);
                                        tdkTestObj.addParameter("event_id",eventId);
					tdkTestObj.addParameter("evttxappname","gen_single_event");
                                        tdkTestObj.addParameter("keyCode",keyCode);
                                        tdkTestObj.addParameter("keyType",keyType);
                                        print "Broadcasting IR Key Event (%s:%x,%s:%x)"%(keyCodeStr,keyCode,keyTypeStr,keyType)
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        #checking for Broadcast event invocation status
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Broadcasting Key success";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: Broadcasting Key failed";

					#sleep for 1 sec to receive IR key event that is broadcasted from second app
					time.sleep(2);

                                        #Getting last received event details
                                        tdkTestObj = obj.createTestStep('IARMBUS_GetLastReceivedEventDetails');
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details=tdkTestObj.getResultDetails();
                                        print details
                                        #checking for event received status
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
						print "Successfully received broadcasted Event"
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
						print "Failed to receive broadcasted Event"
				    # End of for loop
				    print '\n********************************\n';
                                # End of for loop

                                #calling IARM_Bus_UnRegisterEventHandler API
                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                tdkTestObj.addParameter("owner_name",ownerName);
                                #Register for Broadcast event
                                tdkTestObj.addParameter("event_id",eventId);
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
