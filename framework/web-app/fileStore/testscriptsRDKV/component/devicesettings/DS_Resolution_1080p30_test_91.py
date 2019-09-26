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
  <id>667</id>
  <version>1</version>
  <name>DS_Resolution_1080p30_test_91</name>
  <primitive_test_id>83</primitive_test_id>
  <primitive_test_name>DS_SetResolution</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test script Sets and gets the 1080p30 Resolution of Video Output Port
Test Case ID:CT_DS_91.
Note:This script will return duplicates, If running second time without restarting agent. Agent process may lead to crash/restart.This is an issue with DS</synopsis>
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
    <test_case_id>CT_DS_91</test_case_id>
    <test_objective>Device Setting –  Get and Set the display Resolution setting with 1080p30</test_objective>
    <test_type>Positive(Boundary condition)</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.
3.display device should be connected.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()
Host::getVideoOutputPort()
AudioOutputPort::getSupportedResolutions()
VideoOutputPort::getDfeaultResolution()
VideoOutputPort::setResolution(string)
VideoOutputPort::isDisplayConnected()
VideoOutputPort::getResolution()
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>setResolution: string -
E.g.: 1080p30</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get the list resolution supported by a given port.
3.Device_Settings_Agent will get the default resolution supported by a given port.
4.Device_Settings_Agent will get the status of display connection.
5.Device_Settings_Agent will get the display resolution.
6. Device_Settings_Agent will set the new display resolution.
7. Device_Settings_Agent will check for the new display resolution and will return SUCCESS or FAILURE based on the result. </automation_approch>
    <except_output>
Checkpoint 1. Check the display connection status with “Connected” status.

Checkpoint 2. Check the display Resolution value before and after setting it.
Checkpoint 3. Check for the presence of the defaultResoultion and current resolution in the list of supported resolutions.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_HOST_Resolutions
TestMgr_DS_VOP_setResolution
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_Resolution_1080p30_test_91</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>DS_Resolution_1080p30_test_91</remarks>
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
obj.configureTestCase(ip,port,'CT_DS_90');
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
                    #calling DS_Resolution get list of supported resolutions and the default resolution
                    tdkTestObj = obj.createTestStep('DS_Resolution');
                    tdkTestObj.addParameter("port_name","HDMI0");
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    resolutiondetails = tdkTestObj.getResultDetails();
                    #Check for SUCCESS/FAILURE return value of DS_Resolution
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully gets the list of supported and default resolutions";
                        print "%s" %resolutiondetails;
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE :Failed to get the list of supported resolutions";
                    #calling DS_SetResolution to set and get the display resolution as 1080i50    
                    resolution="1080p30";
                    print "Resolution value set to:%s" %resolution;
                    if resolution in resolutiondetails:
                        tdkTestObj = obj.createTestStep('DS_SetResolution');
                        tdkTestObj.addParameter("resolution",resolution);
                        tdkTestObj.addParameter("port_name","HDMI0");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        resolutiondetails = tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of DS_SetResolution
                        if expectedresult in actualresult:
                                print "SUCCESS:set and get resolution Success";
                                print "getresolution %s" %resolutiondetails;
                                #comparing the resolution before and after setting
                                if resolution in resolutiondetails :
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the resolutions are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Both the resolutions are not same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE:set and get resolution fails";
                    else:
                        print "FAILURE:Requested resolution are not supported by this device";
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
                    print "FAILURE:Connection Failed";
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
