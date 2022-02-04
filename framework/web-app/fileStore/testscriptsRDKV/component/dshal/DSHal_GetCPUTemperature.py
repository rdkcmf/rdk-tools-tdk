##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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
  <version>1</version>
  <name>DSHal_GetCPUTemperature</name>
  <primitive_test_id/>
  <primitive_test_name>DSHal_GetCPUTemperature</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test script to get the CPU Temperature in centigrade</synopsis>
  <groups_id/>
  <execution_time>2</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Video_Accelerator</box_type>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_56</test_case_id>
    <test_objective>Test script to get the CPU Temperature in centigrade</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3,Video_Accelerator</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetCPUTemperature(&amp;temp)</api_or_interface_used>
    <input_parameters>temp - to hold CPU temperature</input_parameters>
    <automation_approch>1.TM loads the DSHAL agent via the test agent.
2.DSHAL agent will invoke the API dsGetCPUTemperature
3.Check whether the obtained CPU temperature is within the expected range
4.Update the test result as SUCCESS/FAILURE 
5.Unload the module</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call is success
Checkpoint 2.CPU temperature should be greater than 0 and less than 125C.</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_GetCPUTemperature</test_script>
    <skipped>No</skipped>
    <release_version>M75</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("dshal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DSHal_GetCPUTemperature');

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";
    print "\nTEST STEP1 : Get the CPU Temperature using dsGetCPUTemperature API"
    print "EXEPECTED OUTPUT : Should get the temperature in centigrade"
    tdkTestObj = obj.createTestStep('DSHal_GetCPUTemperature');
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    if expectedResult in actualResult:
        details = tdkTestObj.getResultDetails();
        print "ACTUAL RESULT  : dsGetCPUTemperature call is success"
        print "Value Returned : CPU Temperature in centigrade : +%sC" %(details)

        print "\nTEST STEP2 : Check whether CPU temperature is within expected range"
        print "EXEPECTED OUTPUT : CPU Temperature should be in 0-125C range"
        if float(details) > float(0) and float(details) < float(125):
            print "ACTUAL RESULT : CPU temperature lies in expected range"
            print "[TEST EXECUTION RESULT] : SUCCESS\n"
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            print "ACTUAL RESULT : CPU temperature not in expected range"
            print "[TEST EXECUTION RESULT] : FAILURE\n"
            tdkTestObj.setResultStatus("FAILURE");
    else:
        tdkTestObj.setResultStatus("FAILURE");
        details = tdkTestObj.getResultDetails();
        print "ACTUAL RESULT  : dsGetCPUTemperature call failed"
        print "Value Returned : ",details
        print "[TEST EXECUTION RESULT] : FAILURE\n"

    obj.unloadModule("dshal");
else:
    print "Load module failed";
    obj.setLoadModuleStatus("FAILURE");

