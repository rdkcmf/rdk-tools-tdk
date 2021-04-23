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
  <version>2</version>
  <name>RDKV_CERT_PVS_Functional_WebKitBrowser_TimeTo_LoadURL</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The script is to get the time taken for loading a url in webkitbrowser</synopsis>
  <groups_id/>
  <execution_time>6</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_09</test_case_id>
    <test_objective>The objective of the script is to get the time taken for loading a url in webkitbrowser</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>browser_test_url :string </input_parameters>
    <automation_approch>1. As a pre requisite disable all other plugins and enable WebKitBrowser plugin.
2. Set the browser_test_url (URL used to be launched) in WebKitBrowser.
3. Find the timestamps for last 2 "URLChange" logs for the given  browser_test_url .
4. Find the output by calculating the difference between above timestamps.</automation_approch>
    <expected_output>The Browser must load URL within expected range of ms.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_WebKitBrowser_TimeTo_LoadURL</test_script>
    <skipped>No</skipped>
    <release_version>M83</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from BrowserPerformanceUtility import *
import PerformanceTestVariables 
from datetime import datetime
import json
from web_socket_util import *
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_WebKitBrowser_TimeTo_LoadURL');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    event_listener = None
    browser_test_url = PerformanceTestVariables.browser_test_url
    thunder_port = PerformanceTestVariables.thunder_port
    print port
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status,curr_webkit_status,curr_cobalt_status = check_pre_requisites(obj)
    print "Current values \nWebKitBrowser:%s\nCobalt:%s"%(curr_webkit_status,curr_cobalt_status);
    if status == "FAILURE":
        if "FAILURE" not in (curr_webkit_status,curr_cobalt_status):
            set_status=set_pre_requisites(obj)
            #Need to revert the values since we are changing plugin status
            revert="YES"
            if set_status == "SUCCESS":
                status,webkit_status,cobalt_status = check_pre_requisites(obj)
            else:
                status = "FAILURE"
    if status == "SUCCESS" and browser_test_url != "":
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 5,"method": "WebKitBrowser.1.register","params": {"event": "urlchange", "id": "client.events.1" }}'],"/jsonrpc",False)
        time.sleep(5)
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult()
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Current URL:",current_url
            print "\nSet Browser test URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",browser_test_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in result:
                continue_count = 0
                url_change_count = 0
                while url_change_count < 2:
                    if (continue_count > 60):
                        print "\n URL change related events are not triggered \n"
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                    if (len(event_listener.getEventsBuffer())== 0):
                        continue_count += 1
                        time.sleep(1)
                        continue
                    event_log = event_listener.getEventsBuffer().pop(0)
                    print "\n Triggered event: ",event_log
                    json_msg = json.loads(event_log.split('$$$')[1])
                    if "urlchange" in event_log and browser_test_url in event_log:
                        if not json_msg["params"]["loaded"]:
                            url_triggered_time = event_log.split('$$$')[0]
                            url_change_count += 1
                        elif json_msg["params"]["loaded"]:
                            url_changed_time = event_log.split('$$$')[0]
                            url_change_count += 1
                        else:
                            continue_count += 1
                    else:
                        continue_count += 1
                else: 
                    print "\nValidate if the URL is set successfully or not"
                    tdkTestObj = obj.createTestStep('rdkservice_getValue');
                    tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                    tdkTestObj.executeTestCase(expectedResult);
                    new_url = tdkTestObj.getResultDetails();
                    result = tdkTestObj.getResult()
                    if browser_test_url in new_url and expectedResult in result:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "URL(",new_url,") is set successfully"
                        print "\nURL triggered at: {} (UTC)".format(url_triggered_time)
                        print "URL changed at: {} (UTC)".format(url_changed_time)
                        url_triggered_timein_millisec = getTimeInMilliSec(url_triggered_time)
                        url_changed_timin_millisec = getTimeInMilliSec(url_changed_time)
                        url_loaded_time = url_changed_timin_millisec - url_triggered_timein_millisec
                        print "Time taken to load the URL: {} ms\n".format(url_loaded_time)
                        conf_file,result = getConfigFileName(tdkTestObj.realpath)
                        result1, url_loadtime_threshold_value = getDeviceConfigKeyValue(conf_file,"URL_LOADTIME_THRESHOLD_VALUE")
                        result2,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                        if all(value != "" for value in (url_loadtime_threshold_value,offset)):
                            if 0 < int(url_loaded_time) < (int(url_loadtime_threshold_value) + int(offset)):
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "\n The time taken to load the URL is within the expected limit\n"
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "\n The time taken to load the URL is not within the expected limit \n"
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Failed to get the threshold value from config file"
                    else:
                        print "\nFailed to load the URL ",browser_test_url
                        print "current url:",new_url
                        tdkTestObj.setResultStatus("FAILURE");
                #Set the URL back to previous
                tdkTestObj = obj.createTestStep('rdkservice_setValue');
                tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                tdkTestObj.addParameter("value",current_url);
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult();
                if result == "SUCCESS":
                    print "\nURL is reverted successfully"
                    tdkTestObj.setResultStatus("SUCCESS");
                else:
                    print "\nFailed to revert the URL"
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Failed to set the URL"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "\nFailed to get current URL from webkitbrowser"
        event_listener.disconnect()
        time.sleep(5)
    else:
        print "\nPre conditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "\nRevert the values before exiting"
        status = revert_value(curr_webkit_status,curr_cobalt_status,obj);
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
