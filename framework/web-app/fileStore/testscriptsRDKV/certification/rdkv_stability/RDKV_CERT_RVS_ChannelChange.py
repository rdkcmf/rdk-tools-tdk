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
  <version>6</version>
  <name>RDKV_CERT_RVS_ChannelChange</name>
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
    <automation_approch>1. As pre requisite, disable all the other plugins and enable webkitinstance only.
2. Get the current URL
3. Load the application to change channels for a given number of times.
4.Validate the channel change using events
5. Check if the CPU load and Memory usage is within the expected value.
6.Revert all values before exiting</automation_approch>
    <expected_output>Channel should change for the given number of times. The cpu load and memory usage must be within the expected values.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_ChannelChange</test_script>
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
import MediaValidationVariables

obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True) 

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_ChannelChange')

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

webkit_console_socket = None
channel_change_count = 1
max_channel_change_count = StabilityTestVariables.max_channel_change_count
output_file = '{}{}_{}_{}_CPUMemoryInfo.json'.format(obj.logpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    #Take the channel change URL and replace TM-IP with actual TestManager IP
    channel_change_url = StabilityTestVariables.channel_change_url
    tm_url = obj.url.split("/")[2]
    channel_change_url=channel_change_url.replace("TM-IP",tm_url)
    #Write the TestManager IP and stream path to the channels.js file
    #where the user can configure their own channels for the test.
    filename = obj.realpath+"fileStore/lightning-apps/channels.js"
    basepath = MediaValidationVariables.test_streams_base_path.replace("http:","")
    with open(filename, 'r') as the_file:
        buf = the_file.readlines()
        line_to_add = 'var basepath = "'+basepath+'"\n'
        if line_to_add in buf:
            print "The stream path is already configured"
        else:
            print "Configuring the stream path for channel change test"
            with open(filename, 'w') as out_file:
                for line in buf:
                    if line == "*/\n":
                        line = "*/\n"+line_to_add
                    out_file.write(line)
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    webkit_instance = StabilityTestVariables.webkit_instance
    set_method = webkit_instance+'.1.url'
    if webkit_instance in "WebKitBrowser":
        webinspect_port = StabilityTestVariables.webinspect_port
    elif webkit_instance in "LightningApp":
        webinspect_port = StabilityTestVariables.lightning_app_webinspect_port
    else:
        webinspect_port = StabilityTestVariables.html_app_webinspect_port
    plugin_list = [webkit_instance,"Cobalt","DeviceInfo"]
    plugins_cur_status_dict = get_plugins_status(obj,plugin_list)
    time.sleep(10)
    status = "SUCCESS"
    plugin_status_needed = {webkit_instance:"resumed","Cobalt":"deactivated","DeviceInfo":"activated"}
    if any(plugins_cur_status_dict[plugin] == "FAILURE" for plugin in plugin_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif plugin_status_needed != plugins_cur_status_dict :
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_plugins_status = get_plugins_status(obj,plugin_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS":
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method",set_method);
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult()
        current_url = tdkTestObj.getResultDetails();
	if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
	    webkit_console_socket = createEventListener(ip,webinspect_port,[],"/devtools/page/1",False)
	    time.sleep(10)
            print "Current URL:",current_url
            print "\nSet Channel change test URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method",set_method);
            tdkTestObj.addParameter("value",channel_change_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
	    print "\nValidate if the URL is set successfully or not"
            tdkTestObj = obj.createTestStep('rdkservice_getValue');
            tdkTestObj.addParameter("method",set_method);
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
                            print "\n ##### Validating CPU load and memory usage #####\n"
            		    print "Iteration : ", channel_change_count
            		    tdkTestObj = obj.createTestStep('rdkservice_validateResourceUsage')
            		    tdkTestObj.executeTestCase(expectedResult)
            		    status = tdkTestObj.getResult()
            		    result = tdkTestObj.getResultDetails()
            		    if expectedResult in status and result != "ERROR":
            		        tdkTestObj.setResultStatus("SUCCESS")
            		        cpuload = result.split(',')[0]
            		        memory_usage = result.split(',')[1]
			        result_dict["iteration"] = channel_change_count
                                result_dict["remarks"] = remarks
                                result_dict["cpu_load"] = float(cpuload)
                                result_dict["memory_usage"] = float(memory_usage)
                                result_dict_list.append(result_dict)
			    else:
				print "\n Error while validating Resource usage"
                		tdkTestObj.setResultStatus("FAILURE")
                		break
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
                tdkTestObj.addParameter("method",set_method);
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
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
