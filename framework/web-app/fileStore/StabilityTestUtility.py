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
#########################################################################
from rdkv_performancelib import *
import ast
import json
import urllib

expectedResult ="SUCCESS"

def get_plugins_status(obj,plugins):
    cur_plugin_state_dict = {}
    for plugin in plugins:
            plugin_obj = obj.createTestStep('rdkservice_getPluginStatus')
            plugin_obj.addParameter("plugin",plugin)
            plugin_obj.executeTestCase(expectedResult)
            if expectedResult in plugin_obj.getResult():
                cur_plugin_state_dict[plugin] = plugin_obj.getResultDetails()
                plugin_obj.setResultStatus("SUCCESS")
            else:
                cur_plugin_state_dict[plugin] = "FAILURE";
                plugin_obj.setResultStatus("FAILURE")
    return cur_plugin_state_dict

def set_plugins_status(obj,plugins_state_dict):
    plugin_status_list = []
    plugin_status = ""
    for plugin in plugins_state_dict:
        if plugins_state_dict[plugin] != "deactivated" and plugins_state_dict[plugin] != "None":
            print "{}  activating".format(plugin)
            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
            tdkTestObj.addParameter("plugin",plugin)
            tdkTestObj.addParameter("status","activate")
            tdkTestObj.executeTestCase(expectedResult)
            plugin_status = tdkTestObj.getResult()
            if plugin_status == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
        elif plugins_state_dict[plugin] == "deactivated":
            print "{} disabling".format(plugin)
            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
            tdkTestObj.addParameter("plugin",plugin)
            tdkTestObj.addParameter("status","deactivate")
            tdkTestObj.executeTestCase(expectedResult)
            plugin_status = tdkTestObj.getResult()
            if expectedResult in plugin_status:
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
        plugin_status_list.append(plugin_status)
    if all(status == "SUCCESS" for status in plugin_status_list):
        return "SUCCESS"
    else:
        return "FAILURE"

def launch_cobalt(obj):
    return_val = "SUCCESS"
    plugin = "Cobalt"
    tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
    tdkTestObj.addParameter("plugin",plugin)
    tdkTestObj.addParameter("status","activate")
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    if result == "SUCCESS":
        tdkTestObj.setResultStatus("SUCCESS")
        print "\n checking playback is happening in foreground"
        tdkTestObj = obj.createTestStep('rdkservice_getValue')
        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder")
        tdkTestObj.executeTestCase(expectedResult)
        zorder = tdkTestObj.getResultDetails()
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            zorder = ast.literal_eval(zorder)["clients"]
            if len(zorder) != 0:
                tdkTestObj.setResultStatus("SUCCESS")
                if zorder[0] == "cobalt":
                    print "\n Cobalt is playing in the foreground"
                else:
                    param_val = '{"client": "Cobalt"}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.moveToFront")
                    tdkTestObj.addParameter("value",param_val)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if result == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print "\n Unable to move Cobalt to foreground"
                        return_val = "FAILURE"
                        tdkTestObj.setResultStatus("FAILURE")
            else:
                print "org.rdk.RDKShell.1.getZOrder returned empty clients list"
                return_val = "FAILURE"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Unable to get getZOrder value"
            return_val = "FAILURE"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        return_val = "FAILURE"
    return return_val

def get_validation_params(obj):
    validation_dict = {}
    print "\n getting validation params from conf file"
    conf_file,result = getConfigFileName(obj.realpath)
    result, validation_required = getDeviceConfigKeyValue(conf_file,"VALIDATION_REQ")
    if result == "SUCCESS":
        if validation_required == "NO":
            validation_dict["validation_required"] = False
        else:
            validation_dict["validation_required"] = True
            result,validation_dict["ssh_method"] = getDeviceConfigKeyValue(conf_file,"SSH_METHOD")
            validation_dict["host_name"] = obj.IP
            result,validation_dict["user_name"] = getDeviceConfigKeyValue(conf_file,"SSH_USERNAME")
            result,validation_dict["password"] = getDeviceConfigKeyValue(conf_file,"SSH_PASSWORD")
            result,validation_dict["video_validation_script"] = getDeviceConfigKeyValue(conf_file,"VIDEO_VALIDATION_SCRIPT_FILE")
    else:
        print "Failed to get the validation required value from config file, please configure values before test"
    if any(value == "" for value in validation_dict.itervalues()):
        print "please configure values before test"
        validation_dict = {}
    return validation_dict

#------------------------------------------------------------------------
#GET CONFIG FILE NAME
#------------------------------------------------------------------------
def get_configfile_name(obj):
    url = obj.url + '/deviceGroup/getDeviceDetails?deviceIp='+obj.IP
    try:
        data = urllib.urlopen(url).read()
        deviceDetails = json.loads(data)
        deviceName = deviceDetails["devicename"]
        deviceType = deviceDetails["boxtype"]

        deviceConfigFile=""
        status ="SUCCESS"
        configPath = obj.realpath + "/"   + "fileStore/tdkvRDKServiceConfig"
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
    except:
        print "Unable to get Device Details from REST !!!"
        status = "FAILURE"

    return deviceConfigFile,status;

#------------------------------------------------------------------------
#REBOOT DEVICE AS A PRE-REQUESITE
#------------------------------------------------------------------------
def pre_requisite_reboot(obj):
    result = "SUCCESS";
    conf_file, status = get_configfile_name(obj);
    result, reboot_required = getDeviceConfigKeyValue(conf_file,"PRE_REQ_REBOOT")

    if reboot_required.lower() == "yes":

        print "\nRebooting the device as a pre-requisite before starting the script\n"

        #Get the required values to reboot the device
        url = obj.url + '/deviceGroup/getThunderDevicePorts?stbIp='+obj.IP
        try:
            data = urllib.urlopen(url).read()
            thunderPortDetails = json.loads(data)
            devicePort= thunderPortDetails['thunderPort']
        except Exception as e:
            print "Unable to get Thunder Port from REST to trigger the reboot !!!"
            print "Error message received :\n",e;
            result = "FAILURE"

        #Reboot the device
        try:
            cmd = "curl --silent --data-binary '{\"jsonrpc\": \"2.0\", \"id\": 1234567890, \"method\": \"Controller.1.harakiri\" }' -H 'content-type:text/plain;' http://"+ str(obj.IP)+":"+str(devicePort)+ "/jsonrpc"
            os.system(cmd)

            print "WAIT TO COMPLETE THE REBOOT PROCESS"
            time.sleep(150)
        except Exception as e:
            print "ERROR!! \nEXCEPTION OCCURRED WHILE REBOOTING DEVICE!!"
            print "Error message received :\n",e;
            result = "FAILURE"

    if result == "FAILURE" or reboot_required != "Yes":
        print "Device is not rebooted before starting the execution\n"

    return result;

#----------------------------------------------------------------------------
#GET THE STATUS OF DEVICE
#----------------------------------------------------------------------------
def check_device_state(obj):
    #get the resource usage and validate
    print "\nGet CPU and Memory usage"
    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
    tdkTestObj.addParameter("plugin","DeviceInfo")
    tdkTestObj.executeTestCase(expectedResult)
    status = tdkTestObj.getResult()
    result = tdkTestObj.getResultDetails()
    curr_status = result;
    if expectedResult in status:
        if "activated" != result:
            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
            tdkTestObj.addParameter("plugin","DeviceInfo")
            tdkTestObj.addParameter("status","activate")
            tdkTestObj.executeTestCase(expectedResult)
            plugin_status = tdkTestObj.getResult()
            if plugin_status == "SUCCESS":
                print "\nActivated DeviceInfo plugin to get the resource usage details"
                result = "activated"
            else:
                result = "deactivated"
        if result == "activated":
            tdkTestObj = obj.createTestStep('rdkservice_validateResourceUsage')
            tdkTestObj.executeTestCase(expectedResult)
            status = tdkTestObj.getResult()
            result = tdkTestObj.getResultDetails()
            if expectedResult in status and "ERROR" not in result:
                print "\nCPU and Memory usage is within expected range\n"
                result = "SUCCESS"
            elif result == "EXCEPTION OCCURED":
                print "\n Failed to get the resource usage"
            else:
                print "\n CPU and/or Memory usage is higher than expected range\n"
            #Revert DeviceInfo Plugin status
            if curr_status == "deactivated":
                tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
                tdkTestObj.addParameter("plugin","DeviceInfo")
                tdkTestObj.addParameter("status","deactivate")
                tdkTestObj.executeTestCase(expectedResult)
                plugin_status = tdkTestObj.getResult()
                if expectedResult in plugin_status:
                    print "Reverted the plugin status"
                else:
                    print "Unable to revert the plugin status"
                    result = "FAILURE"
        else:
            print "Unable to activate the DeviceInfo plugin"
    else:
        print "Unable to get the status of DeviceInfo plugin"
    time.sleep(5)
    return result;
