#!/usr/bin/env python
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

from browser_testing_tools import *

import os
import string
from subprocess import Popen,PIPE,STDOUT,call

if __name__ == '__main__':

    b = BrowserTestingTools(sys.argv)
    driver = b.createDriver()

    try:
        version = "1.0.2"

        b.launchBrowser(driver, "https://webkit.org/perf/sunspider-{:s}/sunspider-{:s}/driver.html".format(version, version))

        WebDriverWait(driver, 360).until(EC.presence_of_element_located((By.NAME, "other")))

        element = driver.find_element_by_id("selfUrl")
        url = element.get_attribute('value').replace("%22v%22:%20%22sunspider-{:s}%22,%20".format(version), "");

        dir_path = os.path.dirname(os.path.realpath(__file__))
        proc = Popen('rhino {0}/sunspider-analyze-results.js \"{1}\"'.format(dir_path, url), shell=True, stdout=PIPE, )
        tmp_str = proc.stdout.readline()

        b.saveValuesToCSVFile("sunspidermark", tmp_str, 'plotsunspidermarkMain.csv')

        labels = proc.stdout.readline()
        values = proc.stdout.readline()
        b.saveValuesToCSVFile(labels.strip('\n'), values, 'plotSunspider.csv')

    finally:
        b.quitDriver(driver)


