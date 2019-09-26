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

import string

if __name__ == '__main__':

    b = BrowserTestingTools(sys.argv)
    driver = b.createDriver()

    try:
        b.launchBrowser(driver, "http://browserbench.org/Speedometer/")

        elem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "buttons")))

        button = elem.find_element_by_xpath("button");

        button.send_keys(Keys.ENTER);

        j = 0
        while j < 500:
            elem = driver.find_element_by_xpath("//div[@id='progress-completed']")
            if elem.get_attribute("style") == "width: 100%;":
                break
            time.sleep(2)
            j = j + 1

        elem = driver.find_element_by_id("result-number")

        fo = open("plotSpeedometerMain.csv", "wb")
        fo.write("Runs / Minute\n")
        fo.write(elem.text.strip('"'))
        fo.close()

    finally:
        b.quitDriver(driver)


