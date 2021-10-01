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
  <version>19</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_SVS_CheckSSLCertificateExpiry</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkvsecurity_executeInDUT</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Checking if the SSL certificates available in the DUT are expected to expire within the specified time</synopsis>
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
    <test_case_id>RDKV_SECURITY_03</test_case_id>
    <test_objective>Checking if the SSL Certificates present in DUT are expected to expire within the specified time</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. openssl tool must be available in the DUT
2. The path for the SSL certificates folder and the expected expiry period(in seconds) within which to check should be specified in the device.config
3. Credentials to ssh to the DUT should be available in device.config
4. Expired certificates key should be configured in config file to mention device contains expired certificates or not</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Retrieve the SSH credentials, expiry period, certificate path and expired certificate status from device.config
2. Execute the openssl command to check the expiry of each certificate in the specified folder and return the command output which is a multiline string with the "Certificate will expire"/"Certificate will not expire" string and the name of certificates that are expected to expire along with their expiry date.
3. From the output string, check if there are any certificates that are expected to expire within the specified time(with "Certificate will expire" string). The test pass/fail based on the absence/presence of "Certificate will expire" string as well as expired certificates status.</automation_approch>
    <expected_output>The multiline output string should not contain  "Certificate will expire" substring if "expired_certificates" key configured as "no"</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_security</test_stub_interface>
    <test_script>RdkvSecurity_CheckSSLCertificateExpiry</test_script>
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
obj.configureTestCase(ip,port,'RDKV_CERT_SVS_CheckSSLCertificateExpiry');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result.upper());

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    configKeyList = ["EXPIRY_PERIOD" , "CERT_PATH", "SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD", "PRESENCE_OF_EXPIRED_CERTIFICATES"]
    configValues = {}
    tdkTestObj = obj.createTestStep('rdkvsecurity_getDeviceConfig')
    #Get each configuration from device config file
    for configKey in configKeyList:
        tdkTestObj.addParameter("basePath",obj.realpath)
        tdkTestObj.addParameter("configKey",configKey)
        tdkTestObj.executeTestCase(expectedResult)
        configValues[configKey] = tdkTestObj.getResultDetails()
        if "FAILURE" not in configValues[configKey] and configValues[configKey] != "":
            print "SUCCESS: Successfully retrieved %s configuration from device config file" %(configKey)
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "FAILURE: Failed to retrieve %s configuration from device config file" %(configKey)
            if configValues[configKey] == "":
                print "\n Please configure the %s key in the device config file" %(configKey)
            tdkTestObj.setResultStatus("FAILURE")
            result = "FAILURE"
            break
    if "FAILURE" != result:
        if "directSSH" == configValues["SSH_METHOD"] :
            if configValues["SSH_PASSWORD"] == "None":
                configValues["SSH_PASSWORD"] = ""
            credentials = obj.IP + ',' + configValues["SSH_USERNAME"] + ',' + configValues["SSH_PASSWORD"]
            command = 'for pem in '+ configValues["CERT_PATH"] + '/*.pem; do if ! openssl x509 -checkend ' + configValues["EXPIRY_PERIOD"] + ' -in "$pem"; then printf \'%s: %s\\n\' "$(openssl x509 -enddate -noout -in "$pem"|cut -d= -f 2)" "$pem"; fi done'
            print "COMMAND: %s" %(command)

            #Primitive test case which associated to this Script
            tdkTestObj = obj.createTestStep('rdkvsecurity_executeInDUT');
            #Add the parameters to ssh to the DUT and execute the command
            tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
            tdkTestObj.addParameter("credentials", credentials);
            tdkTestObj.addParameter("command", command);

            #Execute the test case in DUT
            tdkTestObj.executeTestCase(expectedResult);

            #Get the result of execution
            output = tdkTestObj.getResultDetails();
            if "Certificate will expire" in output:
                certListToBeExpired = []
                for line in output.splitlines():
                    if (".pem" in line) and (line not in command):
                        certListToBeExpired.append (line)
                months = int(configValues["EXPIRY_PERIOD"])/2630000
                if "yes" in configValues["PRESENCE_OF_EXPIRED_CERTIFICATES"].lower():
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "SUCCESS: Few Certificates are expected to expire within %d months: %s\n" %(months,certListToBeExpired)
                elif "no" in configValues["PRESENCE_OF_EXPIRED_CERTIFICATES"].lower():
                    tdkTestObj.setResultStatus("FAILURE");
                    print "FAILURE: Few Certificates are expected to expire within %d months: %s\n" %(months,certListToBeExpired)
            else:
                if "yes" in configValues["PRESENCE_OF_EXPIRED_CERTIFICATES"].lower():
                    tdkTestObj.setResultStatus("FAILURE");
                    print "FAILURE: No certificate expires within specified time but configured as expired certificates are present in the device"
                elif "no" in configValues["PRESENCE_OF_EXPIRED_CERTIFICATES"].lower():
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "SUCCESS: No certificate expires within specified time"
        else:
            print "FAILURE: Currently only supports directSSH ssh method"
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print "FAILURE: Failed to get configuration values"
        tdkTestObj.setResultStatus("FAILURE");

    #Unload the module
    obj.unloadModule("rdkv_security");

else:
    #Set load module status
    obj.setLoadModuleStatus("FAILURE");
    print "FAILURE: Failed to load module"

