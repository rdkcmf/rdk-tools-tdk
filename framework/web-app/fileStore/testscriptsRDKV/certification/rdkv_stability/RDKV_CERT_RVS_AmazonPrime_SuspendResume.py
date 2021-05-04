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
  <version>1</version>
  <name>RDKV_CERT_RVS_AmazonPrime_SuspendResume</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to suspend and resume Amazon Prime for given number of times</synopsis>
  <groups_id/>
  <execution_time>720</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_STABILITY_31</test_case_id>
    <test_objective>The objective of this test is to suspend and resume Amazon Prime for given number of times</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>suspend_resume_max_count : int</input_parameters>
    <automation_approch>1. As pre requisite, disable all the other plugins and enable Amazon only.
2. Suspend Amazon using RDKShell plugin .
3. Resume Amazon using RDKShell plugin.
4. Check if the CPU load and Memory usage is within the expected value.
5. Repeat steps 2 to 4 for given number of times.
6. Revert all values.</automation_approch>
    <expected_output>Suspend and Resume should happen and the CPU load and memory usage must be within the expected range of values.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_AmazonPrime_SuspendResume</test_script>
    <skipped>No</skipped>
    <release_version>M88</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
from rdkv_stabilitylib import *
import StabilityTestVariables
from rdkv_performancelib import *
import StabilityTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_AmazonPrime_SuspendResume');

output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}
max_count = StabilityTestVariables.suspend_resume_max_count

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Amazon","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated","Amazon":"resumed","DeviceInfo":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
    if status == "SUCCESS":
        print "\nPre conditions for the test are set successfully"
        time.sleep(10)
        iteration = 0
        while iteration < max_count:
            suspend_status,start_suspend = suspend_plugin(obj,"Amazon")
            time.sleep(5)
            if suspend_status == expectedResult:
                tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                tdkTestObj.addParameter("plugin","Amazon")
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                amazon_status = tdkTestObj.getResultDetails()
                if amazon_status == 'suspended' and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print "\nAmazon plugin Suspended Successfully\n"
                    resume_status,start_resume = launch_plugin(obj,"Amazon")
                    time.sleep(5)
                    if resume_status == expectedResult:
                        tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                        tdkTestObj.addParameter("plugin","Amazon")
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        amazon_status = tdkTestObj.getResultDetails()
                        if amazon_status == 'resumed' and expectedResult in result:
                            print "\nAmazon plugin Resumed Successfully\n"
                            result_dict = {}
                            iteration += 1
                            #get the CPU load
                            tdkTestObj = obj.createTestStep('rdkservice_getCPULoad')
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            cpuload = tdkTestObj.getResultDetails()
                            if result == "SUCCESS":
                                tdkTestObj.setResultStatus("SUCCESS")
                                #validate the cpuload
                                tdkTestObj = obj.createTestStep('rdkservice_validateCPULoad')
                                tdkTestObj.addParameter('value',float(cpuload))
                                tdkTestObj.addParameter('threshold',90.0)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                is_high_cpuload = tdkTestObj.getResultDetails()
                                if is_high_cpuload == "YES"  or expectedResult not in result:
                                    print "\nCPU load is high :{}% after :{} times\n".format(cpuload,iteration)
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                                else:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print "\nCPU load: {}% after {} iterations\n".format(cpuload,iteration)
                            else:
                                print "Unable to get cpuload"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                            #get the memory usage
                            tdkTestObj = obj.createTestStep('rdkservice_getMemoryUsage')
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            memory_usage = tdkTestObj.getResultDetails()
                            if (result == "SUCCESS"):
                                tdkTestObj.setResultStatus("SUCCESS")
                                #validate memory usage
                                tdkTestObj = obj.createTestStep('rdkservice_validateMemoryUsage')
                                tdkTestObj.addParameter('value',float(memory_usage))
                                tdkTestObj.addParameter('threshold',90.0)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                is_high_memory_usage = tdkTestObj.getResultDetails()
                                if is_high_memory_usage == "YES" or expectedResult not in result:
                                    print "\n Memory usage is high :{}% after {} iterations\n".format(memory_usage,iteration)
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                                else:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print "\n Memory usage is {}% after {} iterations\n".format(memory_usage,iteration)
                            else:
                                print "\n Unable to get the memory usage\n"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                            result_dict["iteration"] = iteration
                            result_dict["cpu_load"] = float(cpuload)
                            result_dict["memory_usage"] = float(memory_usage)
                            result_dict_list.append(result_dict)
                        else:
                            print "Amazon plugin is not in Resumed state, current Amazon Status: ",amazon_status
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        print "Unable to set Amazon plugin to resumed state"
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                else:
                    print "Amazon is not in Suspended state, current Amazon Status: ",amazon_status
                    tdkTestObj.setResultStatus("FAILURE")
                    break
            else:
                print "Unable to set Amazon plugin to suspended state"
                break
        else:
            print "\n Successfully completed the {} iterations\n".format(iteration)
        cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
        json.dump(cpu_mem_info_dict,json_file)
        json_file.close()
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
