#!/usr/bin/python

##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2019 RDK Management
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

from selenium import webdriver;
import tdkbE2EUtility;
from tdkbE2EUtility import *;
import subprocess
import time
import os

#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------

def startSeleniumGrid(tdkTestObj,ClientType,GridUrl,LoginStatus = "LocalLogin"):

# Syntax      : startSeleniumGrid()
# Description : This will start selenium hub and node in machines
# Parameters  : ClientType : LAN/WLAN
#               GridUrl : URL to be opened in the browser
#               LoginStatus : Login/NoLogin
# Return Value: SUCCESS/FAILURE

    try:
        Status = "FAILURE"
        driver = "Failed to initialize the webdriver"
        global profile;
        print "Starting the Selenium Hub in TM machine"
        #Kill selenium hub and node as a pre-requisite before starting new hub and node
        Prerequ_Status = kill_hub_node(ClientType)
        if "SUCCESS" in Prerequ_Status:
            print "Webui Pre-requisite success"

            status = startHub()
            if "SUCCESS" in status:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: Selenium Hub started successfully\n"

                print "Starting Selenium Node in", ClientType, " client machine"
                status = initiateNode(ClientType)
                if status == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "SUCCESS: Node Started successfully\n"
                    isProxyEnabled = tdkbE2EUtility.proxy_enabled;
                    profile = webdriver.FirefoxProfile()
                    if isProxyEnabled == "True":
                        print "Set proxy for the web browser"
                        profile = setProxy(profile);

                    if ClientType == "LAN" or ClientType == "WAN":
                        if LoginStatus == "LocalLogin" or LoginStatus == "NoLogin" or LoginStatus == "MSOLogin":
                            Status,driver = openLocalWebUI(GridUrl,tdkTestObj,LoginStatus);
                        elif LoginStatus == "CaptivePortal":
                            Status,driver = openCaptivePortal(GridUrl,tdkTestObj);
			elif LoginStatus == "CheckUIAccessibility":
                            Status,driver = isUIAvailable(GridUrl,tdkTestObj)
                    elif ClientType == "WLAN":
                        Status = "SUCCESS";
                        driver = "Driver will be initialized while opening the WebUI";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "FAILURE: Failed to start node in client machine\n"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Failed to start the selenium hub\n"
        else:
            print "Webui Pre-requisite failed"
    except Exception as error:
        print "Got Exception at the function startSeleniumGrid()"
        print error;
        driver = "Failed to set the driver"
        Status = "FAILURE"
    return driver,Status;

#---------------------------------------------------------------------------------
#End of function
#---------------------------------------------------------------------------------

def startHub():

# Syntax      : startHub()
# Description : Function to start the selenium hub in TM machine
# Parameters  : None
# Return Value: SUCCESS/FAILURE

    try:
        command = "sh %s start_hub %s %s %s" %(tdkbE2EUtility.start_hub_script,tdkbE2EUtility.webui_hub_selenium_path,tdkbE2EUtility.webui_logfile,tdkbE2EUtility.hub_machine_ip)
        print command
        output = subprocess.check_output(command,shell=True)
    except Exception as error:
        print "Got Exception at the function startHub()"
        print error;
        output = "Unable to start selenium hub in TM machine. Please check if any instances are already running."
    return output

#---------------------------------------------------------------------------------
#End of function
#---------------------------------------------------------------------------------

def initiateNode(clientType):

# Syntax      : initiateNode()
# Description : Function to start node from client machine
# Parameters  : clientType - Client in which the node should start
# Return Value: SUCCESS/FAILURE

    try:
        status = clientConnect(clientType)
        if clientType == "LAN":
            script = tdkbE2EUtility.lan_script;
            node_machine_ip = tdkbE2EUtility.lan_ip;
            node_selenium_path = tdkbE2EUtility.webui_node_lan_selenium_path
            node_logfile = tdkbE2EUtility.webui_node_lan_logfile
        elif clientType == "WLAN":
            script = tdkbE2EUtility.wlan_script;
            node_machine_ip = tdkbE2EUtility.wlan_ip;
            node_selenium_path = tdkbE2EUtility.webui_node_wlan_selenium_path
            node_logfile = tdkbE2EUtility.webui_node_wlan_logfile
        elif clientType == "WAN":
            script = tdkbE2EUtility.wan_script;
            node_machine_ip = tdkbE2EUtility.wan_ip;
            node_selenium_path = tdkbE2EUtility.webui_node_wan_selenium_path
            node_logfile = tdkbE2EUtility.webui_node_wan_logfile
        if status == "SUCCESS":
            command = "sh %s start_node %s %s %s %s" %(script,node_selenium_path,tdkbE2EUtility.hub_machine_ip,node_logfile,node_machine_ip)
            status = executeCommand(command)
    except Exception as error:
        print "Got Exception at the function initiateNode()"
        print error;
        status = "Unable to start selenium in node machine. Please check if any instances are already running."
    return status
#---------------------------------------------------------------------------------
#End of function
#---------------------------------------------------------------------------------

def setProxy(profile):

# Syntax      : setProxy()
# Description : Function to set proxy for the browser
# Parameters  : profile : the web browser profile
# Return Value: SUCCESS/FAILURE

    try:
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", tdkbE2EUtility.proxy_host)
        profile.set_preference("network.proxy.http_port",tdkbE2EUtility.proxy_port)
        profile.set_preference("network.proxy.socks_username", tdkbE2EUtility.proxy_username)
        profile.set_preference("network.proxy.socks_password", tdkbE2EUtility.proxy_password)
        profile.set_preference("network.proxy.no_proxies_on",tdkbE2EUtility.no_proxy )

        profile.update_preferences()
        executable_path  = tdkbE2EUtility.proxy_path
    except Exception as error:
        print "Got Exception at the function setProxy()"
        print error;
        profile = "Unable to update the profile with proxy settings"
    return profile;

#---------------------------------------------------------------------------------
#End of function
#---------------------------------------------------------------------------------

def kill_hub_node(clientType):

# Syntax      : kill_hub_node()
# Description : Function to kill hub and node before exiting the script
# Parameters  : clientType - Client in which the node started
# Return Value: SUCCESS/FAILURE

    if clientType == "LAN":
        script = tdkbE2EUtility.lan_script;
    elif clientType == "WLAN":
        script = tdkbE2EUtility.wlan_script;
    elif clientType == "WAN":
        script = tdkbE2EUtility.wan_script;
    print "Killing hub"
    p = subprocess.call([tdkbE2EUtility.start_hub_script, 'kill_selenium'])
    print "Killing node"
    status = clientConnect(clientType)
    if status == "SUCCESS":
        command = "source %s kill_selenium" %(script)
        status = executeCommand(command)
        return "SUCCESS"
    else:
        return "FAILURE"
#---------------------------------------------------------------------------------
#End of function
#---------------------------------------------------------------------------------

def openLocalWebUI(GridUrl,tdkTestObj,LoginStatus):

# syntax       : openLocalWebUI()
# Description  : This function is to open the given URL in the browser of client machine
# Parameters  : LoginStatus : Login/NoLogin
#               GridUrl : URL to be opened in the browser
# Return Value: SUCCESS/FAILURE

    try:
        print "Opening the requested URL in browser"
        hub_url = "http://%s:4444/wd/hub" %tdkbE2EUtility.hub_machine_ip
        driver = webdriver.Remote(browser_profile=profile,command_executor=hub_url)
        driver.get(GridUrl);
	#Uncomment below line and comment next line if UI page has changed
	#checkUI = driver.find_element_by_xpath("/html/body/div[1]/div[3]/h1").text 
        checkUI = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/h1").text
        if "Gateway > Login" == checkUI:
            tdkTestObj.setResultStatus("SUCCESS");
            print "SUCCESS: Successfully opened the xfinity UI page\n"
            if LoginStatus != "NoLogin":
                if LoginStatus == "LocalLogin":
                    driver.find_element_by_id("username").send_keys(tdkbE2EUtility.ui_username)
                    driver.find_element_by_id("password").send_keys(tdkbE2EUtility.ui_password)
                elif LoginStatus == "MSOLogin":
                    driver.find_element_by_id("username").send_keys(tdkbE2EUtility.mso_ui_username)
                    driver.find_element_by_id("password").send_keys(tdkbE2EUtility.mso_ui_password)

		#Uncomment below line and comment next line if UI page has changed
		#driver.find_element_by_class_name("btn").submit()
                driver.find_element_by_class_name("form-btn").submit()
                time.sleep(30)
                checkLogin= driver.find_element_by_xpath("//div[1]/div[3]/div[1]/ul[1]/li[2]/a").text
                if "Logout" == checkLogin:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Successfully logged in to the UI page"
                    Status = "SUCCESS"
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Failed to login to the UI page"
            else:
                Status = "SUCCESS"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "FAILURE: Failed to open the Xfinity login page\n"
    except Exception as error:
        print "Got Exception at the function openLocalWebUI()"
        print error;
        driver.quit()
        Status = "FAILURE"
    return Status,driver;

#---------------------------------------------------------------------------------
#End of function
#---------------------------------------------------------------------------------

def openCaptivePortal(GridUrl,tdkTestObj):

# syntax       : openopenCaptivePortal()
# Description  : This function is to open the captive portal in the browser of client machine
# Parameters  : GridUrl : URL to be opened in the browser
# Return Value: SUCCESS/FAILURE

    try:
        print "Opening the requested URL in browser"
        hub_url = "http://%s:4444/wd/hub" %tdkbE2EUtility.hub_machine_ip
        driver = webdriver.Remote(browser_profile=profile,command_executor=hub_url)
        driver.get(GridUrl);
        checkUI = driver.find_element_by_xpath('//*[@id="get_set_up"]').text
        if "Let's Get Set Up" == checkUI:
            tdkTestObj.setResultStatus("SUCCESS");
            Status = "SUCCESS"
            print "SUCCESS: Successfully opened the captive portal UI page\n"
        else:
            Status = "FAILURE"
            tdkTestObj.setResultStatus("FAILURE");
            print "FAILURE: Failed to open the captive portal login page\n"
    except Exception as error:
        print "Got Exception at the function openCaptivePortal()"
        print error;
        driver.quit();
        Status = "FAILURE"
    return Status,driver;

#---------------------------------------------------------------------------------
#End of function
#---------------------------------------------------------------------------------
def isUIAvailable(GridUrl,tdkTestObj):

# syntax       : isUIAvailable()
# Description  : This function will handle the invalid scenarios like the MSO UI must not be available in ethwan mode
# Parameters  : expectedResult : SUCCESS/FAILURE
#               GridUrl : URL to be opened in the browser
# Return Value: SUCCESS/FAILURE

    try:
        print "Opening the requested URL in browser"
        hub_url = "http://%s:4444/wd/hub" %tdkbE2EUtility.hub_machine_ip
        driver = webdriver.Remote(browser_profile=profile,command_executor=hub_url)
        driver.get(GridUrl);
        Status = "FAILURE"
        driver.quit()
    except Exception as error:
        print "Got Exception in opening the UI page"
        print error;
        Status = "SUCCESS"
    return Status,driver;
