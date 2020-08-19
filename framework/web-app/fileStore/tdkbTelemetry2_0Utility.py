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

from tdkbVariables import *;
from time import sleep;

#################################################################################
# A utility function to get the telemetry2_0 parameter values
#
# Syntax       : getinitialTelemetry2_0Values(tdkTestObj,telStatus,version,URL)
# Parameter    : tdkTestObj
# Return Value : return the status,initial enable Status,Version and URL
#################################################################################
def getinitialTelemetry2_0Values(tdkTestObj):
    expectedresult="SUCCESS";
    getStatus = 0;
    defaultTelstatus = " ";
    defURL = " " ;
    defVersion = " ";

    tdkTestObj.addParameter("ParamName","Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.Enable");
    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    defaultTelstatus  = tdkTestObj.getResultDetails();
    if expectedresult in actualresult :
       #Set the result status of execution
       tdkTestObj.setResultStatus("SUCCESS");
       print "Telemetry Enable status is:",defaultTelstatus;

       tdkTestObj.addParameter("ParamName","Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.Version");
       #Execute testcase on DUT
       tdkTestObj.executeTestCase(expectedresult);
       actualresult = tdkTestObj.getResult();
       defVersion= tdkTestObj.getResultDetails();
       if expectedresult in actualresult:
          #Set the result status of execution
          tdkTestObj.setResultStatus("SUCCESS");
          print "Telemetry Version  is:",defVersion;

          tdkTestObj.addParameter("ParamName","Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.ConfigURL");
          #Execute the test case in DUT
          tdkTestObj.executeTestCase(expectedresult);
          actualresult = tdkTestObj.getResult();
          defURL = tdkTestObj.getResultDetails();
          if expectedresult in actualresult:
             getStatus = 1;
             #Set the result status of execution
             tdkTestObj.setResultStatus("SUCCESS");
             print "Telemetry config URL  ",defURL;
          else:
              #Set the result status of execution
              tdkTestObj.setResultStatus("FAILURE");
              print "Failed to get Telemetry config URL"
       else:
           #Set the result status of execution
           tdkTestObj.setResultStatus("FAILURE");
           print " Failed to Get the Telemetry Version";
    else:
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE");
        print "Failed to get Telemetry Enable status";

    return getStatus,defaultTelstatus,defURL,defVersion;

#################################################################################
# A utility function to set the telemetry2_0 parameter values
#
# Syntax       : setTelemetry2_0Values(tdkTestObj,telStatus,version,URL)
# Parameter    : tdkTestObj,telStatus,version,URL
# Return Value : return the status
#################################################################################
def setTelemetry2_0Values(tdkTestObj,telStatus,version,URL):
    setStatus = 0;
    expectedresult="SUCCESS";

    tdkTestObj.addParameter("ParamName","Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.Enable");
    tdkTestObj.addParameter("ParamValue",telStatus);
    tdkTestObj.addParameter("Type","bool");
    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedresult in actualresult:
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        print "Telemetry Enable status is:",details

        tdkTestObj.addParameter("ParamName","Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.Version");
        tdkTestObj.addParameter("ParamValue",version);
        tdkTestObj.addParameter("Type","string");
        #Execute the test case in DUT
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedresult in actualresult:
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS");
            print "Telemetry Version set status is:",details

            tdkTestObj.addParameter("ParamName","Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.ConfigURL");
            tdkTestObj.addParameter("ParamValue",URL);
            tdkTestObj.addParameter("Type","string");
            #Execute the test case in DUT
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            if expectedresult in actualresult:
                setStatus = 1;
                #Set the result status of execution
                tdkTestObj.setResultStatus("SUCCESS");
                print "Telemetry ConfigURL is",details;
            else:
                #Set the result status of execution
                tdkTestObj.setResultStatus("FAILURE");
                print "Failed to set the Telemetry ConfigURL";
        else:
            #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE");
            print "Failed to set the Telemetry Version";
    else:
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE");
        print "Failed to set the Telemetry Enable status";
    return  setStatus;

#################################################################################
# A utility function to get the PID value of the given process
#
# Syntax       : getPID(tdkTestObj,ps_name)
# Parameter    : tdkTestObj, process Name
# Return Value : return the status and PID value
#################################################################################
def getPID(tdkTestObj,ps_name):
    status = 1;
    cmd = "pidof %s" %ps_name;
    expectedresult="SUCCESS";
    tdkTestObj.addParameter("command",cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails().strip().replace("\\n", "");
    return details,actualresult;

#################################################################################
# A utility function to Enable the Telemetry Debug Logs
#
# Syntax       : enableTelemetryDebugLogs(tdkTestObj)
# Parameter    : tdkTestObj
# Return Value : return the result and details
#################################################################################
def enableTelemetryDebugLogs(tdkTestObj):
    status =1;
    cmd = "touch /nvram/enable_t2_debug";
    expectedresult="SUCCESS";
    tdkTestObj.addParameter("command",cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails().strip().replace("\\n", "");
    return actualresult,details;

#################################################################################
# A utility function to check Pre-requisite for Telemetry2_0
#
# Syntax       : telemetry2_0_Prerequisite(sysobj,tdkTestObj_Sys_ExeCmd,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_set)
# Parameter    : sysObj,tdkTestObj_Sys_ExeCmd,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_set
# Return Value : return the status,Revert Flag, initial Status,initial Version and initial URL
#################################################################################
def telemetry2_0_Prerequisite(sysobj,tdkTestObj_Sys_ExeCmd,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_set):
    SetURL = TEL_CONFIG_URL ;
    expectedresult = "SUCCESS"
    preReq_Status = 0;
    revertFlag = 0;
    paramSet = 0;
    initialStatus = "";
    initialVersion = "";
    initialURL = "";
    enableRes,enableDetails = enableTelemetryDebugLogs(tdkTestObj_Sys_ExeCmd);
    if expectedresult in enableRes:
        tdkTestObj_Sys_ExeCmd.setResultStatus("SUCCESS");
        print "TEST STEP : Enable the Telemetry Debug logs";
        print "EXPECTED RESULT : Should Enable the Telemetry Debug logs";
        print "ACTUAL RESULT : Telemetry Debug logs was Enabled";
        print "[TEST EXECUTION RESULT] : SUCCESS"
        pid,pidresult = getPID(tdkTestObj_Sys_ExeCmd,"telemetry2_0");

        if expectedresult in pidresult:
            tdkTestObj_Sys_ExeCmd.setResultStatus("SUCCESS");
            print "TEST STEP : Get the PID value of Telemetry2_0 Process";
            print "EXPECTED RESULT : Should get the PID value of Telemetry Process";
            print "ACTUAL RESULT : Telemetry PID value was retrieved Successfully";
            print "[TEST EXECUTION RESULT] : SUCCESS"

            if pid != "":
                preReq_Status = 1;
                print "telemetry2_0 Process is already Running, PID is ",pid
            else:
                print "telemetry2_0 Process is not running in initial stage"
                getResult,initialStatus,initialURL,initialVersion = getinitialTelemetry2_0Values(tdkTestObj_Tr181_Get);
                if getResult == 1:
                    tdkTestObj_Tr181_Get.setResultStatus("SUCCESS");
                    print "TEST STEP : Get the values of Telemetry2_0 Enable,Version and ConfigURL value";
                    print "EXPECTED RESULT : Should get the values of Telemetry2_0 Enable,Version and ConfigURL";
                    print "ACTUAL RESULT : Telemetry2_0 Enable,Version and ConfigURL values retrieved Successfully";
                    print "[TEST EXECUTION RESULT] : SUCCESS"

                    if initialStatus == "true" and initialVersion == 2 and initialURL == SetURL:
                        paramSet = 1;
                    else:
                        setResult = setTelemetry2_0Values(tdkTestObj_Tr181_set,"true","2",SetURL);
                        if setResult == 1:
                            revertFlag = 1;
                            tdkTestObj_Tr181_set.setResultStatus("SUCCESS");
                            print "TEST STEP : Set the values of Telemetry2_0 Enable,Version and ConfigURL value";
                            print "EXPECTED RESULT : Set operation of Telemetry2_0 Enable,Version and ConfigURL should Success";
                            print "ACTUAL RESULT : Successfully set the values of Telemetry2_0 Enable,Version and ConfigURL";
                            print "[TEST EXECUTION RESULT] : SUCCESS"
                            paramSet = 1;
                        else:
                            paramSet = 0;
                            tdkTestObj_Tr181_set.setResultStatus("FAILURE");
                            print "TEST STEP : Set the values of Telemetry2_0 Enable,Version and ConfigURL value";
                            print "EXPECTED RESULT : Set operation of Telemetry2_0 Enable,Version and ConfigURL should Success";
                            print "ACTUAL RESULT : Failed to set the values of Telemetry2_0 Enable,Version and ConfigURL";
                            print "[TEST EXECUTION RESULT] : FAILURE"

                    if paramSet == 1:
                        print "******************************************************"
                        print "Initiating Reboot Please wait till the device comes up";
                        print"*******************************************************"
                        sysobj .initiateReboot();
                        sleep(300);
                        pid,pidresult = getPID(tdkTestObj_Sys_ExeCmd,"telemetry2_0");

                        if expectedresult in pidresult and pid != "":
                            tdkTestObj_Sys_ExeCmd.setResultStatus("SUCCESS");
                            print "TEST STEP : Get the PID value of Telemetry2_0 to make sure process is running";
                            print "EXPECTED RESULT : telemetry2_0 process should be running";
                            print "ACTUAL RESULT : telemetry2_0 process is running after reboot, PID is",pid;
                            print "[TEST EXECUTION RESULT] : SUCCESS"
                            preReq_Status = 1;
                        else:
                            tdkTestObj_Sys_ExeCmd.setResultStatus("FAILURE");
                            print "TEST STEP : Get the PID value of Telemetry2_0 to make sure process is running";
                            print "EXPECTED RESULT : telemetry2_0 process should be running";
                            print "ACTUAL RESULT : telemetry2_0 process is NOT running after reboot";
                            print "[TEST EXECUTION RESULT] : FAILURE"
                    else:
                        tdkTestObj_Tr181_set.setResultStatus("FAILURE");
                        print "Parameters set operation was Failed"
                else:
                    tdkTestObj_Tr181_Get.setResultStatus("FAILURE");
                    print "TEST STEP : Get the values of Telemetry2_0 Enable,Version and ConfigURL value";
                    print "EXPECTED RESULT : Should get the values of Telemetry2_0 Enable,Version and ConfigURL";
                    print "ACTUAL RESULT : Failed to get Telemetry2_0 Enable,Version and ConfigURL values";
                    print "[TEST EXECUTION RESULT] : FAILURE"
        else:
            tdkTestObj_Sys_ExeCmd.setResultStatus("FAILURE");
            print "TEST STEP : Get the PID value of Telemetry2_0 Process";
            print "EXPECTED RESULT : Should get the PID value of Telemetry Process";
            print "ACTUAL RESULT : Failed to get the Telemetry PID value";
            print "[TEST EXECUTION RESULT] : FAILURE"
    else:
        tdkTestObj_Sys_ExeCmd.setResultStatus("FAILURE");
        print "TEST STEP : Enable the Telemetry Debug logs";
        print "EXPECTED RESULT : Should Enable the Telemetry Debug logs";
        print "ACTUAL RESULT : Failed to Enable Telemetry Debug logs";
        print "[TEST EXECUTION RESULT] : FAILURE"

    return preReq_Status,revertFlag,initialStatus,initialVersion,initialURL;

#################################################################################
# A utility function to run after all simulations on Telemetry2_0
#
# Syntax       : telemetry2_0_PostProcess(sysobj,tdkTestObj_Sys_ExeCmd,tdkTestObj_Tr181_set,revertFlag,initialStatus,initialVersion,initialURL)
# Parameter    : sysobj,tdkTestObj_Sys_ExeCmd,tdkTestObj_Tr181_set,revertFlag,initialStatus,initialVersion,initialURL
# Return Value : return the status
#################################################################################
def telemetry2_0_PostProcess(sysobj,tdkTestObj_Sys_ExeCmd,tdkTestObj_Tr181_set,revertFlag,initialStatus,initialVersion,initialURL):
    postprocess_Status = 0;
    if revertFlag == 1:
        print "Revert Flag was SET, Initiating Revert operations"
        revertResult = setTelemetry2_0Values(tdkTestObj_Tr181_set,initialStatus,initialVersion,initialURL);
        if revertResult == 1:
            tdkTestObj_Tr181_set.setResultStatus("SUCCESS");
            print "TEST STEP : Revert the Telemetry parameters";
            print "EXPECTED RESULT : Telemetry parameters should be reverted ";
            print "ACTUAL RESULT : Revert operation was success";
            print "[TEST EXECUTION RESULT] : SUCCESS"

            print "******************************************************"
            print "Initiating Reboot Please wait till the device comes up";
            print"*******************************************************"
            sysobj .initiateReboot();
            sleep(300);
            pid,pidresult = getPID(tdkTestObj_Sys_ExeCmd,"telemetry2_0");

            if expectedresult in pidresult and pid == "":
                postprocess_Status = 1;
                tdkTestObj_Sys_ExeCmd.setResultStatus("SUCCESS");
                print "TEST STEP : Get the PID value of telemetry2_0";
                print "EXPECTED RESULT : Telemetry process shouldnt be running";
                print "ACTUAL RESULT : telemetry2_0 Process is NOT Running After Reboot";
                print "[TEST EXECUTION RESULT] : SUCCESS"
            else:
                tdkTestObj_Sys_ExeCmd.setResultStatus("FAILURE");
                print "TEST STEP : Get the PID value of telemetry2_0";
                print "EXPECTED RESULT : Telemetry process Should not be running";
                print "ACTUAL RESULT : telemetry2_0 Process is  Running After Reboot";
                print "[TEST EXECUTION RESULT] : FAILURE"
        else:
            tdkTestObj_Tr181_set.setResultStatus("FAILURE");
            print "TEST STEP : Revert the Telemetry parameters";
            print "EXPECTED RESULT : Telemetry parameters should be reverted ";
            print "ACTUAL RESULT : Revert operation was Failed";
            print "[TEST EXECUTION RESULT] : FAILURE"
    else:
        postprocess_Status = 1;
        print "Revert Flag is not set, no need for Revert Operation"

    return postprocess_Status;

#################################################################################
# A utility function to get the number of lines from the Telemetry Log File
#
# Syntax       : getTelLogFileTotalLinesCount(tdkTestObj)
# Parameter    : tdkTestObj
# Return Value : return the number of lines
#################################################################################
def getTelLogFileTotalLinesCount(tdkTestObj):
    cmd = "cat /rdklogs/logs/telemetry2_0.txt.0 | wc -l";
    expectedresult="SUCCESS";
    tdkTestObj.addParameter("command",cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails().strip().replace("\\n", "");
    linecount = int(details);
    return actualresult,linecount;

#################################################################################
# A utility function to Kill the running proccess
#
# Syntax       : killProcess(tdkTestObj_Sys_ExeCmd,pid,scriptName)
# Parameter    : tdkTestObj_Sys_ExeCmd,pid,scriptname
# Return Value : return the actualresult
################################################################################
def killProcess(tdkTestObj_Sys_ExeCmd,pid,scriptname):
    expectedresult="SUCCESS";
    if scriptname !="":
       cmd = "kill %d ;sh %s &" %(pid,scriptname);
       tdkTestObj_Sys_ExeCmd.addParameter("command",cmd);
       tdkTestObj_Sys_ExeCmd.executeTestCase(expectedresult);
       actualresult = tdkTestObj_Sys_ExeCmd.getResult();
       details = tdkTestObj_Sys_ExeCmd.getResultDetails().strip().replace("\\n", "");
    else:
        cmd = "kill %d " %pid;
        tdkTestObj_Sys_ExeCmd.addParameter("command",cmd);
        tdkTestObj_Sys_ExeCmd.executeTestCase(expectedresult);
        actualresult = tdkTestObj_Sys_ExeCmd.getResult();
        details = tdkTestObj_Sys_ExeCmd.getResultDetails().strip().replace("\\n", "");
    return actualresult;

#################################################################################
# A utility function to Check if process restarted
#
# Syntax       : checkProcessRestarted(tdkTestObj_Sys_ExeCmd,processname)
# Parameter    : tdkTestObj_Sys_ExeCmd,processname
# Return Value : return the actualresult,pid
################################################################################
def checkProcessRestarted(tdkTestObj_Sys_ExeCmd,processname):
    print "Check for every 10 secs whether the process is up"
    retryCount = 0;
    MAX_RETRY =5 ;
    expectedresult="SUCCESS";
    while retryCount < MAX_RETRY:
          pid,actualresult = getPID(tdkTestObj_Sys_ExeCmd,processname);
          if expectedresult in actualresult and pid != "":
             break;
          else:
              sleep(10);
              retryCount = retryCount + 1;
    if pid == "":
       print "Retry Again: Check for every 5 mins whether the process is up"
       retryCount = 0;
       while retryCount < MAX_RETRY:
             pid,actualresult = getPID(tdkTestObj_Sys_ExeCmd,processname);
             if expectedresult in actualresult and pid != "":
                break;
             else:
                 sleep(300);
                 retryCount = retryCount + 1;
    return  actualresult,pid;
