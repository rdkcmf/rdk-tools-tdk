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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>NM_WifiMgr_networkMgrEvent_switchToPrivate</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>NetSrvMgrAgent_WifiMgr_BroadcastEvent</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective:To broadcast network manager switch to private event and check if netsrvmgr process receives it
Test CaseID:CT_NM_32
Test Type: Positive</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>1</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>IPClient-Wifi</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_NM_32</test_case_id>
    <test_objective>To broadcast network manager switch to private event and check if netsrvmgr process receives it</test_objective>
    <test_type>Positive</test_type>
    <test_setup>IPClient-Wifi</test_setup>
    <pre_requisite>1. netSrvMgr should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>IARM_Bus_Init (test agent process_name)
IARM_Bus_Connect()
IARM_Bus_BroadcastEvent(IARM_BUS_NM_SRV_MGR_NAME,IARM_BUS_NETWORK_MANAGER_EVENT_SWITCH_TO_PRIVATE,(void*)&amp;eventData,sizeof(eventData))
IARM_Bus_Disconnect()
IARM_Bus_Term</api_or_interface_used>
    <input_parameters>string owner
int event_id
string event_log
int value</input_parameters>
    <automation_approch>1. TM loads the IARMBUS_Agent via the test agent
2. IARMBUS_Agent initializes and registers with IARM Bus Daemon.
3. TM loads netsrvmgr_agent via the test agent. 
4. netsrvmgr_agent broadcast the event IARM_BUS_NETWORK_MANAGER_EVENT_SWITCH_TO_PRIVATE to netsrvmgr.
6. The stub will invokes the RPC method for checking if the event is registered and send the results.
7. The stub function will verify and sends the results as Json response 
8. TM will recieve and display the result.
9. IARMBUS_Agent deregisters from the IARM Bus Daemon.</automation_approch>
    <except_output>Checkpoint 1 stub will parse for event messages in netsrvmgr.log file.</except_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_NetSrvMgrAgent_WifiMgr_BroadcastEvent</test_stub_interface>
    <test_script>NM_WifiMgr_networkMgrEvent_switchToPrivate</test_script>
    <skipped>No</skipped>
    <release_version>M49</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
    <!--  -->
  </script_tags>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from iarmbus import IARMBUS_Init,IARMBUS_Connect,IARMBUS_DisConnect,IARMBUS_Term;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","2.0");
iarmObj.configureTestCase(ip,port,'NM_WifiMgr_networkMgrEvent_autoSwitchToPrivateEnabled');
#Get the result of connection with test component and STB
iarmLoadStatus = iarmObj.getLoadModuleResult();
print "Iarmbus module loading status : %s" %iarmLoadStatus ;
#Set the module loading status
iarmObj.setLoadModuleStatus(iarmLoadStatus);

if "SUCCESS" in iarmLoadStatus.upper():
        #Calling IARMBUS API "IARM_Bus_Init"
        result = IARMBUS_Init(iarmObj,"SUCCESS")
        #Check for SUCCESS/FAILURE return value of IARMBUS_Init
        if "SUCCESS" in result:
                #Calling IARMBUS API "IARM_Bus_Connect"
                result = IARMBUS_Connect(iarmObj,"SUCCESS")
                #Check for SUCCESS/FAILURE return value of IARMBUS_Connect
                if "SUCCESS" in result:
                        nmObj = tdklib.TDKScriptingLibrary("netsrvmgr","2.0");
                        nmObj.configureTestCase(ip,port,'NM_WifiMgr_networkMgrEvent_autoSwitchToPrivateEnabled');
                        #Get the result of connection with test component and STB
                        nmLoadStatus = nmObj.getLoadModuleResult();
                        print "NetSrvMgr module loading status : %s" %nmLoadStatus;
                        #Set the module loading status
                        nmObj.setLoadModuleStatus(nmLoadStatus);

                        if "SUCCESS" in nmLoadStatus.upper():
                                tdkTestObj = nmObj.createTestStep('NetSrvMgrAgent_WifiMgr_BroadcastEvent');
                                expectedresult="SUCCESS";
                                #Explicitly disable auto switch to private
                                tdkTestObj.addParameter("owner", "NET_SRV_MGR");
                                tdkTestObj.addParameter("event_id", 6);
                                tdkTestObj.addParameter("event_log","event handler value of bAutoSwitchToPrivateEnabled 0");
                                tdkTestObj.addParameter("value",0);
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details = tdkTestObj.getResultDetails();
                                #Check for SUCCESS return value of Testcase
                                if "SUCCESS" in actualresult.upper():
                                        #Configuring the test object for starting test execution
                                        tdkTestObj.addParameter("owner", "NET_SRV_MGR");
                                        tdkTestObj.addParameter("event_id", 4);
                                        tdkTestObj.addParameter("event_log","Service Manager msg Box Activated");
                                        tdkTestObj.addParameter("value",1);
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details = tdkTestObj.getResultDetails();
                                        #Check for SUCCESS return value of Testcase
                                        if "SUCCESS" in actualresult.upper():
                                              tdkTestObj.setResultStatus("SUCCESS");
                                	      print "Broadcasting Netwrok Manager Switch to Private Event Result : %s"%actualresult;
	                                      print "Details : %s"%details;
                                        else:
                                              tdkTestObj.addParameter("owner", "NET_SRV_MGR");
                                              tdkTestObj.addParameter("event_id", 4);
                                              tdkTestObj.addParameter("event_log","explicit call to switch to private");
                                              tdkTestObj.addParameter("value",1);
                                              tdkTestObj.executeTestCase(expectedresult);
                                              actualresult = tdkTestObj.getResult();
                                              details = tdkTestObj.getResultDetails();
                                              #Check for SUCCESS return value of Testcase
                                              if "SUCCESS" in actualresult.upper():
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                	            print "Broadcasting Netwrok Manager Switch to Private Event Result : %s"%actualresult;
	                                            print "Details : %s"%details; 
                                              else:
                                                    print "Broadcasting Event failed";
                                                    print "Details : %s"%details;
                                	            tdkTestObj.setResultStatus("FAILURE");
                                else: 
                                         print "Failed to Disable the auto switch to private";
                                         tdkTestObj.setResultStatus("FAILURE");   
                                #Unload netsrvmgr module
                                nmObj.unloadModule("netsrvmgr");
                        else:
                                print "Failed to Load netsrvmgr Module"
                        #Calling IARM_Bus_DisConnect API
                        result = IARMBUS_DisConnect(iarmObj,"SUCCESS")
                else:
                        print "IARMBUS Connect failed"
                #calling IARMBUS API "IARM_Bus_Term"
                result = IARMBUS_Term(iarmObj,"SUCCESS")
        else:
                print "IARMBUS Init failed"
        #Unload iarmbus module
        iarmObj.unloadModule("iarmbus");
else:
        print "Failed to Load iarmbus Module " 
