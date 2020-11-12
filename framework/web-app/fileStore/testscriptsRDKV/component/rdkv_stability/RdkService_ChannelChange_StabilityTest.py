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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RdkService_ChannelChange_StabilityTest</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_checkChannelChangeLog</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to do the stability testing by changing the channel for given number of times.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>168</execution_time>
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
from rdkv_performancelib import *
import rdkv_performancelib
import StabilityTestVariables
from web_socket_util import *
from StabilityTestUtility import *

obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True) 

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RdkService_ChannelChange_StabilityTest')

webkit_console_socket = None
channel_change_count = 1
max_channel_change_count = StabilityTestVariables.max_channel_change_count
output_file = '{}logs/logs/{}_{}_{}_CPUMemoryInfo.json'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    channel_change_url = StabilityTestVariables.channel_change_url
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status,curr_ux_status,curr_webkit_status,curr_cobalt_status = check_pre_requisites(obj)
    print "Current values \nUX:%s\nWebKitBrowser:%s\nCobalt:%s"%(curr_ux_status,curr_webkit_status,curr_cobalt_status);
    if status == "FAILURE":
        set_pre_requisites(obj)
        #Need to revert the values since we are changing plugin status
        revert="YES"
        status,ux_status,webkit_status,cobalt_status = check_pre_requisites(obj)
    plugin_list = ["DeviceInfo","org.rdk.ActivityMonitor"]
    plugins_cur_status = get_plugins_status(obj,plugin_list)
    plugin_status_needed = {"DeviceInfo":"activated","org.rdk.ActivityMonitor":"activated"}
    activated_result = set_plugins_status(obj,plugin_status_needed)
    conf_file,result = getConfigFileName(obj.realpath)
    if result == "SUCCESS":
	result,memory_limit = getDeviceConfigKeyValue(conf_file,"MAX_MEMORY_VALUE")
    if status == "SUCCESS" and activated_result == "SUCCESS" and result == "SUCCESS":
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
	if current_url != None:
            tdkTestObj.setResultStatus("SUCCESS");
	    webkit_console_socket = createEventListener(ip,StabilityTestVariables.webinspect_port,[],"/devtools/page/1",False)
	    time.sleep(10)
            print "Current URL:",current_url
            print "\nSet Channel change test URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",channel_change_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
	    print "\nValidate if the URL is set successfully or not"
            tdkTestObj = obj.createTestStep('rdkservice_getValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.executeTestCase(expectedResult);
            new_url = tdkTestObj.getResultDetails();
	    if new_url == channel_change_url:
                tdkTestObj.setResultStatus("SUCCESS");
                print "URL(",new_url,") is set successfully"
	        validate = False
		continue_count = 0
		check_channel_tune = True
		check_play_count = 0
		error_msg = ""
	        while True:
	            result_dict = {}
	            if (channel_change_count > max_channel_change_count) or (continue_count > 20):
	            	validate = not(continue_count > 20)
	            	break
		    if (len(webkit_console_socket.getEventsBuffer())== 0):
			continue_count += 1
			time.sleep(1)
			continue
		    console_log = webkit_console_socket.getEventsBuffer().pop(0)
		    if check_channel_tune == True:
			#checking whether Tuning print is coming
		        tdkTestObj = obj.createTestStep('rdkservice_checkChannelChangeLog')
		        tdkTestObj.addParameter('log',console_log)
		        tdkTestObj.addParameter('text','Tuning to channel')
		        tdkTestObj.executeTestCase(expectedResult)
		        result_val = tdkTestObj.getResultDetails()
		        if result_val == "SUCCESS":
		    	    tdkTestObj.setResultStatus("SUCCESS")
		    	    check_channel_tune = False
			    channel_change_log = json.loads(console_log)
			    remarks = channel_change_log.get("params").get("message").get("text")
		     	    continue
 		    else:
			#checking for playing event
		        tdkTestObj = obj.createTestStep('rdkservice_checkChannelChangeLog')
                        tdkTestObj.addParameter('log',console_log)
                        tdkTestObj.addParameter('text','Playing')
                        tdkTestObj.executeTestCase(expectedResult)
                        result_val = tdkTestObj.getResultDetails()
                        if result_val == "SUCCESS":
     		            check_channel_tune = True
     			    check_play_count = 0
     		 	    continue_count = 0
     			    tdkTestObj = obj.createTestStep('rdkservice_getCPULoad')
     			    tdkTestObj.executeTestCase(expectedResult)
     			    result = tdkTestObj.getResult()
     			    cpuload = tdkTestObj.getResultDetails()
			    if (result == "SUCCESS"):
			        tdkTestObj.setResultStatus("SUCCESS")
			        #validate the cpuload
			        tdkTestObj = obj.createTestStep('rdkservice_validateCPULoad')
			        tdkTestObj.addParameter('value',int(cpuload))
			        tdkTestObj.addParameter('threshold',90)
			        tdkTestObj.executeTestCase(expectedResult)
			        is_high_cpuload = tdkTestObj.getResultDetails()
      			        if is_high_cpuload == "YES" :
			            error_msg = "\ncpu load is high :{} at channel change :{} times\nchannel_info:{}\n".format(cpuload,channel_change_count,remarks)
                                    tdkTestObj.setResultStatus("FAILURE")
			            break
			        else:
			    	    tdkTestObj.setResultStatus("SUCCESS")
				    print "\ncpu load is:{}% at channel change: {} times\n".format(cpuload,channel_change_count)
		            else:
		   	        tdkTestObj.setResultStatus("FAILURE")
			        error_msg = "\nUnable to get cpuload\n"
				break
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
                                tdkTestObj.addParameter('threshold',float(memory_limit))
				tdkTestObj.executeTestCase(expectedResult)
				is_high_memory_usage = tdkTestObj.getResultDetails()
				if is_high_memory_usage == "YES":
				    error_msg = "\nmemory usage is high :{} MB at channel change:{} times\nchannel_info:{}\n".format(memory_usage,channel_change_count,remarks)
				    tdkTestObj.setResultStatus("FAILURE")
                                    break
                                else:
                                    tdkTestObj.setResultStatus("SUCCESS")
				    print "\nmemory usage is {} MB at channel change {} times\n".format(memory_usage,channel_change_count)
			    else:
				error_msg = "\n Unable to get the memory usage\n"
				tdkTestObj.setResultStatus("FAILURE")
				break
			    result_dict["iteration"] = channel_change_count
                            result_dict["remarks"] = remarks
                            result_dict["cpu_load"] = int(cpuload)
                            result_dict["memory_usage"] = memory_usage
                            result_dict_list.append(result_dict)
                            channel_change_count += 1
		        else:
			    check_play_count += 1
			    if(check_play_count > 4):
			        error_msg = "\nNot able to play the content after {} times channel change,remarks: {}\n".format(channel_change_count,remarks)
			        tdkTestObj.setResultStatus("FAILURE")
			        break
                if (validate):
	            print "\nSuccessfully completed {} channel changes\n".format(max_channel_change_count)
	            tdkTestObj.setResultStatus("SUCCESS")
		elif(continue_count > 20):
		    print "\nchannel change didn't happen after {}channel changes\n".format(channel_change_count)
		    tdkTestObj.setResultStatus("FAILURE")
		else:
		    print error_msg
		webkit_console_socket.disconnect()    
	        cpu_mem_info_dict["channelChangeDetails"] = result_dict_list
	        json.dump(cpu_mem_info_dict,json_file)
	        json_file.close()
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
            else:
		print "Failed to load the URL:{}, Current URL:{}".format(browser_test_url,new_url)
		tdkTestObj.setResultStatus("FAILURE");
	else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to get the current URL loaded in webkit"
    else:
        print "Pre conditions are not met"
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = revert_value(curr_ux_status,curr_webkit_status,curr_cobalt_status,obj);
    set_plugins_status(obj,plugins_cur_status)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

