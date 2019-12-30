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
  <version>1</version>
  <name>MocaHal_Get_SelfNode_RxDroppedPackets</name>
  <primitive_test_id/>
  <primitive_test_name>MocaHal_GetRxDroppedPackets</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To get the total number of packets dropped during reception</synopsis>
  <groups_id/>
  <execution_time>1</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_MOCA_HAL_55</test_case_id>
    <test_objective>To get the total number of packets dropped during reception</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3</test_setup>
    <pre_requisite>1.Initialize the moca handle
RMH_Initialize(NULL, NULL);
2.Destroy the moca handle at the end of the test.</pre_requisite>
    <api_or_interface_used>SoC_IMPL__RMH_Stats_GetRxDroppedPackets</api_or_interface_used>
    <input_parameters>[in]	handle	The RMH handle as preturned by RMH_Initialize.
[out]	response	The number of packets dropped</input_parameters>
    <automation_approch>1. TM loads the Moca hal agent via the test agent.
2. Using systemutil ExecuteCmd command get the rx dropped packets using linux command
3. Moca hal agent will invoke the api SoC_IMPL__RMH_Stats_GetRxDroppedPackets 
4. Check the value from mocahal interface is greater than or equal to the value from linux command and return SUCCESS/FAILURE status.</automation_approch>
    <except_output>Checkpoint 1.Verify the API call return value
                   Checkpoint 2.Verify the value from mocahal interface is greater than or equal to the value from linux command</except_output>
    <priority>High</priority>
    <test_stub_interface>libmocahalstub.so</test_stub_interface>
    <test_script>MocaHal_Get_SelfNode_RxDroppedPackets</test_script>
    <skipped>No</skipped>
    <release_version>M72</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
mocahalObj = tdklib.TDKScriptingLibrary("mocahal","2.0");
sysObj = tdklib.TDKScriptingLibrary("systemutil","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
mocahalObj.configureTestCase(ip,port,'MocaHal_Get_SelfNode_RxDroppedPackets');
sysObj.configureTestCase(ip,port,'MocaHal_Get_SelfNode_RxDroppedPackets');

#Get the result of connection with test component and STB
mocaLoadStatus = sysObj.getLoadModuleResult();
print "[MOCA HAL LIB LOAD STATUS]  :  %s" %mocaLoadStatus;
mocahalObj.setLoadModuleStatus(mocaLoadStatus.upper());
sysLoadStatus = sysObj.getLoadModuleResult();
print "[SYSTEM UTIL LIB LOAD STATUS]  :  %s" %sysLoadStatus;
sysObj.setLoadModuleStatus(sysLoadStatus.upper());

if "SUCCESS" in mocaLoadStatus.upper() and sysLoadStatus.upper():
    expectedResult="SUCCESS"

    #Prmitive test case
    tdkTestObj = mocahalObj.createTestStep('MocaHal_GetName');
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    print "RESULT: MocaHal_GetName : " , actualResult
    ifName = tdkTestObj.getResultDetails();
    print "DETAILS: MocaHal_GetName : " , ifName 

    if expectedResult in actualResult and ifName:
        tdkTestObj.setResultStatus("SUCCESS")
        print "Self node Interface name retrieved: ", ifName
        #Get RxPackets using system command
        tdkTestObj = sysObj.createTestStep('ExecuteCommand');
        cmd = "cat /sys/class/net/" + ifName + "/statistics/rx_dropped | tr -d '\n'";
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase("SUCCESS");
        actualResult = tdkTestObj.getResult();
        rxPackets = tdkTestObj.getResultDetails();
        print "RxDroppedPackets from linux command: ",rxPackets

        if expectedResult in actualResult and rxPackets:
            tdkTestObj.setResultStatus("SUCCESS")
            #Prmitive test case 
            tdkTestObj = mocahalObj.createTestStep('MocaHal_GetRxDroppedPackets');
            #Execute the test case in STB
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            print "RESULT: GetRxDroppedPackets : " , actualResult
            rxDroppedPackets = tdkTestObj.getResultDetails();
            print "DETAILS: GetRxDroppedPackets : " , rxDroppedPackets

            if expectedResult in actualResult and rxDroppedPackets:
                print "RxDroppedPackets retrieved: ", rxDroppedPackets
                if rxDroppedPackets >= rxPackets:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print "RxDroppedPackets verified"
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print "RxDroppedPackets not verified"
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print "RxDroppedPackets not retrieved"
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print "Execute command failed to get rx dropped packets"
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print "Failed to get self node interface name"

    mocahalObj.unloadModule("mocahal");
    sysObj.unloadModule("systemutil");

else:
    print "Module loading FAILURE";

