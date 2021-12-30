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
  <name>WesterosHal_DisplaySizeListenerTest</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>WesterosHal_GetDisplayInfo</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Add displaysize listener and change resolution size to cross verify callback</synopsis>
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
    <box_type>Video_Accelerator</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>RPI-Client</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>IPClient-3</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>WESTEROS_HAL_02</test_case_id>
    <test_objective>Add displaysize listener and change resolution size to cross verify callback</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG, Xi, Video_Accelrator, RPI</test_setup>
    <pre_requisite>Display Device must be connected with DUT</pre_requisite>
    <api_or_interface_used>WstGLAddDisplaySizeListener</api_or_interface_used>
    <input_parameters>resolution size to create native window</input_parameters>
    <automation_approch>1.Load westeroshal and devicesettings module.
2.Create Native window with 1280x720 resolution size.
3.Change resolution size to to any other supported resolution using devicesettings api.
4.Check if callback data is updated with set resolution size.
5.Destroy Native window</automation_approch>
    <expected_output>Callback data must be updated with set resolution size after resolution change is successfull</expected_output>
    <priority>High</priority>
    <test_stub_interface>libwesteroshalstub.la</test_stub_interface>
    <test_script>WesterosHal_DisplaySizeListenerTest</test_script>
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
wsObj = tdklib.TDKScriptingLibrary("westeroshal","1");
dsObj = tdklib.TDKScriptingLibrary("devicesettings","1.2");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
wsObj.configureTestCase(ip,port,'WesterosHal_DisplaySizeListenerTest');
dsObj.configureTestCase(ip,port,'WesterosHal_DisplaySizeListenerTest');

expectedresult="SUCCESS"

#Get the result of connection with test component and DUT
result = wsObj.getLoadModuleResult().upper();
print "[WESTEROS HAL LIB LOAD STATUS]  :  %s" %result;

if result == "FAILURE":
    exit()

wsObj.setLoadModuleStatus(result);
result = dsObj.getLoadModuleResult().upper();
print "[DEVICESETTING LIB LOAD STATUS]  :  %s" %result;

if result == "FAILURE":
    wsObj.unloadModule("westeroshal");
    exit()

dsObj.setLoadModuleStatus(result);
resolution = "720p"
width = 1280
height = 720
result,details = executeTest(wsObj, 'WesterosHal_CreateNativeWindow', {"width":width,"height":height});
if result:
    result,details = executeTest(wsObj, 'WesterosHal_AddDisplaySizeListener');
    if result:
        result,details = executeTest(dsObj, 'DS_ManagerInitialize');
        if result:
            result,details = executeTest(dsObj, 'DS_IsDisplayConnectedStatus');
            if result and "TRUE" not in details:
                print "TV is not connected\nPlease connect display device to DUT to proceed testing";
                exit()
            elif not result:
                exit()
            result,details = executeTest(dsObj, 'DS_Resolution');
            if result:
                resolutions = details.split(":");
                resolutionList = resolutions[1].split(",");
                resolutionSet = set(resolutionList)
                resolutionSet.remove(resolution);
                resolution = resolutionSet.pop();
            print "Setting Resolution to %s"%resolution
            result,details = executeTest(dsObj, 'DS_SetResolution', {"resolution":resolution,"port_name":"HDMI0"});
            if result:
                tdkTestObj = wsObj.createTestStep('WesterosHal_GetCallBackData');
                tdkTestObj.executeTestCase(expectedresult);
                actualResult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                height = resolution.split('p', 1)[0]
                if actualResult == expectedresult and height in details:
                    print "CallBack returns correct resolution size";
                    print details
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print "CallBack returning wrong resolution";
                    print details
                    tdkTestObj.setResultStatus("FAILURE")
            result,details = executeTest(dsObj, 'DS_ManagerDeInitialize');
            result,details = executeTest(wsObj, 'WesterosHal_DestroyNativeWindow');
    else:
        print "DS Manager Connection FAILED";
 
wsObj.unloadModule("westeroshal");
dsObj.unloadModule("devicesettings");
