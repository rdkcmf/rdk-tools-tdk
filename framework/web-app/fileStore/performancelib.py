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
import requests
import json
import time
import os
import inspect
import ConfigParser
import BrowserPerformanceVariables
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions

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

#---------------------------------------------------------------
#EXECUTE CURL REQUESTS
#---------------------------------------------------------------
def execute_step(data):
    data = '{"jsonrpc": "2.0", "id": 1234567890, '+data+'}'
    headers = {'content-type': 'text/plain;',}
    url = 'http://'+str(deviceIP)+':'+str(devicePort)+'/jsonrpc'
    try:
        response = requests.post(url, headers=headers, data=data, timeout=20)
        json_response = json.loads(response.content)
        return json_response.get("result");
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

#-----------------------------------------------------------------
#GET PLUGIN STATUS
#-----------------------------------------------------------------
def rdkservice_getPluginStatus(plugin):
    data = '"method": "Controller.1.status@'+plugin+'"'
    result = execute_step(data)
    if result != None:
        for x in result:
            WebKitStatus=x["state"]
        return WebKitStatus
    else:
        return "None"

#-----------------------------------------------------------------
#GET THE STATUS OF ALL PLUGIN
#-----------------------------------------------------------------
def rdkservice_getAllPluginStatus():
    statusofPlugin=[];
    data = '"method": "Controller.1.status"'
    result = execute_step(data)
    for x in result:
        plugin = x["callsign"]
        state = x["state"]
        if "autostart" in x.keys():
            autostart = x["autostart"]
        else:
            autostart = "null"
        statusofPlugin.append([plugin,state,autostart]);
    return statusofPlugin;

#------------------------------------------------------------------
#SET PLUGIN STATUS
#------------------------------------------------------------------
def rdkservice_setPluginStatus(plugin,status):
    data = '"method": "Controller.1.'+status+'", "params": {"callsign": "'+plugin+'"}'
    result = execute_step(data)
    return result

#-------------------------------------------------------------------
#CHANGE STATE OF PLUGIN
#-------------------------------------------------------------------
def rdkservice_setPluginState(plugin,state):
    data = '"method": "'+plugin+'.1.state","params": "'+state+'"'
    result = execute_step(data)
    return result

#-------------------------------------------------------------------
#GET THE VALUE OF A METHOD
#-------------------------------------------------------------------
def rdkservice_getValue(method):
    data = '"method": "'+method+'"'
    result = execute_step(data)
    return result

#-------------------------------------------------------------------
#GET THE REQUIRED VALUE FROM A RESULT
#-------------------------------------------------------------------
def rdkservice_getReqValueFromResult(method,reqValue):
    data = '"method": "'+method+'"'
    result = execute_step(data)
    value = result[reqValue]
    return value
#------------------------------------------------------------------
#SET VALUE FOR A METHOD
#------------------------------------------------------------------
def rdkservice_setValue(method,value):
    data = '"method": "'+method+'","params": "'+value+'"'
    print data
    result = execute_step(data)
    return result

#------------------------------------------------------------------
#GET THE NUMBER OF PLUGINS
#------------------------------------------------------------------
def rdkservice_getNoOfPlugins():
    status = rdkservice_getAllPluginStatus();
    NoofPlugins = len(status)
    return  NoofPlugins;

#------------------------------------------------------------------
#REBOOT THE DEVICE
#------------------------------------------------------------------
def rdkservice_rebootDevice(waitTime):
    cmd = "curl --silent --data-binary '{\"jsonrpc\": \"2.0\", \"id\": 1234567890, \"method\": \"Controller.1.harakiri\" }' -H 'content-type:text/plain;' http://"+ str(deviceIP)+":"+str(devicePort)+ "/jsonrpc"
    os.system(cmd)

    print "WAIT TO COMPLETE THE REBOOT PROCESS"
    time.sleep(waitTime)
    return "SUCCESS"

#-------------------------------------------------------------------
#SET WEBDRIVER AND OPEN CHROME BROWSER
#-------------------------------------------------------------------
def openChromeBrowser(url):
   #https://askubuntu.com/questions/432255/what-is-the-display-environment-variable
   os.environ["DISPLAY"] = BrowserPerformanceVariables.display_variable;
   os.environ["PATH"] += BrowserPerformanceVariables.path_of_browser_executable;
   try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(chrome_options=chrome_options) #Opening Chrome
        driver.get(url);
   except Exception as error:
        print "Got exception while opening the browser"
        print error
   return driver;

#-------------------------------------------------------------------
#GET THE BROWSER SCORE FROM CSS3 TEST
#-------------------------------------------------------------------
def rdkservice_getBrowserScore_CSS3():
   try:
        webinspectURL = 'http://'+deviceIP+':'+BrowserPerformanceVariables.webinspect_port+'/Main.html?page=1'
        driver = openChromeBrowser(webinspectURL);
        time.sleep(10)
        action = ActionChains(driver)
        source = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/li[2]/span/span[1]/span[2]/span[2]')
        action.move_to_element(source).context_click().perform()
        time.sleep(10)
        options = driver.find_elements_by_class_name('soft-context-menu')
        try:
            for option in options:
                current_option = option.find_elements_by_class_name('item')
                for item in current_option:
                    if "Expand All" in item.text:
                        item.click()
        except exceptions.StaleElementReferenceException,e:
            pass
        time.sleep(10)
        browser_score= driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol/ol/ol/li[2]/span/span[2]').text
        time.sleep(5)
        driver.quit()
   except Exception as error:
        print "Got exception while getting the browser score"
        print error
        browser_score = "Unable to get the browser score"
        driver.quit()
   return browser_score;

#-------------------------------------------------------------------
#GET THE BROWSER SCORE FROM OCTANE TEST
#-------------------------------------------------------------------
def rdkservice_getBrowserScore_Octane():
   try:
        webinspectURL = 'http://'+deviceIP+':'+BrowserPerformanceVariables.webinspect_port+'/Main.html?page=1'
        driver = openChromeBrowser(webinspectURL);
        time.sleep(10)
        action = ActionChains(driver)
        source = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/li[2]')
        action.move_to_element(source).context_click().perform()
        time.sleep(10)
        options = driver.find_elements_by_class_name('soft-context-menu')
        try:
            for option in options:
                current_option = option.find_elements_by_class_name('item')
                for item in current_option:
                    if "Expand All" in item.text:
                        item.click()
        except exceptions.StaleElementReferenceException,e:
            pass
        time.sleep(10)
        browser_score= driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol/ol/ol/li[1]/span/span[2]').text
        time.sleep(5)
        driver.quit()
   except Exception as error:
        print "Got exception while getting the browser score"
        print error
        browser_score = "Unable to get the browser score"
        driver.quit()
   return browser_score;

#----------------------------------------------------------------------
#GET THE NAME OF DEVICE CONFIG FILE
#----------------------------------------------------------------------
def getConfigFileName(basePath):
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

#-------------------------------------------------------------------------
#GET THE VALUES FROM DEVICE CONFIG FILE
#-------------------------------------------------------------------------
def getDeviceConfigKeyValue(deviceConfigFile,key):
    value  = ""
    status = "SUCCESS"
    deviceConfig  = "device.config"
    try:
        # If the key is none object or empty then exception
        # will be thrown
        if key is None or key == "":
            status = "FAILURE"
            print "\nException Occurred: [%s] key is None or empty" %(inspect.stack()[0][3])
        # Parse the device configuration file and read the
        # data. But if the data is empty it is taken as such
        else:
            config = ConfigParser.ConfigParser()
            config.read(deviceConfigFile)
            value = str(config.get(deviceConfig,key))
    except Exception as e:
        status = "FAILURE"
        print "\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e)

    return status,value
