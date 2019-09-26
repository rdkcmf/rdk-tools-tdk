##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
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
  <id>209</id>
  <version>1</version>
  <name>DS_GetAspect Ratio test_21</name>
  <primitive_test_id>57</primitive_test_id>
  <primitive_test_name>DS_GetAspectRatio</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test script Checks the aspect ratio supported of Video Output Port
Test Case ID : CT_DS_21.Note: This script will through exception when calling second time without restarting agent.This is an issue with DS.</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_21</test_case_id>
    <test_objective>Device Setting –  Checking the current Aspect Ratio  with available Aspect Ratio formats. </test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()
Host::getVideoOutputPort()
VideoOutputPort::Display::getAspectRatio()
VideoOutputPort::isDisplayConnected()
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>null</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent
2.Device_Settings_Agent will get the current Aspect Ratio.
3.Device_Settings_Agent will check for the current aspect Ratio with the list of available aspect Ratio formats.
4.Device_Settings_Agent will return SUCCESS or FAILURE based on the result from the above step(3rd). 
</automation_approch>
    <except_output>Checkpoint 1. Check the current aspect Ratio present in the list of available aspect Ratio formats.</except_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_VOP_isDisplayConnected
TestMgr_DS_VOP_getAspectRatio
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_GetAspect Ratio test_21</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_DS_21');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS :Application successfully initialized with Device Settings library";
                #calling DS_IsDisplayConnectedStatus function to check for display connection status
                tdkTestObj = obj.createTestStep('DS_IsDisplayConnectedStatus');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                displaydetails = tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of DS_IsDisplayConnectedStatus
                if (expectedresult in actualresult) and ("TRUE" in displaydetails):
                        print "Display= %s" %displaydetails;
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS:Display connection status verified";
                        #calling DS_GetAspectRatio to get the aspect ratio
                        tdkTestObj = obj.createTestStep('DS_GetAspectRatio');
                        tdkTestObj.addParameter("port_name","HDMI0");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        aspectRatiodetails = tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of DS_GetAspectRatio
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Application gets the Aspect ratio";
                                #just printing the AspectRatio
                                print aspectRatiodetails;
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE:Application fails to get the Aspect Ratio of display device";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE:'vPort.isDisplayConnected' API returns success but the display device is not connected with STB hence this test scenario fails.";
                #calling DS_ManagerDeInitialize to DeInitialize API
                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully DeInitialized the DeviceSetting library";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Deinitalize failed" ;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Device Setting Initialize failed";
        print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
