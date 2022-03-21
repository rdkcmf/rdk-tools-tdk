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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>FCS_Essos_Wayland_Client_Validation</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test to execute the Essos_TDKTestApp as wayland client and verify the results</synopsis>
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
    <!--  -->
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
    <test_case_id>FCS_GRAPHICS_03</test_case_id>
    <test_objective>Test to execute the Essos_TDKTestApp as wayland client and verify the results</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator, RPI</test_setup>
    <pre_requisite>1.TDK Agent should be up and running in the DUT
2.The Essos_TDKTestApp test binary should be available in the device</pre_requisite>
    <api_or_interface_used>Execute the Essos_TDKTestApp application in DUT</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Load the systemutil module.
2.Execute the "Essos_TDKTestApp" command along with "USE_WAYLAND" option to run essos as wayland client, "-d" (debug option) and "-t=20" (timeout option for 20 seconds) in DUT. During the execution, the DUT will execute the avaiable in "Essos_TDKTestApp" test app.
3.Verify the output from the execute command and check if the strings no "VALIDATION ERROR"  statements are present.
4.Based on the ExecuteCommand() return value and the output returned from the EssosValidation application, TM return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1. Verify the API call is success
Checkpoint 2. Verify that the output returned from EssosValidation "VALIDATION ERROR" statements.</expected_output>
    <priority>High</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_Essos_Wayland_Client_Validation</test_script>
    <skipped>No</skipped>
    <release_version>M95</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import FCS_GraphicsValidation_utility
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil","2.0");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'FCS_Essos_Wayland_Client_Validation');
#Get the result of connection with test component and STB
sysutilLoadStatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %sysutilLoadStatus
if "SUCCESS" in sysutilLoadStatus.upper():
    #Get EssosValidation configuration file
    logFile,EssosValidation_log = FCS_GraphicsValidation_utility.getLogFile(obj);

    #Configure Variables to start westeros instance
    display = "wayland-0";
    #Timeout is set to 20 seconds
    timeout = 20;
    #Configure the test to be executed
    Test = "Essos"
    #Run the Essos_TDKTestApp with options 
    #Add -t option for timeout
    options = str(timeout);
    #Add display for westeros instance
    options = options + " " + display + " ";
    #Add USE_WAYLAND option to run essos as wayland client
    options = options + "USE_WAYLAND";
    
    details = FCS_GraphicsValidation_utility.RunTest(obj,Test,logFile,options);
    print "[TEST EXECUTION DETAILS] : %s" %details;
    #Wait for Test to get completed
    time.sleep(35)
    #Transfer Essos_TDKTestApp log file from STB
    try:
        tdkTestObj = obj.createTestStep('FireboltCompliance_DoNothing');
        filepath = tdkTestObj.transferLogs( EssosValidation_log, "false" );
    except:
        print "Transfer of logs unsuccessfull";
        obj.unloadModule("systemutil");
        exit() 
    #Parsing the output of Essos_TDKTestApp
    try:
        FCS_GraphicsValidation_utility.PrintTitle("SUMMARY OF TEST EXECUTION")
        FCS_GraphicsValidation_utility.Summary(filepath,"VALIDATION");
        data = open(filepath,'r');
        message = data.read()
        print "\n**************Essos_TDKTestApp Execution Log - Begin*************\n\n"
        print(message)
        data.close()
        print "\n**************Essos_TDKTestApp Execution - End*************\n\n"
        #Reading the Essos_TDKTestApp Execution log file to check for number of failures 
        #Get Number of failures by filtering "VALIDATION" error statements
        Failures = FCS_GraphicsValidation_utility.getNumberOfFailures(filepath,"VALIDATION")
        if Failures:
            EssosValidationExecutionStatus = "FAILURE"
            print "Observed failures during execution"
        else:
            EssosValidationExecutionStatus = "SUCCESS"
            print "Successfuly Executed the test application"
            print "[TEST EXECUTION RESULT] : %s" %EssosValidationExecutionStatus;
    except:
        print "ERROR : Unable to open execution log file"
        obj.unloadModule("systemutil");
        exit();
    #Delete the log file in DUT
    FCS_GraphicsValidation_utility.deleteLogFile(obj,EssosValidation_log,EssosValidationExecutionStatus);
    obj.unloadModule("systemutil");
else:
    print "Failed to load sysutil module\n";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");
