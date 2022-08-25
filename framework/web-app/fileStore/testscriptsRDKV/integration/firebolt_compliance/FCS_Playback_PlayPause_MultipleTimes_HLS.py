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
  <version>2</version>
  <name>FCS_Playback_PlayPause_MultipleTimes_HLS</name>
  <primitive_test_id/>
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test to do multiple short duration play, pause operations on a HLS stream</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>Video_Accelerator</box_type>
    <box_type>RDKTV</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>FCS_PLAYBACK_23</test_case_id>
    <test_objective>Test to do multiple short duration play, pause operations on a HLS stream</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK TV,Video Accelerator, RPI</test_setup>
    <pre_requisite>1.TDK Agent should be up and running in the DUT
2. Test stream url for a HLS stream should be updated in the config variable video_src_url_hls inside MediaValidationVariables.py library inside filestore
3. FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration should be set as yes/no in the device config file
4. FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration should be set to time in seconds for which each play, pause operation should be carried out
5. FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT configuration should be set to the number of times, the operations should be repeated</pre_requisite>
    <api_or_interface_used>Execute the mediapipelinetests application in DUT</api_or_interface_used>
    <input_parameters>testcasename - "test_trickplay"
test_url - HLS url from MediaValidationVariables library (MediaValidationVariables.video_src_url_hls)
"checkavstatus=yes" - argument to do the video playback verification from SOC side . This argument can be yes/no based on a device configuration(FIREBOLT_COMPLIANCE_CHECK_AV_STATUS) from Device Config file
operations=play:&lt;timeout&gt;,pause:&lt;timeout&gt;,play:&lt;timeout&gt;,pause:&lt;timeout&gt;,play:&lt;timeout&gt;,pause:&lt;timeout&gt; (number of play:&lt;timeout&gt;,pause:&lt;timeout&gt; string depends on the parameter FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT) - a comma separated string of indivudual play/pause &lt;operation:timeout&gt; string where operation could be string "play"/"pause" indicating play/pause operations and timeout is time in seconds for which the operation should be performed. The timeout should be configured in the device configuration(FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT) from Device Config file. The same timeout value can be used for all operations.The play/pause operations are repeted FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT times</input_parameters>
    <automation_approch>1.Load the systemutil module 
2.Retrieve the FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT and FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT config values from Device config file.
3.Retrieve the video_src_url_hls variable from MediaValidationVariables library
4. Construct the mediapipelinetests command based on the retrieved video url, testcasename, FIREBOLT_COMPLIANCE_CHECK_AV_STATUS deviceconfig value, operations
5.Execute the command in DUT. During the execution, the DUT will playback av for FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT seconds, then av is paused for FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT seconds.This sequence of play and pause operations are repeated for FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT times and then application exits by closing the pipeline
6.Verify the output from the execute command and check if the  "Failures: 0" and "Errors: 0" string exists or "failed: 0" string exists in the returned output
7.Based on the ExecuteCommand() return value and the output returned from the mediapipelinetests application, TM return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1. Verify the API call is success
Checkpoint 2. Verify that the output returned from mediapipelinetests contains the strings "Failures: 0" and "Errors: 0" or it contains the string "failed: 0"</expected_output>
    <priority>High</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_Playback_PlayPause_MultipleTimes_HLS</test_script>
    <skipped>No</skipped>
    <release_version>M90</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
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
sysUtilObj.configureTestCase(ip,port,'FCS_Playback_PlayPause_MultipleTimes_HLS');

#Set device configurations to default values
checkAVStatus = "no"
timeoutInSeconds = "10"
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
    test_url = MediaValidationVariables.video_src_url_hls
    #Retrieve the value of configuration parameter 'FIREBOLT_COMPLIANCE_CHECK_AV_STATUS' that specifies whether SOC level playback verification check should be done or not 
    actualresult, check_av_status_flag = getDeviceConfigValue (sysUtilObj, 'FIREBOLT_COMPLIANCE_CHECK_AV_STATUS')
    #If the value of FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is retrieved correctly and its value is "yes", argument to check the SOC level AV status should be passed to test application
    if expectedResult in actualresult.upper() and check_av_status_flag == "yes":
        print "Video Decoder proc check is added"
        checkAVStatus = check_av_status_flag
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
    #Construct the trickplay operation string by calling the setOperations() separately for each play/pause operation along with the timeout argument
    #The operations specifies the operation(fastforward/rewind/seek/play/pause) to be executed from the mediapipeline trickplay test
    #Sample oprations strings is "operations=play:10,pause:10,play:10,pause:10,play:10,pause:10,play:10,pause:10,play:10,pause:10,play:10,pause:10"
    #The play and pause operations are added FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT or 3(default) times
    #For adding the operation to the trickplay operations string, execute setOperations (operation_name_string, arguments...)
    #eg: setOperations ("play", 10)
    #For repeating the previous operations, execute setOperations ("repeat", number of operations to be repeated, number of times the operations should be repeated)
    #Eg: To repeat "play", "pause" operations 3 times, setOperations ("play", 10), setOperations ("pause", 10), setOperations ("repeat", 2, 2)
    #for iterator in range (repeatCount):
    setOperations ("play", timeoutInSeconds)
    setOperations ("pause", timeoutInSeconds)
    #Repeat the above operation for repeatCount-1 times more
    setOperations ("repeat", 2, repeatCount-1)

    #To do the AV playback through 'playbin' element, we are using 'mediapipelinetests' test application that is available in TDK along with required parameters
    #Sample command = "mediapipelinetests test_trickplay <HLS_STREAM_URL> checkavstatus=yes operations=play:30,pause:30,play:30,pause:30,play:30,pause:30,play:30,pause:30,play:30,pause:30,play:30,pause:30"
    command = getMediaPipelineTestCommand (test_name, test_url, checkavstatus = checkAVStatus, operations = getOperations ()) 
    print "Executing command in DUT: ", command
    
    tdkTestObj.addParameter("command", command)
    tdkTestObj.executeTestCase(expectedResult)
    actualresult = tdkTestObj.getResult()
    output = tdkTestObj.getResultDetails().replace(r'\n', '\n'); output = output[output.find('\n'):]
    print "OUTPUT: ...\n", output

    #Check if the command executed successfully
    if expectedResult in actualresult.upper() and output:
        #Check the output string returned from 'mediapipelinetests' to verify if the test suite executed successfully 
        executionStatus = checkMediaPipelineTestStatus (output)
        
        if expectedResult in executionStatus:
            tdkTestObj.setResultStatus("SUCCESS")
            print "Multiple play,pause operations on HLS stream was successfull"
            print "Mediapipeline test executed successfully"
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print "Multiple play,pause operations on HLS stream failed"
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print "Mediapipeline test execution failed"
    #Unload the modules
    sysUtilObj.unloadModule("systemutil")
else:
    print "Module load failed"
