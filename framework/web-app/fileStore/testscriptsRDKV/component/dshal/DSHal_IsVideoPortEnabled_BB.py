##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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
  <name>DSHal_IsVideoPortEnabled_BB</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_IsVideoPortEnabled</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check if the video port enable status is retrieved for BaseBand port type</synopsis>
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
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_147</test_case_id>
    <test_objective>To check if the video port enable status is retrieved for BaseBand port type</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetVideoPort(dsVideoPortType_t type, int index, int *handle)
dsIsVideoPortEnabled(int handle, bool *enabled)</api_or_interface_used>
    <input_parameters>type - Video port type
index- Video port index
handle - Video port handle</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via the test agent.
2 . DSHAL agent will invoke the api dsGetVideoPort to get the handle for port type which is not supported for dsIsVideoPortEnabled API
3 . DSHAL agent will invoke the api dsIsVideoPortEnabled to get the video port enable status
4. TM checks if the API call fails and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call is success</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_IsVideoPortEnabled_BB</test_script>
    <skipped>No</skipped>
    <release_version>M80</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import deviceCapabilities;
from dshalUtility import *;

#Test component to be tested
dshalObj = tdklib.TDKScriptingLibrary("dshal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
dshalObj.configureTestCase(ip,port,'DSHal_IsVideoPortEnabled_BB');

#Get the result of connection with test component and STB
dshalloadModuleStatus = dshalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %dshalloadModuleStatus;

#Check if Base Band port is supported by the DUT
capable = deviceCapabilities.getconfig(dshalObj,"videoPort","BB")

if "SUCCESS" in dshalloadModuleStatus.upper() and capable:
    dshalObj.setLoadModuleStatus(dshalloadModuleStatus);
    expectedResult="SUCCESS";
    #Prmitive test case which associated to this Script
    tdkTestObj = dshalObj.createTestStep('DSHal_GetVideoPort');
    tdkTestObj.addParameter("portType", videoPortType["BB"]);
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    print "DSHal_GetVideoPort result: ", actualResult

    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        details = tdkTestObj.getResultDetails();
        print details;
        expectedResult = "SUCCESS";

        tdkTestObj = dshalObj.createTestStep('DSHal_IsVideoPortEnabled');
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        print "DSHal_IsVideoPortEnabled result: ", actualResult;
        details = tdkTestObj.getResultDetails();
        print "Video port enable status: ", details
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            print "BaseBand Video port enable status retrieved";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "BaseBand Video port enable status not retrieved";
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "BaseBand Video port handle not retrieved";

    dshalObj.unloadModule("dshal");

elif not capable and "SUCCESS" in dshalloadModuleStatus.upper():
    print "Exiting from script";
    dshalObj.setLoadModuleStatus("FAILURE");
    dshalObj.unloadModule("dshal");

else:
    print "Module load failed";
