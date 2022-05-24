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
  <version>7</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_MVS_Animation_Check_Graphics_workload</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkv_media_test</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to perform animation of multiple objects from count of 1,10,20,50,100,250,500,1000 one by one for the provided duration using lightning application and check how many objects can be rendered by the device with expected FPS value.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
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
    <test_case_id>RDKV_Media_Validation_11</test_case_id>
    <test_objective>Test Script to perform animation of multiple objects from count of 1,10,20,50,100,250,500,1000 one by one for the provided duration using lightning application and check how many objects can be rendered by the device with expected FPS value.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2.Lightning Multi Animation app should be hosted</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Lightning Multi Animation App URL: string
webinspect_port: string
thunder_port :string
expected_fps:int
threshold:int</input_parameters>
    <automation_approch>1. As pre requisite, launch LightningApp  webkit instance via RDKShell, open websocket conntion to webinspect page
2. Store the details of other launched apps. Move the LightningApp  webkit instance to front, if its z-order is low.
3. Launch LightningApp webkit instance with the Multi Animation app url with the arguments like fps,threshold,ip,port,duration and testing methods
4. App performs animation of multiple objects from count of 1,10,20,50,100,250,500,1000 one by one for the provided duration.
5. App starts with animation of single object for provided duration and collect the fps for every second, then find the average of collected fps.
6. If the average FPS obtained is greater than or equal to expected fps value (i.e) expected_fps - threshold, then app increases number of objects to 10. Again average fps is calculated and checked, then app decides to proceed for further more number of objects or not.
7. Average fps for single object animation should be as expected. If this condition is satisfied test result is set as SUCCESS or else FAILURE.
8. Test script finally gives the number of objects the device can animate with expected FPS
9. Revert all values</automation_approch>
    <expected_output>Device should be able to atleast animate single object with expected FPS and number of objects the device can animate with expected FPS should be obtained</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_media</test_stub_interface>
    <test_script>RDKV_CERT_MVS_Animation_Check_Graphics_workload</test_script>
    <skipped>No</skipped>
    <release_version>M84</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from rdkv_medialib import *
import MediaValidationVariables
from MediaValidationUtility import *

obj = tdklib.TDKScriptingLibrary("rdkv_media","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_MVS_Animation_Check_Graphics_workload')

webkit_console_socket = None

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "\nCheck Pre conditions..."
    tdkTestObj = obj.createTestStep('rdkv_media_pre_requisites');
    tdkTestObj.executeTestCase(expectedResult);
    setWebKitSocketPort(webinspect_port_lightning)
    # Setting the pre-requites for media test. Launching the wekit instance via RDKShell and
    # moving it to the front, openning a socket connection to the webkit inspect page and
    # disabling proc validation
    pre_requisite_status,webkit_console_socket,validation_dict = setMediaTestPreRequisites(obj,"LightningApp",False)
    config_status = "SUCCESS"
    conf_file,result = getDeviceConfigFile(obj.realpath)
    result1, expected_fps  = readDeviceConfigKeyValue(conf_file,"EXPECTED_FPS")
    result2, threshold     = readDeviceConfigKeyValue(conf_file,"FPS_THRESHOLD")
    result3, logging_method= readDeviceConfigKeyValue(conf_file,"LOGGING_METHOD")
    if "SUCCESS" in result1 and "SUCCESS" in result2 and "SUCCESS" in result3:
        if expected_fps == "" and threshold == "" and logging_method == "":
            config_status = "FAILURE"
            print "Please set expected_fps and threshold values in device config file"
    else:
        config_status = "FAILURE"
        print "Failed to get the FPS value & threshold value from device config file"
    if pre_requisite_status == "SUCCESS" and config_status == "SUCCESS":
        tdkTestObj.setResultStatus("SUCCESS");
        print "Pre conditions for the test are set successfully"

        print "\nSet Multiple objects Animation test url..."
        #Setting device config file
        setDeviceConfigFile(conf_file)
        appURL    = MediaValidationVariables.lightning_multianimation_test_app_url
        # Setting Animation test app URL arguments
        setURLArgument("port",MediaValidationVariables.thunder_port)
        setURLArgument("duration",MediaValidationVariables.animation_duration)
        setURLArgument("testtype","generic")
        setURLArgument("autotest","true")
        setURLArgument("fps",expected_fps)
        setURLArgument("threshold",threshold)
        appArguments = getURLArguments()
        # Getting the complete test app URL
        animation_test_url = getTestURL(appURL,appArguments)

        # Setting the animation test url in webkit instance using RDKShell        
        launch_status = launchPlugin(obj,"LightningApp",animation_test_url)
        if "SUCCESS" in launch_status:
            continue_count = 0
            avgerage_fps_list = []
            minfps = float(int(expected_fps) - int(threshold))
            # Monitoring the app progress, checking whether app performs animation properly or any hang detected in between,
            # and getting the test result from the app
            file_check_count = 0
            logging_flag = 0
            hang_detected = 0
            test_result = ""
            lastLine = None
            lastIndex = 0
            app_log_file = obj.logpath+"/"+str(obj.execID)+"/"+str(obj.execID)+"_"+str(obj.execDevId)+"_"+str(obj.resultId)+"_mvs_applog.txt"
            if logging_method == "REST_API":
                while True:
                    if file_check_count > 60:
                        print "\nREST API Logging is not happening properly. Exiting..."
                        break;
                    if os.path.exists(app_log_file):
                        logging_flag = 1
                        break;
                    else:
                        file_check_count += 1
                        time.sleep(1);

                while logging_flag:
                    if continue_count > 180:
                        hang_detected = 1
                        print "\nApp not proceeding for 3 min. Exiting..."
                        break;
 
                    with open(app_log_file,'r') as f:
                        lines = f.readlines()
                    if lines:
                        if len(lines) != lastIndex:
                            continue_count = 0
                            #print(lastIndex,len(lines))
                            for i in range(lastIndex,len(lines)):
                                if "[DiagnosticInfo]: CPU Load" not in lines[i]:
                                    print(lines[i])
                                if "[DiagnosticInfo]: No.of Animated Objects" in lines[i]:
                                    avgerage_fps_list.append(lines[i])
                                if "TEST COMPLETED" in lines[i] or "TEST STOPPED" in lines[i]:
                                    test_result = lines[i]

                            #lastLine  = lines[-1]
                            lastIndex = len(lines)
                            if test_result != "":
                                break;
                        else:
                            continue_count += 1
                    else:
                        continue_count += 1
 
                    time.sleep(1)
            elif logging_method == "WEB_INSPECT":
                while True:
                    if continue_count > 180:
                        print "\nApp not proceeding for 3 mins. Exiting..."
                        break
                    if (len(webkit_console_socket.getEventsBuffer())== 0):
                        time.sleep(1)
                        continue_count += 1
                        continue
                    else:
                        continue_count = 0
                    console_log = webkit_console_socket.getEventsBuffer().pop(0)
                    if "[DiagnosticInfo]: CPU Load" not in console_log:
                        dispConsoleLog(console_log)
                    if "[DiagnosticInfo]: No.of Animated Objects" in console_log:
                        log_message = getConsoleMessage(console_log)
                        avgerage_fps_list.append(log_message)
                    if "TEST COMPLETED" in console_log or "TEST STOPPED" in console_log:
                        break;
                webkit_console_socket.disconnect()
            avg_fps_single_object = str(avgerage_fps_list[0]).split(",")[1].split(":")[1]
            if "NaN" in avg_fps_single_object:
                print "Failed to get the average FPS Value"
                print "[TEST EXECUTION RESULT]: FAILURE"
                tdkTestObj.setResultStatus("FAILURE");
            elif float(avg_fps_single_object) >= minfps:
                print "Average FPS (for single object) >= %f" %(minfps)
                print "\nBelow are the no.of objects the device can animate with the expected FPS:"
                for info in avgerage_fps_list:
                    if float(str(info).split(",")[1].split(":")[1]) >= minfps:
                        print info
                print "\n[TEST EXECUTION RESULT]: SUCCESS"
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                print "Average FPS (for single object) < %f" %(minfps)
                print "Average FPS for single object animation is not as expected"
                print "[TEST EXECUTION RESULT]: FAILURE"
                tdkTestObj.setResultStatus("FAILURE");

            print "\nSet post conditions..."
            tdkTestObj = obj.createTestStep('rdkv_media_post_requisites');
            tdkTestObj.executeTestCase(expectedResult);
            # Setting the post-requites for media test.Removing app url from webkit instance and
            # moving next high z-order app to front (residentApp if its active)
            post_requisite_status = setMediaTestPostRequisites(obj,"LightningApp")
            if post_requisite_status == "SUCCESS":
                print "Post conditions for the test are set successfully\n"
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                print "Post conditions are not met\n"
                tdkTestObj.setResultStatus("FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to load the Animation Test URL in Webkit\n"
    else:
        print "Pre conditions are not met\n"
        tdkTestObj.setResultStatus("FAILURE");
    obj.unloadModule("rdkv_media");
else:
    obj.setLoadModuleStatus("FAILURE");
    print "Failed to load module"

