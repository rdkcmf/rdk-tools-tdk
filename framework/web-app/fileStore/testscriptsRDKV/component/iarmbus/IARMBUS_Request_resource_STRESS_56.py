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
  <id>946</id>
  <version>1</version>
  <name>IARMBUS_Request_resource_STRESS_56</name>
  <primitive_test_id>11</primitive_test_id>
  <primitive_test_name>IARMBUS_RequestResource</primitive_test_name>
  <primitive_test_version>3</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test script tests Request multiple alternate resources for multiple times with every 100 milli seconds gap.				
TEST CASE ID:CT_IARMBUS_56</synopsis>
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
    <test_case_id>CT_IARMBUS_56</test_case_id>
    <test_objective>IARMBUS -Request multiple alternate resources for multiple times with every 100 mill seconds gap.</test_objective>
    <test_type>Stress</test_type>
    <test_setup>XI3-1 / XG1-1</test_setup>
    <pre_requisite>“IARMDaemonMain” process should be running.</pre_requisite>
    <api_or_interface_used>IARM_Bus_Init(char *)
IARM_Bus_Connect()
IARM_BusDaemon_RequestOwnership(IARM_Bus_ResrcType_t )
IARM_BusDaemon_ReleaseOwnership(IARM_Bus_ResrcType_t )
IARM_Bus_Disconnect()
IARM_Bus_Term()</api_or_interface_used>
    <input_parameters>IARM_Bus_Init : 
char *  - (test agent process_name)
IARM_Bus_Connect : None
IARM_BusDaemon_RequestOwnership : IARM_Bus_ResrcType_t – IARM_BUS_RESOURCE_MAX
IARM_BusDaemon_ReleaseOwnership : IARM_Bus_ResrcType_t - IARM_BUS_RESOURCE_DECODER_1
IARM_Bus_Disconnect : None
IARM_Bus_Term : None</input_parameters>
    <automation_approch>1.TM loads the IARMBUS_Agent via the test agent
2.The IARMBUS_Agent initializes and registers with IARM Bus Daemon . 
3.IARMBUS_Agent will request for resource IARM_BUS_RESOURCE_DECODER_1.
4.IARMBUS_Agent will release resource IARM_BUS_RESOURCE_DECODER_1.
5.IARMBUS_Agent deregisters from the IARM Bus Daemon.
6.For each API called in the script, IARMBUS_Agent will send SUCCESS or FAILURE status to Test Agent by comparing the return vale of APIs.
7. Above 3 to 4 steps will be repeated for n number times and the result will be passed to TM</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>libiarmbusstub.so
1.TestMgr_IARMBUS_Init
2.TestMgr_IARMBUS_Term
3.TestMgr_IARMBUS_Connect
4.TestMgr_IARMBUS_Disconnect
5.TestMgr_IARMBUS_RequestResource
6.TestMgr_IARMBUS_ReleaseResource</test_stub_interface>
    <test_script>IARMBUS_Request_resource_STRESS_56</test_script>
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
obj.configureTestCase(ip,port,'CT_IARMBUS_56');
loadmodulestatus =obj.getLoadModuleResult();
print "Iarmbus module loading status  :  %s" %loadmodulestatus ;
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
                        print "SUCCESS: Application successfully connected with IARMBUS ";
                        i = 0;
                        for i in range(0,10):
                            print "****************%d" %i;
                            #calling IARMBUS API "IARM_BusDaemon_RequestOwnership"
                            tdkTestObj = obj.createTestStep('IARMBUS_RequestResource');
                            # Requesting decoder 0 resource
                            tdkTestObj.addParameter("resource_type",1);
                            expectedresult="SUCCESS"
                            tdkTestObj.executeTestCase(expectedresult);
                            actualresult = tdkTestObj.getResult();
                            details=tdkTestObj.getResultDetails();
                            #Check for SUCCESS/FAILURE return value of IARMBUS_RequestResource
                            if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Requested resource is allocated successfully for the application";
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
                                        print "SUCCESS: Allocated resource is successfully released";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: IARM_BusDaemon_ReleaseOwnership failed. %s" %details;

                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: IARM_BusDaemon_RequestOwnership failed. %s" %details;
                            time.sleep(10/1000);
                            #calling IARMBUS API "IARM_BusDaemon_RequestOwnership"
                            tdkTestObj = obj.createTestStep('IARMBUS_RequestResource');
                            #Requesting decoder 0 resource
                            tdkTestObj.addParameter("resource_type",2);
                            expectedresult="SUCCESS"
                            tdkTestObj.executeTestCase(expectedresult);
                            actualresult = tdkTestObj.getResult();
                            details=tdkTestObj.getResultDetails();
                            #Check for SUCCESS/FAILURE return value of IARMBUS_RequestResource
                            if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Requested resource is allocated successfully for the application";
                                #calling IARMBUS API "IARM_BusDaemon_ReleaseOwnership"
                                tdkTestObj = obj.createTestStep('IARMBUS_ReleaseResource');
                                tdkTestObj.addParameter("resource_type",2);
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value 
                                if expectedresult in actualresult:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print "SUCCESS: Allocated  resource is successfully released";
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "FAILURE: IARM_BusDaemon_ReleaseOwnership failed. %s" %details;

                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: IARM_BusDaemon_RequestOwnership failed. %s" %details;

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
