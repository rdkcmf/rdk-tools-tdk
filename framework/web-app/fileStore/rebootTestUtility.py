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
import performancelib
from performancelib import *
from RebootTestVariables import *

iter_no=0
count=0
#Status of each validation step
StatusUptime= [];
StatusInterface= [];
StatusControllerUI= [];
StatusNoOfPlugins= [];
StatusPlugin= [];

#-------------------------------------------------------
#VALIDATE UPTIME VALUE AFTER REBOOT
#-------------------------------------------------------
def validateUptime(TimeAfterReboot,validate):
    if 0 < int(TimeAfterReboot)<200:
        return "SUCCESS"
    elif validate == "Yes":
        print "Failed to reboot the device. Exiting the Script"
        exitScript(StatusUptime,iter_no);
    else:
        StatusUptime.append(iter_no)
        return "FAILURE"

#-------------------------------------------------------
#FUNCTION TO GET THE INTERFACE STATUS
#-------------------------------------------------------
def getIFStatus(IF_name,validate):
    method = "NetworkControl.1.up@"+IF_name;
    status = rdkservice_getValue(method)
    if status == True:
        return "ENABLED"
    elif validate == "Yes":
        print "Ethernet Interface is not up after reboot. Exiting the script"
        exitScript(StatusInterface,iter_no);
    else:
        StatusInterface.append(iter_no)
        return "DISABLED";
#------------------------------------------------------
#VALIDATE THE NUMBER OF PLUGINS AFTER REBOOT
#------------------------------------------------------
def validateNoOfPlugins(NumberBeforeReboot, NumberAfterReboot, validate):
    if int(NumberBeforeReboot) == int(NumberAfterReboot):
        return "SUCCESS"
    elif validate == "Yes":
        print "The number of plugins before and after reboot are not same"
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
        print "Mismatch in status of plugins before and after reboot"
        Diff_after_reboot = [item for item in statusAfterReboot if item not in statusBeforeReboot]
        Initial_value = [item for item in statusBeforeReboot if item not in statusAfterReboot]
        print "The status after reboot:\n ", Diff_after_reboot;
        print "The status before reboot: \n", Initial_value;

        if validate == "Yes":
            exitScript(StatusPlugin,iter_no)
        else:
            StatusPlugin.append(iter_no)
            return "FAILURE"

#------------------------------------------------------
#GET THE STATUS OF CONTROLLER UI
#------------------------------------------------------
def getUIStatus(validate):
    url = 'http://'+str(performancelib.deviceIP)+':'+str(performancelib.devicePort)+'/Service/Controller/UI'
    statusCode = urllib2.urlopen(url,timeout=3).getcode()
    if statusCode == 200:
        return "ACCESSIBLE"
    elif validate == "Yes":
        print "The controller UI is not up after reboot"
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
    print "\n--------------------------------------------"
    print "SUMMARY OF REBOOT SCRIPT"
    print "----------------------------------------------"
    if len(StatusUptime) > 0:
        print "Iterations where uptime failed :",StatusUptime;
    if len(StatusInterface) > 0:
        print "Iterations where interface is down :",StatusInterface;
    if len(StatusControllerUI) > 0:
        print "Iterations where controller UI is not accessible", StatusControllerUI;
    if len(StatusNoOfPlugins) > 0:
        print "Iterations where there is mismatch in no of plugins",StatusNoOfPlugins;
    if len(StatusPlugin) > 0:
        print "Iterations where status of plugins are different", StatusPlugin;

    print "\nNumber of reboots:%d/%d"%(count,repeatCount)
    print "Number of failures in Uptime status: ", ("NIL" if len(StatusUptime)== 0 else len(StatusUptime))
    print "Number of failures in Interface status: ", ("NIL" if len(StatusInterface)== 0 else len(StatusInterface))
    print "Number of failures in controller ui status: ", ("NIL" if len(StatusControllerUI)== 0 else len(StatusControllerUI))
    print "Number of failures in plugin count: ", ("NIL" if len(StatusNoOfPlugins)== 0 else len(StatusNoOfPlugins))
    print "Number of failures in plugin status: ", ("NIL" if len(StatusPlugin)== 0 else len(StatusPlugin))
