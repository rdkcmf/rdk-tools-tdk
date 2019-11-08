##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2019 RDK Management
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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>XUPNP_GetSerialNumFromOutFile</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>XUPNP_ReadXDiscOutputFile</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To get Serial Number value from xdiscovery output file.
Testcase ID: CT_XUPNP_16</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_XUPNP_16</test_case_id>
    <test_objective>To get Serial Number value from xdiscovery output file.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1.start_upnp.sh should be started.
2.Process xcal-device and xdiscovery should be running on GW Box and xdiscovery should be running on IPClient Box</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>string paramName=sno</input_parameters>
    <automation_approch>1.TM loads xupnp_agent via the test agent. 
2.The stub will invokes the RPC method for checking the parameter name in output.json file and send the results.
3. The stub function will verify the presence of parameter name and  sends the results as Json response 
4. TM will receive and display the result.
5. TM will convert the details as a list.
6. Using systemutil ExecuteCommand command get the parameter from tr181Set -g Device.DeviceInfo.SerialNumber. 
7 If the serial number obtained from the tr181Set -g Device.DeviceInfo.SerialNumber is present in the list created in step 5 the result is success else failure.</automation_approch>
    <expected_output>Checkpoint 1 stub will parse for parameter name in output.json file
Checkpoint 2 the parameter from the ExecuteCommand  should be present in the parameter list obtained from output.json</expected_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_XUPNP_ReadXDiscOutputFile</test_stub_interface>
    <test_script>XUPNP_GetSerialNumFromOutFile</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
xUpnpObj = tdklib.TDKScriptingLibrary("xupnp","2.0");
xUpnpObj.configureTestCase(ip,port,'XUPNP_GetSerialNumFromOutFile');
#Get the result of connection with test component and STB
xupnpLoadStatus = xUpnpObj.getLoadModuleResult();
print "XUPNP module loading status : %s" %xupnpLoadStatus;
#Set the module loading status
xUpnpObj.setLoadModuleStatus(xupnpLoadStatus);

sysUtilObj = tdklib.TDKScriptingLibrary("systemutil","1");
sysUtilObj.configureTestCase(ip,port,'XUPNP_GetSerialNumFromOutFile');
sysUtilLoadStatus = sysUtilObj.getLoadModuleResult();
print "System module loading status : %s" %sysUtilLoadStatus;
#Set the module loading status
sysUtilObj.setLoadModuleStatus(sysUtilLoadStatus);

if ("SUCCESS" in xupnpLoadStatus.upper()) and ("SUCCESS" in sysUtilLoadStatus.upper()):
        tdkTestObj = xUpnpObj.createTestStep('XUPNP_ReadXDiscOutputFile');
        expectedresult="SUCCESS";
        #Configuring the test object for starting test execution
        tdkTestObj.addParameter("paramName","sno");
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
	print "GetSerialNum Result : %s"%actualresult;
        #Check for SUCCESS return value of XUPNP_ReadXDiscOutputFile
        if "SUCCESS" in actualresult.upper():
                tdkTestObj.setResultStatus("SUCCESS");
        	details = details.replace('\\t','').replace('\\','').replace('\"','')
        	details_list = details.split(',')
        	print "GetSerialNum Details : %s"%str(details_list);
		serial_num_list = [ detail.split(':')[1] for detail in details_list]
                
		#get the serialnumber from tr181Set -g Device.DeviceInfo.SerialNumber and compare
		tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand');
		cmd = "tr181Set -g Device.DeviceInfo.SerialNumber &> /opt/TDK/serial.txt;cat /opt/TDK/serial.txt | tr -d '\n';rm /opt/TDK/serial.txt";
		print cmd;
    		tdkTestObj.addParameter("command", cmd);
    		tdkTestObj.executeTestCase("SUCCESS");
		actualresult = tdkTestObj.getResult();
    		details = tdkTestObj.getResultDetails().strip();

		serial_num = details
		print "Serial number from Device.DeviceInfo.SerialNumber: %s" %serial_num
		if expectedresult in actualresult and serial_num in serial_num_list:
			tdkTestObj.setResultStatus("SUCCESS");
        		print "Actual Result: Serial Number retrieved from tr181Set -g Device.DeviceInfo.SerialNumber and output.json are same"
        		print "[TEST EXECUTION RESULT] : SUCCESS"
		else:
			tdkTestObj.setResultStatus("FAILURE");
        		print "Actual Result: Serial Number retrieved from tr181Set -g Device.DeviceInfo.SerialNumber and output.json are not same"
        		print "[TEST EXECUTION RESULT] : FAILURE"
	else:
		tdkTestObj.setResultStatus("FAILURE");
                print "Serial Number not retrieved from output.json"
        #Unload xupnp module
        xUpnpObj.unloadModule("xupnp");
	sysUtilObj.unloadModule("systemutil");



