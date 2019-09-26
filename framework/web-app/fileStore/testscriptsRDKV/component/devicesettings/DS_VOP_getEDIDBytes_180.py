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
  <name>DS_VOP_getEDIDBytes_180</name>
  <primitive_test_id/>
  <primitive_test_name>DS_VOP_getEDIDBytes</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Objective: This function is used to get the EDID information of the connected video display.
Test Case ID: CT_DS_180
Test Type: Positive.</synopsis>
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
    <test_case_id>CT_DS_180</test_case_id>
    <test_objective>This function is used to get the EDID information of the connected video display.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>void getEDIDBytes(std::vector&lt;uint8_t&gt; &amp;edid)</api_or_interface_used>
    <input_parameters>string port_name("HDMI0")</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get   EDID bytes for given video putput port name.
3.Device_Settings_Agent will check if EDID Checksum is valid.
4.Device_Settings_Agent will return SUCCESS or FAILURE based on the result from the above step</automation_approch>
    <except_output>Checkpoint 1. Check EDID value is at least 128 bytes.
Checkpoint 2. Check EDID Checksum is valid.</except_output>
    <priority>High</priority>
    <test_stub_interface>none</test_stub_interface>
    <test_script>DS_VOP_getEDIDBytes_180</test_script>
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

#To Check whether HDMI device is connected or not.
#Test component to be tested
dsObj = tdklib.TDKScriptingLibrary("devicesettings","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

dsObj.configureTestCase(ip,port,'DS_isDisplayConnected');

isDisplayConnected = "false"

#Get the result of connection with test component and STB
result =dsObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

if "SUCCESS" in result.upper():
        #Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(dsObj);
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Check for display connection status
                result = devicesettings.dsIsDisplayConnected(dsObj)
                if "TRUE" in result:
                        #Get the result of execution
                        print "HDMI display connected"
                        isDisplayConnected = "true"
                else:
                        print "HDMI display not connected."
                        isDisplayConnected = "false"

                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = devicesettings.dsManagerDeInitialize(dsObj)
        else:
                print "Failed to initialize DSMgr"

        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");
else:
        print "DS loading failed";

if isDisplayConnected == "true":
        print " "
        print "[HDMI device is connected proceeding to execute the script....!!!]"
        print " "
else:
        print " "
        print "[HDMI device not connected.]"
        print "[Please test connecting HDMI device. Exiting....!!!]"
        print " "
        exit()


#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DS_VOP_getEDIDBytes_180');

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
			portNames = ["HDMI0"]

                        for portName in portNames:

                                #calling Device Settings - Get the EDID bytes for the Video port connected.
                                tdkTestObj = obj.createTestStep('DS_VOP_getEDIDBytes');

                                tdkTestObj.addParameter("port_name",portName);
                                expectedresult="SUCCESS"
                                print " "
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details = tdkTestObj.getResultDetails()
                                print "[DS_VOP_getEDIDBytes RESULT] : %s" %actualresult;
                                print "[PortName: %s DETAILS] : %s" %(portName,details);

                                #Check for SUCCESS/FAILURE return value of DS_VOP_getEDIDBytes
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "DS_VOP_getEDIDBytes successful";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "DS_VOP_getEDIDBytes failed";

                                print " "
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Get DS_HOST_getVideoOutputPorts";

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
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
