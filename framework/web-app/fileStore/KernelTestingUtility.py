##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2023 RDK Management
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
import os
import ConfigParser
import tdklib
from SSHUtility import *
def executeTestCommand(sshinfo,command):
    output = ""
    status = "SUCCESS"
    sshmethod = sshinfo[0]
    if sshmethod == "directSSH":
        host_name = sshinfo[1]
        user_name = sshinfo[2]
        password  = sshinfo[3]
    else:
        #TODO
        print "Secure ssh to CPE"
        pass
    try:
        output = ssh_and_execute (sshmethod, host_name, user_name, password, command)
        print("Kernel testing command execution success\n")
    except Exception as e:
        print e
        status = "FAILURE"
        print "Exception occured during ssh session"
        print("Kernel testing command execution failed\n")
    return status,output
def executeTestCommandUsingTDKAgent(tdkTestObj,command):
    output = ""
    expectedResult = "SUCCESS"
    tdkTestObj.addParameter("command", command)
    tdkTestObj.executeTestCase(expectedResult)
    actualresult = tdkTestObj.getResult()
    if expectedResult in actualresult.upper():
        output = tdkTestObj.getResultDetails()
        tdkTestObj.setResultStatus("SUCCESS")
        print("Kernel testing command execution success\n")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("Kernel testing command execution failed\n")
    return actualresult,output
def getLTPTestStatusAndSummary(output):
    test_status=""
    test_result=""
    if output != "":
        print "=================== Test Summary ===================="
        output = output.replace(r'\n',"\n").split("\n")
        for info in output:
            print(info)
            if "Status" in info:
                test_result=info.split(":")[1]
        if "PASSED" in test_result:
            test_status="SUCCESS"
        else:
            test_status="FAILURE"
    return test_status
#Function to retrieve the device configuration from device config file
def getDeviceConfigValue (tdklibObj, configKey):
    try:
        #Retrieve the device details(device name) and device type from tdk library
        result = "SUCCESS"
        configValue = ""
        deviceDetails = tdklibObj.getDeviceDetails()
        deviceType = tdklibObj.getDeviceBoxType()
        #Construct the tdkvRDKServiceConfig path in TM
        configPath = tdklibObj.realpath+ "/" + "fileStore/tdkvRDKServiceConfig"
        #Construct the device configuration file path
        #The device configuration file can be either <device-name>.config or <box-type>.config, so we are checking for both
        deviceNameConfigFile = configPath + "/" + deviceDetails["devicename"] + ".config"
        deviceTypeConfigFile = configPath + "/" + deviceType + ".config"
        # Check whether device / platform config files are present
        if os.path.exists (deviceNameConfigFile) == True:
            deviceConfigFile = deviceNameConfigFile
        elif os.path.exists (deviceTypeConfigFile) == True:
            deviceConfigFile = deviceTypeConfigFile
        else:
            print "FAILURE : No Device config file found : " + deviceNameConfigFile + " or " + deviceTypeConfigFile
            result = "FAILURE"
        #Continue only if the device config file exists
        if (len (deviceConfigFile) != 0):
            configParser = ConfigParser.ConfigParser()
            configParser.read(r'%s' % deviceConfigFile)
            #Retrieve the value of config key from device config file
            configValue = configParser.get('device.config', configKey)
        else:
            print "DeviceConfig file not available"
            result = "FAILURE"
    except Exception as e:
        print e
        print "Exception occurred while retrieving device configuration"
        result = "FAILURE"
    return result, configValue
def getSSHInfo(obj,ip):
    sshinfo = []
    status = "SUCCESS"
    status1,sshmethod=getDeviceConfigValue(obj,"SSH_METHOD")
    status2,user     =getDeviceConfigValue(obj,"SSH_USERNAME")
    status3,password =getDeviceConfigValue(obj,"SSH_PASSWORD")
    if status1 == "SUCCESS" and status2 == "SUCCESS" and status3 == "SUCCESS":
        sshinfo = [sshmethod,ip,user,password]
    else:
        status = "FAILURE"
        print "Plz check the device ssh configurations"
    return status,sshinfo

