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
  <name>HWPerformance_Stress-ng_Memory_Copy</name>
  <primitive_test_id/>
  <primitive_test_name>ExecuteCommand</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Execute Stress-ng opensource performance tool to exercise processor cache and system memory by doing memcpy and memmove</synopsis>
  <groups_id/>
  <execution_time>1</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks>Stress-ng tool will be available in the later release for executions</remarks>
  <skip>true</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_HWPerformance_06</test_case_id>
    <test_objective>Execute Stress-ng opensource performance tool to exercise processor cache and system memory by doing memcpy and memmove</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG, Video Accelerator</test_setup>
    <pre_requisite>1. TDK Agent should be up and running 2. stress-ng binary should be available in DUT 3. Log parsing script HWPerf_metric_parser.sh and xml file HWPerf_metric_details.xml should be available at $TDK_PATH</pre_requisite>
    <api_or_interface_used>Executes the stress-ng binary</api_or_interface_used>
    <input_parameters>--memcpy 0 -t 30 --metrics-brief --log-file /tmp/stressng-report.txt</input_parameters>
    <automation_approch>1. Execute the stress-ng binary with the required parameters and save the log in $TDK_PATH/logs/performance.log 2. Parse the stress-ng log using HWPerf_metric_parser.sh script and save the metrices value as Json response in logparser-results.txt. 3. Return the metrices as Json response. Note. More details on stress-ng is given in corresponding manual page</automation_approch>
    <expected_output>The command should execute successfully</expected_output>
    <priority>Low</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>HWPerformance_Stress-ng_Memory_Copy</test_script>
    <skipped>No</skipped>
    <release_version>M84</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>

sysUtilObj = tdklib.TDKScriptingLibrary("systemutil","1");
sysUtilObj.configureTestCase(ip,port,'HWPerformance_Stress-ng_Memory_Copy');
sysUtilLoadStatus = sysUtilObj.getLoadModuleResult();
print "System module loading status : %s" %sysUtilLoadStatus;
#Set the module loading status
sysUtilObj.setLoadModuleStatus(sysUtilLoadStatus);

if ("SUCCESS" in sysUtilLoadStatus.upper()):
         # Execute Stress-ng and get the result
         tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand');
         App_with_args="stress-ng --memcpy 0 -t 30 --metrics-brief --log-file /tmp/stressng-report.txt;"
         Parse_log="sh $TDK_PATH/HWPerf_metric_parser.sh stress-ng_Memory_Copying;"
         Display_metric="cat $TDK_PATH/logs/logparser-results.txt"
         final_cmd = App_with_args + Parse_log + Display_metric
         print final_cmd;
         tdkTestObj.addParameter("command", final_cmd);
         tdkTestObj.executeTestCase("SUCCESS");
         actualresult = tdkTestObj.getResult();
         details = tdkTestObj.getResultDetails().strip();
         expectedresult = "SUCCESS"
         print "Json reponse: %s" %details
         if expectedresult in actualresult:
                 tdkTestObj.setResultStatus("SUCCESS");
                 print "[TEST EXECUTION RESULT] : SUCCESS"
         else:
                 tdkTestObj.setResultStatus("FAILURE");
                 print "[TEST EXECUTION RESULT] : FAILURE"
        
         #Unload systemutil module
         sysUtilObj.unloadModule("systemutil");
