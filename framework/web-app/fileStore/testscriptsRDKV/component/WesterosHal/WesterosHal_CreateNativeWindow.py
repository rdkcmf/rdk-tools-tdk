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
  <name>WesterosHal_CreateNativeWindow</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>WesterosHal_CreateNativeWindow</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Create a native window with 1280x720 size</synopsis>
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
    <box_type>Hybrid-1</box_type>
    <box_type>IPClient-3</box_type>
    <box_type>Video_Accelerator</box_type>
    <box_type>RPI-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>WESTEROS_HAL_01</test_case_id>
    <test_objective>Create a native window with 1280x720 size</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG, Xi, Video_Accelerator, RPI</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>WstGLCreateNativeWindow, WstGLGetDisplayInfo, WstGLDestroyNativeWindow</api_or_interface_used>
    <input_parameters>width and height for native window creation</input_parameters>
    <automation_approch>1.Load westeroshal module.
2.Create native window with 1280x720 size.
3.Invoke GetDisplayInfo and verify if 1280x720 size is returned.
4.Destroy the native window created.</automation_approch>
    <expected_output>CheckPoint 1. Native Window must be created successfully.
CheckPoint 2. DisplayInfo must return 720p resolution size for the native window created.</expected_output>
    <priority>High</priority>
    <test_stub_interface>libwesteroshalstub.la</test_stub_interface>
    <test_script>WesterosHal_CreateNativeWindow</test_script>
    <skipped>No</skipped>
    <release_version>M96</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from tdkvutility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("westeroshal","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'WesterosHal_CreateNativeWindow');

expectedresult = "SUCCESS"

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

if result.upper() == "SUCCESS":
    width = 1280
    height = 720
    #Prmitive test case which associated to this Script
    result,details = executeTest(obj, 'WesterosHal_CreateNativeWindow', {"width":width,"height":height});
    if result:
        tdkTestObj = obj.createTestStep('WesterosHal_GetDisplayInfo');
        tdkTestObj.executeTestCase("SUCCESS");
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if actualResult == expectedresult:
            if str(width) in details and str(height) in details:
                print "DisplayInfo returns correct size";
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                print "DisplayInfo returns wrong size";
                tdkTestObj.setResultStatus("FAILURE");
        else:
            print "GetDisplayInfo FAILURE";
            tdkTestObj.setResultStatus("FAILURE");
        result,details = executeTest(obj, 'WesterosHal_DestroyNativeWindow');

    if result:
        print "[TEST EXECUTION RESULT] : SUCCESS";    
    else:
        print "[TEST EXECUTION RESULT] : FAILURE";

    #UNload Module
    obj.unloadModule("westeroshal");

else:
     print "Module load failed";
