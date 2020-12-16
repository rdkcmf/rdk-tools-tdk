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

def get_ssh_params(obj):
    ssh_dict = {}
    print "\n getting ssh params from conf file"
    conf_file,result = getConfigFileName(obj.realpath)
    if result == "SUCCESS":
        result,ssh_dict["ssh_method"] = getDeviceConfigKeyValue(conf_file,"SSH_METHOD")
        if ssh_dict["ssh_method"] == "directSSH":
            ssh_dict["host_name"] = obj.IP
            result,ssh_dict["user_name"] = getDeviceConfigKeyValue(conf_file,"SSH_USERNAME")
	    result,ssh_dict["password"] = getDeviceConfigKeyValue(conf_file,"SSH_PASSWORD")
        else:
            #TODO
	    print "selected ssh method is {}".format(ssh_dict["ssh_method"])
            pass
    else:
        print "Failed to find the device specific config file"
    if any(value == "" for value in ssh_dict.itervalues()):
	print "please configure values before test"
	ssh_dict = {}
    return ssh_dict
