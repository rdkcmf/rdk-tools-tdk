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
  <version>6</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>FCS_Security_Kernel_Utilities_permissions_Test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Applications and utilities MUST NOT have the setgid or setuid bit set</synopsis>
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
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>FCS_Security_13</test_case_id>
    <test_objective>Applications and utilities file permission for suid/guid/lsattr
</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator,RPI,RDK TV</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Application_utilities_filePath_suid_guid,Application_utilities_filePath_lsattr</input_parameters>
    <automation_approch>1.Verify g and s bits not set in the file permissions.
2.Application utilities to be tested must be confirmed,Presence of i attribute in lsattr.</automation_approch>
    <expected_output>1.Applications and utilities MUST NOT have the setgid or setuid bit set
2. Unchanging files in writable partitions MUST be marked with "immutable.</expected_output>
    <priority>Medium</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_Security_Kernel_Utilities_Permissions_Test</test_script>
    <skipped>No</skipped>
    <release_version>M106</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from tdkvutility import *
from time import *
from rdkv_performancelib import * ;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("firebolt_compliance","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil","1");
obj.configureTestCase(ip,port,'FCS_Security_Kernel_Utilities_permissions_Test');
sysUtilLoadStatus = obj.getLoadModuleResult();
print "System module loading status : %s" %sysUtilLoadStatus;
#Set the module loading status
obj.setLoadModuleStatus(sysUtilLoadStatus);
if "SUCCESS" in sysUtilLoadStatus.upper():
    print "\nTEST STEP 1:Verify g and s bits not set in the file permissions. Application utilities to be tested must be confirmed"
    conf_file=getConfigFileNameDetail(obj)
    configParam="Application_utilities_filePath_suid_guid"
    status ,UserInput=getDeviceConfigValue(conf_file,configParam)
    print("Utilities  Input file  ",UserInput)
    result,details,tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command":"ls -l {}".format(UserInput)}, True)
    output = tdkTestObj.getResultDetails().replace(r'\n', '\n');
    details_list=output.split("\n")
    for line in details_list[:-1]:
        print(line)
        str1=line.split(" ")
        val=str(str1[0])
        print("Utilities permission  ",str1[0])
        if "s" and "g"and "S" in val:
            print "FAILURE: 's/S' bits set in the file permissions"
            tdkTestObj.setResultStatus("FAILURE");
        else:
            print "SUCCESS: 's/S' bits not set in the file permissions"
            tdkTestObj.setResultStatus("SUCCESS");
    
    print "\nTEST STEP 2: Unchanging files in writable partitions MUST be marked with 'immutable.'"
    conf_file=getConfigFileNameDetail(obj)
    configParam="Application_utilities_filePath_lsattr"
    status ,UserInput=getDeviceConfigValue(conf_file,configParam)
    print("Utilities  Input file ",UserInput)
    result,details,tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command":"lsattr  {}".format(UserInput)}, True)
    output = tdkTestObj.getResultDetails().replace(r'\n', '\n');
    details_list=output.split("\n")
    for line in details_list[:-1]:
        print(line)
	str1=line.split(" ")
        val=str(str1[0])
        print("Utilities permission value is ",str1[0])
        if "i" in val:
            print "SUCCESS:Availability of 'i' attribute in lsattr"
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            print "FAILURE:Unavailability of 'i' attribute in lsattr"
            tdkTestObj.setResultStatus("FAILURE");

    obj.unloadModule("systemutil");

else:
    print "Load module failed"
