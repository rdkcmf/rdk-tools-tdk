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

from time import sleep;
from tdkbVariables import *;
from tdkutility import *;

#Setting the below values to
#1 -the expected policy to be set priorily
#0 -script will do policy change and reboot
DUT_Mode_Fixed_Mode_OnBootup = 0;
DUT_Mode_Fixed_Mode = 0;
DUT_Mode_Primary_Priority_OnBootup = 0;
DUT_Mode_Primary_Priority= 0;
#log file location for VLAN MANAGER
VLANLOG ="/rdklogs/logs/VLANIFACEMGRLog.txt.0"
#The Expected Wan Manager Policies
ExpectedPolicyList = "FIXED_MODE_ON_BOOTUP, FIXED_MODE, PRIMARY_PRIORITY, PRIMARY_PRIORITY_ON_BOOTUP, MULTIWAN_MODE";
#The Expected Wan Manager interface names
interfaceName = ["dsl0", "eth3", "veip0"];
#The Expected Wan Manager Display Names
displayName =["DSL","WANOE","GPON"];
#The Reporting Period Prameter List
ReportingparamList = ["Device.DSL.X_RDK_Report.DSL.Enabled", "Device.DSL.X_RDK_Report.DSL.ReportingPeriod", "Device.DSL.X_RDK_Report.DSL.Default.ReportingPeriod", "Device.DSL.X_RDK_Report.DSL.Default.OverrideTTL"];
#DSL WAN Parameters
DSL_WAN_Params = ["Device.X_RDK_WanManager.CPEInterface.1.Wan.Enable", "Device.X_RDK_WanManager.CPEInterface.1.Wan.Status", "Device.X_RDK_WanManager.CPEInterface.1.Wan.ActiveLink"];
#WANoE WAN Parameters
WANoE_WAN_Params = ["Device.X_RDK_WanManager.CPEInterface.2.Wan.Enable", "Device.X_RDK_WanManager.CPEInterface.2.Wan.Status", "Device.X_RDK_WanManager.CPEInterface.2.Wan.ActiveLink"];
#Log file to check for DSL Diagnostic Report logs
DSL_log_file = "/rdklogs/logs/XDSLMANAGERLog.txt.0";

#################################################################################
# A utility function to check if the policy is from ExpectedPolicyList
#
# Syntax       : is_policy_expected(policy, step)
# Parameter    : tdkTestObj, policy, step
# Return Value : status
#################################################################################
def is_policy_expected(tdkTestObj, policy, step):
    status = 1;
    if policy in ExpectedPolicyList :
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP %d :Check  if the policy is one from ExpectedPolicyList" %step;
        print "EXPECTED RESULT %d: policy value should be within the expected list" %step;
        print "ACTUAL RESULT %d: policy value is within the expected list" %step;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS";
        status = 0;
        return status;
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "TEST STEP %d :Check the check the policy is one from ExpectedPolicyList" %step;
        print "EXPECTED RESULT %d: policy value should be within the expected list" %step;
        print "ACTUAL RESULT %d: policy value is not within the expected list" %step;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : FAILURE";
        return status;

#################################################################################
# A utility function to set the required policy
#
# Syntax       : set_policy(new_policy, policy_initial, tdkTestObj1, revert)
# Parameter    : new_policy, policy_initial, tdkTestObj1, revert
# Return Value : return to the invoking script
#################################################################################
def set_policy(new_policy, policy_initial, obj1, revert):
    if revert == 1 :
        if policy_initial != new_policy :
            print "Revert Operation is required for Wan Manager Policy";
            policy_set = policy_initial;
        else:
            print "Revert operation is not required for Wan Manager Policy";
            return;
    else:
        policy_set = new_policy;
    expectedresult="SUCCESS";
    #save device's current state before it goes for reboot
    obj1.saveCurrentState();
    tdkTestObj1 = obj1.createTestStep('ExecuteCmdReboot');
    query="sleep 2 && dmcli eRT setv Device.X_RDK_WanManager.Policy string \"%s\" &"%policy_set;
    print "query:%s" %query;
    tdkTestObj1.addParameter("command", query);
    #Execute the test case in DUT
    tdkTestObj1.executeTestCase(expectedresult);
    sleep(300);
    print "Set operation completed";
    #Restore previous state after reboot
    obj1.restorePreviousStateAfterReboot();
    sleep(60);
    return;

#################################################################################
# A utility function to get the policy
#
# Syntax       : get_policy(tdkTestObj, step)
# Parameter    : tdkTestObj, step
# Return Value : status, policy
#################################################################################
def get_policy(tdkTestObj, step) :
    expectedresult= "SUCCESS";
    status = 1;
    tdkTestObj.addParameter("ParamName","Device.X_RDK_WanManager.Policy");
    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    policy = details.strip().replace("\\n", "");
    if expectedresult in actualresult and policy != "":
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP %d :Check the value of wanmanager policy " %step;
        print "EXPECTED RESULT %d: Should get wanmanager policy" %step;
        print "ACTUAL RESULT %d: The value received is %s" %(step, policy);
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS";
        status = 0;
        return status,policy;
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "TEST STEP %d :Check the value of wanmanager policy" %step;
        print "EXPECTED RESULT %d: Should get wanmanager policy" %step;
        print "ACTUAL RESULT %d: The value received is %s" %(step, policy);
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : FAILURE";
        return status,policy;

#################################################################################
# A utility function to get the number of lines from the Log file
#
# Syntax       : getLogFileTotalLinesCount(tdkTestObj, string, step)
# Parameter    : tdkTestObj, string,  step
# Return Value : return the number of lines and the current step
#################################################################################

def getLogFileTotalLinesCount(tdkTestObj, string, step):
    cmd = "grep -ire " + "\"" + string + "\"  " + DSL_log_file + " | wc -l";
    expectedresult="SUCCESS";
    tdkTestObj.addParameter("command",cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "\n*********************************************";
    print "TEST STEP %d : Get the number of log lines currently present" %step;
    print "EXPECTED RESULT %d : Should get the number of log lines currently present" %step;
    print "Query : %s" %cmd;
    count = 0;

    if expectedresult in actualresult:
        count = int(tdkTestObj.getResultDetails().strip().replace("\\n", ""));
        tdkTestObj.setResultStatus("SUCCESS");
        print "ACTUAL RESULT %d: Successfully captured the number of log lines present : %d" %(step, count);
        print "[TEST EXECUTION RESULT] : SUCCESS";
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "ACTUAL RESULT %d: Failed to  capture the number of log lines present : %s" %(step, details);
        print "[TEST EXECUTION RESULT] : FAILURE";
    print "*********************************************\n";
    return count,step;

#################################################################################
# A utility function to get Reporting Parameter values
#
# Syntax       : getReportingParams(tdkTestObj, step)
# Parameter    : tdkTestObj, step
# Return Value : return the values and status
#################################################################################

def getReportingParams(obj, step):
    expectedresult="SUCCESS";
    status = 1;
    get_value = [];
    tdkTestObj,actualresult,get_value = getMultipleParameterValues(obj,ReportingparamList);
    print "TEST STEP %d: Get the values of Device.DSL.X_RDK_Report.DSL.Enabled, Device.DSL.X_RDK_Report.DSL.ReportingPeriod, Device.DSL.X_RDK_Report.DSL.Default.ReportingPeriod and Device.DSL.X_RDK_Report.DSL.Default.OverrideTTL" %step;
    print "EXPECTED RESULT %d: Should get the values of each parameter successfully" %step;

    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "ACTUAL RESULT %d: Values are respectively :%s" %(step, get_value);
        print "[TEST EXECUTION RESULT] : SUCCESS";

        if get_value[0] != "" and get_value[1] != "" and get_value[2] != "" and get_value[3] != "":
            status = 0;
            tdkTestObj.setResultStatus("SUCCESS");
            print "Successfully retrived the values";
            print "[TEST EXECUTION RESULT] : SUCCESS";
        else :
            tdkTestObj.setResultStatus("FAILURE");
            print "Failed to retrive the values";
            print "[TEST EXECUTION RESULT] : FAILURE";
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "ACTUAL RESULT %d: Values are respectively :%s" %(step, get_value);
        print "[TEST EXECUTION RESULT] : FAILURE";
    return tdkTestObj,get_value,status;

#################################################################################
# A utility function to set Reporting parameters
#
# Syntax       : setReportingParams(tdkTestObj, expectedresult, value_list, step)
# Parameter    : tdkTestObj, expectedresult, value_list, step
# Return Value : return the status
#################################################################################

def setReportingParams(tdkTestObj, expectedresult, value_list, step):
    status = 1;
    if value_list[3] == "0" :
        list = "Device.DSL.X_RDK_Report.DSL.Enabled|" + value_list[0] + "|boolean|Device.DSL.X_RDK_Report.DSL.ReportingPeriod|" + value_list[1] + "|unsignedint|Device.DSL.X_RDK_Report.DSL.Default.ReportingPeriod|" + value_list[2] + "|unsignedint";
    else :
        list = "Device.DSL.X_RDK_Report.DSL.Enabled|" + value_list[0] + "|boolean|Device.DSL.X_RDK_Report.DSL.ReportingPeriod|" + value_list[1] + "|unsignedint|Device.DSL.X_RDK_Report.DSL.Default.ReportingPeriod|" + value_list[2] + "|unsignedint|Device.DSL.X_RDK_Report.DSL.Default.OverrideTTL|" + value_list[3] + "|unsignedint";
    tdkTestObj.addParameter("paramList",list);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "TEST STEP %d : Set Device.DSL.X_RDK_Report.DSL.Enabled to %s, Device.DSL.X_RDK_Report.DSL.ReportingPeriod to %s, Device.DSL.X_RDK_Report.DSL.Default.ReportingPeriod to %s and Device.DSL.X_RDK_Report.DSL.Default.OverrideTTL to %s" %(step, value_list[0], value_list[1], value_list[2], value_list[3]);
    print "EXPECTED RESULT %d : The set operation should be success" %step;

    if expectedresult in actualresult:
        status = 0;
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        print "ACTUAL RESULT %d: The reporting parameters are set successfully" %step;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS";
    else:
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE");
        print "ACTUAL RESULT %d: Failed to set reporting parameters successfully" %step;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : FAILURE";
    return status;

#################################################################################
# A utility function to check the status of DSL WAN connection
#
# Syntax       : getDSLWANStatus(tdkTestObj, step)
# Parameter    : obj, step
# Return Value : return the status
#################################################################################

def getDSLWANStatus(obj, step):
    active = 1;
    expectedresult="SUCCESS";
    tdkTestObj,actualresult,dsl_wan = getMultipleParameterValues(obj,DSL_WAN_Params);
    print "CPE Interface WAN parameters are : %s" %DSL_WAN_Params;
    print "TEST STEP %d: Get the values of CPEInterface WAN parameters for DSL" %step;
    print "EXPECTED RESULT %d: Should get the values of each parameter successfully" %step;

    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "ACTUAL RESULT %d: Values are respectively :%s" %(step, dsl_wan);
        print "[TEST EXECUTION RESULT] : SUCCESS";

        if dsl_wan[1] == "Up" and dsl_wan[2] == "true":
            active = 0;
            print "DSL WAN status is Up";
        else:
            print "DSL WAN status is not Up";
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "ACTUAL RESULT %d: Values are respectively :%s" %(step, dsl_wan);
        print "[TEST EXECUTION RESULT] : FAILURE";
    return tdkTestObj,dsl_wan,active;

#################################################################################
# A utility function to check the status of WANoE WAN connection
#
# Syntax       : geWANoEWANStatus(tdkTestObj, step)
# Parameter    : obj, step
# Return Value : return the status
#################################################################################

def getWANoEWANStatus(obj, step):
    active = 1;
    expectedresult="SUCCESS";
    tdkTestObj,actualresult,wanoe_wan = getMultipleParameterValues(obj,WANoE_WAN_Params);
    print "CPE Interface WAN parameters are : %s" %WANoE_WAN_Params;
    print "TEST STEP %d: Get the values of CPEInterface WAN parameters for WANoE" %step;
    print "EXPECTED RESULT %d: Should get the values of each parameter successfully" %step;

    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "ACTUAL RESULT %d: Values are respectively :%s" %(step, wanoe_wan);
        print "[TEST EXECUTION RESULT] : SUCCESS";

        if wanoe_wan[1] == "Up" and wanoe_wan[2] == "true":
            active = 0;
            print "WANoE WAN status is Up";
        else:
            print "WANoE WAN status is not Up";
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "ACTUAL RESULT %d: Values are respectively :%s" %(step, wanoe_wan);
        print "[TEST EXECUTION RESULT] : FAILURE";
    return wanoe_wan,active;

#################################################################################
# Pre-requisite function for scripts checking DSL Diagnostic Report sending
#
# Syntax       : dslreports_prereq(tdkTestObj, rep_params, step)
# Parameter    : tdkTestObj, rep_params, step
# Return Value : return the status
#################################################################################

def dslreports_prereq(tdkTestObj, rep_params, step):
    status = 1;
    expectedresult = "SUCCESS";
    #Set the Default reporting period and Reporting period to 0
    print "TEST STEP %d : Set Device.DSL.X_RDK_Report.DSL.Default.ReportingPeriod and Device.DSL.X_RDK_Report.DSL.ReportingPeriod to 0" %step;
    print "EXPECTED RESULT %d : The values are set successfully" %step;
    rep_period = "0";
    def_period = "0";
    list = "Device.DSL.X_RDK_Report.DSL.ReportingPeriod|" + rep_period + "|unsignedint|Device.DSL.X_RDK_Report.DSL.Default.ReportingPeriod|" + def_period + "|unsignedint";
    tdkTestObj.addParameter("paramList",list);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();

    if expectedresult in actualresult:
        status = 0;
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        print "ACTUAL RESULT %d: The reporting parameters are set successfully" %step;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS";

        if int(rep_params[3]) == 0 :
            #As override TTL is 0, sleeping for the duration of Default reporting period
            print "Sleeping for %s" %rep_params[2];
            sleep(int(rep_params[2]));
        else:
            #As override TTL is not 0, sleeping for the duration of Reporting period if it is non-zero, else sleeping for Default reporting period
            if int(rep_params[1]) == 0 :
                sleep_time = rep_params[2];
            else:
                sleep_time = rep_params[1];
            print "Sleeping for %s" %sleep_time;
            sleep(int(sleep_time));
    else:
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE");
        print "ACTUAL RESULT %d: Failed to set reporting parameters successfully" %step;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : FAILURE";
    #Intoduce a common sleep time before initial line count is captured
    sleep(5);
    return status;

#################################################################################
# Function for script to Disable and Enable the WAN interface
# Syntax       : EnableDisableInterafce(intrNo,setValue)
# Parameter    : instance of interface, Value to be set
# Return Value : return the status
#################################################################################
def EnableDisableInterafce(intrNo,setValue,tdkTestObj):
    tdkTestObj.addParameter("ParamName","Device.X_RDK_WanManager.CPEInterface.%d.Wan.Enable"%intrNo);
    tdkTestObj.addParameter("ParamValue",setValue);
    tdkTestObj.addParameter("Type","bool");
    expectedresult= "SUCCESS";
    #Execute testcase on DUT
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    Setresult = tdkTestObj.getResultDetails();

    return actualresult,tdkTestObj;

#################################################################################
# Function for script to Make Wan Priorties unequal to set equal Wan Type
# Syntax       : MakePriorityUnEqual ()
# Parameter    : None
# Return Value : return the revertflag,default,actualresult
###############################################################################
def MakePriorityUnEqual (tdkTestObj_Get,tdkTestObj_Set):
    paramList =["Device.X_RDK_WanManager.CPEInterface.1.Wan.Priority","Device.X_RDK_WanManager.CPEInterface.2.Wan.Priority"];
    priority1 = 0;
    revertflag = 0;
    default = [];
    print "TEST STEP : Making WAN priorities Un-equal if equal";
    print "EXPECTED RESULT : Should make WAN priorities Un-equal if equal";
    for item in paramList:
        tdkTestObj = tdkTestObj_Get;
        tdkTestObj.addParameter("ParamName",item);
        expectedresult= "SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails().strip().replace("\\n", "");
        if expectedresult in actualresult:
            default.append(details);
        else:
            print "Get operation failed for %s"%item
            break;

    if expectedresult in actualresult:
        if default [0] == default [1]:
            revertflag =1;
            print "The priorities are equal and changing the priority for 2nd interface";
            tdkTestObj = tdkTestObj_Set;
            tdkTestObj.addParameter("ParamName","Device.X_RDK_WanManager.CPEInterface.2.Wan.Priority")
            tdkTestObj.addParameter("ParamValue","2");
            tdkTestObj.addParameter("Type","int");
            expectedresult= "SUCCESS";
            #Execute testcase on DUT
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            Setresult = tdkTestObj.getResultDetails();
        else:
            print "The priorities are unequal and no change is required";
        print "ACTUAL RESULT :Priorities are Un-equal now"
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS";
    else:
         print "ACTUAL RESULT : Making WAN Type un-equal cannot be procceeded as get operation failed for %s" %item;
         print "[TEST EXECUTION RESULT]:  FAILURE";
    return revertflag,default,actualresult;

#################################################################################
# Function for script to Make Wan Priorties equal
# Syntax       : MakePriorityEqual (tdkTestObj_Get,tdkTestObj_Set)
# Parameter    : tdkTestObj_Get,tdkTestObj_Set
# Return Value : return the revertflag,default,actualresult
###############################################################################
def MakePriorityEqual (tdkTestObj_Get,tdkTestObj_Set):
    paramList =["Device.X_RDK_WanManager.CPEInterface.1.Wan.Priority","Device.X_RDK_WanManager.CPEInterface.2.Wan.Priority"];
    revertflag = 0;
    default = [];

    for item in paramList:
        tdkTestObj = tdkTestObj_Get;
        tdkTestObj.addParameter("ParamName",item);
        expectedresult= "SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails().strip().replace("\\n", "");
        if expectedresult in actualresult:
            default.append(details);
        else:
            break;
    print "Default priority Values are :",default;
    if expectedresult in actualresult:
        if default [0] != default [1]:
            revertflag =1;
            default[0] = str(default[0]);
            print "The priorities are unequal and changing the priority for 2nd interface";
            tdkTestObj = tdkTestObj_Set;
            tdkTestObj.addParameter("ParamName","Device.X_RDK_WanManager.CPEInterface.2.Wan.Priority");
            tdkTestObj.addParameter("ParamValue",(default[0]));
            tdkTestObj.addParameter("Type","int");
            expectedresult= "SUCCESS";
            #Execute testcase on DUT
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            Setresult = tdkTestObj.getResultDetails();
        else:
            print "The priorities are equal and no change is required";
    return revertflag,default,actualresult;

#################################################################################
# Function for script to Make Wan Type unequal
# Syntax       : MakeWANTypeUnEqual (tdkTestObj_Get,tdkTestObj_Set)
# Parameter    : tdkTestObj_Get,tdkTestObj_Set
# Return Value : return the revertflag,default,actualresult
###############################################################################
def MakeWANTypeUnEqual(tdkTestObj_Get,tdkTestObj_Set):
    paramList = ["Device.X_RDK_WanManager.CPEInterface.1.Wan.Type","Device.X_RDK_WanManager.CPEInterface.2.Wan.Type"];
    revertflag = 0;
    default = [];
    print "TEST STEP : Making WAN Type Un-equal if equal";
    print "EXPECTED RESULT : Should make WAN Type Un-equal if equal"

    for item in paramList:
        tdkTestObj = tdkTestObj_Get;
        tdkTestObj.addParameter("ParamName",item);
        expectedresult= "SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails().strip().replace("\\n", "");
        if expectedresult in actualresult:
            default.append(details);
        else:
            print "Get operation failed for %s "%item;
            break;

    print "Current WAN Type  Values are :",default;

    if expectedresult in actualresult:
        if default [0] == default [1]:
            revertflag =1;
            if default [1] == "Primary":
                setValue = "Secondary";
            else:
                 setValue = "Primary";
            print "The Wan Types are equal and changing the WAN Type for 2nd interface";
            tdkTestObj = tdkTestObj_Set;
            tdkTestObj.addParameter("ParamName","Device.X_RDK_WanManager.CPEInterface.2.Wan.Type");
            tdkTestObj.addParameter("ParamValue",setValue);
            tdkTestObj.addParameter("Type","string");
            expectedresult= "SUCCESS";
            #Execute testcase on DUT
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            Setresult = tdkTestObj.getResultDetails();
        else:
            print "The Wan Types are un-equal and no change is required";

        print "ACTUAL RESULT :WAN Type are Un-equal now"
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS";
    else:
         print "ACTUAL RESULT : Making WAN Type un-equal cannot be procceeded as get operation failed for %s" %item;
         print "[TEST EXECUTION RESULT]:  FAILURE";
    return revertflag,default,actualresult;

#################################################################################
# Function to get the current Wan Type and Priority for DSL and WANOE interafces
# Syntax       : GetCurrentWanTypeAndPriority (tdkTestObj)
# Parameter    : tdkTestObj
# Return Value : return the defaults,actualresult
###############################################################################
def GetCurrentWanTypeAndPriority(tdkTestObj):
     paramList = ["Device.X_RDK_WanManager.CPEInterface.1.Wan.Type","Device.X_RDK_WanManager.CPEInterface.2.Wan.Type","Device.X_RDK_WanManager.CPEInterface.1.Wan.Priority","Device.X_RDK_WanManager.CPEInterface.2.Wan.Priority"];
     defaults = [];
     expectedresult="SUCCESS";
     print "The current WAN Type and Priority values are being fetched";

     for item in paramList:
         tdkTestObj.addParameter("ParamName",item);
         #Execute the test case in DUT
         tdkTestObj.executeTestCase(expectedresult);
         actualresult = tdkTestObj.getResult();
         details = tdkTestObj.getResultDetails().strip().replace("\\n", "");
         if expectedresult in actualresult:
             defaults.append(details);
         else:
             print "Set operation failed for %s" %item;
             break;
     return defaults,actualresult;

#################################################################################
# Function to Set the requested Wan Type and Priority for DSL and WANOE interafces
# Syntax       : SetWANTypePriority (tdkTestObj,wanDSL,wanWANOE,priDSL,priWANOE)
# Parameter    : tdkTestObj,wanDSL,wanWANOE,priDSL,priWANOE
# Return Value : return the actualresult
###############################################################################
def SetWANTypePriority(tdkTestObj,wanDSL,wanWANOE,priDSL,priWANOE):

    paramList = ["Device.X_RDK_WanManager.CPEInterface.1.Wan.Priority","Device.X_RDK_WanManager.CPEInterface.2.Wan.Priority","Device.X_RDK_WanManager.CPEInterface.1.Wan.Type","Device.X_RDK_WanManager.CPEInterface.2.Wan.Type"];
    dataType = ["int","int","string","string"];
    setValues = [priDSL,priWANOE,wanDSL,wanWANOE];
    index =0;

    for item in paramList:
        tdkTestObj.addParameter("ParamName",item)
        tdkTestObj.addParameter("ParamValue",setValues[index]);
        tdkTestObj.addParameter("Type",dataType[index]);
        expectedresult= "SUCCESS";
        #Execute testcase on DUT
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        Setresult = tdkTestObj.getResultDetails();
        index =index +1;
        if expectedresult in actualresult:
           print "Set operation sucesss for %s" %item;
        else:
            print "Set operation failed for %s" %item;
            break;
    return actualresult;

#################################################################################
# Function to Set the requested Wan Type and Priority for DSL and WANOE interafces
# Syntax       : SetWANTypethenPriority(tdkTestObj,wanDSL,wanWANOE,priDSL,priWANOE)
# Parameter    : tdkTestObj,wanDSL,wanWANOE,priDSL,priWANOE
# Return Value : return the actualresult
###############################################################################
def SetWANTypethenPriority(tdkTestObj,wanDSL,wanWANOE,priDSL,priWANOE):

    paramList = ["Device.X_RDK_WanManager.CPEInterface.1.Wan.Type","Device.X_RDK_WanManager.CPEInterface.2.Wan.Type","Device.X_RDK_WanManager.CPEInterface.1.Wan.Priority","Device.X_RDK_WanManager.CPEInterface.2.Wan.Priority"];
    dataType = ["string","string","int","int",];
    setValues = [wanDSL,wanWANOE,priDSL,priWANOE];
    index =0;

    for item in paramList:
        tdkTestObj.addParameter("ParamName",item)
        tdkTestObj.addParameter("ParamValue",setValues[index]);
        tdkTestObj.addParameter("Type",dataType[index]);
        expectedresult= "SUCCESS";
        #Execute testcase on DUT
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        Setresult = tdkTestObj.getResultDetails();
        index =index +1;
        if expectedresult in actualresult:
           print "Set operation successs for %s" %item;
        else:
            print "Set operation failed for %s" %item;
            break;
    return actualresult;

#################################################################################
# Function to Disable and Enable DSL and WANOE interfaces
# Syntax       : ToggleDSLAndWANOEInterfaces(tdkTestObj_Set,setValue)
# Parameter    : tdkTestObj_Set,setValue
# Return Value : return the actualresult
###############################################################################

def ToggleDSLAndWANOEInterfaces(tdkTestObj_Set,setValue):
    paramlist = ["Device.X_RDK_WanManager.CPEInterface.1.Wan.Enable","Device.X_RDK_WanManager.CPEInterface.2.Wan.Enable"];
    for item in paramlist:
        tdkTestObj = tdkTestObj_Set;
        tdkTestObj.addParameter("ParamName",item);
        tdkTestObj.addParameter("ParamValue",setValue);
        tdkTestObj.addParameter("Type","bool");
        #Execute testcase on DUT
        expectedresult ="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        Setresult = tdkTestObj.getResultDetails();
        if expectedresult in actualresult:
           print "%s set to %s successfully" %(item,setValue);
        else:
            print "%s set to %s failed"  %(item,setValue);
            break;
    return actualresult;
