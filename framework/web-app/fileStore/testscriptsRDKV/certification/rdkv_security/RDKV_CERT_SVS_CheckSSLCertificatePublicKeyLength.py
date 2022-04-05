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
  <name>RDKV_CERT_SVS_CheckSSLCertificatePublicKeyLength</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkvsecurity_executeInDUT</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Checks whether all SSL certificate  public key length is greater than configured key length</synopsis>
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
    <test_case_id>RDKV_SECURITY_12</test_case_id>
    <test_objective>Checks for the ssl certificates public key length is greater than configured key length</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1.Configure the certification path (variable $CERT_PATH) and certificate public key length available in fileStore/tdkvRDKServiceConfig/device.config file</pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Retrieve the SSH credentials and certificate path from device.config
2. Execute the openssl command to check the public key length of each certificate in the specified folder and return the command output which is a multiline string with the "insecure" string and the name of certificates having public key less than a configured key length.
3. From the output string, check if there are any certificates that are having public key less than a configured public key length(with "insecure" string). The test pass/fail based on the absence/presence of "insecure" string.</automation_approch>
    <expected_output>All certificates should have  public key length not less than a configured key length</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_security</test_stub_interface>
    <test_script>RDKV_CERT_SVS_CheckSSLCertificatePublicKeyLength</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
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
obj.configureTestCase(ip,port,'RDKV_CERT_SVS_CheckSSLCertificatePublicKeyLength');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result.upper());

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    configKeyList = ["CERT_PATH", "SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD", "SSL_CERTIFICATE_KEY_LENGTH"]
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
            command =  'for pem in ' + configValues["CERT_PATH"] + '/*.pem; do if [[ $( openssl x509 -in "$pem" -text -noout | grep "Public-Key" | cut -d\( -f 2 | cut -d\'' ' \' -f 1 ) -lt ' + configValues["SSL_CERTIFICATE_KEY_LENGTH"] + '&& $( openssl x509 -in "$pem" -text -noout | grep "Public-Key" | cut -d\( -f 2 | cut -d\'' ' \' -f 1 ) -ne "0" ]]; then printf \'%s-------%d is insecure \\n\' "$pem" "$( openssl x509 -in "$pem" -text -noout | grep "Public-Key" | cut -d\( -f 2 | cut -d\'' ' \' -f 1 )"; fi done'
            print "COMMAND : %s" %(command)            
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
            if output and "FAILURE" not in output:
                shortKeyCertList = []
                for line in output.splitlines():
                    if (".pem" in line) and (line not in command) and (configValues["CERT_PATH"]+"/*.pem" not in line) and ("is insecure" in line):
                        shortKeyCertList.append (line)
                if shortKeyCertList:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "FAILURE: Few Certificates are having public key length less than configured key length %s: \n%s" %(configValues["SSL_CERTIFICATE_KEY_LENGTH"],shortKeyCertList)
                else:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "SUCCESS: All certificates are having public key length greater than configured key length"
            else:
                tdkTestObj.setResultStatus("FAILURE")
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

                                     
