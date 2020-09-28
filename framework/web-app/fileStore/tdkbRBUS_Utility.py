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

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from time import sleep;
from tdkutility import *;

#################################################################################
# A utility function to check whether RBUS is enable or not
#
# Syntax       : isRBUSEnabled(tdkTestObj_Tr181_Get)
# Parameter    : tdkTestObj_Tr181_Get
# Return Value : def_result,default_value
################################################################################
def isRBUSEnabled(tdkTestObj_Tr181_Get):
    expectedresult="SUCCESS";
    parameter_Name = "Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.RBUS.Enable";
    def_result,default_value = getTR181Value(tdkTestObj_Tr181_Get,parameter_Name);
    return def_result,default_value;

#################################################################################
# A utility function to Enable/Disable RBUS Enable Status
#
# Syntax       : doEnableDisableRBUS(enableFlag,sysobj,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_Set)
# Parameter    : enableFlag,sysobj,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_Set
# Return Value : rbus_set,revert_flag
################################################################################
def doEnableDisableRBUS(enableFlag,sysobj,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_Set):
    expectedresult="SUCCESS";
    rbus_set = 0;
    revert_flag = 0;
    parameter_Name = "Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.RBUS.Enable";
    def_result,default_value = isRBUSEnabled(tdkTestObj_Tr181_Get);

    if  expectedresult in def_result:
        if default_value == enableFlag:
            rbus_set = 1;
            print "RBUS Enable status is already ",enableFlag
        else:
            set_result, set_details = setTR181Value(tdkTestObj_Tr181_Set,parameter_Name,enableFlag,"bool");

            if expectedresult  in set_result:
                revert_flag = 1;
                print "TEST STEP : Set the RBUS Enable status to ",enableFlag;
                print "EXPECTED RESULT :  Set Operation should be success";
                print "ACTUAL RESULT : Set operation was success";
                print "[TEST EXECUTION RESULT] : SUCCESS";
                tdkTestObj_Tr181_Set.setResultStatus("SUCCESS");

                doRebootDUT(sysobj);

                get_result,get_details = getTR181Value(tdkTestObj_Tr181_Get,parameter_Name);

                if expectedresult  in get_result and get_details == enableFlag:
                    rbus_set = 1;
                    print "TEST STEP : Get the Enable Status of RBUS ";
                    print "EXPECTED RESULT : Get operation should be success";
                    print "ACTUAL RESULT : RBUS Enable status %s" %get_details;
                    print "[TEST EXECUTION RESULT] : SUCCESS";
                    tdkTestObj_Tr181_Get.setResultStatus("SUCCESS");
                else:
                    revert_flag  = 0;
                    print "TEST STEP : Get the Enable Status of RBUS ";
                    print "EXPECTED RESULT : Get operation should be success";
                    print "ACTUAL RESULT : Failed to get RBUS Enable status";
                    print "[TEST EXECUTION RESULT] : FAILURE";
                    tdkTestObj_Tr181_Get.setResultStatus("FAILURE");
            else:
                rbus_set = 0;
                print "TEST STEP : Set the RBUS Enable status to ",enableFlag;
                print "EXPECTED RESULT :  Set Operation should be success";
                print "ACTUAL RESULT : Set operation Failed";
                print "[TEST EXECUTION RESULT] : FAILURE";
                tdkTestObj_Tr181_Set.setResultStatus("FAILURE");
    else:
        rbus_set = 0;
        print "[TEST EXECUTION RESULT] : FAILURE";
        tdkTestObj_Tr181_Get.setResultStatus("FAILURE");

    #rbus_set = 1 - Successful operation and revert_flag = 1 - initial RBUS enable value was disabled
    return rbus_set,revert_flag;

#################################################################################
# A utility function to check the prerequisite of RBUS
#
# Syntax       : rbus_PreRequisite(sysobj,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_Set,tdkTestObj_Sys_ExeCmd)
# Parameter    : sysobj,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_Set,tdkTestObj_Sys_ExeCmd
# Return Value : rbus_set,revert_flag
################################################################################
def rbus_PreRequisite(sysobj,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_Set,tdkTestObj_Sys_ExeCmd):
    expectedresult="SUCCESS";
    revert_flag = 0;
    rbus_set = 0;
    rbus_set,revert_flag = doEnableDisableRBUS("true",sysobj,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_Set);

    if rbus_set == 1:
        print "RBUS was Enabled successfully"
        tdkTestObj_Tr181_Get.setResultStatus("SUCCESS");

        actualresult,pid_value = getPID(tdkTestObj_Sys_ExeCmd,"rbus_session_mgr");
        if expectedresult  in actualresult and pid_value != "":
            print "RBUS process was running successfully"
            tdkTestObj_Tr181_Get.setResultStatus("SUCCESS");
        else:
            rbus_set = 0;
            print "RBUS was Enabled but RBUS process was NOT running"
            tdkTestObj_Tr181_Get.setResultStatus("FAILURE");
    else:
        print "Failed to Enable RBUS"
        tdkTestObj_Tr181_Get.setResultStatus("FAILURE");

    return rbus_set,revert_flag;

#################################################################################
# A utility function to check the post process of RBUS
#
# Syntax       : rbus_PostProcess(sysobj,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_Set,tdkTestObj_Sys_ExeCmd,revert_flag)
# Parameter    : sysobj,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_Set,tdkTestObj_Sys_ExeCmd,revert_flag
# Return Value : post_process_value
################################################################################
def rbus_PostProcess(sysobj,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_Set,tdkTestObj_Sys_ExeCmd,revert_flag):
    post_process_value = 1;
    expectedresult="SUCCESS";
    parameter_Name = "Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.RBUS.Enable";

    #Revert Flag will set only when the initial value was false
    if revert_flag == 1:
        set_result, set_details = setTR181Value(tdkTestObj_Tr181_Set,parameter_Name,"false","bool");

        if expectedresult in set_result:
            print "TEST STEP : Set the RBUS Enable status to False";
            print "EXPECTED RESULT : Set operation should be success";
            print "ACTUAL RESULT : Set operation was success";
            print "[TEST EXECUTION RESULT] : SUCCESS";
            tdkTestObj_Tr181_Set.setResultStatus("SUCCESS");

            doRebootDUT(sysobj);

            get_result,get_details = getTR181Value(tdkTestObj_Tr181_Get,parameter_Name);

            if expectedresult  in get_result and get_details == "false":
                print "TEST STEP : Get the Enable Status of RBUS ";
                print "EXPECTED RESULT : Get operation should be success";
                print "ACTUAL RESULT : RBUS Enable status %s" %get_details;
                print "[TEST EXECUTION RESULT] : SUCCESS";
                tdkTestObj_Tr181_Get.setResultStatus("SUCCESS");

                actualresult,pid_value = getPID(tdkTestObj_Sys_ExeCmd,"rbus_session_mgr");

                #Since RBUS was disabled, PID value should be empty
                if expectedresult  in actualresult and pid_value == "":
                    print "TEST STEP : Get the PID of RBUS";
                    print "EXPECTED RESULT :  Should get the PID value o RBUS";
                    print "ACTUAL RESULT : PID of RBUS %s" %pid_value;
                    print "[TEST EXECUTION RESULT] : SUCCESS";
                    tdkTestObj_Tr181_Get.setResultStatus("SUCCESS");
                else:
                    post_process_value = 0;
                    print "TEST STEP : Get the PID of RBUS";
                    print "EXPECTED RESULT :  Should get the PID value o RBUS";
                    print "ACTUAL RESULT : Failed to PID value ";
                    print "[TEST EXECUTION RESULT] : FAILURE";
                    tdkTestObj_Tr181_Get.setResultStatus("FAILURE");
            else:
                post_process_value = 0;
                print "TEST STEP : Get the Enable Status of RBUS ";
                print "EXPECTED RESULT : Get operation should be success";
                print "ACTUAL RESULT : Failed to get RBUS Enable status";
                print "[TEST EXECUTION RESULT] : FAILURE";
                tdkTestObj_Tr181_Get.setResultStatus("FAILURE");
        else:
            post_process_value = 0;
            print "TEST STEP : Set the RBUS Enable status to False";
            print "EXPECTED RESULT : Set operation should be success";
            print "ACTUAL RESULT : Set operation was Failed";
            print "[TEST EXECUTION RESULT] : FAILURE";
            tdkTestObj_Tr181_Set.setResultStatus("FAILURE");
    else:
        print "Revert Flag was not set, No need for revert Operation"

    return post_process_value;
