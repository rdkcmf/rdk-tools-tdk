#!/bin/bash
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2017 RDK Management
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

#To send http request to a network
wget_http_network()
{
        value="$(wget --bind-address=$var2 -q --tries=1 -T 60 http://$var3:$var4 && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#To send https request to a network
wget_https_network()
{
        value="$(wget --bind-address=$var2 -q --tries=1 -T 60 https://$var3:$var4 --no-check-certificate && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

# FTP to the client devices
ftpToClient()
{
value="$(SERVER=$var2
USER=$var3
PASSW=$var4
ftp -v -n $SERVER <<END_OF_SESSION
user $USER $PASSW
END_OF_SESSION
)"
echo "OUTPUT:$value"
}

# To set the TCP server in listening mode
tcp_init_server()
{
        iperf -s -B $var3 > $var2 &
        value="$(ps aux | grep iperf | grep -v grep > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}
#To send TCP request from client to server
tcp_request()
{
        iperf -c $var2 -B $var3 > $var4 2>&1
        bindStatus="$(cat $var4 | grep "bind failed:" && echo "FAILURE" || echo "SUCCESS")"
        echo "bindStatus:$bindStatus"
        if [ $bindStatus = "SUCCESS" ]; then
                value="$(cat $var4 | grep bits/sec | cut -d ' ' -f 11)"
                echo "OUTPUT:$value"
        else
                echo "OUTPUT:"
        fi
}
#To get the bandwidth from server
validate_tcp_server_output()
{
        serverOutput="$(cat $var2 | grep bits/sec | cut -d ' ' -f 11)"
        echo "OUTPUT:$serverOutput"
        deleteTmpFile="$(sudo rm $var2 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
}
#To get the throughput from server
validate_tcp_server_output_throughput()
{
        serverOutput="$(cat $var2 | grep bits/sec | cut -d ' ' -f 11)"
        size="$(cat $var2 | grep bits/sec | cut -d ' ' -f 12)"
        echo "OUTPUT:$serverOutput $size"
        deleteTmpFile="$(sudo rm $var2 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
}

#To start iperf server in one of the clients
tcp_init_server_perf()
{
        iperf -s -B $var3 -t $var4 -i $var5 > $var2 &
        value="$(ps aux | grep iperf | grep -v grep > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#To start iperf client in machine to be tested
tcp_request_perf()
{
        iperf -f m -c $var2 -B $var3 -t $var5 -i $var6 > $var4 2>&1 &
}

#To parse the output from iperf client and find the throughput data of machine under test
tcp_get_client_throughput()
{
        bindStatus="$(cat $var2 | grep "bind failed:" && echo "FAILURE" || echo "SUCCESS")"
        echo "bindStatus:$bindStatus"
        if [ $bindStatus = "SUCCESS" ]; then
                value="$(cat $var2 | grep bits/sec | awk '{ print $7 }' | tr '\n' ',')"
                #remove the trailing ,
                value=${value%?}
                #save the throughput output into a file
                echo $value>$var3
                echo "OUTPUT:$value"
        else
                echo "OUTPUT:"
        fi
}

#To kill iperf pid
kill_iperf()
{
        pkill iperf
        value="$(ps aux | grep iperf | grep -v "grep" > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}
#To start node
start_node()
{
        export DISPLAY=:0
        java -jar $var2 -role node -host $var5 -hub http://$var3:4444/grid/register/ > $var4 2>&1 &
        sleep 20
        value="$(cat $var4 | grep "The node is registered to the hub and ready to use" > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}
#To kill the selenium hub and node
kill_selenium()
{
        sudo kill -9 `echo $(ps -ef | grep selenium | grep -v grep|awk '{print $2;}')`
}

# Store the arguments to a variable
event=$1
var2=$2
var3=$3
var4=$4
var5=$5
var6=$6

# Invoke the function based on the argument passed
case $event in
   "wget_http_network")
        wget_http_network;;
   "wget_https_network")
        wget_https_network;;
   "ftpToClient")
        ftpToClient;;
   "tcp_init_server")
	tcp_init_server;;
   "tcp_request")
	tcp_request;;
   "validate_tcp_server_output")
	validate_tcp_server_output;;
   "validate_tcp_server_output_throughput")
	validate_tcp_server_output_throughput;;
   "tcp_init_server_perf")
        tcp_init_server_perf;;
   "tcp_request_perf")
        tcp_request_perf;;
   "tcp_get_client_throughput")
        tcp_get_client_throughput;;
   "kill_iperf")
        kill_iperf;;
    "start_node")
        start_node;;
    "kill_selenium")
        kill_selenium;;
   *) echo "Invalid Argument passed";;
esac

