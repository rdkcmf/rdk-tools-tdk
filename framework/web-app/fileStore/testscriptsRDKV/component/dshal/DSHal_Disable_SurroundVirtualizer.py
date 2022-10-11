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
  <name>DSHal_Disable_SurroundVirtualizer</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_SetSurroundVirtualizer</primitive_test_name>
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
    <box_type>RDKTV</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_158</test_case_id>
    <test_objective>To disable the surround virtualizer mode after reboot and check whether feature is disabled.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK TV</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetAudioPort(dsAudioPortType_t type, int index, int *handle)
dsGetSurroundVirtualizer(int handle, dsSurroundVirtualizer_t* virtualizer)
dsSetSurroundVirtualizer(int handle, dsSurroundVirtualizer_t virtualizer)</api_or_interface_used>
    <input_parameters>type - Audio port type
index- Audio port index
handle - Audio port handle
virtualizer - Audio port surround virtualizer</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via the test agent.
2. DSHAL agent will invoke the api dsSetSurroundVirtualizer to set the virtualizer mode and boost.
3. DSHAL agent will invoke the api dsGetSurroundVirtualizer to get the virtualizer mode and boost.
4. TM checks if the virtualizer mode and boost are returned as expected and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Both virtualizer mode and boost must be returned as expected</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_Disable_SurroundVirtualizer</test_script>
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
obj.configureTestCase(ip,port,'DSHal_Disable_SurroundVirtualizer');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

#Check if SurroundVirtualizer is supported by the DUT
capable = deviceCapabilities.getconfig(dshalObj,"SurroundVirtualizer")

if "SUCCESS" in result.upper() and capable:
    expectedResult="SUCCESS";
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('DSHal_GetAudioPort');
    tdkTestObj.addParameter("portType", audioPortType["SPEAKER"]);
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
        #Valid range for boost : 0-96
        Boost_test1 = 75;
        Boost_test2 = 25;
        Boost_expected_value = 0;
        print "\nWhen Surround Virtualizer is disabled , Mode and boost must be returned as 0"
        for boost in [Boost_test1,Boost_test2]:
            print "\n Testing for Boost ", boost
            tdkTestObj = obj.createTestStep('DSHal_SetSurroundVirtualizer');
            tdkTestObj.addParameter("mode",Mode);
            tdkTestObj.addParameter("boost",boost);
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            print "DSHal_SetSurroundVirtualizer result: " , actualResult
            if expectedResult in actualResult:
                tdkTestObj.setResultStatus("SUCCESS");
                details = tdkTestObj.getResultDetails();
                print "SetSurroundVirtualizer result : " , details

                #Prmitive test case which associated to this Script
                tdkTestObj = obj.createTestStep('DSHal_GetSurroundVirtualizer');
                tdkTestObj.executeTestCase(expectedResult);
                actualResult = tdkTestObj.getResult();
                print "DSHal_GetSurroundVirtualizer result: " , actualResult
                if expectedResult in actualResult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    details = tdkTestObj.getResultDetails();
                    print "GetSurroundVirtualizer Result : " , details
                    settings = details.split(",");
                    parameters = [Mode,Boost_expected_value];
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
                    print "GetSurroundVirtualizer Result : " , details

            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print "SetSurroundVirtualizer Result : " , details

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
