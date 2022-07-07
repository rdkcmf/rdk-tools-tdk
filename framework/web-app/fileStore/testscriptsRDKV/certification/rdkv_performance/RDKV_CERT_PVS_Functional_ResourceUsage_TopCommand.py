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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>2</version>
  <name>RDKV_CERT_PVS_Functional_ResourceUsage_TopCommand</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to get the top command output of device.</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_15</test_case_id>
    <test_objective>The objective of this test is to get the top command output of device.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Execute the top command in DUT and find the output.
2. Verify any process has %CPU more than 90.
3. Execute top command with option to sort based on %MEM .
4. Verify any process has %MEM more than 90.
</automation_approch>
    <expected_output>No process should have %CPU more 90 or %MEM more than 90</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_ResourceUsage_TopCommand</test_script>
    <skipped>No</skipped>
    <release_version>M84</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import json
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_ResourceUsage_TopCommand');


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
        #command to get the top output
        command = "top -b -n 1 -o +%CPU -w 512 | awk '/PID USER/,0' | awk '{print $9,$12}' | awk '{if($1>90)print $1,$2}'"
        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
        tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
        tdkTestObj.addParameter("command",command)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        output = tdkTestObj.getResultDetails()
        if output != "EXCEPTION" and expectedResult in result:
            print "Checking %CPU of processes\n"
            if output.split("\n")[1] == "" :
                print "\n No process has CPU usage greater than 90% \n"
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "\n Process details with CPU usage greater than 90% :\n"
                output = output.split("\n")
                output.pop(0)
                print "\n %CPU \t COMMAND"
                for line in output:
                    print line
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "Error occurred during SSH, please check ssh details in configuration file"
            tdkTestObj.setResultStatus("FAILURE")
        command = "top -b -n 1 -o +%MEM -w 512 | awk '/PID USER/,0' | awk '{print $10,$12}' | awk '{if($1>90)print $1,$2}'"
        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
        tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
        tdkTestObj.addParameter("command",command)
        tdkTestObj.executeTestCase(expectedResult)
        output = tdkTestObj.getResultDetails()
        result = tdkTestObj.getResult()
        if output != "EXCEPTION" and expectedResult in result:
            print "\n Checking %MEM of processes:\n"
            if output.split("\n")[1] == "" :
                print "\n No process has Memory usage greater than 90% \n"
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "\n Process details with Memory usage greater than 90% :\n"
                output = output.split("\n")
                output.pop(0)
                print "\n %MEM \t COMMAND"
                for line in output:
                    print line
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
