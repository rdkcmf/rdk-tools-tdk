#!/usr/bin/python
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
#

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

from selenium import webdriver;
import pexpect
from pexpect import pxssh
import tdkcConfigParserUtility;
from tdkcConfigParserUtility import *;
import subprocess
import time
import os

#------------------------------------------------------------------------------
# Global variables
#------------------------------------------------------------------------------
isSessionActive = False


#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------
def startHub():
# Syntax      : startHub()
# Description : Function to start the selenium hub in TM machine
# Parameters  : None
# Return Value: SUCCESS/FAILURE

    try:
        start_selenium_script = tdkcConfigParserUtility.start_selenium_script;
        hub_selenium_path = tdkcConfigParserUtility.hub_selenium_path;
        hub_machine_ip = tdkcConfigParserUtility.hub_machine_ip;
        hub_logfile = tdkcConfigParserUtility.hub_logfile;

        command = "sh %s start_hub %s %s %s" %(start_selenium_script,hub_selenium_path,hub_machine_ip,hub_logfile)
        print "Command Executed : " ,command
        output = subprocess.check_output(command,shell=True)
    except Exception as error:
        print "Got Exception at the function startHub()"
        print error;
        output = "Unable to start selenium hub in TM machine. Please check if any instances are already running."
    return output



def startNode():
# Syntax      : startNode()
# Description : Function to start node from client machine
# Return Value: SUCCESS/FAILURE
    try:
        start_selenium_script = tdkcConfigParserUtility.start_selenium_script_client;
        hub_machine_ip = tdkcConfigParserUtility.hub_machine_ip;
        node_machine_ip = tdkcConfigParserUtility.node_machine_ip;
        node_selenium_path = tdkcConfigParserUtility.node_selenium_path
        node_logfile = tdkcConfigParserUtility.node_logfile

        command = "sh %s start_node %s %s %s %s" %(start_selenium_script,node_selenium_path,hub_machine_ip,node_logfile,node_machine_ip)
        status = clientConnect()
        if status == "SUCCESS":
            print "Command Executed : " ,command
            status = executeCommand(command)
    except Exception as error:
        print "Got Exception at the function startNode()"
        print error;
        status = "Unable to start selenium in node machine. Please check if any instances are already running."
    return status


def executeCommand(command):
# executeCommand
# Syntax      : executeCommand()
# Description : Function to execute the command
# Parameters  : command - Command to be executed
# Return Value: SUCCESS/FAILURE
	try:
                session.sendline(command)
                session.prompt()
                status=session.before
		status=status.strip()
		print "Command Output : %s" %status
		if "OUTPUT:" in status:
			status=status.split(":")[1]
		else:
			status = "FAILURE"
        except Exception, e:
	       print e;
               status = "FAILURE";
        return status;


def clientConnect():
# clientConnect
# Syntax      : clientConnect()
# Description : Function to connect to the client machine.
# Return Value: SUCCESS/FAILURE
    try:
        status = "SUCCESS";
        global session;
        global isSessionActive;
        node_machine_ip = tdkcConfigParserUtility.node_machine_ip;
        node_username   = tdkcConfigParserUtility.node_username;
        node_password   = tdkcConfigParserUtility.node_password;

        print "Connecting to client machine ..."
        session = pxssh.pxssh(options={
                  "StrictHostKeyChecking": "no",
                  "UserKnownHostsFile": "/dev/null"})

        isSessionActive = session.login(node_machine_ip,node_username,node_password);

    except Exception, e:
        print e;
        status = "FAILURE"
    print "Connection to client machine : %s" %status;
    return status;


def clientDisconnect():
# clientDisconnect
# Syntax      : clientDisconnect()
# Description : Function to disconnect from the client machine
# Parameters  : None
# Return Value: SUCCESS/FAILURE
       	try:
		status = "SUCCESS"
                global isSessionActive;
		if isSessionActive == True:
               		session.logout()
			session.close()
		else:
			status = "No active session"
       	except Exception, e:
		print e;
          	status = e;
	print "Disconnect from client machine:%s" %status;
	return status;


def kill_hub_node():
# Syntax      : kill_hub_node()
# Description : Function to kill hub and node before exiting the script
# Return Value: SUCCESS/FAILURE
    
    print "Killing hub"
    p = subprocess.call([tdkcConfigParserUtility.start_selenium_script, 'kill_selenium'])
    print "Killing node"
    status = clientConnect()
    if status == "SUCCESS":
        command = "source %s kill_selenium" %(tdkcConfigParserUtility.start_selenium_script_client)
        status = executeCommand(command)
        status = clientDisconnect()
        return status
    else:
        return "FAILURE"


def startSeleniumGrid(tdkTestObj,GridUrl,CheckUIXpath,CheckUIData,LoginStatus = "LocalLogin"):
# Syntax      : startSeleniumGrid()
# Description : This will start selenium hub and node in machines
# Parameters  : GridUrl : URL to be opened in the browser
#               LoginStatus : Login/NoLogin
# Return Value: SUCCESS/FAILURE
    try:
        Status = "FAILURE"
        driver = "Failed to initialize the webdriver"
        global profile;
        #Kill selenium hub and node as a pre-requisite before starting new hub and node
        print "\nSetting WebUI pre-requisite"
        Prerequ_Status = kill_hub_node()
        if "SUCCESS" in Prerequ_Status:
            print "SUCCESS: WebUI pre-requisite set successfully"

            print "\nStarting the Selenium Hub in TM machine"
            status = startHub()
            if "SUCCESS" in status:
                print "SUCCESS: Selenium Hub started successfully"

                print "\nStarting Selenium Node in client/host machine"
                status = startNode()
                if "SUCCESS" in status:
                    print "SUCCESS: Node Started successfully"

                    profile = webdriver.FirefoxProfile()
                    if LoginStatus == "NoLogin":
                            Status,driver = openLocalWebUI(tdkTestObj,GridUrl,LoginStatus,CheckUIXpath,CheckUIData);
                else:
                    print "FAILURE: Failed to start node in client machine\n"
            else:
                print "FAILURE: Failed to start the selenium hub\n"
        else:
            print "FAILURE: Failed to set WebUI pre-requisite\n"
    except Exception as error:
        print "Got Exception at the function startSeleniumGrid()"
        print error;
        driver = "Failed to set the driver"
        Status = "FAILURE"
    return driver,Status;

def openLocalWebUI(tdkTestObj,GridUrl,LoginStatus,CheckUIXpath,CheckUIData):
# syntax       : openLocalWebUI()
# Description  : This function is to open the given URL in the browser of client machine
# Parameters   : LoginStatus : Login/NoLogin
#                GridUrl : URL to be opened in the browser
#                CheckUIXpath : xpath of the element to be checked
#                CheckUIData  : data to be compared with text in UI          
# Return Value: SUCCESS/FAILURE
    try:
        print "\nOpening the requested URL in browser"
        hub_url = "http://%s:4444/wd/hub" %tdkcConfigParserUtility.hub_machine_ip
        driver = webdriver.Remote(browser_profile=profile,command_executor=hub_url)
        driver.get(GridUrl);
        time.sleep(5);
        checkUI = driver.find_element_by_xpath(CheckUIXpath).text
        print "URL Requested : "    ,driver.current_url
        print "Data from Web UI : " ,checkUI
        if checkUI == CheckUIData:
            print "SUCCESS: opened the web UI page Successfully"
            if LoginStatus == "NoLogin":
                Status = "SUCCESS"
        else:
            Status = "FAILURE"
            print "FAILURE: Failed to open the web login page"
    except Exception as error:
        print "Got Exception at the function openLocalWebUI()"
        print error;
        kill_web_driver(driver)
        Status = "FAILURE"
    return Status,driver;


def IsWEBDriverActive(driver):
# syntax       : IsWEBDriverActive()
# Description  : Function to check whether driver is quit or not
# Parameters   : driver - selenium web driver
# Return Value : TRUE/FALSE
    try:
        URL = driver.current_url
        print "Current URL :",URL
        print "Current session ID : ",driver.session_id
        return "TRUE"
    except Exception as error:
        print (str(error).split("Stacktrace:",1)[0].replace("\\n","").replace("\n",""))
        return "FALSE"

def kill_web_driver(driver):
# syntax       : kill_web_driver()
# Description  : Function to quit the web-driver
# Parameters   : driver - selenium web driver
# Return Value : SUCCESS/FAILURE

    Status = "SUCCESS"
    print "Kill web-driver"
    if IsWEBDriverActive(driver) == "TRUE":
        print "Killing selenium web-driver ..."
        driver.quit();
        time.sleep(3);
        if IsWEBDriverActive(driver) == "FALSE":
            print "SUCCESS: Selenium web-driver killed successfully\n"
        else:
            Status = "FALSE"
            print "FAILURE: Selenium web-driver kill failed\n"
    else:
        print "SUCCESS: Selenium web-driver killed already\n"
    return Status


def setWebRTCInfoInWEBUI(driver):
# Syntax      : setWebRTCInfoInWEBUI()
# Description : Method to set webrtc info in demo page
# Parameters  : driver - selenium web-driver
# Return Value: SUCCESS/FAILURE

    try:
        Status = "SUCCESS"
        print "Setting WebRTC info ..."
        print "ers IP = "     ,tdkcConfigParserUtility.ersIP
        print "ers Port = "   ,tdkcConfigParserUtility.ersPort
        print "roomName = "   ,tdkcConfigParserUtility.roomName
        print "streamName = " ,tdkcConfigParserUtility.streamName

        driver.find_element_by_id("ersIp6").clear();
        driver.find_element_by_id("ersPort6").clear();
        driver.find_element_by_id("roomName6").clear();
        driver.find_element_by_id("streamName6").clear();
        driver.find_element_by_id("ersIp6").send_keys(tdkcConfigParserUtility.ersIP);
        driver.find_element_by_id("ersPort6").send_keys(tdkcConfigParserUtility.ersPort);
        driver.find_element_by_id("roomName6").send_keys(tdkcConfigParserUtility.roomName);
        driver.find_element_by_id("streamName6").send_keys(tdkcConfigParserUtility.streamName);
        driver.find_element_by_xpath(tdkcConfigParserUtility.debug).click()
    except Exception as error:
        print "Got Exception at the function setWebRTCInfoInWEBUI()"
        print error;
        kill_web_driver(driver)
        Status = "FAILURE"
    return Status


def getWebRTCInfoInWEBUI(driver):
# Syntax      : getWebRTCInfoInWEBUI()
# Description : Method to get webrtc info from demo page
# Parameters  : driver - selenium web-driver
# Return Value: SUCCESS/FAILURE

    try:
        Status = "SUCCESS"
        print "Getting WebRTC info ..."
        ersIP = driver.find_element_by_id("ersIp6").get_attribute('value')
        ersPort = driver.find_element_by_id("ersPort6").get_attribute('value')
        roomName = driver.find_element_by_id("roomName6").get_attribute('value')
        streamName = driver.find_element_by_id("streamName6").get_attribute('value')
        debugLog = driver.find_element_by_xpath(tdkcConfigParserUtility.debug).get_attribute('checked')
        Info = [ ersIP, ersPort, roomName, streamName, debugLog ]
    except Exception as error:
        print "Got Exception at the function getWebRTCInfoFromWEBUI()"
        print error;
        kill_web_driver(driver)
        Info = []
        Status = "FAILURE"
    return Status,Info


def verifyWebRTCInfoInWEBUI(driver):
# Syntax      : verifyWebRTCInfoInWEBUI()
# Description : Method to check whether webrtc info set
#               is availabe in demo page
# Parameters  : driver - selenium web-driver
# Return Value: SUCCESS/FAILURE

    Status,Info = getWebRTCInfoInWEBUI(driver)
    if Status == "SUCCESS":
        ersIP = tdkcConfigParserUtility.ersIP
        ersPort = tdkcConfigParserUtility.ersPort
        roomName = tdkcConfigParserUtility.roomName
        streamName = tdkcConfigParserUtility.streamName
        if Info[0] == ersIP and Info[1] == ersPort and Info[2] == roomName and Info[3] == streamName and Info[4] == "true":
            setStatus = "SUCCESS"
        else:
            setStatus = "FAILURE"
    else:
        setStatus = "FAILURE"
    return setStatus


def playStreamInWEBUI(driver):
# Syntax      : playStreamInWEBUI()
# Description : Method to click play button in UI
# Parameters  : driver - selenium web-driver
# Return Value: SUCCESS/FAILURE

    try:
        Status = "SUCCESS"
        print "Going to Play the Stream ..."
        playButtonEnable = driver.find_element_by_id("play6").is_enabled()
        if "True" in str(playButtonEnable):
            print "Play button Enabled : True , Status : Not Clicked"
            print "Clicking Play button ..."
            driver.find_element_by_id("play6").click()
            time.sleep(30)
            playButtonEnable = driver.find_element_by_id("play6").is_enabled()
            if "False" in str(playButtonEnable):
                Status = "SUCCESS"
                print "Play button Enabled : False , Status : Clicked"
            else:
                Status = "FAILURE"
                print "Play button Enabled : True , Status : Not Clicked"
        else:
            Status = "FAILURE"
            print "Play button Enabled : False"
    except Exception as error:
        print "Got Exception at the function playStreamInWEBUI()"
        print error;
        kill_web_driver(driver)
        Status = "FAILURE"
    return Status


def pauseStreamInWEBUI(driver):
# Syntax      : pauseStreamInWEBUI()
# Description : Method to click pause button in UI
# Parameters  : driver - selenium web-driver
# Return Value: SUCCESS/FAILURE

    try:
        Status = "SUCCESS"
        print "Going to Pause the Stream ..."
        pauseButtonEnable = driver.find_element_by_id("pause6").is_enabled()
        if "True" in str(pauseButtonEnable):
            print "Pause button Enabled : True , Status : Not Clicked"
            print "Clicking Pause button ..."
            driver.find_element_by_id("pause6").click()
            time.sleep(30)
            pauseButtonEnable = driver.find_element_by_id("pause6").is_enabled()
            if "False" in str(pauseButtonEnable):
                Status = "SUCCESS"
                print "Pause button Enabled : False , Status : Clicked"
            else:
                Status = "FAILURE"
                print "Pause button Enabled : True , Status : Not Clicked"
        else:
            Status = "FAILURE"
            print "Pause button Enabled : False"
    except Exception as error:
        print "Got Exception at the function pauseStreamInWEBUI()"
        print error;
        kill_web_driver(driver)
        Status = "FAILURE"
    return Status


def stopStreamInWEBUI(driver):
# Syntax      : stopStreamInWEBUI()
# Description : Method to click stop button in UI
# Parameters  : driver - selenium web-driver
# Return Value: SUCCESS/FAILURE

    try:
        Status = "SUCCESS"
        print "Going to Stop the Stream ..."
        stopButtonEnable = driver.find_element_by_id("stop6").is_enabled()
        if "True" in str(stopButtonEnable):
            print "Stop button Enabled : True , Status : Not Clicked"
            print "Clicking Stop button ..."
            driver.find_element_by_id("stop6").click()
            time.sleep(30)
            stopButtonEnable = driver.find_element_by_id("stop6").is_enabled()
            if "False" in str(stopButtonEnable):
                Status = "SUCCESS"
                print "Stop button Enabled : False , Status : Clicked"
            else:
                Status = "FAILURE"
                print "Stop button Enabled : True , Status : Not Clicked"
        else:
            Status = "FAILURE"
            print "Stop button Enabled : False"
    except Exception as error:
        print "Got Exception at the function stopStreamInWEBUI()"
        print error;
        kill_web_driver(driver)
        Status = "FAILURE"
    return Status


def getDebugMsgInWEBUI(driver):
# Syntax      : getDebugMsgInWEBUI()
# Description : Method to get debug log msg from browser
# Parameters  : driver - selenium web-driver
# Return Value: SUCCESS/FAILURE

    try:
	Status = "SUCCESS"
        print "Getting web UI debug message"	
        Msg = driver.find_element_by_id("debug6").text
    except Exception as error:
        print "Got Exception at the function getDebugMsgInWEBUI()"
        print error;
        kill_web_driver(driver)
        Msg = ""
        Status = "FAILURE"
    return Status,Msg


