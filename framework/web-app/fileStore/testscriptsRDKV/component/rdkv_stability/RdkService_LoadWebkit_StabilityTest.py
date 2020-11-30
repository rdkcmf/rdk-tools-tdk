##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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
  <name>RdkService_LoadWebkit_StabilityTest</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of the test is to stress load the system with redirects and see if the WPEWebkit process continues to operate nominally.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>300</execution_time>
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
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_STABILITY_04</test_case_id>
    <test_objective>The objective of the test is to stress load the system with redirects and see if the WPEWebkit process continues to operate nominally.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>stress_test_url : string
expected_url_pattern : string
stress_test_duration: int
</input_parameters>
    <automation_approch>1. As a pre requisite disable all plugins and enable WebKitBrowser plugin and DeviceInfo plugin.
2. Get the current URL in webkitbrowser
3. Load the application URL for a given time
4. Validate the redirection of URLs in webkit. 
5. Check webkit plugin is in resumed state in each iteration
5. Check if the CPU load and Memory usage is within the expected value.
6.Revert all values before exiting</automation_approch>
    <expected_output>URL redirection should work. WebKitBrowser should be in resumed state during the iterations and the cpu load and memory usage must be within the expected values.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RdkService_LoadWebkit_StabilityTest</test_script>
    <skipped>No</skipped>
    <release_version>M83</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
from rdkv_stabilitylib import *
import StabilityTestVariables
from rdkv_performancelib import *
import re

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RdkService_LoadWebkit_StabilityTest');

output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}
test_interval = 120

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    stress_test_url = StabilityTestVariables.stress_test_url;
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"resumed","Cobalt":"deactivated","DeviceInfo":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        status = "FAILURE"
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        plugins_status_dict = get_plugins_status(obj,plugins_list)
        if plugins_status_dict == plugin_status_needed:
            status = "SUCCESS"
    conf_file,result = getConfigFileName(obj.realpath)
    if result == "SUCCESS":
        mem_result, memory_max_limit = getDeviceConfigKeyValue(conf_file,"MAX_MEMORY_VALUE")
        if memory_max_limit == "":
            print "\n Configure MAX_MEMORY_VALUE in device specific configuration file"
    if status == "SUCCESS" and result == "SUCCESS" and  memory_max_limit != "":
        print "\nPre conditions for the test are set successfully"
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        if current_url != None:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Current URL:",current_url
            print "\nSet Stress test URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",stress_test_url);
            tdkTestObj.executeTestCase(expectedResult);
            time.sleep(10)
            result = tdkTestObj.getResult();
            print "\nValidate if the URL is set successfully or not"
            tdkTestObj = obj.createTestStep('rdkservice_getValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.executeTestCase(expectedResult);
            new_url = tdkTestObj.getResultDetails();
            exp_url_pattern = StabilityTestVariables.expected_url_pattern
            match_result = re.match(exp_url_pattern,new_url) 
            if match_result:
                run_value1 = int(new_url.split('?')[1].split('&')[0].split('=')[1])
                print "\nSuccessfully set Stress test URL"
                tdkTestObj.setResultStatus("SUCCESS")
                test_time_in_mins = int(StabilityTestVariables.stress_test_duration)
                test_time_in_millisec = test_time_in_mins * 60 * 1000
                time_limit = int(round(time.time() * 1000)) + test_time_in_millisec
                iteration = 0
                completed = True
                time.sleep(10)
                while int(round(time.time() * 1000)) < time_limit:
                    tdkTestObj = obj.createTestStep('rdkservice_getValue');
                    tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                    tdkTestObj.executeTestCase(expectedResult);
                    redirected_url = tdkTestObj.getResultDetails()
                    run_value2 = int(redirected_url.split('?')[1].split('&')[0].split('=')[1])
                    if run_value2 > run_value1 :
                        print "\nURL redirecting is working fine\n"
                        tdkTestObj.setResultStatus("SUCCESS")
                        print "\nGet the WebkitBrowser plugin status:\n"
                        tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                        tdkTestObj.addParameter("plugin","WebKitBrowser")
                        tdkTestObj.executeTestCase(expectedResult)
                        webkit_status = tdkTestObj.getResultDetails()
                        if webkit_status == 'resumed':
                            tdkTestObj.setResultStatus("SUCCESS")
                            print "\nWebKitbrowser is in resumed state\n"
                            result_dict = {}
                            iteration += 1
                            #get the cpu load
                            tdkTestObj = obj.createTestStep('rdkservice_getCPULoad')
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            cpuload = tdkTestObj.getResultDetails()
                            if result == "SUCCESS":
                                tdkTestObj.setResultStatus("SUCCESS")
                                #validate the cpuload
                                tdkTestObj = obj.createTestStep('rdkservice_validateCPULoad')
                                tdkTestObj.addParameter('value',int(cpuload))
                                tdkTestObj.addParameter('threshold',90)
                                tdkTestObj.executeTestCase(expectedResult)
                                is_high_cpuload = tdkTestObj.getResultDetails()
                                if is_high_cpuload == "YES" :
                                    print "\ncpu load is high :{}% after :{} times\n".format(cpuload,iteration)
                                    tdkTestObj.setResultStatus("FAILURE")
                                    completed = False
                                    break
                                else:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print "\ncpu load: {}% after {} iterations\n".format(cpuload,iteration)
                            else:
                                print "Unable to get cpuload"
                                tdkTestObj.setResultStatus("FAILURE")
                                completed = False
                                break
                            #get the memory usage
                            tdkTestObj = obj.createTestStep('rdkservice_getMemoryUsage')
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            memory_usage = tdkTestObj.getResultDetails()
                            if (result == "SUCCESS"):
                                tdkTestObj.setResultStatus("SUCCESS")
                                #validate memory usage
                                memory_usage = float(memory_usage)/(1024*1024)
                                tdkTestObj = obj.createTestStep('rdkservice_validateMemoryUsage')
                                tdkTestObj.addParameter('value',memory_usage)
                                tdkTestObj.addParameter('threshold',float(memory_max_limit))
                                tdkTestObj.executeTestCase(expectedResult)
                                is_high_memory_usage = tdkTestObj.getResultDetails()
                                if is_high_memory_usage == "YES":
                                    print "\nmemory usage is high :{} MB after {} iterations\n".format(memory_usage,iteration)
                                    tdkTestObj.setResultStatus("FAILURE")
                                    completed = False
                                    break
                                else:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print "\nmemory usage is {} MB after {} iterations\n".format(memory_usage,iteration)
                            else:
                                print "\n Unable to get the memory usage\n"
                                tdkTestObj.setResultStatus("FAILURE")
                                completed = False
                                break
                            result_dict["iteration"] = iteration
                            result_dict["cpu_load"] = int(cpuload)
                            result_dict["memory_usage"] = memory_usage
                            result_dict_list.append(result_dict)
                            run_value1 = run_value2
                            time.sleep(test_interval)
                        else:
                            print "WebKitBrowser is not in Resumed state, current state: ",webkit_status
                            tdkTestObj.setResultStatus("FAILURE")
                            completed = False
                            break
                    else:
                        print "\nURL redirecting is not working\n"
                        tdkTestObj.setResultStatus("FAILURE")
                        completed = False
                        break
                if(completed):
                    print "\nsuccessfully completed the {} times in {} minutes\n".format(iteration,test_time_in_mins)
                    #Set the URL back to previous
                    tdkTestObj = obj.createTestStep('rdkservice_setValue');
                    tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                    tdkTestObj.addParameter("value",current_url);
                    tdkTestObj.executeTestCase(expectedResult);
                    result = tdkTestObj.getResult();
                    if result == "SUCCESS":
                        print "URL is reverted successfully"
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        print "Failed to revert the URL"
                        tdkTestObj.setResultStatus("FAILURE");
                cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                json.dump(cpu_mem_info_dict,json_file)
                json_file.close()
            else:
                print "Unable to launch the URL"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "Unable to get the current URL in webkit"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
