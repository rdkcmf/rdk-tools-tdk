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
  <name>DSHal_GetVolumeLeveller_Reboot</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_GetVolumeLeveller</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To get the volume leveller mode &amp; level  after reboot and check whether feature is disabled.</synopsis>
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
    <box_type>IPClient-Wifi</box_type>
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_163</test_case_id>
    <test_objective>To get the volume leveller mode after reboot and check whether feature is disabled.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Xi,Video_Accelerator</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetAudioPort(dsAudioPortType_t type, int index, int *handle)
dsGetVolumeleveller(int handledsVolumeLeveller_t *volLeveller)</api_or_interface_used>
    <input_parameters>type - Audio port type
index- Audio port index
handle - Audio port handle
volLeveller - Audio port volume leveller</input_parameters>
    <automation_approch>1. TM will reboot the device and loads the DSHAL agent via the test agent.
2 . DSHAL agent will invoke the api dsGetVolumeleveller to get the volume leveller mode and level.
3. TM checks if the volumeLeveller mode and level are 0 and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Both volumeleveller mode and level must return 0 after reboot</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_GetVolumeLeveller_Reboot</test_script>
    <skipped>No</skipped>
    <release_version>M90</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
import deviceCapabilities;
from dshalUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("dshal","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DSHal_GetVolumeLeveller_Reboot');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

#Check if VolumeLeveller is supported by the DUT
capable = deviceCapabilities.getconfig(obj,"VolumeLeveller");

if "SUCCESS" in result.upper() and capable:
    print "Rebooting the device\n\n";
    obj.initiateReboot();

    expectedResult="SUCCESS";
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('DSHal_GetAudioPort');
    tdkTestObj.addParameter("portType", audioPortType["HDMI"]);
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    print "DSHal_GetAudioPort result: ", actualResult
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        details = tdkTestObj.getResultDetails();
        print details

        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('DSHal_GetVolumeLeveller');
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        print "DSHal_GetVolumeLeveller result: " , actualResult
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            details = tdkTestObj.getResultDetails();
            print "VolumeLeveller Result : " , details
            settings = details.split(",");
            parameters = ["Mode","Level"];
            iteration = 0;
            fail_params = [];
            for data in settings:
                if "Level" in settings:
                    item = data.split(':');
                    if (int(item[1]) == 0):
                        print "Expected %s is obtained"%(parameters[iteration]);
                    else:
                        print "Expected %s after Reboot : 0"%(parameters[iteration]);
                        print "%s obtained : %s"%(parameters[iteration],item[1]);
                        tdkTestObj.setResultStatus("FAILURE");
                        fail_params = parameters[iteration];
                iteration += 1;

            if fail_params:
                print "\n\nTEST FAILED due to unexpected %s"%(fail_params);
        else:
            tdkTestObj.setResultStatus("FAILURE");
            details = tdkTestObj.getResultDetails();
            print "VolumeLeveller Result : " , details

    else:
        tdkTestObj.setResultStatus("FAILURE");
        details = tdkTestObj.getResultDetails();
        print details
    
    obj.unloadModule("dshal");

elif not capable and "SUCCESS" in result.upper():
    print "Exiting from script";
    obj.setLoadModuleStatus("FAILURE");
    obj.unloadModule("dshal");

else:
    print "Module load failed"
