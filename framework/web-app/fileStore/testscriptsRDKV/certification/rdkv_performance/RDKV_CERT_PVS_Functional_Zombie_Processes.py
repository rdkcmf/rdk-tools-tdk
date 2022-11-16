##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2022 RDK Management
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
  <version>11</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PVS_Functional_Zombie_Processes</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this script is to find if there is any zombie process in the device</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>4</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_135</test_case_id>
    <test_objective>The objective of this script is to validate if there is any zombie is running on the device</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. SSH the device
2. Run the command to check for the zombie process
3. Validate if there is any zombie process is running on the device </automation_approch>
    <expected_output>The device should not have any zombie process running inside it</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_Zombie_Processes</test_script>
    <skipped>No</skipped>
    <release_version>M107</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import json
from rdkv_performancelib import *
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_Zombie_Processes');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    if ssh_param_dict != {} and expectedResult in result:
        tdkTestObj.setResultStatus("SUCCESS")
        #command to check the zombie process in device
        command = 'top -b1 -n1 | grep Z | wc -l'
        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
        tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
        tdkTestObj.addParameter("command",command)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        output = tdkTestObj.getResultDetails()
        if output != "EXCEPTION" and expectedResult in result:
            print "Validate zombie process:"
            zombie_count = int(output.splitlines()[1])
            if zombie_count == 0:
                print "There is no zombie process in this device"
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                #command to print the zombie process in device
                command = 'top -b1 -n1 | grep Z'
                tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                tdkTestObj.addParameter("command",command)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                output = tdkTestObj.getResultDetails()
                zombie_process = output.replace(command,"")
                print "The number of Zombie process running in the device are: {}% \n".format(zombie_count)
                tdkTestObj.setResultStatus("FAILURE")
		print "The zombie process running in this device are: {} \n".format(zombie_process)
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "Error occurred during SSH, please check ssh details in configuration file"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Please configure the SSH details in configuration file"
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"