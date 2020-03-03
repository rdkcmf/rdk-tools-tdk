#!/usr/bin/python

##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2018 RDK Management
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
# Methods
#------------------------------------------------------------------------------
import os
import sys
#from pexpect import pxssh
import ConfigParser
import tdklib
from time import sleep
import commands

#Global variable to check whether login session is active
isSessionActive = False

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
        configFilePath = configFilePath + "/tdkvDeviceConfig"

        print "Device config file:", configFilePath+'/'+deviceConfig

        #Parse the device configuration file
        config = ConfigParser.ConfigParser()
        config.read(configFilePath+'/'+deviceConfig)

        #Parse the file and store the values in global variables
        global setup_type
        setup_type = config.get(deviceConfig, 'SETUP_TYPE')

        global ssid_2ghz_name
        ssid_2ghz_name = config.get(deviceConfig, "SSID_2GHZ_NAME")

        global ssid_2ghz_pwd
        ssid_2ghz_pwd = config.get(deviceConfig, "SSID_2GHZ_PWD")

        global ssid_2ghz_invalid_pwd
        ssid_2ghz_invalid_pwd = config.get(deviceConfig, "SSID_2GHZ_INVALID_PWD")

        global ssid_2ghz_index
        global radio_2ghz_index
        global ssid_5ghz_index
        global radio_5ghz_index

        if setup_type == "TDK":
            ssid_2ghz_index = config.get(deviceConfig, "TDK_SSID_2GHZ_INDEX")
            radio_2ghz_index = config.get(deviceConfig, "TDK_RADIO_2GHZ_INDEX")
            ssid_5ghz_index = config.get(deviceConfig, "TDK_SSID_5GHZ_INDEX")
            radio_5ghz_index = config.get(deviceConfig, "TDK_RADIO_5GHZ_INDEX")
        else:
            print "SETUP TYPE IS NOT VALID";
        global ssid_5ghz_name
        ssid_5ghz_name = config.get(deviceConfig, "SSID_5GHZ_NAME")

        global ssid_5ghz_pwd
        ssid_5ghz_pwd = config.get(deviceConfig, "SSID_5GHZ_PWD")

        global ssid_5ghz_invalid_pwd
        ssid_5ghz_invalid_pwd = config.get(deviceConfig, "SSID_5GHZ_INVALID_PWD")

        global wlan_2ghz_ssid_connect_status
        wlan_2ghz_ssid_connect_status = config.get(deviceConfig, "WLAN_2GHZ_SSID_CONNECT_STATUS")

        global wlan_5ghz_ssid_connect_status
        wlan_5ghz_ssid_connect_status = config.get(deviceConfig, "WLAN_5GHZ_SSID_CONNECT_STATUS")

        global wlan_2ghz_ssid_disconnect_status
        wlan_2ghz_ssid_disconnect_status = config.get(deviceConfig, "WLAN_2GHZ_SSID_DISCONNECT_STATUS")

        global wlan_5ghz_ssid_disconnect_status
        wlan_5ghz_ssid_disconnect_status = config.get(deviceConfig, "WLAN_5GHZ_SSID_DISCONNECT_STATUS")

        global ssid_invalid_name
        ssid_invalid_name = config.get(deviceConfig, "SSID_INVALID_NAME")

        global ssid_invalid_pwd
        ssid_invalid_pwd = config.get(deviceConfig, "SSID_INVALID_PWD")

        global ap_5ghz_preshared_key
	ap_5ghz_preshared_key = config.get(deviceConfig, "AP_5GHZ_PRESHARED_KEY")

        global ap_2ghz_preshared_key
	ap_2ghz_preshared_key = config.get(deviceConfig, "AP_2GHZ_PRESHARED_KEY")

	global ap_5ghz_key_passphrase
	ap_5ghz_key_passphrase = config.get(deviceConfig, "AP_5GHZ_KEY_PASSPHRASE")

	global ap_2ghz_key_passphrase
	ap_2ghz_key_passphrase = config.get(deviceConfig, "AP_2GHZ_KEY_PASSPHRASE")

	global ap_5ghz_security_mode 
	ap_5ghz_security_mode = config.get(deviceConfig, "AP_5GHZ_SECURITY_MODE")

	global ap_2ghz_security_mode 
	ap_2ghz_security_mode = config.get(deviceConfig, "AP_2GHZ_SECURITY_MODE")

	global ap_5ghz_wep_key
	ap_5ghz_wep_key = config.get(deviceConfig, "AP_5GHZ_WEP_KEY")

	global ap_2ghz_wep_key
	ap_2ghz_wep_key = config.get(deviceConfig, "AP_2GHZ_WEP_KEY")

        global ssid_5ghz_name_new
        ssid_5ghz_name_new = config.get(deviceConfig, "SSID_5GHZ_NAME_NEW")

        global ssid_2ghz_name_new
        ssid_2ghz_name_new = config.get(deviceConfig, "SSID_2GHZ_NAME_NEW")

        global ssid_5ghz_pwd_new
        ssid_5ghz_pwd_new = config.get(deviceConfig, "SSID_5GHZ_PWD_NEW")

        global ssid_2ghz_pwd_new
        ssid_2ghz_pwd_new = config.get(deviceConfig, "SSID_2GHZ_PWD_NEW")

        global ap_5ghz_preshared_key_new
        ap_5ghz_preshared_key_new = config.get(deviceConfig, "AP_5GHZ_PRESHARED_KEY_NEW")

        global ap_2ghz_preshared_key_new
        ap_2ghz_preshared_key_new = config.get(deviceConfig, "AP_2GHZ_PRESHARED_KEY_NEW")

        global ap_5ghz_key_passphrase_new
        ap_5ghz_key_passphrase_new = config.get(deviceConfig, "AP_5GHZ_KEY_PASSPHRASE_NEW")

        global ap_2ghz_key_passphrase_new
        ap_2ghz_key_passphrase_new = config.get(deviceConfig, "AP_2GHZ_KEY_PASSPHRASE_NEW")

        global ap_5ghz_security_mode_new
        ap_5ghz_security_mode_new = config.get(deviceConfig, "AP_5GHZ_SECURITY_MODE_NEW")

        global ap_2ghz_security_mode_new
        ap_2ghz_security_mode_new = config.get(deviceConfig, "AP_2GHZ_SECURITY_MODE_NEW")

        global ap_5ghz_wep_key_new
        ap_5ghz_wep_key_new = config.get(deviceConfig, "AP_5GHZ_WEP_KEY_NEW")

        global ap_2ghz_wep_key_new
        ap_2ghz_wep_key_new = config.get(deviceConfig, "AP_2GHZ_WEP_KEY_NEW")

	global wifi_interface
	wifi_interface = config.get(deviceConfig, "WIFI_INTERFACE")

        global set_5ghz_freq_list
        set_5ghz_freq_list = config.get(deviceConfig, "SET_5GHZ_FREQ_LIST")

        global set_2ghz_freq_list
        set_2ghz_freq_list = config.get(deviceConfig, "SET_2GHZ_FREQ_LIST")

    except Exception, e:
        print e;
        status = "Failed to parse the device specific configuration file"
    return status;
########## End of Function ##########


def isConnectedtoSSID(obj,radioIndex):
    retValue = "FALSE"
    expectedresult="SUCCESS";
    parseStatus = parseDeviceConfig(obj);
    # Getting current station connection status
    tdkTestObj = obj.createTestStep("WIFI_HAL_GetStats");
    if expectedresult in parseStatus:
        print "==========PARSED THE DEVICE CONFIGURATION FILE SUCCESSFULLY==========";
        tdkTestObj.addParameter("radioIndex",radioIndex);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");
            SSID_GET = details.split(":")[1].split(",")[0].split("=")[1];
            print "==========GET SSID NAME OPERATION SUCCESS==========";
            if radioIndex == 0:
                print "SSID of Current station:",SSID_GET;
                print "SSID to be connected:",ssid_2ghz_name;
                if SSID_GET == ssid_2ghz_name:
                    print "==========CLIENT CONNECTED TO REQUIRED SSID==========";
                    retValue = "TRUE"
            else:
                print "SSID of Current station:",SSID_GET;
                print "SSID to be connected:",ssid_5ghz_name;
                if SSID_GET == ssid_5ghz_name:
                    print "==========CLIENT CONNECTED TO REQUIRED SSID==========";
                    retValue = "TRUE"

            if retValue == "FALSE":
                expectedresult = "SUCCESS";
                print "==========CLIENT IS NOT CONNECTED TO REQUIRED SSID==========";
                print "Connecting to required SSID....."
                tdkTestObj = obj.createTestStep("WIFI_HAL_ConnectEndpoint");
                if radioIndex == 0:
                    tdkTestObj.addParameter("radioIndex",0);
                    tdkTestObj.addParameter("ssid",ssid_2ghz_name);
                    tdkTestObj.addParameter("security_mode",int(ap_2ghz_security_mode));
                    tdkTestObj.addParameter("WEPKey",ap_2ghz_wep_key);
                    tdkTestObj.addParameter("PreSharedKey",ap_2ghz_preshared_key);
                    tdkTestObj.addParameter("KeyPassphrase",ap_2ghz_key_passphrase);
                    tdkTestObj.addParameter("saveSSID",1);

                else:
                    tdkTestObj.addParameter("radioIndex",1);
                    tdkTestObj.addParameter("ssid",ssid_5ghz_name);
                    tdkTestObj.addParameter("security_mode",int(ap_5ghz_security_mode));
                    tdkTestObj.addParameter("WEPKey",ap_5ghz_wep_key);
                    tdkTestObj.addParameter("PreSharedKey",ap_5ghz_preshared_key);
                    tdkTestObj.addParameter("KeyPassphrase",ap_5ghz_key_passphrase);
                    tdkTestObj.addParameter("saveSSID",1);

                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "==========CONNECTION INITIATION SUCCESS==========";
                    # Getting current station connection status after 15 seconds
                    sleep(15);
                    tdkTestObj = obj.createTestStep("WIFI_HAL_GetStats");
                    tdkTestObj.addParameter("radioIndex",radioIndex);
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    if expectedresult in actualresult:
                        SSID_GET = details.split(":")[1].split(",")[0].split("=")[1];
                        print "SSID of Current station:",SSID_GET;
                        if radioIndex == 0 and SSID_GET == ssid_2ghz_name:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "==========CONNECTION SUCCESS==========";
                            retValue = "TRUE"
                        elif radioIndex == 1 and SSID_GET == ssid_5ghz_name:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "==========CONNECTION SUCCESS==========";
                            retValue = "TRUE"
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "==========CONNECTION FAILED==========";
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Get Current Station status operation failed";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "==========CONNECTION INITIATION FAILED==========";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Get Current Station status operation failed";
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "Failed to parse the device configuration file";
    return retValue
########## End of Function ##########

