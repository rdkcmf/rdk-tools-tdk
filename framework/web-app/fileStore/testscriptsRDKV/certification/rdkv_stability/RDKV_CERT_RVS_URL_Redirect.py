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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>3</version>
  <name>RDKV_CERT_RVS_URL_Redirect</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of the test is to stress load the system with redirects and see if the WPEWebkit process continues to operate nominally.</synopsis>
  <groups_id/>
  <execution_time>620</execution_time>
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
    <automation_approch>1. As a pre requisite disable all plugins and enable LightningApp/WebKitBrowser plugin and DeviceInfo plugin.
2. Get the current URL.
3. Load the application URL for a given time
4. Validate the redirection of URLs in webkit instance. 
5. Check the webkit instance plugin(LightningApp/WebKitBrowser) is in resumed state in each iteration
5. Check if the CPU load and Memory usage is within the expected value.
6.Revert all values before exiting</automation_approch>
    <expected_output>URL redirection should work. Webkit instance should be in resumed state during the iterations and the cpu load and memory usage must be within the expected values.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_URL_Redirect</test_script>
    <skipped>No</skipped>
    <release_version>M83</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
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
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_URL_Redirect');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}{}_{}_{}_CPUMemoryInfo.json'.format(obj.logpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}
test_interval = 120

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    stress_test_url = StabilityTestVariables.stress_test_url;
    print "\n Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    webkit_instance = StabilityTestVariables.webkit_instance
    set_method = webkit_instance+'.1.url'
    plugins_list = ["Cobalt","DeviceInfo",webkit_instance]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(20)
    status = "SUCCESS"
    plugin_status_needed = {webkit_instance:"resumed","Cobalt":"deactivated","DeviceInfo":"activated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        set_status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS" :
        print "\n Pre conditions for the test are set successfully"
        print "\n Get the URL in {}".format(webkit_instance)
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method",set_method);
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult()
        if current_url != None and  expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            print "\n Current URL:",current_url
            print "\n Set Stress test URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method",set_method);
            tdkTestObj.addParameter("value",stress_test_url);
            tdkTestObj.executeTestCase(expectedResult);
            time.sleep(10)
            result = tdkTestObj.getResult();
            if expectedResult in result:
                print "\n Validate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method",set_method);
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult()
                if expectedResult in result:
                    new_url = tdkTestObj.getResultDetails();
                    exp_url_pattern = StabilityTestVariables.expected_url_pattern
                    match_result = re.match(exp_url_pattern,new_url) 
                    if match_result:
                        run_value1 = int(new_url.split('?')[1].split('&')[0].split('=')[1])
                        print "\n Successfully set Stress test URL"
                        tdkTestObj.setResultStatus("SUCCESS")
                        test_time_in_mins = int(StabilityTestVariables.stress_test_duration)
                        test_time_in_millisec = test_time_in_mins * 60 * 1000
                        time_limit = int(round(time.time() * 1000)) + test_time_in_millisec
                        iteration = 0
                        completed = True
                        time.sleep(10)
                        while int(round(time.time() * 1000)) < time_limit:
                            tdkTestObj = obj.createTestStep('rdkservice_getValue');
                            tdkTestObj.addParameter("method",set_method);
                            tdkTestObj.executeTestCase(expectedResult);
                            result = tdkTestObj.getResult()
                            if expectedResult in result:
                                redirected_url = tdkTestObj.getResultDetails()
                                run_value2 = int(redirected_url.split('?')[1].split('&')[0].split('=')[1])
                                if run_value2 > run_value1 :
                                    print "\n URL redirecting is working fine\n"
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print "\n Get the {} plugin status:\n".format(webkit_instance)
                                    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                                    tdkTestObj.addParameter("plugin",webkit_instance)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result = tdkTestObj.getResult()
                                    webkit_status = tdkTestObj.getResultDetails()
                                    if webkit_status == 'resumed' and expectedResult in result:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print "\n {} is in resumed state\n".format(webkit_instance)
                                        result_dict = {}
                                        iteration += 1
                                        #get the cpu load
					print "Iteration : ", iteration
            				tdkTestObj = obj.createTestStep('rdkservice_validateResourceUsage')
            				tdkTestObj.executeTestCase(expectedResult)
            				status = tdkTestObj.getResult()
            				result = tdkTestObj.getResultDetails()
            				if expectedResult in status and result != "ERROR":
            				    tdkTestObj.setResultStatus("SUCCESS")
            				    cpuload = result.split(',')[0]
            				    memory_usage = result.split(',')[1]
                                            result_dict["iteration"] = iteration
                                            result_dict["cpu_load"] = float(cpuload)
                                            result_dict["memory_usage"] = float(memory_usage)
                                            result_dict_list.append(result_dict)
					else:
					    completed = False 
					    print "\n Error while validating Resource usage"
                			    tdkTestObj.setResultStatus("FAILURE")
                			    break
                                        run_value1 = run_value2
                                        time.sleep(test_interval)
                                    else:
                                        print "\n {} is not in Resumed state, current state: {} ".format(webkit_instance,webkit_status)
                                        tdkTestObj.setResultStatus("FAILURE")
                                        completed = False
                                        break
                                else:
                                    print "\n URL redirecting is not working"
                                    tdkTestObj.setResultStatus("FAILURE")
                                    completed = False
                                    break
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print "\n Unable to get the URL"
                        if(completed):
                            print "\n Successfully completed the {} times in {} minutes\n".format(iteration,test_time_in_mins)
                            #Set the URL back to previous
                            tdkTestObj = obj.createTestStep('rdkservice_setValue');
                            tdkTestObj.addParameter("method",set_method);
                            tdkTestObj.addParameter("value",current_url);
                            tdkTestObj.executeTestCase(expectedResult);
                            result = tdkTestObj.getResult();
                            if result == "SUCCESS":
                                print "\n URL is reverted successfully"
                                tdkTestObj.setResultStatus("SUCCESS");
                            else:
                                print "\n Failed to revert the URL"
                                tdkTestObj.setResultStatus("FAILURE");
                        cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                        json.dump(cpu_mem_info_dict,json_file)
                        json_file.close()
                    else:
                        print "\n Unable to launch the URL"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print "\n Unable to get the URL after setting it"
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print "\n Failed to set the URL"
        else:
            print "\n Unable to get the current URL"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "\n Failed to load module"
