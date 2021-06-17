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
import os
import inspect
import importlib
import ConfigParser
import MediaValidationVariables
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions
from rdkv_performancelib import getDeviceConfigKeyValue
from SSHUtility import *

deviceIP=""
devicePort=""
deviceName=""
deviceType=""

#METHODS
#---------------------------------------------------------------
#INITIALIZE THE MODULE
#---------------------------------------------------------------
def init_module(libobj,port,deviceInfo):
    global deviceIP
    global devicePort
    global deviceName
    global deviceType
    deviceIP = libobj.ip;
    devicePort = port
    deviceName = deviceInfo["devicename"]
    deviceType = deviceInfo["boxtype"]


def rdkv_media_pre_requisites():
    return "SUCCESS"
def rdkv_media_test():
    return "SUCCESS"
def rdkv_media_post_requisites():
    return "SUCCESS"

#----------------------------------------------------------------------
#GET THE NAME OF DEVICE CONFIG FILE
#----------------------------------------------------------------------
def getDeviceConfigFile(basePath):
    deviceConfigFile=""
    status ="SUCCESS"
    configPath = basePath + "/"   + "fileStore/tdkvRDKServiceConfig"
    deviceNameConfigFile = configPath + "/" + deviceName + ".config"
    deviceTypeConfigFile = configPath + "/" + deviceType + ".config"
    # Check whether device / platform config files required for
    # executing the test are present
    if os.path.exists(deviceNameConfigFile) == True:
        deviceConfigFile = deviceNameConfigFile
        print "[INFO]: Using Device config file: %s" %(deviceNameConfigFile)
    elif os.path.exists(deviceTypeConfigFile) == True:
        deviceConfigFile = deviceTypeConfigFile
        print "[INFO]: Using Device config file: %s" %(deviceTypeConfigFile)
    else:
        status = "FAILURE"
        print "[ERROR]: No Device config file found : %s or %s" %(deviceNameConfigFile,deviceTypeConfigFile)
    return deviceConfigFile,status;


#-------------------------------------------------------------------
# Function to read the proc validation parameters from device config file
#-------------------------------------------------------------------
def rdkv_media_getProcCheckInfo(realpath):
    validation_dict = {}
    print "\n Reading proc validation params from conf file..."
    conf_file,result = getDeviceConfigFile(realpath)
    result, proc_check = getDeviceConfigKeyValue(conf_file,"VALIDATION_REQ")
    if result == "SUCCESS":
        if proc_check == "NO":
            validation_dict["proc_check"] = False
        else:
            validation_dict["proc_check"] = True
            result,validation_dict["ssh_method"]    = getDeviceConfigKeyValue(conf_file,"SSH_METHOD")
            validation_dict["host_name"] = deviceIP
            result,validation_dict["user_name"] = getDeviceConfigKeyValue(conf_file,"SSH_USERNAME")
            result,validation_dict["password"]  = getDeviceConfigKeyValue(conf_file,"SSH_PASSWORD")
            result,validation_dict["validation_script"] = getDeviceConfigKeyValue(conf_file,"VIDEO_VALIDATION_SCRIPT_FILE")
            if validation_dict["password"] == "None":
                password = ""
            else:
                password = validation_dict["password"]
            credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
            validation_dict["credentials"] = credentials
    else:
        print "Failed to get the validation parameters from config file, please configure values before test"
    if any(value == "" for value in validation_dict.itervalues()):
        print "please configure validation parameters before test"
        validation_dict = {}
    return validation_dict


#-------------------------------------------------------------------
# Function to check required pattern in proc entry file
#-------------------------------------------------------------------
def rdkv_media_checkProcEntry(sshMethod,credentials,validation_script):
    result = "FAILURE"
    validation_script = validation_script.split('.py')[0]
    try:
        lib = importlib.import_module(validation_script)
        method = "check_video_status"
        method_to_call = getattr(lib, method)
        result = method_to_call(sshMethod,credentials)
    except Exception as e:
        print "[ERROR]: Failed to import video validation script file, please check the configuration"
        result = "FAILURE"
    finally:
        return result


#-------------------------------------------------------------------
#SET WEBDRIVER AND OPEN CHROME BROWSER
#-------------------------------------------------------------------
def openChromeBrowser(url):
   #https://askubuntu.com/questions/432255/what-is-the-display-environment-variable
   os.environ["DISPLAY"] = MediaValidationVariables.display_variable;
   os.environ["PATH"] += MediaValidationVariables.path_of_browser_executable;
   try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(chrome_options=chrome_options) #Opening Chrome
        driver.get(url);
   except Exception as error:
        print "Got exception while opening the browser"
        print error
        driver = "EXCEPTION OCCURRED"
   return driver;

#-------------------------------------------------------------------
#GET THE DATA FROM UI
#-------------------------------------------------------------------
def rdkv_media_readUIData(elementExpandXpath,dataXpath,count):
   try:
        webinspectURL = 'http://' + deviceIP + ':' + MediaValidationVariables.webinspect_port + '/Main.html?page=1'
        print "url:",webinspectURL
        driver = openChromeBrowser(webinspectURL);
        if driver != "EXCEPTION OCCURRED":
            time.sleep(10)
            action = ActionChains(driver)
            source = driver.find_element_by_xpath(elementExpandXpath)
            time.sleep(3)
            action.move_to_element(source).context_click().perform()
            time.sleep(10)
            options = driver.find_elements_by_class_name('soft-context-menu')
            time.sleep(3)
            try:
                for option in options:
                    current_option = option.find_elements_by_class_name('item')
                    time.sleep(3)
                    for item in current_option:
                        if "Expand All" in item.text:
                            item.click()
            except exceptions.StaleElementReferenceException,e:
                pass
            time.sleep(10)
            ui_data_list = []
            for i in range(0,count):
                ui_data = driver.find_element_by_xpath(dataXpath).text
                if ui_data != None and str(ui_data).strip() != "":
                    ui_data_list.append(str(ui_data))
                time.sleep(2)
            ui_data_list = [ x for x in ui_data_list if x != None ]
            ui_data = str(",".join(ui_data_list))
            print "\n Data read from web UI: ",ui_data
            time.sleep(5)
            driver.quit()
        else:
            ui_data = "Unable to get the data from the web UI"
   except Exception as error:
        print "Got exception while getting the data from the web UI"
        print error
        ui_data = "Unable to get the data from the web UI"
        driver.quit()
   return ui_data




