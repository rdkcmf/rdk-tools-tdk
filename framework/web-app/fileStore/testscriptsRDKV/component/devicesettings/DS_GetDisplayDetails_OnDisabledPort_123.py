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
  <id>1599</id>
  <version>4</version>
  <name>DS_GetDisplayDetails_OnDisabledPort_123</name>
  <primitive_test_id>657</primitive_test_id>
  <primitive_test_name>DS_SetEnable</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Verify that EDID value is retrieved even when HDMI port is connected and disabled. In order to disable fetching of display details manual plugout of HDMI is required.
TestcaseID: CT_DS123</synopsis>
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
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS123</test_case_id>
    <test_objective>Verify that EDID value is not retrieved when HDMI is plugged out. Verify that EDID value is retrieved even when HDMI port is connected and disabled.</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XG1-1/XI3-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize() 
device::VideoOutputPort::enable
device::VideoOutputPort::disable
device::VideoOutputPort::getDisplay()::getManufacturerWeek()
device::VideoOutputPort::getDisplay()::getManufacturerYear()
device::VideoOutputPort::getDisplay()::getProductCode()
device::VideoOutputPort::getDisplay()::getSerialNumber()
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>integer enable(0,1)
string port_name="HDMI0"</input_parameters>
    <automation_approch>1.TM loads the Device_Settings_Agent via the test agent 
2. Set the Videooutput port to disable and get the details about the videoOutputPort.
3. Set the Videooutput port to enable and get the details about the videoOutputPort.
4.Device_Settings_Agent will list the details about videoOutputPort.</automation_approch>
    <except_output>Checkpoint 1 Check for return value of the devicedetails after port disable / enable .</except_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_VOP_setEnable
TestMgr_DS_VOP_getDisplayDetails
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_GetDisplayDetails_OnDisabledPort_123</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>XITHREE-721 </remarks>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import devicesettings;

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
obj.configureTestCase(ip,port,'DS_GetDisplayDetails_OnDisabledPort_123');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
        #Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(obj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Check for display connection status
                result = devicesettings.dsIsDisplayConnected(obj)
                if "TRUE" in result:
                    #calling Device Settings - Set Port to disable
                    tdkTestObj = obj.createTestStep('DS_SetEnable');
                    enable=0
                    print "Setting Port enable to %d" %enable;
                    tdkTestObj.addParameter("enable",enable);
                    tdkTestObj.addParameter("port_name","HDMI0");
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    print "[Port Disable RESULT] : %s" %actualresult;
                    details = tdkTestObj.getResultDetails();
                    print "Port Disable Details: %s"%details;
                    #Check for SUCCESS/FAILURE return value of DS_SetEnable
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");

                    # Get DisplayDetails after port disable
                    tdkTestObj = obj.createTestStep('DS_DisplayDetails');
                    tdkTestObj.addParameter("port_name","HDMI0");
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    print "[GetPortDisplayDetails RESULT] : %s" %actualresult;
                    displaydetails = tdkTestObj.getResultDetails();
                    print "[PortDisplayDetails]: %s"%displaydetails;
                    #Check for SUCCESS/FAILURE return value of DS_GetDisplayDetails
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");

                    #calling Device Settings - Set Port to enable
                    tdkTestObj = obj.createTestStep('DS_SetEnable');
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

                    # Get DisplayDetails after port enable
                    tdkTestObj = obj.createTestStep('DS_DisplayDetails');
                    tdkTestObj.addParameter("port_name","HDMI0");
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    print "[GetPortDisplayDetails RESULT] : %s" %actualresult;
                    displaydetails = tdkTestObj.getResultDetails();
                    print "[PortDisplayDetails]: %s"%displaydetails;
                    #Check for SUCCESS/FAILURE return value of DS_GetDisplayDetails
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                else:
                    # Get DisplayDetails when HDMI display is not connected
                    tdkTestObj = obj.createTestStep('DS_DisplayDetails');
                    tdkTestObj.addParameter("port_name","HDMI0");
                    expectedresult="FAILURE"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    print "[GetPortDisplayDetails RESULT] : %s" %actualresult;
                    displaydetails = tdkTestObj.getResultDetails();
                    print "[PortDisplayDetails]: %s"%displaydetails;
                    #Check for SUCCESS/FAILURE return value of DS_GetDisplayDetails
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");

                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = devicesettings.dsManagerDeInitialize(obj)

        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
