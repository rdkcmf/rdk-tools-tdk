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
  <name>RDKV_CERT_RVS_WebKitBrowser_Video_FPS</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to play a YouTube URL in WebKitBowser and validate FPS for 6 hrs.</synopsis>
  <groups_id/>
  <execution_time>380</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <test_cases>
    <test_case_id>RDKV_STABILITY_36</test_case_id>
    <test_objective>The objective of this test is to play a YouTube URL in WebKitBowser and validate FPS for 6 hrs.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Launch WebkitBrowser using RDKShell
2. Set URL of a YouTube video using url method.
3. Check the fps value using the fps method of WebKitBrowser.
4. Validate the average fps value in every 1hr for total 6hrs
 </automation_approch>
    <expected_output>The average fps value must be greater than the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_WebKitBrowser_Video_FPS</test_script>
    <skipped>No</skipped>
    <release_version>M89</release_version>
    <remarks/>
  </test_cases>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <script_tags/>
</xml>

'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
import StabilityTestVariables
from StabilityTestUtility import *
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_WebKitBrowser_Video_FPS');

output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}
test_interval = 120

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"resumed","Cobalt":"deactivated","DeviceInfo":"activated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        new_plugin_status = get_plugins_status(obj,plugins_list)
        if new_plugin_status != plugin_status_needed:
            status = "FAILURE"
    test_duration = StabilityTestVariables.fps_test_duration
    conf_file,file_status = getConfigFileName(obj.realpath)
    fps_config_status,fps_threshold = getDeviceConfigKeyValue(conf_file,"EXPECTED_FPS")
    offset_status,offset = getDeviceConfigKeyValue(conf_file,"FPS_THRESHOLD")
    video_url = StabilityTestVariables.cobalt_test_url
    if status == "SUCCESS" and all(value != "" for value in (fps_threshold,offset,video_url)):
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue')
        tdkTestObj.addParameter("method","WebKitBrowser.1.url")
        tdkTestObj.executeTestCase(expectedResult)
        current_url = tdkTestObj.getResultDetails()
        result = tdkTestObj.getResult()
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","WebKitBrowser.1.url")
            tdkTestObj.addParameter("value",video_url)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if result == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(60)
                print "\n Check whether URL is set"
                tdkTestObj = obj.createTestStep('rdkservice_getValue')
                tdkTestObj.addParameter("method","WebKitBrowser.1.url")
                tdkTestObj.executeTestCase(expectedResult)
                webkit_url = tdkTestObj.getResultDetails()
		print webkit_url
                result = tdkTestObj.getResult()
                if video_url in webkit_url  and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print "\n URL: {} is set successfully".format(video_url)
                    test_time_in_mins = int(StabilityTestVariables.fps_test_duration)
                    test_time_in_millisec = test_time_in_mins * 60 * 1000
                    time_limit = int(round(time.time() * 1000)) + test_time_in_millisec
                    iteration = 0
                    completed = True
                    total_fps = 0
                    frequency = 30
                    while int(round(time.time() * 1000)) < time_limit:
                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                        tdkTestObj.addParameter("method","WebKitBrowser.1.fps")
                        tdkTestObj.executeTestCase(expectedResult)
                        fps = tdkTestObj.getResultDetails()
                        result = tdkTestObj.getResult()
                        if expectedResult in result:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print "\n FPS value : {}".format(fps)
                            total_fps += int(fps)
                            result_dict = {}
                            iteration += 1
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
                                    print "\n Memory usage is high :{}% after {} iterations".format(memory_usage,iteration)
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                                else:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print "\n Memory usage is {}% after {} iterations".format(memory_usage,iteration)
                            else:
                                print "\n Unable to get the memory usage"
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                            result_dict["iteration"] = iteration
                            result_dict["cpu_load"] = float(cpuload)
                            result_dict["memory_usage"] = float(memory_usage)
                            result_dict_list.append(result_dict)
                            time.sleep(test_interval)
                            if iteration % frequency == 0:
                                avg_fps = total_fps / frequency
                                total_fps = 0
                                if avg_fps < ( int(fps_threshold) - int(offset)):
                                    print "\n Average FPS value is : {} which is less than threshold value".format(avg_fps)
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                                else:
                                    print "\n Average FPS value is : {} which is greater than threshold value".format(avg_fps)
                        else:
                            print "\n Error while getting fps value"
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        print "\n Successfully completed {} iterations in {} minutes".format(iteration,test_time_in_mins)
                    cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                    json.dump(cpu_mem_info_dict,json_file)
                    json_file.close()
                else:
                    print "\n Unable to set the video URL in WebkitBrowser"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while setting video URL in WebKitBrowser"
                tdkTestObj.setResultStatus("FAILURE")
            #Set the URL back to previous
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",current_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if result == "SUCCESS":
                print "\n URL is reverted successfully"
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                print "\n Failed to revert the URL"
                tdkTestObj.setResultStatus("FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "\n Unable to get the current URL loaded in webkit"
    else:
        print "\n Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "\n Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_stability");
else:
    print "Failed to load module"
    obj.setLoadModuleStatus("FAILURE");
