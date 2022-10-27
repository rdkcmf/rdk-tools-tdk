#!/bin/bash
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

##Update local packages list
apt-get update

##Setting up tools for building Lightning Apps   

#Install npm  
apt install npm -y

#Install node using npm
npm install -g n

#Update if version not latest
n latest 
npm install -g npm@latest

#Update 
apt -y update && apt -y upgrade

#Make it as stable version
n stable
NODE_VERSION=$(node --version | sed 's/v\([0-9]*\).*/\1/g')
echo "Stable node version: $NODE_VERSION"
#download nodejs stable version
curl -sL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash -
#Install nodejs
apt-get install -y nodejs

#Install Lightning CLI tool
npm install -g rdkcentral/Lightning-CLI

#verify the npm and node versions
echo "npm version:"
npm --version || echo "npm is not installed."
echo "node version:"
node --version || echo "node is not installed."
echo "Commands for installing npm, node and Lightning-CLI are executed."

##Restart Tomcat7

echo "Restarting the Tomcat7..."
echo "Stopping Tomcat..."
/etc/init.d/tomcat7 stop
echo "Startng Tomcat..."
/etc/init.d/tomcat7 start
echo "Please wait, continuing in a minute..."
sleep 50

#function for npm
build_lightning_apps()
{	echo "build_lightning_apps"
	npm i
	lng build
	rm -rf node_modules
	cd ..
}

##Building the Lightning Apps

DIR="/opt/apache-tomcat-7.0.96/webapps/rdk-test-tool"
if [ -d "$DIR" ]; then
	echo "The directory ${DIR} exists, proceeding to build Lightning apps..."
	#Setting up and building Lightning Apps in their given path

	#Permission to read and execute access for everyone
	chmod -R 755 /opt/apache-tomcat-7.0.96/webapps/rdk-test-tool/fileStore/lightning-apps

	echo "Building App tdkunifiedplayer..."
	cd /opt/apache-tomcat-7.0.96/webapps/rdk-test-tool/fileStore/lightning-apps/tdkunifiedplayer
        build_lightning_apps
		
	echo "Building App tdkanimations..."
	cd tdkanimations/
	build_lightning_apps

	echo "Building App tdkmultianimations..."
	cd tdkmultianimations/
	build_lightning_apps
	
	echo "Building App tdkobjectanimations..."
	cd tdkobjectanimations/
	build_lightning_apps

	echo "Building App tdkipchange..."
	cd tdkipchange/
	build_lightning_apps
	
	echo "Lightning apps are built. Please verify by launching the apps with below urls..."
echo -e "For tdkunifiedplayer: http://<TM_IP>:<port>/rdk-test-tool/fileStore/lightning-apps/tdkunifiedplayer/build/index.html?\nplayer=hlsjs&url=<video_src_url>&operations=pause(10),play(10)&autotest=true&type=hls"
echo -e "For tdkanimations: http://<TM_IP>:<port>/rdk-test-tool/fileStore/lightning-apps/tdkanimations/build/index.html?\noperations=pause(10),play(10),stop(10),stopNow(10)&autotest=true&ip=xx.xx.xx.xxxx&port=9998"
echo -e "For tdkmultianimations: http://<TM_IP>:<port>/rdk-test-tool/fileStore/lightning-apps/tdkmultianimations/build/index.html?\nip=xx.xx.xx.xx&threshold=10&fps=30&autotest=true&duration=60&testtype=generic&port=9998"
echo -e "For tdkobjectanimations: http://<TM_IP>:<port>/rdk-test-tool/fileStore/lightning-apps/tdkobjectanimations/build/index.html?\nip=xx.xx.xx.xx&port=9998&object=Text&text=demo&duration=60count=500&showfps=true&autotest=true",
echo -e "For tdkipchange: http://<TM_IP>:<port>/rdk-test-tool/fileStore/lightning-apps/tdkipchange/build/index.html?\ntmURL=<TM_URL>&deviceName=<Name_of_device_in_TM>&tmUserName=<user_name>&tmPassword=<password>&ipAddressType=<ipv4 or ipv6>"
else
	echo "Error: ${DIR} not found. Can not continue."
	exit 1
fi
