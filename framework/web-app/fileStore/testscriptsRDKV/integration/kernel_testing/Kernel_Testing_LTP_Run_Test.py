##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2023 RDK Management
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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Kernel_Testing_LTP_Run_Test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>kernel_test_execute</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To execute LTP test and get the test results</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <box_type>Video_Accelerator</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>RDKTV</box_type>
    <box_type>RPI-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
      <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>KERNEL_TEST_1</test_case_id>
    <test_objective>To execute LTP test and get the test result</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator, RPI, RDKTV</test_setup>
    <pre_requisite>LTP Binaries must be installed in the DUT</pre_requisite>
    <api_or_interface_used>systemutil</api_or_interface_used>
    <input_parameters>Test Protocol to be executed</input_parameters>
    <automation_approch>1.Load the systemutil module
2.Construct the command to Execute the required LTP Protocol Test Binaries 
3.Execute the constructed Command in the DUT and verify the Results</automation_approch>
    <expected_output>All Protocol Test_uites must be SUCCESS</expected_output>
    <priority>Medium</priority>
    <test_stub_interface>systemutil</test_stub_interface>
    <test_script>Kernel_Testing_LTP_Run_Test</test_script>
    <skipped></skipped>
    <release_version>M108</release_version>
    <remarks></remarks>
  </test_cases>
</xml> 

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from KernelTestingUtility import *
from KernelTestingVariables import *
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
#Test component to be tested
expectedResult="SUCCESS"

if(input_test_suites == ' '):
    print "\n Please enter Test_Suite name's in KernelTestingVariable.py file"
    exit

print "\nEntered input_test_suites are:",(input_test_suites)
#Using systemutil library for command execution
sysUtilObj = tdklib.TDKScriptingLibrary("systemutil","1")
sysUtilObj.configureTestCase(ip,port,'Kernel_Testing_LTP_Run_Test');
#Load the systemutil library
sysutilloadModuleStatus =sysUtilObj.getLoadModuleResult()
print "[System Util LIB LOAD STATUS]  :  %s" %sysutilloadModuleStatus
sysUtilObj.setLoadModuleStatus(sysutilloadModuleStatus)
if "SUCCESS" in sysutilloadModuleStatus.upper():
    tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand')
    for protocol in input_test_suites.split(','):
        print "\nExecuting kernel %s test using tdk agent" %(protocol)
        command = "sh " + kernel_test_ltp_script_path + "/ltp_executor.sh "+ protocol+ ' '  + " 2>/dev/null"
        print command
	result,output=executeTestCommandUsingTDKAgent(tdkTestObj,command)
	if "SUCCESS" in result.upper():
	    test_status=getLTPTestStatusAndSummary(output)
	    if test_status == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS")
		print "Kernel test %s passed\n" %(protocol)
            else:
		tdkTestObj.setResultStatus("FAILURE")
		print "Kernel test %s failed\n" %(protocol)
            print "Test_suit of %s is completed\n" %(protocol)
            print "-"*100
    print "User specified %s Test_Suites are executed\n" %(input_test_suites)
    sysUtilObj.unloadModule("systemutil");
else:
    print "SystemUtil Module load failed"
    sysUtilObj.setLoadModuleStatus("FAILURE");

