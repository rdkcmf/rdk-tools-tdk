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
  <name>Container_Check_Special_Permission_Iarmbus</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Containerization_Donothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check that containeirzed tdk image added special permissions to IARMBUS</synopsis>
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
    <test_case_id>CT_Container_32</test_case_id>
    <test_objective>Check that containeirzed tdk image added special permissions to IARMBUS</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Emulator hybrid</test_setup>
    <pre_requisite>Emulator containerized image booted in a VM</pre_requisite>
    <api_or_interface_used>N/A</api_or_interface_used>
    <input_parameters>N/A</input_parameters>
    <automation_approch>1. TM loads the SystemUtilAgent
2. SystemUtilAgent will check check if system-local-tdk.conf was added to the emulator image
3. TM will check if the system-local-tdk.conf contains needed permissions to IARMBUS and return SUCCESS/FAILURE status.
4. TM unloads the SystemUtilAgent</automation_approch>
    <except_output>Checkpoint 1.Check if the system-local-tdk.conf contains needed permissions to IARMBUS</except_output>
    <priority>High</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>Container_Check_Special_Permission_Iarmbus</test_script>
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
import os.path;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

def CheckFileExists(obj, folderPath, fileName):
        fileList = [];
	status = False;
        tdkTestObj = obj.createTestStep('ExecuteCommand');
        expectedResult="SUCCESS";

        cmd = "ls " + folderPath + " | tr \'\n\' \' \'";
        print cmd;

        #configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                print "Output: ", details;
                fileList = details.split();
                print fileList;
		if fileName in fileList:
			status = True;
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "File exists";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "File does not exist";

        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Command execution failed";
        return status;



obj.configureTestCase(ip,port,'Container_Check_Special_Permission_Iarmbus');

#Get the result of connection with test component and STB
loadStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadStatus;
obj.setLoadModuleStatus(loadStatus.upper());

if "SUCCESS" in loadStatus.upper():
	#Prmitive test case which associated to this Script
        processList = ["dbusDaemonInit", "rmfStreamerInit", "systemd"];
        result = container.CheckProcessTree(obj, True, processList);
	if result:
		folder = "/etc/dbus-1/";
		fileName = "system-local-tdk.conf";
		status = CheckFileExists(obj, folder, fileName)
		if status:
			patternList = ["\"allow own=\\\"process.iarm.agent\\\"\"", "\"allow own=\\\"process.iarm.Daemon\\\"\"",	"\"allow send_destination=\\\"process.iarm.Daemon\\\"\"", "\"allow receive_sender=\\\"process.iarm.Daemon\\\"\"", "\"allow send_destination=\\\"process.iarm.agent\\\"\"", "\"allow receive_sender=\\\"process.iarm.agent\\\"\""];
			fileName = folder + fileName;
			for pattern in patternList:
				status, value = container.FindPatternFromFile(obj, fileName, "", pattern);			
		

	else:
		print "Please test with containerized image";

obj.unloadModule("systemutil");
