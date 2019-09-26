##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
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
#

#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import os
import sys
import time
import signal
import subprocess
import tdklib
import pipes
import urllib
import json
from tdkbVariables import *;

def getDeviceBoxType(self):

        # Create an object for getDeviceBoxType

        # Syntax      : OBJ.getDeviceBoxType()
        # Description : Create an object of Device Box Type
        # Parameters  : None
        # Return Value: Return the box type

                 url = self.url + '/deviceGroup/getDeviceBoxType?deviceIp='+self.ip
                 response = urllib.urlopen(url).read()
                 if 'SUCCESS' in response:
                        boxType = json.loads(response)
                 else:
                        print "#TDK_@error-ERROR : Unable to get Device Box Type from REST !!!"
                        exit()

                 sys.stdout.flush()
                 return boxType['boxtype']

        ########## End of Function ##########

def SnmpExecuteCmd(snmpMethod,communityString,snmpVersion,OID,ipAddress):

        # To invoke and fetch status of SNMP command for a particular box

        # Parameters   : SnmpMethod, SnmpVersion, OID, IP_Address
        # snmpMethod   : Method name. e.g., snmpget, snmpset, snmpwalk etc.,
        # communityString : Community String to be used for SNMP Get/Set
        # snmpVersion  : Version of snmp
        # OID          : Object ID
        # ipAddress   : IP address of the device
        # Return Value : Console output of the snmp command

        if "." in ipAddress:
                cmd=snmpMethod + ' ' + snmpVersion + ' -c ' + communityString + ' ' + ipAddress + ' ' +  OID
        else:
                cmd=snmpMethod + ' -c ' + communityString + ' ' + snmpVersion + ' udp6:['+ ipAddress + '] ' + OID

        class Timout(Exception):
                pass
        def timeoutHandler(signum, frame):
                raise Timout
        signal.signal(signal.SIGALRM, timeoutHandler)
        signal.alarm(20)

        # Executing request command
        try:
                print "SNMP Request:\"",cmd," \""
                sys.stdout.flush()
                snmpResponse = subprocess.check_output(cmd, shell=True)
                print "SNMP Response: ",snmpResponse;
                snmpResponse = snmpResponse.replace("<<", "")
                snmpResponse = snmpResponse.replace(">>", "")
                snmpResponse = unicode(snmpResponse, errors='ignore')
                signal.alarm(0)  # reset the alarm
        except Timout:
                print "Timeout!! Taking too long"
                snmpError = "ERROR: Timeout!! Taking too long"
                sys.stdout.flush()
                signal.alarm(0)  # reset the alarm
                return snmpError
        except:
                print "Unable to execute snmp command"
                snmpError = "ERROR: Unable to execute snmp command"
                sys.stdout.flush()
                signal.alarm(0)  # reset the alarm
                return snmpError

        return snmpResponse

        ########## End of Function ##########


def getCommunityString(obj,method):

        # Create an object for getCommunityString

        # Syntax      : OBJ.getCommunityString()
        # Description : Get the Community string for SNMP
        # Parameters  : method - GET/SET
        # Return Value: Return the commmunity string

        if method == "snmpget":
                cmd="sh %s/tdk_utility.sh parseConfigFile SNMPGET_COMMUNITY_STRING" %TDK_PATH
                print "Request for Community String,GET:", cmd
        else:
                cmd="sh %s/tdk_utility.sh parseConfigFile SNMPSET_COMMUNITY_STRING" %TDK_PATH
                print "Request for Community String,SET:", cmd

        tdkTestObj = obj.createTestStep('ExecuteCmd');
        tdkTestObj.addParameter("command", cmd)
        tdkTestObj.executeTestCase("SUCCESS");
        communityString = tdkTestObj.getResultDetails();
        communityString = communityString.replace("\\n", "");
        print "communityString:", communityString

        return communityString;

        ########## End of Function ##########

def getIPAddress(obj):

        # Create an object for getIPAddress

        # Syntax      : OBJ.getIPAddress()
        # Description : Get the IP Address for SNMP
        # Parameters  : sysObj - Object for the module loaded
        # Return Value: Return the IP Address

        cmd="sh %s/tdk_platform_utility.sh getCMIPAddress" %TDK_PATH
        print "Request for IP Address:", cmd
        tdkTestObj = obj.createTestStep('ExecuteCmd');
        tdkTestObj.addParameter("command", cmd)
        tdkTestObj.executeTestCase("SUCCESS");
        ipAddress = tdkTestObj.getResultDetails();
        ipAddress = ipAddress.replace("\\n", "");
        print "IP Address:", ipAddress
        return ipAddress;

        ########## End of Function ##########

def getMACAddress(obj):

        # Create an object for getMACAddress

        # Syntax      : OBJ.getMACAddress()
        # Description : Get the MAC Address for SNMP
        # Parameters  : sysObj - Object for the module loaded
        # Return Value: Return the MAC Address

        cmd="sh %s/tdk_platform_utility.sh getCMMACAddress" %TDK_PATH
        print "Request for CM MAC Address:", cmd
        tdkTestObj = obj.createTestStep('ExecuteCmd');
        tdkTestObj.addParameter("command", cmd)
        tdkTestObj.executeTestCase("SUCCESS");
        MACAddress = tdkTestObj.getResultDetails();
        MACAddress = MACAddress.replace("\\n", "");
        print "MAC Address:", MACAddress
        return MACAddress;

        ########## End of Function ##########
