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
  <id>1379</id>
  <version>1</version>
  <name>RDKLogger_Log_Trace7</name>
  <primitive_test_id>591</primitive_test_id>
  <primitive_test_name>RDKLogger_Log_Msg</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To log a TRACE7 level message.
Test Case ID: CT_RDKLogger_20
Test Type: Positive</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
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
    <test_case_id>CT_RDKLogger_20</test_case_id>
    <test_objective>To log a TRACE7 level message</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1/XI3-1</test_setup>
    <pre_requisite>1. RDK debug manager module should be intialized 
2. Module should have TRACE7 level configured in debug.ini file</pre_requisite>
    <api_or_interface_used>rdk_dbg_MsgRaw()</api_or_interface_used>
    <input_parameters>rdk_dbg_MsgRaw: 
string – level (e.g., TRACE7)
string – module (e.g., TEST)
string - message (e.g., "Test Trace7")</input_parameters>
    <automation_approch>1. TM loads RDKLoggerStub_agent via the test agent.
2. TM will invoke “TestMgr_RDKLogger_Log_Msg” in RDKLoggerStub_agent.
3. RDKLoggerStub_agent will call rdk_logger_init() API of the component and get the result.  
4. On success of rdk_logger_init() API, RDKLoggerStub_agent will call RDK_LOG() API of the component.
5. RDKLoggerStub_Agent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1..Check for the log message logged by the API.
Checkpoint 2.Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>librdkloggerstub.so 
TestMgr_RDKLogger_Log_Msg</test_stub_interface>
    <test_script>RDKLogger_Log_Trace7</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
from tdklib import TDKScriptingLibrary;

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = TDKScriptingLibrary("rdklogger","2.0");
obj.configureTestCase(ip,port,'RDKLogger_Log_Trace7');
#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "rdklogger module loading status :%s" %result;

#Check for SUCCESS/FAILURE of rdklogger module
if "SUCCESS" in result.upper():
    #Set the module loading status
    obj.setLoadModuleStatus("SUCCESS");

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('RDKLogger_Log_Msg');

    expectedRes = "SUCCESS"

    module = "TEST4"
    print "Requested module: %s"%module
    tdkTestObj.addParameter("module",module);
    level = "TRACE7"
    print "Requested level: %s"%level
    tdkTestObj.addParameter("level",level);
    msg = "Test Trace7 message"
    print "Requested message: %s"%msg
    tdkTestObj.addParameter("msg",msg);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedRes);

    #Get the result of execution
    result = tdkTestObj.getResult();
    print "[TEST EXECUTION RESULT] : %s" %result;
    details = tdkTestObj.getResultDetails();
    #Set the result status of execution
    if "SUCCESS" in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
        print "rdklogger logging Successful";
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "rdklogger logging Failed: [%s]"%details;

    #unloading rdklogger module
    obj.unloadModule("rdklogger");
else:
    print "Failed to load rdklogger module";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");
