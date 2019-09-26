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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Container_Block_Dependency</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Containerization_Donothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check containers boot dependencies from BLOCK containers</synopsis>
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
    <test_case_id>CT_Container_27</test_case_id>
    <test_objective>Check containers boot dependencies from BLOCK containers</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Emulator Hybrid</test_setup>
    <pre_requisite>Emulator containerized image booted in a VM</pre_requisite>
    <api_or_interface_used>Linux commands</api_or_interface_used>
    <input_parameters>NA</input_parameters>
    <automation_approch>1. TM loads the SystemUtilAgent
2. SystemUtilAgent will add a sleep to delay dbus starting for 10 sec in the file '/containers/dbus/rootfs/etc/rc.d/S00'
3. SystemUtilAgent will remove the block dependency from dbus for testing purpose
4. SystemUtilAgent will change the order of starting containers to "rmfserv dbus rdk-base"
5. SystemUtilAgent will stop each container 
6. SystemUtilAgent will start the containers and check the containers started in order and the output does not contain the notification string "notify reported success event for "dbus"Container Started successfully"
7. SystemUtilAgent will add a block marker in dbus container to assure the next container wait for dbus finishing to start
8. SystemUtilAgent will stop each container
9. SystemUtilAgent will start the containers and check the containers started in order and the output contains the notification string "notify reported success event for "dbus"Container Started successfully"
10. TM will return FAILURE/SUCCESS status based on the output in step9.
11. TM unloads the SystemUtilAgent</automation_approch>
    <except_output>Checkpoint 1.Check the containers started in order and the output contains the notification string "notify reported success event for "dbus"Container Started successfully"</except_output>
    <priority>High</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>Container_Block_Dependency</test_script>
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

def CheckPatternInFile(obj, pattern, fileName):
        status = False;
        tdkTestObj = obj.createTestStep('ExecuteCommand');
        expectedResult="SUCCESS";

        cmd = "grep " + pattern + " " + fileName;
        print cmd;

        #configure the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                print "Output: ", details.replace('\\','');
                print "Pattern: ", pattern;
                if pattern in details.replace('\\',''):
                        print ("Pattern found");
                        status = True;
                else:
                        print ("Pattern not Found");
        else:
                print ("Command execution failed");
        return (tdkTestObj, status);


#Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'Container_Block_Dependency');

#Get the result of connection with test component and STB
loadStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadStatus;
obj.setLoadModuleStatus(loadStatus.upper());

if "SUCCESS" in loadStatus.upper():
	#Prmitive test case which associated to this Script
        processList = ["dbusDaemonInit", "rmfStreamerInit", "systemd"];
        result = container.CheckProcessTree(obj, True, processList);
	if result:
		cmd = "sed -i '/dbusDaemonInit.sh/asleep 10'";
		fileName = "/containers/dbus/rootfs/etc/rc.d/S00";
		status = container.UpdateFile(obj, cmd, fileName);
			
		containerList = ["rmfserv", "dbus", "rdk-base"];
		cmd = "echo " + ' '.join(containerList) + " > ";
		fileName = "/etc/containers_order.conf";
		status = container.UpdateFile(obj, cmd, fileName);
		
		for containerName in containerList:
			container.StopContainer(obj,containerName);
		path = "/usr/bin/start_containers.sh";	
		container.StartContainer(obj,path);
		sleep(10);
		container.checkOrderCreation(obj,containerList);
		pattern = "notify reported success event for \"dbus\"Container Started successfully";
		testObj, status = CheckPatternInFile(obj, pattern, "/tmp/start_status.log");
		if status:
			testObj.setResultStatus("FAILURE");
		else:
			testObj.setResultStatus("SUCCESS");
		
		cmd = "sed -i 's/dbus/dbus--block/'";
		fileName = "/etc/containers_order.conf";
		status = container.UpdateFile(obj, cmd, fileName);
		
		for containerName in containerList:
			container.StopContainer(obj,containerName);
                path = "/usr/bin/start_containers.sh";
                container.StartContainer(obj,path);
		sleep(30);
		container.checkOrderCreation(obj,containerList);
                pattern = "notify reported success event for \"dbus\"Container Started successfully";
		testObj,status = CheckPatternInFile(obj, pattern, "/tmp/start_status.log");
		if status:
			testObj.setResultStatus("SUCCESS");
		else:
			testObj.setResultStatus("FAILURE");
	
		cmd = "sed -i '/sleep 10/d'";
		fileName = "/containers/dbus/rootfs/etc/rc.d/S00";
		container.UpdateFile(obj, cmd, fileName);

	else:
		print "Please test with containerized image";

obj.unloadModule("systemutil");
