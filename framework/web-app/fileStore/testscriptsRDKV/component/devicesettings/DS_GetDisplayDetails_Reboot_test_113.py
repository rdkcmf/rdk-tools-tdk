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
  <id>672</id>
  <version>2</version>
  <name>DS_GetDisplayDetails_Reboot_test_113</name>
  <primitive_test_id>55</primitive_test_id>
  <primitive_test_name>DS_DisplayDetails</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test script compares the display details of Video Output Port before and after rebooting the STB
Test Case ID : CT_DS_113</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS113</test_case_id>
    <test_objective>Device Setting –  Listing display details before and after rebooting the device</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.
3.Agent executable should be up and from startup.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()
Host::getVideoOutputPort()
VideoOutputPort::getDisplay()
VideoOutputPort::isDisplayConnected()
VideoOutputPort::getManufacturerWeek()
VideoOutputPort::getManufacturerYear()
VideoOutputPort::getProductCode()
VideoOutputPort::getSerialNumber()
device::Manager::DeInitialize()
</api_or_interface_used>
    <input_parameters>null</input_parameters>
    <automation_approch>1.TM loads the Device_Settings_Agent via the test agent 
2.Device_Settings_Agent will list the details about videoOutputPort before rebooting the box.
3.TM issues command to reboot the device.
4.Device_Settings_Agent will list the details about VOP after rebooting the box.
5.TM will get the two list and compare both are same.
6.Depends on result of above 5th step TM will return success or failure.</automation_approch>
    <except_output>Checkpoint 1 Check for return value of the APIs.
Checkpoint 2 Check for the list before and after the reboot.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_VOP_isDisplayConnected
TestMgr_DS_VOP_getDisplayDetails
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_GetDisplayDetails_Reboot_test_113</test_script>
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
obj.configureTestCase(ip,port,'CT_DS_113');
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
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS:Display connection status verified";
                        #calling DS_GetDisplayDetails to get the
                        tdkTestObj = obj.createTestStep('DS_DisplayDetails');
                        tdkTestObj.addParameter("port_name","HDMI0");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        displaydetailsBefore = tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of DS_GetDisplayDetails
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Application list the details of display device";
                                #printing list of device details
                                print displaydetailsBefore;
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE:Application fails to display the details of display device";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE:'vPort.isDisplayConnected' API returns success but the display device is not connected with STB hence this test scenario fails.";
        obj.initiateReboot();
        #------------------After Reboot----------#
        print "#------------------After Reboot----------#";

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
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS:Display connection status verified";
                        #calling DS_GetDisplayDetails to get the
                        tdkTestObj = obj.createTestStep('DS_DisplayDetails');
                        tdkTestObj.addParameter("port_name","HDMI0");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        displaydetailsAfter = tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of DS_GetDisplayDetails
                        if expectedresult in actualresult:
                                print "SUCCESS: Application list the details of display device";
                                if displaydetailsAfter == displaydetailsBefore:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Success: The display list are same before and after rebooting the device";
                                        #printing list of device details
                                        print displaydetailsAfter;
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: The display list are not same before and after rebooting the device";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE:Application fails to display the details of display device";

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
