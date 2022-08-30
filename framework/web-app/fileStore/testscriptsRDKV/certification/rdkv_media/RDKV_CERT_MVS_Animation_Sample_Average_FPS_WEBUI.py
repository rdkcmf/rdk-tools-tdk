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
  <version>8</version>
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
    <box_type>RDKTV</box_type>
    <!-- -->
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
    <test_setup>RDKTV,RPI, Accelerator</test_setup>
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
    <automation_approch>1. As pre requisite, launch LightningApp  webkit instance via RDKShell, open websocket conntion to webinspect page
2. Store the details of other launched apps. Move the LightningApp  webkit instance to front, if its z-order is low.
3. Launch LightningApp webkit instance with Sample animation app url
4. App performs animation and display FPS on the UI.
5. Using selenium, open the webinpect page of the webkit instance and using the xpaths provided read the FPS data for given number of times
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
from rdkv_medialib import *
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
    print "\nCheck Pre conditions..."
    tdkTestObj = obj.createTestStep('rdkv_media_pre_requisites');
    tdkTestObj.executeTestCase(expectedResult);
    socketConnectionEnableDisable(False);
    # Setting the pre-requites for media test. Launching the wekit instance via RDKShell and
    # moving it to the front, openning a socket connection to the webkit inspect page and
    # disabling proc validation
    pre_requisite_status,webkit_console_socket,validation_dict = setMediaTestPreRequisites(obj,"LightningApp",False)
    config_status = "SUCCESS"
    conf_file,result = getDeviceConfigFile(obj.realpath)
    result1, expected_fps  = readDeviceConfigKeyValue(conf_file,"EXPECTED_FPS")
    result2, threshold     = readDeviceConfigKeyValue(conf_file,"FPS_THRESHOLD")
    if "SUCCESS" in result1 and "SUCCESS" in result2:
        if expected_fps == "" and threshold == "":
            config_status = "FAILURE"
            print "Please set expected_fps and threshold values in device config file"
    else:
        config_status = "FAILURE"
        print "Failed to get the FPS value & threshold value from device config file"
    if pre_requisite_status == "SUCCESS" and config_status == "SUCCESS":
        tdkTestObj.setResultStatus("SUCCESS");
        print "Pre conditions for the test are set successfully"

        print "\nSet Sample animation test app url..."
        #Setting device config file
        setDeviceConfigFile(conf_file)
        animation_test_url = MediaValidationVariables.sample_animation_test_url

        # Setting the animation test url in webkit instance using RDKShell
        launch_status = launchPlugin(obj,"LightningApp",animation_test_url)
        if "SUCCESS" in launch_status:
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
                tdkTestObj = obj.createTestStep('rdkv_media_test');
                tdkTestObj.executeTestCase(expectedResult);
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
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to load the Sample Animation URL in Webkit\n"

        print "\nSet post conditions..."
        tdkTestObj = obj.createTestStep('rdkv_media_post_requisites');
        tdkTestObj.executeTestCase(expectedResult);
        # Setting the post-requites for media test.Removing app url from webkit instance and
        # moving next high z-order app to front (residentApp if its active)
        post_requisite_status = setMediaTestPostRequisites(obj,"LightningApp",webkit_console_socket)
        if post_requisite_status == "SUCCESS":
            print "Post conditions for the test are set successfully\n"
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            print "Post conditions are not met\n"
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print "Pre conditions are not met\n"
        tdkTestObj.setResultStatus("FAILURE");
    obj.unloadModule("rdkv_media");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

