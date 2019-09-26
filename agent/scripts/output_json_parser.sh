##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
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

SCRIPT_PATH=$TDK_PATH/script/
LOG_PATH=$TDK_PATH/
LOGFILE=output_json_parser_details.log
STREAMING_IP=$1
BASE_URL=$2

echo "Streaming IP :" $STREAMING_IP
echo "Base Url     :" $BASE_URL

#Parse xdiscovery.conf file to get the location of output.json file
outputjsonfile=`cat $XDISCOVERY_PATH/xdiscovery.conf|grep outputJsonFile=|grep -v "#"|awk -F "=" '{print $2}' | tr -d '\r\n'`
echo "Location of output.json file="$outputjsonfile
if [ $? == 0 ] && [ "$outputjsonfile" != "" ]; then
        echo "SUCCESS<DETAILS>Parsed output.json location" > $LOG_PATH/$LOGFILE
	if [ -e $outputjsonfile ]; then
        	echo $outputjsonfile "file found"
        	echo "SUCCESS<DETAILS>"$outputjsonfile" file found" >> $LOG_PATH/$LOGFILE
        else
        	echo $outputjsonfile "file not found"
        	echo "FAILURE<DETAILS>"$outputjsonfile" file not found" > $LOG_PATH/$LOGFILE
        	exit 1
        fi
else
        echo "FAILURE<DETAILS>Unable to parse output.json location" > $LOG_PATH/$LOGFILE
        exit 1
fi

#Read play url from output.json
if [ "$STREAMING_IP" == "mdvr" ]; then
	playUrl=`cat $outputjsonfile |grep playbackUrl|cut -f2- -d":"|cut -f1 -d "&"|cut -f2 -d "\""|head -1`
	echo "mDVR PlayUrl="$playUrl
        if [ $? == 0 ] && [ "$playUrl" != "" ]; then
                echo "SUCCESS<DETAILS>PlayUrl="$playUrl >> $LOG_PATH/$LOGFILE
        else
                echo "Unable to read play url from output.json"
                echo "FAILURE<DETAILS>Unable to read play url from output.json" >> $LOG_PATH/$LOGFILE
                exit 1
        fi
else 
	playUrl=`cat $outputjsonfile |grep playbackUrl|cut -f2- -d":"|cut -f1 -d "&"|grep $STREAMING_IP|cut -f2 -d "\""`
	echo "StreamingIP PlayUrl="$playUrl
	if [ $? == 0 ] && [ "$playUrl" != "" ]; then
		echo "SUCCESS<DETAILS>PlayUrl="$playUrl >> $LOG_PATH/$LOGFILE
	else
		playUrl=`cat $outputjsonfile |grep playbackUrl|cut -f2- -d":"|cut -f1 -d "&"|grep 127.0.0.1|cut -f2 -d "\""`
		echo "LoopbackIP PlayUrl="$playUrl
        	if [ $? == 0 ] && [ "$playUrl" != "" ]; then
			echo "SUCCESS<DETAILS>PlayUrl="$playUrl >> $LOG_PATH/$LOGFILE
        	else
			displayJson=`cat $outputjsonfile`
			echo "output.json contents:\n"$displayJson
                	echo "FAILURE<DETAILS>Unable to read play url from output.json" >> $LOG_PATH/$LOGFILE
                	exit 1
        	fi
 	fi
fi

#parse the base URL
baseUrl=`echo $BASE_URL |cut -f2 -d "?"`
echo "Service locator="$baseUrl
if [ $? == 0 ] && [ "$baseUrl" != "" ]; then
        echo "SUCCESS<DETAILS>Service locator="$baseUrl >> $LOG_PATH/$LOGFILE
else
        echo "FAILURE<DETAILS>Unable to read service locator from base url" >> $LOG_PATH/$LOGFILE
        exit 1
fi

#Concatenate to get final url
final_url=$playUrl"&"$baseUrl
echo "Final Url="$final_url
echo $final_url >> $LOG_PATH/$LOGFILE
