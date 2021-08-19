##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2017 RDK Management
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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>USBCtrl_Termination</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>USBCtrl_Init</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>API validation for usbctrl termination</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_USBCtrl_02</test_case_id>
    <test_objective>API validation for usbctrl termination</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Pace xg1v3</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>rusbCtrl_term</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. TM loads the USBCtrl_Agent
2. USBCtrl_Agent will invoke rusbCtrl_term API to to terminate USBCtrl
3. TM will check if the result is 0 and return SUCCESS/FAILURE status.
4. TM unloads the USBCtrl_Agent</automation_approch>
    <except_output>Checkpoint 1.Check the invocation of the API is success.
Checkpoint 2.Check the result is 0</except_output>
    <priority>High</priority>
    <test_stub_interface>Checkpoint 1.Check the invocation of the API is success.
Checkpoint 2.Check the result is 0</test_stub_interface>
    <test_script>USBCtrl_Termination</test_script>
    <skipped>No</skipped>
    <release_version></release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("usbctrl","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'USBCtrl_Termination');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result.upper());

if "SUCCESS" in result.upper():
	print "Module loading success";
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('USBCtrl_Init');
        expectedresult="SUCCESS";
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);

        #Get the result of execution
        result = tdkTestObj.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
	tdkTestObj.setResultStatus(result);

	details = tdkTestObj.getResultDetails();
	print details;
	if "SUCCESS" in result:
		#Prmitive test case which associated to this Script
		tdkTestObj = obj.createTestStep('USBCtrl_Term');
		expectedresult="SUCCESS";
		#Execute the test case in STB
		tdkTestObj.executeTestCase(expectedresult);

		#Get the result of execution
		result = tdkTestObj.getResult();
		print "[TEST EXECUTION RESULT] : %s" %result;
		tdkTestObj.setResultStatus(result);

		details = tdkTestObj.getResultDetails();
		print details;

	obj.unloadModule("usbctrl");
