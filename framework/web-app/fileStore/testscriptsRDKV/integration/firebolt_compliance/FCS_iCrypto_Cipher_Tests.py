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
  <name>FCS_iCrypto_Cipher_Tests</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test to execute the iCrypto Cipher Encrypt and Decrypt functionalities and verify the results</synopsis>
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
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>FCS_ICRYPTO_03</test_case_id>
    <test_objective>Test to execute the iCrypto Cipher Encrypt and Decrypt functionalities and verify the results</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator, RPI</test_setup>
    <pre_requisite>1.TDK Agent should be up and running in the DUT
2. The iCrypto interface test binary should be available in the device</pre_requisite>
    <api_or_interface_used>Execute the iCrypto Interface test application, "cgfacetests" in DUT</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Load the systemuitl module.
2.Execute the Cipher Interface tests in DUT. During the execution, the DUT will execute all the tests available in iCrypto interface tests suite.
3.The output to be obtained from Encrypt and Decrypt are known beforehand to the application and hence the verification is done based on the data.
4.During the execution a vault object is obtained and raw data is encrypted using aes->Encrypt of Cipher module and the output is verified with the encrypted data known beforehand in the application.
5.An encrypted data is decrypted using aes->Decrypt and the output is verified with the unencrypted data known beforehand in the application.
6.Verify the output from the execute command and check if the string "0 FAILED" exists in the returned output
7.Based on the ExecuteCommand() return value and the output returned from the Cipher tests of "cgfacetests" application, TM return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1. Verify the API call is success
Checkpoint 2. Verify that the output of Cipher Tests returned from cgfacetests contains the strings "TOTAL:" and "0 FAILED"</expected_output>
    <priority>High</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_iCrypto_Cipher_Tests</test_script>
    <skipped>No</skipped>
    <release_version>M94</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time
import FCS_iCrypto_utility

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'FCS_iCrypto_Cipher_Tests');

#Get the result of connection with test component and STB
sysutilLoadStatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %sysutilLoadStatus
if "SUCCESS" in sysutilLoadStatus.upper():

    #Get iCrypto configuration file
    logFile,iCrypto_log = FCS_iCrypto_utility.getLogFile(obj);

    #Configure the test to be executed
    Test = "interfaceTest"
    Module = "Cipher"

    #Run the interface test
    details = FCS_iCrypto_utility.RunTest(obj,Test,logFile);
    print "[TEST EXECUTION DETAILS] : %s" %details;
    time.sleep(3);

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
        ResultFile = FCS_iCrypto_utility.GetTestResults(obj,filepath,Module);
        FCS_iCrypto_utility.Summary(ResultFile);
        data = open(ResultFile,'r');
        message = data.read()
        print "\n**************iCrypto TestApp Execution Log - Begin*************\n\n"
        print(message)
        data.close()
        print "\n**************iCrypto TestApp Execution - End*************\n\n"

        #Reading the iCrypto Execution log file to check for number of failures 
        Failures = FCS_iCrypto_utility.getNumberOfFailures(ResultFile,"ModuleTest")
        if Failures:
            FCS_iCrypto_utility.PrintTitle("SUMMARY OF FAILED TESTCASES")
            FCS_iCrypto_utility.FailureSummary(ResultFile);
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
