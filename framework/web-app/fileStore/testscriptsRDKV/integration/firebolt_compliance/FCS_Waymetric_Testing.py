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
  <name>FCS_Waymetric_Testing</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To execute waymetric application for measuring the impact of Wayland (Display Server) as compared to rendering directly with EGL on graphics performance</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>FCS_GRAPHICS_04</test_case_id>
    <test_objective>To execute waymetric application for measuring the impact of Wayland (Display Server) as compared to rendering directly with EGL on graphics performance</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator</test_setup>
    <pre_requisite>1.waymetric application must be present in the device
    2.Device must not run any graphics rendering application while waymetric application is started</pre_requisite>
    <api_or_interface_used>Execute the waymetric application in the device</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Load the systemutil module.
    2.Execute the "waymetric" application with "--no-multi" option to skip multi test.
    3.Verify application is executed successfully, obtain the speed indices from the waymetric test report.
    4.Upon successfull retriving all speed indices, TM will set the execution as SUCCESS.</automation_approch>
    <expected_output>speed indices must be successfully obtained</expected_output>
    <priority>High</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_Waymetric_Testing</test_script>
    <skipped>No</skipped>
    <release_version>M95</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import FCS_GraphicsValidation_utility
import time
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil","2.0");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'FCS_Waymetric_Testing');
#Get the result of connection with test component and STB
sysutilLoadStatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %sysutilLoadStatus
if "SUCCESS" in sysutilLoadStatus.upper():
    #Get EssosValidation configuration file
    logFile,Waymetric_log = FCS_GraphicsValidation_utility.getLogFile(obj);
    #Configure the test to be executed
    Test = "waymetric"
    #Run the waymetric app  with options 
    #Add --no-multi option to avoid multi testing
    options = " --no-multi "
    #Add logFile to capture App output
    options = options + logFile
 
    print "\nStarting Test Execution\n"
    tdkTestObj = obj.createTestStep('ExecuteCommand');
    #Test to be executed
    cmd = Test + " " + options;
    tdkTestObj.addParameter("command", cmd);
    #Execute the test case in STB
    tdkTestObj.executeTestCase("SUCCESS");
    #Get the result of execution
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "[TEST EXECUTION RESULT] : %s" %actualResult;
    if "SUCCESS" not in actualResult:
        print "Unable to execute %s" %(test);
        tdkTestObj.setResultStatus("FAILURE");

    #Transfer waymetric report from STB
    try:
        tdkTestObj = obj.createTestStep('FireboltCompliance_DoNothing');
        filepath = tdkTestObj.transferLogs( Waymetric_log, "false" );
    except:
        print "Transfer of logs unsuccessfull";
        obj.unloadModule("systemutil");
        exit() 

    FCS_GraphicsValidation_utility.PrintTitle("SUMMARY OF TEST EXECUTION")
    waymetric_index = FCS_GraphicsValidation_utility.Summary(filepath,"speed index");

    try:
        data = open(filepath,'r');
        message = data.read()
        print "\n**************Waymetric Execution Log - Begin*************\n\n"
        print(message)
        data.close()
        print "\n**************Waymetric Execution - End*************\n\n"
    except:
        print "ERROR : Unable to open execution log file"
        obj.unloadModule("systemutil");
        exit();


    if waymetric_index:
        FCS_GraphicsValidation_utility.deleteLogFile(obj,Waymetric_log,"SUCCESS");
    else:
        print "Waymetric Testing Failed"
        FCS_GraphicsValidation_utility.deleteLogFile(obj,Waymetric_log,"FAILURE");

    obj.unloadModule("systemutil");
else:
    print "Failed to load sysutil module\n";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");
