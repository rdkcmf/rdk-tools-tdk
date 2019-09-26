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
  <name>DS_HOST_getAudioOutputPortFromName_150</name>
  <primitive_test_id/>
  <primitive_test_name>DS_HOST_getAudioOutputPortFromName</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test script is used to get the reference to the audio output port by its name.
TestcaseID: CT_DS150</synopsis>
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
    <test_case_id>CT_DS_150</test_case_id>
    <test_objective>This test script is used to get the reference to the audio output port by its name.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>AudioOutputPort &amp;getAudioOutputPort(const std::string &amp;name)</api_or_interface_used>
    <input_parameters>string port_name ("SPDIF0","HDMI0")</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get the audio output port instance by portname.
3.Device_Settings_Agent will check if port name retrieved using port instance is same as port name provided.
4.Device_Settings_Agent will return SUCCESS or FAILURE based on the result from the above step</automation_approch>
    <except_output>Checkpoint 1. Check if port name retrieved using port instance is same as port name provided</except_output>
    <priority>High</priority>
    <test_stub_interface>none</test_stub_interface>
    <test_script>DS_HOST_getAudioOutputPortFromName_150</test_script>
    <skipped>No</skipped>
    <release_version>M27</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import devicesettings;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DS_HOST_getAudioOutputPortFromName_150');

#Get the result of connection with test component and STB
loadmodulestatus=obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
        #Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(obj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result.upper():
                #Check for display connection status
                result = devicesettings.dsIsDisplayConnected(obj)
                if "TRUE" in result:
	                tdkTestObj = obj.createTestStep('DS_HOST_getAudioOutputPorts');
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details = tdkTestObj.getResultDetails();
                        print "[TEST EXECUTION RESULT] : %s" %actualresult;
                        print "Details: [%s]"%details;
			if "SUCCESS" in actualresult.upper():
	                        #Primitive test case which associated to this Script
				tdkTestObj = obj.createTestStep('DS_HOST_getAudioOutputPortFromName');
				audioList = details.split(",")
				for portName in audioList:
					print "Getting the audio output port from ", portName
					tdkTestObj.addParameter("port_name",portName);
					expectedresult="SUCCESS"
		                        tdkTestObj.executeTestCase(expectedresult);
		                        actualresult = tdkTestObj.getResult();
		                        details = tdkTestObj.getResultDetails();
		                        print "[TEST EXECUTION RESULT] : %s" %actualresult;
		                        print "Details: [%s]"%details;
		                        #Set the result status of execution
		                        if expectedresult in actualresult:
	        	                        tdkTestObj.setResultStatus("SUCCESS");
		                        else:
        		                        tdkTestObj.setResultStatus("FAILURE");

			else :
				tdkTestObj.setResultStatus("FAILURE");
				print "Failed to get the audio output ports"

                else :
                        print "Display device not connected. Skipping testcase"

		#Calling DS_ManagerDeInitialize to DeInitialize API
		result = devicesettings.dsManagerDeInitialize(obj)

	obj.unloadModule("devicesettings");
else :
	print "Failed to Load Module"
