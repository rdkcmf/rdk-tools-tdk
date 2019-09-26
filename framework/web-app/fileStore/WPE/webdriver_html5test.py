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
        b.launchBrowser(driver, "https://html5test.com")

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "pointsPanel")))

        elems = driver.find_elements_by_xpath("//table[contains(@id, 'table-')]")
        n = 0
        valuesList = []
        html5Tests = []
        while n < len(elems):
            elem = elems[n].find_element_by_xpath("thead/tr/th/div/div[@class='grade']")
            score_full = elem.text.replace("\\n", "").strip('"')
            score = score_full.split("/")
            valuesList.append(score[0])
            elem = elems[n].find_element_by_css_selector("th")
            title = elem.text.replace("\\n", "").strip('"')
            html5Tests.append(title[0:len(title)-len(score_full)])
            n = n + 1

        elem = driver.find_element_by_css_selector(".pointsPanel h2 strong")
        b.saveValuesToCSVFile("html5testmark", elem.text.strip('"'), 'plothtml5testmarkMain.csv')

        labels = ",".join(map(str, html5Tests))
        values = ",".join(valuesList)

        b.saveValuesToCSVFile(labels, values, 'plotHtml5test.csv')

    finally:
        b.quitDriver(driver)


