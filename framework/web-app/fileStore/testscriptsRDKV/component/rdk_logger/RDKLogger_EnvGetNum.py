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
  <id>550</id>
  <version>3</version>
  <name>RDKLogger_EnvGetNum</name>
  <primitive_test_id>409</primitive_test_id>
  <primitive_test_name>RDKLogger_EnvGetNum</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This tests the getting of number from module.
Test Case ID: CT_RDKLogger_05
Test Type: Positive</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_RDKLogger_05</test_case_id>
    <test_objective>To get the registered number of the specified environment variable</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1/XI3-1</test_setup>
    <pre_requisite>RDK debug manager module should be intialized</pre_requisite>
    <api_or_interface_used>rdk_logger_envGetNum()</api_or_interface_used>
    <input_parameters>rdk_logger_envGetNum:  
string – module (e.g., QAMSRC)</input_parameters>
    <automation_approch>1. TM loads RDKLoggerStub_agent via the test agent.  
2. TM will invoke “TestMgr_RDKLogger_EnvGetNum” in RDKLoggerStub_agent. 
3. RDKLoggerStub_agent will call rdk_logger_init() API of the component and get the result.  
4. On success of rdk_logger_init() API, RDKLoggerStub_agent will call rdk_logger_envGetNum() API of the component and get the result. 
5. Depending on the return value of API, RDKLoggerStub_Agent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1..Check for the registered number of the module returned by the API.
Checkpoint 2.Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>librdkloggerstub.so 
TestMgr_RDKLogger_EnvGetNum</test_stub_interface>
    <test_script>RDKLogger_EnvGetNum</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
  </script_tags>
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
obj.configureTestCase(ip,port,'RDKLogger_EnvGetNum');
#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "rdklogger module loading status :%s" %result;

#Check for SUCCESS/FAILURE of rdklogger module
if "SUCCESS" in result.upper():
    #Set the module loading status
    obj.setLoadModuleStatus("SUCCESS"); 

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('RDKLogger_EnvGetNum');

    expectedRes = "SUCCESS"
    module = "PXYSRVC"
    print "Requested module: %s"%module
    tdkTestObj.addParameter("module",module);
   
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedRes);

    #Get the result of execution
    result = tdkTestObj.getResult();
    print "[TEST EXECUTION RESULT] : %s" %result;
    details = tdkTestObj.getResultDetails();
    if "SUCCESS" in result.upper():
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        print "rdklogger env get number Successful: [%s]" %details;
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "rdklogger env get number Failed: [%s]"%details;

    #unloading rdklogger module
    obj.unloadModule("rdklogger");
else:
    print "Failed to load rdklogger module";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");
