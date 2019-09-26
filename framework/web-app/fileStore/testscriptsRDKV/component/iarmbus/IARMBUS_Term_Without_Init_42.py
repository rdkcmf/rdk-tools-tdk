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
  <id>809</id>
  <version>2</version>
  <name>IARMBUS_Term_Without_Init_42</name>
  <primitive_test_id>5</primitive_test_id>
  <primitive_test_name>IARMBUS_Term</primitive_test_name>
  <primitive_test_version>0</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test script will check Terminating an application with IARMBUS without Initializing				
TEST CASE ID:CT_IARMBUS_42</synopsis>
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
    <test_case_id>CT_IARMBUS_42</test_case_id>
    <test_objective>IARMBUS – Terminating an application with IARMBUS without Initializing</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XI3-1 / XG1-1</test_setup>
    <pre_requisite>“IARMDaemonMain” process should be running.</pre_requisite>
    <api_or_interface_used>IARM_Bus_Term()</api_or_interface_used>
    <input_parameters>IARM_Bus_Term : None</input_parameters>
    <automation_approch>1.TM loads the IARMBUS_Agent via the test agent.
2.The IARMBUS_Agent initializes and registers with IARM Bus Daemon . 
3.IARMBUS_Agent deregisters from the IARM Bus Daemon.
4.For each API called in the script, IARMBUS_Agent will send SUCCESS or FAILURE status to Test Agent by comparing the return vale of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for failure status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libiarmbusstub.so

1.TestMgr_IARMBUS_Term</test_stub_interface>
    <test_script>IARMBUS_Term_Without_Init_42</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");
# Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_IARMBUS_42');
loadmodulestatus =obj.getLoadModuleResult();
print "Iarmbus module loading status  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        #calling IARMBUS API "IARM_Bus_Term"
        tdkTestObj = obj.createTestStep('IARMBUS_Term');
        
        expectedresult="FAILURE";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details=tdkTestObj.getResultDetails();
        #Check for SUCCESS/FAILURE return value of IARMBUS_Term
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: Cannot Terminate Iarm bus without Init";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: IARM_Bus Term success without Init";

        obj.unloadModule("iarmbus");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
