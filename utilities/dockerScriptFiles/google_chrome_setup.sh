##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2022 RDK Management
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

#!/bin/bash

##Download Google Chrome

echo "Downloading Google Chrome..."
PACKAGE_NAME=google-chrome-stable_106.0.5249.119-1_amd64.deb
wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/${PACKAGE_NAME} && echo "Google Chrome is downloaded."
#Stop automatic updates of Google Chrome
touch /etc/default/google-chrome
#Installing Google Chrome
echo "Installing Google Chrome..."
dpkg -i $PACKAGE_NAME
#Fix if any error occurs during installation
apt --fix-broken install -y
#Get Google Chrome version (stored in variable)
echo "Get Google Chrome version"
CHROME_VERSION=$(google-chrome --version | awk '{print $3}') || echo "Google Chrome is not installed."
echo $CHROME_VERSION
CHROME_VERSION_MAJOR=$(google-chrome --version | sed 's/Google Chrome \([0-9]*\).*/\1/g')

##Download chromedriver

#Download chromedriver with same version as that of Google Chrome
echo "Downloading chromedriver having version same as that of Google Chrome..."
DRIVER_VERSION="`wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION_MAJOR}`"
echo "chromedriver version: $DRIVER_VERSION"
wget https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip && echo "chromedriver downloaded succesfully"
#Extract chromedriver in directory tdk/selenium_path
mkdir tdk
cd tdk/
mkdir selenium_path
cd /
mv chromedriver_linux64.zip /tdk/selenium_path/
cd tdk/selenium_path
echo "Extracting chromedriver in :/tdk/selenium/ path"
unzip chromedriver_linux64.zip && echo "Extracted the chromedriver_linux64.zip."
cp /tdk/selenium_path/chromedriver /usr/local/bin/
sleep 2
DRIVER_VERSION=$(chromedriver --version)
echo $DRIVER_VERSION

##Compare the installed version of Google Chrome and chromedriver

DRIVER_VERSION_MAJOR=$(chromedriver --version | sed 's/ChromeDriver \([0-9]*\).*/\1/g')
echo "Google Chrome version major: $CHROME_VERSION_MAJOR"
echo "chromedriver version major: $DRIVER_VERSION_MAJOR"
if [ $CHROME_VERSION_MAJOR != $DRIVER_VERSION_MAJOR ]; then
    echo "VERSION MISMATCH";
    exit 1;
else
    echo "Verified that Google Chrome and chromedriver versions are compatible."
fi

##Execute permissions for chromedriver path

echo "Execute permission for chromedriver path"
cd /tdk
chmod 777 selenium_path
chmod 777 selenium_path/chromedriver
cd ..

echo "Google Chrome setup is done."