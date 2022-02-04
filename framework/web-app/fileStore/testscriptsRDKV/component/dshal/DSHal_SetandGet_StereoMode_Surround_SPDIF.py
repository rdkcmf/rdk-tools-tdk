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
  <name>DSHal_SetandGet_StereoMode_Surround_SPDIF</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_GetStereoMode</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To set SPDIF audio port stereo mode to "SURROUND"</synopsis>
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
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_9</test_case_id>
    <test_objective>To set SPDIF audio port stereo mode to "SURROUND"</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3,Video_Accelerator</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems
5. Stop dsMgr.service</pre_requisite>
    <api_or_interface_used>dsGetAudioPort(dsAudioPortType_t type, int index, int *handle)
dsSetStereoMode(int handle, dsAudioStereoMode_t mode)
dsGetStereoMode(int handle, dsAudioStereoMode_t *stereoMode)</api_or_interface_used>
    <input_parameters>type - Audio port type
index- Audio port index
handle - Audio port handle
mode - Audio port stereo mode to set
stereoMode - Audio port stereo mode retrieved</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via the test agent.
2 . DSHAL agent will invoke the api dsSetStereoMode to set the stereo mode to "SURROUND"
3 . DSHAL agent will invoke the api dsGetStereoMode to get the stereo mode 
4. TM checks if the stereo mode is same as that set and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call is success
Checkpoint 2 Verify that the stereo mode is set</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_SetandGet_StereoMode_Surround_SPDIF</test_script>
    <skipped>No</skipped>
    <release_version>M73</release_version>
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
dshalObj.configureTestCase(ip,port,'DSHal_SetandGet_StereoMode_Surround_SPDIF');

#Get the result of connection with test component and STB
dshalloadModuleStatus = dshalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %dshalloadModuleStatus;

#Check if SPDIF port is supported by DUT
capable = deviceCapabilities.getconfig(dshalObj,"audioPort","SPDIF");


if "SUCCESS" in dshalloadModuleStatus.upper() and capable:
	dshalObj.setLoadModuleStatus(dshalloadModuleStatus);
        expectedResult="SUCCESS";
        #Prmitive test case which associated to this Script
        tdkTestObj = dshalObj.createTestStep('DSHal_GetAudioPort');
        tdkTestObj.addParameter("portType", audioPortType["SPDIF"]);
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        print "DSHal_GetAudioPort result: ", actualResult

        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            details = tdkTestObj.getResultDetails();
            print details;

            #Prmitive test case which associated to this Script
            tdkTestObj = dshalObj.createTestStep('DSHal_SetStereoMode');
            tdkTestObj.addParameter("stereoMode", stereoModeType["SURROUND"]);
            #Execute the test case in STB
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            print "DSHal_SetStereoMode result: ", actualResult

            if expectedResult in actualResult:
                tdkTestObj.setResultStatus("SUCCESS");
                details = tdkTestObj.getResultDetails();
                print "DSHal_SetStereoMode: ", details
            
                tdkTestObj = dshalObj.createTestStep('DSHal_GetStereoMode');
                #Execute the test case in STB
                tdkTestObj.executeTestCase(expectedResult);
                actualResult = tdkTestObj.getResult();
                print "DSHal_GetStereoMode result: ", actualResult
                if expectedResult in actualResult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    details = tdkTestObj.getResultDetails();
                    print "StereoMode retrieved", details
                    if int(details) == stereoModeType["SURROUND"]:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "StereoMode set to SURROUND successfully";
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "StereoMode not set to SURROUND";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Failed to get stereo mode";
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "DSHal_SetStereoMode failed";

        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "AudioPort handle not retrieved";

        dshalObj.unloadModule("dshal");


elif not capable and "SUCCESS" in dshalloadModuleStatus.upper():
    print "Exiting from script";
    dshalObj.setLoadModuleStatus("FAILURE");
    dshalObj.unloadModule("dshal");

else:
    print "Module load failed";
