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
  <name>DS_VOP_setDisplayConnected_178</name>
  <primitive_test_id/>
  <primitive_test_name>DS_VOP_setDisplayConnected</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Objective: This API is used to set the video output port display to be connected.
Test Case Id: CT_DS_178
Test Type: positive</synopsis>
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
    <test_case_id>CT_DS_178</test_case_id>
    <test_objective>This API is used to set the video output port display to be connected.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>void setDisplayConnected(const bool connected)</api_or_interface_used>
    <input_parameters>string port_name("HDMI0")
int connected (0,1)</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will set video output port display connection to enable or disable.
3.Device_Settings_Agent will check video output port display connection is enabled or disabled successfully.
6.Device_Settings_Agent will return SUCCESS or FAILURE based on the result from the above step</automation_approch>
    <except_output>Checkpoint 1. Check if video output port display connection is enabled or disabled successfully.</except_output>
    <priority>High</priority>
    <test_stub_interface>none</test_stub_interface>
    <test_script>DS_VOP_setDisplayConnected_178</test_script>
    <skipped>No</skipped>
    <release_version>M27</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import devicesettings;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","2.0");
obj.configureTestCase(ip,port,'DS_VOP_setDisplayConnected_178');
#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():

        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        print "[DS Initialize RESULT] : %s" %actualresult;

        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
		
                #Get the Video Ports supported.
                tdkTestObj = obj.createTestStep('DS_HOST_getVideoOutputPorts');
                expectedresult="SUCCESS"
                print " "
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails()
                print "[DS_HOST_getVideoOutputPorts RESULT] : %s" %actualresult;
                print "[DS_HOST_getVideoOutputPorts DETAILS] : %s" %details;

                #Check for SUCCESS/FAILURE return value of DS_HOST_getVideoOutputPorts.
                if expectedresult in actualresult:
                	tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: Get DS_HOST_getVideoOutputPorts";

                        portNames = details.split(',')
                        print "Port Names: ",portNames

                        for portName in portNames:
				for connected in range (0,2):
                                	#calling Device Settings - set Display Connected.
                                	tdkTestObj = obj.createTestStep('DS_VOP_setDisplayConnected');
                                	tdkTestObj.addParameter("port_name",portName);
					tdkTestObj.addParameter("connected",connected);
                                	expectedresult="FAILURE"
                                	print " "
                                	tdkTestObj.executeTestCase(expectedresult);
                                	actualresult = tdkTestObj.getResult();
                                	details = tdkTestObj.getResultDetails()
                                	print "[RESULT:%s PortName: %s DETAILS:%s]" %(actualresult,portName,details);

                                	#Check for SUCCESS/FAILURE return value of DS_VOP_setDisplayConnected
                                        if expectedresult in actualresult:
						tdkTestObj.setResultStatus("SUCCESS");
						print "Error occured while executing unsupported API setDisplayConnected"
                                	else:
						connResult = devicesettings.dsIsDisplayConnected(obj)
						print "[PortName: %s IsDisplayConnected:%s]" %(portName,connResult);
						if connected == 0 and connResult == "TRUE":
							tdkTestObj.setResultStatus("FAILURE");
							print "setDisplayConnected to false but isDisplayConnected is true"
						elif connected == 1 and connResult == "FALSE":
							tdkTestObj.setResultStatus("FAILURE");
							print "setDisplayConnected to true but isDisplayConnected is false"
						else:
							tdkTestObj.setResultStatus("SUCCESS");
							print "setDisplayConnected value matches with isDisplayConnected result"

		                print " "
		else:
			tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Get DS_HOST_getVideoOutputPorts"


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

        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
