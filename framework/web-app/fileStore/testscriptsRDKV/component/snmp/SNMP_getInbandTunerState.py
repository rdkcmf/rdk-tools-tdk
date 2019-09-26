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
  <name>SNMP_getInbandTunerState</name>
  <primitive_test_id/>
  <primitive_test_name>SNMP_GetCommString</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test gets the in-band tuner state of the host</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_SNMP_08</test_case_id>
    <test_objective>To get in-band tuner current status of the host using snmpwalk command</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite/>
    <api_or_interface_used>GetCommString()</api_or_interface_used>
    <input_parameters>"SnmpMethod : snmpwalk
SnmpVersion : v2c
OID : 1.3.6.1.4.1.4491.2.3.1.1.1.2.7.1.1.13.1"</input_parameters>
    <automation_approch>"1.TM will load the snmp_protocolagent via Test agent
2.From python script, invoke SnmpExecuteCmd function in snmplib to get the value of given OID
3. GetCommString function in the SNMP stub  will be called from snmplib to get the community string.
4.Responses from the snmplib and executecmd will be logged in Script log.
6. Validation of  the result is done within the python script and send the result status to Test Manager.
7.Test Manager will publish the result in GUI as PASS/FAILURE based on the response from snmplib"</automation_approch>
    <except_output>"CheckPoint 1:
Response of snmp command should be logged in the script log

CheckPoint 2:
Stub and lib function result should be success and should see corresponding log in the script log

CheckPoint 3:
TestManager GUI will publish the result as PASS in Execution/Console page of Test Manager"</except_output>
    <priority>High</priority>
    <test_stub_interface>libsnmpstub.so</test_stub_interface>
    <test_script>SNMP_getInbandTunerState</test_script>
    <skipped>No</skipped>
    <release_version>M48</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import snmplib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("snmp","2");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'SNMP_getInbandTunerState');

#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('SNMP_GetCommString');
    expectedresult="SUCCESS"
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    commString = tdkTestObj.getResultDetails();
    print "[SNMP_GetCommString RESULT] : %s" %actualresult;
    print "Community String: %s" %commString;
    snmpResponse =snmplib.SnmpExecuteCmd("snmpwalk",commString, "-v 2c", "1.3.6.1.4.1.4491.2.3.1.1.1.2.7.1.1.13.1", ip);
    actResponse =snmpResponse.split("=")[-1]

    #Logic for verification will be done in the next iteration
    if "1" in actResponse:
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP 1:Execute snmpwalk to get In-band tuner current state";
        print "EXPECTED RESULT 1: snmpwalk should get In-band tuner current state";
        print "ACTUAL RESULT 1: %s" %actResponse;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS :ready" ;
    elif "2" in actResponse:
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP 1:Execute snmpwalk to get In-band tuner current state";
        print "EXPECTED RESULT 1: snmpwalk should get In-band tuner current state";
        print "ACTUAL RESULT 1: %s" %actResponse;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS :waitingSync" ;
    elif "3" in actResponse:
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP 1:Execute snmpwalk to get In-band tuner current state";
        print "EXPECTED RESULT 1: snmpwalk should get In-band tuner current state";
        print "ACTUAL RESULT 1: %s" %actResponse;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS :waitingQam" ;
    elif "4" in actResponse:
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP 1:Execute snmpwalk to get In-band tuner current state";
        print "EXPECTED RESULT 1: snmpwalk should get In-band tuner current state";
        print "ACTUAL RESULT 1: %s" %actResponse;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS :foundSync-Tuner has successfully tuned to an analog channel" ;
    elif "5" in actResponse:
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP 1:Execute snmpwalk to get In-band tuner current state";
        print "EXPECTED RESULT 1: snmpwalk should get In-band tuner current state";
        print "ACTUAL RESULT 1: %s" %actResponse;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS :foundQam - Tuner has successfully tuned to a digital channel" ;
    elif "6" in actResponse:
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP 1:Execute snmpwalk to get In-band tuner current state";
        print "EXPECTED RESULT 1: snmpwalk should get In-band tuner current state";
        print "ACTUAL RESULT 1: %s" %actResponse;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS :unknown" ;
    elif "7" in actResponse:
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP 1:Execute snmpwalk to get In-band tuner current state";
        print "EXPECTED RESULT 1: snmpwalk should get In-band tuner current state";
        print "ACTUAL RESULT 1: %s" %actResponse;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS :standby" ;
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "TEST STEP 1:Execute snmpwalk to get In-band tuner current state";
        print "EXPECTED RESULT 1: snmpwalk should get In-band tuner current state";
        print "ACTUAL RESULT 1: %s" %actResponse;
        print "[TEST EXECUTION RESULT] : FAILURE : Tuning failed";
    obj.unloadModule("snmp");
else:
        print "FAILURE to load snmp module";
        obj.setLoadModuleStatus("FAILURE");
        print "Module loading FAILURE";

