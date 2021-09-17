##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
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
  <version>21</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>FCS_iCrypto_InterfaceTests_OpenSSL</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test to execute the iCrypto Interface tests suites and th OpenSSL verify the results</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2</execution_time>
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
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <box_type>IPClient-WiFi</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>FCS_ICRYPTO_01</test_case_id>
    <test_objective>Test to execute the iCrypto Interface tests suites with OpenSSL and verify the results</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator, RPI</test_setup>
    <pre_requisite>1.TDK Agent should be up and running in the DUT
2. The iCrypto interface test binary should be available in the device</pre_requisite>
    <api_or_interface_used>Execute the iCrypto Interface test application, "cgfacetests" in DUT</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Load the systemuitl module.
2.Execute the "cgfacetests" command in DUT. During the execution, the DUT will execute all the tests available in iCrypto interface tests suite.
3.This test script is currently validated the iCrypto test applciation with OpenSSL implementation only. Test support for validating SECAPI based implementation will be in the test application future.
4.Verify the output from the execute command and check if the strings "TOTAL:" and "0 FAILED" exists in the returned output
5.Based on the ExecuteCommand() return value and the output returned from the cgfacetests application, TM return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1. Verify the API call is success
Checkpoint 2. Verify that the output returned from cgfacetests contains the strings "TOTAL:" and "0 FAILED"</expected_output>
    <priority>High</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_iCrypto_InterfaceTests_OpenSSL</test_script>
    <skipped>No</skipped>
    <release_version>M93</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import FCS_iCrypto_utility

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'FCS_iCrypto_InterfaceTests_OpenSSL');

#Get the result of connection with test component and STB
sysutilLoadStatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %sysutilLoadStatus
if "SUCCESS" in sysutilLoadStatus.upper():

    #Get iCrypto configuration file
    logFile,iCrypto_log = FCS_iCrypto_utility.getLogFile(obj);

    #Configure the test to be executed
    Test = "interfaceTest"

    #Run the interface test for OpenSSL
    details = FCS_iCrypto_utility.RunTest(obj,Test,logFile);
    print "[TEST EXECUTION DETAILS] : %s" %details;

    #Transfer iCrypto log file from STB
    try:
        tdkTestObj = obj.createTestStep('FireboltCompliance_DoNothing');
        filepath = tdkTestObj.transferLogs( iCrypto_log, "false" );
    except:
        print "Transfer of logs unsuccessfull";
        obj.unloadModule("systemutil");
        exit() 

    #Parsing the output of iCrypto test app
    try:
        FCS_iCrypto_utility.PrintTitle("Test script is developed to work with OpenSSL implementation")
        FCS_iCrypto_utility.Summary(filepath);
        FCS_iCrypto_utility.PrintTitle("SUMMARY OF FAILED TESTCASES")
        FCS_iCrypto_utility.FailureSummary(filepath);
        data = open(filepath,'r');
        message = data.read()
        print "\n**************iCrypto TestApp Execution Log - Begin*************\n\n"
        print(message)
        data.close()
        print "\n**************iCrypto TestApp Execution - End*************\n\n"

        #Reading the iCrypto Execution log file to check for number of failures 
        Failures = FCS_iCrypto_utility.getNumberOfFailures(filepath)
        if Failures:
            iCryptoExecutionStatus = "FAILURE"
            print "Observed failures during execution"
        else:
            iCryptoExecutionStatus = "SUCCESS"
            print "Successfuly Executed the test application"
        print "[TEST EXECUTION RESULT] : %s" %iCryptoExecutionStatus;
    except:
        print "ERROR : Unable to open execution log file"
        obj.unloadModule("systemutil");
        exit();

    #Delete the log file in DUT
    FCS_iCrypto_utility.deleteLogFile(obj,iCrypto_log,iCryptoExecutionStatus);

    obj.unloadModule("systemutil");

else:
    print "Failed to load sysutil module\n";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");
