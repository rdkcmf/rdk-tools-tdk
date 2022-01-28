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
#########################################################################

import os
import ConfigParser
import MediaValidationVariables
from devicesettings import *
# Global variable to store the operations string and use_aamp configuration
operations = ""
use_aamp = ""

#Execution log File
executionLogFile = " /opt/TDK/logs/AgentConsole.log "

#List consisting of HLS url
HLS_URL = [MediaValidationVariables.video_src_url_short_duration_hls,MediaValidationVariables.video_src_url_hls,MediaValidationVariables.video_src_url_4k_hls,MediaValidationVariables.video_src_url_live_hls,MediaValidationVariables.video_src_url_hls_h264,MediaValidationVariables.video_src_url_hls_h264_iframe]
URL_TYPE = {MediaValidationVariables.video_src_url_vp9 : MediaValidationVariables.vp9_url_type, MediaValidationVariables.video_src_url_hevc:MediaValidationVariables.hevc_url_type, MediaValidationVariables.video_src_url_dolby:MediaValidationVariables.dolby_url_type , MediaValidationVariables.video_src_url_opus:MediaValidationVariables.opus_url_type, MediaValidationVariables.video_src_url_aac:MediaValidationVariables.aac_url_type}

######################################################################
#
# Functions
#
######################################################################

#Function to retrieve the device configuration from device config file
def getDeviceConfigValue (tdklibObj, configKey):
    try:
        global use_aamp
        result = "SUCCESS"
        #Retrieve the device details(device name) and device type from tdk library
        configValue = ""
        deviceDetails = tdklibObj.getDeviceDetails()
        deviceType = tdklibObj.getDeviceBoxType()
        #Construct the tdkvRDKServiceConfig path in TM
        configPath = tdklibObj.realpath+ "/" + "fileStore/tdkvRDKServiceConfig"
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
            use_aamp = configParser.get('device.config',"FIREBOLT_COMPLIANCE_USE_AAMP_FOR_HLS")
        else:
            print "DeviceConfig file not available"
            result = "FAILURE"
    except Exception as e:
        print "Exception occurred while retrieving device configuration  : " + e
        result = "FAILURE"
    return result, configValue


# Function to construct the trickplay operations string from operation, timeout/duration and seek argument values
# Individual operation with arguments(timeout, position etc) should be passed as input (eg: setOperations (seek, 10, 20)
# Separate operations(eg: play:10,pause:10)  should be added by calling the setOperations() separatley
# (eg: setOperations (play, 10) , setOperations (pause, 10) etc)
# For repeating the previous trickplay operations give operation argument as "repeat", followed by the number of operations to be repeated and the repeat count (eg: setOperations (repeat, 1, 2)- for repeating last operation 2 times or setOperations (repeat, 2, 6)- for repeating last 2 operations 6 times etc)
def setOperations (operation, *arguments):
    try:
        global operations
        #if the repeat operation command is recieved, the previous operations should be repeated the number of times provided as the second argument to repeat
        #Repeat operation will not proceed if there are no previous operations in the string
        if operations and operation == "repeat":
            #The first argument to repeat is the number of previous operation that needs to be repeated
            numberOfOperations = arguments[0]
            #From the operations string, extract the last 'numberOfOperations' number of operations
            #since individual operations are seperated by ',', split the operations string to a list of strings
            splitList = [idx for idx, ch in enumerate(operations) if ch == ',']
            #If there are enough operations to be repeated, select the last 'numberOfOperations' number of operations
            if (len(splitList) > (numberOfOperations - 1)):
                splitIndex = splitList [-numberOfOperations]
                operationsToBeRepeated = operations[splitIndex+1:]
            else:
                operationsToBeRepeated = operations
                for indx in range (0, arguments[1]):
                    operations += "," + operationsToBeRepeated
        elif operation != "repeat":
            if operations != "":
                operations += ","
            operations += operation
            #Add all the arguments
            for argument in arguments:
                operations += ":" + argument
        #If there are no operations to be repeated, then repeat command is invalid
        else:
            raise Exception("There are no operations to be repeated")
    except Exception as e:
        print ("Exception occurred while updating the operations string  : " , e)

# Function to retrieve the saved trickplay operation string
def getOperations ():
    return operations

#Function to construct the mediapipelinetest command to be executed in the DUT
def getMediaPipelineTestCommand (testName, testUrl, **arguments):
    #First construct the command with mandatory arguments
    command = "mediapipelinetests " + testName + " " + testUrl
    #Based on the test, the arguments can vary, parse through the variabled arguments
    #and add the available variables
    for name, value in arguments.items ():
        command += " " + name + "=" + value

    #Feature to modify hls url to aamp url based on configuration
    if (use_aamp == "yes"):
        testUrl_list = testUrl.split();
        url_list = set()
        #Check if HLS URL is present in command
        url_list = (set(testUrl_list) & set(HLS_URL));
        for url in testUrl_list:
            if URL_TYPE.get(url, "not available").lower() == "hls":
                url_list.add(url);
        if url_list:
            for url in url_list:
                #Change hls generic url to aamp url
                url_updated = url.replace("https","aamps",1).replace("http","aamp",1);
                command = command.replace(url,url_updated);
            #Update GST_LOG_LEVEL to skip error statements check while using aamp for playback
            command = "export GST_LOG_LEVEL=0;  " + command;
    return command

#Function to check mediapipeline test execution status from output string
#Returns 'SUCCESS'/'FAILURE' based on the analysis of the output string
def checkMediaPipelineTestStatus (outputString):
    #If the output string returned from 'mediapipelinetests' contains strings "Failures: 0" and "Errors: 0"  or it contains string "failed: 0", then the test suite executed successfully otherwise the test failed
    passStringList = ["Failures: 0", "Errors: 0"]
    passString = "failed: 0"

    if ((all (token in outputString for token in passStringList)) or (passString in outputString)):
        result = "SUCCESS"
    else:
        result = "FAILURE"

    return result

def ResolutionTestStart(dsObj, resolution):
    result = dsManagerInitialize(dsObj)
    ResolutionSet = False
    ResolutionBeforePlayback = False
    gotResolution = False
    #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
    if "SUCCESS" in result:
         #Calling DS_IsDisplayConnectedStatus function to check for display connection status
         result = dsIsDisplayConnected(dsObj)
         if "TRUE" in result:
             #Save a copy of current resolution
             ResolutionBeforePlayback = dsGetResolution(dsObj,"SUCCESS",kwargs={'portName':"HDMI0"});
             resolutionList = dsGetSupportedResolutions(dsObj)
             if not resolutionList:
                 print "Unable to retrieve SupportedResolutionList\n"
             else:
                 resolutionSet = set(resolutionList)
                 #Check resolution is supported by the device
                 for i in range(0,len(resolutionList)):
                     if resolution in resolutionList[i]:
                        resolution = resolutionList[i]
                        gotResolution = True
                        break;
                 if not gotResolution:
                    print "%s is not supported by DUT\nTestcase not applicable for this platform"%resolution;
                    return False,"Not Applicable"
             if resolution != ResolutionBeforePlayback:
                 result = dsSetResolution(dsObj,"SUCCESS",kwargs={'portName':"HDMI0",'resolution':resolution});
                 if result != resolution:
                    print "[TEST EXECUTION] : FAILURE";
                 else:
                    ResolutionSet = True
             else:
                 print "Resolution value already set to %s\n Proceeding with playback "%resolution;
                 ResolutionSet = True
         else:
             print "\nTV not connected\nExiting from testcase";
    else:
        print "\nConnection Failed";
    return ResolutionSet,ResolutionBeforePlayback

def ResolutionTestStop(dsObj, resolution, ResolutionBeforePlayback=""):
    if resolution and resolution != ResolutionBeforePlayback:
        print "\nReverting resolution to %s"%ResolutionBeforePlayback
        result = dsSetResolution(dsObj,"SUCCESS",kwargs={'portName':"HDMI0",'resolution':ResolutionBeforePlayback});
        if result != ResolutionBeforePlayback:
            print "[TEST EXECUTION] : FAILURE\nResolution revert failed";
        else:
            print "Resolution reverted";
    result = dsManagerDeInitialize(dsObj)
    if "FAILURE" in result:
        print "dsManagerDeInitialize FAILED" 
    return result
