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
  <name>RDKV_CERT_SVS_CheckSSHLegalBanners</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkvsecurity_executeInDUT</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Checks for the presence and contents of legal banner file</synopsis>
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
    <test_case_id>RDKV_SECURITY_11</test_case_id>
    <test_objective>Checks existence and presence of contents of ssbanner file</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Configure the availability of ssh banner file (variable $SSH_BANNER_AVAILABLE) available in fileStore/tdkvRDKServiceConfig/device.config file</pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Check the configured availability of ssh banner file
2. Check the presence of contents in banner file if availability is yes
3. Pass/fail the test based on the availability configured and presence of contents of banner file</automation_approch>
    <expected_output>SSH banner file should exists if configured availability as yes</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_security</test_stub_interface>
    <test_script>RDKV_CERT_SVS_CheckSSHLegalBanners</test_script>
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
obj.configureTestCase(ip,port,'RDKV_CERT_SVS_CheckSSHLegalBanners');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result.upper());

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Retrieving Configuration values from config file......."
    configKeyList = ["SSH_BANNER_AVAILABLE", "SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD"]
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
            print "Checking whether SSH Legal Banner file exists or not"
            command = '[ -f "/etc/sshbanner.txt" ] && echo 1 || echo 0'
            print "COMMAND : %s" %(command)
            tdkTestObj = obj.createTestStep('rdkvsecurity_executeInDUT')
            tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
            tdkTestObj.addParameter("credentials", credentials);
            tdkTestObj.addParameter("command", command);
            tdkTestObj.executeTestCase(expectedResult);
            output = tdkTestObj.getResultDetails();
            output = str(output).split("\n")
            if configValues["SSH_BANNER_AVAILABLE"].lower() == "yes" and int(output[1]) == 1:
                print "SUCCESS: SSH Legal Banner file exists checking presence of contents........"
                tdkTestObj.setResultStatus("SUCCESS")
                command = '[ -s "/etc/sshbanner.txt" ] && echo 1 ||  echo 0'
                print "COMMAND : %s" %(command)
                tdkTestObj = obj.createTestStep('rdkvsecurity_executeInDUT');
                tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
                tdkTestObj.addParameter("credentials", credentials);
                tdkTestObj.addParameter("command", command);
                tdkTestObj.executeTestCase(expectedResult);
                output = tdkTestObj.getResultDetails();
                output = str(output).split("\n")
                if int(output[1]) == 1:
                    print "SUCCESS: Contents present in legal banner file"
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print "FAILURE: Legal banner file is empty"
                    tdkTestObj.setResultStatus("FAILURE")
                
            elif configValues["SSH_BANNER_AVAILABLE"].lower() == "no"  and int(output[1]) == 0:
                print "SUCCESS: SSH Legal Banner file not present in the device as configured"
                tdkTestObj.setResultStatus("SUCCESS")
            elif configValues["SSH_BANNER_AVAILABLE"].lower() == "yes"  and int(output[1]) == 0:
                print "FAILURE: SSH Legal Banner file not present in the device but configured availability as YES"
                tdkTestObj.setResultStatus("FAILURE")
            elif configValues["SSH_BANNER_AVAILABLE"].lower() == "no"  and int(output[1]) == 1:
                print "FAILURE: SSH Legal Banner file present in the device but configured as NO"
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

                                                
