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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_Profiling_Execute_Systemd_Analyze</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkv_profiling_systemd_analyze_execute</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test case is to execute the systemd-analyze command in the device to get stats on the service initialization</synopsis>
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
    <test_case_id>RDKV_PROFILING_19</test_case_id>
    <test_objective>The objective of this test case is to execute the systemd-analyze command in the device to get stats on the service initialization</test_objective>
    <test_type>Positive </test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>Systemd-analyze should be present in device</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device details</input_parameters>
    <automation_approch>1.Reboot the device.
    2.Execute the systemd-analyze command.
    3.Systemd-analyze output is captured in SVG file format, transfer svg file from DUT to TestManager and display it for user reference </automation_approch>
    <expected_output>To successfully get the output of systemd-analyze</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_profiling</test_stub_interface>
    <test_script>RDKV_Profiling_Execute_Systemd_Analyze</test_script>
    <skipped>No</skipped>
    <release_version>M94</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
import json
from StabilityTestUtility import *
from RDKVProfilingVariables import *
from rdkv_profilinglib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_profiling","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Profiling_Execute_Systemd_Analyze');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)
expectedResult = "SUCCESS"
conf_file = get_configfile_name(obj)
if expectedResult in result.upper():
    #rebooting the device
    rebootwaitTime = 160
    tdkTestObj = obj.createTestStep('rdkservice_rebootDevice')
    tdkTestObj.addParameter("waitTime",rebootwaitTime)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResultDetails()
    if expectedResult in result:
        tdkTestObj.setResultStatus("SUCCESS")
        print "\n Rebooted device successfully \n"
        #Get the result of systemd_analyze tool
        tdkTestObj = obj.createTestStep("rdkv_profiling_systemd_analyze_execute")
        tdkTestObj.addParameter('deviceIP',ip)
        tdkTestObj.addParameter('deviceConfig',conf_file)
        tdkTestObj.addParameter('realPath',obj.realpath)
        tdkTestObj.addParameter('logPath',obj.logpath)
        tdkTestObj.addParameter('execId',obj.execID)
        tdkTestObj.addParameter('execDeviceId',obj.execDevId)
        tdkTestObj.addParameter('execResultId',obj.resultId)
        tdkTestObj.executeTestCase(expectedResult)
        details = tdkTestObj.getResultDetails()
        result = tdkTestObj.getResult()
        if "SUCCESS" in result:
            print "\nsystemd_analyze tool execution success and transferred the log"
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "\nsystemd_analyze tool execution or log transfer failed"
            tdkTestObj.setResultStatus("FAILURE")
    else:
       print "Device is not rebooted"
       tdkTestObj.setResultStatus("FAILURE")
    obj.unloadModule("rdkv_profiling")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"

