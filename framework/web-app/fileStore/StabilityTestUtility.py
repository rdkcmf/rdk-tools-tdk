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
from performancelib import *
import ast

expectedResult ="SUCCESS"


def get_plugins_status(obj,plugins):
	cur_plugin_state_dict = {}
	for plugin in plugins:
		plugin_obj = obj.createTestStep('rdkservice_getPluginStatus')
                plugin_obj.addParameter("plugin",plugin)
		plugin_obj.executeTestCase(expectedResult)
		cur_plugin_state_dict[plugin] = plugin_obj.getResultDetails()
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
                    if plugins_state_dict[plugin] == "resumed":
                        print "{} resuming".format(plugin)
                        tdkTestObj = obj.createTestStep('rdkservice_setPluginState')
                        tdkTestObj.addParameter("plugin",plugin)
                        tdkTestObj.addParameter("state","resumed")
                        tdkTestObj.executeTestCase(expectedResult)
                        plugin_status = tdkTestObj.getResult()
            elif plugins_state_dict[plugin] == "deactivated":
                print "{} disabling".format(plugin)
                tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
                tdkTestObj.addParameter("plugin",plugin)
                tdkTestObj.addParameter("status","deactivate")
                tdkTestObj.executeTestCase(expectedResult)
                plugin_status = tdkTestObj.getResult()
	    plugin_status_list.append(plugin_status)
	if all(status == "SUCCESS" for status in plugin_status_list):
		tdkTestObj.setResultStatus("SUCCESS")
        	return "SUCCESS"
   	else:
        	tdkTestObj.setResultStatus("FAILURE")
        	return "FAILURE"

def launch_cobalt(obj):
	return_val = "SUCCESS"
	print "\n launch cobalt using rdkshell"
    	params = '{"callsign": "Cobalt", "type":"", "uri":"", "x":0, "y":0, "w":1920, "h":1080}'
        tdkTestObj = obj.createTestStep('rdkservice_setValue')
        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.launch")
        tdkTestObj.addParameter("value",params)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
	    print "\n checking playback is happening in forground"
            tdkTestObj = obj.createTestStep('rdkservice_getValue')
            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder")
            tdkTestObj.executeTestCase(expectedResult)
            zorder = tdkTestObj.getResultDetails()
	    result = tdkTestObj.getResult()
	    if result == "SUCCESS":
		tdkTestObj.setResultStatus("SUCCESS")
                zorder = ast.literal_eval(zorder)["clients"]
		eorder.append("cobalt")
                if zorder[0] != "cobalt":
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
		    print "\n Cobalt is playing in the foreground"
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
	result, validation_dict["memory_max_limit"] = getDeviceConfigKeyValue(conf_file,"MAX_MEMORY_VALUE")
        result, validation_required = getDeviceConfigKeyValue(conf_file,"VALIDATION_REQ")
        if result == "SUCCESS":
            if validation_required == "NO":
                validation_dict["validation_required"] = False
            else:
                validation_dict["validation_required"] = True
                result,validation_dict["ssh_method"] = getDeviceConfigKeyValue(conf_file,"SSH_METHOD")
                if validation_dict["ssh_method"] == "directSSH":
          	    result,validation_dict["host_name"] = getDeviceConfigKeyValue(conf_file,"SSH_IP")
                    result,validation_dict["user_name"] = getDeviceConfigKeyValue(conf_file,"SSH_USERNAME")
		    result,validation_dict["password"] = getDeviceConfigKeyValue(conf_file,"SSH_PASSWORD")
                else:
                    #TODO
		    print "selected ssh method is {}".format(validation_dict["ssh_method"])
                    pass
                result,validation_dict["validation_method"] = getDeviceConfigKeyValue(conf_file,"VALIDATION_METHOD")
                result,validation_dict["validation_file"] = getDeviceConfigKeyValue(conf_file,"VALIDATION_FILE")
		result,validation_dict["min_cdb"] = getDeviceConfigKeyValue(conf_file,"MIN_CDB")
        else:
            print "Failed to get the validation required value from config file, please configure values before test"
	if any(value == "" for value in validation_dict.itervalues()):
	    print "please configure values before test"
	    validation_dict = {}
	return validation_dict
