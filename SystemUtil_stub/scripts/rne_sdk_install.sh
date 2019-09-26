#!/bin/sh
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2018 RDK Management
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

source test.config
echo $SAMPLE_APP_URL
#Current directory as SDK workspace directory
if [ -e raspberrypi-rdk-hybrid-RNE-SDK-2.0.sh ] 
then
	echo "Found the RNE SDK setup script"
else
        echo "Not able to find the RNE SDK setup script"
	exit
fi

#Remove the sdk_extract folder if already presents
rm -rf sdk_extract

#Executing the shell script to setup the RNE SDK envrionment
./raspberrypi-rdk-hybrid-RNE-SDK-2.0.sh -d sdk_extract -y
if [ $? -eq 0 ];then
	echo "Extracted the SDK Successfully"
else
	echo "Failed to extract the SDK "
	exit
fi

#Sourcing the SDK environment
cd sdk_extract
source environment-setup-cortexa7t2hf-vfp-vfpv4-neon-rdk-linux-gnueabi
cd ../

#Removing the already existing Sample_App folder
rm -rf Sample_App

#Cloning the Sample App 
if [ "x$SAMPLE_APP_URL" = "x" ]; then
	echo "SAMPLE_APP_URL value is empty"
        exit
else
	git clone $SAMPLE_APP_URL Sample_App
	if [ $? -eq 0 ];then
        	echo "Sample code cloned successfully"
	else
        	echo "Failed to clone the Sample code"
        	exit
	fi
fi

#Executing the Sample App building
cd Sample_App/samples/
#Commenting --enable-breakpad in build_samples.sh file
sed -i 's/.*--enable-breakpad/#&/' build_samples.sh
./build_samples.sh
cd ../../

