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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PVS_Functional_IOWait_Time</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this script is to validate whether the CPUs in device are waiting for a significant amount of time for the disk subsystem to catchup .</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_134</test_case_id>
    <test_objective>The objective of this script is to validate whether the CPU cores in device are waiting for a significant amount of time for the disk subsystem to catchup.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. SSH to the device
2. Check for the number of CPU cores available in the device
3. Get the iowait time using iostat tool and calculate the average wait time of each CPU cores in the device using the equation (1/no. of CPU cores) >= iowait%
4. If the iowait time% is greater than number of CPU cores, then the CPUs are waiting a significant amount of time for the disk subsystem to catch up.
 </automation_approch>
    <expected_output>The iowait time should not be greater than the available CPUs in the device</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_IOWait_Time</test_script>
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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_IOWait_Time');

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
        #command to check the number of cpu cores in the device
        command = 'grep -c processor /proc/cpuinfo'
        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
        tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
        tdkTestObj.addParameter("command",command)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        output = tdkTestObj.getResultDetails()
        CPU_cores =float(output.splitlines()[1])
        cpu_cores_percentage =float(1/CPU_cores)
        if output != "EXCEPTION" and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            #command to check the iowait time of the device using iostat tool
            command = "iostat -c | sed -n '4p' | sed 's/  */ /g' | cut -d ' ' -f5"
            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
            tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
            tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
            tdkTestObj.addParameter("command",command)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            output = tdkTestObj.getResultDetails()
            if output != "EXCEPTION" and expectedResult in result:
                iowait_time = float(output.splitlines()[1])
                print "Validate iowait time for the CPU cores"
                if iowait_time <= cpu_cores_percentage :
                    print "The iowait time is not greater than the CPUs in the device.\nCPU cores:{}\niowait time:{}%".format(CPU_cores,iowait_time)
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print "CPU cores are waiting a significant amount of time for the disk subsystem to catch up.\nCPU cores:{}\niowait time: {}% \n".format(CPU_cores,iowait_time)
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "Error occurred while checking the iowait of the device"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "Error occurred while checking the number of cores"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Please configure the SSH details in configuration file"
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
