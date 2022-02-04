##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2018 RDK Management
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
<?xml version="1.0" encoding="UTF-8"?>
<xml>
  <id/>
  <version>2</version>
  <name>WIFI_HAL_5GHzGetRadioChannelsInUse</name>
  <primitive_test_id/>
  <primitive_test_name>WIFI_HAL_GetOrSetParamStringValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test if the list returned by wifi_getRadioChannelsInUse() api for 5GHz is a subset of the list returned by wifi_getRadioPossibleChannels() for 5GHz</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-Wifi</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_WIFI_HAL_2</test_case_id>
    <test_objective>Test if the list returned by wifi_getRadioChannelsInUse() api for 5GHz is a subset of the list returned by wifi_getRadioPossibleChannels() for 5GHz.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>IPClient-Wifi,Video_Accelerator</test_setup>
    <pre_requisite>1.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>wifi_getRadioSupportedFrequencyBands()
wifi_getRadioPossibleChannels()
wifi_getRadioChannelsInUse()
</api_or_interface_used>
    <input_parameters>methodName:getRadioSupportedFrequencyBands
methodName : getRadioPossibleChannels
methodName : getRadioChannelsInUse
radioIndex  : 1</input_parameters>
    <automation_approch>1.Load the module.
2.Invoke wifi_getRadioSupportedFrequencyBands() to check whether 5GHz frequency band is supported.
2.If 5GHz band is supported, invoke wifi_getRadioPossibleChannels() api and get the list of radio possible channels for radio 1.
3.Invoke and wifi_getRadioChannelsInUse() api and get the list of radio channels in use for radio 1.
4.If the list returned by wifi_getRadioChannelsInUse() is a subset of list returned by wifi_getRadioPossibleChannels() return SUCCESS,else FAILURE.
5.Unload the module.</automation_approch>
    <expected_output>The channel in use must one of the value returned by possible channels</expected_output>
    <priority>High</priority>
    <test_stub_interface>WIFI_HAL</test_stub_interface>
    <test_script>WIFI_HAL_5GHzGetRadioChannelsInUse</test_script>
    <skipped>No</skipped>
    <release_version>M61</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkvWifiUtility;
from tdkvWifiUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("wifihal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'WIFI_HAL_5GHzGetRadioChannelsInUse');


#Get the result of connection with test component and DUT
loadmodulestatus =obj.getLoadModuleResult();

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    print "\nTEST STEP 1: To invoke the wifi_getRadioSupportedFrequencyBands() to get frequency bands";
    print "EXPECTED RESULT : Should get details of supported frequency bands";
    tdkTestObj = obj.createTestStep("WIFI_HAL_GetOrSetParamStringValue");
    tdkTestObj.addParameter("methodName","getRadioSupportedFrequencyBands");
    tdkTestObj.addParameter("radioIndex",1);
    expectedresult="SUCCESS";
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS");
        SupportedFrequencyBands = details.split(":")[1].strip(" ");
        print "ACTUAL RESULT : Supported Frequency Bands = ",SupportedFrequencyBands;
        if "5GHz" in SupportedFrequencyBands:
            #Script to load the configuration file of the component
            tdkTestObj = obj.createTestStep("WIFI_HAL_GetOrSetParamStringValue");
            #Giving the method name to invoke the api for getting possible Radio Channel. ie,wifi_getRadioPossibleChannels()
            tdkTestObj.addParameter("methodName","getRadioPossibleChannels");
            #Radio index is 0 for 2.4GHz and 1 for 5GHz
            tdkTestObj.addParameter("radioIndex",1);
            expectedresult="SUCCESS";
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            if expectedresult in actualresult:
                #Set the result status of execution
                tdkTestObj.setResultStatus("SUCCESS");
                print "TEST STEP 2: Get the possible Radio Channels for 5GHz";
                print "EXPECTED RESULT 2: Should get the possible Radio Channels for 5GHz";
                print "ACTUAL RESULT 2: %s" %details;
                #Get the result of execution
                print "[TEST EXECUTION RESULT] : SUCCESS";
                possibleCh = details.split(":")[1].strip();
                #Giving the method name to invoke the api for getting Radio Channel in use. ie,wifi_getRadioChannelsInUse()
                tdkTestObj.addParameter("methodName","getRadioChannelsInUse");
                #Radio index is 0 for 2.4GHz and 1 for 5GHz
                tdkTestObj.addParameter("radioIndex",1);
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                if expectedresult in actualresult :
                    print "TEST STEP 3: Get the possible Channels in use for 5GHz";
                    print "EXPECTED RESULT 3: Should get the Radio Channels in use for 5GHz";
                    print "ACTUAL RESULT 3: %s" %details;
                    chInUse = details.split(":")[1].strip();
                    flag = 1
                    for index in range(len(chInUse)):
                        if chInUse[index] not in possibleCh:
                            flag = 0;
                            break;
                    if flag == 1 :
                        #Set the result status of execution
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Channel in use is from the possible channel list for 5GHz";
                        #Get the result of execution
                        print "[TEST EXECUTION RESULT] : SUCCESS";
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "ERROR:Channel In use not from the possible channel list for 5GHz";
                        print "[TEST EXECUTION RESULT] : FAILURE";
                else:
                    #Set the result status of execution
                    tdkTestObj.setResultStatus("FAILURE");
                    print "TEST STEP 3: Get the possible Channels in use for 5GHz";
                    print "EXPECTED RESULT 3: Should get the Radio Channels in use for 5GHz";
                    print "ACTUAL RESULT 3: %s" %details;
                    #Get the result of execution
                    print "[TEST EXECUTION RESULT] : FAILURE";
            else:
                #Set the result status of execution
                tdkTestObj.setResultStatus("FAILURE");
                print "TEST STEP 2: Get the possible Radio Channels for 5GHz";
                print "EXPECTED RESULT 2: Should get the possible Radio Channels for 5GHz";
                print "ACTUAL RESULT 2: %s" %details;
                #Get the result of execution
                print "[TEST EXECUTION RESULT] : FAILURE";
        else:
            print "Frequency band 5GHz not supported : Skipping getRadioChannelsInUse validation"
            print "[TEST EXECUTION RESULT] : SUCCESS";
            tdkTestObj.setResultStatus("SUCCESS");
    else:
        print "wifi_getRadioSupportedFrequencyBands() operation failed"
        print "[TEST EXECUTION RESULT] : FAILURE"
        tdkTestObj.setResultStatus("FAILURE");

    obj.unloadModule("wifihal");
else:
    print "Failed to load the module";
    obj.setLoadModuleStatus("FAILURE");
    print "Module loading failed";
