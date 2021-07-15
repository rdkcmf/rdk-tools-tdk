##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
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
  <name>RDKV_CERT_SVS_PortScan_TCP_SCTP_INIT</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkvsecurity_executeInTM</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Scanning the TCP ports of the device with SCTP INIT scan technique to find out if additional ports are open other than the  expected list of open ports</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_SECURITY_19</test_case_id>
    <test_objective>Scanning the TCP ports of the device  with SCTP INIT technique to find out if additional ports are open other than the expected list of open ports</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. nmap tool should be installed in the TM machine
2. Open ports list corresponding to the device should be added in the device configuration file (variable $TCP_PORTS) available in fileStore/tdkvRDKServiceConfig/device.config file</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Execute the nmap with SCTP INIT scan type to scan all TCP ports of the DUT
2. From the output returned by nmap, create a list of open ports.
3. Get the expected open ports list from the device.config file (variable $TCP_PORTS) and compare it with the nmap output
4. Pass/fail the test based on the absence/presence of additional open ports</automation_approch>
    <expected_output>The open ports list generated from nmap output should not have any additional ports other than the expected open ports from the list (variable $TCP_PORTS) in the device.config</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_security</test_stub_interface>
    <test_script>RDKV_CERT_SVS_PortScan_TCP_SCTP_INIT</test_script>
    <skipped>No</skipped>
    <release_version>M87</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_security","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_SVS_PortScan_TCP_SCTP_INIT');


#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result.upper());

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('rdkvsecurity_executeInTM');
    #command to be executed for scanning tcp ports
    command = "nmap -sY " + obj.IP
    print "COMMAND : %s" %(command)
    tdkTestObj.addParameter("command", command);

    #Execute the test case in DUT
    print "Scanning the TCP open ports using SCTP Init scan type"
    tdkTestObj.executeTestCase(expectedResult);
   
    #Get the result of execution
    scanResult = tdkTestObj.getResultDetails();
    if "FAILURE" != scanResult:
        tdkTestObj.setResultStatus("SUCCESS");
        portList = []
        #The output of port scan is a multiline string from which the open port numbers needs to b saved to a list
        for line in scanResult.splitlines():
             #Port numbers are followed by "/tcp" substring
             if "/tcp" in line:
                 portList.append (line.split("/")[0])
        if not portList:
             tdkTestObj.setResultStatus("SUCCESS");
             print "SUCCESS: No TCP open ports detected"
        else:
             print "Open ports are: %s" %(portList)
             #Get the list of expected open ports from device config file
             tdkTestObj = obj.createTestStep('rdkvsecurity_getDeviceConfig')
             tdkTestObj.addParameter("basePath",obj.realpath)
             tdkTestObj.addParameter("configKey","TCP_PORTS")
             tdkTestObj.executeTestCase(expectedResult)
             expected_portList = tdkTestObj.getResultDetails()
             print "Configured expected open ports are: %s" %(expected_portList)
             if "FAILURE" not in expected_portList:
                 additional_portList = []
                 for port in portList:
                     if port not in expected_portList:
                         additional_portList.append (port)
                 if not additional_portList:
                     tdkTestObj.setResultStatus("SUCCESS");
                     print "SUCCESS: No additional TCP open ports detected"
                 else:
                     tdkTestObj.setResultStatus("FAILURE");
                     print "FAILURE: Additional TCP open ports detected!!!\nPorts: %s" %(additional_portList)
             else:
                 tdkTestObj.setResultStatus("FAILURE");
                 print "FAILURE: Failed to retrieve expected open ports list"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "FAILURE: Failed to execute nmap successfully"

    #Unload the module
    obj.unloadModule("rdkv_security");

else:
    obj.setLoadModuleStatus("FAILURE");
    print "FAILURE: Failed to load module"
