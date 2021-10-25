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
# module imports
#------------------------------------------------------------------------------

import os
import sys
import time
import urllib2
import requests
import json,ast
import ConfigParser
import xml.etree.ElementTree as ET
from tdkvRDKServicesSupportlib import *
from tdkvRDKServicesEventHandlerlib import *


#-----------------------------------------------------------------------------------------------
# getDeviceConfigKeyValue
#-----------------------------------------------------------------------------------------------
# Syntax      : getDeviceConfigKeyValue(key)
# Description : Method to get the value of the provided key from the device config file
# Parameter   : key - Tag configured in the device config file
# Return Value: Function execution status (SUCCESS/FAILURE) & Key Value
#-----------------------------------------------------------------------------------------------

def getDeviceConfigKeyValue(key):
    value  = ""
    status = "SUCCESS"

    try:
        # If the key is none object or empty then exception
        # will be thrown
        if key is None or key == "":
            status = "FAILURE"
            print "\nException Occurred: [%s] key is None or empty" %(inspect.stack()[0][3])
        # Parse the device configuration file and read the
        # data. But if the data is empty it is taken as such
        else:
            config = ConfigParser.ConfigParser()
            config.read(deviceConfigFile)
            value = str(config.get(deviceConfig,key))
    except Exception as e:
        status = "FAILURE"
        print "\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e)

    return status,value


#-----------------------------------------------------------------------------------------------
# readDeviceConfigKeys
#-----------------------------------------------------------------------------------------------
# Syntax      : readDeviceConfigKeys(keys)
# Description : Method to get the value of the all the given keys from the device config file
# Parameter   : keys - List of tags configured in the device config file
# Return Value: Overall key read status (SUCCESS/FAILURE) & Key Values
#-----------------------------------------------------------------------------------------------
def readDeviceConfigKeys(keys):
    value  = ""
    allstatus = []
    allvalues = []
    # If the keys are none object or empty then exception
    # will be thrown
    if keys is None or keys == "":
        status = "FAILURE"
        print "\nException Occurred: [%s] key is None or empty" %(inspect.stack()[0][3])
    else:
        keys = keys.split(",")
        for key in keys:
            status,result = getDeviceConfigKeyValue(key)
            allstatus.append(status)
            allvalues.append(result)
        value = ",".join(allvalues)
        if "FAILURE" in allstatus:
            status = "FAILURE"
        else:
            status = "SUCCESS"

    return status,value



#-----------------------------------------------------------------------------------------------
# executePluginTests
#-----------------------------------------------------------------------------------------------
# Syntax      : executePluginTests(deviceIP,port,deviceName,deviceType,basePath, pluginName, testCaseID)
# Description : Method to check whether Plugins template xml and given plugin test case
#               xmls exists and start the test execution
# Parameter   : pluginName - name of the plugin
#             : deviceIP - IP of the test device
#             : port     - Port for testing
#             : deviceName - name of the test device
#             : deviceType - type of the test device
#             : basePath   - TDK TM webapps path
#             : testCaseID - test case Id. By default all the test cases will be executed
# Return Value: SUCCESS/FAILURE
#-----------------------------------------------------------------------------------------------

def executePluginTests(libobj, deviceIPAddress, devicePort, testDeviceName, testDeviceType, basePath, TMUrl, pluginName, testCaseID="all"):

    # This method is the entry-point to the RDK Services Testing
    # framework. API should be invoked from external lib/script

    # Port Number to be used for sending the JSON request
    global portNo
    portNo = str(devicePort)
    # Method of sending the JSON request like (curl/others)
    global execMethod

    # IP of the test device passed from external lib/script
    global deviceIP
    deviceIP = str(deviceIPAddress)

    # Name of the test device passed from external lib/script
    global deviceName
    deviceName = str(testDeviceName)

    # Type of the test device passed from external lib/script
    global deviceType
    deviceType = str(testDeviceType)

    # By default, [device.config] section will be taken
    # from config file. Different sections can be added
    # and used in future
    global deviceConfig
    deviceConfig  = "device"   + ".config"
    #deviceConfig = deviceName + ".config"

    # TM base path
    global basePathLoc
    basePathLoc = basePath

    # TM Url
    global tmURL
    tmURL = TMUrl

    # TDK lib object
    global libObj
    libObj = libobj.parentTestCase

    # Check if performance enabled
    global IsPerformanceSelected
    IsPerformanceSelected = libObj.performanceBenchMarkingEnabled

    # Response time threshold for performance measurement
    global maxResponseTime

    # Form the path of the plugin XMLs
    global pluginXML
    global pluginTestCaseXML
    XMLPath  = basePath + "/" + "fileStore/tdkvRDKServiceXMLs"
    pluginXML = XMLPath + "/" + "ThunderPlugins"   + ".xml"
    pluginTestCaseXML = XMLPath + "/" + pluginName + "Plugin_TestCases.xml"

    # Check whether plugin XML files required for executing
    # the test are present
    status = "SUCCESS"
    if os.path.exists(pluginXML) == False:
        print "Cannot proceed : File %s not found" %(pluginXML)
        status = "FAILURE"
    if os.path.exists(pluginTestCaseXML) == False:
        print "Cannot proceed : File %s not found" %(pluginTestCaseXML)
        status = "FAILURE"


    global deviceConfigFile
    configPath = basePath + "/"   + "fileStore/tdkvRDKServiceConfig"
    deviceNameConfigFile = configPath + "/" + deviceName + ".config"
    deviceTypeConfigFile = configPath + "/" + deviceType + ".config"

    # Check whether device / platform config files required for
    # executing the test are present
    if os.path.exists(deviceNameConfigFile) == True:
        deviceConfigFile = deviceNameConfigFile
        print "[INFO]: Using Device config file: %s" %(deviceNameConfigFile)
    elif os.path.exists(deviceTypeConfigFile) == True:
        deviceConfigFile = deviceTypeConfigFile
        print "[INFO]: Using Device config file: %s" %(deviceTypeConfigFile)
    else:
        status = "FAILURE"
        print "[ERROR]: No Device config file found : %s or %s" %(deviceNameConfigFile,deviceTypeConfigFile)

    # If config file is found, then get the execMethod details.
    if status == "SUCCESS":
        status1,execMethod = getDeviceConfigKeyValue("EXEC_METHOD")
        if status1 == "SUCCESS" and execMethod != "":
            status = "SUCCESS"
            print "[INFO]: Device Port No used for testing : ",portNo
            print "[INFO]: Method for Sending JSON request : ",execMethod
        else:
            status = "FAILURE"
            print "[ERROR]: No proper test EXEC_METHOD input"

    # If Performance measurement enabled, get the max response time
    if status == "SUCCESS" and IsPerformanceSelected == "true":
        status2,maxResponseTime = getDeviceConfigKeyValue("MAX_RESPONSE_TIME")
        if status2 == "SUCCESS" and str(maxResponseTime).strip() != "":
            print "[INFO]: Performance measurement Enabled, MAX_RESPONSE_TIME : %s" %(maxResponseTime)
        else:
            status = "FAILURE"
            print "[ERROR]: No proper MAX_RESPONSE_TIME input for performance measurement"


    # Start the test execution and get the plugin test status
    if status == "SUCCESS":
        pluginTestsStatus = executeTestCases(testCaseID)
        if "FAILURE" in pluginTestsStatus:
            status = "FAILURE"

    print "\nFinal Plugin Tests Status: %s\n" %(status)
    return status



#-----------------------------------------------------------------------------------------------
# executeTestCases
#-----------------------------------------------------------------------------------------------
# Syntax      : executeTestCases(testCaseID)
# Description : Method to perform below steps based on the configurations present in
#               plugin test case XML
#               a. execute Pre-requisite steps
#               b. execute all the Test Cases
#               c. execute Post-requisite steps
# Parameter   : testCaseID - test case Id. By default all the test cases will be
#               executed
# Return Value: List of status (SUCCESS/FAILURE)
#-----------------------------------------------------------------------------------------------

def executeTestCases(testCaseID="all"):

    # Parse the plugin template & test case XMLs and get the
    # root node

    global thunderPlugins
    global testPlugin
    try:
        tree1 = ET.parse(pluginXML)
        tree2 = ET.parse(pluginTestCaseXML)

        thunderPlugins = tree1.getroot()
        testPlugin = tree2.getroot()

    except Exception as e:
        print "\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e)
        return ["FAILURE"]

    # Get the testPlugin node information such as pluginName and PluginVersion
    testPluginInfo = getTestPluginInfo(testPlugin)
    print "\n####################################################################################"
    print "              PLUGIN NAME :  %s   " %(testPluginInfo.get("pluginName").upper())
    print "####################################################################################"
    print "PLUGIN TOTAL TEST CASES: %d\n" %(len(testPlugin.findall("testCase")))

    global testStepJSONCmd
    global testStepResults
    testStepResults = []
    global bktestStepResults
    bktestStepResults = []
    global revertTestInfo
    revertTestInfo = {}
    global pluginPreRequisiteStatus
    pluginPreRequisiteStatus = []
    global pluginPostRequisiteStatus
    pluginPostRequisiteStatus = []

    global iterInterval
    iterInterval = 0
    global repeatInterval
    repeatInterval = 0

    global eventListener
    eventListener = None
    global eventsInfo
    eventsInfo = {}
    global logDisplay
    logDisplay = True

    global eventResgisterTag
    eventResgisterTag = None
    global eventsBufferBackup
    eventsBufferBackup = []

    global customTimeout
    customTimeout = None

    global apiPerformanceInfo
    apiPerformanceInfo = []

    # ------------------------------- PLUGIN PRE-REQUISITES ----------------------------------
    # Perform plugin pre-requisite steps such as activate or deactivate plugins common for all
    # the tests . Revert operations are not supported as part of pre/post requisite steps. If
    # any of the plugin pre-requisite fails then none of the test cases will be executed.

    if testPlugin.find("pluginPreRequisite") is not None:
        print "#---------------------------- Plugin Pre-requisite ----------------------------#"
        pluginPreRequisiteStatus = executePrePostRequisite(testPlugin.find("pluginPreRequisite"),"Pre")
        if "FAILURE" in pluginPreRequisiteStatus:
            print "\nPlugin Pre-requisite Status: FAILURE"
            totalTests = len(testPlugin.findall("testCase"))
            dispTestSummary(testPluginInfo.get("pluginName").upper(),totalTests,0,0,0,0)
            # Log API Performance data if enabled
            if IsPerformanceSelected == "true":
                performanceStatus = dispPerformanceSummary()
            return pluginPreRequisiteStatus
        else:
            print "\nPlugin Pre-requisite Status: SUCCESS"


    global pluginTestsSummary
    pluginTestsSummary = []
    global combinedTestStatus
    combinedTestStatus = []

    # Execute all the test cases one by one and update test case name, Id and status into
    # pluginTestsSummary, if testCaseID="all"
    for testCase in testPlugin.findall("testCase"):
        testCaseInfo = getTestCaseInfo(testCase).copy()

        if testCaseID != "all" and testCaseID != testCaseInfo.get("testCaseId"):
            continue;

        print "\n\n"
        print "#==============================================================================#"
        print "TEST CASE NAME   : " ,testCaseInfo.get("testCaseName")
        print "TEST CASE ID     : " ,testCaseInfo.get("testCaseId")
        print "DESCRIPTION      : " ,testCaseInfo.get("desc")
        print "#==============================================================================#"

        # Check if the test case is configurable for a device/platform or a general one. If the test case
        # is configurable, then check its applicability for the current test device by checking the device
        # config file. If the test case is not applicable then mark it as N/A and proceed to the next one
        if testCaseInfo.get("configurableTest") == "true":
            status,keyData = readDeviceConfigKeys(testCaseInfo.get("testKey"))
            keyData = keyData.split(",") if keyData != "" else keyData

            if testCaseInfo.get("arguments") is not None and testCaseInfo.get("arguments") != "":
                arg = testCaseInfo.get("arguments").split(",")
            else:
                arg = ""
            if status == "SUCCESS":
                status,testCaseApplicability = checkTestCaseApplicability(testCaseInfo.get("useMethodTag"),keyData,arg)
                if status == "SUCCESS" and testCaseApplicability == "FALSE":
                    print "\n This test case is N/A, proceeding to next test"
                    pluginTestsSummary.append({"testCaseName":testCaseInfo.get("testCaseName"), "testCaseId":testCaseInfo.get("testCaseId"), "status":"N/A"})
                    print "\n##--------- [TEST EXECUTION STATUS] : N/A ----------##"
                    continue;
                elif status == "FAILURE":
                    print "\nError Occurred while checking test case applicability\n"
            else:
                print "\nError Occurred while checking test case applicability\n"

            if status == "FAILURE":
                pluginTestsSummary.append({"testCaseName":testCaseInfo.get("testCaseName"), "testCaseId":testCaseInfo.get("testCaseId"), "status":"FAILURE"})
                print "\n##--------- [TEST EXECUTION STATUS] : FAILURE ----------##"
                continue;


        testStepResults = []
        revertTestInfo  = {}
        testCasePreRequisiteStatus  = []
        testCasePostRequisiteStatus = []

        if eventListener is not None:
            eventListener.clearEventsBuffer()

        # ---------------------------- TEST CASE PRE-REQUISITE  --------------------------------
        # Perform test case pre-requisite steps such as activate or deactivate plugins specific
        # for the current test case alone. If any of the pre-requisite steps fails then the
        # current test will not be executed and marked as failure

        if testCase.find("testCasePreRequisite") is not None:
            print "\n#-------------- Test Case Pre-Requisite ---------------#"
            testCasePreRequisiteStatus = executePrePostRequisite(testCase.find("testCasePreRequisite"),"Pre")
            if "FAILURE" in testCasePreRequisiteStatus:
                pluginTestsSummary.append({"testCaseName":testCaseInfo.get("testCaseName"), "testCaseId":testCaseInfo.get("testCaseId"), "status":"FAILURE"})
                print "\nTest Case Pre-requisite Status: FAILURE\n"
                continue;
            else:
                print "\nTest Case Pre-requisite Status: SUCCESS\n"

        testStepResults = []
        revertTestInfo  = {}
        allTestStepStatus = []
        global currentTestStepId
        currentTestStepId = 0
        global currentIterationId
        currentIterationId = 0

        # ---------------------------- TEST TYPE DIRECT / SETANDGET ----------------------------
        # Test Case consist of list of test steps (API calls) which gets executed one by one
        # without any looping. After executing all the test steps, revert action takes place,
        # if testCaseType is setandget and revert is enabled

        if testCaseInfo.get("testCaseType") == "direct" or testCaseInfo.get("testCaseType") == "setandget":
            for testStep in testCase.findall("testStep"):
                currentTestStepId = testStep.attrib.get("testStepId")
                setTestStepDelay(testStep.attrib)
                status = executeTestStepDirect(testCaseInfo,testStep)
                if status == "FAILURE":
                    allTestStepStatus.append(status)
                    break;
                elif status == "FALSE":
                    continue;
                else:
                    allTestStepStatus.append(status)

            # IF the testCaseType is setandget, revert enabled and revertGet/revertSet/revertFlag
            # test steps are SUCCESS, then perform revert operation
            if testCaseInfo.get("testCaseType") == "setandget" and testCaseInfo.get("revert") == "true":
                if revertTestInfo.get("revertFlags") is not None:
                    if "TRUE" in [ flag.get("status") for flag in revertTestInfo.get("revertFlags")]:
                        revertTestStepStatus = revertTest(revertTestInfo)
                        allTestStepStatus.extend(revertTestStepStatus)


        # ---------------------------- TEST TYPE LOOP  -----------------------------------------
        # Test Case consist of list of test steps which may or may not contain sub-test steps
        # If testStepType is not loop, then those test steps are executed normally. If testStepType
        # is loop, then all the sub-test steps are iterated collectively based on the iteration
        # parameter. After executing all the test steps, revert action takes place,if revert is enabled

        elif testCaseInfo.get("testCaseType") == "loop":
            for testStep in testCase.findall("testStep"):
                currentTestStepId = testStep.attrib.get("testStepId")
                setTestStepDelay(testStep.attrib)
                iterInterval = 0
                if testStep.attrib.get("iterInterval") is not None:
                    iterInterval = int(testStep.attrib.get("iterInterval"))

                if testStep.attrib.get("testStepType") == "loop":
                    loopTestStepStatus = executeTestStepLoop(testCaseInfo,testStep)
                    if "FAILURE" in loopTestStepStatus:
                        allTestStepStatus.append("FAILURE")
                        break;
                    elif "FALSE" in loopTestStepStatus:
                        continue;
                    else:
                        allTestStepStatus.append("SUCCESS")
                else:
                    status = executeTestStepDirect(testCaseInfo,testStep)
                    if status == "FAILURE":
                        allTestStepStatus.append(status)
                        break;
                    elif status == "FALSE":
                        continue;
                    else:
                        allTestStepStatus.append(status)

            # If revert enabled and revertGet/revertSet/revertFlag test step status are SUCCESS,
            # perform revert operation
            if testCaseInfo.get("revert") == "true" and revertTestInfo.get("revertFlags") is not None:
                if "TRUE" in [ flag.get("status") for flag in revertTestInfo.get("revertFlags")]:
                    revertTestStepStatus = revertTest(revertTestInfo)
                    allTestStepStatus.extend(revertTestStepStatus)


        # ---------------------------- TEST TYPE STRESS ----------------------------------------
        # Test Case consist of list of test steps which may or may not contain sub-test steps
        # If testStepType is not repeat, then those test steps are executed normally. If testStepType
        # is repeat, then all the sub-test steps are repeated collectively for given repeat number
        # of times. After executing all the test steps, revert action takes place,if revert is enabled
        # STRESS test case type does not support loop test step

        elif testCaseInfo.get("testCaseType") == "stress":
            repeatValError = 0
            repeatMax = testCaseInfo.get("repeat")
            if testCaseInfo.get("configurableRepeat") == "true":
                status,result = getDeviceConfigKeyValue(testCaseInfo.get("repeatKey"))
                if status == "SUCCESS" and str(result).strip() != "":
                    repeatMax = result
                elif str(result).strip() == "":
                    repeatValError = 1
                    print "\nException Occurred: No Repeat count provided in config file\n"
                else:
                    repeatValError = 1
            elif repeatMax is None or str(repeatMax).strip() == "":
                repeatValError = 1
                print "\nException Occurred: No Repeat count provided\n"

            repeatStepStatus = []
            if repeatValError == 0:
                for testStep in testCase.findall("testStep"):
                    currentTestStepId = testStep.attrib.get("testStepId")
                    setTestStepDelay(testStep.attrib)
                    repeatInterval = 0
                    if testStep.attrib.get("repeatInterval") is not None:
                        repeatInterval = int(testStep.attrib.get("repeatInterval"))

                    if testStep.attrib.get("testStepType") == "repeat":
                        repeatStepStatus = executeTestStepRepeat(testCaseInfo,testStep,repeatMax)
                        if "FAILURE" in repeatStepStatus:
                            allTestStepStatus.append("FAILURE")
                            break;
                        elif "FALSE" in repeatStepStatus:
                            continue;
                        else:
                            allTestStepStatus.append("SUCCESS")
                    else:
                        status = executeTestStepDirect(testCaseInfo,testStep)
                        if status == "FAILURE":
                            allTestStepStatus.append(status)
                            break;
                        elif status == "FALSE":
                            continue;
                        else:
                            allTestStepStatus.append(status)

                # If revert enabled and revertGet/revertSet/revertFlag test step status are SUCCESS,
                # perform revert operation
                if testCaseInfo.get("revert") == "true" and revertTestInfo.get("revertFlags") is not None:
                    if "TRUE" in [ flag.get("status") for flag in revertTestInfo.get("revertFlags")]:
                        revertTestStepStatus = revertTest(revertTestInfo)
                        allTestStepStatus.extend(revertTestStepStatus)
            else:
                allTestStepStatus.append("FAILURE")

        if "FAILURE" in allTestStepStatus:
            print "\n##--------- [TEST EXECUTION STATUS] : FAILURE ----------##\n"
        else:
            print "\n##--------- [TEST EXECUTION STATUS] : SUCCESS ----------##\n"


        testStepResults = []
        revertTestInfo = {}

        # ---------------------------- TEST CASE POST-REQUISITE --------------------------------
        # Perform test case post-requisite steps such as activate or deactivate plugins specific
        # for the current test case alone. If any of the post-requisite steps fails then the
        # current test will be marked as failure

        if testCase.find("testCasePostRequisite") is not None:
            print "\n#-------------- Test Case Post-Requisite --------------#"
            testCasePostRequisiteStatus = executePrePostRequisite(testCase.find("testCasePostRequisite"),"Post")
            if "FAILURE" in testCasePostRequisiteStatus:
                print "\nTest Case Post-requisite Status: FAILURE\n"
            else:
                print "\nTest Case Post-requisite Status: SUCCESS\n"

        # Update the test case status by checking the status of each test steps executed
        # (directly / repeatedly / looped) and test case post-requisite execution status
        if "FAILURE" in allTestStepStatus or "FAILURE" in testCasePostRequisiteStatus:
            pluginTestsSummary.append({"testCaseName":testCaseInfo.get("testCaseName"), "testCaseId":testCaseInfo.get("testCaseId"), "status":"FAILURE"})
        else:
            pluginTestsSummary.append({"testCaseName":testCaseInfo.get("testCaseName"), "testCaseId":testCaseInfo.get("testCaseId"), "status":"SUCCESS"})


        if testCaseID != "all" and testCaseID == testCaseInfo.get("testCaseId"):
            break;



    # After executing all the test cases, store the status of each test case in combinedTestStatus
    combinedTestStatus = [ test.get("status") for test in pluginTestsSummary ]
    if combinedTestStatus == [] and testCaseID != "all":
        combinedTestStatus.append("FAILURE")
        print "\nException Occurred: Provided Test Case ID %s not found" %(testCaseID)

    testStepResults = []
    revertTestInfo  = {}

    # ------------------------------- PLUGIN POST-REQUISITES ----------------------------------
    # Perform plugin post-requisite steps such as activate or deactivate plugins, common for
    # all test cases. Revert operations are not supported as part of pre/post requisite steps
    # if any pos-requisite step fails then plugin execution status will be marked as failure

    if testPlugin.find("pluginPostRequisite") is not None or eventListener is not None:
        print "\n#---------------------------- Plugin Post-requisite ----------------------------#"
        if eventListener is not None:
            print "\nPost Requisite : UnRegister_Events"
            print "Post Requisite No : 0"
            print "------------- Event-Handling -------------"
            eventListener.disconnect()
            unRegisterStatus = getEventsUnRegistrationInfo()
            print "\n#--------- [Post-requisite Status] : %s ----------#" %(unRegisterStatus[0])
        if testPlugin.find("pluginPostRequisite") is not None:
            pluginPostRequisiteStatus = executePrePostRequisite(testPlugin.find("pluginPostRequisite"),"Post")
        if eventListener is not None:
            pluginPostRequisiteStatus.extend(unRegisterStatus)

        if "FAILURE" in pluginPostRequisiteStatus:
            print "\nPlugin Post-requisite Status: FAILURE"
        else:
            print "\nPlugin Post-requisite Status: SUCCESS"


    # Append the post-requisite step status along with test cases status
    combinedTestStatus.extend(pluginPostRequisiteStatus)

    # Display PASSED / FAILED / N/A Test list and plugin Summary details
    dispPluginTestsSummary(testPluginInfo.get("pluginName").upper(),pluginTestsSummary)

    # Log API Performance data if enabled
    if IsPerformanceSelected == "true":
        performanceStatus = dispPerformanceSummary()
        combinedTestStatus.append(performanceStatus)

    return combinedTestStatus



#-----------------------------------------------------------------------------------------------
# executePrePostRequisite
#-----------------------------------------------------------------------------------------------
# Syntax      : executePrePostRequisite(prepostrequisite)
# Description : Method to execute the pre-post requisite steps
# Parameter   : prepostrequisite - plugin pre/post requisite node
#             : node - Pre/Post
# Return Value: List of pre/post requisite step status (SUCCESS/FAILURE)
#-----------------------------------------------------------------------------------------------

def executePrePostRequisite(prepostrequisite,node):

    # In test case XML, pluginPreRequisite / pluginPostRequisite node
    # or testCasePreRequisite / testCasePostRequisite node within testCase
    # can have N number of prerequisite / postrequisite tags and each
    # pre/post requisite can have N number of test steps of two types
    # (direct/loop). Revert operations are not supported
    allprepostRequisiteStatus = []

    # Executing all the pre/post requisites one by one and updating
    # the status
    for requisite in prepostrequisite:
        global testStepResults
        testStepResults = []
        requisiteInfo = requisite.attrib.copy()
        if logDisplay:
            print "\n%s Requisite : %s" %(node,requisiteInfo.get("requisiteName"))
            print "%s Requisite No : %s" %(node,requisiteInfo.get("requisiteId"))

        if requisiteInfo.get("type") == "eventRegister" and eventListener is None:
            global eventResgisterTag
            eventResgisterTag = requisite
            requisiteStepStatus = executeEventHandlerRequisite(requisite)
        else:
            requisiteStepStatus = executeRegularRequisite(requisite)

        if logDisplay:
            if "FAILURE" in requisiteStepStatus:
                print "\n#--------- [%s-requisite Status] : FAILURE ----------#" %(node)
            else:
                print "\n#--------- [%s-requisite Status] : SUCCESS ----------#" %(node)

        # If any of the pre/post requisites fails, then
        # execution will be broken
        allprepostRequisiteStatus.extend(requisiteStepStatus)
        if "FAILURE" in allprepostRequisiteStatus:
            break;

    return allprepostRequisiteStatus


#-----------------------------------------------------------------------------------------------
# executeEventHandlerRequisite
#-----------------------------------------------------------------------------------------------
def executeEventHandlerRequisite(requisite):
    eventAPIs = []
    registerMethods = []
    unregisterMethods = []
    eventtestStepInfo = {}
    eventsRegisterJsonCmds   = []
    eventsUnRegisterJsonCmds = []
    for event in requisite.findall("event"):
        eventInfo = event.attrib.copy()
        eventAPIInfo = getTestPluginAPIInfo(eventInfo.get("pluginName"), eventInfo.get("eventName"), "event")
        registerMethod   = eventAPIInfo.get("serviceName") + "." + eventAPIInfo.get("serviceVersion") + "." + "register"
        unregisterMethod = eventAPIInfo.get("serviceName") + "." + eventAPIInfo.get("serviceVersion") + "." + "unregister"
        params =  { "event"   : eventAPIInfo.get("eventName") , "id" : eventAPIInfo.get("eventId") }

        jsonCmd = { "jsonrpc" : "2.0" , "id" : 2 , "method" : registerMethod , "params" : params}
        jsonCmd = json.dumps(jsonCmd)
        eventsRegisterJsonCmds.append(jsonCmd)

        jsonCmd = { "jsonrpc" : "2.0" , "id" : 2 , "method" : unregisterMethod , "params" : params}
        jsonCmd = json.dumps(jsonCmd)
        eventsUnRegisterJsonCmds.append(jsonCmd)

        eventAPIs.append(eventAPIInfo.get("eventName"))
        registerMethods.append(registerMethod)
        unregisterMethods.append(unregisterMethod)
    registerMethods   = list(set(registerMethods))
    unregisterMethods = list(set(unregisterMethods))

    # Update EventInfo Global variable
    global eventsInfo
    eventsInfo["eventAPIs"] = eventAPIs
    eventsInfo["registerMethods"]   = registerMethods
    eventsInfo["unregisterMethods"] = unregisterMethods
    eventsInfo["eventsRegisterJsonCmds"]   = eventsRegisterJsonCmds
    eventsInfo["eventsUnRegisterJsonCmds"] = eventsUnRegisterJsonCmds

    # Create Event listener Object
    global eventListener
    print "------------- Event-Handling -------------"
    if requisite.attrib.get("trace") == "true":
        traceEnable = True
    else:
        traceEnable = False
    eventListener = createEventListener(deviceIP,portNo,eventsInfo,traceEnable)
    count = 1
    maxTime = (len(eventsInfo.get("eventAPIs")) * 2) + 3
    # Wait until all events are registered
    while eventListener.getListenerFlag() == False and count <= maxTime:
        count += 1
        time.sleep(1)

    # Check listerner flag & registered info
    registerIssues = []
    if eventListener.getListenerFlag() == True:
        registerInfo = eventListener.getEventsRegisterInfo()
        for eventStatus in registerInfo:
            if eventStatus.get("status") == "FAILURE":
                registerIssues.append(eventStatus)
        if len(registerInfo) != 0 and len(registerIssues) == 0:
            registerStatus = "SUCCESS"
        else:
            registerStatus = "FAILURE"
    else:
        registerStatus = "FAILURE"

    # Display details of the event(s) failed to register
    if len(registerIssues) != 0:
        print "\n Failed to register below event(s)"
        for issue in registerIssues:
            print issue.get("response")

    # Display event register test step info
    eventtestStepInfo["name"] = requisite.attrib.get("requisiteName")
    eventtestStepInfo["testStepId"] = "1"
    eventtestStepInfo["pluginAPI"] = ",".join(registerMethods)
    eventtestStepInfo["paramTypeInfo"] = {"type":"directString"}
    eventtestStepInfo["resultGeneration"] = {"expectedValues":"null"}
    eventRegisterParams = ",".join(eventAPIs)
    result = {"Test_Step_Status":registerStatus}
    if logDisplay:
        dispTestStepInfo(eventtestStepInfo,eventRegisterParams,result)

    return [registerStatus]



#-----------------------------------------------------------------------------------------------
# executeRegularRequisite
#-----------------------------------------------------------------------------------------------
def executeRegularRequisite(requisite):
    requisiteStepStatus = []
    # Executing all the test steps under each pre/post requisite
    # and updating the status
    requisiteInfo = requisite.attrib.copy()
    for testStep in requisite.findall("testStep"):
        global currentTestStepId
        currentTestStepId = testStep.attrib.get("testStepId")
        setTestStepDelay(testStep.attrib)
        # If any of the test step fails, then execution
        # will be broken
        if testStep.attrib.get("testStepType") == "loop":
            global iterInterval
            iterInterval = 0
            if testStep.attrib.get("iterInterval") is not None:
                iterInterval = int(testStep.attrib.get("iterInterval"))
            loopTestStepStatus = executeTestStepLoop(requisiteInfo,testStep)
            if "FAILURE" in loopTestStepStatus:
                requisiteStepStatus.append("FAILURE")
                break;
            elif "FALSE" in loopTestStepStatus:
                continue;
            else:
                requisiteStepStatus.append("SUCCESS")
        else:
            status = executeTestStepDirect(requisiteInfo,testStep)
            if status == "FAILURE":
                requisiteStepStatus.append(status)
                break;
            elif status == "FALSE":
                continue;
            else:
                requisiteStepStatus.append(status)
    return requisiteStepStatus



#-----------------------------------------------------------------------------------------------
# executeTestStepDirect
#-----------------------------------------------------------------------------------------------
# Syntax      : executeTestStepDirect(testCaseInfo,testStep)
# Description : Method to execute direct test steps which does not involve loop/repeat
# Parameter   : testCaseInfo - Test Case details
#             : testStep     - Test Step node
# Return Value: Test Step status (SUCCESS/FAILURE)
#-----------------------------------------------------------------------------------------------

def executeTestStepDirect(testCaseInfo,testStep):

    # This method is to start the execution of the direct test
    # steps. Test step informations, test API and params are taken
    testStepInfo = getTestStepInfo(testStep).copy()
    testParams = testStepInfo.get("params")
    testMethod = getTestStepAPI(testStepInfo)
    testStepInfo["pluginAPI"] = testMethod

    # There are scenarios where we need to use the result of previous
    # test step results. In such case, we need to save the result of
    # test step whose result is used by other steps. Result is saved
    # when saveResult="true" option is added. Since this is a direct
    # test step there will not be any sub-test-steps & iteration, so
    # those values are set to 1
    saveResultInfo = {}
    saveResultInfo = {"subtestStepId":1,"iterationId":1}
    status,result = executeTest(testMethod,testParams,testStepInfo,saveResultInfo)

    # If the test step has revertGet="yes" or revertSet="yes" option
    # then it indicates that this test step is the one used for revert
    # Get/Set operation, so test step details & results will be saved
    if status == "SUCCESS":
        testStepResultList = []
        testStepResultInfo = {}
        testStepResultInfo = {"revertId":1,"result":result.copy()}
        testStepResultList.append(testStepResultInfo)
        saveRevertTestInfo(testCaseInfo,testStepInfo,testStepResultList)
        if revertTestInfo.get("revertFlags") is None and testStepInfo.get("revertFlag") == "yes":
            revertTestInfo["revertFlags"] = [{"revertId":1,"status":"TRUE"}]

    return status


#-----------------------------------------------------------------------------------------------
# executeTestStepLoop
#-----------------------------------------------------------------------------------------------
# Syntax      : executeTestStepLoop(testCaseInfo,testStep)
# Description : Method to execute test step which involves looping of several sub-test-steps
# Parameter   : testCaseInfo - Test Case details
#             : testStep     - Test Step node
# Return Value: List of Sub Test Step status (SUCCESS/FAILURE)
#-----------------------------------------------------------------------------------------------

def executeTestStepLoop(testCaseInfo,testStep):
    # This method is used to start the execution of the test
    # step whose type is loop. All the sub-test-steps are
    # executed one by one
    testStepId = testStep.attrib.get("testStepId")

    # Check whether the loop test step is conditional based
    # If yes, get the conditional status and proceed only
    # when there is no parse error and condition is met
    if testStep.find("conditionalExecution") is not None:
        conditionalExec = testStep.find("conditionalExecution").attrib.copy()
        if conditionalExec.get("enable") == "true":
            parserInfo = getPreviousResultParserInfo(testStep.find("conditionalExecution")).copy()
            status,result = getConditionalExecutionStatus(testStepResults,parserInfo)
            if status == "FAILURE":
                return [status]
            elif result == "FALSE":
                return [result]

    iterationCount = 0
    iterationInfo  = {}
    allRevertGetInfo  = []
    allRevertFlagInfo = []
    allsubTestStepInfo = []
    allIterTestStepStatus = []

    # Store the all sub test step details
    for subTestStep in testStep:
        subTestStepInfo = getTestStepInfo(subTestStep).copy()
        if subTestStepInfo.get("iterationInfo") is not None:
            iterationInfo.update(subTestStepInfo.get("iterationInfo").copy())
        allsubTestStepInfo.append(subTestStepInfo)

    # Based on the iteration parameter, execute the sub test
    # steps in loop
    if type(iterationInfo.get("value")) == list:
        iterationData = iterationInfo.get("value")
    else:
        iterationData = iterationInfo.get("value").split(",")

    for iterable in iterationData:
        revertSetFlag   = 0
        revertCheckFlag = 0
        iterationCount += 1
        global currentIterationId
        currentIterationId = iterationCount
        allsubTestStepStatus = []
        # Sets iteration Interval (i.e) delay between iteration
        if iterInterval != 0 and currentIterationId != 1:
            time.sleep(iterInterval)
        for subTestStepInfos in allsubTestStepInfo:

            # After getting the sub-test-step details, update the Id
            # with iteration count value. e.g 1.3
            subTestStepInfo = subTestStepInfos.copy()
            setTestStepDelay(subTestStepInfo)
            subTestStepInfo["testStepId"] = str(testStepId) + "." + str(iterationCount)
            testParams = subTestStepInfo.get("params")

            # Some parameters takes iterable as it value, update such
            #  params with iterable if any
            for param in subTestStepInfo.get("iterableParams"):
                testParams[param] = iterable

            # Some parameters takes value from previous test step & to
            # get that previous result we may need iterable. Here, iterable
            # passed to the previous result parser, test param gets updated
            # & parseStatus is captured
            for parserInfos in subTestStepInfo.get("dynamicParamInfo"):
                parserInfo = parserInfos.copy()
                parserInfo = updatePreviousResultParserInfo(parserInfo,iterable).copy()
                status,result = getPreviousTestStepResult(testStepResults,parserInfo)
                subTestStepInfo["parseStatus"] = status if status == "FAILURE" else ""
                testParams[parserInfo.get("tag")] = result.get(parserInfo.get("tag"))

            # Sometimes iterable value should be passed as expected values
            if subTestStepInfo.get("setdynamicExpectedValue") is not None:
                resultGenExpInfo = subTestStepInfo.get("resultGeneration").copy()
                allexpectedValues = resultGenExpInfo["expectedValues"]
                if allexpectedValues != "null":
                    allexpectedValues = allexpectedValues + "," + str(iterable)
                    resultGenExpInfo["expectedValues"] = allexpectedValues
                else:
                    resultGenExpInfo["expectedValues"] = str(iterable)
                subTestStepInfo["resultGeneration"] = resultGenExpInfo.copy()


            # There are scenarios, where expected values of the test step is
            # decided based on previous result. Here, iterable passed to the previous
            # result parser, expected value gets updated & parseStatus is captured
            if subTestStepInfo.get("dynamicExpectedValuesInfo") is not None:
                parserInfo = subTestStepInfo.get("dynamicExpectedValuesInfo").copy()
                parserInfo = updatePreviousResultParserInfo(parserInfo,iterable).copy()
                status,result = getPreviousTestStepResult(testStepResults,parserInfo)
                subTestStepInfo["parseStatus"] = status if status == "FAILURE" else ""
                resultGenExpInfo = subTestStepInfo.get("resultGeneration").copy()
                allexpectedValues = resultGenExpInfo["expectedValues"]
                result = [ str(data) for data in result.values() ]
                if allexpectedValues != "null":
                    allexpectedValues = allexpectedValues + "," + ",".join(result)
                    resultGenExpInfo["expectedValues"] = allexpectedValues
                else:
                    resultGenExpInfo["expectedValues"] = ",".join(result)
                subTestStepInfo["resultGeneration"] = resultGenExpInfo.copy()

            # There are scenarios, where test steps should get executed based
            # on some conditions, which may depend on previous result. Here,
            # iterable passed to the conditional execution status check function,
            # status gets updated & parseStatus is captured
            # E.g, Test Step A (check plugin status) & B(Activate Plugin)
            # B should be executed only when result of A is status:deactivated
            if subTestStepInfo.get("dynamicConditionalExecInfo") is not None:
                parserInfo = subTestStepInfo.get("dynamicConditionalExecInfo").copy()
                parserInfo = updatePreviousResultParserInfo(parserInfo,iterable).copy()
                status,result = getConditionalExecutionStatus(testStepResults,parserInfo)
                subTestStepInfo["parseStatus"] = status if status == "FAILURE" else ""
                subTestStepInfo["ConditionalExecStatus"] = result

            # Iterable value can also be passed as argument for the result
            # generation functions
            if subTestStepInfo.get("dynamicResultGenArg") == "true":
                resultGenArguments = subTestStepInfo.get("resultGeneration").get("arguments")
                if resultGenArguments != None:
                    resultGenArguments = resultGenArguments + "," + str(iterable)
                else:
                    resultGenArguments = str(iterable)
                resultGenArgInfo = subTestStepInfo.get("resultGeneration").copy()
                resultGenArgInfo["arguments"] = resultGenArguments
                subTestStepInfo["resultGeneration"] = resultGenArgInfo.copy()

            if subTestStepInfo.get("dynamicArgumentInfo") is not None:
                parserInfo = subTestStepInfo.get("dynamicArgumentInfo").copy()
                parserInfo = updatePreviousResultParserInfo(parserInfo,iterable).copy()
                status,result = getPreviousTestStepResult(testStepResults,parserInfo)
                subTestStepInfo["parseStatus"] = status if status == "FAILURE" else ""
                resultGenArgInfo = subTestStepInfo.get("resultGeneration").copy()
                allarguments = subTestStepInfo.get("resultGeneration").get("arguments")
                result = [ str(data) for data in result.values() ]
                if allarguments != None:
                    allarguments =  allarguments + "," + ",".join(result)
                    resultGenArgInfo["arguments"] = allarguments
                else:
                    resultGenArgInfo["arguments"] = ",".join(result)
                subTestStepInfo["resultGeneration"] = resultGenArgInfo.copy()


            # After updating the sub-test-step info with dynamic iterable
            # values, execution is started.
            testMethod = getTestStepAPI(subTestStepInfo)
            subTestStepInfo["pluginAPI"] = testMethod

            # Sub test step Id and iteration count are captured for saving
            # the sub-test-step result
            saveResultInfo = {}
            saveResultInfo = {"subtestStepId":subTestStepInfo.get("subtestStepId"),"iterationId":iterationCount}
            status,result = executeTest(testMethod,testParams,subTestStepInfo,saveResultInfo)

            # If the sub-test-step has revertGet="yes" or revertSet="yes" option
            # then it indicates that this sub-test-step is the one used for revert
            # Get/Set operation & details are saved if sub-test-step is success
            if status == "SUCCESS":
                allsubTestStepStatus.append(status)
                saveRevertTestInfo(testCaseInfo,subTestStepInfo,allRevertGetInfo)
                if subTestStepInfo.get("revertGet") == "yes":
                    revertGetInfo = {}
                    revertGetInfo["params"] = testParams.copy()
                    revertGetInfo["result"] = result.copy()
                    revertGetInfo["revertId"] = iterationCount
                    allRevertGetInfo.append(revertGetInfo)
                elif subTestStepInfo.get("revertSet") == "yes":
                    revertSetFlag   = 1
                if subTestStepInfo.get("revertFlag") == "yes":
                    revertCheckFlag = 1

            elif status == "FAILURE":
                allsubTestStepStatus.append(status)
                break;
            else:
                continue;

        # If any of the sub-test-step status is failed, current iteration
        # execution will be broken
        allIterTestStepStatus.extend(allsubTestStepStatus)
        if revertSetFlag == 1 and revertCheckFlag == 1:
            allRevertFlagInfo.append({"revertId":iterationCount,"status":"TRUE"})

    if revertTestInfo.get("revertGet") is not None and len(allRevertGetInfo):
        revertTestInfo.get("revertGet")["resultInfo"] = allRevertGetInfo
    elif revertTestInfo.get("revertFlags") is None and len(allRevertFlagInfo):
        revertTestInfo["revertFlags"] = allRevertFlagInfo

    return allIterTestStepStatus



#-----------------------------------------------------------------------------------------------
# executeTestStepRepeat
#-----------------------------------------------------------------------------------------------
# Syntax      : executeTestStepRepeat(testCaseInfo,testStep,repeatMax)
# Description : Method to repeat the test step for given N number of times
# Parameter   : testCaseInfo - Test Case details
#             : testStep     - Test Step node
#             : repeatMax    - N number of times to be repeated
# Return Value: List of Sub Test Step status (SUCCESS/FAILURE)
#-----------------------------------------------------------------------------------------------

def executeTestStepRepeat(testCaseInfo,testStep,repeatMax):

    # This method is used to repeat the test step for N number of
    # times (STRESS testing). Test step may or may not contain
    # sub-test-steps (only direct type)
    allRepeatTestStepStatus = []
    testStepId = testStep.attrib.get("testStepId")

    # Check whether the repeat test step is conditional based
    # If yes, get the conditional status and proceed only
    # when there is no parse error and condition is met
    if testStep.find("conditionalExecution") is not None:
        conditionalExec = testStep.find("conditionalExecution").attrib.copy()
        if conditionalExec.get("enable") == "true":
            parserInfo = getPreviousResultParserInfo(testStep.find("conditionalExecution")).copy()
            status,result = getConditionalExecutionStatus(testStepResults,parserInfo)
            if status == "FAILURE":
                return [status]
            elif result == "FALSE":
                return [result]

    # Execute all the sub-test-steps N times
    for repeatCounter in range(1,(int(repeatMax) + 1)):
        allsubTestStepStatus = []
        global currentIterationId
        currentIterationId = repeatCounter
        # Set Repeat Interval (i.e) delay between the repeats
        if repeatInterval != 0 and currentIterationId != 1:
            time.sleep(repeatInterval)
        for subTestStep in testStep:

            # After getting the sub-test-step details, update the Id
            # with repeater count value. e.g 1.2
            subTestStepInfo = getTestStepInfo(subTestStep).copy()
            subTestStepInfo["testStepId"] = str(testStepId) + "." + str(repeatCounter)
            setTestStepDelay(subTestStepInfo)

            testParams = subTestStepInfo.get("params")
            testMethod = getTestStepAPI(subTestStepInfo)
            subTestStepInfo["pluginAPI"] = testMethod

            # Sub test step Id and repeater count are captured for saving
            # the sub-test-step result
            saveResultInfo = {}
            saveResultInfo = {"subtestStepId":subTestStepInfo.get("subtestStepId"),"iterationId":repeatCounter}
            status,result = executeTest(testMethod,testParams,subTestStepInfo,saveResultInfo)

            # If the sub-test-step has revertGet="yes" or revertSet="yes" option
            # then it indicates that this sub-test-step is the one used for revert
            # Get/Set operation & details are saved,if sub-test-step is success
            if status == "SUCCESS":
                allsubTestStepStatus.append(status)
                subtestStepResultInfo = {}
                subtestStepResultInfo = {"revertId":1,"result":result.copy()}
                saveRevertTestInfo(testCaseInfo,subTestStepInfo,[subtestStepResultInfo])
                if revertTestInfo.get("revertFlags") is None and subTestStepInfo.get("revertFlag") == "yes":
                    revertTestInfo["revertFlags"] = [{"revertId":1,"status":"TRUE"}]
            elif status == "FAILURE":
                allsubTestStepStatus.append(status)
                break;
            else:
                continue;

        # If any of the sub-test-step status is failed in any of the repeatation
        # execution will be broken
        allRepeatTestStepStatus.extend(allsubTestStepStatus)
        if "FAILURE" in allRepeatTestStepStatus:
            break;

    return allRepeatTestStepStatus


#-----------------------------------------------------------------------------------------------
# executeTest
#-----------------------------------------------------------------------------------------------
# Syntax      : executeTest(testMethod,testParams,testStepInfo,saveResultInfo)
# Description : Method to initiate test execution
# Parameter   : testMethod     - Plugin API
#             : testParams     - API params
#             : testStepInfo   - test step details
#             : saveResultInfo - save result details (sub-test-step & iteration Id)
# Return Value: Execution status (SUCCESS/FAILURE) & result
#-----------------------------------------------------------------------------------------------

def executeTest(testMethod,testParams,testStepInfo,saveResultInfo):

    result = {}
    global eventListener

    # There are few parameters whose values should be added along
    # with the API e.g Controller.1.status@DeviceInfo , here param
    # callsign:DeviceInfo should be removed from params list.
    if testStepInfo.get("indexOnlyParam") is not None:
        del testParams[testStepInfo.get("indexOnlyParam")]

    parseStatus = testStepInfo.get("parseStatus")
    methodNotFound = testStepInfo.get("methodNotFound")
    conditionalExecStatus = testStepInfo.get("ConditionalExecStatus")

    # Forming the test step input param, it can be of any type, like
    # string / list / dict, obtained directly or using user configurations
    paramGenStatus,testParams = getTestStepInputParam(testStepInfo.get("paramTypeInfo"),testParams)
    parseStatus = paramGenStatus if paramGenStatus == "FAILURE" else parseStatus

    # Check whether test step is EventListener and check whether events
    # are registered
    if testStepInfo.get("action") == "eventListener" and eventListener is not None:
        eventRegistration = "SUCCESS"
    elif testStepInfo.get("action") == "eventListener" and eventListener is None:
        eventRegistration = "FAILURE"
    else:
        eventRegistration = "FALSE"

    # If the test step does not have any issues in forming the test API
    # and params & if the condition to execute satisfies, then test is initated
    if parseStatus != "FAILURE" and conditionalExecStatus != "FALSE" and methodNotFound is None and eventRegistration != "FAILURE":
        rebootStep      = testStepInfo.get("rebootStep")
        IPChangeStep    = testStepInfo.get("ipChangeStep")
        closeConnection = testStepInfo.get("closeConn")
        if (rebootStep == "yes" or IPChangeStep == "yes") and eventListener is not None and closeConnection != "false":
            if rebootStep == "yes":
                print "\nClosing websocket connection before reboot..."
            elif IPChangeStep == "yes":
                print "\nClosing websocket connection before IP Change..."
            eventListener.disconnect()
            time.sleep(5)
            eventListener = None

        if testStepInfo.get("action") == "eventListener":
            execStatus,response = getListenedEvent(testMethod,testStepInfo.get("clear"))
        elif testStepInfo.get("action") in ["eventRegister","eventUnRegister"]:
            testParams,execStatus,response = newEventHandler(testMethod,testStepInfo)
        elif testStepInfo.get("action") == "externalFnCall":
            execStatus,response = "SUCCESS",None
        else:
            execStatus,response = executeCommand(testMethod,testParams)

        # After the successful test execution, the response obtained
        # is parsed based on the user configurations and result is generated
        if execStatus == "SUCCESS":
            if testStepInfo.get("action") == "eventListener":
                result = testStepResultGeneration(response,testStepInfo.get("resultGeneration"),"eventListener")
            elif testStepInfo.get("action") in ["eventRegister","eventUnRegister"]:
                result  = testStepResultGeneration(response,testStepInfo.get("resultGeneration"),testStepInfo.get("action"))
            elif testStepInfo.get("action") == "externalFnCall":
                result = testStepResultGeneration(response,testStepInfo.get("resultGeneration"),"externalFnCall")
            else:
                result = testStepResultGeneration(response,testStepInfo.get("resultGeneration"))
            testStepStatus = result.get("Test_Step_Status")
            if logDisplay:
                dispTestStepInfo(testStepInfo,testParams,result)

            # Test step results are saved for other test steps to use
            # If Id is something like 1.2, then the suffix ( iteration/repeatation)
            # count value are removed
            if testStepInfo.get("saveResult") == "true":
                testStepId = str(testStepInfo.get("testStepId"))
                testStepId = testStepId.split(".")[0] if "." in testStepId else testStepId
                saveResult = saveResultInfo.copy()
                saveResult["result"] = result.copy()
                saveTestStepResult(testStepId,saveResult.copy())

            # Invoking reboot handler to restore the device status
            if testStepInfo.get("rebootStep") == "yes":
               setUpAfterReboot = handleDeviceReboot()
               if setUpAfterReboot == "FAILURE":
                   testStepStatus = "FAILURE"
            elif testStepInfo.get("ipChangeStep") == "yes":
               newIPUpdateStatus = handleDeviceIPChange()
               if newIPUpdateStatus == "FAILURE":
                   testStepStatus = "FAILURE"
            elif testStepInfo.get("PluginOnStep") == "yes":
                setUpPluginOn = handlePluginOn()
                if setUpPluginOn == "FAILURE":
                    testStepStatus = "FAILURE"

            return testStepStatus,result
        else:
            return execStatus,result

    elif parseStatus == "FAILURE":
        return parseStatus,result
    elif conditionalExecStatus == "FALSE":
        return conditionalExecStatus,result
    elif methodNotFound is not None:
        print "\nError Occurred: %s method not found in %s Plugin" %(methodNotFound.get("method"),methodNotFound.get("plugin"))
        return "FAILURE",result
    elif eventRegistration == "FAILURE":
        print "\nError Occurred: No Events are Registered but Listeners are used"
        return "FAILURE",result
    else:
        print "\nError Occurred: Undefined behaviour"
        return "FAILURE",result

#-----------------------------------------------------------------------------------------------
# executeCommand
#-----------------------------------------------------------------------------------------------
# Syntax      : executeCommand(testMethod,testParams)
# Description : Method to send JSON command and receive the response
# Parameter   : testMethod  - Plugin API
#             : testParams  - API params
# Return Value: Execution status (SUCCESS/FAILURE) & response
#-----------------------------------------------------------------------------------------------

def executeCommand(testMethod,testParams):

    # JSON request formation
    jsonCmd = { "jsonrpc" : "2.0" , "id" : 2 , "method" : testMethod}

    if testParams != {} and testParams != [] and testParams != "":
        jsonCmd["params"] = testParams

    jsonCmd = json.dumps(jsonCmd)
    requestURL = "http://" + deviceIP + ":" + portNo + "/jsonrpc"

    #print "Cmd : ",jsonCmd
    global testStepJSONCmd
    testStepJSONCmd = jsonCmd
    executeStatus = "SUCCESS"
    jsonResponse = {}
    try:
        global customTimeout
        if customTimeout != None:
            responseTimeout = customTimeout
            customTimeout = None
        else:
            responseTimeout = 30
        if execMethod.upper() == "CURL":
            req_post = requests.post(requestURL,data=jsonCmd,timeout=responseTimeout)
            jsonResponse = json.loads(req_post.content,strict=False)
            if IsPerformanceSelected == "true":
                responseTime = req_post.elapsed.total_seconds()
        else:
            executeStatus = "FAILURE"
            print "\nError Occurred: Unknown method type for sending JSON Request"

        #Getting the response time for performance metrics
        if IsPerformanceSelected == "true" and execMethod.upper() in ["CURL","TTS"]:
            print "\n\nResponse Time of %s : %s" %(testMethod,responseTime)
            responseCheckStatus = "OK"
            if (float(responseTime) <= 0 or float(responseTime) > float(maxResponseTime)):
                print "Device took more than usual to respond"
                responseCheckStatus = "HIGH"
            apiResponseInfo = {"API":testMethod,"RESPONSE_TIME":responseTime,"STATUS":responseCheckStatus}
            apiPerformanceInfo.append(apiResponseInfo)

    except Exception as e:
        executeStatus = "FAILURE"
        print "\nException Occurred : %s" %(e)
        print "\nJSON Command Sent : %s" %(jsonCmd)

    #print "Output: " , jsonResponse

    return executeStatus,jsonResponse



#-----------------------------------------------------------------------------------------------
# getListenedEvent
#-----------------------------------------------------------------------------------------------
# Syntax      : getListenedEvent(eventAPI,clearStatus)
# Description : Method to find the expected events from the listened events
# Parameter   : eventAPI  - Event API used for selecting the events from buffer
#             : clearStatus - True/False whether to clear the events buffer or not
# Return Value: Execution status (SUCCESS/FAILURE) & selected events
#-----------------------------------------------------------------------------------------------
def getListenedEvent(eventAPI,clearStatus):
    status = "SUCCESS"
    listenedEvents = []

    time.sleep(2)
    eventsBuffer = eventListener.getEventsBuffer()
    global eventsBufferBackup
    if eventsBufferBackup != []:
        eventsBuffer.extend(eventsBufferBackup)
        eventsBufferBackup = []
    for eventResponse in eventsBuffer:
        if eventAPI in eventResponse:
            try:
                eventJsonResponse = json.loads(eventResponse)
            except Exception as e:
                status = "FAILURE"
                print "\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e)
            listenedEvents.append(eventJsonResponse)

    if clearStatus is None or clearStatus == "true":
        eventListener.clearEventsBuffer()
    return status,listenedEvents

#-----------------------------------------------------------------------------------------------
# getEventsUnRegistrationInfo
#-----------------------------------------------------------------------------------------------
def getEventsUnRegistrationInfo():
    count = 1
    maxTime = (len(eventsInfo.get("eventAPIs")) * 2) + 3
    # Wait until all events are unregistered
    while eventListener.getListenerFlag() == True and count <= maxTime:
        count += 1
        time.sleep(1)

    # Check unregistered info
    unregisterIssues = []
    unregisterInfo = eventListener.getEventsUnRegisterInfo()
    for eventStatus in unregisterInfo:
        if eventStatus.get("status") == "FAILURE":
            unregisterIssues.append(eventStatus)
    if len(unregisterInfo) != 0 and len(unregisterIssues) == 0:
        unregisterStatus = "SUCCESS"
    else:
        unregisterStatus = "FAILURE"

    # Display details of the event(s) failed to unregister
    if len(unregisterIssues) != 0:
        print "\n Failed to unregister below event(s)"
        for issue in unregisterIssues:
            print issue.get("response")

    # Display event register test step info
    eventtestStepInfo = {}
    eventtestStepInfo["name"] = "UnRegister_Events"
    eventtestStepInfo["testStepId"] = "1"
    eventtestStepInfo["pluginAPI"] = ",".join(eventsInfo.get("unregisterMethods"))
    eventtestStepInfo["paramTypeInfo"] = {"type":"directString"}
    eventtestStepInfo["resultGeneration"] = {"expectedValues":"null"}
    eventUnRegisterParams = ",".join(eventsInfo.get("eventAPIs"))
    result = {"Test_Step_Status":unregisterStatus}
    dispTestStepInfo(eventtestStepInfo,eventUnRegisterParams,result)

    return [unregisterStatus]


def newEventHandler(eventMethod,testStepInfo):
    if testStepInfo.get("params") != {}:
        eventID = ".".join(testStepInfo.get("params").values()) + "." + testStepInfo.get("eventId")
    else:
        eventID = testStepInfo.get("eventId")
    eventParams =  { "event" : testStepInfo.get("eventName") , "id" : eventID }

    jsonCmd = { "jsonrpc" : "2.0" , "id" : 2 , "method" : eventMethod , "params" : eventParams}
    jsonCmd = json.dumps(jsonCmd)
    if eventListener is not None:
        if testStepInfo.get("action") == "eventRegister":
            eventListener.setNewEventDetails(jsonCmd,"register")
        else:
            eventListener.setNewEventDetails(jsonCmd,"unregister")
        time.sleep(5)
        execStatus = "SUCCESS"
        response = eventListener.getNewEventResponse()
    else:
        execStatus = "FAILURE"
        print "\n [ERROR]: Event Handler thread not started"

    #execStatus,response = executeCommand(eventMethod,eventParams)
    return eventParams,execStatus,response




def handleDeviceReboot():
    #Reboot handling restore websocket & plugin status
    timeout = time.time() + 60*5   # 5 minutes from now
    print "\nWaiting for the device to come up..."
    time.sleep(30)
    deviceStatus = "DOWN"
    while True:
        status = getTestDeviceStatus()
        if status == "FREE":
            deviceStatus = "UP"
            break;
        elif time.time() > timeout:
            deviceStatus = "DOWN"
            print "Device is not coming up event after 5 mins"
            break;
        time.sleep(5)

    if deviceStatus == "UP":
        print "Device is UP. Setting back pre-requisites if any..."
        setUpStatus = setUpPreRequisitesBack()
        return setUpStatus
    else:
        return "FAILURE"


def getTestDeviceStatus():
    try:
        data = '{"jsonrpc":"2.0","id":"2","method": "Controller.1.status@Controller"}'
        headers = {'content-type': 'text/plain;'}
        url = 'http://' + deviceIP + ':' + portNo + '/jsonrpc'
        response = requests.post(url, headers=headers, data=data, timeout=3)
        if response.status_code == 200:
            return "FREE"
        else:
            return "NOT_FOUND"
    except Exception as e:
        return "NOT_FOUND"


def handlePluginOn():
    print "\nTurning ON Plugin. Setting back pre-requisites if any..."
    setUpStatus = setUpPreRequisitesBack()
    return setUpStatus

def handleDeviceIPChange():
    #IP change handling, get the latest IP from TM and update here
    print "\nWaiting for the device IP change..."
    time.sleep(90)
    url = tmURL + '/deviceGroup/getDeviceDetails?deviceName=' + deviceName
    newIP = ""
    try:
        response = urllib2.urlopen(url,timeout=5)
        deviceDetails = json.load(response)
        newIP = str(deviceDetails.get("deviceip"))
        global deviceIP
        deviceIP = newIP
        print "NewIP is %s. Updated new device IP" %(newIP)
        time.sleep(5)
        if eventResgisterTag != None:
            global logDisplay
            logDisplay = False
            global eventListener
            if eventListener != None:
                global eventsBufferBackup
                eventsBufferBackup = eventListener.getEventsBuffer();
                print "Storing events buffer",eventsBufferBackup
                eventListener = None
            requisiteStepStatus = executeEventHandlerRequisite(eventResgisterTag)
            logDisplay = True
            if "FAILURE" in requisiteStepStatus:
                print "Event listener thread not started with new IP"
                return "FAILURE"
            else:
                print "Event listener thread started with new IP properly"
                return "SUCCESS"
        else:
            return "SUCCESS"
    except:
        print "Unable to get Device Details from REST !!!"
        sys.stdout.flush()
        return "FAILURE"



def setUpPreRequisitesBack():
    if testPlugin.find("pluginPreRequisite") is not None:
        global testStepResults
        global bktestStepResults
        bktestStepResults = testStepResults
        global logDisplay
        logDisplay = False
        global eventListener
        if eventListener != None:
            global eventsBufferBackup
            eventsBufferBackup = eventListener.getEventsBuffer();
            print "Storing events buffer",eventsBufferBackup
            eventListener = None
        time.sleep(1)
        setPreRequisiteStatus = executePrePostRequisite(testPlugin.find("pluginPreRequisite"),"Pre")
        logDisplay = True
        testStepResults = bktestStepResults
        if "FAILURE" in setPreRequisiteStatus:
            print "Plugin pre-requisites are not set back properly"
            return "FAILURE"
        else:
            print "Plugin pre-requisites are set back properly"
            return "SUCCESS"
    else:
        return "SUCCESS"



#-----------------------------------------------------------------------------------------------
# getTestPluginInfo
#-----------------------------------------------------------------------------------------------
# Syntax      : getTestPluginInfo(testPlugin)
# Description : Method to get the plugin details such as plugin name & version
# Parameter   : testPlugin - testPlugin node
# Return Value: Plugin info dictionary
#-----------------------------------------------------------------------------------------------
def getTestPluginInfo(testPlugin):
    testPluginInfo = testPlugin.attrib
    return testPluginInfo


#-----------------------------------------------------------------------------------------------
# getTestPluginAPIInfo
#-----------------------------------------------------------------------------------------------
# Syntax      : getTestPluginAPIInfo(pluginName, testMethod, type)
# Description : Method to get the plugin API details from the template XML
# Parameter   : pluginName - Name of the test plugin
#             : testMethod - test API name
#             : apiType       - Type of the API (method/event)
# Return Value: Plugin API info dictionary
#-----------------------------------------------------------------------------------------------
def getTestPluginAPIInfo(pluginName, testMethod, apiType="method"):

    pluginAPIInfo = {}
    for plugin in thunderPlugins:
        if pluginName in plugin.attrib.get("pluginName"):
            for method in plugin.findall(apiType):
                if testMethod in method.attrib.get("name") and len(testMethod) == len(method.attrib.get("name")):
                    pluginAPIInfo = method.attrib.copy()
                    pluginAPIInfo["serviceName"] = plugin.attrib.get("serviceName")
                    pluginAPIInfo["serviceVersion"] = plugin.attrib.get("serviceVersion")

                    apiParams = {}
                    apiParamsType = {}
                    if method.find("params") is not None:
                        pluginAPIInfo["paramTypeInfo"] = method.find("params").attrib.copy()
                        for param in method.find("params"):
                            apiParams[param.attrib.get("tag")] = param.attrib.get("defaultValue")
                            apiParamsType[param.attrib.get("tag")] = param.attrib.get("type")
                    pluginAPIInfo["params"] = apiParams
                    pluginAPIInfo["paramsType"] = apiParamsType

                    if method.find("expectedValues") is not None and method.find("expectedValues").text is not None:
                        pluginAPIInfo["expectedValues"] = method.find("expectedValues").text
                    else:
                        pluginAPIInfo["expectedValues"] = "null"
                    break;

    return pluginAPIInfo

#-----------------------------------------------------------------------------------------------
# getTestCaseInfo
#-----------------------------------------------------------------------------------------------
# Syntax      : getTestCaseInfo(testCase)
# Description : Method to get the test case details
# Parameter   : testCase - testCase node
# Return Value: Test Case info dictionary
#-----------------------------------------------------------------------------------------------
def getTestCaseInfo(testCase):
    testCaseInfo = testCase.attrib
    if testCase.find('testCaseInfo') is not None:
        testCaseInfo.update(testCase.find('testCaseInfo').attrib)
    else:
        testCaseInfo["testCaseType"] = "direct"
    return testCaseInfo

#-----------------------------------------------------------------------------------------------
# setTestStepDelay
#-----------------------------------------------------------------------------------------------
# Syntax      : setTestStepDelay(testStepInfo)
# Description : Method to set delay between test steps
# Parameter   : testStepInfo - test step info
# Return Value: Nil
#-----------------------------------------------------------------------------------------------
def setTestStepDelay(testStepInfo):
    if testStepInfo.get("delay") is not None:
        delay = int(testStepInfo.get("delay"))
        time.sleep(delay)

#-----------------------------------------------------------------------------------------------
# getTestStepAPI
#-----------------------------------------------------------------------------------------------
# Syntax      : getTestStepAPI(testStepInfo)
# Description : Method to form the test API
# Parameter   : testStepInfo - test step details
# Return Value: Test API
#-----------------------------------------------------------------------------------------------
def getTestStepAPI(testStepInfo):
    if testStepInfo.get("action") == "eventListener":
        testMethod = str(testStepInfo.get("eventId")) + "." + str(testStepInfo.get("eventName"))
        return testMethod
    if testStepInfo.get("action") == "eventRegister":
        testMethod = str(testStepInfo.get("serviceName"))    + "." + \
                     str(testStepInfo.get("serviceVersion")) + "." + "register"
        return testMethod
    if testStepInfo.get("action") == "eventUnRegister":
        testMethod = str(testStepInfo.get("serviceName"))    + "." + \
                     str(testStepInfo.get("serviceVersion")) + "." + "unregister"
        return testMethod

    if testStepInfo.get("action") == "externalFnCall":
        testMethod = None
        return testMethod

    testMethod = str(testStepInfo.get("serviceName"))    + "." + \
                 str(testStepInfo.get("serviceVersion")) + "." + \
                 str(testStepInfo.get("api"))

    if testStepInfo.get("indexOnlyParam") is not None:
        indexParam = testStepInfo.get("indexOnlyParam")
        testMethod = testMethod + "@" + str(testStepInfo.get("params").get(indexParam))
    elif testStepInfo.get("indexParam") is not None:
        indexParam = testStepInfo.get("indexParam")
        testMethod = testMethod + "@" + str(testStepInfo.get("params").get(indexParam))

    return testMethod


#-----------------------------------------------------------------------------------------------
# getTestStepInfo
#-----------------------------------------------------------------------------------------------
# Syntax      : getTestStepInfo(testStep)
# Description : Method to get all the details of the test step
# Parameter   : testStep - testStep node
# Return Value: Test Step info dictionary
#-----------------------------------------------------------------------------------------------
def getTestStepInfo(testStep):
    testParams = {}
    revertParams = []
    paramTypeInfo = {}
    iterableParams = []
    dynamicParamInfo = []

    testStepInfo = testStep.attrib.copy()
    if testStepInfo.get("testStepId") is not None and testStepInfo.get("testStepType") is None:
        testStepInfo["testStepType"] = "direct"
    if testStepInfo.get("action") in ["eventListener","eventRegister","eventUnRegister"]:
        apiType = "event"
    elif testStepInfo.get("action") == "externalFnCall":
        apiType = None
    else:
        apiType = "method"

    # Check whether step step has plugin name and plugin version details
    # If not, use the default plugin info provide in testPlugin node
    # Based on the plugin details, get the test API details from template XML
    if apiType != None:
        if "pluginName" in testStepInfo.keys():
            pluginAPIInfo = getTestPluginAPIInfo(testStepInfo.get("pluginName"),testStepInfo.get(apiType), apiType).copy()
        else:
            pluginAPIInfo = getTestPluginAPIInfo(testPlugin.attrib.get("pluginName"),testStepInfo.get(apiType), apiType).copy()
            testStepInfo["pluginName"] = testPlugin.attrib.get("pluginName")
    else:
        pluginAPIInfo = {}

    # Getting the Service Name and Version
    # If API has specific version, then it is taken as Service Version
    # or else the common version for the plugin is used for the testing
    testStepInfo["serviceName"]   = pluginAPIInfo.get("serviceName")
    if pluginAPIInfo.get("version") is not None:
        testStepInfo["serviceVersion"] = pluginAPIInfo.get("version")
    else:
        testStepInfo["serviceVersion"] = pluginAPIInfo.get("serviceVersion")

    # Populating essential parameters for methods/Events
    if testStepInfo.get("action") in ["eventListener","eventRegister","eventUnRegister"]:
        testStepInfo["eventId"] = pluginAPIInfo.get("eventId")
        testStepInfo["eventName"] = pluginAPIInfo.get("eventName")
    else:
        testStepInfo["api"] = pluginAPIInfo.get("api")


    # If not able to get the test API info, capture the details under
    # methodNotFound tag
    if testStepInfo.get("api") is None and testStepInfo.get("eventName") is None and testStepInfo.get("action") != "externalFnCall":
        methodInfo = {}
        methodInfo = {"method":testStepInfo.get(apiType),"plugin":testStepInfo.get("pluginName")}
        testStepInfo["methodNotFound"] = methodInfo.copy()

    # Get the details of custom response timeout configurations made
    # for this particular test case if any
    if testStepInfo.get("timeoutKey") != None:
        status,keyData = readDeviceConfigKeys(testStepInfo.get("timeoutKey"))
        if status == "SUCCESS" and  keyData != "":
            global customTimeout
            customTimeout = int(keyData)
        else:
            print "Unable to get the custom timeout: %s, proceeding with default value" %(testStepInfo.get("timeoutKey"))

    # Get the details of all the test params one by one
    if testStep.find("params") is not None:
        for param in testStep.find("params"):

            # Check whether the param is indexOnly/index type
            # If yes, capture the param tag
            if param.attrib.get("indexOnly") == "true":
                testStepInfo["indexOnlyParam"] = param.attrib.get("tag")
            elif param.attrib.get("index") == "true":
                testStepInfo["indexParam"] = param.attrib.get("tag")

            # Populate the param value using any of the below methods
            # a. Use default value from template XML if useDefault="true"
            # b. Get value from previous test step results if usePreviousResult="true"
            # c. Get value from device config file if useConfigFile="true"
            # d. Use the provided value
            if param.attrib.get("useDefault") == "true":
                testParams[param.attrib.get("tag")] = pluginAPIInfo.get("params").get(param.attrib.get("tag"))
            elif param.attrib.get("usePreviousResult") == "true":
                parserInfo = getPreviousResultParserInfo(param).copy()
                if param.attrib.get("useIterableArg") != "true" and param.attrib.get("subId") is None:
                    status,result = getPreviousTestStepResult(testStepResults,parserInfo)
                    testStepInfo["parseStatus"] = status if status == "FAILURE" else ""
                    testParams[param.attrib.get("tag")] = result.get(param.attrib.get("tag"))
                else:
                    parserInfo["tag"] = param.attrib.get("tag")
                    parserInfo["useIterableArg"] = param.attrib.get("useIterableArg")
                    dynamicParamInfo.append(parserInfo)
                    testParams[param.attrib.get("tag")] = None
            elif param.attrib.get("useConfigFile") == "true":
                status,result = readDeviceConfigKeys(param.attrib.get("key"))
                testStepInfo["parseStatus"] = status if status == "FAILURE" else ""
                testParams[param.attrib.get("tag")] = result
            else:
                testParams[param.attrib.get("tag")] = param.attrib.get("value")

            # During revert operation, the params & its values obtained using
            # Get method are substituted for the params of Set method. So capture
            # the param tag if revertParam="yes"
            if testStepInfo.get("revertSet") == "yes" and param.attrib.get("revertParam") == "yes":
                revertParams.append(param.attrib.get("tag"))

            # If iteration="true", it indicates that the test steps are iterated
            # based on this param values. So capture the param tag & values
            if param.attrib.get("iteration") == "true":
                iterationInfo = {}
                iterationInfo = {"tag":param.attrib.get("tag"),"value":testParams.get(param.attrib.get("tag"))}
                testStepInfo["iterationInfo"] = iterationInfo.copy()
                iterableParams.append(param.attrib.get("tag"))

            # If useIterable="true", it indicates that the param takes one of
            # the iteration values as its value. So add the param to iterableParams
            elif param.attrib.get("useIterable") == "true":
                iterableParams.append(param.attrib.get("tag"))

            # Check how the param needs to passed and whether it is generated by
            # framework or the user. Below are the types of params
            # a. directString
            # b. directList
            # c. directDict
            if pluginAPIInfo.get("paramTypeInfo") is not None and pluginAPIInfo.get("paramTypeInfo") != {}:
                if pluginAPIInfo.get("paramTypeInfo").get("paramType") == "directString":
                    paramTypeInfo["type"] = "directString"
                elif pluginAPIInfo.get("paramTypeInfo").get("paramType") == "directList":
                    paramTypeInfo["type"] = "directList"
                elif pluginAPIInfo.get("paramTypeInfo").get("paramType") == "directBool":
                    paramTypeInfo["type"] = "directBool"
                elif pluginAPIInfo.get("paramTypeInfo").get("paramType") == "userGenerate":
                    paramTypeInfo["type"] = "userGenerate"
                    paramTypeInfo["tag"]  = pluginAPIInfo.get("paramTypeInfo").get("useMethodTag")
                else:
                    paramTypeInfo["type"] = "directDict"

                if pluginAPIInfo.get("paramTypeInfo").get("paramKey") is not None:
                    paramTypeInfo["paramKey"] = pluginAPIInfo.get("paramTypeInfo").get("paramKey")
            else:
                paramTypeInfo["type"] = "directDict"


            if pluginAPIInfo.get("paramsType") is not None:
                paramTypeInfo["individualparamsType"] = pluginAPIInfo.get("paramsType").copy()
            else:
                paramTypeInfo["individualparamsType"] = {}


    testStepInfo["params"] = testParams.copy()
    testStepInfo["paramTypeInfo"] = paramTypeInfo.copy()
    testStepInfo["revertParams"] = revertParams
    testStepInfo["iterableParams"] = iterableParams
    testStepInfo["dynamicParamInfo"]  = dynamicParamInfo

    # Check whether the test step has user configured result generation steps
    if testStep.find("resultGeneration") is not None:
        testStepInfo["resultGeneration"] = testStep.find("resultGeneration").attrib.copy()

        # Arguments can be updated in any/all of the below ways
        # a. Get the from device config file if useConfigFile="true"
        # b. Use the provided expected value
        # c. Get iterable as expectedValue
        # d. Use previous result as argument
        if "arguments" not in testStepInfo.get("resultGeneration").keys():
            arguments = testStep.find("resultGeneration").find("arguments")
            if arguments is not None:
                allarguments = ""
                argumentInfo = arguments.attrib.copy()
                if argumentInfo.get("value") is not None and argumentInfo.get("value") != "":
                    allarguments = argumentInfo.get("value")

                if argumentInfo.get("useConfigFile") == "true":
                    status,result = readDeviceConfigKeys(argumentInfo.get("key"))
                    testStepInfo["parseStatus"] = status if status == "FAILURE" else ""
                    if allarguments != "":
                        allarguments = allarguments + "," + str(result)
                    else:
                        allarguments = result

                if argumentInfo.get("usePreviousResult") == "true":
                    parserInfo = getPreviousResultParserInfo(arguments).copy()
                    # If getting previous test result does not involve any dynamic
                    # values like iterable or result of sub-test-step (understood
                    # its executed already) then invoke the parser function and
                    # update the arguments
                    if argumentInfo.get("useIterableArg") != "true" and argumentInfo.get("subId") is None:
                        status,result = getPreviousTestStepResult(testStepResults,parserInfo)
                        testStepInfo["parseStatus"] = status if status == "FAILURE" else ""
                        result = [ str(data) for data in result.values() ]
                        if allarguments != "":
                            allarguments = allarguments + "," + ",".join(result)
                        elif result is not None:
                            allarguments = ",".join(result)
                    # If not, expected value will be obtained dynamically during the
                    # iteration or repeatation
                    else:
                        testStepInfo["dynamicArgumentInfo"] = parserInfo.copy()
                        testStepInfo.get("dynamicArgumentInfo")["useIterableArg"] = argumentInfo.get("useIterableArg")

                # Check whether iterable value should be passed as argument for result
                # generation for a loop test step type
                if argumentInfo.get("useIterableArg") == "true":
                    testStepInfo["dynamicResultGenArg"] = "true"

                if allarguments != "":
                    testStepInfo.get("resultGeneration")["arguments"] = allarguments

        # Expected values can be updated in any/all of the below ways
        # a. Use the default expected values from the template XML
        # b. Get the expected value from the previous test result
        # c. Get the from device config file if useConfigFile="true"
        # d. Use the provided expected value
        # e. Get iterable as expectedValue
        if "expectedValues" not in testStepInfo.get("resultGeneration").keys():
            expectedValues = testStep.find("resultGeneration").find("expectedValues")
            if expectedValues is not None:
                allexpectedValues = ""
                expectedValInfo = expectedValues.attrib.copy()
                if expectedValInfo.get("value") is not None and expectedValInfo.get("value") != "":
                    allexpectedValues = expectedValInfo.get("value")
                elif expectedValInfo.get("useDefault") == "true":
                    allexpectedValues = pluginAPIInfo.get("expectedValues")

                if expectedValInfo.get("useConfigFile") == "true":
                    status,result = readDeviceConfigKeys(expectedValInfo.get("key"))
                    testStepInfo["parseStatus"] = status if status == "FAILURE" else ""
                    if allexpectedValues != "":
                        allexpectedValues = str(allexpectedValues) + "," + str(result)
                    else:
                        allexpectedValues = result

                if expectedValInfo.get("usePreviousResult") == "true":
                    parserInfo = getPreviousResultParserInfo(expectedValues).copy()
                    # If getting previous test result does not involve any dynamic
                    # values like iterable or result of sub-test-step (understood
                    # its executed already) then invoke the parser function and
                    # update the expected value
                    if expectedValInfo.get("useIterableArg") != "true" and expectedValInfo.get("subId") is None:
                        status,result = getPreviousTestStepResult(testStepResults,parserInfo)
                        testStepInfo["parseStatus"] = status if status == "FAILURE" else ""
                        result = [ str(data) for data in result.values() ]
                        if allexpectedValues != "":
                            allexpectedValues = allexpectedValues + "," + ",".join(result)
                        elif result is not None:
                            allexpectedValues = ",".join(result)
                    # If not, expected value will be obtained dynamically during the
                    # iteration or repeatation
                    else:
                        testStepInfo["dynamicExpectedValuesInfo"] = parserInfo.copy()
                        testStepInfo.get("dynamicExpectedValuesInfo")["useIterableArg"] = expectedValInfo.get("useIterableArg")

                if expectedValInfo.get("useIterableValue") == "true":
                    testStepInfo["setdynamicExpectedValue"] = "true"

                if allexpectedValues != "":
                    testStepInfo.get("resultGeneration")["expectedValues"] = allexpectedValues
                else:
                    testStepInfo.get("resultGeneration")["expectedValues"] = "null"
            else:
                testStepInfo.get("resultGeneration")["expectedValues"] = pluginAPIInfo.get("expectedValues")
        elif not str(testStepInfo.get("resultGeneration").get("expectedValues")) != "":
            testStepInfo.get("resultGeneration")["expectedValues"] = "null"
    else:
        testStepInfo["resultGeneration"] = {"expectedValues":pluginAPIInfo.get("expectedValues")}

    # Check whether the test step has to be executed only when it satisfy
    # condition.
    if testStep.find("conditionalExecution") is not None:
        conditionalExec = testStep.find("conditionalExecution").attrib.copy()
        if conditionalExec.get("enable") == "true":
            parserInfo = getPreviousResultParserInfo(testStep.find("conditionalExecution")).copy()
            # If getting previous test result does not involve any dynamic
            # values like iterable or result of sub-test-step (understood that
            # its not executed already) then invoke parser function to get the
            # conditional execution status
            if conditionalExec.get("useIterableArg") != "true" and conditionalExec.get("subId") is None:
                status,result = getConditionalExecutionStatus(testStepResults,parserInfo)
                testStepInfo["parseStatus"] = status if status == "FAILURE" else ""
                testStepInfo["ConditionalExecStatus"] = result
            #  If not, conditional execution status will be obtained dynamically
            # during the iteration or repeatation
            else:
                testStepInfo["dynamicConditionalExecInfo"] = parserInfo.copy()
                testStepInfo.get("dynamicConditionalExecInfo")["useIterableArg"] = conditionalExec.get("useIterableArg")
                testStepInfo["ConditionalExecStatus"] = "null"

    return testStepInfo

#-----------------------------------------------------------------------------------------------
# getTestStepInputParam
#-----------------------------------------------------------------------------------------------
# Syntax      : getTestStepInputParam(paramTypeInfo,testParams)
# Description : Method to form the test step input param or use the user configurations
#             : and generate the param
# Parameter   : paramTypeInfo - type of the param
#             : testParams    - test input params
# Return Value: Function execution status & Test params
#-----------------------------------------------------------------------------------------------

def getTestStepInputParam(paramTypeInfo,testParams):
    paramGenStatus = "SUCCESS"

    updatedParams = testParams.copy()
    individualParamsType = paramTypeInfo.get("individualparamsType")
    if individualParamsType is not None and individualParamsType != {}:
        for param in individualParamsType.keys():
            if param in updatedParams.keys():
                if updatedParams.get(param) is not None:
                    if individualParamsType.get(param) == "int":
                        updatedParams[param] = int(updatedParams.get(param))
                    elif individualParamsType.get(param) == "float":
                        updatedParams[param] = float(updatedParams.get(param))
                    elif individualParamsType.get(param) == "bool":
                        if str(updatedParams.get(param)).lower() == "true":
                            updatedParams[param] = True
                        else:
                            updatedParams[param] = False
                    elif individualParamsType.get(param) == "list":
                        if str(updatedParams.get(param)).strip() != "":
                            updatedParams[param] = updatedParams.get(param).split(",")
                        else:
                            updatedParams[param] = []
                else:
                    updatedParams[param] = updatedParams.get(param)


        testParams = updatedParams.copy()

    paramType = paramTypeInfo.get("type")
    paramValues = testParams.values()

    # Parameter can be formed in below ways:
    # a. params:"1080i"                   // directString method
    # b. params:['A','B']                 // directList method
    # c. params:{"callsign","DeviceInfo"} // directDict method
    if paramType == "directString":
        inputParams = str(paramValues[0]) if len(paramValues) != 0 else ""
    elif paramType == "directList":
        inputParams = str(paramValues[0]).split(",") if len(paramValues) != 0 else []
    elif paramType == "directBool":
        if str(paramValues[0]).lower() == "true":
            inputParams = True
        else:
            inputParams = False
    elif paramType == "userGenerate":
        tag = paramTypeInfo.get("tag")
        paramGenStatus,inputParams = generateComplexTestInputParam(tag,testParams)
    else:
        if paramTypeInfo.get("paramKey") is not None:
            inputParams = {paramTypeInfo.get("paramKey"):testParams.copy()}
        else:
            inputParams = testParams.copy()

    return paramGenStatus,inputParams

#-----------------------------------------------------------------------------------------------
# getTestStepParamInfo
#-----------------------------------------------------------------------------------------------
# Syntax      : getTestStepParamInfo(params)
# Description : Method to get the test param details to display
# Parameter   : params - test params
# Return Value: Params info List
#-----------------------------------------------------------------------------------------------
def getTestStepParamsInfo(params):
    paramsInfo = []
    for param in params.keys():
        if params[param] is not None:
            info = param + " - " + str(params[param])
        else:
            info = param + " - " + "None"
        paramsInfo.append(info)
    return paramsInfo

#-----------------------------------------------------------------------------------------------
# dispTestStepInfo
#-----------------------------------------------------------------------------------------------
# Syntax      : dispTestStepInfo(testStepInfo,testParams,result)
# Description : Method to display the test step details
# Parameter   : testStepInfo - test step details
#             : testParams   - test input params
#             : result       - result details
# Return Value: Nil
#-----------------------------------------------------------------------------------------------
def dispTestStepInfo(testStepInfo,testParams,result):

    testMethod = testStepInfo.get("pluginAPI")
    print "\nTEST STEP NAME   : ", testStepInfo.get("name")
    print "TEST STEP ID     : "  , testStepInfo.get("testStepId")
    if testStepInfo.get("action") == "externalFnCall":
        resultGenInfo = testStepInfo.get("resultGeneration")
        testMethod = resultGenInfo.get("useMethodTag") if resultGenInfo != None else None
        print "EXT METHOD NAME  : " , testMethod
    else:
        print "PLUGIN API NAME  : "  , testMethod

    paramType = testStepInfo.get("paramTypeInfo").get("type")
    if paramType == "userGenerate":
        if type(testParams) is dict:
            paramType = "directDict"
        elif type(testParams) is list:
            paramType = "directList"
        elif type(testParams) is bool:
            paramType = "directBool"
        else:
            paramType = "directString"

    if testParams != {}:
        if paramType == "directDict" and testParams != {}:
            paramsInfo = getTestStepParamsInfo(testParams)
            print "INPUT PARAMETER  : ", ", ".join(paramsInfo)
            #print "INPUT PARAMETERS : ", paramsInfo[0]
            #paramsInfo.pop(0)
            #for param in paramsInfo:
            #    print "%-16s    %s" %(" ",param)
        elif paramType == "directList" or paramType == "directString" or "directBool":
            print "INPUT PARAMETER  : ", testParams

    if testStepInfo.get("resultGeneration").get("expectedValues") != "null":
        print "EXPECTED VALUES  : " , testStepInfo.get("resultGeneration").get("expectedValues")

    print "TEST STEP STATUS :  %s"  %( result.get("Test_Step_Status"))
    del result["Test_Step_Status"]
    message = result.get("Test_Step_Message")
    if result.get("Test_Step_Message") is not None:
        del result["Test_Step_Message"]
    if result:
        print "----------------- Result -----------------"
        for resultTag in result.keys():
            if type(result[resultTag]) is list:
                if len(result[resultTag]) != 0:
                    print "%-16s :  " %(resultTag.upper())
                    print "["
                    for resultData in result[resultTag]:
                        print "%s" %(str(resultData))
                    print "]\n"
                else:
                    print "%-16s :  []" %(resultTag.upper())
            else:
                print "%-16s :  %s" %(resultTag.upper(),result[resultTag])
                #print "%s :  %s" %((resultTag.upper()).ljust(16," "),result[resultTag])

    if message is not None and message.strip() != "":
        print "\n[MESSAGE]: %s" %(message)



#-----------------------------------------------------------------------------------------------
# testStepResultGeneration
#-----------------------------------------------------------------------------------------------
# Syntax      : testStepResultGeneration(testStepResponse,resultGenerationInfo)
# Description : Method to get the required result from the test JSON response
# Parameter   : testStepResponse     - test output JSON response
#             : resultGenerationInfo - result generation details
# Return Value: Test Result Dictionary
#-----------------------------------------------------------------------------------------------
def testStepResultGeneration(testStepResponse,resultGenerationInfo, action="execution"):

    info = {}
    otherInfo  = {}
    if action == "eventListener":
        result = []
        for response in testStepResponse:
            eventResult = response.get("param") if response.get("param") is not None else response.get("params")
            result.append(eventResult)
    if action in ["eventRegister","eventUnRegister"]:
        if testStepResponse.get("result") is not None:
            result = testStepResponse.get("result")
        else:
            result = testStepResponse.get("params")
    elif action == "execution":
        result = testStepResponse.get("result")
        responseInfo = testStepResponse.copy()
        for responseKey in responseInfo.keys():
            if responseKey not in [ "jsonrpc","id","result" ]:
                otherInfo[responseKey] = responseInfo[responseKey]

    if "useMethodTag" in resultGenerationInfo.keys():
        tag = resultGenerationInfo.get("useMethodTag")
        arg = resultGenerationInfo.get("arguments")
        if arg is not None and arg!= "":
            arg = arg.split(",")
        else:
            arg = []
        expectedValues = resultGenerationInfo.get("expectedValues")
        if expectedValues != None and expectedValues != "null":
             expectedValues = expectedValues.split(",")
        else:
             expectedValues = []
        if action in ["eventListener","eventRegister","eventUnRegister"]:
            info = CheckAndGenerateEventResult(result,tag,arg,expectedValues)
        elif action == "externalFnCall":
            paths = [ basePathLoc, deviceConfigFile, deviceIP ]
            info = ExecExternalFnAndGenerateResult(tag,arg,expectedValues,paths)
        else:
            info = CheckAndGenerateTestStepResult(result,tag,arg,expectedValues,otherInfo)
        if info["Test_Step_Status"] == "FAILURE" and action != "eventListener" and action != "externalFnCall":
            print "\nJSON Cmd : ",testStepJSONCmd
            print "\nResponse : ",testStepResponse

    else:
        if resultGenerationInfo.get("expectedValues") == "null" and result is None:
            info["Test_Step_Status"] = "SUCCESS"
        else:
            info["Test_Step_Status"] = "FAILURE"
    return info


#-----------------------------------------------------------------------------------------------
# saveTestStepResult
#-----------------------------------------------------------------------------------------------
# Syntax      : saveTestStepResult(testStepId,result)
# Description : Method to save the test step result
# Parameter   : testStepId - test step Id
#             : result     - test step result
# Return Value: Nil
#-----------------------------------------------------------------------------------------------
def saveTestStepResult(testStepId,result):
    allSavedTestStepIds = []
    for testStepResult in testStepResults:
        allSavedTestStepIds.append(testStepResult.get("testStepId"))

    if testStepId in allSavedTestStepIds:
        for testStepResult in testStepResults:
            if testStepId == testStepResult.get("testStepId"):
                testStepResult.get("result").append(result)
                break;
    else:
        resultInfo = {}
        resultInfo["testStepId"] = testStepId
        resultInfo["result"]     = [result]
        testStepResults.append(resultInfo)


#-----------------------------------------------------------------------------------------------
# getPreviousResultParserInfo
#-----------------------------------------------------------------------------------------------
# Syntax      : getPreviousResultParserInfo(tag)
# Description : Method to get the parser details for parsing the previous test result
# Parameter   : tag - node like param, expectedValues & conditionalExecution
# Return Value: Parser Info Dictionary
#-----------------------------------------------------------------------------------------------
def getPreviousResultParserInfo(tag):
    parserInfo = {}
    if tag.attrib.get("Id") is not None and tag.attrib.get("Id") != "":
        parserInfo["testStepIds"] = tag.attrib.get("Id").split(",")
    else:
        parserInfo["testStepIds"] = []
    if tag.attrib.get("subId") is not None and tag.attrib.get("subId") != "":
        parserInfo["subtestStepIds"] = tag.attrib.get("subId").split(",")
    else:
        parserInfo["subtestStepIds"] = []

    parserInfo["useMethodTag"]  = tag.attrib.get("useMethodTag")
    if tag.attrib.get("arguments") is not None and str(tag.attrib.get("arguments")) != "":
        parserInfo["arguments"] = tag.attrib.get("arguments").split(",")
    else:
        parserInfo["arguments"] = []
    return parserInfo


#-----------------------------------------------------------------------------------------------
# updatePreviousResultParserInfo
#-----------------------------------------------------------------------------------------------
# Syntax      : updatePreviousResultParserInfo(resultParserInfo,iterable)
# Description : Method to update the parser info with iterable values
# Parameter   : resultParserInfo - current parser info
#             : iterable         - iterable value
# Return Value: Updated Parser Info Dictionary
#-----------------------------------------------------------------------------------------------
def updatePreviousResultParserInfo(resultParserInfo,iterable):
    parserInfo = resultParserInfo.copy()
    if parserInfo.get("useIterableArg") == "true":
        if parserInfo.get("arguments") is not None and len(parserInfo.get("arguments")) != 0:
            parserInfo.get("arguments").append(iterable)
        else:
            parserInfo["arguments"] = [iterable]
    return parserInfo


#-----------------------------------------------------------------------------------------------
# getConditionalExecutionStatus
#-----------------------------------------------------------------------------------------------
# Syntax      : getConditionalExecutionStatus(testStepResults,parserInfo)
# Description : Method to get the conditional execution status
# Parameter   : testStepResults  - test step result details
#             : parserInfo       - parser details
# Return Value: Function execution status & Condition status (TRUE/FALSE)
#-----------------------------------------------------------------------------------------------
def getConditionalExecutionStatus(testStepResults,parserInfo):
    result = ""
    status = "FAILURE"
    selectedTestStepResults = []
    for resultInfo in testStepResults:
        testStepResult = []
        if resultInfo.get("testStepId") in parserInfo.get("testStepIds"):
            if resultInfo.get("testStepId") != currentTestStepId:
                for results in resultInfo.get("result"):
                    testStepResult.append(results.get("result"))

        elif resultInfo.get("testStepId") == currentTestStepId:
            if parserInfo.get("subtestStepIds") is not None:
                for results in resultInfo.get("result"):
                    if results.get("subtestStepId") in parserInfo.get("subtestStepIds"):
                        if results.get("iterationId") == currentIterationId:
                            testStepResult.append(results.get("result"))

        if len(testStepResult):
            testStepResultInfo = {resultInfo.get("testStepId"):testStepResult}
            selectedTestStepResults.append(testStepResultInfo)

    tag = parserInfo.get("useMethodTag")
    arg = parserInfo.get("arguments")
    status,result = CheckAndGenerateConditionalExecStatus(selectedTestStepResults,tag,arg)
    return status,result


#-----------------------------------------------------------------------------------------------
# getPreviousTestStepResult
#-----------------------------------------------------------------------------------------------
# Syntax      : getPreviousTestStepResult(testStepResults,parserInfo)
# Description : Method to get the previous test step result details
# Parameter   : testStepResults  - test step result details
#             : parserInfo       - parser details
# Return Value: Function execution status & test step result
#-----------------------------------------------------------------------------------------------
def getPreviousTestStepResult(testStepResults,parserInfo):
    result = {}
    status = "FAILURE"
    selectedTestStepResults = []
    for resultInfo in testStepResults:
        testStepResult = []
        if resultInfo.get("testStepId") in parserInfo.get("testStepIds"):
            if resultInfo.get("testStepId") != currentTestStepId:
                for results in resultInfo.get("result"):
                    testStepResult.append(results.get("result"))

        elif resultInfo.get("testStepId") == currentTestStepId:
            if parserInfo.get("subtestStepIds") is not None:
                for results in resultInfo.get("result"):
                    if results.get("subtestStepId") in parserInfo.get("subtestStepIds"):
                        if results.get("iterationId") == currentIterationId:
                            testStepResult.append(results.get("result"))

        if len(testStepResult):
            testStepResultInfo = {resultInfo.get("testStepId"):testStepResult}
            selectedTestStepResults.append(testStepResultInfo)

    tag = parserInfo.get("useMethodTag")
    arg = parserInfo.get("arguments")
    status,result = parsePreviousTestStepResult(selectedTestStepResults,tag,arg)
    return status,result


#-----------------------------------------------------------------------------------------------
# saveRevertTestInfo
#-----------------------------------------------------------------------------------------------
# Syntax      : saveRevertTestInfo(testCaseInfo,testStepInfo,testStepResult)
# Description : Method to save the test API details for revert Get/Set operation
# Parameter   : testCaseInfo   - test case details
#             : testStepInfo   - test step details
#             : testStepResult - test step results
# Return Value: Nil
#-----------------------------------------------------------------------------------------------
def saveRevertTestInfo(testCaseInfo,testStepInfo,testStepResult):

    testCaseType = testCaseInfo.get("testCaseType")
    if testCaseType == "setandget" or testCaseType == "loop" or testCaseType == "stress":
        testMethod = testStepInfo.get("pluginAPI")

        if testCaseInfo.get("revert") == "true" and testStepInfo.get("revertGet") == "yes":
            if revertTestInfo.get("revertGet") is None:
                revertGetInfo = {}
                revertGetInfo = testStepInfo.copy()
                revertGetInfo["method"] = testMethod
                revertGetInfo["testStepId"] = currentTestStepId
                revertGetInfo["resultInfo"] = testStepResult
                revertTestInfo["revertGet"] = revertGetInfo
        if testCaseInfo.get("revert") == "true" and testStepInfo.get("revertSet") == "yes":
            if revertTestInfo.get("revertSet") is None:
                revertSetInfo = {}
                revertSetInfo = testStepInfo.copy()
                revertSetInfo["method"] = testMethod
                revertSetInfo["testStepId"] = currentTestStepId
                revertSetInfo["revertParams"] = testStepInfo.get("revertParams")
                revertTestInfo["revertSet"] = revertSetInfo



#-----------------------------------------------------------------------------------------------
# revertTest
#-----------------------------------------------------------------------------------------------
# Syntax      : revertTest(revertTestInfo)
# Description : Method to perform revert operation
# Parameter   : revertTestInfo - revert test details
# Return Value: Revert Test step status List (SUCCESS/FAILURE)
#-----------------------------------------------------------------------------------------------
def revertTest(revertTestInfo):
    revertGetMethod = revertTestInfo.get("revertGet").get("method")
    revertSetMethod = revertTestInfo.get("revertSet").get("method")
    revertGetParams = revertTestInfo.get("revertGet").get("params").copy()
    revertSetParams = revertTestInfo.get("revertSet").get("params").copy()
    revertGetParamTypeInfo = revertTestInfo.get("revertGet").get("paramTypeInfo").copy()
    revertSetParamTypeInfo = revertTestInfo.get("revertSet").get("paramTypeInfo").copy()

    revertFlags = revertTestInfo.get("revertFlags")
    revertFlagIds = [ flag.get("revertId") for flag in revertFlags ]
    revertTestStepStatus = []

    # In revert action, the result obtained using the Get method is used
    # Set method's input param values . If there are many results for Get
    # method, then based on each result Set method is invoked

    # E.g Get API result - category - Info, state - disabled, module - Bluetooth
    #     Set API Params - {"category":"Info","state":"disabled","module":"Bluetooth"}
    # The substitution takes place based on the param tags. So, user should maintain
    # same tag name in the result generation

    print "\n\n--------------Revert operation--------------"
    for GetResultInfo in revertTestInfo.get("revertGet").get("resultInfo"):
        revertOperation = "TRUE"

        # If the revertGet test step is direct and if revertFlags has
        # the status TRUE, then revert operation takes place

        # If the revertGet test step is loop and it the corresponding
        # revertFlags status is TRUE, then revert operation takes place
        if revertTestInfo.get("revertGet").get("testStepType") != "direct":
            for flag in revertFlags:
                if flag.get("revertId") == GetResultInfo.get("revertId"):
                    revertOperation = flag.get("status")
                    break;
            if GetResultInfo.get("revertId") not in revertFlagIds:
                revertOperation = "FALSE"
        if revertOperation != "TRUE":
            continue;

        if GetResultInfo.get("params") is not None:
            for param in GetResultInfo.get("params").keys():
                revertGetParams[param] = str(GetResultInfo.get("params").get(param))

        for param in revertTestInfo.get("revertSet").get("revertParams"):
            revertSetParams[param] = str(GetResultInfo.get("result").get(param))

        parseStatus = "SUCCESS"
        paramGenStatus,revertSetParams = getTestStepInputParam(revertSetParamTypeInfo,revertSetParams)
        parseStatus = paramGenStatus if paramGenStatus == "FAILURE" else parseStatus

        paramGenStatus,revertGetParams = getTestStepInputParam(revertGetParamTypeInfo,revertGetParams)
        parseStatus = paramGenStatus if paramGenStatus == "FAILURE" else parseStatus


        # Revert Set Operation
        if parseStatus == "SUCCESS":

            # Before reverting, current settings of the test feature is checked
            # If the settings are not as expected, then revert operation takes place
            revertNeedStatus = checkAPICurrentValueBeforeRevert(revertTestInfo.get("revertGet"),revertGetMethod,revertGetParams,GetResultInfo.get("result"))
            if revertNeedStatus != "TRUE":
                print "\n[INFO]: Feature setting is as expected. No revert operation, proceeding..."
                continue;

            execStatus,response = executeCommand(revertSetMethod,revertSetParams)
            if execStatus == "SUCCESS":
                result = testStepResultGeneration(response,revertTestInfo.get("revertSet").get("resultGeneration"))
                revertTestStepStatus.append(result.get("Test_Step_Status"))
                dispTestStepInfo(revertTestInfo.get("revertSet"),revertSetParams,result)

                # Revert Get Operation
                execStatus,response = executeCommand(revertGetMethod,revertGetParams)
                if execStatus == "SUCCESS":
                    result = testStepResultGeneration(response,revertTestInfo.get("revertGet").get("resultGeneration"))
                    revertStatus = result.get("Test_Step_Status")
                    dispTestStepInfo(revertTestInfo.get("revertGet"),revertGetParams,result)
                    compareStatus = compareActualAndRevertResults(GetResultInfo.get("result"),result)
                    if "FAILURE" in revertStatus or "FAILURE" in compareStatus:
                        revertTestStepStatus.append("FAILURE")
                    else:
                       revertTestStepStatus.append("SUCCESS")
                else:
                    revertTestStepStatus.append("FAILURE")
            else:
                revertTestStepStatus.append("FAILURE")
        else:
            revertTestStepStatus.append("FAILURE")

    return revertTestStepStatus

#-----------------------------------------------------------------------------------------------
# checkAPICurrentValueBeforeRevert
#-----------------------------------------------------------------------------------------------
# Syntax      : checkAPICurrentValueBeforeRevert(APIGetInfo,APIGetMethod,APIGetParams,APICheckResult)
# Description : Method to check the feature settings before revert operation
# Parameter   : APIGetInfo   - API info
#             : APIGetMethod - Get API
#             : APIGetParams - API params
#             : APICheckResult - API expected result
# Return Value: SUCCESS/FAILURE
#-----------------------------------------------------------------------------------------------

def checkAPICurrentValueBeforeRevert(APIGetInfo,APIGetMethod,APIGetParams,APICheckResult):
    revertNeedStatus = "FALSE"
    execStatus,response = executeCommand(APIGetMethod,APIGetParams)
    if execStatus == "SUCCESS":
        result = testStepResultGeneration(response,APIGetInfo.get("resultGeneration"))
        APIGetStatus = result.get("Test_Step_Status")
        compareStatus = compareActualAndRevertResults(APICheckResult,result)
        if "FAILURE" in APIGetStatus or "FAILURE" in compareStatus:
            revertNeedStatus = "TRUE"
    else:
        revertNeedStatus = "TRUE"
    if revertNeedStatus == "FALSE":
        dispTestStepInfo(APIGetInfo,APIGetParams,result)

    return revertNeedStatus


#-----------------------------------------------------------------------------------------------
# compareActualAndRevertResults
#-----------------------------------------------------------------------------------------------
# Syntax      : compareActualAndRevertResults(actualResults,revertResults)
# Description : Method to compare the result of actual Get & result of Get method
#               after revert
# Parameter   : actualResults - actual Get method results
#             : revertResults - revert Get method results
# Return Value: SUCCESS/FAILURE
#-----------------------------------------------------------------------------------------------
def compareActualAndRevertResults(actualResults,revertResults):
    status = "SUCCESS"
    for resultTag in actualResults.keys():
        if actualResults.get(resultTag) != revertResults.get(resultTag):
            status = "FAILURE"
    return status


#-----------------------------------------------------------------------------------------------
# dispPluginTestsSummary
#-----------------------------------------------------------------------------------------------
# Syntax      : dispPluginTestsSummary(pluginName,pluginTestsSummary)
# Description : Method to display the list of test case passed/failed and plugin
#               summary details
# Parameter   : pluginName         - name of the plugin
#             : pluginTestsSummary - plugin test case summary
# Return Value: Nil
#-----------------------------------------------------------------------------------------------
def dispPluginTestsSummary(pluginName,pluginTestsSummary):
    totalTests = len(pluginTestsSummary)
    passedTests = 0
    failedTests = 0
    executedTests = 0
    notApplicableTests = 0
    passedTestCases = []
    failedTestCases = []
    notApplicableTestCases = []
    for test in pluginTestsSummary:
        if test.get("status") == "SUCCESS":
            passedTests += 1
            passedTestCases.append(test.get("testCaseName"))
        elif test.get("status") == "FAILURE":
            failedTests += 1
            failedTestCases.append(test.get("testCaseName"))
        else:
            notApplicableTests += 1
            notApplicableTestCases.append(test.get("testCaseName"))

    executedTests = passedTests + failedTests


    #Commenting table format summary due to formatting issue in TM log
    '''print "============================================================"
    print "| %-30s | %-5s  %-7s  %-7s |" %("PLUGIN-NAME","TOTAL","PASSED","FAILED")
    print "============================================================"
    print "| %-30s | %-5s  %-7s  %-7s |" %(pluginName,totalTests,passedTests,failedTests)
    print "------------------------------------------------------------"'''

    counter = 0
    if len(passedTestCases):
        print "\n\n------------------- PASSED TEST CASES LIST -------------------"
        dispTestCaseList(passedTestCases)
    if len(failedTestCases):
        print "\n\n------------------- FAILED TEST CASES LIST -------------------"
        dispTestCaseList(failedTestCases)
    if len(notApplicableTestCases):
        print "\n\n------------------- N/A TEST CASES LIST ----------------------"
        dispTestCaseList(notApplicableTestCases)

    dispTestSummary(pluginName,totalTests,executedTests,passedTests,failedTests,notApplicableTests)


def dispTestSummary(pluginName,totalTests,executedTests,passedTests,failedTests,notApplicableTests):
    print "\n\n======================== PLUGIN TEST SUMMARY ======================"
    print "PLUGIN NAME    : " ,pluginName
    print "TOTAL TESTS    : " ,totalTests
    print "EXECUTED TESTS : " ,executedTests
    print "PASSED TESTS   : " ,passedTests
    print "FAILED TESTS   : " ,failedTests
    print "N/A TESTS      : " ,notApplicableTests


def dispTestCaseList(testCaseList):
    counter = 0
    for test in testCaseList:
        print "%d. %s" %((counter+1),test)
        counter += 1


def dispPerformanceSummary():
    global libObj
    global apiPerformanceInfo

    loggingStatus = "SUCCESS"
    destPath = basePathLoc + "/logs/" + str(libObj.execID) + "/" + str(libObj.execDevId) + "/" + str(libObj.resultId)
    performanceLogFile = '{}_{}_{}_RDKServices_API_ResponseTime.json'.format(str(libObj.execID),str(libObj.execDevId), str(libObj.resultId))
    performanceLogPath = destPath + "/" + performanceLogFile
    performanceStatus = "SUCCESS"
    try:
        print "\n\n======================== PERFORMANCE SUMMARY ======================"
        # Set Performance status based on API response check status
        performanceCheckStatus = "SUCCESS"
        for api_info in apiPerformanceInfo:
            if api_info.get("STATUS") == "HIGH":
                print api_info
                performanceCheckStatus = "FAILURE"
        print "[PERPORMANCE CHECK STATUS]: ",performanceCheckStatus

        if not os.path.exists(destPath):
            print "\nCreating log directory..."
            os.makedirs(destPath)
        if os.path.exists(destPath):
            print "Log directory available. Logging performance data..."
            json_file = open(performanceLogPath,"w")
            performanceInfo = {}
            performanceInfo["RDKServices_API_ResponseTime"] = apiPerformanceInfo
            json.dump(performanceInfo,json_file)
            json_file.close()
            print "Performance Log File: %s" %(performanceLogFile)
            print "API Performance data logged successfully !!!"
        else:
            loggingStatus = "FAILURE"
            print "[ERROR]: Dir path not available to log performance data"

        if performanceCheckStatus == "FAILURE" or loggingStatus == "FAILURE":
            performanceStatus = "FAILURE"

    except Exception as e:
        performanceStatus = "FAILURE"
        print "\nException Occurred : %s" %(e)
    return performanceStatus

#-----------------------------------------------------------------------------------------------
