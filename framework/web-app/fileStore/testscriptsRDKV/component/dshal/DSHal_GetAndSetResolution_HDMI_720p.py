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
  <name>DSHal_GetAndSetResolution_HDMI_720p</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_GetResolution</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check if the resolution is set to 720p</synopsis>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_111</test_case_id>
    <test_objective>To check if the resolution is set to 720p</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetVideoPort(dsVideoPortType_t type, int index, int *handle)
dsGetResolution(int handle, dsVideoPortResolution_t *resolution)
dsSetResolution(int handle, dsVideoPortResolution_t *resolution, bool persist)</api_or_interface_used>
    <input_parameters>type - Video port type
index- Video port index
handle - Video port handle
resolution - resolution</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via the test agent.
2 . DSHAL agent will invoke the api dsGetVideoPort to get the handle for HDMI port
3 . DSHAL agent will invoke the api dsSetResolution to set the resolution to 720p
4 . DSHAL agent will invoke the api dsGetResolution
5. TM checks if the resolution is set and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call is success
Checkpoint 2 Verify that the resolution is set</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_GetAndSetResolution_HDMI_720p</test_script>
    <skipped>No</skipped>
    <release_version>M76</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from dshalUtility import *;

#Test component to be tested
dshalObj = tdklib.TDKScriptingLibrary("dshal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
dshalObj.configureTestCase(ip,port,'DSHal_GetAndSetResolution_HDMI_720p');

#Get the result of connection with test component and STB
dshalloadModuleStatus = dshalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %dshalloadModuleStatus;

dshalObj.setLoadModuleStatus(dshalloadModuleStatus);

if "SUCCESS" in dshalloadModuleStatus.upper():
    expectedResult="SUCCESS";
    #Prmitive test case which associated to this Script
    tdkTestObj = dshalObj.createTestStep('DSHal_GetVideoPort');
    tdkTestObj.addParameter("portType", videoPortType["HDMI"]);
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    print "DSHal_GetVideoPort result: ", actualResult

    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        details = tdkTestObj.getResultDetails();
        print details;

        tdkTestObj = dshalObj.createTestStep('DSHal_IsDisplayConnected');
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        print "DSHal_IsDisplayConnected result: ", actualResult
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            details = tdkTestObj.getResultDetails();
            print "Display connection status: ", details
            if details == "true":
                resolution = "720p";
                tdkTestObj = dshalObj.createTestStep('DSHal_SetResolution');
                tdkTestObj.addParameter("resolution",resolution);
                tdkTestObj.addParameter("pixelResolution",0); #1920x1080 Resolution
                tdkTestObj.addParameter("aspectRatio",0); #4:3 aspect ratio
                tdkTestObj.addParameter("stereoScopicMode",0); #Unknown mode
                #Execute the test case in STB
                tdkTestObj.executeTestCase(expectedResult);
                actualResult = tdkTestObj.getResult();
                print "DSHal_SetResolution result: ", actualResult;
                if expectedResult in actualResult:
                    details = tdkTestObj.getResultDetails();
                    print details;
                    tdkTestObj = dshalObj.createTestStep('DSHal_GetResolution');
                    #Execute the test case in STB
                    tdkTestObj.executeTestCase(expectedResult);
                    actualResult = tdkTestObj.getResult();
                    print "DSHal_GetResolution result: ", actualResult;
                    if expectedResult in actualResult:
                        resolutionName = tdkTestObj.getResultDetails();
                        print "Resolution Name retrieved: ", resolutionName;

                        if resolution in resolutionName:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "Resolution set properly";
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Resolution not set";
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "DSHal_GetResolution call failed";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "DSHal_SetResolution call failed";
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Please test connecting a display device";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Failed to get display connection status";
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "VideoPort handle not retrieved";

    dshalObj.unloadModule("dshal");

else:
    print "Module load failed";
