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

        #global variables for selenium framework
        global start_selenium_script
        start_selenium_script = config.get(deviceConfig,'START_SELENIUM_SCRIPT');

        global start_selenium_script_client
        start_selenium_script_client = config.get(deviceConfig,'START_SELENIUM_SCRIPT_CLIENT');

        global hub_machine_ip
        hub_machine_ip = config.get(deviceConfig,'HUB_MACHINE_IP');

        global hub_logfile
        hub_logfile = config.get(deviceConfig,'HUB_LOGFILE');

        global hub_selenium_path
        hub_selenium_path = config.get(deviceConfig,'HUB_SELENIUM_PATH');

        global node_machine_ip
        node_machine_ip = config.get(deviceConfig,'NODE_MACHINE_IP');

        global node_username
        node_username = config.get(deviceConfig,'NODE_USERNAME');

        global node_password
        node_password = config.get(deviceConfig,'NODE_PASSWORD');

        global node_logfile
        node_logfile = config.get(deviceConfig,'NODE_LOGFILE');

        global node_selenium_path
        node_selenium_path = config.get(deviceConfig,'NODE_SELENIUM_PATH');

        global ersIP
        ersIP  = config.get(deviceConfig,'ERS_IP');

        global ersPort
        ersPort = config.get(deviceConfig,'ERS_PORT');

        global roomName
        roomName  = config.get(deviceConfig,'ROOM_NAME');

        global streamName
        streamName = config.get(deviceConfig,'STREAM_NAME');

        global webrtcDemoURL
        webrtcDemoURL = config.get(deviceConfig,'WEBRTC_DEMO_URL');

        global UICheckXpath
        UICheckXpath = config.get(deviceConfig,'UI_CHECK_XPATH');

        global UICheckData
        UICheckData = config.get(deviceConfig,'UI_CHECK_DATA');

        global debug
        debug = config.get(deviceConfig,'UI_DEBUG_XPATH');

    except Exception, e:
        print e;
        status = "Failed to parse the device specific configuration file"
    return status;

