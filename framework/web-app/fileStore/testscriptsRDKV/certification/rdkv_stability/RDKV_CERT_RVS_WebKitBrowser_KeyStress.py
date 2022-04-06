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
  <name>RDKV_CERT_RVS_WebKitBrowser_KeyStress</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to do stress test with keys for WebKitBrowser</synopsis>
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
    <test_case_id>RDKV_STABILITY_26</test_case_id>
    <test_objective>The objective of this test is to do stress test with keys for WebKitBrowser</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1.Wpeframework process should be up and running in the device.
2.Webinspect page should be loading after enabling WebKitBrowser.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Enable WebKitBrowser and DeviceInfo plugins.
2. Set URL for keyStress test in WebKitBrowser.
3. In a loop of minimum 100 iterations Send 10 keys using generatekey method of RDKSHell to the system.
4. Validate the key press using webinspect console logs.
5. Validate cpu load and memory usage in each iteration.
6. Revert plugins status after completing the test</automation_approch>
    <expected_output>DUT should be stable after each iteration of keypresses.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_WebKitBrowser_KeyStress</test_script>
    <skipped>No</skipped>
    <release_version>M88</release_version>
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
from web_socket_util import *
import json

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_WebKitBrowser_KeyStress');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

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
    stress_test_url = obj.url+'/fileStore/lightning-apps/KeyStressTest.html'
    webkit_console_socket = None
    keys_list = [50,51,52,53,54,55,56,57,37,38]
    max_count = StabilityTestVariables.key_stress_max_count
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"resumed","Cobalt":"deactivated","DeviceInfo":"activated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
	new_plugins_status = get_plugins_status(obj,plugins_list)
	if new_plugins_status != plugin_status_needed:
	    status = "FAILURE"
    if status == "SUCCESS" :
        webkit_console_socket = createEventListener(ip,StabilityTestVariables.webinspect_port,[],"/devtools/page/1",False)
        print "\nPre conditions for the test are set successfully"
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult()
        if current_url != None and  expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Current URL:",current_url
            print "\nSet Stress test URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",stress_test_url);
            tdkTestObj.executeTestCase(expectedResult);
            time.sleep(10)
            result = tdkTestObj.getResult();
            if expectedResult in result:
		tdkTestObj.setResultStatus("SUCCESS")
                print "\nValidate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult()
                if expectedResult in result:
                    new_url = tdkTestObj.getResultDetails();
                    if new_url == stress_test_url:
			tdkTestObj.setResultStatus("SUCCESS")
                        key_code_received = True
                        for count in range(0,max_count):
                            result_dict = {}
                            params = '{"keys":[ {"keyCode": 50,"modifiers": [],"delay":1.0,"callsign":"WebKitBrowser","client":"WebKitBrowser"},{"keyCode": 51,"modifiers": [],"delay":1.0,"callsign":"WebKitBrowser","client":"WebKitBrowser"},{"keyCode": 52,"modifiers": [],"delay":1.0,"callsign":"WebKitBrowser","client":"WebKitBrowser"},{"keyCode": 53,"modifiers": [],"delay":1.0,"callsign":"WebKitBrowser","client":"WebKitBrowser"},{"keyCode": 54,"modifiers": [],"delay":1.0,"callsign":"WebKitBrowser","client":"WebKitBrowser"},{"keyCode": 55,"modifiers": [],"delay":1.0,"callsign":"WebKitBrowser","client":"WebKitBrowser"},{"keyCode": 56,"modifiers": [],"delay":1.0,"callsign":"WebKitBrowser","client":"WebKitBrowser"},{"keyCode": 57,"modifiers": [],"delay":1.0,"callsign":"WebKitBrowser","client":"WebKitBrowser"},{"keyCode": 37,"modifiers": [],"delay":1.0,"callsign":"WebKitBrowser","client":"WebKitBrowser"},{"keyCode": 38,"modifiers": [],"delay":1.0,"callsign":"WebKitBrowser","client":"WebKitBrowser"}]}'
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                            tdkTestObj.addParameter("value",params)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            if expectedResult in result:
				tdkTestObj.setResultStatus("SUCCESS")
                                time.sleep(10)
                                if (len(webkit_console_socket.getEventsBuffer())== 0):
                                    print "\n No events occurred corresponding to key press\n"
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                                else:
                                    print "\n Checking key press events \n"
                                    for index,key in enumerate(keys_list):
                                        key_press_log_with_time = webkit_console_socket.getEventsBuffer()[index]
                                        key_press = key_press_log_with_time.split('$$$')[1]
                                        key_press_log = json.loads(key_press)
                                        key_code = key_press_log.get("params").get("message").get("text")
                                        key_code = int(key_code.split(":")[1])
                                        if key != key_code:
                                            print "Key press event is not received for Key code :",key_code
                                            tdkTestObj.setResultStatus("FAILURE")
                                            key_code_received = False
                                            break
                                    else:
                                        print "\n All key codes are received successfully \n"
                                        webkit_console_socket.clearEventsBuffer()
                                        #get the cpu load
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
                                    if not key_code_received:
                                        break
                            else:
                                print "\nError while executing generate key method\n"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\nsuccessfully completed the {} iterations \n".format(max_count)
                        cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                        json.dump(cpu_mem_info_dict,json_file)
                        json_file.close()
                        webkit_console_socket.disconnect()
                        time.sleep(5)
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
                        print "Unable to launch the URL"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print "Unable to get the URL after setting it"
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print "Failed to set the URL"
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
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
