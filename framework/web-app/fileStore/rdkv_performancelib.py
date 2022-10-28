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
from SSHUtility import *
import SSHUtility
import re
from datetime import datetime
import importlib
import PerformanceTestVariables
import sys
import socket
import ast
import urllib 
from SecurityTokenUtility import *
import web_socket_util

deviceIP=""
devicePort=""
deviceName=""
deviceType=""
deviceMac=""
realpath=""
securityEnabled=False
deviceToken=""

graphical_plugins_list = PerformanceTestVariables.graphical_plugins_list
excluded_process_list = PerformanceTestVariables.excluded_process_list
#METHODS
#---------------------------------------------------------------
#INITIALIZE THE MODULE
#---------------------------------------------------------------
def init_module(libobj,port,deviceInfo):
    global deviceIP
    global devicePort
    global deviceName
    global deviceType
    global libObj
    global realpath
    global deviceMac
    deviceIP = libobj.ip;
    devicePort = port
    deviceName = deviceInfo["devicename"]
    deviceType = deviceInfo["boxtype"]
    libObj = libobj
    try:
        deviceMac = deviceInfo["mac"]
        SSHUtility.deviceMAC = deviceMac
        SSHUtility.realpath = libobj.realpath
    except Exception as e:
       print "\nException Occurred while getting MAC \n"
       print e

#---------------------------------------------------------------
#POST CURL REQUEST USING PYTHON REQUESTS
#---------------------------------------------------------------
def postCURLRequest(data,securityEnabled):
    status = "SUCCESS"
    json_response={}
    if securityEnabled:
        Bearer = 'Bearer ' + deviceToken
        headers = {'content-type': 'text/plain;',"Authorization":Bearer}
    else:
        headers = {'content-type': 'text/plain;',}
    url = 'http://'+str(deviceIP)+':'+str(devicePort)+'/jsonrpc'
    try:
        response = requests.post(url, headers=headers, data=data, timeout=20)
        json_response = json.loads(response.content)
        if json_response.get("error") != None and "Missing or invalid token" in json_response.get("error").get("message"):
            status = "INVALID TOKEN"
    except requests.exceptions.RequestException as e:
        status = "FAILURE"
        print "ERROR!! \nEXCEPTION OCCURRED WHILE EXECUTING CURL COMMANDS!!"
        print "Command : ",data
        print "Error message received :\n",e;
        response = "EXCEPTION OCCURRED"
    return response,json_response,status

#---------------------------------------------------------------
#EXECUTE CURL REQUESTS
#---------------------------------------------------------------
def execute_step(Data):
    status = "SUCCESS"
    global securityEnabled
    try:
        data = '{"jsonrpc": "2.0", "id": 1234567890, '+Data+'}'
        response,json_response,status = postCURLRequest(data,securityEnabled)
        if status == "INVALID TOKEN":
           print "\nAuthorization issue occurred. Update Token & Re-try..."
           global deviceToken
           tokenFile = libObj.realpath + "/" + "fileStore/tdkvRDKServiceConfig/tokenConfig/" + deviceName + ".config"
           if not securityEnabled:
               # Create the Device Token config file and update the token
               token_status,deviceToken = read_token_config(deviceIP,tokenFile)
               if token_status == "SUCCESS":
                   print "\nDevice Security Token obtained successfully"
               else:
                   print "\nFailed to get the device security token"
               securityEnabled = True
           else:
               # Update the token in the device token config file
               token_status,deviceToken  = handleDeviceTokenChange(deviceIP,tokenFile)
           if token_status == "SUCCESS":
               response,json_response,status = postCURLRequest(data,securityEnabled)
           else:
               print "\nFailed to update the token in token config file"
           if status == "INVALID TOKEN":
               token_status,deviceToken  = handleDeviceTokenChange(deviceIP,tokenFile)
               if token_status=="SUCCESS":
                   response,json_response,status = postCURLRequest(data,securityEnabled)
               else:
                   status = "FAILURE"
        web_socket_util.deviceToken = deviceToken
        if status == "SUCCESS":
            print "\n---------------------------------------------------------------------------------------------------"
            print "Json command : ", data
            print "\n Response : ", json_response, "\n"
            print "----------------------------------------------------------------------------------------------------\n"
            result = json_response.get("result")
            if result != None and "'success': False" in str(result):
                result = "EXCEPTION OCCURRED"

            IsPerformanceSelected = libObj.parentTestCase.performanceBenchMarkingEnabled
            if IsPerformanceSelected == "true":
                conf_file,result = getConfigFileName(libObj.realpath)
                result, max_response_time = getDeviceConfigKeyValue(conf_file,"MAX_RESPONSE_TIME")
                time_taken = response.elapsed.total_seconds()
                print "Time Taken for",Data,"is :", time_taken
                if (float(time_taken) <= 0 or float(time_taken) > float(max_response_time)):
                    print "Device took more than usual to respond."
                    print "Exiting the script"
                    result = "EXCEPTION OCCURRED"
        else:
            result = response;
        return result;
    except requests.exceptions.RequestException as e:
        print "ERROR!! \nEXCEPTION OCCURRED WHILE EXECUTING CURL COMMANDS!!"
        print "Error message received :\n",e;
        return "EXCEPTION OCCURRED"

#-----------------------------------------------------------------
#GET PLUGIN STATUS
#-----------------------------------------------------------------
def rdkservice_getPluginStatus(plugin):
    data = '"method": "Controller.1.status@'+plugin+'"'
    result = execute_step(data)
    if result != None and result != "EXCEPTION OCCURRED":
        for x in result:
            WebKitStatus=x["state"]
        return WebKitStatus
    else:
        return result;

#-----------------------------------------------------------------
#GET THE STATUS OF ALL PLUGIN
#-----------------------------------------------------------------
def rdkservice_getAllPluginStatus():
    statusofPlugin=[];
    data = '"method": "Controller.1.status"'
    result = execute_step(data)
    if result != "EXCEPTION OCCURRED":
        for x in result:
            plugin = x["callsign"]
            state = x["state"]
            if "autostart" in x.keys():
                autostart = x["autostart"]
            else:
                autostart = "null"
            statusofPlugin.append([plugin,state,autostart]);
        return statusofPlugin;
    else:
        return result;

#------------------------------------------------------------------
#SET PLUGIN STATUS
#------------------------------------------------------------------
def rdkservice_setPluginStatus(plugin,status,uri=''):
    data = ''
    if plugin in graphical_plugins_list:
        rdkshell_activated = check_status_of_rdkshell()
        if rdkshell_activated:
            if status in "activate":
                data = '"method":"org.rdk.RDKShell.1.launch", "params":{"callsign": "'+plugin+'", "type":"", "uri":"'+uri+'"}'
            else:
                data = '"method":"org.rdk.RDKShell.1.destroy", "params":{"callsign": "'+plugin+'"}'
    else:
        data = '"method": "Controller.1.'+status+'", "params": {"callsign": "'+plugin+'"}'
    if data != '':
        result = execute_step(data)
    else:
        result = "EXCEPTION OCCURRED"
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
    if result != "EXCEPTION OCCURRED":
        value = result[reqValue]
        return value
    else:
        return result

#-------------------------------------------------------------------
#GET THE VALUE OF METHOD WITH PARAMETERS
#-------------------------------------------------------------------
def rdkservice_getValueWithParams(method,params):
    data = '"method": "'+method+'","params": '+params
    result = execute_step(data)
    return result

#------------------------------------------------------------------
#SET VALUE FOR A METHOD
#------------------------------------------------------------------
def rdkservice_setValue(method,value):
    data = '"method": "'+method+'","params": '+value
    result = execute_step(data)
    return result

#------------------------------------------------------------------
#GET THE NUMBER OF PLUGINS
#------------------------------------------------------------------
def rdkservice_getNoOfPlugins():
    status = rdkservice_getAllPluginStatus();
    if status != "EXCEPTION OCCURRED":
        NoofPlugins = len(status)
        return  NoofPlugins;
    else:
        return status;

#-------------------------------------------------------------------
#SET WEBDRIVER AND OPEN CHROME BROWSER
#-------------------------------------------------------------------
def openChromeBrowser(url):
   #https://askubuntu.com/questions/432255/what-is-the-display-environment-variable
   os.environ["DISPLAY"] = BrowserPerformanceVariables.display_variable;
   os.environ["PATH"] += BrowserPerformanceVariables.path_of_browser_executable;
   try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(chrome_options=chrome_options) #Opening Chrome
        driver.get(url);
   except Exception as error:
        print "Got exception while opening the browser"
        print error
        driver = "EXCEPTION OCCURRED"
   return driver;

#-------------------------------------------------------------------
#GET THE BROWSER SCORE FROM CSS3 TEST
#-------------------------------------------------------------------
def rdkservice_getBrowserScore_CSS3():
   try:
        browser_score_dict = {}
        browser_subcategory_list = BrowserPerformanceVariables.css3_test_subcategory_list
        webinspectURL = 'http://'+deviceIP+':'+BrowserPerformanceVariables.webinspect_port+'/Main.html?page=1'
        driver = openChromeBrowser(webinspectURL);
        if driver != "EXCEPTION OCCURRED":
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
            browser_score_dict["main_score"] = browser_score.replace("%","")
            print "\nThe Browser score using CSS3 test is : ",browser_score
            print "\n Subcategory scores:\n"
            print "===================================="
            for i in range(1,109):
                sub_category = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol/ol[2]/ol['+str(i)+']/ol[1]/li[1]/span/span').text

                parent = driver.find_elements_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol/ol[2]/ol['+str(i)+']/ol[1]/li')
                count = len(parent)
                score = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol/ol[2]/ol['+str(i)+']/ol[1]/li['+str(count-1)+']/span/span[2]').text
                if sub_category in browser_subcategory_list:
                    new_score = score.replace("%","")
                    browser_score_dict[sub_category] = new_score
                print sub_category + '  :  ' + score
            print '\n'
            time.sleep(5)
            driver.quit()
        else:
            browser_score_dict["main_score"]= "Unable to get the browser score"
   except Exception as error:
        print "Got exception while getting the browser score"
        print error
        browser_score_dict["main_score"] = "Unable to get the browser score"
        driver.quit()
   browser_score_dict = json.dumps(browser_score_dict)
   return browser_score_dict

#-------------------------------------------------------------------
#GET THE BROWSER SCORE FROM OCTANE TEST
#-------------------------------------------------------------------
def rdkservice_getBrowserScore_Octane():
   try:
        browser_score_dict = {}
        browser_subcategory_list = BrowserPerformanceVariables.octane_test_subcategory_list
        webinspectURL = 'http://'+deviceIP+':'+BrowserPerformanceVariables.webinspect_port+'/Main.html?page=1'
        driver = openChromeBrowser(webinspectURL);
        if driver != "EXCEPTION OCCURRED":
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
            browser_score_dict["main_score"] = browser_score
            print "\nThe Browser score using Octane test is : ",browser_score
            print "\n Subcategory scores:\n"
            print "===================================="
            for i in range(1,5):
                for j in range(1,5):
                    sub_category = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol/ol[3]/ol['+str(i)+']/ol['+str(j)+']/ol/li[1]/span/span[2]').text
                    score = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol/ol[3]/ol['+str(i)+']/ol['+str(j)+']/ol/li[2]/span/span[2]').text
                    if sub_category in browser_subcategory_list:
                        browser_score_dict[sub_category] = score
                    print sub_category + '     :    ' + score
            sub_category = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol/ol[3]/ol[4]/ol[5]/ol/li[1]/span/span[2]').text
            score = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol/ol[3]/ol[4]/ol[5]/ol/li[2]/span/span[2]').text
            if sub_category in browser_subcategory_list:
                browser_score_dict[sub_category] = score
            print sub_category + '     :    ' + score + '\n'
            time.sleep(10)
            driver.quit()
        else:
            browser_score_dict["main_score"] = "Unable to get the browser score"
   except Exception as error:
        print "Got exception while getting the browser score"
        print error
        browser_score_dict["main_score"] = "Unable to get the browser score"
        driver.quit()
   browser_score_dict = json.dumps(browser_score_dict)
   return browser_score_dict

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

#-------------------------------------------------------------------
#GET THE BROWSER SCORE FROM HTML5 TEST
#-------------------------------------------------------------------
def rdkservice_getBrowserScore_HTML5():
   try:
        browser_score_dict = {}
        browser_subcategory_list = BrowserPerformanceVariables.html5_test_subcategory_list
        webinspectURL = 'http://'+deviceIP+':'+BrowserPerformanceVariables.webinspect_port+'/Main.html?page=1'
        print "url:",webinspectURL
        driver = openChromeBrowser(webinspectURL);
        if driver != "EXCEPTION OCCURRED":
            time.sleep(10)
            action = ActionChains(driver)
            source = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/li[2]/span/span[1]/span[1]')
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
            browser_score = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol/ol[2]/ol[3]/ol[1]/ol[1]/ol/li[2]/span/span[2]').text
            max_browser_score_text = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol[1]/ol[2]/ol[3]/ol[1]/ol[1]/ol/li[3]/span/span[2]').text
            browser_score = browser_score + ' ' + max_browser_score_text
            browser_score_dict["main_score"] = browser_score
            print "\n Browser score from HTML5 test: {}".format(browser_score)
            print "\n Subcategory scores:\n"
            print "===================================="
            for i in range(1,3):
                for j in range(1,5):
                    parent = driver.find_elements_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol[1]/ol[2]/ol[3]/ol[2]/ol/ol['+str(i)+']/ol/ol['+str(j)+']/ol')
                    count = len(parent)
                    for k in range(2,count+1):
                       sub_category = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol[1]/ol[2]/ol[3]/ol[2]/ol/ol['+str(i)+']/ol/ol['+str(j)+']/ol['+str(k)+']/ol[1]/ol/ol/li[1]/span/span').text
                       score = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol[1]/ol[2]/ol[3]/ol[2]/ol/ol['+str(i)+']/ol/ol['+str(j)+']/ol['+str(k)+']/ol[1]/ol/ol/ol/ol/li[1]/span/span[2]').text
                       if sub_category in browser_subcategory_list:
                           browser_score_dict[sub_category] = score.split('/')[0]
                       print "{}   :{}".format(sub_category,score)
            time.sleep(5)
            driver.quit()
        else:
            browser_score_dict["main_score"] = "Unable to get the browser score"
   except Exception as error:
        print "Got exception while getting the browser score"
        print error
        browser_score_dict["main_score"] = "Unable to get the browser score"
        driver.quit()
   browser_score_dict = json.dumps(browser_score_dict)
   return browser_score_dict;

#-------------------------------------------------------------------
#GET THE BROWSER SCORE FROM SUNSPIDER TEST
#-------------------------------------------------------------------
def rdkservice_getBrowserScore_SunSpider():
   try:
        browser_score = ''
        browser_score_dict = {}
        browser_subcategory_list = BrowserPerformanceVariables.sunspider_test_subcategory_list
        webinspectURL = 'http://'+deviceIP+':'+BrowserPerformanceVariables.webinspect_port+'/Main.html?page=1'
        driver = openChromeBrowser(webinspectURL);
        if driver != "EXCEPTION OCCURRED":
            time.sleep(60)
            action = ActionChains(driver)
            source = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/li[6]/span/span[1]/span[1]')
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
            parent = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol')
            children = parent.find_elements_by_tag_name("li")
            text_values = ''
            total_score_text = 'Total:'
            for child in children:
                text_values += child.text
                if total_score_text in child.text:
                    browser_score = child.text
            if browser_score == '':
                browser_score_dict["main_score"] = "FAILURE"
            else:
                browser_score_dict["main_score"] = browser_score.split("Total: ")[1]
            driver.quit()
            text_values = text_values.replace('<br>','\n').replace('</pre>','\n')
            text_list = text_values.split('\n')
            for category in text_list:
                sub_category_list = category.replace("\"","").split(':')
                sub_category = sub_category_list[0].strip()
                if sub_category in browser_subcategory_list:
                    score = sub_category_list[1].split('ms')[0].strip()
                    browser_score_dict[sub_category] = score
            print "Details of SunSider Test:\n",text_values
        else:
            browser_score_dict["main_score"] = "FAILURE"
   except Exception as error:
        print "Got exception while getting the browser score"
        print error
        browser_score_dict["main_score"] = "FAILURE"
        driver.quit()
   browser_score_dict = json.dumps(browser_score_dict)
   return browser_score_dict;

#-------------------------------------------------------------------
#GET THE TIMESTAMP FROM THE LOG STRING
#-------------------------------------------------------------------
def getTimeStampFromString(log_string):
    match = re.search(r"(\d{2}:\d{2}:\d{2}\.\d{6})",log_string)
    return match.group(1)

#-------------------------------------------------------------------
#GET THE TIME IN MILLISEC FROM THE STRING
#-------------------------------------------------------------------
def getTimeInMilliSec(time_string):
    microsec_frm_time_string = int(time_string.split(".")[-1])
    time_string = time_string.replace(time_string.split(".")[-1],"")
    time_string = time_string.replace(".",":")
    time_string = time_string + str(microsec_frm_time_string/1000)
    hours, minutes, seconds, millisec = time_string.split(':')
    time_in_millisec = int(hours) * 3600000 + int(minutes) * 60000 + int(seconds)*1000 + int(millisec)
    return time_in_millisec

#-------------------------------------------------------------------
#GET THE OUTPUT OF A COMMAND EXECUTED
#-------------------------------------------------------------------
def rdkservice_getRequiredLog(ssh_method,credentials,command):
    output = ""
    credentials_list = credentials.split(',')
    host_name = credentials_list[0]
    user_name = credentials_list[1]
    password = credentials_list[2]
    lib = importlib.import_module("SSHUtility")
    if ssh_method == "directSSH":
        method = "ssh_and_execute"
    else:
        method = "ssh_and_execute_" + ssh_method
    method_to_call = getattr(lib, method)
    try:
        if ssh_method == "directSSH":
            output = method_to_call(ssh_method,host_name,user_name,password,command)
        else:
            output = method_to_call(host_name,user_name,password,command)
    except Exception as e:
        print "Exception occured during ssh session"
        print e
    finally:
        if output == "":
            output = "EXCEPTION"
        return output

#-------------------------------------------------------------------
#GET THE SSH DETAILS FROM CONFIGURATION FILE
#-------------------------------------------------------------------
def rdkservice_getSSHParams(realpath,deviceIP):
    ssh_dict = {}
    print "\n getting ssh params from conf file"
    conf_file,result = getConfigFileName(realpath)
    if result == "SUCCESS":
        result,ssh_method = getDeviceConfigKeyValue(conf_file,"SSH_METHOD")
        result,user_name = getDeviceConfigKeyValue(conf_file,"SSH_USERNAME")
        result,password = getDeviceConfigKeyValue(conf_file,"SSH_PASSWORD")
        if any(value == "" for value in (ssh_method,user_name,password)):
            print "please configure values before test"
            ssh_dict = {}
        else:
            ssh_dict["ssh_method"] = ssh_method
            if password.upper() == "NONE":
                password = ""
            ssh_dict["credentials"] = deviceIP +","+ user_name +","+ password
    else:
        print "Failed to find the device specific config file"
    ssh_dict = json.dumps(ssh_dict)
    return ssh_dict

#-------------------------------------------------------------------
#SUSPEND A GIVEN PLUGIN USING RDKSHELL
#-------------------------------------------------------------------
def suspend_plugin(obj,plugin):
    status = expectedResult = "SUCCESS"
    print "\n Suspending {} \n".format(plugin)
    params = '{"callsign":"'+plugin+'"}'
    tdkTestObj = obj.createTestStep('rdkservice_setValue')
    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.suspend")
    tdkTestObj.addParameter("value",params)
    start_suspend = str(datetime.utcnow()).split()[1]
    tdkTestObj.executeTestCase(expectedResult);
    result = tdkTestObj.getResult();
    if result == "SUCCESS":
        print "\n Suspended {} plugin \n".format(plugin)
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        print "\n Unable to Suspend {} plugin \n".format(plugin)
        tdkTestObj.setResultStatus("FAILURE")
        status = "FAILURE"
    return status,start_suspend

#-------------------------------------------------------------------
#LAUNCH A GIVEN PLUGIN USING RDKSHELL
#-------------------------------------------------------------------
def launch_plugin(obj,plugin,uri=''):
    status = expectedResult = "SUCCESS"
    start_launch = ""
    rdkshell_activated = check_status_of_rdkshell()
    if rdkshell_activated:
        print "\n Resuming {} \n".format(plugin)
        params = '{"callsign":"'+plugin+'", "type":"", "uri":"' + uri + '"}'
        tdkTestObj = obj.createTestStep('rdkservice_setValue')
        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.launch")
        tdkTestObj.addParameter("value",params)
        start_launch = str(datetime.utcnow()).split()[1] 
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult();
        if result == "SUCCESS":
            print "\n Resumed {} plugin \n".format(plugin)
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "\n Unable to Resume {} plugin \n".format(plugin)
            tdkTestObj.setResultStatus("FAILURE")
            status = "FAILURE"
    else:
        status = "FAILURE"
    return status,start_launch

#-------------------------------------------------------------------
#GET BLUETOOTH MAC OF DUT
#-------------------------------------------------------------------
def rdkservice_getBluetoothMac():
    method = "org.rdk.System.1.getDeviceInfo"
    reqValue = "bluetooth_mac"
    data = '"method": "'+method+'","params":{"params":"'+reqValue+'"}'
    result = execute_step(data)
    if result != "EXCEPTION OCCURRED":
        value = result[reqValue]
        return value
    else:
        return result

#-------------------------------------------------------------------
#GET SUPPORTED PLUGINS FROM DEVICE CONFIG FILE
#-------------------------------------------------------------------
def rdkservice_getSupportedPlugins(realpath,plugins):
    conf_file,result = getConfigFileName(realpath)
    if result == "SUCCESS":
        status,supported_plugins = getDeviceConfigKeyValue(conf_file,"SUPPORTED_PLUGINS")
        if supported_plugins != "":
            plugins_list = plugins.split(',')
            supported_plugins_list = supported_plugins.split(',')
            if not all(plugin in supported_plugins_list for plugin in plugins_list):
                updated_plugins_list = [plugin for plugin in plugins_list if plugin in supported_plugins_list]
                plugins = ','.join(plugin for plugin in updated_plugins_list)
        else:
            print "\n Please configure the supported plugins in device configuration file \n"
            plugins = "FAILURE"
        return plugins
    else:
        return result

#-------------------------------------------------------------------
#VALIDATE VIDEO PLAYBACK IN PREMIUM APPS
#-------------------------------------------------------------------
def rdkservice_validateVideoPlayback(sshmethod,credentials,video_validation_script):
    result = "SUCCESS"
    video_validation_script = video_validation_script.split('.py')[0]
    try:
        lib = importlib.import_module(video_validation_script)
        method = "check_video_status"
        method_to_call = getattr(lib, method)
        result = method_to_call(sshmethod,credentials)
    except Exception as e:
        print "\n ERROR OCCURRED WHILE IMPORTING THE VIDEO VALIDATION SCRIPT FILE, PLEASE CHECK THE CONFIGURATION \n"
        result = "FAILURE"
    finally:
        return result

#-------------------------------------------------------------------
#VALIDATE PLUGIN FUNCTIONALITY
#The function will launch the plugin and validate the functionality
#of the plugin. eg: launch Cobalt, set video URL and validate video
#playback
#-------------------------------------------------------------------
def rdkservice_validatePluginFunctionality(plugin,operations,validation_details):
    result = "FAILURE"
    operations = json.loads(operations)
    validation_details = json.loads(validation_details)
    movedToFront = False
    #Activate plugin
    print "\n Activating plugin : {}".format(plugin)
    if plugin == "ResidentApp":
        status = rdkservice_setPluginStatus(plugin,"activate",validation_details[1])
    else:
        status = rdkservice_setPluginStatus(plugin,"activate")
    time.sleep(5)
    #Check status
    if status != "EXCEPTION OCCURRED":
        curr_status = rdkservice_getPluginStatus(plugin)
        time.sleep(10)
        if curr_status in ("activated","resumed"):
            zorder_result = rdkservice_getValue("org.rdk.RDKShell.1.getZOrder")
            if zorder_result != "EXCEPTION OCCURRED":
                zorder = zorder_result["clients"]
                zorder = exclude_from_zorder(zorder) 
                if plugin.lower() in zorder:
                    if zorder[0].lower() != plugin.lower():
                        param = '{"client": "'+plugin+'"}'
                        movetofront_result = rdkservice_setValue("org.rdk.RDKShell.1.moveToFront",param)
                        if movetofront_result != "EXCEPTION OCCURRED":
                            movedToFront = True
                    else:
                        movedToFront = True
                else:
                    print "\n {} is not present in the zorder: {}".format(plugin,zorder)
                if movedToFront:
                    for operation in operations:
                        method = [plugin_method for plugin_method in operation][0]
                        value = [operation[plugin_method] for plugin_method in operation][0]
                        response = rdkservice_setValue(method,value)
                        sys.stdout.flush()
                        if response == "EXCEPTION OCCURRED":
                            print "\n Error while executing {} method".format(method)
                            break
                        time.sleep(20)
                    else:
                        print "\n Successfully completed launching and setting the operations for {} plugin".format(plugin)
                        validation_check = validation_details[0]
                        if validation_check == "video_validation":
                            time.sleep(20)
                            sshmethod = validation_details[1]
                            credentials = validation_details[2]
                            video_validation_script = validation_details[3]
                            video_status =  rdkservice_validateVideoPlayback(sshmethod,credentials,video_validation_script)
                            sys.stdout.flush()
                            if video_status != "SUCCESS":
                                print "\n Video is not playing"
                                return result
                            else:
                                print "\n Video is playing"
                                result = "SUCCESS"
                        elif validation_check == "no_validation":
                            print "\n Validation is not needed, proceeding the test"
                            result = "SUCCESS"
                        else:
                            method = validation_check
                            expected_value = validation_details[1]
                            value = rdkservice_getValue(method)
                            if value not in ("EXCEPTION OCCURRED", None) and expected_value in value:
                                print "\n The value:{} set for {} plugin".format(value,plugin)
                                result = "SUCCESS"
                            else:
                                print "\n Expected Value is not present, Current value: {}".format(value)
                                return result
                else:
                    print "\n Error while moving {} plugin to front ".format(plugin)
            else:
                print "\n Error while getting the zorder result"
        else:
            print "\n Plugin is not activated, current status: {}".format(curr_status)
    else:
        print "\n Error while activating the plugin"
    return result

#-------------------------------------------------------------------
#VALIDATE IPV4 ADDRESS
#-------------------------------------------------------------------
def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton available
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False
    return True

#-------------------------------------------------------------------
#VALIDATE IPV6 ADDRESS
#-------------------------------------------------------------------
def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True

#-------------------------------------------------------------------
#GET DEVICE UPTIME
#-------------------------------------------------------------------
def get_device_uptime(obj):
    uptime = -1
    expectedResult = 'SUCCESS'
    device_info = 'DeviceInfo'
    tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
    tdkTestObj.addParameter('plugin',device_info)
    tdkTestObj.addParameter("status",'activate')
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    if expectedResult in result:
        tdkTestObj.setResultStatus("SUCCESS")
        time.sleep(5)
        tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
        tdkTestObj.addParameter('plugin',device_info)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        device_info_status = tdkTestObj.getResultDetails()
        if device_info_status in 'activated':
            tdkTestObj.setResultStatus("SUCCESS")
            time.sleep(5)
            tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
            tdkTestObj.addParameter("method","DeviceInfo.1.systeminfo")
            tdkTestObj.addParameter("reqValue","uptime")
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult()
            if expectedResult in result:
                uptime = int(tdkTestObj.getResultDetails())
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print '\n Error while executing DeviceInfo.1.systeminfo method'
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print '\n Unable to activate DeviceInfo plugin, current status: ',device_info_status
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print '\n Error while activating DeviceInfo'
        tdkTestObj.setResultStatus("FAILURE")
    return uptime

#-------------------------------------------------------------------
#MOVE THE PLUGIN TO FRONT OR BACK BASED ON ARGUMENTS
#-------------------------------------------------------------------
def move_plugin(obj,plugin,method):
    result_val = "FAILURE"
    expectedResult = "SUCCESS"
    param_val = '{"client": "'+plugin+'"}'
    tdkTestObj = obj.createTestStep('rdkservice_setValue')
    tdkTestObj.addParameter("method","org.rdk.RDKShell.1."+method)
    tdkTestObj.addParameter("value",param_val)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    if expectedResult in result:
        tdkTestObj.setResultStatus("SUCCESS")
        print "\n Check whether {} is in front".format(plugin)
        time.sleep(5)
        tdkTestObj = obj.createTestStep('rdkservice_getValue')
        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.getZOrder")
        tdkTestObj.executeTestCase(expectedResult)
        zorder = tdkTestObj.getResultDetails()
        zorder_status = tdkTestObj.getResult()
        if expectedResult in zorder_status :
            zorder = ast.literal_eval(zorder)["clients"]
            zorder = exclude_from_zorder(zorder)
            print "zorder: ",zorder
            if  plugin.lower() in zorder and plugin.lower() == zorder[0]:
                result_val = "SUCCESS"
                print "\n {} is in front".format(plugin)
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "\n {} is not in front".format(plugin)
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "\n Unable to get zorder"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "\n Error while executing {} method".format(method)
        tdkTestObj.setResultStatus("FAILURE")
    return result_val

#-------------------------------------------------------------------
#REMOVE UNWANTED PROCESSES FROM ZORDER AND RETURN UPDATED ZORDER
#-------------------------------------------------------------------
def exclude_from_zorder(zorder):
   new_zorder = [ element for element in zorder if element not in excluded_process_list ] 
   return new_zorder

#-------------------------------------------------------------------------
#Utility functions for Hardware Performance threshold validation - START
#-------------------------------------------------------------------------
def hardwarePerformanceThresholdComparison(sysUtilObj,message,unit,reverserscheck="false"):
    status=[]
    threshold_Check=thresholdCheck(sysUtilObj)
    if threshold_Check=="TRUE":
        print "***************************User Enabled Threshold check*********************************************"

        transferLogDetails=json.loads(message)
        configParam=transferLogDetails["utility"].upper()
        thresholdValueDevice=transferLogDetails["values"]
        conf_file,result=getConfigFileNameDetail(sysUtilObj)
        result,thresholdLimitConfig=getDeviceConfigValue(conf_file,configParam)
        thresholdValueConfig=json.loads(thresholdLimitConfig)

        for(key1,Value1),(key2,Value2) in zip(thresholdValueDevice.items(),thresholdValueConfig.items()):
            hw_Device_pname=key1
            hw_Config_pname=key2

            hw_Device_Value=float(Value1.split(" ")[0])
            hw_Config_value=float(Value2.split(" ")[0])
            if hw_Device_Value >= hw_Config_value if reverserscheck == "false" else hw_Device_Value <= hw_Config_value :
                status.append("SUCCESS")
                print("Success :Device performance value {0}{2} is in the expected threshold value {1}{2}".format(hw_Device_Value,hw_Config_value,unit))
            else:
                status.append("FAILURE")
                print("FAILURE :Device performance value {0}{2} is not in the expected threshold value {1}{2}".format(hw_Device_Value,hw_Config_value,unit))
        return "FAILURE" if "FAILURE" in status else "SUCCESS"

    else:
         print "*********************************User Disable  Threshold check**********************************"
         status="SUCCESS"
         return status

#--------------------------------------------------------------------------
#   Check ThresholdCheck User Input from Config File
#--------------------------------------------------------------------------
def thresholdCheck(Obj):
    configParam="Threshold_Check"
    conf_file=getConfigFileNameDetail(Obj)
    Threshold_Check_UserInput=getDeviceConfigValue(conf_file,configParam)
    status ,Threshold_Check_UserInput=getDeviceConfigValue(conf_file,configParam)
    return Threshold_Check_UserInput
#-------------------------------------------------------------------------
#   Get Avg Threshold Config Value
#-------------------------------------------------------------------------
def getDeviceConfigValue(conf_file,configParam):
    value=""
    status="SUCCESS"
    deviceConfig="device.config"
    config=ConfigParser.ConfigParser()
    config.read(conf_file)
    value=str(config.get(deviceConfig,configParam))
    return status,value
#-----------------------------------------------------------------------
# Get Config File Details for Threshold Comparison
#-----------------------------------------------------------------------
def getConfigFileNameDetail(obj):
    url = obj.url + '/deviceGroup/getDeviceDetails?deviceIp='+obj.IP
    try:
        data = urllib.urlopen(url).read()
        deviceDetails = json.loads(data)
        device_Name = deviceDetails["devicename"]
        device_Type = deviceDetails["boxtype"]
        deviceConfigFile=""
        status ="SUCCESS"
        configPath = obj.realpath + "/"   + "fileStore/tdkvRDKServiceConfig"
        deviceNameConfigFile = configPath + "/" + device_Name + ".config"
        deviceTypeConfigFile = configPath + "/" + device_Type + ".config"
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
    except:
        print "Unable to get Device Details from REST !!!"
        status = "FAILURE"
    return deviceConfigFile,status;

#-------------------------------------------------------------------------
#Utility functions for Hardware Performance threshold validation - END
#-------------------------------------------------------------------------

#-------------------------------------------------------------------
#CHECK THE STATUS OF RDKSHELL PLUGIN AND ACTIVATE IF NEEDED
#-------------------------------------------------------------------
def check_status_of_rdkshell():
    activated = False
    rdkshell_status = rdkservice_getPluginStatus("org.rdk.RDKShell")
    if "activated" == rdkshell_status:
        activated = True
    elif "deactivated" == rdkshell_status:
        set_status = rdkservice_setPluginStatus("org.rdk.RDKShell","activate")
        time.sleep(2)
        rdkshell_status = rdkservice_getPluginStatus("org.rdk.RDKShell")
        if "activated" in rdkshell_status:
            activated = True
        else:
            print "\n Unable to activate RDKShell plugin"
    else:
        print "\n RDKShell status in DUT:",rdkshell_status
    return activated

#-------------------------------------------------------------------
#GET THE BROWSER SCORE FROM ANIMATION BENCHMARK TEST
#-------------------------------------------------------------------
def rdkservice_getBrowserScore_AnimationBenchmark():
    fps_list = []
    try:
        browser_score_dict = {}
        webinspectURL = 'http://'+deviceIP+':'+BrowserPerformanceVariables.webinspect_port+'/Main.html?page=1'
        driver = openChromeBrowser(webinspectURL);
        if driver != "EXCEPTION OCCURRED":
            time.sleep(10)
            action = ActionChains(driver)
            source = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/li[2]')
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
            for count in range(0,5):
                fps_info = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/li[2]/span/span[2]').text
                if "FPS" in fps_info:
                    fps_value = fps_info.split(' ')[0]
                    fps_list.append(float(fps_value))
                    time.sleep(1)
                else:
                    print "\n Error while getting FPS value"
                    browser_score_dict["main_score"] = "Unable to get the browser score"
                    break
            else:
                average_fps = sum(fps_list)/len(fps_list)
                browser_score_dict["main_score"] = round(average_fps,2)
        else:
            browser_score_dict["main_score"] = "Unable to get the browser score"
    except Exception as error:
        print "Got exception while getting the browser score"
        print error
        browser_score_dict["main_score"] = "Unable to get the browser score"
        driver.quit()
    browser_score_dict = json.dumps(browser_score_dict)
    return browser_score_dict

#-------------------------------------------------------------------
#GET THE GRAPHICAL PLUGINS SUPPORTED BY THE DUT
#-------------------------------------------------------------------
def get_graphical_plugins(conf_file):
    status,graphical_plugins = getDeviceConfigKeyValue(conf_file,"AVAILABLE_GRAPHICAL_PLUGINS")
    if graphical_plugins != "":
        plugins_list = graphical_plugins.split(',')
    else:
        print "\n Please configure the available graphical plugins in device config file"
        plugins_list = []
    return plugins_list

#-------------------------------------------------------------------
#GET THE BROWSER SCORE FROM SPEEDOMETER TEST
#-------------------------------------------------------------------

def rdkservice_getBrowserScore_Speedometer():
    try:
        browser_score_dict = {}
        webinspectURL = 'http://'+deviceIP+':'+BrowserPerformanceVariables.webinspect_port+'/Main.html?page=1'
        driver = openChromeBrowser(webinspectURL);
        if driver != "EXCEPTION OCCURRED":
            time.sleep(10)
            action = ActionChains(driver)
            source = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/li[2]/div')
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
            speedometer_score = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol/ol[4]/li[4]/span/span[2]').text
            browser_score_dict["main_score"] = speedometer_score
        else:
            browser_score_dict["main_score"] = "Unable to get the browser score"
    except Exception as error:
        print "Got exception while getting the browser score"
        print error
        browser_score_dict["main_score"] = "Unable to get the browser score"
        driver.quit()
    browser_score_dict = json.dumps(browser_score_dict)
    return browser_score_dict

#-------------------------------------------------------------------
#GET THE BROWSER SCORE FROM MOTIONMARK TEST
#-------------------------------------------------------------------
def rdkservice_getBrowserScore_MotionMark():
    try:
        browser_score_dict = {}
        webinspectURL = 'http://'+deviceIP+':'+BrowserPerformanceVariables.webinspect_port+'/Main.html?page=1'
        driver = openChromeBrowser(webinspectURL);
        if driver != "EXCEPTION OCCURRED":
            time.sleep(10)
            action = ActionChains(driver)
            source = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/li[2]/span/span/span[2]/span[2]')
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
            motionmark_score = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol/ol[2]/ol[2]/ol[1]/li[1]/span/span[2]').text
            browser_score_dict["main_score"] = motionmark_score
            for i in range(2,10):
                sub_category = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol/ol[2]/ol[2]/ol[2]/ol[2]/ol[2]/ol['+str(i)+']/li[1]/span/span[2]').text
                score = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol/ol[2]/ol[2]/ol[2]/ol[1]/ol[1]/ol[2]/ol['+str(i)+']/li[1]/span/span[2]').text
                print sub_category + '  :  ' + score
            print '\n'
            time.sleep(5)
            driver.quit()
        else:
            browser_score_dict["main_score"] = "Unable to get the browser score"
    except Exception as error:
        print "Got exception while getting the browser score"
        print error
        browser_score_dict["main_score"] = "Unable to get the browser score"
        driver.quit()
    browser_score_dict = json.dumps(browser_score_dict)
    return browser_score_dict


#-------------------------------------------------------------------
#GET THE BROWSER SCORE FROM MOTIONMARK TEST
#-------------------------------------------------------------------
def rdkservice_getBrowserScore_MotionMark():
    try:
        browser_score_dict = {}
        webinspectURL = 'http://'+deviceIP+':'+BrowserPerformanceVariables.webinspect_port+'/Main.html?page=1'
        driver = openChromeBrowser(webinspectURL);
        if driver != "EXCEPTION OCCURRED":
            time.sleep(10)
            action = ActionChains(driver)
            source = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/li[2]/span/span/span[2]/span[2]')
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
            motionmark_score = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol/ol[2]/ol[2]/ol[1]/li[1]/span/span[2]').text
            browser_score_dict["main_score"] = motionmark_score
            for i in range(2,10):
                sub_category = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol/ol[2]/ol[2]/ol[2]/ol[2]/ol[2]/ol['+str(i)+']/li[1]/span/span[2]').text
                score = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol/ol[2]/ol[2]/ol[2]/ol[1]/ol[1]/ol[2]/ol['+str(i)+']/li[1]/span/span[2]').text
                print sub_category + '  :  ' + score
            print '\n'
            time.sleep(5)
            driver.quit()
        else:
            browser_score_dict["main_score"] = "Unable to get the browser score"
    except Exception as error:
        print "Got exception while getting the browser score"
        print error
        browser_score_dict["main_score"] = "Unable to get the browser score"
        driver.quit()
    browser_score_dict = json.dumps(browser_score_dict)
    return browser_score_dict

#-------------------------------------------------------------------
#GET THE BROWSER SCORE FROM SMASHCAT TEST
#-------------------------------------------------------------------
def rdkservice_getBrowserScore_Smashcat():
    try:
        browser_score_dict = {}
        webinspectURL = 'http://'+deviceIP+':'+BrowserPerformanceVariables.webinspect_port+'/Main.html?page=1'
        driver = openChromeBrowser(webinspectURL);
        if driver != "EXCEPTION OCCURRED":
            time.sleep(10)
            action = ActionChains(driver)
            source = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/li[2]')
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
            smashcat_score_list = []
            count = 1
            while (count<3):
                try:
                    smashcat_score = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol[1]/ol[1]/li[1]/span/span[2]').text
                except exceptions.StaleElementReferenceException,e:
                    smashcat_score = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol[1]/ol[1]/li[1]/span/span[2]').text
                smashcat_score = int(smashcat_score.split('f')[0])
                print "score =",smashcat_score
                time.sleep(2)
                smashcat_score_list.append(smashcat_score)
                count = count +1
            smashcat_score =(sum(smashcat_score_list))/2
            browser_score_dict["main_score"] = smashcat_score
            driver.quit()
        else:
            browser_score_dict["main_score"] = "Unable to get the browser score"
    except Exception as error:
        print "Got exception while getting the browser score"
        print error
        browser_score_dict["main_score"] = "Unable to get the browser score"
        driver.quit()
    browser_score_dict = json.dumps(browser_score_dict)
    return browser_score_dict

#-------------------------------------------------------------------
#GET THE BROWSER SCORE FROM KRAKEN TEST
#-------------------------------------------------------------------

def rdkservice_getBrowserScore_Kraken():
    try:
        browser_score_dict = {}
        webinspectURL = 'http://'+deviceIP+':'+BrowserPerformanceVariables.webinspect_port+'/Main.html?page=1'
        driver = openChromeBrowser(webinspectURL);
        if driver != "EXCEPTION OCCURRED":
            time.sleep(10)
            action = ActionChains(driver)
            source = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/li[2]')
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
            time.sleep(20)
            kraken_score = driver.find_element_by_xpath('//*[@id="tab-browser"]/div/div/div/div[2]/div/ol/ol/ol/ol[1]/ol/ol[4]/li[8]/span/span').text
            kraken_score = kraken_score.split("Total: ")[1]
            browser_score_dict["main_score"] = kraken_score.split('ms')[0].strip()
            driver.quit()
        else:
            browser_score_dict["main_score"] = "Unable to get the browser score"
    except Exception as error:
        print "Got exception while getting the browser score"
        print error
        browser_score_dict["main_score"] = "Unable to get the browser score"
        driver.quit()
    browser_score_dict = json.dumps(browser_score_dict)
    return browser_score_dict
#--------------------------------------------------------
# OPEN A LOG FILE TO REDIRECT THE LOGS
#--------------------------------------------------------
def open_write_logfile(obj,filename,script_name,data=""):
    new_path = "fileStore/"
    output_file = '{}{}.txt'.format(obj.realpath+new_path,filename)
    if os.path.isfile(output_file):
        with open(output_file, 'r') as the_file:
            buf = the_file.readlines()
        with open(output_file, 'w') as the_file:
            for line in buf:
                if script_name in line:
                    data = line.strip() + " ::: " + data.split(" ::: ")[-1]
                elif line.split(" ::: ")[0] != script_name:
                    print "Writing existing line"
                    the_file.write(line)

    print "\nWriting performance data to file ", output_file
    with open(output_file, 'a+') as out_file:
        out_file.write(data)
#--------------------------------------------------------------
#GET PVS DATA AND WRITE TO LOG FILE
#--------------------------------------------------------------
def getDataAndWriteInFile(Value,obj):
    #getImageName
    ImageName = rdkservice_getValueWithParams("org.rdk.System.1.getDeviceInfo",'["imageVersion"]')
    filename = ImageName["imageVersion"]
    delimiter = " ::: "
    #open_write_logfile(libObj,filename,obj.execName)
    count1 = sum(1 for d in Value if 'THRESHOLD_VALUE' in d)
    count2 = sum(1 for d in Value if 'Threshold value' in d)
    count = count1 + count2
    for i in range (count):
        data = obj.execName + delimiter
        for item in Value:
            if "THRESHOLD_VALUE" in item or "Threshold value" in item:
                threshold_value = item.split(":")[1]
                Value.remove(item)
                break;
        for item in Value:
            if "Time taken " in item or "Browser " in item:
                data = data + item.split(":")[0] + delimiter + threshold_value + delimiter
                data = data + item.split(":")[1]
                Value.remove(item)
                break;
        data = data + "\n"
        print data
        open_write_logfile(libObj,filename,obj.execName,data)
#---------------------------------------------------------------------------------------
# PVS Execution Summary
#---------------------------------------------------------------------------------------
def getSummary(Summ_list,obj = False):
    if obj != False:
       Value = [x for x in Summ_list]
       getDataAndWriteInFile(Value,obj)

    print("############## Execution Summary #######################")
    for key in Summ_list:
        print(key)
        value = key.split(':')[1]
        if 'ms' in value:
            value = value.split('m')[0]
        if float(value) < 0:
            print "Check if VM and DUT time is synchronized OR Check if any previous steps got failed."
