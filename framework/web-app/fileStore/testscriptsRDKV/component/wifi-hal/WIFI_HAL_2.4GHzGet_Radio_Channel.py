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
  <version>1</version>
  <name>WIFI_HAL_2.4GHzGet_Radio_Channel</name>
  <primitive_test_id/>
  <primitive_test_name>WIFI_HAL_GetOrSetParamStringValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To get the current radio channel for 2.4GHz</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-Wifi</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_WIFI_HAL_28</test_case_id>
    <test_objective>Test if the list returned by wifi_getRadioChannel() api for 2.4GHz is a subset of the list returned by wifi_getRadioPossibleChannels() for 2.4GHz.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>IPClient-Wifi</test_setup>
    <pre_requisite>1.Ccsp Components  should be in a running state else invoke cosa_start.sh manually that includes all the ccsp components and TDK Component
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>wifi_getRadioPossibleChannels()
wifi_getRadioChannel()
wifi_connectEndpoint()
</api_or_interface_used>
    <input_parameters>methodName : getRadioPossibleChannels
methodName : getRadioChannel
radioIndex  : 0</input_parameters>
    <automation_approch>1.Load the module.
2.Check if the DUT is connected to the required SSID, if not do the connection using wifi_connectEndpoint().
3.Using WIFI_HAL_GetOrSetParamStringValue, invoke wifi_getRadioPossibleChannels() api and get the list of radio possible channels for radio 0.
4.Using WIFI_HAL_GetOrSetParamULongValue, invoke wifi_getRadioChannel() api and get the list of radio channels in use for radio 0
5.If the value returned by wifi_getRadioChannel() is a subset of list returned by wifi_getRadioPossibleChannels() return SUCCESS,else FAILURE.
6.Unload the module.</automation_approch>
    <except_output>The channel must be one of the value returned by possible channels</except_output>
    <priority>High</priority>
    <test_stub_interface>wifihal</test_stub_interface>
    <test_script>WIFI_HAL_2.4GHzGet_Radio_Channel</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkvWifiUtility;
from tdkvWifiUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("wifihal","1");
sysObj = tdklib.TDKScriptingLibrary("sysutil","RDKB");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'WIFI_HAL_2.4GHzGetRadioChannel');
sysObj.configureTestCase(ip,port,'WIFI_HAL_2.4GHzGetRadioChannel');

#Get the result of connection with test component and DUT
loadmodulestatus1 =obj.getLoadModuleResult();
loadmodulestatus2 =sysObj.getLoadModuleResult();

if "SUCCESS" in loadmodulestatus1.upper() and loadmodulestatus2.upper():
    obj.setLoadModuleStatus("SUCCESS");
    sysObj.setLoadModuleStatus("SUCCESS");
    radioIndex = 0
    connectresult = isConnectedtoSSID(obj,sysObj,radioIndex);
    if "TRUE" in connectresult:
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('WIFI_HAL_GetOrSetParamStringValue');
        #Giving the method name to invoke the api for getting the possible channels, wifi_getRadioPossibleChannels()
        tdkTestObj.addParameter("methodName","getRadioPossibleChannels");
        #Radio index is 0 for 2.4GHz and 1 for 5GHz
        tdkTestObj.addParameter("radioIndex",0);
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedresult in actualresult:
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS");
            print "TEST STEP 1: Get the possible radio channels"
            print "EXPECTED RESULT 1: Should get the possible radio channels for 2.4GHz"
            print "ACTUAL RESULT 1: %s" %details

            if details.split(":")[1].strip() != "":
                #if possible channels are given as 1-11
                if "-" in details:
                    #get the possible channels as a list of integers
                    PossibleChannelRange = [int(x) for x in details.split(":")[1].split("-")];
                    print PossibleChannelRange
                    PossibleChannels = range(PossibleChannelRange[0],PossibleChannelRange[1]+1);
                    print "Possible channels are ", PossibleChannels;
                #if possible channels are given as values eg:1,2,3,4,5
                else:
                    #get the possible channels as a list of integers
                    PossibleChannels = [int(x) for x in details.split(":")[1].split(",")];
                    print "Possible channels are ", PossibleChannels;

                #Prmitive test case which associated to this Script
                tdkTestObj = obj.createTestStep('WIFI_HAL_GetOrSetParamULongValue');
                #Giving the method name to invoke the api for getting the current radio channel, wifi_getRadioChannel()
                tdkTestObj.addParameter("methodName","getRadioChannel");
                #Radio index is 0 for 2.4GHz and 1 for 5GHz
                tdkTestObj.addParameter("radioIndex",0);
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                print details
                if expectedresult in actualresult:
                    radioCh = details.split(":")[1].strip;
                    if int(radioCh) in PossibleChannels:
                        #Set the result status of execution
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "TEST STEP 2: Get the Radio channel present in possible channel list"
                        print "EXPECTED RESULT 2: Should get the Radio channel present in possible channel list"
                        print "ACTUAL RESULT 2: %s" %details
                        #Get the result of execution
                        print "[TEST EXECUTION RESULT] : SUCCESS";
                    else:
                        #Set the result status of execution
                        tdkTestObj.setResultStatus("FAILURE");
                        print "TEST STEP 2: Get the Radio channel present in possible channel list"
                        print "EXPECTED RESULT 2: Should get the Radio channel present in possible channel list"
                        print "ACTUAL RESULT 2: %s" %details
                        #Get the result of execution
                        print "[TEST EXECUTION RESULT] : FAILURE";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "wifi_getRadioChannel() call failed"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "wifi_getRadioPossibleChannels() returned NULL instead of channel list"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "wifi_getRadioPossibleChannels() call failed"
    else:
        print "Connecting to SSID operation failed"

    obj.unloadModule("wifihal");
    sysObj.unloadModule("sysutil");
else:
    print "Failed to load the module";
    sysObj.setLoadModuleStatus("FAILURE");
    obj.setLoadModuleStatus("FAILURE");
    print "Module loading failed";

