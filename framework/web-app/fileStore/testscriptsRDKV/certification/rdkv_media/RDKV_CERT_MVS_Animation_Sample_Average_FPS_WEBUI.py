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
  <version>6</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_MVS_Animation_Sample_Average_FPS_WEBUI</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkv_media_test</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test is to launch an existing sample animation application and get the FPS value displayed in the UI using selenium and calculate the average FPS</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
    <test_case_id>RDKV_Media_Validation_41</test_case_id>
    <test_objective>Test is to launch an existing sample animation application and get the FPS value displayed in the UI using selenium and calculate the average FPS</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2.Lightning Animation app should be hosted</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>sample_animation_test_url: string
webinspect_port: string
expected_fps:int
threshold:int
element_expand_xpath:string
ui_data_xpath:string
display_variable:string
path_of_browser_executable:string</input_parameters>
    <automation_approch>1. As pre requisite, disable all the other plugins and enable webkitbrowser only.
2. Get the current URL in webkitbrowser
3. Load the Sample Animation app url
4. App performs animation and display FPS on the UI.
5. Using selenium, open the webinpect page of the webkit browser and using the xpaths provided read the FPS data for given number of times
6. Calculate average FPS value and check whether FPS obtained is greater than or equal to expected fps value (i.e) expected_fps - threshold.
7. Revert all values</automation_approch>
    <expected_output>Animation should happen and average FPS should be grater than or equal to expected fps value.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_media</test_stub_interface>
    <test_script>RDKV_CERT_MVS_Animation_Sample_Average_FPS_WEBUI</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from BrowserPerformanceUtility import *
from rdkv_performancelib import *
import MediaValidationVariables
from MediaValidationUtility import *
import re


obj = tdklib.TDKScriptingLibrary("rdkv_media","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_MVS_Animation_Sample_Average_FPS_WEBUI')

webkit_console_socket = None

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    animation_test_url = MediaValidationVariables.sample_animation_test_url

    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status,curr_ux_status,curr_webkit_status,curr_cobalt_status = check_pre_requisites(obj)
    print "Current values \nWebKitBrowser:%s\nCobalt:%s"%(curr_webkit_status,curr_cobalt_status);
    if status == "FAILURE":
        set_pre_requisites(obj)
        #Need to revert the values since we are changing plugin status
        revert="YES"
        status,ux_status,webkit_status,cobalt_status = check_pre_requisites(obj)
    #Check residentApp status and deactivate if its activated
    check_status,resapp_status,resapp_revert,resapp_url = checkAndDeactivateResidentApp(obj)
    #Reading the FPS and threshold for FPS from the device config file
    config_status = "SUCCESS"
    conf_file,result = getConfigFileName(obj.realpath)
    result1, expected_fps  = getDeviceConfigKeyValue(conf_file,"EXPECTED_FPS")
    result2, threshold     = getDeviceConfigKeyValue(conf_file,"FPS_THRESHOLD")
    if "SUCCESS" in result1 and "SUCCESS" in result2:
        if expected_fps == "" and threshold == "":
            config_status = "FAILURE"
            print "Please set expected_fps and threshold values in device config file"
    else:
        config_status = "FAILURE"
        print "Failed to get the FPS value & threshold value from device config file"
    if status == "SUCCESS" and check_status == "SUCCESS" and config_status == "SUCCESS":
        print "\nPre conditions for the test are set successfully";
        print "\nGet the URL in WebKitBrowser"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result =  tdkTestObj.getResult()
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Current URL:",current_url
            print "\nSet Canvas Animation test app URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",animation_test_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in result:
                time.sleep(10)
                print "\nValidate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                tdkTestObj.executeTestCase(expectedResult);
                new_url = tdkTestObj.getResultDetails();
                result = tdkTestObj.getResult()
                if new_url in animation_test_url and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "URL(",new_url,") is set successfully"
                    tdkTestObj = obj.createTestStep('rdkv_media_readUIData');
                    tdkTestObj.addParameter("elementExpandXpath",MediaValidationVariables.element_expand_xpath);
                    tdkTestObj.addParameter("dataXpath",MediaValidationVariables.ui_data_xpath);
                    tdkTestObj.addParameter("count",30);
                    tdkTestObj.executeTestCase(expectedResult);
                    result = tdkTestObj.getResult()
                    ui_data = tdkTestObj.getResultDetails();
                    if ui_data != "Unable to get the data from the web UI" and expectedResult in result:
                        tdkTestObj.setResultStatus("SUCCESS")
                        fps_list = []
                        for i in ui_data.split(","):
                            if i != None and re.search(r"\d+(\.\d+)?",i) != None:
                                fps_list.append(int(re.search(r"\d+(\.\d+)?",i).group(0)))
                        if len(fps_list) > 0:
                            avg_fps = sum(fps_list)/len(fps_list)
                        else:
                            avg_fps = 0
                        print "Collected FPS: ",fps_list
                        print "Average FPS: ",avg_fps
                        minfps = float(int(expected_fps) - int(threshold))
                        if float(avg_fps) >= minfps:
                            print "Average FPS is >= %f" %(minfps)
                            print "Sample Animation App is rendered and average FPS is as expected"
                            print "[TEST EXECUTION RESULT]: SUCCESS\n"
                            tdkTestObj.setResultStatus("SUCCESS");
                        else:
                            print "Average FPS is < %f" %(minfps)
                            print "Sample Animation App is rendered and average FPS is not as expected"
                            print "[TEST EXECUTION RESULT]: FAILURE\n"
                            tdkTestObj.setResultStatus("FAILURE");
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print "\n Failed to get the data from WEBUI\n"
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
                    print "Failed to load the URL %s" %(new_url)
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Failed to set the URL"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to get the current URL loaded in webkit"
    else:
        print "Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print "Revert the values before exiting"
        status = revert_value(curr_ux_status,curr_webkit_status,curr_cobalt_status,obj);
    if resapp_revert=="YES":
        setURLAndActivateResidentApp(obj,resapp_url)
        time.sleep(10)
    obj.unloadModule("rdkv_media");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
