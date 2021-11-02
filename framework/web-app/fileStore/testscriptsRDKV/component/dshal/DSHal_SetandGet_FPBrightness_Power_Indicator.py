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
  <version>2</version>
  <name>DSHal_SetandGet_FPBrightness_Power_Indicator</name>
  <primitive_test_id/>
  <primitive_test_name>DSHal_SetFPBrightness</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To Set  and Get the Brigtness of Power indicator</synopsis>
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
    <test_case_id>CT_DS_HAL_53</test_case_id>
    <test_objective>To set the brightness of Power indicator and check using get method</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetFPBrightness(dsFPDIndicator_t eIndicator, dsFPDBrightness_t *pBrightness)
dsSetFPBrightness (dsFPDIndicator_t eIndicator, dsFPDBrightness_t eBrightness)</api_or_interface_used>
    <input_parameters>indicator - indicator index(0-4)
brightness -  brightness to be set (0-100)</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via the test agent.
2 . DSHAL agent will invoke the api dsGetFPBrightness to get the initial brightness of the indicator
3 . DSHAL agent will invoke the api dsSetFPBrightness to set the brightness to initial value + 10 (considering max brightness as 100)
4. DSHAL agent will invoke the api dsGetFPBrightness to get the brightness of the indicator
4. TM checks if the brightness is same as that set and return SUCCESS/FAILURE status..</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call is success
Checkpoint 2 Verify that the brightness is set</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_SetandGet_FPBrightness_Power_Indicator</test_script>
    <skipped>No</skipped>
    <release_version>M75</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import deviceCapabilities;
#Test component to be tested
dshalObj = tdklib.TDKScriptingLibrary("dshal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
dshalObj.configureTestCase(ip,port,'DSHal_SetandGet_FPBrightness_Power_Indicator');

#Get the result of connection with test component and STB
dshalloadModuleStatus = dshalObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %dshalloadModuleStatus;

#Check if devicesupports PowerIndicator
capable = deviceCapabilities.getconfig(dshalObj,"Indicator","Power");

if "SUCCESS" in dshalloadModuleStatus.upper() and capable:
    dshalObj.setLoadModuleStatus(dshalloadModuleStatus);
    expectedResult = "SUCCESS"
    #for power indicator the value is 1
    indicator_dict = {"Message":0,"Power":1,"Record":2,"Remote":3,"RFBypass":4}
    indicator_name = "Power"
    indicator = indicator_dict[indicator_name] 
    tdkTestObj = dshalObj.createTestStep('DSHal_GetFPBrightness');
    tdkTestObj.addParameter("indicator",indicator)
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        details = tdkTestObj.getResultDetails()
	print "initial brightness of {} indicator: {} ".format(indicator_name,details)
        brightness = (int(details)+ 10)%100
        #Prmitive test case which associated to this Script
        tdkTestObj = dshalObj.createTestStep('DSHal_SetFPBrightness');
        tdkTestObj.addParameter("indicator",indicator)
        tdkTestObj.addParameter("brightness",brightness)
    
        #Execute the test case in STB
	print "trying to set brightness to:",brightness
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        print "DSHAL_SetFPBrightness result: ",actualResult
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            details = tdkTestObj.getResultDetails();
            print details;
            #Prmitive test case which associated to this Script
            tdkTestObj = dshalObj.createTestStep('DSHal_GetFPBrightness');
            tdkTestObj.addParameter("indicator",indicator)
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                if int(details)== brightness:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Brightness of {} indicator is: {}".format(indicator_name,str(details))
		    print "Both values are same"
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Brightness of {} indicator not set to : {}".format(indicator_name,str(brightness))
                    print "Brightness of {} indicator : {} ".format(str(details))
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "DSHal_GetFPBrightness failed"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "DSHal_SetFPBrightness failed"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "DSHal_GetFPBrightness failed"

    dshalObj.unloadModule("dshal");

elif not capable and "SUCCESS" in dshalloadModuleStatus.upper():
    print "Exiting from script";
    dshalObj.setLoadModuleStatus("FAILURE");
    dshalObj.unloadModule("dshal");

else:
    print "Module load failed";
