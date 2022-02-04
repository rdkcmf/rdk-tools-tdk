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
  <name>DSHal_Disable_VolumeLeveller</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_SetVolumeLeveller</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To  disable the Surround Virtualizer mode</synopsis>
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
    <test_case_id>CT_DS_HAL_167</test_case_id>
    <test_objective>To disable the surround volumeLeveller mode after reboot and check whether feature is disabled.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Xi,Video_Accelerator</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetAudioPort(dsAudioPortType_t type, int index, int *handle)
dsGetVolumeLeveller(int handle, dsVolumeLeveller_t* volumeLeveller)
dsSetVolumeLeveller(int handle, dsVolumeLeveller_t volumeLeveller)</api_or_interface_used>
    <input_parameters>type - Audio port type
index- Audio port index
handle - Audio port handle
volumeLeveller - Audio port surround volumeLeveller</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via the test agent.
2. DSHAL agent will invoke the api dsSetVolumeLeveller to set the volumeLeveller mode and level.
3. DSHAL agent will invoke the api dsGetVolumeLeveller to get the volumeLeveller mode and level.
4. TM checks if the volumeLeveller mode and level are returned as expected and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Both volumeLeveller mode and level must be returned as expected</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_Disable_VolumeLeveller</test_script>
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
obj.configureTestCase(ip,port,'DSHal_Disable_VolumeLeveller');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

#Check if VolumeLeveller is supported by the DUT
capable = deviceCapabilities.getconfig(obj,"VolumeLeveller");

if "SUCCESS" in result.upper() and capable:
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

        #Valid Mode values  : 0-Disable, 1-Normal, 2-AUTO
        Mode = 0;
        #Valid range for level : 0-10
        Level_test1 = 7;
        Level_test2 = 5;
        Level_expected_value = 0;
        print "\nWhen Volume Leveller is disabled , Mode and level must be returned as 0"
        for level in [Level_test1,Level_test2]:
            print "\n Testing for Level ", level
            tdkTestObj = obj.createTestStep('DSHal_SetVolumeLeveller');
            tdkTestObj.addParameter("mode",Mode);
            tdkTestObj.addParameter("level",level);
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            print "DSHal_SetVolumeLeveller result: " , actualResult
            if expectedResult in actualResult:
                tdkTestObj.setResultStatus("SUCCESS");
                details = tdkTestObj.getResultDetails();
                print "SetVolumeLeveller result : " , details
               
                #Prmitive test case which associated to this Script
                tdkTestObj = obj.createTestStep('DSHal_GetVolumeLeveller');
                tdkTestObj.executeTestCase(expectedResult);
                actualResult = tdkTestObj.getResult();
                print "DSHal_GetVolumeLeveller result: " , actualResult
                if expectedResult in actualResult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    details = tdkTestObj.getResultDetails();
                    print "GetVolumeLeveller Result : " , details
                    settings = details.split(",");
                    parameters = [Mode,Level_expected_value];
                    iteration = 0;
                    fail_params = [];
                    for data in settings:
                        item = data.split(':');
                        if (int(item[1]) == parameters[iteration]):
                            print "Expected %s is obtained"%(item[0]);
                        else:
                            print "Expected %s : %s"%(item[0],parameters[iteration]);
                            print "%s obtained : %s"%(item[0],item[1]);
                            fail_params = item[0];
                            tdkTestObj.setResultStatus("FAILURE");
                        iteration += 1;  
                    print " "
                    if fail_params:
                        print "\n\nTEST FAILED due to unexpected %s"%(fail_params);

                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    details = tdkTestObj.getResultDetails();
                    print "GetVolumeLeveller Result : " , details
 
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print "SetVolumeLeveller Result : " , details

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
