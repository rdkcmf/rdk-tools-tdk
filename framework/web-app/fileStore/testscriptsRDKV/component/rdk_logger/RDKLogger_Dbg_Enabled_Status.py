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
  <id>532</id>
  <version>3</version>
  <name>RDKLogger_Dbg_Enabled_Status</name>
  <primitive_test_id>401</primitive_test_id>
  <primitive_test_name>RDKLogger_Dbg_Enabled_Status</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This tests the debug enabled status functionality of RDK Logger.
Test Case ID: CT_RDKLogger_03
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
    <test_case_id>CT_RDKLogger_03</test_case_id>
    <test_objective>To check if a particular log level is enabled for a module</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1/XI3-1</test_setup>
    <pre_requisite>RDK debug manager module should be intialized</pre_requisite>
    <api_or_interface_used>rdk_dbg_enabled()</api_or_interface_used>
    <input_parameters>rdk_dbg_enabled:  
string – level (e.g., INFO)
string – module (e.g., QAMSRC)</input_parameters>
    <automation_approch>1. TM loads RDKLoggerStub_agent via the test agent.  
2. TM will invoke “TestMgr_RDKLogger_Dbg_Enabled_Status” in RDKLoggerStub_agent. 
3. RDKLoggerStub_agent will call rdk_logger_init() API of the component and get the result.  
4. On success of rdk_logger_init() API, RDKLoggerStub_agent will call rdk_dbg_enabled() API of the component and get the result. 
5. RDKLoggerStub_agent will call a helper function to find if specified module and level are enabled in debug.ini file. 
6. RDKLoggerStub_Agent will send SUCCESS or FAILURE to TM after comparing return  value of rdk_dbg_enabled() API and helper function.</automation_approch>
    <except_output>Checkpoint 1..Check for the return value of  rdk_dbg_enabled API and cross check with debug.ini settings.
Checkpoint 2.Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>librdkloggerstub.so 
TestMgr_RDKLogger_Dbg_Enabled_Status</test_stub_interface>
    <test_script>RDKLogger_Dbg_Enabled_Status</test_script>
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
obj.configureTestCase(ip,port,'RDKLogger_Dbg_Enabled_Status');
#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "rdklogger module loading status :%s" %result;

#Check for SUCCESS/FAILURE of rdklogger module
if "SUCCESS" in result.upper():
    #Set the module loading status
    obj.setLoadModuleStatus("SUCCESS");

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('RDKLogger_Dbg_Enabled_Status');

    expectedRes = "SUCCESS"
    module = "DVR"
    print "Requested module: %s"%module
    tdkTestObj.addParameter("module",module);
    level = "ERROR"
    print "Requested level: %s"%level
    tdkTestObj.addParameter("level",level);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedRes);

    #Get the result of execution
    result = tdkTestObj.getResult();
    print "[TEST EXECUTION RESULT] : %s" %result;
    details = tdkTestObj.getResultDetails();
    #Set the result status of execution
    if "SUCCESS" in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
        print "rdklogger dbg enabled status Successful: [%s]" %details;
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "rdklogger dbg enabled status Failed: [%s]"%details;

    #unloading rdklogger module
    obj.unloadModule("rdklogger");
else:
    print "Failed to load rdklogger module";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");
