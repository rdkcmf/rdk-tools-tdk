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
  <name>DSHal_SetVersion</name>
  <primitive_test_id/>
  <primitive_test_name>DSHal_SetVersion</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test script to set the 4 byte runtime version of the dsHAL</synopsis>
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
    <test_case_id>CT_DS_HAL_58</test_case_id>
    <test_objective>Test script to set the 4 byte runtime version of the dsHAL</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3,Video_Accelerator</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetVersion(&amp;version)
dsSetVersion(version)</api_or_interface_used>
    <input_parameters>version - DSHAL version number</input_parameters>
    <automation_approch>1.TM loads the DSHAL agent via the test agent.
2.DSHAL agent will invoke the API dsGetVersion to get the current version
3.DSHAL agent will invoke the API dsSetVersion to set new version number
4.DSHAL agent will invoke the API dsGetVersion to get the latest version.
5.Version number set and latest version number should be same
6.Revert to actual version number using dsSetVersion  API
7.Update the test result as SUCCESS/FAILURE 
8.Unload the module</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call is success
Checkpoint 2.Version number set and version number obtained using dsGetVersion should be same</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_SetVersion</test_script>
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

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DSHal_SetVersion');

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";
    print "\nTEST STEP1 : Get the DSHAL version number using dsGetVersion"
    print "EXPECTED RESULT : Should get the current DSHAL version"
    tdkTestObj = obj.createTestStep('DSHal_GetVersion');
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        details = tdkTestObj.getResultDetails();
        prevVersion = details
        prevVersionNo = int(prevVersion)//(2**16)
        print "ACTUAL RESULT  : dsGetVersion call is SUCCESS"
        print "Value Returned : DSHAL Version Number : %s or %.2f" %(prevVersion,round(prevVersionNo,2))
    
        print "\nTEST STEP2 : Set new DSHAL version number using dsSetVersion"
        print "EXPECTED RESULT : Able to set new DSHAL version number"
        expectedResult="SUCCESS";
        # Version number 2.0
        setVersion = 131072  
        if int(prevVersion) == int(setVersion):
            # Version number 1.0
            setVersion = 65536
        tdkTestObj = obj.createTestStep('DSHal_SetVersion');
        tdkTestObj.addParameter("version", setVersion);
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            details = tdkTestObj.getResultDetails();
            print "ACTUAL RESULT : ",details
            print "DSHAL Version Number Set  : %d or %.2f" %(setVersion,round((setVersion//(2**16)),2))

            print "\nTEST STEP3 : Get the DSHAL version number using dsGetVersion"
            print "EXPECTED RESULT : Should get the DSHAL version set"
            tdkTestObj = obj.createTestStep('DSHal_GetVersion');
            expectedResult="SUCCESS";
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                currVersion = details
                currVersionNo = int(currVersion)//(2**16)
                print "ACTUAL RESULT  : dsGetVersion call is SUCCESS"
                print "Value Returned : DSHAL Version Number : %s or %.2f" %(currVersion,round(currVersionNo,2))

                print "\nTEST STEP4 : Compare DSHAL version set and current version"
                print "EXPECTED RESULT : DSHAL version set and current version should be same"
                if int(setVersion) == int(currVersion):
                    print "ACTUAL RESULT : Able to set DSHAL version successfully"
                    print "[TEST EXECUTION RESULT] : SUCCESS"
                    tdkTestObj.setResultStatus("SUCCESS");
                else:
                    print "ACTUAL RESULT : Not Able to set DSHAL version"
                    print "[TEST EXECUTION RESULT] : FAILURE"
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print "ACTUAL RESULT : dsGetVersion call failed"
                print "Value Retuned : ",details
                print "[TEST EXECUTION RESULT] : FAILURE"

            print "\nTEST STEP5 : Revert DSHAL version number"
            print "EXPECTED RESULT : Able to set previous DSHAL version number"
            expectedResult="SUCCESS";
            tdkTestObj = obj.createTestStep('DSHal_SetVersion');
            tdkTestObj.addParameter("version", int(prevVersion));
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            if expectedResult in actualResult:
                tdkTestObj.setResultStatus("SUCCESS");
                details = tdkTestObj.getResultDetails();
                print "ACTUAL RESULT  : DSHAL version number reverted successfully"
                print "DSHAL Version Number Set  : %s or %.2f" %(prevVersion,round((int(prevVersion)//(2**16)),2))
                print "[TEST EXECUTION RESULT] : SUCCESS\n"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print "ACTUAL RESULT  : DSHAL version number revert failed"
                print "[TEST EXECUTION RESULT] : FAILURE\n"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            details = tdkTestObj.getResultDetails();
            print "ACTUAL RESULT : dsSetVersion call failed"
            print "Value Retuned : ",details
            print "[TEST EXECUTION RESULT] : FAILURE\n"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        details = tdkTestObj.getResultDetails();
        print "ACTUAL RESULT : dsGetVersion call failed"
        print "Value Retuned : ",details
        print "[TEST EXECUTION RESULT] : FAILURE\n"

    obj.unloadModule("dshal");
else:
    print "Load module failed";
    obj.setLoadModuleStatus("FAILURE");


