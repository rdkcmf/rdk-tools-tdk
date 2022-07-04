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

import re
import tdklib;
import ConfigParser
import os
from tdkvutility import *

#Define the search term:
pattern = "VALIDATION"

#Create an empty list:
tests = []
expectedResult="SUCCESS";
log_transfer = "yes";

#Function to retrieve the device configuration from device config file
def getDeviceConfigValue (tdklibObj, configKey):
    try:
        global log_transfer;
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
            if configKey == "FIREBOLT_COMPLIANCE_TRANSFER_LOG":
                log_transfer = configValue;
        else:
            print "DeviceConfig file not available"
            result = "FAILURE"
    except Exception as e:
        print "Exception occurred while retrieving device configuration  : " + e
        result = "FAILURE"
    return result, configValue

def getLogFile(obj):
    #Get EssosTestApp configuration file
    try:
        GraphicsValidationConfigFile = obj.realpath+'fileStore/GraphicsValidation_log.config'
        configParser = ConfigParser.ConfigParser()
        configParser.read(r'%s' % GraphicsValidationConfigFile )
        #EssosValidation execution log file
        GraphicsValidation_log = configParser.get('GraphicsTestApp-config', 'logfile')
        logFile = GraphicsValidation_log.split('/')
        logFile = logFile[-1]
        print "GraphicsValidation Execution Log File Name : " , logFile
        return logFile,GraphicsValidation_log
    except:
        print "\nUnable to acquire log file from GraphicsValidation_log.config\nConfigure the log file in GraphicsValidation_log.config to proceed with the testcase"
        exit()

#Prints the given string in title format
def PrintTitle(string=" ",title=0):
    print "#"*50
    print string
    if title:
        print "#"*50

#Lists the number of failures observed as part of the execution
#Parses the output from the Test app and returns the total number of failures
def getNumberOfFailures(obj,fileName,checkPattern=""):
    failed = 0;
    if (log_transfer == "no"):
        result,details,tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command":"cat GraphicsTDKTest.txt | wc -l"}, True)
        if int(details.strip(r'\n')):
            if not checkPattern:
               result,details,tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command":"grep -inr error GraphicsTDKTest.txt | wc -l"}, True)
            else:
               command = "grep -inr " + checkPattern + " GraphicsTDKTest.txt | grep -inr error | wc -l"
               result,details,tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command":command}, True)
            failed = int(details.strip(r'\n'));
        else:
            print "Execution failed";
            return "error"
    else:
        if os.path.exists(fileName):
            if os.stat(fileName).st_size == 0:
                print "Execution failed";
                return "error"
        for line in open(fileName):
            if line !='':
                if checkPattern:
                    word = re.findall(checkPattern, line)
                else:
                    word = True;
                if word:
                    if "ERROR" in line.upper():
                        failed = failed +1;
    print "Number of FAILURES:",failed
    return failed

#Lists the Summary details of the testcases performed in the execution
################################# Sample Output ###############################################
###############################################################################################
#VALIDATION SUCCESS : EssContextCreate()
#VALIDATION SUCCESS : EssContextSetTerminateListener( ctx, 0, &terminateListener )
#VALIDATION SUCCESS : EssContextSetKeyListener( ctx, 0, &keyListener )
#VALIDATION SUCCESS : EssContextSetPointerListener( ctx, 0, &pointerListener )
#VALIDATION SUCCESS : EssContextSetTouchListener( ctx, 0, &touchListener )
#VALIDATION SUCCESS : EssContextSetSettingsListener( ctx, ctx, &settingsListener )
#VALIDATION SUCCESS : EssContextSetGamepadConnectionListener( ctx, ctx, &gpConnectionListener )
#VALIDATION SUCCESS : EssContextInit( ctx )
###############################################################################################
###############################################################################################
def Summary(fileName,PATTERN=""):
    gotInfo = False;
    if PATTERN:
        pattern = PATTERN;
    else:
        pattern = "ERROR"
    for line in open(fileName):
        if line !='':
            word = re.findall(pattern, line)
            if word:
                print line.strip('\n')
                gotInfo = True;
    return gotInfo

#Deletes the logFile present in DUT
def deleteLogFile(obj,GraphicsValidation_log,GraphicsValidationExecutionStatus):
    print "\nDelete the GraphicsValidation Execution log file from STB"
    tdkTestObj = obj.createTestStep('ExecuteCommand');
    cmd = "rm " + GraphicsValidation_log
    print cmd;
    #configre the command
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    if expectedResult in actualResult:
        print "GraphicsValidation Execution log file deleted from STB"
        tdkTestObj.setResultStatus("SUCCESS");
        if "FAILURE" in GraphicsValidationExecutionStatus:
            PrintTitle("GraphicsValidationExecution Status is FAILURE",1);
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print "Unable to delete GraphicsValidation Execution log file from STB"
        tdkTestObj.setResultStatus("FAILURE");


#Executes the configured Test APP
def RunTest(obj,Test,logFile,options=""):
    #Prmitive test case which associated to this Script
    print "\nStarting Test Execution\n"
    tdkTestObj = obj.createTestStep('ExecuteCommand');
    #Test to be executed
    cmd = "sh RunGraphicsTDKTest.sh " + Test + " " + options;
    #log the app output in a logFile
    cmd =  cmd + " > " + logFile;
    tdkTestObj.addParameter("command", cmd);
    #Execute the test case in STB
    tdkTestObj.executeTestCase("SUCCESS");
    #Get the result of execution
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "[TEST EXECUTION RESULT] : %s" %actualResult;
    if expectedResult not in actualResult:
        print "Unable to execute %s" %(test);
        tdkTestObj.setResultStatus("FAILURE");
    return details
