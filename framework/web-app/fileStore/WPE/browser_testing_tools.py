##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2018 SoftAtHome
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

import os
import pkg_resources
import getopt
import sys
import datetime
import time
from junit_xml import (TestCase, TestSuite)

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import logging
from selenium.webdriver.remote.remote_connection import LOGGER
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Browser names list
BROWSER_QTWEBKIT = 'qtwebkit'
BROWSER_WPE = 'wpe'
DEFAULT_BROWSER = BROWSER_WPE

class BrowserTestingTools:
    # default browser
    browser = DEFAULT_BROWSER

    config = {
        # This element contains the target IP address to use
        'target': None,
        # This element contains the port to use
        'port': None,
    }

    def __usage(self):
       print "Run unit tests"
       print "python [-t] target_ip_addr [-p] target_ip_port"
       print "options:"
       print "-t, --target : target ip address"
       print "-p, --port : target ip port"
       print "-b, --browser : browser name"
       return

    def __init__(self, argv):
        try:
            opts, args = getopt.getopt(argv[1:], "ht:p:b:",
                 ["help", "target=", "port=", "browser="])
        except getopt.GetoptError, err:
            self.__usage()
            sys.exit(2)

        for o, a in opts:
            if o in ("-h", "--help"):
                self.__usage()
            elif o in ("-t", "--target"):
                self.config['target'] = a
            elif o in ("-p", "--port"):
                self.config['port'] = a
            elif o in ("-b", "--browser"):
                self.browser = a.lower()
            else:
                print "unknown option"
                self.__usage()
        if self.config['target'] == None:
            self.__usage()
            sys.exit()
        if self.config['port'] == None:
            if self.browser == BROWSER_WPE:
                self.config['port'] = 9518
            elif self.browser == BROWSER_QTWEBKIT:
                self.config['port'] = 9517
            else:
                self.__usage()
                sys.exit()

    def createDriver(self):
        caps = {}
        caps['browserName'] = 'Safari'
        if self.browser == BROWSER_QTWEBKIT:
            # Reuse current WebView in qtrabrowser
            caps['browserStartWindow'] = ''
            # Allow to run multiple WebDriver sessions in sequence
            # within the same qtrabrowser process
            caps['reuseUI'] = True
        return webdriver.Remote(desired_capabilities=caps,
                command_executor="http://{0}:{1}/".format(self.config['target'], self.config['port']))

    def launchBrowser(self, driver, url):
        driver.get(url)
        # We will wait up to 10 seconds for page loading
        WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    def quitDriver(self, driver):
        # For QtWebKit browser we want to keep
        # the sames windows to avoid qtrabrowser
        # process be killed at the call of this
        # function.
        if self.browser != BROWSER_QTWEBKIT:
            driver.quit()

    def saveValuesToCSVFile(self, labels, values, fileName):
        f = open(fileName,'w')
        f.write(labels + "\n")
        f.write(values)
        f.close()
        return

    def saveValuesToJUnitFormatXMLFile(self, names, status, className, xmlFileName):
        assert len(names) == len(status), "len(names) != len(status)"

        tcs = []
        i = 0
        while i < len(names):
            tc = TestCase(names[i], className)
            if status[i] == 0:
                tc.add_error_info("test failed");
            tcs.append(tc)
            i = i + 1
        ts = [TestSuite(className + "-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S"), tcs)]
        with open(xmlFileName, 'w') as f:
            TestSuite.to_file(f, ts)
        return

    def find_elements_by_xpath(self, driver, xpath):
        # This appears to be an issue with the element not actually loading in time for selenium to locate it.
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        return driver.find_elements(By.XPATH, xpath)

