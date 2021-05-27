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
  <name>RDKV_CERT_PACS_AmazonPrime_Check_VideoPlayback</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate video playback in Amazon prime.</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_43</test_case_id>
    <test_objective>The objective of this test is to validate video playback in Amazon prime.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>amazon_test_url : string</input_parameters>
    <automation_approch>1. Launch Amazon plugin using RDKShell
2. Get the zorder and moveToFront if Amazon is not in front.
3. Click OK to login as the existing user, using generateKey method.
4. Launch the given video url using deepLinkUrl method.
5. Click OK to start playing the video
6. Validate the video playback</automation_approch>
    <expected_output>User must be able to play the video in Amazon prime.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_AmazonPrime_Check_VideoPlayback</test_script>
    <skipped>No</skipped>
    <release_version>M89</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from StabilityTestUtility import *
import PerformanceTestVariables
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_AmazonPrime_Check_VideoPlayback');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugin = "Amazon"
    amazon_test_url = PerformanceTestVariables.amazon_test_url
    if amazon_test_url == "":
        print "\n Please configure the amazon_test_url value in PerformanceTestVariables \n"
    plugins_list = ["WebKitBrowser","Cobalt","Amazon"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"Amazon":"deactivated","WebKitBrowser":"deactivated","Cobalt":"deactivated"}
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if  plugin_status_needed != new_plugins_status:
            status = "FAILURE"
    validation_dict = get_validation_params(obj)
    if status == "SUCCESS" and validation_dict != {} and amazon_test_url != "":
        if validation_dict["validation_required"]:
            if validation_dict["password"] == "None":
                password = ""
            else:
                password = validation_dict["password"]
            credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
        #Launch amazon and move to front
        launch_status, start_time = launch_plugin(obj,plugin)
        time.sleep(30)
        if launch_status == "SUCCESS":
            movedToFront = True
            tdkTestObj = obj.createTestStep('rdkservice_getValue')
            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder")
            tdkTestObj.executeTestCase(expectedResult)
            zorder = tdkTestObj.getResultDetails()
            zorder_status = tdkTestObj.getResult()
            if expectedResult in zorder_status:
                tdkTestObj.setResultStatus("SUCCESS")
                zorder = ast.literal_eval(zorder)["clients"]
                if zorder[0].lower() == plugin.lower():
                    print "\n{} plugin is in foreground\n".format(plugin)
                else:
                    param_val = '{"client": "'+plugin+'"}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.moveToFront")
                    tdkTestObj.addParameter("value",param_val)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if result == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        movedToFront = False
                        tdkTestObj.setResultStatus("FAILURE")
                if movedToFront:
                    #Press OK to proceed
                    params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if expectedResult in result:
                        tdkTestObj.setResultStatus("SUCCESS")
                        time.sleep(20)
                        print "\n Set the URL \n"
                        video_params = '{"url":"'+amazon_test_url+'"}'
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","Amazon.1.deepLinkUrl")
                        tdkTestObj.addParameter("value",video_params)
                        tdkTestObj.executeTestCase(expectedResult)
                        amazon_result = tdkTestObj.getResult()
                        if expectedResult in amazon_result:
                            tdkTestObj.setResultStatus("SUCCESS")
                            time.sleep(10)
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                            tdkTestObj.addParameter("value",params)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            if expectedResult in result:
                                tdkTestObj.setResultStatus("SUCCESS")
                                time.sleep(30)
                                result_val = "SUCCESS"
                                if validation_dict["validation_required"]:
                                    tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                                    tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                                    tdkTestObj.addParameter("credentials",credentials)
                                    tdkTestObj.addParameter("video_validation_script",validation_dict["video_validation_script"])
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result_val = tdkTestObj.getResultDetails()
                                    if result_val == "SUCCESS" :
                                        print "\nVideo playback is happening\n"
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print "\n Video playback is not happening \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n User opted for skipping Video validation, completing the test \n"
                            else:
                                print "\n Error while pressing OK \n"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Error while setting video in Amazon plugin \n"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error while pressing OK \n"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Unable to move plugin to front \n"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while executing getZorder \n"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error occured during plugin launch. Stopping the test \n"
        #Deactivate Amazon
        print "\n Exiting from Amazon \n"
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
        tdkTestObj.addParameter("plugin","Amazon")
        tdkTestObj.addParameter("status","deactivate")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "Unable to deactivate Amazon"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Preconditions are not met"
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print "\n Revert the values before exiting \n"
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"
