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
  <version>18</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>FCS_Playback_EOS_DASH</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To test the End Of Stream detection scenario for a DASH stream through playbin gst element and westerossink</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <test_case_id>FCS_PLAYBACK_06</test_case_id>
    <test_objective>To test the End Of Stream detection scenario for a DASH stream through 'playbin' and 'westerossink' gst elements</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator, RPI</test_setup>
    <pre_requisite>1.TDK Agent should be up and running in the DUT
2. Test stream url for an DASH stream should be updated in the config variable video_src_url_short_duration_dash inside MediaValidationVariables.py library inside filestore
3. FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration should be set as yes/no in the device config file
4. FIREBOLT_COMPLIANCE_EOS_TIMEOUT configuration should be set to time to wait for receiving EOS</pre_requisite>
    <api_or_interface_used>Execute the mediapipelinetests application in DUT</api_or_interface_used>
    <input_parameters>testcasename - "test_EOS"
test_url - DASH url from MediaValidationVariables library (MediaValidationVariables.video_src_url_short_duration_dash)
"checkavstatus=yes" - argument to do the video playback verification from SOC side . This argument can be yes/no based on a device cofiguration(FIREBOLT_COMPLIANCE_CHECK_AV_STATUS) from Device Config file
timeout - a string to specify the time in seconds for waiting to receive EOS . This argument is the value of device cofiguration(FIREBOLT_COMPLIANCE_EOS_TIMEOUT) from Device Config file.The default timeout of test application is 6 minutes, so for EOS test cases, if the test stream is longer than 6 minutes the total timeout in seconds ( stream duration + ~5 seconds as buffer) should be explicitly specified in configuration parameter 'FIREBOLT_COMPLIANCE_EOS_TIMEOUT' inside device config file</input_parameters>
    <automation_approch>1.Load the systemuitl module 
2.Retrieve the FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_EOS_TIMEOUT config values from Device config file.
3.Retrieve the video_src_url_short_duration_dash variable from MediaValidationVariables library
4. Construct the mediapipelinetests command based on the retrieved video url, testcasename, FIREBOLT_COMPLIANCE_CHECK_AV_STATUS deviceconfig value and timeout
5.Execute the command in DUT
6.Verify the output from the execute command and check if the  "Failures: 0" and "Errors: 0" string exists
7.Based on the ExecuteCommand() return value and the output returned from the mediapipelinetests application, TM return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1. Verify the API call is success
Checkpoint 2. Verify that the output returned from mediapipelinetests contains the strings "Failures: 0" and "Errors: 0"</expected_output>
    <priority>High</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_Playback_EOS_DASH</test_script>
    <skipped>No</skipped>
    <release_version>M89</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import MediaValidationVariables
from rdkv_performancelib import *

#Test component to be tested
fcObj = tdklib.TDKScriptingLibrary("firebolt_compliance","1")
#Using systemutil library for command execution
sysUtilObj = tdklib.TDKScriptingLibrary("systemutil","1")

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
sysUtilObj.configureTestCase(ip,port,'FCS_Playback_EOS_DASH')

#Set device configurations to default values
checkAVStatus = "no"
#The default timeout of test application is 6 minutes, so for EOS test cases, if the test stream is longer than 6 minutes the total timeout in seconds ( stream duration + ~5 seconds as buffer) should be explicitly specified in configuration parameter 'FIREBOLT_COMPLIANCE_EOS_TIMEOUT' inside device config file
#the default timeout value given below is only for following the similar way as other FCS playback scripts, in EOS tests, the default timeout is 6 minutes
timeoutInSeconds = "10"

#Method to retrieve the device configuration from device config file
def getDeviceConfigValue (configKey):
    try:
        result = "SUCCESS"
        configValue = ""

        #Retrieve the device details(device name) and device type from tdk library
        deviceDetails = sysUtilObj.getDeviceDetails()
        deviceType = sysUtilObj.getDeviceBoxType()

        #Construct the tdkvRDKServiceConfig path in TM
        configPath = sysUtilObj.realpath+ "/" + "fileStore/tdkvRDKServiceConfig"

        #Construct the device configuration file path
        #The device configuration file can be either <device-name>.config or <box-type>.config, so we are checking for both
        deviceNameConfigFile = configPath + "/" + deviceDetails["devicename"] + ".config"
        deviceTypeConfigFile = configPath + "/" + deviceType + ".config"

        # Check whether device / platform config files are present
        if os.path.exists (deviceNameConfigFile) == True:
            deviceConfigFile = deviceNameConfigFile
        elif os.path.exists (deviceTypeConfigFile) == True:
            deviceConfigFile = deviceTypeConfigFile
        else:
            print "FAILURE : No Device config file found : " + deviceNameConfigFile + " or " + deviceTypeConfigFile
            result = "FAILURE"

        #Continue only if the device config file exists 
        if (len (deviceConfigFile) != 0):
            configParser = ConfigParser.ConfigParser()
            configParser.read(r'%s' % deviceConfigFile)
            #Retrieve the value of config key from device config file
            configValue = configParser.get('device.config', configKey)
        else:
            print "DeviceConfig file not available"
            result = "FAILURE"
    except Exception as e:
        print "Exception occurred while retrieving device configuration  : " + e
        result = "FAILURE"
    return result, configValue

#Load the systemutil library
sysutilloadModuleStatus =sysUtilObj.getLoadModuleResult()
print "[System Util LIB LOAD STATUS]  :  %s" %sysutilloadModuleStatus
sysUtilObj.setLoadModuleStatus(sysutilloadModuleStatus)

if "SUCCESS" in sysutilloadModuleStatus.upper():
    expectedResult="SUCCESS"
    
    #Construct the command with the url and execute the command in DUT
    tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand')
    
    #The test name specifies the test case to be executed from the mediapipeline test suite
    test_name = "test_EOS"

    #Test url for the stream to be played is retrieved from MediaValidationVariables library
    test_url = MediaValidationVariables.video_src_url_short_duration_dash

    #Retrieve the value of configuration parameter 'FIREBOLT_COMPLIANCE_CHECK_AV_STATUS' that specifies whether SOC level playback verification check should be done or not 
    actualresult, check_av_status_flag = getDeviceConfigValue('FIREBOLT_COMPLIANCE_CHECK_AV_STATUS')
    #If the value of FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is retrieved correctly and its value is "yes", argument to check the SOC level AV status should be passed to test application
    if expectedResult in actualresult.upper() and check_av_status_flag == "yes":
        print "Video playback status check is added"
        check_av_status = check_av_status_flag
    #Retrieve the value of configuration parameter 'FIREBOLT_COMPLIANCE_EOS_TIMEOUT' that specifies the EOS timeout in seconds
    #The default timeout of test application is 6 minutes, so for EOS test cases, if the test stream is longer than 6 minutes the total timeout in seconds ( stream duration + ~5 seconds as buffer) should be explicitly specified in configuration parameter 'FIREBOLT_COMPLIANCE_EOS_TIMEOUT' inside device config file
    actualresult, timeout = getDeviceConfigValue('FIREBOLT_COMPLIANCE_EOS_TIMEOUT')
        
    #If the value of FIREBOLT_COMPLIANCE_EOS_TIMEOUT is retrieved correctly and its value is not empty, its value should be passed as the timeout argument to the test application
    if expectedResult in actualresult.upper() and timeout != "":
        timeoutInSeconds = timeout

   
    #To do the AV playback through 'playbin' element, we are using 'mediapipelinetests' test application that is available in TDK along with required parameters
    command = "mediapipelinetests " + test_name + " " + test_url + " checkavstatus=" + check_av_status_flag + " timeout=" + timeoutInSeconds
    print "Executing command in DUT: ", command
    
    tdkTestObj.addParameter("command", command)
    tdkTestObj.executeTestCase(expectedResult)
    actualresult = tdkTestObj.getResult()
    output = tdkTestObj.getResultDetails()
    print "OUTPUT: ", output

    #If the output string returned from 'mediapipelinetests' contains "Failures: 0" and "Errors: 0", then the test suite executed successfully 
    if expectedResult in actualresult.upper() and output:
        passStringList = ["Failures: 0", "Errors: 0"]
        passString = "failed: 0"
        
        if ((all (token in output for token in passStringList)) or (passString in output)):
            tdkTestObj.setResultStatus("SUCCESS")
            print "EOS Detection for DASH stream using 'playbin' and 'westeros-sink' was successfull"
            print "Mediapipeline test executed successfully"
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print "EOS Detection for DASH stream using 'playbin' and 'westeros-sink' failed"
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print "Mediapipeline test execution failed"

    #Unload the modules
    sysUtilObj.unloadModule("systemutil")

else:
    print "Module load failed"
