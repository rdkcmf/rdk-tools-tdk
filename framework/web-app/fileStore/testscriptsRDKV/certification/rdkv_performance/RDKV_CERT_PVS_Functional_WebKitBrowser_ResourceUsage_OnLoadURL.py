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
  <name>RDKV_CERT_PVS_Functional_WebKitBrowser_ResourceUsage_OnLoadURL</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to get and validate the resource usage on launching the WebKitBrowser and load a URL in it.</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-HYB</box_type>
    <box_type>RPI-Client</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_69</test_case_id>
    <test_objective>The objective of this test is to get and validate the resource usage on launching the WebKitBrowser and load a URL in it.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>browser_test_url:string</input_parameters>
    <automation_approch>1. Launch WebKitBrowser using RDKShell
2. Register for the urlchange event
3. Set a URL in WebKitBrowser using WebKitBrowser.1.url method.
4. Verify whether URL is changed using urlchange event.
5. Validate the resource usage by DeviceInfo.1.systemInfo method
6. Revert the status of WebKitBrowser </automation_approch>
    <expected_output>URL should be launched successfully and resource usage must be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_WebKitBrowser_ResourceUsage_OnLoadURL</test_script>
    <skipped>No</skipped>
    <release_version>M93</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import PerformanceTestVariables
from BrowserPerformanceUtility import *
from web_socket_util import *
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_WebKitBrowser_ResourceUsage_OnLoadURL');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    event_listener = None
    browser_test_url = PerformanceTestVariables.browser_test_url
    thunder_port = PerformanceTestVariables.thunder_port
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
    time.sleep(10)
    if status == "SUCCESS" and browser_test_url != "":
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 5,"method": "WebKitBrowser.1.register","params": {"event": "urlchange", "id": "client.events.1" }}'],"/jsonrpc",False)
        time.sleep(10)
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
                tdkTestObj.setResultStatus("SUCCESS")
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
                            url_change_count += 1
                        elif json_msg["params"]["loaded"]:
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
                        print "\n URL(",new_url,") is set successfully"
                        print "\n Validating resource usage:"
                        tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                        tdkTestObj.executeTestCase(expectedResult)
                        resource_usage = tdkTestObj.getResultDetails()
                        result = tdkTestObj.getResult()
                        if expectedResult in result and resource_usage != "ERROR":
                            print "\n Resource usage is within the expected limit"
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\n Error while validating resource usage"
                            tdkTestObj.setResultStatus("FAILURE")
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
