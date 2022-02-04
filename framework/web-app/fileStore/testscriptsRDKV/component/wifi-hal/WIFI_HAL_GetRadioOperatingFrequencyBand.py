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
  <version>6</version>
  <name>WIFI_HAL_GetRadioOperatingFrequencyBand</name>
  <primitive_test_id/>
  <primitive_test_name>WIFI_HAL_GetOrSetParamStringValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To get the radio Operating frequency band and check whether it is from the list of radio Supported frequency bands.</synopsis>
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
    <test_case_id>TC_WIFI_HAL_14</test_case_id>
    <test_objective>To get the radio Operating frequency band and check whether it is from the list of radio Supported frequency bands.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>IPClient-Wifi,Video_Accelerator</test_setup>
    <pre_requisite>1.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>wifi_getRadioSupportedFrequencyBands()
wifi_getRadioOperatingFrequencyBand()
wifi_connectEndpoint()</api_or_interface_used>
    <input_parameters>methodName : getRadioSupportedFrequencyBands
methodName : getRadioOperatingFrequencyBand
radioIndex : 1</input_parameters>
    <automation_approch>1.Load the module.
2.Check if the DUT is connected to the required SSID, if not do the connection using wifi_connectEndpoint().
3.Invoke wifi_getRadioSupportedFrequencyBands() api to get the list of radio supported frequency bands.
4.Invoke wifi_getRadioOperatingFrequencyBand() api to get the current radio operating frequency band and check whether it is from the list of radio supported frequency bands.
5.If yes,return SUCCESS,else FAILURE.
6.Unload the module.</automation_approch>
    <except_output>To get the Radio Operating frequency band and the value should be from the list of Radio Supported Frequency bands.</except_output>
    <priority>High</priority>
    <test_stub_interface>WIFI_HAL</test_stub_interface>
    <test_script>WIFI_HAL_GetRadioOperatingFrequencyBand</test_script>
    <skipped>No</skipped>
    <release_version>M61</release_version>
    <remarks/>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
  </script_tags>
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
obj.configureTestCase(ip,port,'WIFI_HAL_GetRadioOperatingFrequencyBand');

#Get the result of connection with test component and DUT
loadmodulestatus =obj.getLoadModuleResult();

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    radioIndex = 1
    connectresult = isConnectedtoSSID(obj,radioIndex);
    if "TRUE" in connectresult:
        #Script to load the configuration file of the component
        tdkTestObj = obj.createTestStep("WIFI_HAL_GetOrSetParamStringValue");
        #Giving the method name to invoke the api for getting Supported Frequency band. ie,wifi_getRadioSupportedFrequencyBands()
        tdkTestObj.addParameter("methodName","getRadioSupportedFrequencyBands");
        #Radio index is 0 for 2.4GHz and 1 for 5GHz
        tdkTestObj.addParameter("radioIndex",1);
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedresult in actualresult:
            SupportedFrequencyBands = details.split(":")[1].strip(" ");
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS");
            print "TEST STEP 1: Get the Radio Supported Frequency bands";
            print "EXPECTED RESULT 1: Should get the Radio Supported Frequency bands";
            print "ACTUAL RESULT 1: Supported Frequency Bands = ",SupportedFrequencyBands;
            #Get the result of execution
            print "[TEST EXECUTION RESULT] : SUCCESS";
            #Script to load the configuration file of the component
            tdkTestObj = obj.createTestStep("WIFI_HAL_GetOrSetParamStringValue");
            #Giving the method name to invoke the api for getting Operating Frequency band. ie,wifi_getRadioOperatingFrequencyBand()
            tdkTestObj.addParameter("methodName","getRadioOperatingFrequencyBand");
            #Radio index is 0 for 2.4GHz and 1 for 5GHz
            tdkTestObj.addParameter("radioIndex",1);
            expectedresult="SUCCESS";
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            if expectedresult in actualresult:
                OperatingFrequencyBand = details.split(":")[1].strip(" ");
                if OperatingFrequencyBand in SupportedFrequencyBands:
                    #Set the result status of execution
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "TEST STEP 2: Get the Radio Operating Frequency band";
                    print "EXPECTED RESULT 2: The Radio Operating Frequency band must be from the list of Supported Frequency Bands";
                    print "ACTUAL RESULT 2: The Radio Operating Frequency band is from the list of Supported Frequncy Bands"; 
                    print "Operating Frequency Band = ",OperatingFrequencyBand;
                    #Get the result of execution
                    print "[TEST EXECUTION RESULT] : SUCCESS";
                else:
                    #Set the result status of execution
                    tdkTestObj.setResultStatus("FAILURE");
                    print "TEST STEP 2: Get the Radio Operating Frequency band";
                    print "EXPECTED RESULT 2: The Radio Operating Frequency band must be from the list of Supported Frequency Bands";
                    print "ACTUAL RESULT 2: The Radio Operating Frequency band is not from the list of Supported Frequncy Bands";
                    print "Operating Frequency Band = ",OperatingFrequencyBand;
                    #Get the result of execution
                    print "[TEST EXECUTION RESULT] : FAILURE";
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "wifi_getRadioOperatingFrequencyBand() operation failed";
        else:
            #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE");
            print "TEST STEP 1: Get the Radio Supported Frequency bands";
            print "EXPECTED RESULT 1: Should get the Radio Supported Frequency bands";
            print "ACTUAL RESULT 1:  Supported Frequency Bands = ",SupportedFrequencyBands;
            #Get the result of execution
            print "[TEST EXECUTION RESULT] : FAILURE";
    else:
        print "Connecting to SSID operation failed"

    obj.unloadModule("wifihal");
else:
    print "Failed to load the module";
    obj.setLoadModuleStatus("FAILURE");
    print "Module loading failed";
