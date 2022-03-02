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
  <name>FCS_Playback_PlaySeek_Backward_Stress_H264</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test to do multiple backward seek on a H264 stream</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <test_case_id>FCS_PLAYBACK_75</test_case_id>
    <test_objective>Test to do multiple backward seek on a H264 stream</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator, RPI</test_setup>
    <pre_requisite>1.TDK Agent should be up and running in the DUT
2. Test stream url for a H264 stream should be updated in the config variable video_src_url_hls_h264 inside MediaValidationVariables.py library inside filestore
3. FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration should be set as yes/no in the device config file
4. FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration should be set to time in seconds for which the playback should be carried out
5. FIREBOLT_COMPLIANCE_SEEK_STEP configuration should be set to step value in seconds with which the seek operation should be carried out each time decreasing the seek position with step value staring from FIREBOLT_COMPLIANCE_SEEK_STEP * FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT (FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT is the number of times to repeat the seek operation)
6. FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT configuration should be set to the number of times, the operations should be repeated</pre_requisite>
    <api_or_interface_used>Execute the mediapipelinetests application in DUT</api_or_interface_used>
    <input_parameters>1.testcasename - "test_trickplay"
2.test_url - H264 url from MediaValidationVariables library (MediaValidationVariables.video_src_url_hls_h264)
3."checkavstatus=yes" - argument to do the video playback verification from SOC side . This argument can be yes/no based on a device configuration(FIREBOLT_COMPLIANCE_CHECK_AV_STATUS) from Device Config file
4.operations=seek:&lt;timeout&gt;:&lt;seekposition&gt;,seek:&lt;timeout&gt;:&lt;seekposition&gt;,seek:&lt;timeout&gt;:&lt;seekposition&gt;,seek:&lt;timeout&gt;:&lt;seekposition&gt;,seek:&lt;timeout&gt;:&lt;seekposition&gt;,seek:&lt;timeout&gt;:&lt;seekposition&gt; - a ":" seperated string to specify the seek operation to be executed , the time in seconds for which the operation should be performed and seekposition in seconds to which the seek operation should be performed. seekposition will be FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT * FIREBOLT_COMPLIANCE_SEEK_STEP(since we are executing seek FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT times) in first seek, then it would be seekposition - FIREBOLT_COMPLIANCE_SEEK_STEP for the next seek operation, decrementing the seek position with FIREBOLT_COMPLIANCE_SEEK_STEP in each seek.The timeout should be configured in the device configuration(FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT) from Device Config file The seek step and repeat count should also be configured in device configuration(FIREBOLT_COMPLIANCE_SEEK_STEP and FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT)</input_parameters>
    <automation_approch>1.Load the systemutil module 
2.Retrieve the FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_SEEK_POSITION, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT and FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT config values from Device config file.
3.Retrieve the video_src_url_hls_h264 variable from MediaValidationVariables library
4.Construct the mediapipelinetests command based on the retrieved video url, testcasename, FIREBOLT_COMPLIANCE_CHECK_AV_STATUS deviceconfig value, operation, seekposition, timeout and repeatCount
5.Execute the command in DUT. During the execution, the DUT will start av playback, then pipeline seeks to FIREBOLT_COMPLIANCE_SEEK_STEP * FIREBOLT_COMPLIANCE_SEEK_STEP and then av playback is performed for FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT seconds, then seeks to previous seek position - FIREBOLT_COMPLIANCE_SEEK_STEP and performs av playback for FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT seconds.This seek opeartion is repeated FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT times, each time decreasing the seek position by FIREBOLT_COMPLIANCE_SEEK_STEP seconds.Then application exits by closing the pipeline
6.Verify the output from the execute command and check if the  "Failures: 0" and "Errors: 0" string exists or "failed: 0" string exists in the returned output
7.Based on the ExecuteCommand() return value and the output returned from the mediapipelinetests application, TM return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1. Verify the API call is success
Checkpoint 2. Verify that the output returned from mediapipelinetests contains the strings "Failures: 0" and "Errors: 0" or it contains the string "failed: 0"</expected_output>
    <priority>High</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_Playback_PlaySeek_Backward_Stress_H264</test_script>
    <skipped>No</skipped>
    <release_version>M93</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import MediaValidationVariables
from FireboltComplianceUtility import *

#Test component to be tested
fcObj = tdklib.TDKScriptingLibrary("firebolt_compliance","1")
#Using systemutil library for command execution
sysUtilObj = tdklib.TDKScriptingLibrary("systemutil","1")

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
sysUtilObj.configureTestCase(ip,port,'FCS_Playback_PlaySeek_Backward_Stress_H264');

#Set device configurations to default values
checkAVStatus = "no"
timeoutInSeconds = "1"
seekStepInSeconds = "10"
repeatCount = 3

#Load the systemutil library
sysutilloadModuleStatus =sysUtilObj.getLoadModuleResult()
print "[System Util LIB LOAD STATUS]  :  %s" %sysutilloadModuleStatus
sysUtilObj.setLoadModuleStatus(sysutilloadModuleStatus)
if "SUCCESS" in sysutilloadModuleStatus.upper():
    expectedResult="SUCCESS"
    
    #Construct the command with the url and execute the command in DUT
    tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand')
    
    #The test name specifies the test case to be executed from the mediapipeline test suite
    test_name = "test_trickplay"
    #Test url for the stream to be played is retrieved from MediaValidationVariables library
    test_url = MediaValidationVariables.video_src_url_hls_h264
    #Retrieve the value of configuration parameter 'FIREBOLT_COMPLIANCE_CHECK_AV_STATUS' that specifies whether SOC level playback verification check should be done or not 
    actualresult, check_av_status_flag = getDeviceConfigValue (sysUtilObj, 'FIREBOLT_COMPLIANCE_CHECK_AV_STATUS')
    #If the value of FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is retrieved correctly and its value is "yes", argument to check the SOC level AV status should be passed to test application
    if expectedResult in actualresult.upper() and check_av_status_flag == "yes":
        print "Video Decoder proc check is added"
        checkAVStatus = check_av_status_flag
    #Retrieve the value of configuration parameter 'FIREBOLT_COMPLIANCE_SEEK_STEP' that specifies the value in seconds to which the pipeline should increment seek position each time 
    actualresult, seek_step = getDeviceConfigValue (sysUtilObj, 'FIREBOLT_COMPLIANCE_SEEK_STEP')
        
    #If the value of FIREBOLT_COMPLIANCE_SEEK_STEP is retrieved correctly and its value is not empty, seek_step value should be used for calculating the seekposition that has to be passed to the test application
    #if the device config value is empty, default seek position(20sec) is passed
    if expectedResult in actualresult.upper() and seek_step != "":
        seekStepInSeconds = seek_step
    #Retrieve the value of configuration parameter 'FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT' that specifies the video playback timeout in seconds 
    actualresult, timeoutConfigValue = getDeviceConfigValue (sysUtilObj, 'FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT')
        
    #If the value of FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT is retrieved correctly and its value is not empty, timeout value should be passed to the test application
    #if the device config value is empty, default timeout(10sec) is passed
    if expectedResult in actualresult.upper() and timeoutConfigValue != "":
        timeoutInSeconds = timeoutConfigValue
    #Retrieve the value of configuration parameter 'FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT' that specifies the number of times the operations should be reapeted 
    actualresult, repeatCountConfigValue = getDeviceConfigValue (sysUtilObj, 'FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT')
        
    #If the value of FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT is retrieved correctly and its value is not empty, repeatCount value should be set as the retrieved vale
    #if the device config value is empty, default repeatCount(3) is passed
    if expectedResult in actualresult.upper() and repeatCountConfigValue != "":
        repeatCount = int(repeatCountConfigValue)
    #Construct the trickplay operation string by calling the setOperations() separately for each seek operation along with the timeoutand seekposition (seekposition increamented in steps of FIREBOLT_COMPLIANCE_SEEK_STEP) arguments
    #The operations specifies the operation(fastforward/rewind/seek/play/pause) to be executed from the mediapipeline trickplay test
    #Sample oprations strings is "operations=seek:3:60,seek:3:50,seek:3:40,seek:3:30,seek:3:20,seek:3:10" where 3 is time for which playback should happen and 10, 20, 30, 40, 50 ,60 are the seek positions/duration
    #The seek operations are added FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT times
    for iterator in range (repeatCount, 0, -1):
        setOperations ("seek", timeoutInSeconds, str (int (seekStepInSeconds) * iterator))

    #To do the AV playback through 'playbin' element, we are using 'mediapipelinetests' test application that is available in TDK along with required parameters
    #Sample command = "mediapipelinetests test_trickplay <H264_STREAM_URL> checkavstatus=yes operations=seek:3:60,seek:3:50,seek:3:40,seek:3:30,seek:3:20,seek:3:10"
    command = getMediaPipelineTestCommand (test_name, test_url, checkavstatus = checkAVStatus, operations = getOperations ()) 
    print "Executing command in DUT: ", command
    
    tdkTestObj.addParameter("command", command)
    tdkTestObj.executeTestCase(expectedResult)
    actualresult = tdkTestObj.getResult()
    output = tdkTestObj.getResultDetails()
    print "OUTPUT: ", output

    #Check if the command executed successfully
    if expectedResult in actualresult.upper() and output:
        #Check the output string returned from 'mediapipelinetests' to verify if the test suite executed successfully 
        executionStatus = checkMediaPipelineTestStatus (output)
        
        if expectedResult in executionStatus:
            tdkTestObj.setResultStatus("SUCCESS")
            print "Backward seek stress on H264 stream was successfull"
            print "Mediapipeline test executed successfully"
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print "Backward seek stress on H264 stream failed"
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print "Mediapipeline test execution failed"
    #Unload the modules
    sysUtilObj.unloadModule("systemutil")
else:
    print "Module load failed"
