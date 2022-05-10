##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2022 RDK Management
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
  <name>FCS_Gstreamer_Base_Plugins_Test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Gstreamer_Test_Execute</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Execute gst-plugin-base test applications</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
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
  <rdk_versions />
  <test_cases>
    <test_case_id>FCS_Gstreamer_01</test_case_id>
    <test_objective>Execute opensource gst-plugin-base test applications</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator</test_setup>
    <pre_requisite>OpenSource gstreamer base plugins test applications must be present in OPENSOURCE_TEST path</pre_requisite>
    <api_or_interface_used>ExecuteSuite.sh -- MASTER_SUITE to execute opensource test applications</api_or_interface_used>
    <input_parameters>Type of gstreamer plugins to be tested - gst_plugin_base</input_parameters>
    <automation_approch>1.Load the firebolt_compliance module.
    2.Execute the "gst_plugin_base" test applications using the MASTER_SUITE.
    3.Verify all test suites are successfully executed.
    4.Upon successfull execution of all test suites, tdk_agent will set the result as SUCCESS/FAILURE.</automation_approch>
    <expected_output>No test suites should fail as part of gst_plugin_base</expected_output>
    <priority>Medium</priority>
    <test_stub_interface>libfirebolt_compliance.so.0</test_stub_interface>
    <test_script>FCS_Gstreamer_Base_Plugins_Test</test_script>
    <skipped></skipped>
    <release_version>M99</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import os
import re

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("firebolt_compliance","1");
sysUtilObj = tdklib.TDKScriptingLibrary("systemutil","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'FCS_Gstreamer_Base_Plugins_Test');

def getNumberOfFailures(fileName):
    failed = 0;
    if os.stat(fileName).st_size == 0:
        print "Execution failed";
        return "error"
    with open(fileName, 'r') as a:
        word = "Failed Suite List"
        for line in a:
            line = line.rstrip()
            if re.search(r"({})".format(word), line):
                print line
                failed_str = str(line.split(":")[1].strip())
                failed_list = list(failed_str.split(" "))
                failed = len(failed_list)
    print "Number of FAILURES:",failed
    return failed

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

if "success" in result.lower():
  print "GStreamer_plugins_test module successfully loaded";
  #Set the module loading status
  obj.setLoadModuleStatus("SUCCESS");
  #Primitive test case which associated to this Script
  tdkTestObj = obj.createTestStep('Gstreamer_Test_Execute');
  # Configuring the test object for gst-plugin-good test suites execution
  tdkTestObj.addParameter("GStreamer_plugins_type","gst-plugin-base");
  #Execute the test case in STB
  expectedresult="Test Suite Executed"
  tdkTestObj.executeTestCase(expectedresult);
  #Get the result of execution
  actualresult = tdkTestObj.getResult();
  print "Gst plugin base Test Result : %s" %actualresult;
  
  #To Validate the Execution of Test Suites 
  details = tdkTestObj.getResultDetails();
  if "TotalSuite" in details:
      print "Gst plugin base status details : %s" %details;
      details=dict(item.split(":") for item in details.split(" "))
      Resultvalue=details.values();

      if int(Resultvalue[0])==(int(Resultvalue[1])+int(Resultvalue[2])) and int(Resultvalue[2])==0 and expectedresult in actualresult :
          tdkTestObj.setResultStatus("SUCCESS");
      else:
          tdkTestObj.setResultStatus("FAILURE");
     
      #Get the log path of the Gst plugin base Testsuite
      logpath =tdkTestObj.getLogPath();
      if "TestSummary.log" in logpath:
          print "Log Path :%s"%logpath;
       
          #Transferring the Gst plugin base Testsuite Logs
          filepath = tdkTestObj.transferLogs( logpath, "false" );
    
          #Parsing the output of gst-plugin-base test apps
          data = open(filepath,'r');
          message = data.read()
          print "\n**************GStreamer_plugins_base Execution Log - Begin*************\n\n"
          print(message)
          data.close()
          print "\n**************GStreamer_plugins_base Execution - End*************\n\n"
          failures = getNumberOfFailures(filepath);
          if failures:
              print "Observed Failures during Execution"
              tdkTestObj.setResultStatus("FAILURE");
          else:
              print "Successfully executed all applications under gst-plugin-base"
              tdkTestObj.setResultStatus("SUCCESS");

      else:
          print "Log path is not available and transfer of logs will not be initialised";

  else:
      print " Gst plugin base status details:%s" %details;
      print "Proper Execution details are not received due to error in execution";
      tdkTestObj.setResultStatus("FAILURE");
	 
  #Unloading the opensource test suite module
  obj.unloadModule("firebolt_compliance");

else:
  print "Failed to load GStreamer_plugins_test module";
