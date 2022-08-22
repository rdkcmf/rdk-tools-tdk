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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PVS_Browser_Animation_FPS</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to validate the average fps value obtained from the browser performance benchmark test.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>4</execution_time>
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
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_92</test_case_id>
    <test_objective>The objective of this test is to validate the average fps value obtained from the browser performance benchmark test.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>animation_benchmark_test_url:string</input_parameters>
    <automation_approch>1. Launch WebKitBrowser using RDKShell
2. Set browser test URL using url method
3. Get the current URL and verify
4. Get the 5 different fps values using webinspect page of WebKit and take the average of those 5
5. Validate the score and revert the plugin status </automation_approch>
    <expected_output>The browser score from animation benchmark test should be within the expected range</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Browser_Animation_FPS</test_script>
    <skipped>No</skipped>
    <release_version>M96</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib
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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Browser_Animation_FPS')

# Execution Summary Variable
Summ_list=[]

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    browser_test_url=BrowserPerformanceVariables.animation_benchmark_test_url
    print "\n Check Pre conditions"
    sub_category_failure = False
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status,curr_webkit_status,curr_cobalt_status = check_pre_requisites(obj)
    print "Current values \nWebKitBrowser:%s\nCobalt:%s"%(curr_webkit_status,curr_cobalt_status)
    if status == "FAILURE":
        if "FAILURE" not in (curr_webkit_status,curr_cobalt_status):
            #Need to revert the values since we are changing plugin status
            revert="YES"
            set_status = set_pre_requisites(obj)
            if set_status == "SUCCESS":
                status,webkit_status,cobalt_status = check_pre_requisites(obj)
            else:
                status = "FAILURE"
        else:
            status = "FAILURE"
    if status == "SUCCESS":
        print "\nPre conditions for the test are set successfully"
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue')
        tdkTestObj.addParameter("method","WebKitBrowser.1.url")
        tdkTestObj.executeTestCase(expectedResult)
        current_url = tdkTestObj.getResultDetails()
        result = tdkTestObj.getResult()
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            print "Current URL:",current_url
            print "\nSet test URL"

            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","WebKitBrowser.1.url")
            tdkTestObj.addParameter("value",browser_test_url)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if expectedResult in  result:
                time.sleep(10)

                print "\nValidate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue')
                tdkTestObj.addParameter("method","WebKitBrowser.1.url")
                tdkTestObj.executeTestCase(expectedResult)
                new_url = tdkTestObj.getResultDetails()
                result = tdkTestObj.getResult()
                if new_url == browser_test_url and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print "URL(",new_url,") is set successfully"

                    time.sleep(20)
                    tdkTestObj = obj.createTestStep('rdkservice_getBrowserScore_AnimationBenchmark')
                    tdkTestObj.executeTestCase(expectedResult)
                    browser_score_dict = json.loads(tdkTestObj.getResultDetails())
                    result = tdkTestObj.getResult()
                    if browser_score_dict["main_score"] != "Unable to get the browser score" and expectedResult in result:
                        tdkTestObj.setResultStatus("SUCCESS");
                        browser_score = browser_score_dict["main_score"]
                        conf_file,result = getConfigFileName(tdkTestObj.realpath)
                        result1, animation_threshold_value = getDeviceConfigKeyValue(conf_file,"ANIMATION_BENCHMARK_THRESHOLD_VALUE")
                        if animation_threshold_value != "":
                            print "\n Browser score from test: ",browser_score
                            Summ_list.append('Browser score from test: {} '.format(browser_score))
                            print "\n Threshold value for browser score:",animation_threshold_value
                            Summ_list.append('Threshold value for browser score: {}'.format(animation_threshold_value))
                            if float(browser_score) > float(animation_threshold_value):
                                print "\n The browser performance score is high as expected\n"
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print "\n The browser performance score is lower than expected \n"
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print "Failed to get the threshold value from config file"
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print "Failed to get the browser score"
                else:
                    print "Failed to load the URL",new_url
                    tdkTestObj.setResultStatus("FAILURE")
                #Set the URL back to previous
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","WebKitBrowser.1.url")
                tdkTestObj.addParameter("value",current_url)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if result == "SUCCESS":
                    print "URL is reverted successfully"
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print "Failed to revert the URL"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print "Failed to set URL to webkitbrowser"
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print "Failed to get URL in webkitbrowser"
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE")

    getSummary(Summ_list,obj)
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = revert_value(curr_webkit_status,curr_cobalt_status,obj)
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
