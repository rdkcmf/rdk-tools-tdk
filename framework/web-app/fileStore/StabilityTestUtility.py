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
