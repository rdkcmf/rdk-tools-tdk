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
  <id>417</id>
  <version>6</version>
  <name>IARMBUS_DummyCall_Persistent_test</name>
  <primitive_test_id/>
  <primitive_test_name>IARMBUS_BusCall</primitive_test_name>
  <primitive_test_version>9</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test script tests the successful Dummy RPC calls for 'x' times
Test Case ID : CT_IARMBUS_41</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
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
    <test_case_id>CT_IARMBUS_40</test_case_id>
    <test_objective>IARMBUS – Creating and Calling Dummy RPC calls for 'x' times</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1 / XG1-1</test_setup>
    <pre_requisite>1. “IARMDaemonMain” Process should be running.</pre_requisite>
    <api_or_interface_used>IARM_Bus_Init(char *) 
IARM_Bus_Connect()
IARM_Bus_Call(const char *,  const char *, void *, size_t )
IARM_Bus_RegisterCall(const char *methodName, IARM_BusCall_t handler)
IARM_Bus_Disconnect()
IARM_Bus_Term()</api_or_interface_used>
    <input_parameters>IARM_Bus_Init : 
char *  - (test agent process_name)
IARM_Bus_Connect : None
IARM_Bus_Call : 
const char * - IARM_BUS_DUMMYMGR_NAME,
Const char * - IARM_BUS_DUMMYMGR_API_DummyAPI0
void * - param, size_t -sizeof(param)
IARM_Bus_Disconnect : None
IARM_Bus_Term : None</input_parameters>
    <automation_approch>1.TM loads the IARMBUS_Agent via the test agent.
2.The IARMBUS_Agent initializes and registers with IARM Bus Daemon(First Application). 
3.TM loads(initializes and registers) another application with IARM Daemon(second application which Registers the Dummy RPC calls) .
4.IARMBUS_Agent will invoke the Dummy RPC method .
5.IARMBUS_Agent deregisters from the IARM Bus Daemon.
6. Repeat steps 3-5 for 'x' times
7.For each API called in the script, IARMBUS_Agent will send SUCCESS or FAILURE status to Test Agent by comparing the return vale of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libiarmbusstub.so
1.TestMgr_IARMBUS_Init
2.TestMgr_IARMBUS_Term
3.TestMgr_IARMBUS_Connect
4.TestMgr_IARMBUS_Disconnect
5.TestMgr_IARMBUS_BusCall</test_stub_interface>
    <test_script>IARMBUS_DummyCall_Persistent_test</test_script>
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
sysUtilObj = tdklib.TDKScriptingLibrary("systemutil","1");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'Dummy');
sysUtilObj.configureTestCase(ip,port,'Dummy');
sysUtilLoadStatus = sysUtilObj.getLoadModuleResult();
loadmodulestatus =obj.getLoadModuleResult();
print "Iarmbus module loading status :  %s" %loadmodulestatus ;
print "System module loading status : %s" %sysUtilLoadStatus;
if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in sysUtilLoadStatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        sysUtilObj.setLoadModuleStatus("SUCCESS");
        #calling IARM_Bus_Init API
        tdkTestObj = obj.createTestStep('IARMBUS_Init');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details=tdkTestObj.getResultDetails();
        #Check for SUCCESS/FAILURE return value of IARMBUS_Init
        if ("SUCCESS" in actualresult):
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: Application successfully initialized with IARMBUS library";
                #calling IARM_Bus_Connect API
                tdkTestObj = obj.createTestStep('IARMBUS_Connect');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details=tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of IARMBUS_Connect IARMBUS_Connect
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: Application successfully connected with IARMBUS ";
                        i=0
                        for i in range(0,100):
                                print "**************** Iteration ", (i+1), " ****************";
                                tdkTestObj = sysUtilObj.createTestStep('SystemUtilAgent_ExecuteBinary');
                                tdkTestObj.addParameter("shell_script", "RunAppInBackground.sh");
                                tdkTestObj.addParameter("log_file", "BackgroundApp.txt");
                                #App name to be executed
                                tdkTestObj.addParameter("tool_path", "DUMMYMgr");
                                tdkTestObj.addParameter("timeout", "0");
                                #Execute the test case in STB
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                #Check for SUCCESS/FAILURE return value
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Second application Invoked successfully";

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

                                                #calling two dummy RPC using IARM_Bus_Call API
                                                tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                                tdkTestObj.addParameter("owner_name","DUMMYMgr");
                                                tdkTestObj.addParameter("method_name","DummyAPI0");
                                                api_0_Data=1;
                                                tdkTestObj.addParameter("testapp_API0_data",api_0_Data);
                                                expectedresult="SUCCESS"
                                                tdkTestObj.executeTestCase(expectedresult);
                                                actualresult = tdkTestObj.getResult();
                                                details=tdkTestObj.getResultDetails();
                                                print details;
                                                #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                                                if expectedresult in actualresult:
                                                        print "SUCCESS: Application invokes RPC-DummyAPI0 successfully";
                                                        dataCompare="%s" %(api_0_Data+10000000);
                                                        if dataCompare in details:
                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                print "SUCCESS: Both data are same";
                                                        else:
                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                print "FAILURE: Both data are not same";
                                                                break;
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "FAILURE: IARM_Bus_Call failed. %s" %details;

                                                tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                                tdkTestObj.addParameter("owner_name","DUMMYMgr");
                                                tdkTestObj.addParameter("method_name","DummyAPI1");
                                                api_1_Data=3;
                                                tdkTestObj.addParameter("testapp_API1_data",api_1_Data);
                                                expectedresult="SUCCESS"
                                                tdkTestObj.executeTestCase(expectedresult);
                                                actualresult = tdkTestObj.getResult();
                                                details=tdkTestObj.getResultDetails();
                                                print details;
                                                #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                                                if expectedresult in actualresult:
                                                        print "SUCCESS: Application invokes an RPC-DummyAPI1 successfully";
                                                        dataCompare="%s" %(api_1_Data+10000000);
                                                        if dataCompare in details:
                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                print "SUCCESS: Both data are same";
                                                        else:
                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                print "FAILURE: Both data are not same";
                                                                break;
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "FAILURE: IARM_Bus_Call failed. %s" %details;

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
                                                print "FAILURE: Failed to sync second application";

                                        time.sleep(1);
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Second application failed to execute";

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
        sysUtilObj.unloadModule("systemutil");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
        sysUtilObj.setLoadModuleStatus("FAILURE");
