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
from pexpect import pxssh
import CertificationSuiteCommonVariables
import requests

def ssh_and_execute(ssh_method, hostname, username, password, command):
    output = ""
    try:
	if (ssh_method == "directSSH"):
            session = pxssh.pxssh(timeout = 2400,options={
                                    "StrictHostKeyChecking": "no",
                                    "UserKnownHostsFile": "/dev/null"})
            print "\nCreating ssh session"
            session.login(hostname,username,password,sync_multiplier=3)
            print "\nExecuting command"
            session.sendline(command)
            session.prompt()
            output = session.before
            print"\nClosing session"
            session.logout()
	else:
	    #TODO
	    print "ssh method other than directSSH is currently not implemented"
	    pass
    except pxssh.ExceptionPxssh as e:
	print "Login to device failed"
    	print e
    return output

def ssh_and_execute_rest(hostname, username, password, command):
    output = ""
    auth_token= ""
    rest_url = ""
    try:
        print "\nFetching config file values for REST api call"
        rest_url = CertificationSuiteCommonVariables.rest_url
        auth_method = CertificationSuiteCommonVariables.auth_method
        if auth_method == "TOKEN":
            auth_token =CertificationSuiteCommonVariables.auth_token
            if auth_token =="" or rest_url == "":
                print "\nPlease configure REST api configurations in device specific config file"
            else:
                headers = {'Content-Type': 'application/json', 'authToken': auth_token,}
                url = str(rest_url.replace("mac",deviceMAC))
                command = command.replace(" grep","grep").replace("|grep",'\|grep').replace("\"","\\\"")
                if "awk" in command:
                    command = command.replace("$","\$")
                command = "\"" + command + "\"";
                response = requests.post(url, headers=headers, data=command, timeout=20)
                print response.content
                output = response.content
                output = command + '\n' + output;
    except Exception as e:
        print "\nLogin to device failed"
        print e
    return output
