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
  <id>89</id>
  <version>1</version>
  <name>IARMBUS Set Key Repeat Interval test</name>
  <primitive_test_id>8</primitive_test_id>
  <primitive_test_name>IARMBUS_BusCall</primitive_test_name>
  <primitive_test_version>8</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test script Sets the Key Repeat Interval of the STB to the desired value
Test Case ID : CT_IARMBUS_25</synopsis>
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
    <test_case_id>CT_IARMBUS_24</test_case_id>
    <test_objective>IARMBUS – Setting Key Repeat Interval time for STB .</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1 / XG1-1</test_setup>
    <pre_requisite>1. “IARMDaemonMain” Process should be running.

2. “irMgrMain” Process should be running.</pre_requisite>
    <api_or_interface_used>IARM_Bus_Init(char *) 
IARM_Bus_Connect()
IARM_Bus_Call(const char *,  const char *, void *, size_t )
IARM_Bus_Disconnect()
IARM_Bus_Term()</api_or_interface_used>
    <input_parameters>IARM_Bus_Init : 
char *  - (test agent process_name)
IARM_Bus_Connect : None
IARM_Bus_Call : 
const char * - IARM_BUS_IRMGR_NAME,
const char * - IARM_BUS_IRMGR_API_GetRepeatInterval,
void * - param, size_t -sizeof(param)
IARM_Bus_Call : 
const char* - IARM_BUS_IRMGR_NAME  
const char* - IARM_BUS_IRMGR_API_SetRepeatInterval
void * - param, size_t -sizeof(param)
IARM_Bus_Disconnect : None
IARM_Bus_Term : None</input_parameters>
    <automation_approch>1.TM loads the IARMBUS_Agent via the test agent.
2.The IARMBUS_Agent initializes and registers with IARM Bus Daemon .
3.IARMBUS_Agent will invoke the RPC for getting the key repeat interval time.  
4.IARMBUS_Agent will return the Key Repeat Interval to the Test Agent.
5.IARMBUS_Agent will set key repeat time.
6.IARMBUS_Agent will invoke the RPC for getting the key repeat interval time.
7.IARMBUS_Agent will return the Key Repeat Interval to the Test Agent.  
8.Test Agent will compare the Key Repeat Interval time before and after setting it.
9.IARMBUS_Agent deregisters from the IARM Bus Daemon.
10.For each API called in the script, IARMBUS_Agent will send SUCCESS or FAILURE status to Test Agent by comparing the return vale of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.

Checkpoint 2.Check the Key Repeat  interval before and after setting the value.</except_output>
    <priority>High</priority>
    <test_stub_interface>libiarmbusstub.so
1.TestMgr_IARMBUS_Init
2.TestMgr_IARMBUS_Term
3.TestMgr_IARMBUS_Connect
4.TestMgr_IARMBUS_Disconnect
5.TestMgr_IARMBUS_BusCall</test_stub_interface>
    <test_script>IARMBUS Set Key Repeat Interval test</test_script>
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
obj.configureTestCase(ip,port,'CT_IARMBUS_25');
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
                        #calling IARMBUS API "IARM_Bus_Call"
                        tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                        #passing prameter for querying key repeat interval time
                        tdkTestObj.addParameter("method_name","GetRepeatInterval");
                        tdkTestObj.addParameter("owner_name","IRMgr");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        print "Query- Key Repeat Interval: %s" %details;
                        #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Query- RPC method invoked for querying key repeat interval ";
                                #calling IARMBUS API "IARM_Bus_Call"
                                tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                #passing prameter for setting key repeat interval time
                                tdkTestObj.addParameter("method_name","SetRepeatInterval");
                                tdkTestObj.addParameter("owner_name","IRMgr");
                                #setting Repeat interval to 100
                                tdkTestObj.addParameter("set_timeout",100);
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
                                print "Set- Key Repeat Interval: %s" %details;
                                #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                                set_interval=details;
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Set- RPC method invoked for setting key repeat interval ";
                                        #calling IARMBUS API "IARM_Bus_Call"
                                        tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                        #passing prameter for querying key repeat interval time
                                        tdkTestObj.addParameter("method_name","GetRepeatInterval");
                                        tdkTestObj.addParameter("owner_name","IRMgr");
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        details=tdkTestObj.getResultDetails();
                                        print "Query- Key Repeat Interval: %s" %details;
                                        actualresult = tdkTestObj.getResult();
                                        get_interval=tdkTestObj.getResultDetails();
                                        #Check for both Repeat Interval before and after setting it
                                        if get_interval == set_interval:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Key Repeat Intervals are same";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: Both the Key Repeat Interval are not same";
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Query- RPC method invoked for setting key repeat interval ";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: GetRepeatInterval ---> IARM_Bus_Call failed. %s " %details;
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: SetRepeatInterval ---> IARM_Bus_Call failed. %s " %details;
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: GetRepeatInterval ---> IARM_Bus_Call failed. %s " %details;
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
                print "FAILURE: IARM_Bus_Init failed. %s" %details;

        print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Unload the iarmbus module
        obj.unloadModule("iarmbus");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
