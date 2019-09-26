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
        b.launchBrowser(driver, 'http://bubblemark.com/dhtml.htm')

        bubbleTests = [1,8,16,32,64,128]
        valuesList = []

        n = 0
        while n < len(bubbleTests):
            driver.execute_script('var element = document.getElementsByTagName("select")[0];' \
                    'element.value = {:d}; element.dispatchEvent(new Event("change"));'.format(bubbleTests[n]));
            time.sleep(10)
            elem = driver.find_element_by_id("dhtml_fps")
            score = elem.text.replace("\\n", "").strip('"').split(" ")
            valuesList.append(score[0])
            n = n + 1

        b.saveValuesToCSVFile("bubblemark", valuesList[4], 'plotBubblemarkMain.csv')

        labels = ",".join(map(str, bubbleTests))
        values = ",".join(valuesList)

        b.saveValuesToCSVFile(labels, values, 'plotBubblemark.csv')

    finally:
        b.quitDriver(driver)


