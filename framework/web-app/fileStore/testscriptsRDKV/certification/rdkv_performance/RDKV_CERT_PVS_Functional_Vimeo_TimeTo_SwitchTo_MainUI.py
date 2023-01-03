##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2022 RDK Management
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
  <version>9</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PVS_Functional_Vimeo_TimeTo_SwitchTo_MainUI</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this script is to get the Time while going back from vimeo to home screen</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>7</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_129</test_case_id>
    <test_objective>The objective of this script is to get the time taken while going back from Vimeo to home screen</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. The URL of the application to be launched.</input_parameters>
    <automation_approch>1. As a pre requisite disable all other plugins and enable WebKitBrowser/LightningApp/HtmlApp plugin based on configuration.
2. Set the Vimeo URL.
3. Get the time taken to go back to home screen from vimeo</automation_approch>
    <expected_output>To get the time taken while going back from vimeo to home screen</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_Vimeo_TimeTo_SwitchTo_MainUI</test_script>
    <skipped>No</skipped>
    <release_version>M105</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from web_socket_util import *
import PerformanceTestVariables
from MediaValidationUtility import *
from StabilityTestUtility import *
from datetime import datetime
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_Vimeo_TimeTo_SwitchTo_MainUI');

webkit_console_socket = None

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Execution summary variable
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    vimeo_test_url = PerformanceTestVariables.vimeo_test_url
    print "\n Check Pre conditions"
    webkit_instance = PerformanceTestVariables.webkit_instance
    set_method = webkit_instance+'.1.url'
    if webkit_instance in "WebKitBrowser":
        webinspect_port = PerformanceTestVariables.webinspect_port
    elif webkit_instance in "LightningApp":
        webinspect_port = PerformanceTestVariables.lightning_app_webinspect_port
    else:
        webinspect_port = PerformanceTestVariables.html_app_webinspect_port
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["Cobalt",webkit_instance]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(20)
    status = "SUCCESS"
    plugin_status_needed = {webkit_instance:"resumed","Cobalt":"deactivated"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting plugin status"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS":
        print "\n Pre conditions for the test are set successfully";
        print "\n Get the URL in {}".format(webkit_instance)
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method",set_method);
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult()
        current_url = tdkTestObj.getResultDetails();
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            time.sleep(60)
            print "\n Current URL:",current_url
            print "\n Set Vimeo URL"
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method",set_method);
            tdkTestObj.addParameter("value",vimeo_test_url);
            tdkTestObj.executeTestCase(expectedResult);
            vimeo_result = tdkTestObj.getResult();
            time.sleep(10)
            if expectedResult in result:
                print "\n Validate if the URL is set successfully or not"
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method",set_method);
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult();  
                new_url = tdkTestObj.getResultDetails();
                if new_url in vimeo_test_url and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print "\n Clicking OK to play video"
                    params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method", "org.rdk.RDKShell.1.generateKey")        
                    tdkTestObj.addParameter("value", params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result1 = tdkTestObj.getResult()
                    time.sleep(40)
                    if "SUCCESS" == (result1):
                        tdkTestObj.setResultStatus("SUCCESS")
                        print"\n Pressing Home button \n"
                        params = '{"keys":[ {"keyCode": 36,"modifiers": [],"delay":1.0}]}'
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method", "org.rdk.RDKShell.1.generateKey")
                        tdkTestObj.addParameter("value", params)
                        start_time = str(datetime.utcnow()).split()[1]
                        tdkTestObj.executeTestCase(expectedResult)
                        rdkshell_result = tdkTestObj.getResult()
                        time.sleep(20)
                        if expectedResult in rdkshell_result:
                            tdkTestObj.setResultStatus("SUCCESS")
                            tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
                            tdkTestObj.addParameter("realpath",obj.realpath)
                            tdkTestObj.addParameter("deviceIP",obj.IP)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
                            if ssh_param_dict != {} and expectedResult in result:
                                tdkTestObj.setResultStatus("SUCCESS")
                                command = 'cat /opt/logs/wpeframework.log | grep -inr ResidentApp.*moveToFront.*Success| tail -1'
                                # get the log line containing the main UI loaded info from wpeframework log
                                tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                                tdkTestObj.addParameter("ssh_method", ssh_param_dict["ssh_method"])
                                tdkTestObj.addParameter("credentials", ssh_param_dict["credentials"])
                                tdkTestObj.addParameter("command", command)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                output = tdkTestObj.getResultDetails()
                                if output != "EXCEPTION" and expectedResult in result:
                                    if "ResidentApp moveToFront Success" in output:
                                        required_line = output.split('\n')[1]
                                        main_ui_launched_time = getTimeStampFromString(required_line)
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                                        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder")
                                        tdkTestObj.executeTestCase(expectedResult)
                                        zorder = tdkTestObj.getResultDetails()
                                        zorder_status = tdkTestObj.getResult()
                                        if expectedResult in zorder_status :
                                            zorder = ast.literal_eval(zorder)["clients"]
                                            print "zorder: ",zorder
                                            resident_app = "ResidentApp"
                                            zorder = exclude_from_zorder(zorder)
                                            if zorder[0].lower() == resident_app.lower():
                                                print "\n Home screen is reached"
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                print"\n Home button pressed at :{} (UTC)".format(start_time)
                                                Summ_list.append('Home button pressed at :{}'.format(start_time))
                                                print"\n Main UI launched at :{} (UTC)  ".format(main_ui_launched_time)
                                                Summ_list.append('Main UI launched at :{}'.format(main_ui_launched_time))
                                                start_time_millisec = getTimeInMilliSec(start_time)
                                                main_ui_launched_time_millisec = getTimeInMilliSec(main_ui_launched_time)
                                                ui_launchtime = main_ui_launched_time_millisec - start_time_millisec
                                                print"\n Time taken for launching Main UI from another window  : {} ms\n".format(ui_launchtime)
                                                Summ_list.append('Time taken for launching Main UI from another window :{}ms'.format(ui_launchtime))
                                                conf_file,result = getConfigFileName(tdkTestObj.realpath)
                                                result1, ui_launch_threshold_value = getDeviceConfigKeyValue(conf_file,"MAIN_UI_SWITCH_TIME_THRESHOLD_VALUE")
                                                Summ_list.append('MAIN_UI_SWITCH_TIME_THRESHOLD_VALUE :{}ms'.format(ui_launch_threshold_value))
                                                result2, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                                Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
                                                if all(value != "" for value in (ui_launch_threshold_value,offset)):
                                                    print "\n Threshold value for time taken for launching Main UI from another window: {} ms".format(ui_launch_threshold_value)
                                                    if 0 < int(ui_launchtime) < (int(ui_launch_threshold_value) + int(offset)):
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print "\n The time taken for launching Main UI from another window is within the expected limit\n"
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "\n The time taken for launching Main UI from another window is not within the expected limit\n"
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print "\n Failed to get the threshold value from config file"
                                            else:
                                                print "\n Home screen is not reached"
                                                tdkTestObj.setResultStatus("FAILURE")
                                        else:
                                            print "\n Error while getting zorder value"
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print "\n Required logs are not present in wpeframework.log"
                                        tdkTestObj.setResultStatus("FAILURE");
                                else:
                                    print "\n Error occured while executing the command \n"
                                    tdkTestObj.setResultStatus("FAILURE");
                            else:
                                print "\n Please configure SSH parameter"
                                tdkTestObj.setResultStatus("FAILURE");
                        else:
                            print "\n Error while executing org.rdk.RDKShell.1.generateKey method \n"
                            tdkTestObj.setResultStatus("FAILURE");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "\n Unable to go back to Home screen"
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "\n Unable to play the video"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "\n Unable to validate the URL"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "\n Unable to get the current URL loaded"
    else:
        print"\n Pre conditions are not met"
        obj.setLoadModuleStatus("FAILURE");
        #Revert the values
        if revert == "YES":
            print "\n Revert the values before exiting"
            status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
    getSummary(Summ_list, obj)
else:
    obj.setLoadModuleStatus("FAILURE");
    print
    "\n Failed to load module"
