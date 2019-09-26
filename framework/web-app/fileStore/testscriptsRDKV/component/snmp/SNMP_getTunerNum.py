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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SNMP_getTunerNum</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SNMP_GetCommString</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test gets the number of tuners connected</synopsis>
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
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_SNMP_07</test_case_id>
    <test_objective>To get number of tuners connected using snmpwalk command
</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>GetCommString()
</api_or_interface_used>
    <input_parameters>"SnmpMethod : snmpwalk
SnmpVersion : v2c
OID : 1.3.6.1.4.1.17270.9225.1.4.1.6"
</input_parameters>
    <automation_approch>"1.TM will load the snmp_protocolagent via Test agent
2.From python script, invoke SnmpExecuteCmd function in snmplib to get the value of given OID
3. GetCommString function in the SNMP stub  will be called from snmplib to get the community string.
4.Responses from the snmplib and executecmd will be logged in Script log.
6. Validation of  the result is done within the python script and send the result status to Test Manager.
7.Test Manager will publish the result in GUI as PASS/FAILURE based on the response from snmplib"
</automation_approch>
    <except_output>"1.TM will load the snmp_protocolagent via Test agent
2.From python script, invoke SnmpExecuteCmd function in snmplib to get the value of given OID
3. GetCommString function in the SNMP stub  will be called from snmplib to get the community string.
4.Responses from the snmplib and executecmd will be logged in Script log.
6. Validation of  the result is done within the python script and send the result status to Test Manager.
7.Test Manager will publish the result in GUI as PASS/FAILURE based on the response from snmplib"
</except_output>
    <priority>High</priority>
    <test_stub_interface>libsnmpstub.so
</test_stub_interface>
    <test_script>SNMP_getTunerNum</test_script>
    <skipped>No</skipped>
    <release_version>M48</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import snmplib;
from trm import getMaxTuner;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("snmp","2");
trmObj = tdklib.TDKScriptingLibrary("trm","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'SNMP_getTunerNum');
trmObj.configureTestCase(ip,port,'SNMP_getTunerNum');

#Get the result of connection with test component and STB
loadmodulestatus1 =obj.getLoadModuleResult();
loadmodulestatus2 =trmObj.getLoadModuleResult();

print "[SNMP LIB LOAD STATUS]  :  %s" %loadmodulestatus1;
print "[TRM LIB LOAD STATUS]  :  %s" %loadmodulestatus2;

if "SUCCESS" in loadmodulestatus1.upper()and "SUCCESS" in loadmodulestatus2.upper():
    obj.setLoadModuleStatus("SUCCESS");
    trmObj.setLoadModuleStatus("SUCCESS");
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('SNMP_GetCommString');
    expectedresult="SUCCESS"
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    commString = tdkTestObj.getResultDetails();
    print "[SNMP_GetCommString RESULT] : %s" %actualresult;
    print "Community String: %s" %commString;
    actResponse =snmplib.SnmpExecuteCmd("snmpwalk",commString, "-v 2c", "1.3.6.1.4.1.17270.9225.1.4.1.6", ip);

    #Checking if the value obtained from snmp and trm are the same
    if "SNMPv2-SMI" in actResponse:
        noTuner=actResponse.split("\"")[1].strip();
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP 1:Execute snmpwalk to get number of tuners connected to the host";
        print "EXPECTED RESULT 1: snmpwalk should get number of tuners connected to the host";
        print "ACTUAL RESULT 1: %s" %actResponse;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS :Number of tuners connected to the host = %s" %noTuner ;
        #Get the tuner number using TRM module
        trmResponse=getMaxTuner(trmObj,'SUCCESS');
            
        if trmResponse== int(noTuner):
                tdkTestObj.setResultStatus("SUCCESS");
                print "[TEST EXECUTION RESULT] : SUCCESS : Number of tuners from snmpwalk same as getMaxTuner = %s" %noTuner ;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "[TEST EXECUTION RESULT] : FAILURE : Number of tuners from snmpwalk not same as getMaxTuner = %s" %noTuner ;

    else:
        tdkTestObj.setResultStatus("FAILURE");
        details = tdkTestObj.getResultDetails();
        print "TEST STEP 1:Execute snmpwalk to get number of tuners connected to the host";
        print "EXPECTED RESULT 1: snmpwalk should get number of tuners connected to the host";
        print "ACTUAL RESULT 1: %s" %actResponse;
        print "[TEST EXECUTION RESULT] : FAILURE to get number of tuners";
    obj.unloadModule("snmp");
    trmObj.unloadModule("trm");
else:
        print "FAILURE to load snmp module";
        obj.setLoadModuleStatus("FAILURE");
        print "Module loading FAILURE";

  
