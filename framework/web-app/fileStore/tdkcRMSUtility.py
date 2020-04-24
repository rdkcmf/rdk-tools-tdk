#!/usr/bin/python
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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
#

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------
import os
import sys
import ConfigParser
import tdklib
import tdkcWEBUIUtility
import tdkcConfigParserUtility;
from tdkcWEBUIUtility import *
from tdkcConfigParserUtility import *;


#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------
def updateWIFIConf(obj,ssid,psk):
# Syntax      : updateWIFIConf()
# Description : Function to set network configurations in wpa_supplicant file
# Parameters  : ssid - name of the AP
#               psk  - pre-shared key for the connection
#               obj  - tdk library object
# Return Value: SUCCESS/FAILURE

    print "\nTEST STEP : To set network configurations in wpa_supplicant.conf file"
    print "EXPECTED RESULT : wpa_supplicant.conf should be updated"
    tdkTestObj = obj.createTestStep('ExecuteCmd_TDKC');
    expectedresult = "SUCCESS"
    tdk_path  = tdkcConfigParserUtility.tdk_path
    cmd = "sh " + tdk_path + "updateNetworkConfig.sh \"configure\" \"" + ssid + "\" \"" + psk + "\""
    print "Command to be executed : %s" %(cmd)
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    if expectedresult in actualresult:
        print "wpa_supplicant.conf updated successfully"
        print "ACTUAL RESULT  : Command Execution to set network configuration Success"
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        cmdOutput = tdkTestObj.getResultDetails();
        print "Value Returned : %s\n" %(cmdOutput)
        print "ACTUAL RESULT  : Command execution to set network configuration Failed"
        print "[TEST EXECUTION RESULT ] : FAILURE\n"
        tdkTestObj.setResultStatus("FAILURE");
    return actualresult

def isConnectedToWIFI(obj):
# Syntax      : isConnectedToWIFI()
# Description : Function to check wifi connection status
# Parameters  : obj  - tdk library object
# Return Value: TRUE/FALSE

    print "\nTEST STEP : To get wifi connection status using ifconfig command"
    print "EXPECTED RESULT : wifi connection status should be obtained"
    tdkTestObj = obj.createTestStep('ExecuteCmd_TDKC');
    expectedresult = "SUCCESS"
    cmd  = "ifconfig wlan0 | grep \"inet addr:\""
    print "Command to be executed : %s" %(cmd)
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    cmdOutput = tdkTestObj.getResultDetails();
    cmdOutput =  str(cmdOutput).replace('\\n',"\n").replace("\\\"","\"")
    if expectedresult in actualresult and "inet addr:" in cmdOutput:
        print "Value Returned : "
        print(cmdOutput)
        print "ACTUAL RESULT  : Command Execution to get wifi connection info Success : wlan0 is UP"
        tdkTestObj.setResultStatus("SUCCESS");
        return "TRUE"
    else:
        print "Value Returned : %s\n" %(cmdOutput)
        print "ACTUAL RESULT  : Command execution to get wifi connection status Failed : wlan0 is DOWN"
        print "[TEST EXECUTION RESULT ] : FAILURE\n"
        tdkTestObj.setResultStatus("FAILURE");
        return "FALSE"

def updateRMSConf(obj,roomID=""):
# Syntax      : updateRMSConf()
# Description : Function to set resolution, roomID in rms.conf and enable rms logging
# Parameters  : roomID - room name of the device
#               obj    - tdk library object
# Return Value: SUCCESS/FAILURE

    print "\nTEST STEP : Update resolution settings & room ID in rms.conf file and enable rms logging"
    print "EXPECTED RESULT : rms.conf should have required resolution,room ID & config.lua file append section should be uncommented"
    tdkTestObj = obj.createTestStep('ExecuteCmd_TDKC');
    expectedresult = "SUCCESS"
    tdk_path  = tdkcConfigParserUtility.tdk_path
    if roomID == "":
        cmd = "sh " + tdk_path + "updateRMSConf.sh \"configure\""
    else:
        cmd = "sh " + tdk_path + "updateRMSConf.sh \"configure\" \"" + roomID + "\""
    print "Command to be executed : %s" %(cmd)
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    if expectedresult in actualresult:
        print "rms.conf & config.lua updated successfully"
        print "ACTUAL RESULT  : Command Execution to update resolutions,room ID in rms.conf & enable rms logging Success"
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        cmdOutput = tdkTestObj.getResultDetails();
        tdkTestObj.setResultStatus("FAILURE");
        print "Value Returned : %s\n" %(cmdOutput)
        print "ACTUAL RESULT  : Command execution to set resolution ,room ID in rms.conf & enable rms logging Failed"
        print "[TEST EXECUTION RESULT ] : FAILURE\n"
    return actualresult

def isCameraStreaming(obj):
# Syntax      : isCameraStreaming()
# Description : Function to check whether camera is streaming or not
# Parameters  : obj  - tdk library object
# Return Value: TRUE/FALSE

    print "\n TEST STEP : Check whether the camera device is streaming or not, using rms log"
    print "EXPECTED RESULT : Should get log prints gst_InitFrame SUCCESS & Inbound connection accepted"
    tdkTestObj = obj.createTestStep('ExecuteCmd_TDKC');
    expectedresult = "SUCCESS"
    data1 = "gst_InitFrame SUCCESS"
    data2 = "Inbound connection accepted"
    cmd = "awk '/" + data1 + "/{print $0} /" + data2 + "/{print $0}' /opt/logs/rms.*.log"
    print "Command to be executed : %s" %(cmd)
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    if expectedresult in actualresult:
        cmdOutput = tdkTestObj.getResultDetails();
        cmdOutput = str(cmdOutput).replace('\\n',"\n").replace("\\\"","\"")
        print "Value Returned : "
        print cmdOutput
        if data1 and data2 in cmdOutput:
            tdkTestObj.setResultStatus("SUCCESS");
            print "ACTUAL RESULT : camera device is streaming properly"
            return "TRUE"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "ACTUAL RESULT : camera device is not streaming properly"
            print "[TEST EXECUTION RESULT ] : FAILURE\n"
            return "FALSE"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "ACTUAL RESULT : Not able to check whether camera device is streaming or not"
        print "[TEST EXECUTION RESULT ] : FAILURE\n"
        return "FALSE"

def revertWIFIConf(obj):
# Syntax      : revertWIFIConf()
# Description : Function to remove the configurations set in wpa_supplicant.conf
# Parameters  : obj  - tdk library object
# Return Value: SUCCESS/FAILURE

    print "\nTEST STEP : Revert wpa_supplicant.conf file"
    print "EXPECTED RESULT : Remove the configurations set from wpa_supplicant.conf"
    tdk_path  = tdkcConfigParserUtility.tdk_path
    tdkTestObj = obj.createTestStep('ExecuteCmd_TDKC');
    expectedresult = "SUCCESS"
    cmd = "sh " + tdk_path + "updateNetworkConfig.sh \"revert\""
    print "Command to be executed : %s" %(cmd)
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    if expectedresult in actualresult:
        print "wpa_supplicant.conf updated successfully"
        print "ACTUAL RESULT  : Command Execution to revert network configuration Success\n"
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        cmdOutput = tdkTestObj.getResultDetails();
        print "ACTUAL RESULT  : Command execution to revert network configuration Failed\n"
        print "Value Returned : %s\n" %(cmdOutput)
        print "[TEST EXECUTION RESULT ] : FAILURE\n"
        tdkTestObj.setResultStatus("FAILURE");
    return actualresult


def revertRMSConf(obj):
# Syntax      : revertRMSConf()
# Description : Function to remove the configurations set in rms.conf and disable rms logging
# Parameters  : obj  - tdk library object
# Return Value: SUCCESS/FAILURE

    print "\nTEST STEP : Revert the configurations in rms.conf and disable rms logging"
    print "EXPECTED RESULT : rms.conf should be reverted & config.lua file append section should be commented"
    tdkTestObj = obj.createTestStep('ExecuteCmd_TDKC');
    expectedresult = "SUCCESS"
    tdk_path  = tdkcConfigParserUtility.tdk_path
    cmd = "sh " + tdk_path + "updateRMSConf.sh \"revert\""
    print "Command to be executed : %s" %(cmd)
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "rms.conf & config.lua reverted successfully"
        print "ACTUAL RESULT  : Command Execution to revert configurations in rms.conf & disable rms logging Success\n"
    else:
        cmdOutput = tdkTestObj.getResultDetails();
        tdkTestObj.setResultStatus("FAILURE");
        print "Value Returned : %s\n" %(cmdOutput)
        print "ACTUAL RESULT  : Command Execution to revert configurations in rms.conf & disable rms logging Failed\n"
        print "[TEST EXECUTION RESULT ] : FAILURE\n"
    return actualresult

def updateWEBRTCDemoPage(driver):
# Syntax      : updateWEBRTCDemoPage()
# Description : Function to set info in demo page and verify it
# Parameters  : driver - selenium webdriver
# Return Value: SUCCESS/FAILURE

    updStatus = "FAILURE"
    print "\nTEST STEP : Set WebRTC info in WebRTC Demo page"
    print "EXPECTED RESULT : WebRTC info should be set and show debug msg should be enabled"
    status = tdkcWEBUIUtility.setWebRTCInfoInWEBUI(driver)
    if status == "SUCCESS":
        print "ACTUAL RESULT : WebRTC info is set & show debug msg enabled successfully\n"
        time.sleep(10);

        print "\nTEST STEP : Get WebRTC info in WebRTC Demo page"
        print "EXPECTED RESULT : Should get the current WebRTC info "
        status,info = tdkcWEBUIUtility.getWebRTCInfoInWEBUI(driver)
        if status == "SUCCESS":
            print "Value Returned : ",info
            print "ACTUAL RESULT  : current WebRTC info retrieved successfully"

            print "\nTEST STEP : Verify WebRTC info in  WebRTC Demo page"
            print "EXPECTED RESULT : current WebRTC info should be same as that of values set"
            status = tdkcWEBUIUtility.verifyWebRTCInfoInWEBUI(driver)
            if status == "SUCCESS":
                updStatus = "SUCCESS"
                print "ACTUAL RESULT : Proper WebRTC info is available in demo page"

            else:
                print "ACTUAL RESULT : WebRTC info in demo page is not proper"
                print "[TEST EXECUTION RESULT ] : FAILURE\n"
        else:
            print "ACTUAL RESULT : get current  WebRTC info failed"
            print "[TEST EXECUTION RESULT ] : FAILURE\n"
    else:
        print "ACTUAL RESULT : WebRTC info set & enable show debug failed"
        print "[TEST EXECUTION RESULT ] : FAILURE\n"
    return updStatus

