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
  <name>RDKV_Profiling_Video_AAMP_Play_DASH_Clear</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkv_profiling_collectd_check_system_memory</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to validate profiling data after performing video playback of dash clear content using lightning uve aamp player app</synopsis>
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
    <test_case_id>RDKV_PROFILING_14</test_case_id>
    <test_objective>The objective of this test is to validate profiling data after performing video playback of dash clear content using lightning uve aamp player app</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2.Lightning UVE AAMP Player app should be hosted
3. User should configure SSH details, profiling threshold values and URL details
4. User should setup Grafana tool</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>lightning_uve_test_app_url: string
webkit_instance:string
thunder_port: string
video_src_url_dash: string
close_interval: int</input_parameters>
    <automation_approch>1. Launch WebKit instance using RDKShell and set the focus.
2. Set the URL of lightning uve aamp test app with video src url.
3. Check whether URL is loaded properly.
4. Check video playback by decoder proc validation if applicable.
5. After few minutes, validate the profiling data from Grafana tool with the threshold values for the pre-configured process list.
6. Execute the smem tool and collect the log
7. Execute pmap tool for the list of given process and collect the log
8. Revert the Webkit instance URL and plugin status.</automation_approch>
    <expected_output>Video playback should happen and profiling data should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_profiling</test_stub_interface>
    <test_script>RDKV_Profiling_Video_AAMP_Play_DASH_Clear</test_script>
    <skipped>No</skipped>
    <release_version>M92</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import ast,time
import json
import RDKVProfilingVariables
from datetime import datetime
from web_socket_util import *
from MediaValidationUtility import *
from MediaValidationVariables import *
from StabilityTestUtility import *
from RDKVProfilingVariables import *
from rdkv_profilinglib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_profiling","1",standAlone=True);

start_datetime_string = str(datetime.utcnow()).split('.')[0]

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Profiling_Video_AAMP_Play_DASH_Clear');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    status = "SUCCESS"
    is_front = False
    process_list = ['WPEFramework','WPEWebProcess','WPENetworkProcess','tr69hostif']
    conf_file,result2 = get_configfile_name(obj)
    time.sleep(30)
    #Validate system wide profiling data before playing AAMP video dash clear
    end_datetime_string = str(datetime.utcnow()).split('.')[0]
    print "\n Validating system wide profiling mettrics from grafana before AAMP video dash clear\n"
    for result,validation_result,system_wide_methods,tdkTestObj in get_systemwide_multiplerequest(obj,conf_file,start_datetime_string,end_datetime_string):
        if expectedResult in (result and validation_result):
            print "Successfully validated the {}\n".format(system_wide_methods)
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "Error while validating the {}\n".format(system_wide_methods)
            tdkTestObj.setResultStatus("FAILURE")
    #Validate process wise profiling data before AAMP video dash clear
    print "\n Validating process wise profiling metrics from grafana before AAMP video dash clear\n"
    for result,validation_result,process_wise_methods_list,tdkTestObj in get_processwise_multiplerequest(obj,conf_file,start_datetime_string,end_datetime_string,process_list):
        if expectedResult in (result and validation_result):
            print "Successfully validated the {}\n".format(process_wise_methods_list)
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "Error while validating the {}\n".format(process_wise_methods_list)
            tdkTestObj.setResultStatus("FAILURE")
    plugin = webkit_instance
    url    = "about:blank"
    print "\nLaunching %s using RDKShell..." %(plugin)
    url = url.replace('\"',"")
    tdkTestObj = obj.createTestStep('rdkservice_setValue')
    params = '{"callsign":"'+plugin+'", "type":"'+plugin+'", "uri":"'+url+'"}'
    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.launch")
    tdkTestObj.addParameter("value",params)
    tdkTestObj.executeTestCase(expectedResult);
    result = tdkTestObj.getResult();
    info = tdkTestObj.getResultDetails();

    config_status = "SUCCESS"
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result1 = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    validation_dict = get_validation_params(obj)
    #conf_file,result2 = getConfigFileName(obj.realpath)
    if result2 == "FAILURE":
        print "\nUnable to get the device config file"
    if result1 == "FAILURE" or result2 == "FAILURE" or ssh_param_dict == {} or validation_dict == {}:
        config_status = "FAILURE"

    if expectedResult in result and expectedResult in config_status:
        print "Resumed %s plugin " %(plugin)
        tdkTestObj.setResultStatus("SUCCESS")
        time.sleep(10)

        #Check zorder to check WebKitBrowser is in the front
        tdkTestObj = obj.createTestStep('rdkservice_getValue')
        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder")
        tdkTestObj.executeTestCase(expectedResult)
        zorder = tdkTestObj.getResultDetails()
        zorder_status = tdkTestObj.getResult()
        if expectedResult in zorder_status :
            tdkTestObj.setResultStatus("SUCCESS")
            zorder = ast.literal_eval(zorder)["clients"]
            if plugin.lower() in zorder and zorder[0].lower() == plugin.lower():
                is_front = True
                print "\n  WebKitBrowser is in front"
            elif plugin.lower() in zorder and zorder[0].lower() != plugin.lower():
                param_val = '{"client": "'+plugin+'"}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.moveToFront")
                tdkTestObj.addParameter("value",param_val)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS")
                    #Check zorder to check WebKitBrowser is in the front
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder")
                    tdkTestObj.executeTestCase(expectedResult)
                    zorder = tdkTestObj.getResultDetails()
                    zorder_status = tdkTestObj.getResult()
                    if expectedResult in zorder_status :
                        zorder = ast.literal_eval(zorder)["clients"]
                        if zorder[0].lower() != plugin.lower():
                            print "\n Successfully moved WebKitBrowser to front"
                            is_front = True
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\n Unable to move WebKitBrowser to front"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error while getting the zorder"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error while executing moveToFront method"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n WebKitBrowser is not present in zorder"
                tdkTestObj.setResultStatus("FAILURE")
        else:
             print "\n Error while getting the zorder"
             tdkTestObj.setResultStatus("FAILURE")

        # Loading the Test App URL if webkit is in front
        if is_front:
            setDeviceConfigFile(conf_file)
            appURL    = lightning_uve_test_app_url
            videoURL  = video_src_url_dash
            # Setting VideoPlayer Operations
            setOperation("close",close_interval)
            operations = getOperations()
            # Setting VideoPlayer test app URL arguments
            setURLArgument("url",videoURL)
            setURLArgument("operations",operations)
            setURLArgument("autotest","true")
            appArguments = getURLArguments()
            # Getting the complete test app URL
            video_test_url = getTestURL(appURL,appArguments)
            video_test_url = video_test_url.replace('\"',"")
            #Example video test url
            #http://*testManagerIP*/rdk-test-tool/fileStore/lightning-apps/tdkuveplayer/build/index.html?
            #url=<video_h264_url>.mpd&operations=close(60)&autotest=true

            print "\nRegistering Webkit Instance URLChange Event..."
            time.sleep(1)
            method = plugin + ".1.register"
            event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 5,"method": "' +method+ '","params": {"event": "urlchange", "id": "client.events.1" }}'],"/jsonrpc",False)
            time.sleep(5)
            print "\nLoading the Test URL %s" %(video_test_url)
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            params = '{"callsign":"'+plugin+'", "type":"'+plugin+'", "uri":"'+video_test_url+'"}'
            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.launch")
            tdkTestObj.addParameter("value",params)
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            info = tdkTestObj.getResultDetails();
            print result,info
            if expectedResult in result:
                print "Resumed %s plugin " %(plugin)
                tdkTestObj.setResultStatus("SUCCESS")
                url_loaded_status = False
                url_change_count  = 0
                continue_count    = 0
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
                    if "urlchange" in event_log and video_test_url in event_log:
                        if not json_msg["params"]["loaded"]:
                            url_change_count += 1
                        elif json_msg["params"]["loaded"]:
                            url_loaded_status = True
                            url_change_count += 1
                        else:
                            continue_count += 1
                    else:
                        continue_count += 1

                if url_loaded_status:
                    print "\n Started playing video...."
                    tdkTestObj.setResultStatus("SUCCESS")
                    video_play_status = True
                    if validation_dict["validation_required"]:
                        print "\nProc validation enabled.Checking proc file..."
                        time.sleep(60)
                        tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                        tdkTestObj.addParameter("sshmethod",ssh_param_dict["ssh_method"])
                        tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                        tdkTestObj.addParameter("video_validation_script",validation_dict["video_validation_script"])
                        tdkTestObj.executeTestCase(expectedResult)
                        result_val = tdkTestObj.getResultDetails()
                        if result_val == "SUCCESS" :
                            tdkTestObj.setResultStatus("SUCCESS")
                            print "\nVideo playback is happening\n"
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            video_play_status = False
                            print "Video playback is not happening"
                        if video_play_status:
                            print "\nContinue video playback..."
                            time.sleep(60)
                    else:
                        print "\n Proc validation skipped.Continue video playback..."
                        time.sleep(120)

                    if video_play_status:
                        print "\n Validate data from Grafana"
                        #Validate system wide profiling data
                        for result,validation_result,system_wide_methods,tdkTestObj in get_systemwidemethods(obj,conf_file):
                            if expectedResult in (result and validation_result):
                                print "Successfully validated the {}\n".format(system_wide_methods)
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print "Error while validating the {}\n".format(system_wide_methods)
                                tdkTestObj.setResultStatus("FAILURE")
                        #Validate process wise profiling data
                        for result,validation_result,process,process_wise_methods_list,tdkTestObj in get_processwisemethods(obj,process_list,conf_file):
                            if expectedResult in (result and validation_result):
                                print "Successfully validated the {} process {}\n".format(process,process_wise_methods_list)
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print "Error while validating the {} process {}\n".format(process,process_wise_methods_list)
                                tdkTestObj.setResultStatus("FAILURE")
                        #smem data collection
                        result,tdkTestObj = get_smemdata(obj,ip,conf_file)
                        if "SUCCESS" in result:
                            print "\nSMEM tool execution success and transferred the log"
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\nSMEM tool execution or log transfer failed"
                            tdkTestObj.setResultStatus("FAILURE")
                        #pmap data collection
                        #Automatic process selection to get pmap data will be added in the later releases
                        result,tdkTestObj = get_pmapdata(obj,ip,conf_file,process_list)
                        if "SUCCESS" in result:
                            print "\npmap tool execution success and transferred the log"
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "\npmap tool execution or log transfer failed"
                            tdkTestObj.setResultStatus("FAILURE")
                        print "\nCheck for profiling alerts...."
                        tdkTestObj = obj.createTestStep("rdkv_profiling_get_alerts")
                        tdkTestObj.addParameter('tmUrl',obj.url)
                        tdkTestObj.addParameter('resultId',obj.resultId)
                        tdkTestObj.executeTestCase(expectedResult)
                        details = tdkTestObj.getResultDetails()
                        result = tdkTestObj.getResult()
                        validation_result = json.loads(details).get("test_step_status")
                        if expectedResult in (result and validation_result):
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")

                    else:
                        print "\n Exiting without collecting the metrics \n"

                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print "\n Test URL is not loaded completely.Exiting Test"

                print "\nReverting Webkit URL to about:blank..."
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                params = '{"callsign":"'+plugin+'", "type":"'+plugin+'", "uri":"'+url+'"}'
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.launch")
                tdkTestObj.addParameter("value",params)
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult();
                info = tdkTestObj.getResultDetails();
                if expectedResult in result:
                    print "Reverted the webkit url"
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Unable to load the Test URL in WebKitBrowser"
                tdkTestObj.setResultStatus("FAILURE")

            event_listener.disconnect()
            time.sleep(5)
        else:
            print "\n Unable to set Webkitbrowser as focused client.Exiting Test"
    else:
        if config_status != "SUCCESS":
            print "\n Preconditions are not met"
            tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Unable to launch webkit browser via RDKShell"
            tdkTestObj.setResultStatus("FAILURE")

    obj.unloadModule("rdkv_profiling")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
