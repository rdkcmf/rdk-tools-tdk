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
  <id>1600</id>
  <version>2</version>
  <name>DS_Resolution_PortStateChange_120</name>
  <primitive_test_id>83</primitive_test_id>
  <primitive_test_name>DS_SetResolution</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Check resolution value change after HDMI port disable/enable.
TestcaseID: CT_DS120</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.2</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS120</test_case_id>
    <test_objective>Check resolution value change after HDMI port disable/enable</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1/XI3-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize() 
device::VideoOutputPort::setResolution
device::VideoOutputPort::getResolution
device::VideoOutputPort::enable
device::VideoOutputPort::disable
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>string resolution="1080i"
string port_name="HDMI0"
integer get_only (0,1)
integer enable(0,1)</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2. Device_Settings_Agent will set the new display resolution.
3. Device_Settings_Agent will set the video output port to disable and then enable 
4. Device_Settings_Agent will check for the display resolution and will return SUCCESS or FAILURE based on the value set in step 2</automation_approch>
    <except_output>Checkpoint 1 Check for return value of the resolution before and after HDMI port disable/enable</except_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_VOP_setResolution
TestMgr_DS_VOP_setEnable
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_Resolution_PortStateChange_120</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>XONE-15300 </remarks>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import devicesettings;

#Test component to be tested
dsObj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
dsObj.configureTestCase(ip,port,'DS_Resolution_PortStateChange_120');
loadmodulestatus =dsObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        dsObj.setLoadModuleStatus("SUCCESS");

        #Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(dsObj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Calling DS_IsDisplayConnectedStatus function to check for display connection status
                result = devicesettings.dsIsDisplayConnected(dsObj)
                if "TRUE" in result:
                    #Save a copy of current resolution
                    copyResolution = devicesettings.dsGetResolution(dsObj,"SUCCESS",kwargs={'portName':"HDMI0"});

                    #Get the resolution list supported by TV.
                    print "Get list of resolutions supported on HDMI0"

                    tdkTestObj = dsObj.createTestStep('DS_Resolution');
                    tdkTestObj.addParameter("port_name","HDMI0");
                    expectedresult = "SUCCESS"
                    #Execute the test case in STB
                    tdkTestObj.executeTestCase(expectedresult);
                    #Get the result of execution
                    result = tdkTestObj.getResult();
                    supportedResolutions = tdkTestObj.getResultDetails();
                    print "Result: [%s] Details: [%s]"%(result,supportedResolutions)
                    #Set the result status of execution
                    if expectedresult in result:
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");

                    list = supportedResolutions.split(":");
                    resolutionList = list[1].split(",");

                    for resolution in resolutionList:
                        if resolution != copyResolution:
                                print "Setting resolution to ",resolution
                                devicesettings.dsSetResolution(dsObj,"SUCCESS",kwargs={'portName':"HDMI0",'resolution':resolution});
                                break;
                        else:
                                print "Resolution value already at ",resolution;

                    #calling Device Settings - Set Port to disable
                    tdkTestObj = dsObj.createTestStep('DS_SetEnable');
                    enable=0;
                    print "Setting Port enable to %d" %enable;
                    tdkTestObj.addParameter("enable",enable);
                    tdkTestObj.addParameter("port_name","HDMI0");
                    expectedresult="SUCCESS";
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    print "[Port Disable RESULT] : %s" %actualresult;
                    enabledetails = tdkTestObj.getResultDetails();
                    print "Port Disable Details: %s"%enabledetails;
                    #Check for SUCCESS/FAILURE return value of DS_SetEnable
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");

                    #calling Device Settings - Set Port to enable
                    tdkTestObj = dsObj.createTestStep('DS_SetEnable');
                    enable=1
                    print "Setting Port enable to %d" %enable;
                    tdkTestObj.addParameter("enable",enable);
                    tdkTestObj.addParameter("port_name","HDMI0");
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    print "[Port Enable RESULT] : %s" %actualresult;
                    details = tdkTestObj.getResultDetails();
                    print "[Port Enable Details]: %s"%details;
                    #Check for SUCCESS/FAILURE return value of DS_SetEnable
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");

                    #calling Device Setting -Get Resolution
                    tdkTestObj = dsObj.createTestStep('DS_SetResolution');
                    print "Resolution before enable:%s" %resolution;
                    tdkTestObj.addParameter("port_name","HDMI0");
                    tdkTestObj.addParameter("get_only",1);
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    print "[DS GetResolution RESULT] : %s" %actualresult;
                    getResolution = tdkTestObj.getResultDetails();
                    print "getResolution:%s" %getResolution;
                    #Check for SUCCESS/FAILURE return value of DS_SetResolution
                    if expectedresult in actualresult:
                        #comparing the resolution before and after port enabling
                        if resolution == getResolution :
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Resolution same after port disable/enable";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "SUCCESS: Resolution changed after port disable/enable";
                    else:
                        tdkTestObj.setResultStatus("FAILURE");

                    #Revert to original value of resolution unless original value was already 1080i
                    if resolution not in copyResolution:
                        devicesettings.dsSetResolution(dsObj,"SUCCESS",kwargs={'portName':"HDMI0",'resolution':copyResolution});
                else:
                    print "Display Device NOT Connected to execute test";

                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = devicesettings.dsManagerDeInitialize(dsObj)

        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        dsObj.setLoadModuleStatus("FAILURE");
