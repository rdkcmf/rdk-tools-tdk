#!/usr/bin/python
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
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
# Methods
#------------------------------------------------------------------------------
import os
import sys
from time import sleep;

def getInstanceNumber(paramName,index):
                try:
                    instanceNumber = 0
                    paramList = paramName.split(".")
                    instanceNumber = paramList[index]
                except:
                        return 0
                return instanceNumber

def readtdkbConfigFile(self):

# Reads config file and returns the value.

# Syntax      : OBJ.readtdkbConfigFile()
# Description : Reads config file and returns the value.
# Parameters  : configFile - Name of config file.
# Return Value: value given in the config file

        configFile = self.realpath + "fileStore/" + "tdkb.config"
        print "Configuration File Found : ", configFile
        sys.stdout.flush()
        HostName="";

        # Checking if file exists
        fileCheck = os.path.isfile(configFile)
        if (fileCheck):
                for line in open(configFile).readlines():
                        if "HOST_NAME" in line:
                                HostName=line.split("=")[1].strip();
                                print "Host name is %s" %HostName;
                if HostName == "":
                    return "NULL"
        else:
                print "Configuration File does not exist."
                sys.stdout.flush()
                exit()
        return HostName;

########## End of Function ##########

def getMultipleParameterValues(obj,paramList):

# getMultipleParameterValues

# Syntax      : getMultipleParameterValues()
# Description : Function to get the values of multiple parameters at single shot
# Parameters  : obj - module object
#             : paramList - List of parameter names
# Return Value: SUCCESS/FAILURE

    expectedresult="SUCCESS";
    status = "SUCCESS";

    actualresult= [];
    orgValue = [];

    #Parse and store the values retrieved in a list
    for index in range(len(paramList)):
            tdkTestObj = obj.createTestStep("TADstub_Get");
            tdkTestObj.addParameter("paramName",paramList[index])
            tdkTestObj.executeTestCase(expectedresult);
            actualresult.append(tdkTestObj.getResult())
            details = tdkTestObj.getResultDetails();
            if details:
                    orgValue.append(details);

    for index in range(len(paramList)):
            if expectedresult not in actualresult[index]:
                    status = "FAILURE";
                    break;

    return (tdkTestObj,status,orgValue);

######### End of Function ##########

def changeAdminPassword(pamobj,password):

# changeAdminPassword

# Syntax      : changeAdminPassword
# Description : Function to change admin password
# Parameters  : sysobj - module object
# Return Value: SUCCESS/FAILURE


     tdkTestObj = pamobj.createTestStep('pam_Setparams');
     tdkTestObj.addParameter("ParamName","Device.Users.User.3.Password");
     tdkTestObj.addParameter("Type","string");
     tdkTestObj.addParameter("ParamValue",password);
     expectedresult="SUCCESS";
     tdkTestObj.executeTestCase(expectedresult);
     actualresult = tdkTestObj.getResult();
     details = tdkTestObj.getResultDetails();
     if expectedresult in actualresult:
         tdkTestObj.setResultStatus("SUCCESS");
         print "TEST STEP : Change the admin password";
         print "EXPECTED RESULT : Should change the admin password";
         print "ACTUAL RESULT : Admin password is changed, %s" %details;
         print "[TEST EXECUTION RESULT] :%s" %actualresult;
     else:
         tdkTestObj.setResultStatus("FAILURE");
         print "TEST STEP : Change the admin password";
         print "EXPECTED RESULT  : Should change the admin password";
         print "ACTUAL RESULT : Failed to change the admin password, %s" %details;
         print "[TEST EXECUTION RESULT] :%s" %actualresult;

######### End of Function ##########
def getTR181Value(tdkTestObj_Tr181_Get,parameter_Name):

# getTR181Value

# Syntax      : getTR181Value
# Description : Function to get a value of TR181 parameter value
# Parameters  : tdkTestObj_Tr181_Get - TR181 Get object
#               parameter_Name - Parameter Name to get a value
# Return Value: actualresult - Result of the execution
#               details - value of the TR181 value

    tdkTestObj_Tr181_Get.addParameter("ParamName",parameter_Name);
    tdkTestObj_Tr181_Get.executeTestCase("SUCCESS");
    actualresult = tdkTestObj_Tr181_Get.getResult();
    details  = tdkTestObj_Tr181_Get.getResultDetails();
    return actualresult,details;

######### End of Function ##########

def setTR181Value(tdkTestObj_Tr181_Set,parameter_Name,parameter_value,parameter_type):

# setTR181Value

# Syntax      : setTR181Value
# Description : Function to set a new value to the TR181 parameter
# Parameters  : tdkTestObj_Tr181_Set - TR181 Set object
#               parameter_Name - Parameter Name to set a value
#               parameter_value - Value to be set
#               parameter_type - Type of the parameter
# Return Value: actualresult - Result of the execution
#               details - execution details

    tdkTestObj_Tr181_Set.addParameter("ParamName",parameter_Name);
    tdkTestObj_Tr181_Set.addParameter("ParamValue",parameter_value);
    tdkTestObj_Tr181_Set.addParameter("Type",parameter_type);
    tdkTestObj_Tr181_Set.executeTestCase("SUCCESS");
    actualresult = tdkTestObj_Tr181_Set.getResult();
    details = tdkTestObj_Tr181_Set.getResultDetails();
    return actualresult,details;

######### End of Function ##########

def doSysutilExecuteCommand(tdkTestObj_Sys_ExeCmd,cmd):

# doSysutilExecuteCommand

# Syntax      : doSysutilExecuteCommand
# Description : Function to do the Execute command operation of sysuti
# Parameters  : tdkTestObj_Sys_ExeCmd - Sysyutil object
#               cmd - command to be executed
# Return Value: actualresult - Result of the execution
#               details - value to be return after execution

    tdkTestObj_Sys_ExeCmd.addParameter("command",cmd);
    tdkTestObj_Sys_ExeCmd.executeTestCase("SUCCESS");
    actualresult = tdkTestObj_Sys_ExeCmd.getResult();
    details = tdkTestObj_Sys_ExeCmd.getResultDetails().strip().replace("\\n", "");
    return actualresult,details;

######### End of Function ##########

def doRebootDUT(sysobj):

# doRebootDUT

# Syntax      : doRebootDUT
# Description : Function to initiate Reboot on DUT
# Parameters  : tdkTestObj_Sys_ExeCmd - Sysyutil object
#               sysobj - sysutil object
# Return Value: None

    print "******************************************************"
    print "Initiating Reboot Please wait till the device comes up";
    sysobj.initiateReboot();
    sleep(300);
    print"*******************************************************"
    print "Reboot operation Successful"

######### End of Function ##########

def getPID(tdkTestObj_Sys_ExeCmd,ps_name):

# getPID

# Syntax      : getPID
# Description : Function to get the PID value of the given process
# Parameters  : tdkTestObj_Sys_ExeCmd - Sysyutil object
#               ps_name - Process Name
# Return Value: actualresult - Result of the execution
#             : details - PID Value of the given process

    cmd = "pidof %s" %ps_name;
    expectedresult="SUCCESS";
    tdkTestObj_Sys_ExeCmd.addParameter("command",cmd);
    tdkTestObj_Sys_ExeCmd.executeTestCase(expectedresult);
    actualresult = tdkTestObj_Sys_ExeCmd.getResult();
    details = tdkTestObj_Sys_ExeCmd.getResultDetails().strip().replace("\\n", "");
    return actualresult,details;

######### End of Function ##########

def isFilePresent(tdkTestObj_Sys_ExeCmd,file_name):

# isFilePresent

# Syntax      : isFilePresent
# Description : Function to Check if given file is present or not
# Parameters  : tdkTestObj_Sys_ExeCmd - Sysyutil object
#               file_name - File Name
# Return Value: actualresult - Result of the execution
#             : details - Details of the execution

    cmd = "ls %s" %file_name;
    expectedresult="SUCCESS";
    tdkTestObj_Sys_ExeCmd.addParameter("command",cmd);
    tdkTestObj_Sys_ExeCmd.executeTestCase(expectedresult);
    actualresult = tdkTestObj_Sys_ExeCmd.getResult();
    details = tdkTestObj_Sys_ExeCmd.getResultDetails().strip().replace("\\n", "");
    return actualresult,details;

######### End of Function ##########

def killProcess(tdkTestObj_Sys_ExeCmd,pid,scriptname):

# killProcess

# Syntax      : killProcess
# Description : Function to Kill the running proccess
# Parameters  : tdkTestObj_Sys_ExeCmd - Sysyutil object
#             : pid - PID of the process to be killed
#             : scriptname - Name of the script to be executed if any
# Return Value: actualresult - Result of the execution

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

######### End of Function ##########

def checkProcessRestarted(tdkTestObj_Sys_ExeCmd,processname):

# checkProcessRestarted

# Syntax      : checkProcessRestarted
# Description : Function to Check if process restarted
# Parameters  : tdkTestObj_Sys_ExeCmd - Sysyutil object
#             : processname - Process Name
# Return Value: actualresult - Result of the execution
#             : pid - PID value of the given process

    print "Check for every 10 secs whether the process is up"
    retryCount = 0;
    MAX_RETRY =5 ;
    expectedresult="SUCCESS";
    while retryCount < MAX_RETRY:
          actualresult,pid = getPID(tdkTestObj_Sys_ExeCmd,processname);
          if expectedresult in actualresult and pid != "":
             break;
          else:
              sleep(10);
              retryCount = retryCount + 1;
    if pid == "":
       print "Retry Again: Check for every 5 mins whether the process is up"
       retryCount = 0;
       while retryCount < MAX_RETRY:
             actualresult,pid = getPID(tdkTestObj_Sys_ExeCmd,processname);
             if expectedresult in actualresult and pid != "":
                break;
             else:
                 sleep(300);
                 retryCount = retryCount + 1;
    return  actualresult,pid;

######### End of Function ##########

#################################Pre-requisite and Post-requsite for OVS ##############################
expectedresult ="SUCCESS";

def ovs_PreRequisite(tdkTestObj_Tr181_Get,tdkTestObj_Tr181_Set):

# ovs_PreRequisite

# Syntax      : ovs_PreRequisite (tdkTestObj_Tr181_Get,tdkTestObj_Tr181_Set)
# Description : Function to ovs Pre-requisite
# Parameters  : tdkTestObj_Tr181_Get -getobject
#             : tdkTestObj_Tr181_Set - setobject
# Return Value: result- status of the function
#             : default -returns default value

    paramlist =["Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.CodeBigFirst.Enable","Device.DeviceInfo.X_RDKCENTRAL-COM_xOpsDeviceMgmt.Mesh.Enable"];
    default =[];
    result ="SUCCESS";
    for item in paramlist:
        def_result,default_value = getTR181Value(tdkTestObj_Tr181_Get,item);
        if expectedresult in def_result:
           default.append(default_value);
        else:
             result ="FAILURE";
             print "get operation failed for %s "%item;
             break;

    setValue = ["false","true"];
    print "\nThe default Values of CodeBig First and  Mesh are ",default;

    print "\n*****As a Pre-requisite Disabling CodeBig First and Enabling Mesh****";

    index =0;
    for item in paramlist:
        set_result, set_details = setTR181Value(tdkTestObj_Tr181_Set,item,setValue[index],"bool");
        if expectedresult in set_result:
           print "%s set %s successfully\n" %(item,setValue[index]);
           index = index + 1;
        else:
             result ="FAILURE";
             print "%s set %s  failed \n" %(item,setValue[index]);
             break;
    return result,default;

def ovs_PostProcess(tdkTestObj_Tr181_Get,tdkTestObj_Tr181_Set,setValue):

# ovs_PostProcess

# Syntax      : ovs_PostProcess(tdkTestObj_Tr181_Get,tdkTestObj_Tr181_Set,setValue):
# Description : Function to ovs Pre-requisite
# Parameters  : tdkTestObj_Tr181_Get -getobject
#             : tdkTestObj_Tr181_Set - setobject
#             : setValue - value to be set
# Return Value: result- status of the function

    result ="SUCCESS";
    paramlist =["Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.CodeBigFirst.Enable","Device.DeviceInfo.X_RDKCENTRAL-COM_xOpsDeviceMgmt.Mesh.Enable"];
    index = 0;
    for item in paramlist:
        set_result, set_details = setTR181Value(tdkTestObj_Tr181_Set,item,setValue[index],"bool");
        if expectedresult in set_result:
           print "%s set %s successfully\n" %(item,setValue[index]);
           index = index + 1;
        else:
             result ="FAILURE";
             print "%s set %s  failed \n" %(item,setValue[index]);
             break;
    return result;


def isOVSEnabled(tdkTestObj_Tr181_Get):

# isOVSEnabled

# Syntax      : isOVSEnabled(tdkTestObj_Tr181_Get):
# Description : Function to check if ovs is enabled
# Parameters  : tdkTestObj_Tr181_Get -getobject
# Return Value: def_result- status of the function
#             : default_value -returns default value

    expectedresult="SUCCESS";
    parameter_Name = "Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.OVS.Enable";
    def_result,default_value = getTR181Value(tdkTestObj_Tr181_Get,parameter_Name);
    return def_result,default_value;

def doEnableDisableOVS(enableFlag,sysobj,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_Set):
# doEnableDisableOVS

# Syntax      : doEnableDisableOVS(enableFlag,sysobj,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_Set):
# Description : Function to Toggle OVS
# Parameters  : enableFlag-value
#             : sysobj - sysutil object
#             : tdkTestObj_Tr181_Get- get object
#             : tdkTestObj_Tr181_Set- set object
# Return Value: ovs_set - gives the status of set
#             : revert_flag - tells wether set operation performed or not
#             : default_value -returns default value

    expectedresult="SUCCESS";
    ovs_set = 0;
    revert_flag = 0;
    parameter_Name = "Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.OVS.Enable";
    def_result,default_value = isOVSEnabled(tdkTestObj_Tr181_Get);

    if  expectedresult in def_result:
        if default_value == enableFlag:
            ovs_set = 1;
            print "OVS Enable status is already ",enableFlag
        else:
            set_result, set_details = setTR181Value(tdkTestObj_Tr181_Set,parameter_Name,enableFlag,"bool");

            if expectedresult  in set_result:
                revert_flag = 1;
                print "TEST STEP : Set the OVS Enable status to ",enableFlag;
                print "EXPECTED RESULT :  Set Operation should be success";
                print "ACTUAL RESULT : Set operation was success";
                print "[TEST EXECUTION RESULT] : SUCCESS";
                tdkTestObj_Tr181_Set.setResultStatus("SUCCESS");

                doRebootDUT(sysobj);

                get_result,get_details = getTR181Value(tdkTestObj_Tr181_Get,parameter_Name);

                if expectedresult  in get_result and get_details == enableFlag:
                    ovs_set = 1;
                    print "TEST STEP : Get the Enable Status of OVS ";
                    print "EXPECTED RESULT : Get operation should be success";
                    print "ACTUAL RESULT : OVS Enable status %s" %get_details;
                    print "[TEST EXECUTION RESULT] : SUCCESS";
                    tdkTestObj_Tr181_Get.setResultStatus("SUCCESS");
                else:
                    revert_flag  = 0;
                    print "TEST STEP : Get the Enable Status of OVS ";
                    print "EXPECTED RESULT : Get operation should be success";
                    print "ACTUAL RESULT : Failed to get OVS Enable status";
                    print "[TEST EXECUTION RESULT] : FAILURE";
                    tdkTestObj_Tr181_Get.setResultStatus("FAILURE");
            else:
                ovs_set = 0;
                print "TEST STEP : Set the OVS Enable status to ",enableFlag;
                print "EXPECTED RESULT :  Set Operation should be success";
                print "ACTUAL RESULT : Set operation Failed";
                print "[TEST EXECUTION RESULT] : FAILURE";
                tdkTestObj_Tr181_Set.setResultStatus("FAILURE");
    else:
        ovs_set = 0;
        print "[TEST EXECUTION RESULT] : FAILURE";
        tdkTestObj_Tr181_Get.setResultStatus("FAILURE");

    #ovs_set = 1 - Successful operation and revert_flag = 1 - initial OVS enable value was disabled
    return ovs_set,revert_flag;
