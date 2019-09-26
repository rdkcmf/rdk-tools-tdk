##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2018 RDK Management
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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Container_Unprivileged_Network_Configuration_Stop_Rmfserv</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Containerization_Donothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check unprivileged container network configuration after stopping rmfserv container</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>20</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Emulator-HYB</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Container_35</test_case_id>
    <test_objective>Check unprivileged container network configuration
after stopping rmfserv container</test_objective>
    <test_type>Negative</test_type>
    <test_setup>Emulator hybrid</test_setup>
    <pre_requisite>Emulator containerized image booted in a VM</pre_requisite>
    <api_or_interface_used>N/A</api_or_interface_used>
    <input_parameters>N/A</input_parameters>
    <automation_approch>1. TM loads the SystemUtilAgent
2. SystemUtilAgent will check if rmfserv has virtual ethernet pair device created
3. SystemUtilAgent will check if the connection with a bridge is properly configured
4. SystemUtilAgent will check the container ipv4 address to the virtualized interface
5. SystemUtilAgent will check in the host if a ethernet was properly created according the veth.conf specifications
6. SystemUtilAgent will stop rmfserv container
7. SystemUtilAgent will check if the virtual ethernet pair was created and return FAILURE/SUCCESS nased on that
8. TM unloads the SystemUtilAgent</automation_approch>
    <except_output>Checkpoint 1.Check if the virtual ethernet pair is not created after stopping rmfserv container</except_output>
    <priority>High</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>Container_Unprivileged_Network_Configuration_Stop_Rmfserv</test_script>
    <skipped>No</skipped>
    <release_version></release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import container;
from time import sleep;

def CheckNWConfig(obj, interface):
	status = False;
        tdkTestObj = obj.createTestStep('ExecuteCommand');
        expectedResult="SUCCESS";

	cmd = "ifconfig " + interface + " | grep \"HWaddr\"";
        print cmd;

        #configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                print "Output: ", details;
		if interface in details:
			status = True;
        return (tdkTestObj, status);

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'Container_Unprivileged_Network_Configuration_Stop_Rmfserv');

#Get the result of connection with test component and STB
loadStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadStatus;
obj.setLoadModuleStatus(loadStatus.upper());

if "SUCCESS" in loadStatus.upper():
	#Prmitive test case which associated to this Script
        processList = ["dbusDaemonInit", "rmfStreamerInit", "systemd"];
        result = container.CheckProcessTree(obj, True, processList);
	if result:
                fileName = "/containers/rmfserv/veth.conf";
                patternList = ["\"lxc.network.type = veth\"", "\"lxc.network.veth.pair = vethrmfserv\"", "\"lxc.network.link = br0\""];
                for pattern in patternList:
                	status, value = container.FindPatternFromFile(obj, fileName, "", pattern);

		field = "\"lxc.network.ipv4 =\"";
		pattern = "";
		status, ipAddr = container.FindPatternFromFile(obj, fileName, field, pattern);
	
		tdkTestObj, status = CheckNWConfig(obj, "br0");
		if status:
	        	tdkTestObj.setResultStatus("SUCCESS");
        	        print "Network configuration is correct";
		else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Network configuration is not correct";
			
		container.StopContainer(obj,"rmfserv");
		tdkTestObj, status = CheckNWConfig(obj, "vethrmfserv");
		if not status:
	        	tdkTestObj.setResultStatus("SUCCESS");
        	        print "Virtual ethrnet pair is not created";
		else:
                        tdkTestObj.setResultStatus("FAILURE");
        	        print "Virtual ethrnet pair is created";
		
		path = "/usr/bin/start_containers.sh";
                container.StartContainer(obj,path);
		sleep(10);
		tdkTestObj, status = CheckNWConfig(obj, "vethrmfserv");
		if status:
	        	tdkTestObj.setResultStatus("SUCCESS");
        	        print "Virtual ethrnet pair is created";
		else:
                        tdkTestObj.setResultStatus("FAILURE");
        	        print "Virtual ethrnet pair is not created";

	else:
		print "Please test with containerized image";

obj.unloadModule("systemutil");
