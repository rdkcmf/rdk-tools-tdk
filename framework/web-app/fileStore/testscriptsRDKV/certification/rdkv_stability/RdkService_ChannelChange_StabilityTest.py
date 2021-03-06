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
  <version>4</version>
  <name>RdkService_ChannelChange_StabilityTest</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_checkChannelChangeLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to do the stability testing by changing the channel for given number of times.</synopsis>
  <groups_id/>
  <execution_time>168</execution_time>
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
    <test_case_id>RDKV_STABILITY_01</test_case_id>
    <test_objective>The objective of this test is to do the stability testing by changing the channel for given number of times.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. Channel change URL
2. Number of channel change
3. Maximum allowed CPU load
4. Maximum allowed Memory usage
</input_parameters>
    <automation_approch>1. As pre requisite, disable all the other plugins and enable webkitbrowser only.
2. Get the current URL in webkitbrowser
3. Load the application to change channels for a given number of times.
4.Validate the channel change using events
5. Check if the CPU load and Memory usage is within the expected value.
6.Revert all values before exiting</automation_approch>
    <expected_output>Channel should change for the given number of times. The cpu load and memory usage must be within the expected values.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RdkService_ChannelChange_StabilityTest</test_script>
    <skipped>No</skipped>
    <release_version>M82</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from rdkv_performancelib import *
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
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    channel_change_url = StabilityTestVariables.channel_change_url
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugin_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    plugins_cur_status_dict = get_plugins_status(obj,plugin_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"resumed","Cobalt":"deactivated","DeviceInfo":"activated"}
    if plugin_status_needed != plugins_cur_status_dict :
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
    if status == "SUCCESS":
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult()
        current_url = tdkTestObj.getResultDetails();
	if current_url != None and expectedResult in result:
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
            result1 = tdkTestObj.getResult()
            new_url = tdkTestObj.getResultDetails();
	    if new_url == channel_change_url and expectedResult == (result and result1):
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
                            tdkTestObj.setResultStatus("SUCCESS")
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
			        tdkTestObj.addParameter('value',float(cpuload))
			        tdkTestObj.addParameter('threshold',90.0)
			        tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult();
			        is_high_cpuload = tdkTestObj.getResultDetails()
      			        if is_high_cpuload == "YES" or  expectedResult not in result:
			            error_msg = "\ncpu load is high :{}% at channel change :{} times\nchannel_info:{}\n".format(cpuload,channel_change_count,remarks)
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
				tdkTestObj = obj.createTestStep('rdkservice_validateMemoryUsage')
                                tdkTestObj.addParameter('value',float(memory_usage))
                                tdkTestObj.addParameter('threshold',90.0)
				tdkTestObj.executeTestCase(expectedResult)
				is_high_memory_usage = tdkTestObj.getResultDetails()
                                result  =  tdkTestObj.getResult()
				if is_high_memory_usage == "YES" or expectedResult not in result:
				    error_msg = "\nmemory usage is high :{} % at channel change:{} times\nchannel_info:{}\n".format(memory_usage,channel_change_count,remarks)
				    tdkTestObj.setResultStatus("FAILURE")
                                    break
                                else:
                                    tdkTestObj.setResultStatus("SUCCESS")
				    print "\nmemory usage is {}% at channel change {} times\n".format(memory_usage,channel_change_count)
			    else:
				error_msg = "\n Unable to get the memory usage\n"
				tdkTestObj.setResultStatus("FAILURE")
				break
			    result_dict["iteration"] = channel_change_count
                            result_dict["remarks"] = remarks
                            result_dict["cpu_load"] = float(cpuload)
                            result_dict["memory_usage"] = float(memory_usage)
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
	        cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
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
		print "Failed to load the URL:{}, Current URL:{}".format(channel_change_url,new_url)
		tdkTestObj.setResultStatus("FAILURE");
	else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to get the current URL loaded in webkit"
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,plugins_cur_status_dict)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
