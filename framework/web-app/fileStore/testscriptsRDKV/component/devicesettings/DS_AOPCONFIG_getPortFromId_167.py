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
  <name>DS_AOPCONFIG_getPortFromId_167</name>
  <primitive_test_id/>
  <primitive_test_name>DS_AOPCONFIG_getPortFromId</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Objective:
Test Case Id: CT_DS_167
Test Type: Positive</synopsis>
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
    <box_type>Emulator-HYB</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_167</test_case_id>
    <test_objective>This API is used to get the type of the audio output port from port id</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>AudioOutputPort  &amp;getPort(int id)</api_or_interface_used>
    <input_parameters>int port_id (0)</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get the audio output port instance by port id.
3.Device_Settings_Agent will check if audio output port id retrieved using audio output port instance is same as port id provided.
4.Device_Settings_Agent will return SUCCESS or FAILURE based on the result from the above step</automation_approch>
    <except_output>Checkpoint 1. Check if port id retrieved using audio output port instance is same as port id provided</except_output>
    <priority>High</priority>
    <test_stub_interface>none</test_stub_interface>
    <test_script>DS_AOPCONFIG_getPortFromId_167</test_script>
    <skipped>No</skipped>
    <release_version>M27</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DS_AOPCONFIG_getPortFromId_167');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;

if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        print "[DS Initialize RESULT] : %s" %actualresult;

        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");

            tdkTestObj = obj.createTestStep('DS_HOST_getAudioOutputPorts');
            expectedresult="SUCCESS"
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            print "[TEST EXECUTION RESULT] : %s" %actualresult;
            print "Supported AudioOutputPorts: [%s]"%details;
            if "SUCCESS" in actualresult.upper():

                #calling Device Settings - Get Port From Id.
		portList = details.split(",")
                portIds = len(portList)
                print "Number of Audio ID's supported is ",portIds

                tdkTestObj = obj.createTestStep('DS_AOPCONFIG_getPortFromId');

		for port_id in range(0,portIds):
	                tdkTestObj.addParameter("port_id",port_id);
        	        expectedresult="SUCCESS"

	        	print " "
        	        tdkTestObj.executeTestCase(expectedresult);
                	actualresult = tdkTestObj.getResult();
	                details = tdkTestObj.getResultDetails()
                	print "[DS_AOPCONFIG_getPortFromId RESULT] : %s" %actualresult;
        	        print "PortId: %d DETAILS : %s" %(port_id,details);

	                #Check for SUCCESS/FAILURE return value of DS_AOPCONFIG_getPortFromId
        	        if expectedresult in actualresult:
                	        tdkTestObj.setResultStatus("SUCCESS");
                        	print "SUCCESS: Get DS_AOPCONFIG_getPortFromId";
	                else:
        	                tdkTestObj.setResultStatus("FAILURE");
                	        print "FAILURE: Get DS_AOPCONFIG_getPortFromId"

                print " "
                #calling DS_ManagerDeInitialize to DeInitialize API
                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "[DS Deinitalize RESULT] : %s" %actualresult;

                #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        tdkTestObj.setResultStatus("FAILURE");
	    else:
		tdkTestObj.setResultStatus("FAILURE");
		print "Failed to get number of AudioOutputPorts"
        else:
                tdkTestObj.setResultStatus("FAILURE");

        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
