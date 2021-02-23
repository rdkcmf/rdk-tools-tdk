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
import BrowserPerformanceUtility
import BrowserPerformanceVariables
import PerformanceTestVariables 
from PerformanceTestUtility import *
from datetime import datetime

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
    browser_test_url = PerformanceTestVariables.browser_test_url
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status,curr_ux_status,curr_webkit_status,curr_cobalt_status = check_pre_requisites(obj)
    print "Current values \nWebKitBrowser:%s\nCobalt:%s"%(curr_webkit_status,curr_cobalt_status);
    if status == "FAILURE":
        if "FAILURE" not in (curr_webkit_status,curr_cobalt_status):
            set_status=set_pre_requisites(obj)
            #Need to revert the values since we are changing plugin status
            revert="YES"
            if set_status == "SUCCESS":
                status,ux_status,webkit_status,cobalt_status = check_pre_requisites(obj)
            else:
                status = "FAILURE"
    if status == "SUCCESS" and browser_test_url != "":
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
                time.sleep(30)
                print "\nValidate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                tdkTestObj.executeTestCase(expectedResult);
                new_url = tdkTestObj.getResultDetails();
                result = tdkTestObj.getResult()
                if browser_test_url in new_url and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "URL(",new_url,") is set successfully"
                    ssh_param_dict = get_ssh_params(obj)
                    if ssh_param_dict != {}:
                        if ssh_param_dict["ssh_method"] == "directSSH":
                            if ssh_param_dict["password"] == "None":
                                password = ""
                            else:
                                password = ssh_param_dict["password"]
                            credentials = ssh_param_dict["host_name"]+','+ssh_param_dict["user_name"]+','+password
                        else:
                            #TODO
                            print "selected ssh method is {}".format(ssh_param_dict["ssh_method"])
                            pass

                        print "\n checking the load time:"
                        command = 'cat /opt/logs/wpeframework.log | grep -inr URLChange:.*url.*'+browser_test_url+'\\" | tail -2'
                        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                        tdkTestObj.addParameter("credentials",credentials)
                        tdkTestObj.addParameter("command",command)
                        tdkTestObj.executeTestCase(expectedResult)
                        output = tdkTestObj.getResultDetails()
                        result = tdkTestObj.getResult()
                        if output != "EXCEPTION" and expectedResult in result:
                            if len(output.split('\n')) == 4 :
                                url_triggered_log = output.split('\n')[1]
                                url_changed_log = output.split('\n')[2]
                                if '"loaded": "true"' in url_changed_log:
                                    url_triggered_time = getTimeStampFromString(url_triggered_log)
                                    print "\nURL triggered at: {} (UTC)".format(url_triggered_time)
                                    url_changed_time = getTimeStampFromString(url_changed_log)
                                    print "URL changed at: {} (UTC)".format(url_changed_time)
                                    url_triggered_timein_millisec = getTimeInMilliSec(url_triggered_time)
                                    url_changed_timin_millisec = getTimeInMilliSec(url_changed_time)
                                    url_loaded_time = url_changed_timin_millisec - url_triggered_timein_millisec
                                    print "Time taken to load the URL: {} ms\n".format(url_loaded_time)
                                    conf_file,result = getConfigFileName(tdkTestObj.realpath)
                                    result, url_loadtime_threshold_value = getDeviceConfigKeyValue(conf_file,"URL_LOADTIME_THRESHOLD_VALUE")
                                    if result == "SUCCESS":
                                        if 0 < int(url_loaded_time) < int(url_loadtime_threshold_value):
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print "\n The time taken to load the URL is within the expected limit\n"
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print "\n The time taken to load the URL is not within the expected limit \n"
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Failed to get the threshold value from config file"
                                else:
                                    print "\n Unable to load the url:",browser_test_url
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Unable to load the url:",browser_test_url
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\nError occurred while executing the command:{} in DUT,\n Please check the SSH details\n ".format(command)
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\nSSH parameters are not configured in Device Configuration file"
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
    else:
        print "\nPre conditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print "\nRevert the values before exiting"
        status = revert_value(curr_ux_status,curr_webkit_status,curr_cobalt_status,obj);
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
