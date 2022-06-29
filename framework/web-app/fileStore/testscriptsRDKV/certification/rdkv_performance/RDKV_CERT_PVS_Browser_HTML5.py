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
  <name>RDKV_CERT_PVS_Browser_HTML5</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getBrowserScore_HTML5</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To get the browser score using HTML5 test</synopsis>
  <groups_id/>
  <execution_time>4</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_05</test_case_id>
    <test_objective>To get the browser score using HTML5 test</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. Threshold value of HTML5 score
2. HTML5 test url</input_parameters>
    <automation_approch>1. As a pre requisite disable all other plugins and enable webkitbrowser plugin.
2. Load the HTML5 Browser test URL
3. Get the final score and validate it
4. Revert all values</automation_approch>
    <expected_output>The browser score from HTML5 should be in the expected range</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Browser_HTML5</test_script>
    <skipped>No</skipped>
    <release_version>M82</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from BrowserPerformanceUtility import *
import BrowserPerformanceUtility
from rdkv_performancelib import *
import rdkv_performancelib
import BrowserPerformanceVariables
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Browser_HTML5')

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

# Execution Summary Variable
Summ_list=[]

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    browser_test_url=BrowserPerformanceVariables.html5_test_url
    browser_subcategory_list = BrowserPerformanceVariables.html5_test_subcategory_list
    sub_category_failure = False
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status,curr_webkit_status,curr_cobalt_status = check_pre_requisites(obj)
    print "Current values \nWebKitBrowser:%s\nCobalt:%s"%(curr_webkit_status,curr_cobalt_status);
    if status == "FAILURE":
        if "FAILURE" not in (curr_webkit_status,curr_cobalt_status):
            set_status= set_pre_requisites(obj)
	    #Need to revert the values since we are changing plugin status
            revert="YES"
            if set_status == "SUCCESS":
                status,webkit_status,cobalt_status = check_pre_requisites(obj)
            else:
                status = "FAILURE"
    if status == "SUCCESS":
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult();
        current_url = tdkTestObj.getResultDetails();
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Current URL:",current_url
            print "\nSet HTML5 test URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",browser_test_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in result:
                time.sleep(10)
                print "\nValidate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult()
                new_url = tdkTestObj.getResultDetails();
                if new_url == browser_test_url and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "URL(",new_url,") is set successfully"
                    time.sleep(20)
	            tdkTestObj = obj.createTestStep('rdkservice_getBrowserScore_HTML5');
                    tdkTestObj.executeTestCase(expectedResult);
                    result = tdkTestObj.getResult()
                    browser_score_dict = json.loads(tdkTestObj.getResultDetails());
                    if browser_score_dict["main_score"] != "Unable to get the browser score" and expectedResult in result:
                        tdkTestObj.setResultStatus("SUCCESS")
	                browser_score = int(browser_score_dict["main_score"].split()[0])
	                print "\n validating browser score with threshold value:"
	                conf_file,result = getConfigFileName(tdkTestObj.realpath)
                        result1, html5_threshold_value = getDeviceConfigKeyValue(conf_file,"HTML5_THRESHOLD_VALUE")
                        result2, html5_subcategory_threshold_values = getDeviceConfigKeyValue(conf_file,"HTML5_SUBCATEGORY_THRESHOLD_VALUES")
                        if all(value != "" for value in (html5_threshold_value,html5_subcategory_threshold_values)):
                            print "\n Threshold value for browser performance main score: ",html5_threshold_value
                            Summ_list.append('Threshold value for browser performance main score:{} '.format(html5_threshold_value))
                            Summ_list.append('Browser score from test: {} '.format(browser_score))
                            if int(browser_score) > int(html5_threshold_value):
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "\n The browser performance main score is high as expected\n"
                                subcategory_threshold_value_list = html5_subcategory_threshold_values.split(',')
                                for index,subcategory in enumerate(browser_subcategory_list):
                                    if int(browser_score_dict[subcategory]) < int(subcategory_threshold_value_list[index]):
                                        print "\n Subcategory {} score:{} is less than the threshold value:{} \n".format(subcategory,browser_score_dict[subcategory],subcategory_threshold_value_list[index])
                                        tdkTestObj.setResultStatus("FAILURE")
                                        sub_category_failure = True
                                if not sub_category_failure:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print "\n The subcategory scores of {} are also as high as expected\n".format(browser_subcategory_list)
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print "\n The overall browser performance is lower than expected \n"
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "\n The browser performance main score is lower than expected \n"
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "\n Failed to get the threshold value from config file \n"
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
	                print "\n Failed to get the browser score \n"
                else:
                    print "Failed to load the URL",new_url
                    tdkTestObj.setResultStatus("FAILURE");
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
                tdkTestObj.setResultStatus("FAILURE");
                print "Failed to set URL in webkitbrowser"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Failed to get URL from webkitbrowser"
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    getSummary(Summ_list)
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = revert_value(curr_webkit_status,curr_cobalt_status,obj);
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
