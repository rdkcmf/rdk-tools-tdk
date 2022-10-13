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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>FCS_Security_Kernel_Mount_filesystems_Test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>filesystem containing no executable code MUST have the noexec option specified.</synopsis>
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
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <box_type>RDKTV</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>FCS_Security_12</test_case_id>
    <test_objective>Check if sysfs has no exec permission enabled</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator,RPI,RDK TV</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch>1.TDK Agent should be up and running in the DUT.
2.Check if sysfs has noexec permission by using "mount" command.</automation_approch>
    <expected_output>sysfs must not be mounted  with noexec permission in the DUT</expected_output>
    <priority>Medium</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_Security_Kernel_Mount_filesystems_Test</test_script>
    <skipped></skipped>
    <release_version>M105</release_version>
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
obj.configureTestCase(ip,port,'FCS_Security_Kernel_Mount_filesystems_Test');
sysUtilLoadStatus = obj.getLoadModuleResult();
print "System module loading status : %s" %sysUtilLoadStatus;
#Set the module loading status
obj.setLoadModuleStatus(sysUtilLoadStatus);

if "SUCCESS" in sysUtilLoadStatus.upper():
    print "\nTEST STEP 1: Check if a filesystem containing no executable code MUST have the noexec option specified."
    result,details,tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command":"mount | grep 'sysfs\'"}, True)
    lst=["sysfs"]
    str1=details.split("\\")
    for line in str1:
        #print(line[i-1]
        for val in lst:
            if val in line:
                if "noexec"  in line:
                    print "SUCCESS:{} noexec option is specified".format(val)
                    tdkTestObj.setResultStatus("SUCCESS");
                else:
                    print "FAILURE:{} noexec option is not  specified".format(val)
                    tdkTestObj.setResultStatus("FAILURE");

    obj.unloadModule("systemutil");

else:
    print "Load module failed"
