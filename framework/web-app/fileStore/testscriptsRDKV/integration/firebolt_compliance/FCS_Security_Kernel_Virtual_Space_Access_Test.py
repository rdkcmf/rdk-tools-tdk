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
  <name>FCS_Security_Kernel_Virtual_Space_Access_Test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test if access for kernel virtual filesystem and address space is removed from the system </synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>1</execution_time>
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
  </box_types>
  <rdk_versions />
  <test_cases>
    <test_case_id>FCS_Security_06</test_case_id>
    <test_objective>Test if access for kernel virtual filesystem and address space access is removed from the system</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator, RPI</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>systemutil</api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch>1.TDK Agent should be up and running in the DUT.
2.Check if kernel virtual filesystem access is removed by verifying "kcore" file is not present in /dev or /proc directories.
3.Check if kernel address space access is removed by verifying "kmem" file is not present in /dev or /proc directories.</automation_approch>
    <expected_output>kcore or kmem files must not be present in /proc/ or /dev directories</expected_output>
    <priority>Medium</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_Security_Kernel_Virtual_Space_Access_Test</test_script>
    <skipped></skipped>
    <release_version>M102</release_version>
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
obj.configureTestCase(ip,port,'FCS_Security_Kernel_Virtual_Space_Access_Test');
sysUtilLoadStatus = obj.getLoadModuleResult();
print "System module loading status : %s" %sysUtilLoadStatus;
#Set the module loading status
obj.setLoadModuleStatus(sysUtilLoadStatus);

if "SUCCESS" in sysUtilLoadStatus.upper():
    print "\nTEST STEP 1: Check if kernel virtual filesystem access is removed"
    print "\nEXPECTED OUTPUT : /proc/kcore or /dev/kcore files must not be present"
    result,details,tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command":"find /dev /proc -iname kcore"}, True)

    if details:
        print "FAILURE: kcore file is present"
        print "This allows read access to all the kernels virtual memory space.\nSupport for /dev/kcore MUST be removed."
        tdkTestObj.setResultStatus("FAILURE");
    else:
        print "SUCCESS: kcore file is not present"
        tdkTestObj.setResultStatus("SUCCESS");

    print "\nTEST STEP 1: Check if access to the virtual address space of kernel is removed"
    print "\nEXPECTED OUTPUT : /proc/kmem or /dev/kmem files must not be present"
    result,details,tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command":"find /dev /proc -iname kmem"}, True)

    if details:
        print "FAILURE: kmem file is present"
        print "This provides access to the virtual address space of the operating system kernel, excluding memory that is associated with an I/O device..\nSupport for /dev/kmem MUST be removed."
        tdkTestObj.setResultStatus("FAILURE");
    else:
        print "SUCCESS: kmem file is not present"
        tdkTestObj.setResultStatus("SUCCESS");
    obj.unloadModule("systemutil");

else:
    print "Load module failed"
