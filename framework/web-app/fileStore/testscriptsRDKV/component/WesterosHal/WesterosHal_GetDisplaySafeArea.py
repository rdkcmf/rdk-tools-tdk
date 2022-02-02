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
  <name>WesterosHal_GetDisplaySafeArea</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>WesterosHal_GetDisplaySafeArea</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Get Display Safe Area of the native window created</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-Wifi</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <box_type>RPI-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>WESTEROS_HAL_03</test_case_id>
    <test_objective>Get Display Safe Area of the native window created</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG, Xi, Video_Accelrator, RPI</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>WstGLGetDisplaySafeArea</api_or_interface_used>
    <input_parameters>resolution size to create native window</input_parameters>
    <automation_approch>1.Load westeroshal and devicesettings module.
2.Create Native window with 1280x720 resolution size.
3.GetDisplaySafeArea for the native window created.
4.Check if safe area is calculated is same as safe area retrieved.
5.Destroy Native window</automation_approch>
    <expected_output>safe area is calculated should be same as safe area retrieved</expected_output>
    <priority>High</priority>
    <test_stub_interface>libwesteroshalstub.la</test_stub_interface>
    <test_script>WesterosHal_GetDisplaySafeArea</test_script>
    <skipped>No</skipped>
    <release_version>M97</release_version>
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
obj.configureTestCase(ip,port,'WesterosHal_GetDisplaySafeArea');
expectedresult = "SUCCESS"
width = 1280
height = 720

#Calculate Safe Area
#The safe area is the region that is less likely to be non-visible due to overscan.
#The safe area values are currently calculated as a 5% border.
def CalculateSafeArea(resolution_width,resolution_height):
    x = int(0.05*resolution_width)
    y = int(0.05*resolution_height)
    w = int(resolution_width - 2*x)
    h = int(resolution_height - 2*y)
    CalculatedSafeArea = "x=" + str(x) +" y=" + str(y) + " w=" + str(w) + " h=" + str(h);
    return CalculatedSafeArea

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
if result.upper() == "SUCCESS":
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
                result,details = executeTest(obj, 'WesterosHal_GetDisplaySafeArea');
                if result:
                   CalculatedSafeArea = CalculateSafeArea(width,height)
                   if str(details) == str(CalculatedSafeArea):
                      print "GetDisplaySafeArea returns correct size"
                   else:
                      print "Calculated SafeArea = ",CalculatedSafeArea
                      print "GetDisplaySafeArea returns wrong size"
                      tdkTestObj.setResultStatus("FAILURE");
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
