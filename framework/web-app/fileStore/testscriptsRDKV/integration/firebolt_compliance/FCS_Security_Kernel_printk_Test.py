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
  <name>FCS_Security_Kernel_printk_Test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check if expected kernel configurations are disabled</synopsis>
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
    <box_type>Video_Accelerator</box_type>
    <box_type>RDKTV</box_type>
    <!--  -->
  </box_types>
  <rdk_versions />
  <test_cases>
    <test_case_id>FCS_Security_08</test_case_id>
    <test_objective>Check if kernel pointers are  hidden if printk is enabled.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK TV,Video Accelerator</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>systemutil</api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch>1.TDK Agent should be up and running in the DUT.
2.Check if printk is enabled by checking /proc/sys/kernel/printk.
3.If printk is enabled, check the level of restriction by checking kptr_restrict.</automation_approch>
    <expected_output>kptr_restrict must be set to 1/2 if printk is enabled.</expected_output>
    <priority>Medium</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_Security_Kernel_printk_Test</test_script>
    <skipped></skipped>
    <release_version>M103</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from tdkvutility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'FCS_Security_Kernel_printk_Test');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

#Path to be extracted
filePath = "/tmp"
#Shell Script path
shellScript = "SecurityTestTDK.sh "
#Test option
testOption = "KERNEL_CONFIG_CHECK "

#Test component to be tested
if "SUCCESS" in result.upper():
    enabled = False;
    printkbuffer = ""
    printkList = ["console_loglevel","default_message_loglevel","minimum_console_loglevel","default_console_loglevel"]
    print "\nTEST STEP 1: Check if printk is enabled"
    result,details,tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command":"cat /proc/sys/kernel/printk"}, True)
    if result and details:
        detailsList = details.split('\\t');
        count = 0;
        for element in detailsList:
            if "0" not in element:
                enabled = True;
                printkbuffer = printkbuffer + "\n%s : %s"%(printkList[count],element.strip('\\n'))
                count = count + 1;
        if enabled:
             print "printk is enabled in the DUT"
             print "loglevels obtained are"
             print printkbuffer
             print "\nTEST STEP 2: Checking level of restriction of printk"
             result,details,tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command":"cat /proc/sys/kernel/kptr_restrict"},True)
             if "0" in details:
                 print "kptr_restrict is set to 0 (the default) (This is the equivalent to %p.)"
                 print "restrict level must be set higher"
                 tdkTestObj.setResultStatus("FAILURE");
             elif "1" or "2" in details:
                 print "kptr_restrict is set to %s which is expected\n"%(details)
                 tdkTestObj.setResultStatus("SUCCESS");
             else:
                 print "Unexpected output from /proc/sys/kernel/kptr_restrict"
                 tdkTestObj.setResultStatus("FAILURE");
        else:
            print "CONFIG_PRINTK is disabled in DUT"
            tdkTestObj.setResultStatus("SUCCESS");
    else:
        print "SUCCESS: /proc/sys/kernel/printk  is not present, its disabled"
        tdkTestObj.setResultStatus("SUCCESS");
    obj.unloadModule("systemutil");
else:
    print "Module load failed"
