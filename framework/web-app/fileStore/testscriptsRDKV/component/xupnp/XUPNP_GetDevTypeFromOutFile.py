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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>2</version>
  <name>XUPNP_GetDevTypeFromOutFile</name>
  <primitive_test_id/>
  <primitive_test_name>XUPNP_ReadXDiscOutputFile</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To get the device type from xdiscovery output file.
Testcase ID: CT_XUPNP_46</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_XUPNP_46</test_case_id>
    <test_objective>To get the device type from xdiscovery output file.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1.start_upnp.sh should be started.
2.Process xcal-device and xdiscovery should be running on GW Box and xdiscovery should be running on IPClient Box</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>string paramName = DevType</input_parameters>
    <automation_approch>1.TM loads xupnp_agent via the test agent. 
2.The stub will invokes the RPC method for checking the parameter name in output.json file and send the results.
3. The stub function will verify the presence of parameter name and  sends the results as Json response 
4. TM will receive and display the result.
5. Create a list of devTypes from the details.
6. Using systemutil ExecuteCommand obtain the devType from cat /etc/device.properties.
7. If the devtype obatained from step 6 is present in the devTypes list , result is success else failure.</automation_approch>
    <except_output>Checkpoint 1 stub will parse for parameter name in output.json file
Checkpoint 2 the parameter from the ExecuteCommand  should be present in the parameter list obtained from output.json</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_XUPNP_ReadXDiscOutputFile</test_stub_interface>
    <test_script>XUPNP_GetDevTypeFromOutFile</test_script>
    <skipped>No</skipped>
    <release_version>M68</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
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
xUpnpObj.configureTestCase(ip,port,'XUPNP_GetDevTypeFromOutFile');

#Get the result of connection with test component and STB
xupnpLoadStatus =xUpnpObj.getLoadModuleResult();
print "XUPNP module loading status : %s" %xupnpLoadStatus;
#Set the module loading status
xUpnpObj.setLoadModuleStatus(xupnpLoadStatus);

sysUtilObj = tdklib.TDKScriptingLibrary("systemutil","1");
sysUtilObj.configureTestCase(ip,port,'XUPNP_GetDevTypeFromOutFile');
sysUtilLoadStatus = sysUtilObj.getLoadModuleResult();
print "System module loading status : %s" %sysUtilLoadStatus;
#Set the module loading status
sysUtilObj.setLoadModuleStatus(sysUtilLoadStatus);

if ("SUCCESS" in xupnpLoadStatus.upper()) and ("SUCCESS" in sysUtilLoadStatus.upper()):
	tdkTestObj = xUpnpObj.createTestStep('XUPNP_ReadXDiscOutputFile');
        expectedresult="SUCCESS";
        #Configuring the test object for starting test execution
        tdkTestObj.addParameter("paramName","DevType");
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
    	print "GetDevType Result : %s"%actualresult;
   	#Check for SUCCESS return value of XUPNP_ReadXDiscOutputFile
    	if "SUCCESS" in actualresult.upper():
        	tdkTestObj.setResultStatus("SUCCESS");
		details = details.replace('\\t','').replace('\\','').replace('\"','')
        	details_list = details.split(',')
        	for detail in details_list:
                	if detail.split(':')[0]!= 'DevType':
                        	details_list.remove(detail)
    		print "GetDevType Details : %s"%str(details_list);
		devType_list = [ detail.split(':')[1] for detail in details_list]
        	
		#for validating the devType, get the value from device.properties and compare
		tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand');
		cmd = "cat /etc/device.properties | grep BOX_TYPE |cut -d '=' -f2 | tr -d '\n'";
		print cmd;
                tdkTestObj.addParameter("command", cmd);
                tdkTestObj.executeTestCase("SUCCESS");
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails().strip();
		dev_type_from_box = details
                print "DevType from box: ", details
		
		#initialize a flag to 0 and set the flag to 1 if both the values are same
		check_flag = 0
                if expectedresult in actualresult:
			for devType in devType_list:
 				if devType in dev_type_from_box:
					check_flag = 1
                        		tdkTestObj.setResultStatus("SUCCESS");
                        		print "Actual Result: devType retrieved from the box and output.json are same"
					print "[TEST EXECUTION RESULT] : SUCCESS"
			else:
				if check_flag == 0:
					tdkTestObj.setResultStatus("FAILURE");
                        		print "Actual Result: devType retrieved from the box and output.json are not same"
                        		print "[TEST EXECUTION RESULT] : FAILURE"

                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "ExecuteCommand Failed.."
                        print "[TEST EXECUTION RESULT] : FAILURE"
	else:
		tdkTestObj.setResultStatus("FAILURE");
		print "Actual Result: devType not found from output.json"
                print "[TEST EXECUTION RESULT] : FAILURE"
	        
	#Unload xupnp module
        xUpnpObj.unloadModule("xupnp");
        sysUtilObj.unloadModule("systemutil");

