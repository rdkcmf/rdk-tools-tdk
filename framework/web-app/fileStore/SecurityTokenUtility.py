##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2022 RDK Management
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
###########################################################################

import os
import json
import ConfigParser
from ConfigParser import SafeConfigParser
from SSHUtility import *


# Method to SSH to the DUT and get the WPE Secutity Token
def get_WPE_ThunderSecurity_Token(deviceIP):
    token  = "None"
    status = "SUCCESS"
    ssh_method = "directSSH"
    host_name  = deviceIP
    user_name  = "root"
    password   = "None"
    command    = "WPEFrameworkSecurityUtility"
    try:
        output = ssh_and_execute(ssh_method,host_name,user_name,password,command)
        if output != "EXCEPTION" and len(output.split('\n')) > 2:
            output = output.split('\n')[1]
            token  = str(json.loads(output).get("token"))
        else:
            status = "FAILURE"
    except Exception as e:
        print "Exception Occurred: ",e
        status = "FAILURE"

    return status,token

# Method to check and create DUT Token config file
def create_token_config(token_config):
    try:
        if not os.path.exists(token_config):
            fd = open(token_config,"w")
            fd.close()
            os.chmod(token_config,0o666)
            print "[INFO]: Created DUT Token Config file"
        if os.path.exists(token_config):
            status = "SUCCESS"
            print "[INFO]: DUT Token Config file available"
        else:
            status = "FAILURE"
            print "[ERROR]: DUT Token config file not available"
    except Exception as e:
        print "Exception Occurred: ",e
        status = "FAILURE"
    return status

# Method to update the token data in DUT Token config file
def update_token_config(deviceIP,token_config):
    status = "SUCCESS"
    try:
        parser = SafeConfigParser()
        parser.read(token_config)
        fd = open(token_config, 'w')
        status,token = get_WPE_ThunderSecurity_Token(deviceIP)
        if status == "SUCCESS":
            if parser.has_section("device_token.config"):
                parser.set("device_token.config","TOKEN",token)
            else:
                parser.add_section("device_token.config")
                parser.set("device_token.config","TOKEN",token)
            parser.write(fd)
            fd.close()
            print "\n[INFO]: Updated Token in DUT Token config file"
        else:
            print "\n[ERROR]: Failed to get Token from the DUT"
            status = "FAILURE"
    except Exception as e:
        print "Exception Occurred: ",e
        status = "FAILURE"
    return status

# Method to check whether DUT Token config file has token info & update
def check_token_config(deviceIP,token_config):
    status = "SUCCESS"
    try:
        parser = SafeConfigParser()
        parser.read(token_config)
        if not parser.has_section("device_token.config"):
            status = update_token_config(deviceIP,token_config)
    except Exception as e:
        print "Exception Occurred: ",e
        status = "FAILURE"
    return status

# Method to read the token form the DUT Token config file
def read_token_config(deviceIP,token_config):
    status = create_token_config(token_config)
    if status == "SUCCESS":
        status = check_token_config(deviceIP,token_config)
        if status == "SUCCESS":
            try:
                parser = SafeConfigParser()
                parser.read(token_config)
                token = parser.get("device_token.config","TOKEN")
            except Exception as e:
                print "Exception Occurred: ",e
                token = "None"
                status = "FAILURE"
        else:
            token = "None"
    else:
        token = "None"
    return status,token


def handleDeviceTokenChange(deviceIP,token_config):
    status = "SUCCESS"
    try:
        status = update_token_config(deviceIP,token_config)
        if status == "SUCCESS":
            status,token = read_token_config(deviceIP,token_config)
            if status == "SUCCESS":
                print "[INFO]: Device token updated successfully !!!"
            else:
                print "[ERROR]: Device token update failed"
        else:
            print "[ERROR]: Device token update failed"
    except Exception as e:
        print "Exception Occurred: ",e
        status = "FAILURE"
        token = "None"
    return status,token
