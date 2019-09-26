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
  <id/>
  <version>1</version>
  <name>DS_VideoOutputPort_getVideoResolution_192</name>
  <primitive_test_id/>
  <primitive_test_name>DS_VOPCONFIG_getVideoResolution</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This tests API used to get a list of supported Video Resolutions by the port type.
TestcaseID: CT_DS192</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>IPClient-4</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_192</test_case_id>
    <test_objective>This tests API used to get a list of supported Video Resolutions by the port type.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>const VideoResolution   &amp;getVideoResolution (int id)</api_or_interface_used>
    <input_parameters>int port_id (0)</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get the video resolution of video output port.
3.Device_Settings_Agent will check if video resolution of video output port is retrievd successfully.
4.Device_Settings_Agent will return SUCCESS or FAILURE based on the result from the above step</automation_approch>
    <except_output>Checkpoint 1. Check if video resolution of video output port is retrievd successfully</except_output>
    <priority>High</priority>
    <test_stub_interface>none</test_stub_interface>
    <test_script>DS_VideoOutputPort_getVideoResolution_192</test_script>
    <skipped>No</skipped>
    <release_version>M27</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import devicesettings;

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

#Load module to be tested
dsObj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
dsObj.configureTestCase(ip,port,'DS_VideoOutputPort_getVideoResolution_192');
dsLoadStatus = dsObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %dsLoadStatus ;
#Set the module loading status
dsObj.setLoadModuleStatus(dsLoadStatus);

if "SUCCESS" in dsLoadStatus.upper():
        #Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(dsObj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Check for display connection status
                result = devicesettings.dsIsDisplayConnected(dsObj)
                if "TRUE" in result:
                        tdkTestObj = dsObj.createTestStep('DS_HOST_getVideoOutputPorts');
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details = tdkTestObj.getResultDetails();
                        print "[TEST EXECUTION RESULT] : %s" %actualresult;
                        print "Details: [%s]"%details;
                        if "SUCCESS" in actualresult.upper():
                                #Primitive test case which associated to this Script
                                tdkTestObj = dsObj.createTestStep('DS_VOPCONFIG_getVideoResolution');
                                portList = details.split(",")
                                for port_id in range (0,len(portList)):
                        		#Invoke primitive testcase
                        		tdkTestObj.addParameter("port_id",port_id);
                        		expectedresult="SUCCESS"
                        		tdkTestObj.executeTestCase(expectedresult);
                        		actualresult = tdkTestObj.getResult();
                        		details = tdkTestObj.getResultDetails();
                        		print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,actualresult)
                        		print "PortId: %d VideoResolution: %s"%(port_id,details);
                        		#Check for SUCCESS/FAILURE return value
                        		if expectedresult in actualresult:
                            			tdkTestObj.setResultStatus("SUCCESS");
                        		else:
                            			tdkTestObj.setResultStatus("FAILURE");
			else:
				tdkTestObj.setResultStatus("FAILURE");
				print "Failed to get VideoOutputPorts"
                else:
                        print "Display device not connected. Skipping testcase"
                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = devicesettings.dsManagerDeInitialize(dsObj)
        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");
