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
  <name>FCS_Security_Kernel_Module_Unload_disable</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Kernel module unload MUST be disabled after boot unless architecturally infeasible.</synopsis>
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
    <test_case_id>FCS_Security_14</test_case_id>
    <test_objective>Kernel module unload MUST be disabled after boot unless architecturally infeasible.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator,RPI,RDK TV</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. rmmod any module (low priority ones),
2.operation should not be permitted (Success)
3.If module removed, reboot the device to maintain its original status</automation_approch>
    <expected_output>Kernel module unload MUST be disabled after boot unless architecturally infeasible.</expected_output>
    <priority>Low</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_Security_Kernel_Module_Unload_disable</test_script>
    <skipped>No</skipped>
    <release_version>M108</release_version>
    <remarks></remarks>
  </test_cases>
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
obj.configureTestCase(ip,port,'FCS_Security_Kernel_Module_Unload_disable');
sysUtilLoadStatus = obj.getLoadModuleResult();
print "System module loading status : %s" %sysUtilLoadStatus;
#Set the module loading status
obj.setLoadModuleStatus(sysUtilLoadStatus);

if "SUCCESS" in sysUtilLoadStatus.upper():
    print "\nTEST STEP :Verify Kernel module unload MUST be disabled after boot unless architecturally infeasible"
    command = 'cd /lib/modules/`uname -r`/kernel ;'
    command = command + 'lsmod | grep -w  "0" | cut -d  " " -f 1'
    result,details,tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command":command}, True)
    output = tdkTestObj.getResultDetails().replace(r'\n', '\n');
    details_list=output.split("\n")
    state= True
    for lst in details_list[1::-1]:
        result,details,tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command":"rmmod ./kernel/{}".format(lst)}, True)
        if not details:
            print "FAILURE:Kernel module {} Removal Operation Is Not restricted to user".format(lst)
            tdkTestObj.setResultStatus("FAILURE");
            state= False
            break     
        else:
            print "SUCCESS:Kernel module Operation Is restricted to user"
            tdkTestObj.setResultStatus("SUCCESS");
    if state==False:
        print "Kernal module operation permitted hence reboot the device to maintain its original status"
        obj.initiateReboot();
    obj.unloadModule("systemutil");

else:
    print "Load module failed"

