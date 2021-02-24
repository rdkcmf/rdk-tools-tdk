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
  <name>XUPNP_BcastTimezoneEvt</name>
  <primitive_test_id/>
  <primitive_test_name>XUPNP_BroadcastEvent</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To broadcast time zone event and check if xcal-device process receives it.
Testcase ID: CT_XUPNP_39</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>RPI-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_XUPNP_39</test_case_id>
    <test_objective>To broadcast time zone event and check if xcal-device process receives it.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>“IARMDaemonMain” and "sysMgrMain" process should be running.</pre_requisite>
    <api_or_interface_used>IARM_Bus_Init : 
char *  - (test agent process_name)
IARM_Bus_Connect : None
IARM_Bus_BroadcastEvent(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_EVENT_SYSTEMSTATE,(void*)&amp;eventData,sizeof(eventData))
IARM_Bus_Disconnect : None
IARM_Bus_Term : None</api_or_interface_used>
    <input_parameters>int stateId
int state=2
int error=0
string payload
string eventLog</input_parameters>
    <automation_approch>1. TM loads the IARMBUS_Agent via the test agent
2. IARMBUS_Agent initializes and registers with IARM Bus Daemon.
3. TM loads xupnp_agent via the test agent. 
4. xupnp_agent broadcast the event IARM_BUS_SYSMGR_EVENT_SYSTEMSTATE to sysMgr.
5. IARMBUS_Agent calls an RPC call(IARM_BUS_SYSMGR_API_GetSystemStates) to get the data passed using Broadcast Event
6. The stub will invokes the RPC method for checking the time zone event is registered and send the results.
7. The stub function will verify and sends the results as Json response 
8. TM will recieve and display the result.
9. IARMBUS_Agent deregisters from the IARM Bus Daemon.</automation_approch>
    <except_output>Checkpoint 1 stub will parse for event messages in xdevice.log file.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_XUPNP_BroadcastEvent</test_stub_interface>
    <test_script>XUPNP_BcastTimezoneEvt</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
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
iarmObj.configureTestCase(ip,port,'XUPNP_BcastTimezoneEvt');
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
                        xUpnpObj = tdklib.TDKScriptingLibrary("xupnp","2.0");
                        xUpnpObj.configureTestCase(ip,port,'XUPNP_BcastTimezoneEvt');
                        #Get the result of connection with test component and STB
                        xupnpLoadStatus = xUpnpObj.getLoadModuleResult();
                        print "XUPNP module loading status : %s" %xupnpLoadStatus;
                        #Set the module loading status
                        xUpnpObj.setLoadModuleStatus(xupnpLoadStatus);

                        if "SUCCESS" in xupnpLoadStatus.upper():
                                tdkTestObj = xUpnpObj.createTestStep('XUPNP_BroadcastEvent');
                                expectedresult="SUCCESS";
                                #Configuring the test object for starting test execution
                                tdkTestObj.addParameter("stateId",14);
                                tdkTestObj.addParameter("eventLog","Received timezone update");
                                tdkTestObj.addParameter("payload","EST0530");
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details = tdkTestObj.getResultDetails();
                                #Check for SUCCESS return value of Testcase
                                if "SUCCESS" in actualresult.upper():
                                        tdkTestObj.setResultStatus("SUCCESS");
                                	print "Broadcasting Timezone Event Result : %s"%actualresult;
	                                print "Details : %s"%details;
                                else:
                                        tdkTestObj.addParameter("stateId",14);
                                        tdkTestObj.addParameter("eventLog","Timezone is available");
                                        tdkTestObj.addParameter("payload","EST0530");
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details = tdkTestObj.getResultDetails();
                                        print "Broadcasting Timezone Event Result : %s"%actualresult;
                                        print "Details : %s"%details;
                                        if "SUCCESS" in actualresult.upper():
                                                tdkTestObj.setResultStatus("SUCCESS");
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                #Unload xupnp module
                                xUpnpObj.unloadModule("xupnp");

                        #Calling IARM_Bus_DisConnect API
                        result = IARMBUS_DisConnect(iarmObj,"SUCCESS")
                #calling IARMBUS API "IARM_Bus_Term"
                result = IARMBUS_Term(iarmObj,"SUCCESS")
        #Unload iarmbus module
        iarmObj.unloadModule("iarmbus");
        print "Rebooting the setup to revert the changes in output.json"
        iarmObj.initiateReboot();
        #Loading and unloading module to exit the test properly
        iarmObj = tdklib.TDKScriptingLibrary("iarmbus","2.0");
        iarmObj.configureTestCase(ip,port,'XUPNP_BcastTimezoneEvt');
        iarmObj.unloadModule("iarmbus");
