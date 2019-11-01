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
  <version>3</version>
  <name>XUPNP_GetIsGatewayFromOutFile</name>
  <primitive_test_id/>
  <primitive_test_name>XUPNP_ReadXDiscOutputFile</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To get isgateway value from xdiscovery output file.
Testcase ID: CT_XUPNP_11</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>RPI-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_XUPNP_11</test_case_id>
    <test_objective>To get isgateway value from xdiscovery output file.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1.start_upnp.sh should be started.
2.Process xcal-device and xdiscovery should be running on GW Box and xdiscovery should be running on IPClient Box</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>string paramName=isgateway</input_parameters>
    <automation_approch>1.TM loads xupnp_agent via the test agent. 
2.The stub will invokes the RPC method for checking the parameter name in output.json file and send the results.
3. The stub function will verify the presence of parameter name and  sends the results as Json response 
4. TM will receive and display the result.
5. TM will create a list of Isgateway values.
6. Again invoke the stub with parameter DevType
7. After getting the values for DevType, TM will create a list of DevType values .
8. TM will create a dictionary with the 2 lists and compare the key and values with the predefined dictionary.
9. If values are same for the corresponding keys of each dictionary then test is success else failure. 
</automation_approch>
    <except_output>Checkpoint 1 stub will parse for parameter name in output.json file
checkpoint 2 Each key will have same value in the corresponding key in the predefined dictionary.</except_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_XUPNP_ReadXDiscOutputFile</test_stub_interface>
    <test_script>XUPNP_GetIsGatewayFromOutFile</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
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
xUpnpObj.configureTestCase(ip,port,'XUPNP_GetIsGatewayFromOutFile');
#Get the result of connection with test component and STB
xupnpLoadStatus = xUpnpObj.getLoadModuleResult();
print "XUPNP module loading status : %s" %xupnpLoadStatus;
#Set the module loading status
xUpnpObj.setLoadModuleStatus(xupnpLoadStatus);

if "SUCCESS" in xupnpLoadStatus.upper():
        tdkTestObj = xUpnpObj.createTestStep('XUPNP_ReadXDiscOutputFile');
        expectedresult="SUCCESS";
        #Configuring the test object for starting test execution
        tdkTestObj.addParameter("paramName","isgateway");
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "GetIsGateway Result : %s"%actualresult;
	if "SUCCESS" in actualresult.upper():
                tdkTestObj.setResultStatus("SUCCESS");
                details = details.replace('\\t','').replace('\\','').replace('\"','')
                details_list = details.split(',')
                isgateway_list = [ detail.split(':',1)[1] for detail in details_list]
                #Get the devtype values
		tdkTestObj = xUpnpObj.createTestStep('XUPNP_ReadXDiscOutputFile');
                expectedresult="SUCCESS";
                #Configuring the test object for starting test execution
                tdkTestObj.addParameter("paramName","DevType");
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "GetDevType Result : %s"%actualresult;
		details = tdkTestObj.getResultDetails();
                if "SUCCESS" in actualresult.upper():
                        tdkTestObj.setResultStatus("SUCCESS");
                        details = details.replace('\\t','').replace('\\','').replace('\"','')
                        details_list = details.split(',')
                        #removing the recvdevtype values from the list
			for detail in details_list:
                                if detail.split(':')[0]!= 'DevType':
                                        details_list.remove(detail)
                        devType_list = [ detail.split(':')[1] for detail in details_list]
                        #creating dictionary with key as devtype and isgateway value as the corresponding value
			dictionary = dict(zip(devType_list, isgateway_list));
                        dict_valid = {'XI3':'no','XI5':'no','XI6':'no','XG1':'yes'};
			for key in dictionary :
                        	if dictionary.get(key) == dict_valid.get(key):
                                	tdkTestObj.setResultStatus("SUCCESS");
                                	print "ACTUAL RESULT : isgateway value is %s for the corresponding DevType %s"%(dictionary.get(key),key);
                        	else:
					tdkTestObj.setResultStatus("FAILURE");
                                	print "[TEST EXECUTION RESULT] : FAILURE";
                else:
			tdkTestObj.setResultStatus("FAILURE");
			print "devtype not found"
	else:
		 tdkTestObj.setResultStatus("FAILURE");
                 print "isgateway parameter not found"
        #Unload xupnp module
        xUpnpObj.unloadModule("xupnp");
