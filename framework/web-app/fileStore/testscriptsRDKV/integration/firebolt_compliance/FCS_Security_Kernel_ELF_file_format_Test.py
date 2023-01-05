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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>FCS_Security_Kernel_ELF_file_format_Test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify ELF file format MUST be used</synopsis>
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
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
    <box_type>RDKTV</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>FCS_Security_15</test_case_id>
    <test_objective>Verify ELF file format MUST be used</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator,RPI,RDK TV</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Use hexdump to find if files having elf header find $WHERE -type f -exec hexdump -n 4 -e '4/1 "%2x" " {}\n"'  {} \; | grep ^7f454c46 
2-find-executable-filetypes
</automation_approch>
    <expected_output>1.ELF file format MUST be used</expected_output>
    <priority>Low</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_Security_Kernel_ELF_file_format_Test</test_script>
    <skipped>No</skipped>
    <release_version>M108</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from tdkvutility import *
from time import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("firebolt_compliance","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil","1");
obj.configureTestCase(ip,port,'FCS_Security_Kernel_ELF_file_format_Test');
sysUtilLoadStatus = obj.getLoadModuleResult();
print "System module loading status : %s" %sysUtilLoadStatus;
#Set the module loading status
obj.setLoadModuleStatus(sysUtilLoadStatus);

if "SUCCESS" in sysUtilLoadStatus.upper():
    print "\nTEST STEP 1:Verify Kernel module Executable filetypes(ELF)"
    command1 = 'cd /usr/bin ;'
    str1='4/1 "%2x" " {}\n"'
    command = command1 + "find $WHERE -type f -exec hexdump -n 4 -e '%s' {} \; | grep 'WPEFramework' "%str1
    print command
    result,details,tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command":command}, True)
    output = tdkTestObj.getResultDetails().replace(r'\n', '\n');
    details_list=output.split("\n")
    for lst in details_list[:1]:
        if '7f454c46' in lst:
            print("SUCCESS:ELF magic number successfully verified ")
            tdkTestObj.setResultStatus("SUCCESS");
            
        else:
            print "FAILURE:Unable to find ELF magic number"
            tdkTestObj.setResultStatus("FAILURE");
    obj.unloadModule("systemutil");

else:
    print "Load module failed"

