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
  <version>4</version>
  <name>RDKV_CERT_RVS_Cobalt_PlayAndExit</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateProcEntry</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to launch cobalt, play video and exit continuously for multiple times and validate CPU load and memory usage.</synopsis>
  <groups_id/>
  <execution_time>1450</execution_time>
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
    <test_case_id>RDKV_STABILITY_11</test_case_id>
    <test_objective>The objective of this test is to launch cobalt, play video and exit continuously for multiple times and validate CPU load and memory usage.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. Time upto which the video should play.
2. The URL of the video to be played
</input_parameters>
    <automation_approch>1. Launch Cobalt using RDKShell.
2. Set the URL of video to be played.
3. Validate if the video is playing using proc entries
4. Validate CPU load
5. Validate memory usage
6. Exit from Cobalt.
7. Repeat above steps until a given time
8. Revert the values.</automation_approch>
    <expected_output>The video should play and exit for the given time.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_Cobalt_PlayAndExit</test_script>
    <skipped>No</skipped>
    <release_version>M85</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import StabilityTestVariables
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Cobalt_PlayAndExit');

output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"

if expectedResult in result.upper():
    cobalt_test_url = StabilityTestVariables.cobalt_test_url;
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated","DeviceInfo":"activated","Cobalt":"deactivated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
    validation_dict = get_validation_params(obj)
    if status == "SUCCESS" and validation_dict != {} :
        if validation_dict["validation_required"]:
            if validation_dict["validation_method"] == "proc_entry":
                if validation_dict["password"] == "None":
                    password = ""
                else:
                    password = validation_dict["password"]
                credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
            else:
                print "\n proc_entry validation is only supported validation method \n"
                validation_dict["validation_required"] = False
        test_time_in_mins = int(StabilityTestVariables.cobalt_play_and_exit_testtime)
        test_time_in_millisec = test_time_in_mins * 60 * 1000
        time_limit = int(round(time.time() * 1000)) + test_time_in_millisec
        iteration = 0
        completed = True
        while int(round(time.time() * 1000)) < time_limit:
            cobal_launch_status = launch_cobalt(obj)
            time.sleep(30)
            print "\n Set the URL : {} using Cobalt deeplink method".format(cobalt_test_url)
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","Cobalt.1.deeplink")
            tdkTestObj.addParameter("value",cobalt_test_url)
            tdkTestObj.executeTestCase(expectedResult)
            cobalt_result = tdkTestObj.getResult()
            time.sleep(10)
            if(cobalt_result == cobal_launch_status == expectedResult):
                tdkTestObj.setResultStatus("SUCCESS")
                print "Clicking OK to play video"
                params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                tdkTestObj.addParameter("value",params)
                tdkTestObj.executeTestCase(expectedResult)
                result1 = tdkTestObj.getResult()
                time.sleep(50)
                #Clicking OK to skip Ad
                params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                tdkTestObj.addParameter("value",params)
                tdkTestObj.executeTestCase(expectedResult)
                result2 = tdkTestObj.getResult()
                time.sleep(30)
                if "SUCCESS" == (result1 and result2):
                    if validation_dict["validation_required"]:
                        tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                        tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                        tdkTestObj.addParameter("credentials",credentials)
                        tdkTestObj.addParameter("procfile",validation_dict["validation_file"])
                        tdkTestObj.addParameter("mincdb",validation_dict["min_cdb"])
                        tdkTestObj.executeTestCase(expectedResult)
                        result_val = tdkTestObj.getResultDetails()
                        if result_val == "SUCCESS" :
                            tdkTestObj.setResultStatus("SUCCESS")
                            print "\nVideo playback is happening\n"
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print "Video playback is not happening"
                            completed =  False
                            break
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
                        tdkTestObj = obj.createTestStep('rdkservice_validateMemoryUsage')
                        tdkTestObj.addParameter('value',float(memory_usage))
                        tdkTestObj.addParameter('threshold',90.0)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        is_high_memory_usage = tdkTestObj.getResultDetails()
                        if is_high_memory_usage == "YES" or expectedResult not in result:
                            print "\nmemory usage is high :{}% after {} iterations\n".format(memory_usage,iteration)
                            tdkTestObj.setResultStatus("FAILURE")
                            completed = False
                            break
                        else:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print "\nmemory usage is {}% after {} iterations".format(memory_usage,iteration)
                    else:
                        print "\n Unable to get the memory usage\n"
                        tdkTestObj.setResultStatus("FAILURE")
                        completed = False
                        break
                    result_dict["iteration"] = iteration
                    result_dict["cpu_load"] = float(cpuload)
                    result_dict["memory_usage"] = float(memory_usage)
                    result_dict_list.append(result_dict)
                    #Deactivate cobalt
                    print "\n Exiting from Cobalt \n"
                    tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
                    tdkTestObj.addParameter("plugin","Cobalt")
                    tdkTestObj.addParameter("status","deactivate")
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if result == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print "Unable to deactivate Cobalt"
                        tdkTestObj.setResultStatus("FAILURE")
                        completed = False
                        break 
                else:
                    print "Unable to press OK button"
                    tdkTestObj.setResultStatus("FAILURE")
                    completed = False
                    break
            else:
                print "Unable to launch the url"
                tdkTestObj.setResultStatus("FAILURE")
                completed = False
                break
        if(completed):
            print "\nsuccessfully completed the {} times in {} minutes".format(iteration,test_time_in_mins)
        cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
        json.dump(cpu_mem_info_dict,json_file)
        json_file.close()
        #Deactivate cobalt if any error happend
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
        tdkTestObj.addParameter("plugin","Cobalt")
        tdkTestObj.addParameter("status","deactivate")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "Unable to deactivate Cobalt"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
