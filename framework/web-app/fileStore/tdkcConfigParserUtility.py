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

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------
import os
import sys
import ConfigParser
import tdklib

def parseDeviceConfig(obj):

# parseDeviceConfig

# Syntax      : parseDeviceConfig()
# Description : Function to parse the device configuration file
# Parameters  : obj - Object of the tdk library
# Return Value: SUCCESS/FAILURE
    try:
        status = "SUCCESS"

        #Get the device name configured in test manager
        deviceDetails = obj.getDeviceDetails()
        deviceName = deviceDetails["devicename"]
        #Get the device configuration file name
        deviceConfig = deviceName + ".config"

        #Get the current directory path
        configFilePath = os.path.dirname(os.path.realpath(__file__))
        configFilePath = configFilePath + "/tdkcDeviceConfig"

        print "Device config file:", configFilePath+'/'+deviceConfig

        #Parse the device configuration file
        config = ConfigParser.ConfigParser()
        config.read(configFilePath+'/'+deviceConfig)

        #Parse the file and store the values in global variables
        global tdk_path
        tdk_path = config.get(deviceConfig, 'TDK_PATH')

        global ssid
        ssid = config.get(deviceConfig, 'SSID')

        global psk
        psk = config.get(deviceConfig, 'PSK')

    except Exception, e:
        print e;
        status = "Failed to parse the device specific configuration file"
    return status;

