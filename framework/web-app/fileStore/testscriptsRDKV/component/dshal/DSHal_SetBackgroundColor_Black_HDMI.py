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
  <name>DSHal_SetBackgroundColor_Black_HDMI</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_SetBackgroundColor</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To set video device background color to Black</synopsis>
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
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_53</test_case_id>
    <test_objective>To set video device background color to Black</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3,Video_Accelerator</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetVideoPort(dsVideoPortType_t type, int index, int *handle)
dsSetBackgroundColor(int handle, dsVideoBackgroundColor_t color)</api_or_interface_used>
    <input_parameters>type - Video port type
index- Video port index
handle - Video port handle
color - BG color to set</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via the test agent.
2 . DSHAL agent will invoke the api dsSetBackgroundColor to set the BG color to Black
3. TM checks if the color is set and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call is success
Checkpoint 2 Verify that the BG color is set to Black</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_SetBackgroundColor_Black_HDMI</test_script>
    <skipped>No</skipped>
    <release_version>M75</release_version>
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
sysObj = tdklib.TDKScriptingLibrary("systemutil","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
dshalObj.configureTestCase(ip,port,'DSHal_SetBackgroundColor_Black_HDMI');
sysObj.configureTestCase(ip,port,'DSHal_SetBackgroundColor_Black_HDMI');

#Get the result of connection with test component and STB
dshalloadModuleStatus = dshalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %dshalloadModuleStatus;
sysloadModuleStatus = dshalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %sysloadModuleStatus;

dshalObj.setLoadModuleStatus(dshalloadModuleStatus);
sysObj.setLoadModuleStatus(sysloadModuleStatus);

if "SUCCESS" in dshalloadModuleStatus.upper() and "SUCCESS" in sysloadModuleStatus.upper():
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
            colorId = {"Blue":0, "Black":1, "None":2, "Invalid":5};
            colorMap = {"Blue":"ff0000ff", "Black":"ff000000", "Invalid":"0", "None":"0"};
    
            if details == "true":
                print "Trying to set BGColor to Black";	
                tdkTestObj = dshalObj.createTestStep('DSHal_SetBackgroundColor');
                tdkTestObj.addParameter("color", colorId["Black"]);
                #Execute the test case in STB
                tdkTestObj.executeTestCase(expectedResult);
                actualResult = tdkTestObj.getResult();
                print "DSHal_SetBackgroundColor result: ", actualResult;
                if expectedResult in actualResult:
                    details = tdkTestObj.getResultDetails();
                    print details;
                    logName = "/opt/TDK/logs/AgentConsole.log";
                    tdkTestObj = sysObj.createTestStep('ExecuteCommand');
                    cmd = "grep dsSetBackgroundColor " + logName + " | grep '" + str(colorMap["Black"]) + "$\|" + str(colorId["Black"]) + "$'"
                    print cmd
                    tdkTestObj.addParameter("command", cmd);
                    tdkTestObj.executeTestCase("SUCCESS");
                    actualresult = tdkTestObj.getResult();
                    color = tdkTestObj.getResultDetails();
                    print "OUTPUT:", color;
                    if colorMap["Black"] in color or str(colorId["Black"]) in color:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "BGColor set to Black";
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "BGColor not set to Black";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Failed to set BGColor";

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
    sysObj.unloadModule("systemutil");

else:
    print "Module load failed";
