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

#Update local packages list
apt update

# install node
node_version=16.x
curl -sL https://deb.nodesource.com/setup_{$node_version} | bash
apt-get install -y nodejs
npm set unsafe-perm true

#verify the npm and node versions
echo "npm version:"
npm --version || echo "npm is not installed."
echo "node version:"
node --version || echo "node is not installed."

#Install Lightning CLI tool
npm install -g rdkcentral/Lightning-CLI

echo "Commands for installing npm, node and Lightning-CLI are executed."

#Restart Tomcat7
echo "Restarting the Tomcat7..."
echo "Stopping Tomcat..."
/etc/init.d/tomcat7 stop
echo "Startng Tomcat..."
/etc/init.d/tomcat7 start
echo "Please wait, continuing in a minute..."
sleep 50

#function for building Lightning App
build_lightning_app()
{
	echo "Building $2 ..."
	cd $1
	npm i
	build_response=$(lng build) && echo $build_response
	rm -rf node_modules
		if [[ ! -z "$build_response" && $build_response != *"Error"* ]]; then
			echo "$2 is built successfully"
		else
			echo "Error: Problem in building $2" >>/dev/stderr
			exit 1
		fi
	cd ..
}

#Building the Lightning Apps
DIR="/opt/apache-tomcat-7.0.96/webapps/rdk-test-tool"
if [ -d "$DIR" ]; then
	echo "The WAR File is extracted and proceeding to build Lightning apps..."
	#Setting up and building Lightning Apps in their given path

	#Permission to read and execute access for everyone
	chmod -R 755 /opt/apache-tomcat-7.0.96/webapps/rdk-test-tool/fileStore/lightning-apps
	cd /opt/apache-tomcat-7.0.96/webapps/rdk-test-tool/fileStore/lightning-apps/

	build_lightning_app "tdkunifiedplayer" "TDK Unified Player"
		
	build_lightning_app "tdkanimations" "TDK Animations Player"

	build_lightning_app "tdkmultianimations" "TDK Multi Animations"
	
	build_lightning_app "tdkobjectanimations" "TDK Object Animations"

	build_lightning_app "tdkipchange" "TDK IP Change"
	
	echo "Lightning Apps are Built Successfully"
else
	echo "Error: ${DIR} not found. Can not continue." >>/dev/stderr
	exit 1
fi
