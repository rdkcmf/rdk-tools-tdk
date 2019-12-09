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
#

# Check whether the SSID to be connected is listed in the network
is_ssid_available()
{
        value="$(nmcli device wifi list | grep $var2)"
        echo "OUTPUT:$value"
}

# Connect to the WIFI SSID
wifi_ssid_connect()
{
        value="$(nmcli device wifi connect $var2 password $var3 | tr -cd [:print:])"
	printf "OUTPUT:$value"
}

# Connect to the WIFI SSID with security mode None
wifi_ssid_connect_openSecurity()
{
        value="$(nmcli device wifi connect $var2 | tr -cd [:print:])"
        printf "OUTPUT:$value"
}
# Disconnect from the WIFI SSID
wifi_ssid_disconnect()
{
        value="$(nmcli device disconnect $var2 | tr -cd [:print:])"
        echo "OUTPUT:$value"
}

# Get the IP address of the WLAN after connecting to WIFI
get_wlan_ip_address()
{
        value="$(ifconfig $var2 | grep "$var3" | cut -d ':' -f 2 | cut -d ' ' -f 1)"
        echo "OUTPUT:$value"
}

# Get the subnet mask of the WLAN after connecting to WIFI
get_wlan_subnet_mask()
{
        value="$(ifconfig $var2 | grep "$var3" | cut -d ':' -f 4 | cut -d ' ' -f 1)"
        echo "OUTPUT:$value"
}

# Get the current SSID name of the WIFI connected
get_connected_ssid_name()
{
        value="$(nmcli device |grep $var2| awk '{ print $4 }')"
        echo "OUTPUT:$value"
}

# Get the current channel number of the WIFI connected
get_channel_number()
{
        value="$(nmcli device wifi list |grep $var2| awk '{ print $4 }')"
        echo "OUTPUT:$value"
}

# Get the current bit rate of the WIFI connected
get_bit_rate()
{
        value="$(nmcli device wifi list |grep $var2| awk '{ print $5 }')"
        echo "OUTPUT:$value"
}

# Get the current security mode of the WIFI connected
get_security_mode()
{
        value="$(nmcli device wifi list |grep $var2| awk '{ print $9 }')"
        echo "OUTPUT:$value"
}

# Refresh the wifi network of the WLAN client
refresh_wifi_network()
{
        wifi_off="$(nmcli radio wifi off > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        wifi_on="$(nmcli radio wifi on > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        if [ $wifi_off = "SUCCESS" ] && [ $wifi_on = "SUCCESS" ]; then
                echo "OUTPUT:SUCCESS"
        else
                echo "OUTPUT:FAILURE"
        fi
}

#Bring up interface
bringup_interface()
{
        up="$(ifconfig $var2 up > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        sleep 5
        if [ $up = "SUCCESS" ]; then
                echo "OUTPUT:SUCCESS"
        else
                echo "OUTPUT:FAILURE"
        fi

}
#Bring down interface
bringdown_interface()
{
        down="$(ifconfig $var2 down > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        sleep 5
        if [ $down = "SUCCESS" ]; then
                echo "OUTPUT:SUCCESS"
        else
                echo "OUTPUT:FAILURE"
        fi
}

#Verify ping to a network
ping_to_network()
{
        route_add_cmd="$(sudo ip route add $var3 via $var4 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
	sleep 10
        ping_cmd="$(ping -I $var2 -c 3 $var3 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        route_del_cmd="$(sudo ip route delete $var3 via $var4 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        if [ $route_add_cmd = "SUCCESS" ] && [ $ping_cmd = "SUCCESS" ]  && [ $route_del_cmd = "SUCCESS" ]; then
                echo "OUTPUT:SUCCESS"
        else
                echo "OUTPUT:FAILURE"
        fi
}

#Verify ping to a host url
ping_to_host()
{
        route_add_cmd="$(sudo route add -net $var2 netmask 255.255.255.255 gw $var3 dev $var4  > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        sleep 10
        ping_cmd="$(ping -I $var4 -c 3 $var2 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        route_del_cmd="$(sudo route del -net $var2 netmask 255.255.255.255 gw $var3 dev $var4  > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        if [ $route_add_cmd = "SUCCESS" ] && [ $ping_cmd = "SUCCESS" ]  && [ $route_del_cmd = "SUCCESS" ]; then
                echo "OUTPUT:SUCCESS"
        else
                echo "OUTPUT:FAILURE"
        fi
}

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

# To get the MAC address of the wlan client
get_wlan_mac()
{
        value="$(ifconfig $var2 | grep HWaddr | awk '{ print $5 }')"
        echo "OUTPUT:$value"
}

# To delete the saved wifi connection in the wlan client
delete_saved_wifi_connections()
{
        ls_2ghz="$(find /etc/NetworkManager/system-connections/ | grep $var2*)"
        ls_5ghz="$(find /etc/NetworkManager/system-connections/ | grep $var3*)"

        if  echo $ls_2ghz | grep -q $var2 ; then
                wifi_2ghz="$(rm /etc/NetworkManager/system-connections/$var2* && echo "SUCCESS" || echo "FAILURE")"
        else
                wifi_2ghz="SUCCESS"
        fi

        if echo $ls_5ghz | grep -q $var3; then
                wifi_5ghz="$(rm /etc/NetworkManager/system-connections/$var3* && echo "SUCCESS" || echo "FAILURE")"
        else
                wifi_5ghz="SUCCESS"
        fi

        if [ $wifi_2ghz = "SUCCESS" ] && [ $wifi_5ghz = "SUCCESS" ]; then
                echo "OUTPUT:SUCCESS"
        else
                echo "OUTPUT:FAILURE"
        fi
}

# Telnet to the client devices
telnetToClient()
{
         value="$({
sleep 2
echo $var3
sleep 2
echo $var4
sleep 1
echo exit
} | telnet $var2 | tr "\n" " ")"
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

# To get the Access point of the wlan client
get_wlan_accesspoint()
{
        value="$(iwconfig $var2 | grep "Access Point" | awk '{ print $6 }')"
        echo "OUTPUT:$value"
}

add_static_route()
{
        value="$(sudo route add -net $var2 netmask 255.255.255.255 gw $var3 dev $var4  > /dev/null && echo "SUCCESS" || echo "FAILURE")"

        echo "OUTPUT:$value"
}

del_static_route()
{
        value="$(sudo route del -net $var2 netmask 255.255.255.255 gw $var3 dev $var4  > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

nslookup_in_client()
{
        outStatus="$(nslookup $var2 $var3)"
        outStatus=$(printf "%s " $outStatus)
        site=$(echo $var2 | sed 's/^.\{4\}//g')
        case $outStatus in
            *"Non-authoritative answer: Name: $var2 Address:"*) value="SUCCESS";;
            *"Non-authoritative answer: $var2 canonical name = $site. Name: $site Address:"*) value="SUCCESS";;
            *)value="FAILURE"
        esac
        echo "OUTPUT:$value"
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

# To set the UDP server in listening mode
udp_init_server()
{
        iperf -s -B $var2 -u &
        value="$(ps aux | grep iperf | grep -v grep > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#To send UDP request from client to server
udp_request()
{
        iperf -c $var2 -B $var4 -u > $var3 2>&1
        bindStatus="$(cat $var3 | grep "bind failed:" && echo "FAILURE" || echo "SUCCESS")"
        if [ $bindStatus = "SUCCESS" ]; then
                echo "OUTPUT:SUCCESS"
        else
                echo "OUTPUT:"
        fi
}

#To validate the UDP output
validate_udp_output()
{
        bandwidth="$(cat $var2 | grep bits/sec | awk '{ print $7 }' | tail -1)"
        lossPercentage="$(cat $var2 | grep bits/sec | awk '{ print $13 }' | tail -1)"
        echo "OUTPUT:$bandwidth,$lossPercentage"
        deleteTmpFile="$(sudo rm $var2 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
}

#To kill iperf pid
kill_iperf()
{
        pkill iperf
        value="$(ps aux | grep iperf | grep -v "grep" > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#File transfer via FTP from Wlan to LAN using PUT command
ftpFromWlan()
{
FTP_FILE=$var5
touch $FTP_FILE
value="$(SERVER=$var2
USER=$var3
PASSW=$var4
ftp -v -n $SERVER <<END_OF_SESSION
user $USER $PASSW
put $FTP_FILE
END_OF_SESSION
rm -rf $FTP_FILE
)"
echo "OUTPUT:$value"

}

#transfer the test file from LAN to WLAN using GET command
ftpFromlan()
{
FTP_FILE=$var5
rm -rf $FTP_FILE
value="$(SERVER=$var2
USER=$var3
PASSW=$var4
ftp -v -n $SERVER <<END_OF_SESSION
user $USER $PASSW
get $FTP_FILE
END_OF_SESSION
)"
echo "OUTPUT:$value"
}

#Verify the FTP download
validate_FTP()
{
        FTP_FILE=$var2
        value="$(ls -lrt $FTP_FILE > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#To do ssh to client machines
ssh_to_client()
{
        value="$(sshpass -p$var2 ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeychecking=no $var3@$var4 ifconfig $var5 | grep "inet add" | cut -d ':' -f 2 | cut -d ' ' -f 1)"
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

#echo "\r\n";

# Invoke the function based on the argument passed
case $event in
   "wifi_ssid_connect")
        wifi_ssid_connect;;
   "wifi_ssid_connect_openSecurity")
        wifi_ssid_connect_openSecurity;;
   "wifi_ssid_disconnect")
        wifi_ssid_disconnect;;
   "get_wlan_ip_address")
        get_wlan_ip_address;;
   "get_wlan_subnet_mask")
        get_wlan_subnet_mask;;
   "get_connected_ssid_name")
        get_connected_ssid_name;;
   "is_ssid_available")
        is_ssid_available;;
   "get_channel_number")
        get_channel_number;;
   "get_bit_rate")
        get_bit_rate;;
   "get_security_mode")
        get_security_mode;;
   "refresh_wifi_network")
        refresh_wifi_network;;
   "bringdown_interface")
        bringdown_interface;;
   "bringup_interface")
        bringup_interface;;
   "ping_to_network")
        ping_to_network;;
   "ping_to_host")
        ping_to_host;;
   "wget_http_network")
        wget_http_network;;
   "wget_https_network")
        wget_https_network;;
   "get_wlan_mac")
        get_wlan_mac;; 
   "delete_saved_wifi_connections")
        delete_saved_wifi_connections;;
   "telnetToClient")
        telnetToClient;;
   "ftpToClient")
        ftpToClient;;
   "get_wlan_accesspoint")
        get_wlan_accesspoint;;
   "add_static_route")
        add_static_route;;
   "del_static_route")
        del_static_route;;
   "nslookup_in_client")
        nslookup_in_client;;
   "tcp_init_server_perf")
        tcp_init_server_perf;;
   "tcp_request_perf")
        tcp_request_perf;;
   "tcp_get_client_throughput")
        tcp_get_client_throughput;;
   "tcp_init_server")
        tcp_init_server;;
   "tcp_request")
        tcp_request;;
   "validate_tcp_server_output")
        validate_tcp_server_output;;
   "validate_tcp_server_output_throughput")
        validate_tcp_server_output_throughput;;
   "udp_init_server")
        udp_init_server;;
   "udp_request")
        udp_request;;
   "validate_udp_output")
        validate_udp_output;;
   "kill_iperf")
        kill_iperf;;
   "ftpFromWlan")
        ftpFromWlan;;
   "ftpFromlan")
        ftpFromlan;;
   "validate_FTP")
        validate_FTP;;
    "ssh_to_client")
        ssh_to_client;;
    "start_node")
        start_node;;
    "kill_selenium")
        kill_selenium;;
   *) echo "Invalid Argument passed";;
esac

