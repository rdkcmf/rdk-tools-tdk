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
  <id>656</id>
  <version>1</version>
  <name>DS_Resolution_STRESS_test_112</name>
  <primitive_test_id>83</primitive_test_id>
  <primitive_test_name>DS_SetResolution</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test is to successfully change the Resolution format  continuously for every 100ms repeatedly for x times.				
Test case ID : CT_DS_112</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
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
    <test_case_id>CT_DS_112</test_case_id>
    <test_objective>Device Setting –  Get and Set the supported display Resolution continuously for every 100ms repeatedly for x times.</test_objective>
    <test_type>Positive(Stress)</test_type>
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
E.g.: 480i.</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get the list resolution supported by a given port.
3.Device_Settings_Agent will get the default resolution supported by a given port.
4.Device_Settings_Agent will get the status of display connection.
5.Device_Settings_Agent will get the display resolution.
6. Device_Settings_Agent will set the new display resolution.
7. Device_Settings_Agent will check for the new display resolution 
8.Device_Settings_Agent will wait for 100 ms and change to another resolution and verify the change.
9. The steps 5-8 will be repeated for 100 times and check the successful change of resolution and store the result.
10.Device_Settings_Agent will return SUCCESS or FAILURE based on the result. 
</automation_approch>
    <except_output>
Checkpoint 1. Check the display connection status with “Connected” status.

Checkpoint 2. Check the display Resolution value before and after setting it.
Checkpoint 3. Check for the presence of the defaultResoultion and current resolution in the list of supported resolutions.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_HOST_Resolutions
TestMgr_DS_VOP_setResolution
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_Resolution_STRESS_test_112</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_DS_112');
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
                        i = 0;
                        for i in range(0,100):
                            print "****************%d" %i;
                            #calling DS_SetResolution to set and get the display resolutions
                           
                            resolution="480i";
                            print "Resolution value set to:%s" %resolution;
                            if resolution in resolutiondetails:
                                    tdkTestObj = obj.createTestStep('DS_SetResolution');
                                    tdkTestObj.addParameter("resolution",resolution);
                                    tdkTestObj.addParameter("port_name","HDMI0");
                                    expectedresult="SUCCESS"
                                    tdkTestObj.executeTestCase(expectedresult);
                                    actualresult = tdkTestObj.getResult();
                                    resolutiondetails1 = tdkTestObj.getResultDetails();
                                    #Check for SUCCESS/FAILURE return value of DS_SetResolution
                                    if expectedresult in actualresult:
                                        print "SUCCESS:set and get resolution Success";
                                        print "getresolution %s" %resolutiondetails1;
                                        #comparing the resolution before and after setting
                                        if resolution in resolutiondetails1 :
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print "SUCCESS: Both the resolutions are same";
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print "FAILURE: Both the resolutions are not same";
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "****************%d" %i;
                                        print "FAILURE:set and get resolution fails";
                            else:
                                    print "FAILURE:Requested resolution are not supported by this device";            
                            time.sleep(100/1000);
                            #calling DS_SetResolution to set and get the display resolutions
                            
                            resolution="720p";
                            print "Resolution value set to:%s" %resolution;
                            if resolution in resolutiondetails:
                                tdkTestObj = obj.createTestStep('DS_SetResolution');
                                tdkTestObj.addParameter("resolution",resolution);
                                tdkTestObj.addParameter("port_name","HDMI0");
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                resolutiondetails2 = tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value of DS_SetResolution
                                if expectedresult in actualresult:
                                    print "SUCCESS:set and get resolution Success";
                                    print "getresolution %s" %resolutiondetails2;
                                    #comparing the resolution before and after setting
                                    if resolution in resolutiondetails2 :
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print "SUCCESS: Both the resolutions are same";
                                    else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print "FAILURE: Both the resolutions are not same";
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "****************%d" %i;
                                    print "FAILURE:set and get resolution fails";                        
                            else:
                                print "FAILURE:Requested resolution are not supported by this device";        
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE :Failed to get the list of supported resolutions";                
                
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
