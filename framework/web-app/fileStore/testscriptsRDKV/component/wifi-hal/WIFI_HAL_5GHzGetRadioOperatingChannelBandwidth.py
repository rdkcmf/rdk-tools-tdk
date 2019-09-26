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
  <version>5</version>
  <name>WIFI_HAL_5GHzGetRadioOperatingChannelBandwidth</name>
  <primitive_test_id/>
  <primitive_test_name>WIFI_HAL_GetOrSetParamStringValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To get the Operating bandwidth for 5GHz and check whether it is in valid range or not.</synopsis>
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
    <test_case_id>TC_WIFI_HAL_4</test_case_id>
    <test_objective>To get the Operating bandwidth for 5GHz and check whether it is in valid range or not.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>IPClient-Wifi</test_setup>
    <pre_requisite>1.Ccsp Components  should be in a running state else invoke cosa_start.sh manually that includes all the ccsp components and TDK Component
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>wifi_getRadioOperatingChannelBandwidth()
wifi_connectEndpoint()</api_or_interface_used>
    <input_parameters>methodName : getRadioOperatingChannelBandwidth
radioIndex : 1</input_parameters>
    <automation_approch>1.Load the module.
2.Check if the DUT is connected to the required SSID, if not do the connection using wifi_connectEndpoint().
3.Get the operating channel bandwidth by invoking wifi_getRadioOperatingChannelBandwidth() api.
4.If the operating channel bandwidth is within the valid range,return SUCCESS,else FAILURE.
5.Unload the module.</automation_approch>
    <except_output>The operating channel bandwidth must be within the valid range.</except_output>
    <priority>High</priority>
    <test_stub_interface>WIFI_HAL</test_stub_interface>
    <test_script>WIFI_HAL_5GHzGetRadioOperatingChannelBandwidth</test_script>
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
sysObj = tdklib.TDKScriptingLibrary("sysutil","RDKB");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'WIFI_HAL_5GHzGetRadioOperatingChannelBandwidth');
sysObj.configureTestCase(ip,port,'WIFI_HAL_5GHzGetRadioOperatingChannelBandwidth');

#Get the result of connection with test component and DUT
loadmodulestatus1 =obj.getLoadModuleResult();
loadmodulestatus2 =sysObj.getLoadModuleResult();

if "SUCCESS" in loadmodulestatus1.upper() and loadmodulestatus2.upper():
    obj.setLoadModuleStatus("SUCCESS");
    sysObj.setLoadModuleStatus("SUCCESS");
    radioIndex = 1
    connectresult = isConnectedtoSSID(obj,sysObj,radioIndex);
    if "TRUE" in connectresult:
        #Script to load the configuration file of the component
        tdkTestObj = obj.createTestStep("WIFI_HAL_GetOrSetParamStringValue");
        #Giving the method name to invoke the api for radio operating channel bandwidth. ie,wifi_getRadioOperatingChannelBandwidth()
        tdkTestObj.addParameter("methodName","getRadioOperatingChannelBandwidth");
        #Radio index is 0 for 2.4GHz and 1 for 5GHz
        tdkTestObj.addParameter("radioIndex",1);
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        #Expected operating bandwidth list:NULL if not connected
        ExpectedList = ["20MHz", "40MHz", "80MHz", "80+80", "160", "NULL"];
        if expectedresult in actualresult :
    	    Bandwidth= details.split(":")[1].strip(" ");
            print Bandwidth;
    	    if Bandwidth in ExpectedList:
                #Set the result status of execution
                tdkTestObj.setResultStatus("SUCCESS");
                print "TEST STEP 1: Get the Radio operating channel bandwidth for 5GHz";
                print "EXPECTED RESULT 1: Should get the Radio operating channel bandwidth from the expected list for 5GHz";
                print "ACTUAL RESULT 1: %s" %Bandwidth;
                #Get the result of execution
                print "[TEST EXECUTION RESULT] : SUCCESS";
    	    else:
	        tdkTestObj.setResultStatus("FAILURE");
    	        print "Operating Channel bandwidth is not from the expected list for 5GHz"
        else:
	    #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE");
            print "TEST STEP 1: Get the Radio operating channel bandwidth for 5GHz";
            print "EXPECTED RESULT 1: Should get the Radio operating channel bandwidth for 5GHz";
            print "ACTUAL RESULT 1: %s" %Bandwidth;
            #Get the result of execution
            print "[TEST EXECUTION RESULT] : FAILURE";
    else:
        print "Connecting to SSID operation failed"

    obj.unloadModule("wifihal");
    sysObj.unloadModule("sysutil");
else:
    print "Failed to load the module";
    sysObj.setLoadModuleStatus("FAILURE");
    obj.setLoadModuleStatus("FAILURE");
    print "Module loading failed";

