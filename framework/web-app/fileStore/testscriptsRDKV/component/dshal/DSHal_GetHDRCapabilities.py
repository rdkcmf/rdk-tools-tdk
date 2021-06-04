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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>1</version>
  <name>DSHal_GetHDRCapabilities</name>
  <primitive_test_id/>
  <primitive_test_name>DSHal_GetHDRCapabilities</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test Script to get STB HDR capabilities</synopsis>
  <groups_id/>
  <execution_time>2</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Video_Accelerator</box_type>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_59</test_case_id>
    <test_objective>Test Script to get STB HDR capabilities as ORed value</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetHDRCapabilities(vdHandle, &amp;capability)</api_or_interface_used>
    <input_parameters>vdHandle - video device handle
capability - to hold STB HDR capability</input_parameters>
    <automation_approch>1.TM loads the DSHAL agent via the test agent.
2.DSHAL agent will invoke the API dsGetHDRCapabilities
3.Check whether proper HDR capability value is obtained if the platform supports it.
4.Update the test result as SUCCESS/FAILURE based on the value obtained.
5.Unload the module</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call is success
Checkpoint 2.Should get the STB HDR capability value</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_GetHDRCapabilities</test_script>
    <skipped>No</skipped>
    <release_version>M75</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("dshal","1");

def check_hdr_capability():
    sysUtilObj = tdklib.TDKScriptingLibrary("systemutil","1");
    sysUtilObj.configureTestCase(ip,port,'DSHal_GetHDRCapabilities');
    sysUtilLoadStatus = sysUtilObj.getLoadModuleResult();
    print "System module loading status : %s" %sysUtilLoadStatus;
    #Set the module loading status
    sysUtilObj.setLoadModuleStatus(sysUtilLoadStatus);

    if "SUCCESS" in sysUtilLoadStatus.upper():
        tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand');
        cmd = "cat /etc/device.properties | grep HDR_CAPABILITY"
        print cmd;
        tdkTestObj.addParameter("command", cmd);
        expectedResult="SUCCESS"
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails()
        if expectedResult in actualResult:
            if details:
                print "Device has HDR capability"
                return True
            else:
                print "Device doesnot have HDR capability"
                return False
        else:
            print "check_hdr_capability failed";
    sysUtilObj.unloadModule("systemutil");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DSHal_GetHDRCapabilities');
imagename= tdklib.getImageName(ip,port);

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";
    HDR_CAPABILITY = check_hdr_capability()
    #print "\nTEST STEP1 : Get the HDR capabilities of SoC using dsGetHDRCapabilities API"
    #print "EXEPECTED OUTPUT : Should get the  OR-ed value of STB HDR capabilities"
    tdkTestObj = obj.createTestStep('DSHal_GetHDRCapabilities');
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    if expectedResult in actualResult:
        details = tdkTestObj.getResultDetails();
        print "ACTUAL RESULT  : dsGetHDRCapabilities call is success"
        print "Value Returned : STB HDR Capabilities : ",details
     
        if (HDR_CAPABILITY and (int(details) > 0)):
            print "HDR standard retrieved as expected";
            print "[TEST EXECUTION RESULT] : SUCCESS\n"
            tdkTestObj.setResultStatus("SUCCESS");
        elif((not(HDR_CAPABILITY)) and (int(details) == 0)):
            print "No HDR standard retrieved as expected";
            print "[TEST EXECUTION RESULT] : SUCCESS\n"
            tdkTestObj.setResultStatus("SUCCESS");
       
    else:
        tdkTestObj.setResultStatus("FAILURE");
        details = tdkTestObj.getResultDetails();
        print "ACTUAL RESULT  : dsGetHDRCapabilities call failed"
        print "Value Returned : ",details
        print "[TEST EXECUTION RESULT] : FAILURE\n"

    obj.unloadModule("dshal");
else:
    print "Load module failed";
    obj.setLoadModuleStatus("FAILURE");

