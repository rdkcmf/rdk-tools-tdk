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
  <version>2</version>
  <name>DS_getSPDIF_SURROUND_AfterReboot_139</name>
  <primitive_test_id/>
  <primitive_test_name>DS_SetStereoMode</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>CT_DS_139-DS_getSPDIF_SURROUND_AfterReboot_139- This test tries to get the value of SPDIF after setting to STEREO and rebooting the device</synopsis>
  <groups_id/>
  <execution_time>8</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_139</test_case_id>
    <test_objective>Device Setting –  This test tries to get the value of SPDIF after setting to STEREO and rebooting the device</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize()
Host::getVideoOutputPort()
Host::getAudioOutputPort()
AudioOutputPort::getSupportedStereoModes()
AudioOutputPort::getStereoMode()
AudioOutputPort::setStereoMode(string)
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>setStereoMode : string
E.g.: STEREO
</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get the supported stereo modes.
3.Device_Settings_Agent will get the current stereo format.
4.Device_Settings_Agent will set new stereo format to STEREO.
5. Reboot the DUT.
6.Device_Settings_Agent will get the current stereo format.
7.Device_Settings_Agent will check the current stereo format with new stereo format set and expect the value to be STEREO.
8.Device_Settings_Agent will return SUCCESS or FAILURE based on the result from the above step</automation_approch>
    <except_output>Checkpoint 1. Check the current stereo mode is present in the list of supported stereo modes.
Checkpoint 2. Check the stereo mode before and after setting it.</except_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_AOP_getSupportedStereoModes
TestMgr_DS_AOP_setStereoMode
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_getSPDIF_SURROUND_AfterReboot_139</test_script>
    <skipped>No</skipped>
    <release_version>M27</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from devicesettings import dsManagerInitialize, dsManagerDeInitialize;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DS_getSPDIF_SURROUND_AfterReboot_139');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():

        #calling Device Settings - initialize API
	result = dsManagerInitialize(obj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
	if "SUCCESS" in result:
                #calling DS_GetSupportedStereoModes get list of StereoModes
                tdkTestObj = obj.createTestStep('DS_GetSupportedStereoModes');
                tdkTestObj.addParameter("port_name","SPDIF0");
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                supportedModes = tdkTestObj.getResultDetails();
                print supportedModes
                #Check for SUCCESS/FAILURE return value of DS_GetSupportedStereoModes
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
			print "Successfully fetched list of supported StereoModes for SPDIF0";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to get supported stereo modes";

		if "STEREO" in supportedModes:
                	#calling DS_SetStereoMode to set stereo mode to "STEREO"
                	tdkTestObj = obj.createTestStep('DS_SetStereoMode');
                	stereomode="STEREO";
                	print "Set stereo mode value to %s" %stereomode;
                	tdkTestObj.addParameter("stereo_mode",stereomode);
                	tdkTestObj.addParameter("port_name","SPDIF0");
                	expectedresult="SUCCESS"
                	tdkTestObj.executeTestCase(expectedresult);
                	actualresult = tdkTestObj.getResult();
                	stereomodedetails = tdkTestObj.getResultDetails();
                	#Check for return value
                	if expectedresult in actualresult:
                        	tdkTestObj.setResultStatus("SUCCESS");
				print "SUCCESS: Setting stereo mode value";
                	else:
                        	tdkTestObj.setResultStatus("FAILURE");
				print "FAILURE: Setting stereo mode value";

			#Calling DS_ManagerDeInitialize to DeInitialize API
			result = dsManagerDeInitialize(obj)

                	#Reboot the STB
                	obj.initiateReboot();

			#Calling Device Settings - initialize API
			result = dsManagerInitialize(obj)
			if "SUCCESS" in result:
                        	#calling DS_SetStereoMode to get the stereo mode
                        	tdkTestObj = obj.createTestStep('DS_SetStereoMode');
                        	tdkTestObj.addParameter("port_name","SPDIF0");
                        	tdkTestObj.addParameter("get_only",1);
                        	expectedresult="SUCCESS"
                        	stereomode="STEREO"
                        	tdkTestObj.executeTestCase(expectedresult);
                        	actualresult = tdkTestObj.getResult();
                        	stereomodedetails = tdkTestObj.getResultDetails();
				print "get mode: %s" %stereomodedetails;
                        	#Check for SUCCESS/FAILURE return value of DS_SetStereoMode
                        	if expectedresult in actualresult:
                                	#comparing stereo modes before and after setting
                                	if stereomode in stereomodedetails:
                                        	tdkTestObj.setResultStatus("SUCCESS");
                                        	print "SUCCESS: STEREO Mode set for SPDIF after Reboot";
                                	else:
                                        	tdkTestObj.setResultStatus("FAILURE");
                                        	print "FAILURE: STEREO Mode not set for SPDIF after Reboot";
                        	else:
                                	tdkTestObj.setResultStatus("FAILURE");
                               	 	print "FAILURE :Application failed to get the Stereomode for SPDIF";
                		#calling DS_ManagerDeInitialize to DeInitialize API 
				result = dsManagerDeInitialize(obj)
        	else:
                	print "Stereo Mode not supported by audio port";
			#Calling Device Settings - DeInitialize API
			result = dsManagerDeInitialize(obj)

        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
