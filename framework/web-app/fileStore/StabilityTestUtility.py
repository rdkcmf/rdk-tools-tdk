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
            if validation_dict["ssh_method"] == "directSSH":
                validation_dict["host_name"] = obj.IP
                result,validation_dict["user_name"] = getDeviceConfigKeyValue(conf_file,"SSH_USERNAME")
                result,validation_dict["password"] = getDeviceConfigKeyValue(conf_file,"SSH_PASSWORD")
            else:
                #TODO
                print "selected ssh method is {}".format(validation_dict["ssh_method"])
                pass
            result,validation_dict["validation_method"] = getDeviceConfigKeyValue(conf_file,"VALIDATION_METHOD")
            result,validation_dict["validation_file"] = getDeviceConfigKeyValue(conf_file,"VIDEO_PROC_FILE")
            result,validation_dict["min_cdb"] = getDeviceConfigKeyValue(conf_file,"MIN_CDB")
    else:
        print "Failed to get the validation required value from config file, please configure values before test"
    if any(value == "" for value in validation_dict.itervalues()):
        print "please configure values before test"
        validation_dict = {}
    return validation_dict
