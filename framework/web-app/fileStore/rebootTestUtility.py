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
import urllib2
import rdkv_performancelib
from rdkv_performancelib import *
from StabilityTestVariables import *
import logging

iter_no=0
count=0
logger = None
#Status of each validation step
StatusUptime= [];
StatusInterface= [];
StatusControllerUI= [];
StatusNoOfPlugins= [];
StatusPlugin= [];

#--------------------------------------------------------
# OPEN A LOG FILE TO REDIRECT THE LOGS
#--------------------------------------------------------
def open_logfile(obj):
    global logger;
    formatter = logging.Formatter('%(message)s')
    logger = logging.getLogger()
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setFormatter(formatter)
    output_file = '{}logs/logs/{}_{}_{}_RebootScriptLog.txt'.format(obj.realpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(output_file, mode='w')
    logger.addHandler(fh)
    return logger;


#-------------------------------------------------------
#VALIDATE UPTIME VALUE AFTER REBOOT
#-------------------------------------------------------
def validateUptime(TimeAfterReboot,validate):
    if 0 < int(TimeAfterReboot)<200:
        return "SUCCESS"
    elif validate == "Yes":
        logger.info("Failed to reboot the device. Exiting the Script")
        exitScript(StatusUptime,iter_no);
    else:
        StatusUptime.append(iter_no)
        return "FAILURE"

#-------------------------------------------------------
#FUNCTION TO GET THE INTERFACE STATUS
#-------------------------------------------------------
def getIFStatus(IF_name,validate):
    revert = True
    curr_status = rdkservice_getPluginStatus('org.rdk.Network')
    if curr_status == 'activated':
        revert = False
        status = None
    else:
        status = rdkservice_setPluginStatus("org.rdk.Network","activate")
    output="FAILURE"
    if status == None:
        method = "org.rdk.Network.1.isInterfaceEnabled"
        value='{"interface":"ETHERNET"}'
        status = rdkservice_setValue(method,value)
        status = status["enabled"]
        if status == True:
            output= "ENABLED"
        elif validate == "Yes":
            logger.info( "Ethernet Interface is not up after reboot. Exiting the script")
            exitScript(StatusInterface,iter_no);
        else:
            StatusInterface.append(iter_no)
            output = "DISABLED";
        if revert:
            rev_status = rdkservice_setPluginStatus("org.rdk.Network","deactivate")
            if rev_status == None:
                logger.info( "Reverted network plugin status")
            else:
                logger.info("Unable to revert network plugin status")
    else:
        logger.info("Unable to enable network plugin")
    return output;

#------------------------------------------------------
#VALIDATE THE NUMBER OF PLUGINS AFTER REBOOT
#------------------------------------------------------
def validateNoOfPlugins(NumberBeforeReboot, NumberAfterReboot, validate):
    if int(NumberBeforeReboot) == int(NumberAfterReboot):
        return "SUCCESS"
    elif validate == "Yes":
        logger.info( "The number of plugins before and after reboot are not same")
        exitScript(StatusNoOfPlugins,iter_no)
    else:
        StatusNoOfPlugins.append(iter_no)
        return "FAILURE"

#------------------------------------------------------
#VALIDATE PLUGIN STATUS AFTER REBOOT
#------------------------------------------------------
def validatePluginStatus(statusBeforeReboot,statusAfterReboot,validate):
    if statusBeforeReboot == statusAfterReboot:
        return "SUCCESS"
    else:
        logger.info( "Mismatch in status of plugins before and after reboot")
        #To convert the plugin status from string to list.
        #START
        len_string = statusAfterReboot.count("]")-1;
        status_after_reboot_list=[];
        status_before_reboot_list=[];
        for i in range(0,len_string):
            sublist_after=[];
            after_reboot=statusAfterReboot.split("[[")[1].split("]")[i];
            if "[" in after_reboot:
                after_reboot= after_reboot.split("[")[1];
            sublist_after.append(after_reboot);
            status_after_reboot_list.append(sublist_after);

            sublist_before=[];
            before_reboot=statusBeforeReboot.split("[[")[1].split("]")[i];
            if "[" in before_reboot:
                before_reboot= before_reboot.split("[")[1];
            sublist_before.append(before_reboot);
            status_before_reboot_list.append(sublist_before);
        #END

        Diff_after_reboot = [item for item in status_after_reboot_list if item not in status_before_reboot_list]
        logger.info("The status after reboot:\n%s", Diff_after_reboot);
        Initial_value = [item for item in status_before_reboot_list if item not in status_after_reboot_list]
        logger.info( "The status before reboot: \n%s", Initial_value);

        if validate == "Yes":
            exitScript(StatusPlugin,iter_no)
        else:
            StatusPlugin.append(iter_no)
            return "FAILURE"

#------------------------------------------------------
#GET THE STATUS OF CONTROLLER UI
#------------------------------------------------------
def getUIStatus(validate):
    url = 'http://'+str(rdkv_performancelib.deviceIP)+':'+str(rdkv_performancelib.devicePort)+'/Service/Controller/UI'
    statusCode = urllib2.urlopen(url,timeout=3).getcode()
    if statusCode == 200:
        return "ACCESSIBLE"
    elif validate == "Yes":
        logger.info( "The controller UI is not up after reboot")
        exitScript(StatusControllerUI,iter_no);
    else:
        StatusControllerUI.append(iter_no)
        return "NOT ACCESSIBLE"

#------------------------------------------------------
#EXITING THE SCRIPT IF VALIDATION FAILS
#------------------------------------------------------
def exitScript(StatusList,status):
    StatusList.append(status);
    getSummary(count+1);
    exit();

#-------------------------------------------------------
#PRINT SUMMARY OF TEST BEFORE EXITING
#-------------------------------------------------------
def getSummary(count):
    logger.info( "\n--------------------------------------------")
    logger.info("SUMMARY OF REBOOT SCRIPT")
    logger.info( "----------------------------------------------")
    if len(StatusUptime) > 0:
        logger.info("Iterations where uptime failed :%s",StatusUptime);
    if len(StatusInterface) > 0:
        logger.info("Iterations where interface is down :%s",StatusInterface);
    if len(StatusControllerUI) > 0:
        logger.info("Iterations where controller UI is not accessible : %s", StatusControllerUI);
    if len(StatusNoOfPlugins) > 0:
        logger.info("Iterations where there is mismatch in no of plugins: %s",StatusNoOfPlugins);
    if len(StatusPlugin) > 0:
        logger.info( "Iterations where status of plugins are different: %s", StatusPlugin);

    logger.info( "\nNumber of reboots:%d/%d"%(count,repeatCount))
    logger.info( "Number of failures in Uptime status: %s", ("NIL" if len(StatusUptime)== 0 else len(StatusUptime)))
    logger.info( "Number of failures in Interface status: %s", ("NIL" if len(StatusInterface)== 0 else len(StatusInterface)))
    logger.info( "Number of failures in controller ui status: %s", ("NIL" if len(StatusControllerUI)== 0 else len(StatusControllerUI)))
    logger.info( "Number of failures in plugin count: %s", ("NIL" if len(StatusNoOfPlugins)== 0 else len(StatusNoOfPlugins)))
    logger.info( "Number of failures in plugin status: %s", ("NIL" if len(StatusPlugin)== 0 else len(StatusPlugin)))
