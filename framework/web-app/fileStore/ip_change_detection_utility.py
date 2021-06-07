##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
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
import time
from rdkv_performancelib import *
from StabilityTestUtility import *
import PerformanceTestVariables
import ast
import rdkv_performancelib
import json
import IPChangeDetectionVariables
import urllib
import sys

# Global variable to store the initial URL in WebKit
current_url = None
# Global variable to store DUT name in TM
device_name = ""

# Function to check the current interface of DUT
def check_current_interface(obj):
    revert = "NO"
    interface = "EMPTY"
    status = "SUCCESS"
    nw_plugin_status_dict = get_plugins_status(obj,["org.rdk.Network"])
    nw_plugin_status = nw_plugin_status_dict["org.rdk.Network"]
    if nw_plugin_status != "activated":
        revert = "YES"
        status = set_plugins_status(obj,{"org.rdk.Network":"activated"})
        nw_plugin_status_dict = get_plugins_status(obj,["org.rdk.Network"])
        nw_plugin_status = nw_plugin_status_dict["org.rdk.Network"]
    if status == "SUCCESS" and nw_plugin_status == "activated":
        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
        tdkTestObj.addParameter("method","org.rdk.Network.1.getDefaultInterface")
        tdkTestObj.addParameter("reqValue","interface")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            interface = tdkTestObj.getResultDetails()
            if interface == "":
                print "\n [Error] Default interface is empty \n"
                tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Default interface of the DUT :\n",interface
                tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "\n Error while executing org.rdk.Network.1.getDefaultInterface method \n"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Unable to activate org.rdk.Network plugin\n"
    return interface,revert

# Function to frame the complete URL of Lightning application from the configuration parameters
def get_lightning_app_url(obj):
    status = "SUCCESS"
    complete_url = ""
    global device_name
    ip_change_app_url = IPChangeDetectionVariables.ip_change_app_url
    device_name = rdkv_performancelib.deviceName
    user_name = IPChangeDetectionVariables.tm_username
    password = IPChangeDetectionVariables.tm_password
    conf_file,file_status = getConfigFileName(obj.realpath)
    ip_address_type_status,ip_address_type = getDeviceConfigKeyValue(conf_file,"DEVICE_IP_ADDRESS_TYPE")
    complete_url = ip_change_app_url+'?tmURL='+obj.url+'&deviceName='+device_name+'&tmUserName='+user_name+'&tmPassword='+password+'&ipAddressType='+ip_address_type
    if any(value == "" for value in (ip_change_app_url,user_name,password,ip_address_type)):
        print "\n Please configure values in IPChangeDetectionVariables and Device specific configuration file \n" 
        status = "FAILURE"
    return status,complete_url

# Function to set the plugins status for launching application and executing test
def set_plugins(obj):
    revert = "NO"
    plugin_status = "SUCCESS"
    plugins_list = ["WebKitBrowser","org.rdk.Wifi"]
    plugin_status_dict = get_plugins_status(obj, plugins_list)
    plugin_status_needed = {"WebKitBrowser":"resumed","org.rdk.Wifi":"activated"}
    if plugin_status_dict != plugin_status_needed:
        revert = "YES"
        plugin_status = set_plugins_status(obj,plugin_status_needed)
        plugin_status_dict2 = get_plugins_status(obj, plugins_list)
        if plugin_status_dict2 != plugin_status_needed:
            plugin_status = "FAILURE"
    return plugin_status,plugin_status_dict,revert

# Function to launch the Lightning App in Webkit
def launch_lightning_app(obj,url):
    expectedResult = "SUCCESS"
    status = "FAILURE"
    global current_url
    print "Load Lightning Application"
    print "\nGet the URL in WebKitBrowser"
    tdkTestObj = obj.createTestStep('rdkservice_getValue');
    tdkTestObj.addParameter("method","WebKitBrowser.1.url");
    tdkTestObj.executeTestCase(expectedResult);
    current_url = tdkTestObj.getResultDetails();
    result = tdkTestObj.getResult();
    if current_url != None and expectedResult in result:
        tdkTestObj.setResultStatus("SUCCESS");
        print "Current URL:",current_url
        tdkTestObj = obj.createTestStep('rdkservice_setValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.addParameter("value",url);
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult();
        if expectedResult in  result:
            time.sleep(10)
            print "\nValidate if the URL is set successfully or not"
            tdkTestObj = obj.createTestStep('rdkservice_getValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.executeTestCase(expectedResult);
            new_url = tdkTestObj.getResultDetails();
            result = tdkTestObj.getResult()
            if new_url == url and expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                print "\n URL(",new_url,") is set successfully \n"
                status = "SUCCESS"
            else:
                print "\n Unable to set URL: {} in WebKitBrowser \n".format(url)
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while executing WebKitBrowser.1.url method \n"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Unable to get the current URL in WebKitBrowser \n"
        tdkTestObj.setResultStatus("FAILURE")
    return status

# Function to get the IP of DUT from TM
def get_curr_device_ip(tm_url):
    url = tm_url + '/deviceGroup/getDeviceDetails?deviceName='+device_name
    try:
        response = urllib.urlopen(url).read()
        deviceDetails = json.loads(response)
        device_ip = deviceDetails["deviceip"]
    except:
        print "Unable to get Device Details from REST !!!"
        exit()
    sys.stdout.flush()
    return device_ip

# Function to enable WIFI interface and set it as default interface
def switch_to_wifi(obj,ap_freq = "2.4",start_time_needed = False):
    status = "FAILURE"
    expectedResult =  "SUCCESS"
    complete_app_url_status,complete_app_url = get_lightning_app_url(obj)
    plugin_status,plugin_status_dict,revert = set_plugins(obj)
    if plugin_status == "SUCCESS" and complete_app_url_status == "SUCCESS":
        tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
        tdkTestObj.addParameter("realpath",obj.realpath)
        tdkTestObj.addParameter("deviceIP",obj.IP)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
        if ssh_param_dict != {} and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            print "\n Enable the RFC Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.PreferredNetworkInterface.Enable in DUT \n"
            #command to enable RFC for PreferredNetworkInterface
            command = "tr181 -s -v true Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.PreferredNetworkInterface.Enable; tr181 Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.PreferredNetworkInterface.Enable"
            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
            tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
            tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
            tdkTestObj.addParameter("command",command)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            output = tdkTestObj.getResultDetails()
            if output != "EXCEPTION" and expectedResult in result:
                if "true" in output.split("\n")[1]:
                    print "\n Enabled RFC feature \n"
                    tdkTestObj.setResultStatus("SUCCESS")
                    #list of interfaces supported by this device including their state
                    tdkTestObj = obj.createTestStep('rdkservice_getValue');
                    tdkTestObj.addParameter("method","org.rdk.Network.1.getInterfaces");
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    interfaces = tdkTestObj.getResultDetails()
                    if expectedResult in result:
                        wifi_interface = False
                        interfaces = ast.literal_eval(interfaces)["interfaces"]
                        for interface in interfaces:
                            if interface["interface"] == "WIFI":
                                wifi_interface = True
                        if wifi_interface:
                            print "\n WiFi interface is present in org.rdk.Network.1.getInterfaces list \n"
                            tdkTestObj.setResultStatus("SUCCESS")
                            params = '{"interface":"WIFI", "enabled":true, "persist":true}'
                            tdkTestObj = obj.createTestStep('rdkservice_setValue');
                            tdkTestObj.addParameter("method","org.rdk.Network.1.setInterfaceEnabled");
                            tdkTestObj.addParameter("value",params);
                            tdkTestObj.executeTestCase(expectedResult);
                            result = tdkTestObj.getResult();
                            if expectedResult in  result:
                                time.sleep(40)
                                tdkTestObj.setResultStatus("SUCCESS")
                                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                                tdkTestObj.addParameter("method","org.rdk.Network.1.getInterfaces");
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                interfaces = tdkTestObj.getResultDetails()
                                if expectedResult in result:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    interfaces = ast.literal_eval(interfaces)["interfaces"]
                                    wifi_dict = {}
                                    for interface in interfaces:
                                        if interface["interface"] == "WIFI":
                                            wifi_dict = interface
                                    if wifi_dict["enabled"]:
                                        app_status = launch_lightning_app(obj,complete_app_url)
                                        if expectedResult in app_status:
                                            time.sleep(40)
                                            wifi_connect_status = connect_wifi(obj,ap_freq)
                                            if expectedResult in wifi_connect_status:
                                                time.sleep(20)
                                                if start_time_needed:
                                                    result,start_time = set_default_interface(obj,"WIFI",start_time_needed)
                                                else:
                                                    result = set_default_interface(obj,"WIFI")
                                                if expectedResult in result:
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                    status = "SUCCESS"
                                                    time.sleep(30)
                                                else:
                                                    print "\n Error while setting WIFI as default interface \n"
                                                    tdkTestObj.setResultStatus("FAILURE")
                                            else:
                                                print "\n Error while connecting to WIFI SSID \n"
                                        else:
                                            print "\n Error while setting URL in WebKitBrowser \n"
                                    else:
                                        print "\n Unable to set WIFI to enabled state \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n Error while executing org.rdk.Network.1.getInterfaces method \n"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Error while executing org.rdk.Network.1.setInterfaceEnabled method \n"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n WIFI is not present in org.rdk.Network.1.getInterfaces output \n"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error while executing org.rdk.Network.1.getInterfaces method \n"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error while enabling RFC for PreferredNetworkInterface\n"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while enabling RFC feature in DUT \n"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Please configure SSH details in Device configuration file \n"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Please check the preconditions before test \n"
    if start_time_needed:
        return status,plugin_status_dict,revert,start_time
    else:
        return status,plugin_status_dict,revert

# Function to connect to a SSID given in the Device configuration file               
def connect_wifi(obj,ap_freq):
    status = "FAILURE"
    conf_file,conf_status = getConfigFileName(obj.realpath)
    if conf_status == "SUCCESS":
        if ap_freq == "2.4":
            ssid_name_key = "WIFI_SSID_NAME"
            password_key = "WIFI_PASSPHRASE"
            security_mode_key = "WIFI_SECURITY_MODE"
        else:
            ssid_name_key = "WIFI_SSID_NAME_5GHZ"
            password_key = "WIFI_PASSPHRASE_5GHZ"
            security_mode_key = "WIFI_SECURITY_MODE_5GHZ"
        result,ssid = getDeviceConfigKeyValue(conf_file,ssid_name_key)
        result,password = getDeviceConfigKeyValue(conf_file,password_key)
        result,security_mode = getDeviceConfigKeyValue(conf_file,security_mode_key)
        if any(value == "" for value in (ssid,password,security_mode)):
            print "please configure values before test"
        else:
            tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
            tdkTestObj.addParameter("method","org.rdk.Wifi.1.getCurrentState")
            tdkTestObj.addParameter("reqValue","state")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if result == "SUCCESS":
                state = int(tdkTestObj.getResultDetails())
                print "\n Current state value of Wifi adapter :{} \n".format(state)
                state_failure = False
                if state not in (0,6):
                    tdkTestObj.setResultStatus("SUCCESS")
                    params = '{"incremental":false,"ssid":"","frequency":""}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.Wifi.1.startScan")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if result == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                        time.sleep(10)
                        print "\n Connecting to SSID : {}\n".format(ssid)
                        params = '{"ssid":"'+ ssid +'", "passphrase": "'+ password +'", "securityMode":'+ security_mode +'}'
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","org.rdk.Wifi.1.connect")
                        tdkTestObj.addParameter("value",params)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        if result == "SUCCESS":
                            tdkTestObj.setResultStatus("SUCCESS")
                            time.sleep(20)
                            device_ip = get_curr_device_ip(obj.url)
                            if obj.IP != device_ip:
                                obj.IP = device_ip
                                time.sleep(50)
                            #check wthether connected
                            print "\n Checking whether DUT is connected to SSID \n"
                            tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
                            tdkTestObj.addParameter("method","org.rdk.Wifi.1.getConnectedSSID")
                            tdkTestObj.addParameter("reqValue","ssid")
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            if result == "SUCCESS":
                                connected_ssid = tdkTestObj.getResultDetails()
                                print " \n Connected SSID Name: {}\n ".format(connected_ssid)
                                if ssid == connected_ssid:
                                    print "Successfully Connected to SSID \n "
                                    status = "SUCCESS"
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print "DUT is not connected to SSID"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Error while executing org.rdk.Wifi.1.getConnectedSSID method \n"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Error while executing org.rdk.Wifi.1.connect method \n"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error while executing org.rdk.Wifi.1.startScan method \n"
                        tdkTestObj.setResultStatus("FAILURE")
                else:               
                    print "\n Wifi adapter is not working \n"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Error while executing org.rdk.Wifi.1.getCurrentState method \n"
                tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Device specific configuration file is missing \n"
    return status

# Function to set default interface
def set_default_interface(obj,interface,start_time_needed = False):
    status = expectedResult = "SUCCESS"
    print "Set {} as default interface".format(interface)
    params = '{ "interface":"'+interface+'", "persist":true}'
    tdkTestObj = obj.createTestStep('rdkservice_setValue');
    tdkTestObj.addParameter("method","org.rdk.Network.1.setDefaultInterface");
    tdkTestObj.addParameter("value",params);
    start_time = str(datetime.utcnow()).split()[1]
    tdkTestObj.executeTestCase(expectedResult);
    result = tdkTestObj.getResult();
    if expectedResult in result:
        print "\n Set default interface method executed successfuly for {} interfce \n".format(interface)
        tdkTestObj.setResultStatus("SUCCESS")
        time.sleep(40)
        device_ip = get_curr_device_ip(obj.url)
        if obj.IP != device_ip:
            obj.IP = device_ip
        new_interface,revert = check_current_interface(obj)
        if interface not in new_interface:
            print "\n Current interface is: {} , unable to set {} interface \n".format(new_interface,interface)
            status = "FAILURE"
    else:
        status = "FAILURE"
        print "\n Unable to set {} as Default interface \n".format(interface)
        tdkTestObj.setResultStatus("FAILURE")
    if start_time_needed:
        return status,start_time
    else:
        return status

# Function to close the Lightning App by setting the initial URL in WebKit
def close_lightning_app(obj):
    expectedResult = "SUCCESS"
    status = "FAILURE"
    tdkTestObj = obj.createTestStep('rdkservice_setValue');
    tdkTestObj.addParameter("method","WebKitBrowser.1.url");
    tdkTestObj.addParameter("value",current_url);
    tdkTestObj.executeTestCase(expectedResult);
    result = tdkTestObj.getResult();
    if expectedResult in  result:
        time.sleep(10)
        print "\nValidate if the URL is set successfully or not"
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        new_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult()
        if new_url == current_url and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            print "URL(",new_url,") is set successfully"
            status = "SUCCESS"
        else:
            print "\n Unable to set URL: {} in WebKitBrowser \n".format(url)
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Error while executing WebKitBrowser.1.url method \n"
        tdkTestObj.setResultStatus("FAILURE")
    return status

def check_cur_ssid_freq(obj):
    return_val = "FAILURE"
    conf_file,conf_status = getConfigFileName(obj.realpath)
    result1,ssid = getDeviceConfigKeyValue(conf_file,"WIFI_SSID_NAME")
    result2,ssid_5ghz = getDeviceConfigKeyValue(conf_file,"WIFI_SSID_NAME_5GHZ")
    if all(value != "" for value in (ssid,ssid_5ghz)):
        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
        tdkTestObj.addParameter("method","org.rdk.Wifi.1.getConnectedSSID")
        tdkTestObj.addParameter("reqValue","ssid")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
            connected_ssid = tdkTestObj.getResultDetails()
            print " \n Connected SSID Name: {}\n ".format(connected_ssid)
            if ssid == connected_ssid:
                return_val = "2.4"
            elif ssid_5ghz == connected_ssid:
                return_val = "5"
            else:
                print "\n DUT is not connected to any of the SSIDs configured in device specific config file \n"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Error while checking connected SSID \n"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Please configure the SSID details in device specific config file\n"
    return return_val
