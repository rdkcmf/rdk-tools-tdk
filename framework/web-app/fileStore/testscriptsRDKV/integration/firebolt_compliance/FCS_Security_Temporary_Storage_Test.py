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
  <name>FCS_Security_Temporary_Storage_Test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test if temporary storage contents are mounted to a dedicated fiesystem and erased on reboot</synopsis>
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
    <box_type>RDKTV</box_type>
  </box_types>
  <rdk_versions />
  <test_cases>
    <test_case_id>FCS_Security_01</test_case_id>
    <test_objective>Test if temporary storage contents are mounted to a dedicated fiesystem and erased on reboot</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK TV,Video Accelerator, RPI</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>systemutil</api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch>1.TDK Agent should be up and running in the DUT.
2.Check if /tmp is dedicated to file system using mount command.
3.Create a dummy file in /tmp and verify file is created successfully.
4.Reboot the DUT and verify whether dummyfile is erased after reboot</automation_approch>
    <expected_output>CheckPoint 1:Temporary storage must be dedicated to a file system.
CheckPoint 2:Dummy file created must be erased after reboot.</expected_output>
    <priority></priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_Security_Temporary_Storage_Test</test_script>
    <skipped></skipped>
    <release_version>M101</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from tdkvutility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("firebolt_compliance","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil","1");
obj.configureTestCase(ip,port,'FCS_Security_Temporary_Storage_Test');
sysUtilLoadStatus = obj.getLoadModuleResult();
print "System module loading status : %s" %sysUtilLoadStatus;
#Set the module loading status
obj.setLoadModuleStatus(sysUtilLoadStatus);

if "SUCCESS" in sysUtilLoadStatus.upper():
    print "\nTEST STEP 1: Check of temporary storage in mounted on a dedicated file system"
    result,details,tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command":"mount | grep '/tmp' -m1"}, True)

    if result and "tmpfs on /tmp type tmpfs" in details:
        print "SUCCESS: Temporary storage mounted on dedicated file system"
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        print "FAILURE: Temporary storage not mounted on dedicated file system"
        print "mount /tmp storage to a dedicated file system"
        tdkTestObj.setResultStatus("FAILURE");

    print "\nTEST STEP 2:Check if temporarily created files are erased after reboot"
    result,details = executeTest(obj, 'ExecuteCommand', {"command": "echo 'TDK test file' > /tmp/testFile"})
    if result:
        result,details,tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command": "cat /tmp/testFile"}, True)
        if result and 'TDK test file' in details:
            print "Temporary file created successfully"
            tdkTestObj.setResultStatus("SUCCESS");
      
            #Rebooting the DUT
            print "Rebooting the device";
            obj.initiateReboot();

            result,details,tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command": "cat /tmp/testFile"}, True)
            if result and 'TDK test file' not in details:
                print "SUCCESS : Temporary file erased after reboot as expected"
                tdkTestObj.setResultStatus("SUCCESS");
  
            elif result and 'TDK test file' in details:
                print "FAILURE : Temporary file not erased after reboot"
                tdkTestObj.setResultStatus("FAILURE");
    
            else:
                print "FAILURE : Unable to verify if temporary file exists or not"
                tdkTestObj.setResultStatus("FAILURE");

        else:
            print "Temporary file creation unsuccessfull"
            tdkTestObj.setResultStatus("FAILURE");
     
    else:
        print "FAILURE : Temporary File was not created successfully"
        tdkTestObj.setResultStatus("FAILURE");
 
    obj.unloadModule("systemutil");

else:
    print "Load module failed"
