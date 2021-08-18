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
  <name>RDKV_CERT_RVS_VideoResize</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to play a test video and resize to different sizes.</synopsis>
  <groups_id/>
  <execution_time>720</execution_time>
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
    <test_case_id>RDKV_STABILITY_34</test_case_id>
    <test_objective>The objective of this test is to play a test video and resize to different sizes.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>video_resize_max_count: int</input_parameters>
    <automation_approch>1. Launch WebKitBrowser using RDKShell.
2. Listen to webinspect console logs.
3. Load videoresize test application in WebKit.
4. In a loop of minimum 300 repeatedly press keys 5,3,4 and 5 in order to resize the video.
6. Validate whether video is resized using the console prints in webinspect page of device.
7. Validate CPU load and memory usage in each iteration.
8. Close the application and disable the WebKitBrowser plugin</automation_approch>
    <expected_output>Video must be resized in each key press and no crash is expected</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_VideoResize</test_script>
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
from web_socket_util import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_VideoResize');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}{}_{}_{}_CPUMemoryInfo.json'.format(obj.logpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}
webkit_url = obj.url+'/fileStore/lightning-apps/VideoResizeTest.html'
video_resize_max_count = StabilityTestVariables.video_resize_max_count

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    webkit_console_socket = None
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    status = "SUCCESS"
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    plugin_status_needed = {"WebKitBrowser":"resumed","Cobalt":"deactivated","DeviceInfo":"activated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        changed_plugins_status_dict = get_plugins_status(obj,plugins_list)
        if changed_plugins_status_dict != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS" :
        webkit_console_socket = createEventListener(ip,StabilityTestVariables.webinspect_port,[],"/devtools/page/1",False)
        print "\nPre conditions for the test are set successfully"
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult();
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Current URL:",current_url
            print "\nSet test URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",webkit_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in  result:
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(5)
                print "\nValidate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                tdkTestObj.executeTestCase(expectedResult);
                new_url = tdkTestObj.getResultDetails();
                result = tdkTestObj.getResult()
                if webkit_url in new_url and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "URL(",new_url,") is set successfully"
                    keys_list = ["2","3","4","5"]
                    keypress_dict = {"2":"50","3":"51","4":"52","5":"53"}
                    key_resolution_dict = {"2":"640x480","3":"1280x720","4":"780x600","5":"500x500"}
                    error_in_loop = False
                    for count in range(0,video_resize_max_count):
                        result_dict = {}
                        for key in keys_list:
                            print "\n Pressing key:{}".format(key)
                            params = '{"keys":[ {"keyCode": '+keypress_dict[key]+',"modifiers": [],"delay":1.0}]}'
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                            tdkTestObj.addParameter("value",params)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            if expectedResult in result:
                                time.sleep(3)
                                print "\n Check whether video is resized \n"
                                width = key_resolution_dict[key].split('x')[0]
                                height = key_resolution_dict[key].split('x')[1]
                                for event in webkit_console_socket.getEventsBuffer():
                                    if "Resizing video to" in event:
                                        resize_log = json.loads(event)
                                        resize_params = resize_log.get("params").get("message").get("parameters")
                                        webkit_console_socket.clearEventsBuffer()
                                        break
                                else:
                                    print "\n Unable to find resize logs corresponding to keycode :{}".format(keypress_dict[key])
                                    tdkTestObj.setResultStatus("FAILURE")
                                    error_in_loop = True
                                    break
                                width_set =  str(resize_params[1]["value"])
                                height_set = str(resize_params[2]["value"])
                                if width in width_set and height in height_set:
                                    print "\n Successfully set size to {}".format(key_resolution_dict[key])
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print "\n Error while setting size to {}".format(key_resolution_dict[key]) 
                                    tdkTestObj.setResultStatus("FAILURE")
                                    error_in_loop = True
                                    break
                            else:
                                print "\n Error while sending key {}".format(keypress_dict[key])
                                tdkTestObj.setResultStatus("FAILURE")
                                error_in_loop = True
                                break
                        if error_in_loop:
                            print "\n Stopping the test"
                            break
                        print "\n ##### Validating CPU load and memory usage #####\n"
			print "Iteration : ", count+1
            		tdkTestObj = obj.createTestStep('rdkservice_validateResourceUsage')
            		tdkTestObj.executeTestCase(expectedResult)
            		status = tdkTestObj.getResult()
            		result = tdkTestObj.getResultDetails()
            		if expectedResult in status and result != "ERROR":
            		    tdkTestObj.setResultStatus("SUCCESS")
            		    cpuload = result.split(',')[0]
            		    memory_usage = result.split(',')[1]
                            result_dict["iteration"] = count+1
                            result_dict["cpu_load"] = float(cpuload)
                            result_dict["memory_usage"] = float(memory_usage)
                            result_dict_list.append(result_dict)
			else:
			    print "\n Error while validating Resource usage"
                	    tdkTestObj.setResultStatus("FAILURE")
                	    break
                    else:
                        print "\nSuccessfully completed the {} iterations \n".format(video_resize_max_count)
                    webkit_console_socket.disconnect()
                    time.sleep(5)
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
                    print "\n Error while loading videoresize application in WebKitBrowser"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while setting URL in WebKitBrowser"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Unable to get the current URL in WebKitBrowser"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
