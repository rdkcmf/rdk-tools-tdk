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
  <version>14</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RdkvSecurity_CheckTLSCompression</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkvsecurity_executeInTM</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Checks the TLS Compression settings</synopsis>
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
    <test_case_id>RDKV_SECURITY_06</test_case_id>
    <test_objective>Checks the TLS Compression settings</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Sslscan tool should be installed in the TM machine
2. Supported SSL/TLS protocols corresponding to the device should be added in the device configuration file (variable $SUPPORTED_SSL_TLS_PROTOCOLS) and test URL (variable $TEST_URL)  available in fileStore/tdkvRDKServiceConfig/device.config file</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Execute the sslscan with parameters to list the protocols and compression settings of the DUT
3. If supported SSL/TLS protocols  configured check whether configured  protocols are enabled
4. Check if Compression is disabled
5. Pass/fail the test based on the enabled/disabled state of the Compression feature</automation_approch>
    <expected_output> If supported SSL/TLS protocol configured,Compression must be disbaled</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_security</test_stub_interface>
    <test_script>RdkvSecurity_CheckTLSCompression</test_script>
    <skipped>No</skipped>
    <release_version>M85</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from rdkv_securitylib import *;
import rdkv_securitylib;


#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_security","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RdkvSecurity_CheckTLSCompression');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
result = obj.getLoadModuleResult();

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    configKeyList = ["SSL_SCAN_PATH","SUPPORTED_SSL_TLS_PROTOCOLS","TEST_WEB_APP_URL"]
    configValues = {}
    tdkTestObj = obj.createTestStep('rdkvsecurity_getDeviceConfig')
    #Get each configuration from device config file
    for configKey in configKeyList:
        tdkTestObj.addParameter("basePath",obj.realpath)
        tdkTestObj.addParameter("configKey",configKey)
        tdkTestObj.executeTestCase(expectedResult)
        configValues[configKey] = tdkTestObj.getResultDetails()
        if "FAILURE" not in configValues[configKey]:
            print "Successfully retrieved %s configuration from device config file" %(configKey)
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "Failed to retrieve %s configuration from device config file" %(configKey)
            tdkTestObj.setResultStatus("FAILURE")
            result = "FAILURE"
            break
    if "FAILURE" != result:
        tdkTestObj = obj.createTestStep('rdkvsecurity_executeInTM');
        command = configValues["SSL_SCAN_PATH"]+"/sslscan "+configValues["TEST_WEB_APP_URL"]
        tdkTestObj.addParameter("command", command);
        tdkTestObj.executeTestCase(expectedResult);
        Result = tdkTestObj.getResultDetails()
        if "FAILURE" not in Result:
            tdkTestObj.setResultStatus("SUCCESS")
            if not configValues["SUPPORTED_SSL_TLS_PROTOCOLS"]:
                print "No supported protocols configured"
                tdkTestObj.setResultStatus("SUCCESS")
                print "Checking TLS Compression settings........"
                for line in  Result.splitlines():
                    Compressionfound = 0;
                    if "Compression" in line and "disabled" in line:
                        Compressionfound = 1;
                        print "Compression disabled"
                        tdkTestObj.setResultStatus("SUCCESS");
                        break;
                    elif "Compression" in line and  "enabled" in line:
                        Compressionfound = 1;
                        print "Compression enabled"
                        tdkTestObj.setResultStatus("FAILURE");
                        break;
                if Compressionfound == 0:
                        print "Compression settings not found"
                        tdkTestObj.setResultStatus("FAILURE");
            else:
                supportedProtocols = configValues["SUPPORTED_SSL_TLS_PROTOCOLS"].split(",")
                print "Supported protocols %s"  %(supportedProtocols)
                print "Checking configured protocols are enabled......."
                for protocol in supportedProtocols:
                    for line in Result.splitlines():
                        if protocol in line:
                            if "enabled" in line:
                                print "%s - Enabled" %(protocol)
                                tdkTestObj.setResultStatus("SUCCESS");
                                break;
                            elif "disabled" in line:
                                print "%s - disabled" %(protocol)
                                tdkTestObj.setResultStatus("FAILURE");
                                break;
                print "Checking TLS Compression settings........"
                for line in  Result.splitlines():
                    Compressionfound = 0;
                    if "Compression" in line and "disabled" in line:
                        Compressionfound = 1;
                        print "Compression disabled"
                        tdkTestObj.setResultStatus("SUCCESS");
                        break;
                    elif "Compression" in line and  "enabled" in line:
                        Compressionfound = 1;
                        print "Compression enabled"
                        tdkTestObj.setResultStatus("FAILURE");
                        break;
                if Compressionfound == 0:
                        print "Compression settings not found"
                        tdkTestObj.setResultStatus("FAILURE");
        else:
            print "SSlScan failed"
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print "Failed to retrieve configuration values from device config file"
        tdkTestObj.setResultStatus("FAILURE");
    obj.unloadModule("rdkv_security");

else:
    obj.setLoadModuleStatus("FAILURE");

    print "Failed to load module"

