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
  <name>RdkService_LongDuration_StabilityTest</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_validateProcEntry</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to do the stability testing by playing a video from Cobalt for a given amount of time and get the cpu load in every 5 mins.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>700</execution_time>
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
    <test_case_id></test_case_id>
    <test_objective></test_objective>
    <test_type></test_type>
    <test_setup></test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch></automation_approch>
    <expected_output></expected_output>
    <priority></priority>
    <test_stub_interface></test_stub_interface>
    <test_script></test_script>
    <skipped></skipped>
    <release_version></release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from BrowserPerformanceUtility import *
import BrowserPerformanceUtility
from performancelib import *
import performancelib
import StabilityTestVariables
from StabilityTestUtility import *
from SSHUtility import *
import ast
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkservices","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RdkService_LongDuration_StabilityTest');

output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}
test_interval = 300

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
	plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"activated","DeviceInfo":"activated"}
	if curr_plugins_status_dict != plugin_status_needed:
		revert = "YES"
		status = set_plugins_status(obj,plugin_status_needed)
	cobal_launch_status = launch_cobalt(obj)
	validation_dict = get_validation_params(obj)
	if status == "SUCCESS" and cobal_launch_status == "SUCCESS" and validation_dict != {} :
		print "\nPre conditions for the test are set successfully"
		print "\n Set the URL : {} usig Cobalt deeplink method".format(cobalt_test_url)
		tdkTestObj = obj.createTestStep('rdkservice_setValue')
		tdkTestObj.addParameter("method","Cobalt.1.deeplink")
		tdkTestObj.addParameter("value",cobalt_test_url)
		tdkTestObj.executeTestCase(expectedResult)
		cobalt_result = tdkTestObj.getResult()
		time.sleep(10)
		if(cobalt_result == expectedResult):
		    tdkTestObj.setResultStatus("SUCCESS")
		    print "Clicking OK to play video"
		    params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
		    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
		    time.sleep(60)
		    if result == "SUCCESS":
			tdkTestObj.setResultStatus("SUCCESS")
			test_time_in_mins = int(StabilityTestVariables.cobalt_test_duration)
                        test_time_in_millisec = test_time_in_mins * 60 * 1000
                        time_limit = int(round(time.time() * 1000)) + test_time_in_millisec
			iteration = 0
			completed = True
			while int(round(time.time() * 1000)) < time_limit:
			    if validation_dict["validation_required"]:
				if validation_dict["validation_method"] == "proc_entry":
				    if validation_dict["ssh_method"] == "directSSH":
					if validation_dict["password"] == "None":
                                            password = ""
                                        else:
                                            password = validation_dict["password"]
					credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
				    else:
					#TODO
					print "selected ssh method is {}".format(validation_dict["ssh_method"])
					pass
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
                                tdkTestObj.addParameter('value',int(cpuload))
                                tdkTestObj.addParameter('threshold',90)
                                tdkTestObj.executeTestCase(expectedResult)
                                is_high_cpuload = tdkTestObj.getResultDetails()
                                if is_high_cpuload == "YES" :
                                    print "\ncpu load is high :{} after :{} times\n".format(cpuload,iteration)
                                    tdkTestObj.setResultStatus("FAILURE")
				    completed = False
                                    break
                            	else:
				    tdkTestObj.setResultStatus("SUCCESS")
				    print "\ncpu load: {} after {} iterations\n".format(cpuload,iteration)
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
                                tdkTestObj.addParameter('threshold',float(validation_dict["memory_max_limit"]))
                                tdkTestObj.executeTestCase(expectedResult)
                                is_high_memory_usage = tdkTestObj.getResultDetails()
                                if is_high_memory_usage == "YES":
                                    print "\nmemory usage is high :{} MB after {} iterations\n".format(memory_usage,iteration)
                                    tdkTestObj.setResultStatus("FAILURE")
				    completed = False
                                    break
                                else:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print "\nmemory usage is {} MB after {} iterations".format(memory_usage,iteration)
                            else:
                                print "\n Unable to get the memory usage\n"
                                tdkTestObj.setResultStatus("FAILURE")
				completed = False
                                break
			    result_dict["iteration"] = iteration
                            result_dict["cpu_load"] = cpuload
                            result_dict["memory_usage"] = memory_usage
                            result_dict_list.append(result_dict)
                            time.sleep(test_interval)
			if(completed):
                      	    print "\nsuccessfully completed the {} times in {} minutes".format(iteration,test_time_in_mins)
			cpu_mem_info_dict["longduration_test_details"] = result_dict_list
                	json.dump(cpu_mem_info_dict,json_file)
                	json_file.close()
		    else:
                        print "Unable to press OK button"
                        tdkTestObj.setResultStatus("FAILURE")

		else:
			print "Unable to launch the url"
			tdkTestObj.setResultStatus("FAILURE")
	else:
       		print "Pre conditions are not met"
    	#Revert the values
    	if revert=="YES":
        	print "Revert the values before exiting"
        	status = set_plugins_status(obj,curr_plugins_status_dict)
    	obj.unloadModule("rdkservices");
else:
    	obj.setLoadModuleStatus("FAILURE");
    	print "Failed to load module"	
