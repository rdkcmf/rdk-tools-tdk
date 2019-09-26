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
#
#Get the interface to connect to WAN. This is stored in the $INTERFACE variable in common.properties file
#source /sysint/conf/common.properties
source /etc/common.properties

#The below variables hold the port numbers used by the agent in the client.
CLIENT_AGENT_PORT=8087
CLIENT_STATUS_PORT=8088
CLIENT_TFTP_PORT=69
CLIENT_AGENT_MONITOR_PORT=8090

#This is the interface on gateway device corresponding to the MoCA network.
HOME_NETWORK_INTERFACE="<moca_network_interfae>" #Interface on gateway device corresponding to the MoCA network.

#Set the below variable to the interface that provides LAN connectivity
#GATEWAY_BOX_WAN_INTERFACE="lan0"
GATEWAY_BOX_WAN_INTERFACE=$(echo $INTERFACE | awk -F":" '{print $1}') 

echo "Configuring iptables... "
if [ $# -lt 5 ]; then
	echo "Error! Insufficient arguments. Format is $0 <client MAC address> <agent port> <status monitoring port> <tftp port> <agent monitoring port>"
	exit 1
fi

#The below variables represent the MAC and port details of the gateway box.
#These forwarding works as below:
#FWD_AGENT_PORT on gateway is forwarded to CLIENT_AGENT_PORT.
#FWD_STATUS_PORT on gateway is forwarded to CLIENT_STATUS_PORT.
#FWD_TFTP_PORT  on gateway is forwarded to CLIENT_TFTP_PORT.
#FWD_AGENT_MONITOR_PORT  on gateway is forwarded to CLIENT_AGENT_MONITOR_PORT.

CLIENT_MAC=$1
FWD_AGENT_PORT=$2
FWD_STATUS_PORT=$3
FWD_TFTP_PORT=$4
FWD_AGENT_MONITOR_PORT=$5

echo "Extracting the ip address of MAC $CLIENT_MAC"
CLIENT_IP=$(arp -i $HOME_NETWORK_INTERFACE -n | grep $CLIENT_MAC | cut -d'(' -f2 | cut -d')' -f1)
echo "Extracted IP is $CLIENT_IP"
if [ -z $CLIENT_IP ]; then
	echo "Error! No matching IP address found. Either the device is not on this network or its ARP cache is not up-to-date."
	exit 1
fi

echo "Enabling forwarding rules..."
PORTS="$CLIENT_AGENT_PORT $CLIENT_STATUS_PORT $CLIENT_TFTP_PORT $CLIENT_AGENT_MONITOR_PORT"
for PORT in $PORTS; do
	#iptables -C returns an error if no matching rule is found in the table. This is done
	#to avoid duplicate rules cluttering the table.
	iptables -C FORWARD -p tcp -d $CLIENT_IP --dport $PORT -j ACCEPT
	if [[ 0 != $? ]]; then
		echo "No matching rule exists. Creating new rule."
		set -e #abort script if this fails.
		iptables -I FORWARD -p tcp -d $CLIENT_IP --dport $PORT -j ACCEPT
		set +e #no longer abort (for trivial errors).
	fi;
done;
echo "Done."

echo "Check for existing NAT rules to the same target or from the same gateway port. They need to be removed."
#Check for rules operating on the same port on this device.
PORTS="$FWD_AGENT_PORT $FWD_STATUS_PORT $FWD_TFTP_PORT $FWD_AGENT_MONITOR_PORT"
for PORT in $PORTS; do
	RULE=$(iptables -t nat -n -L PREROUTING --line-numbers | grep "dpt:$PORT" | cut -d' ' -f1 | head -n 1)
	while [ ! -z "$RULE" ]; do
		echo "Deleting PREROUTING rule from gateway device port $PORT"
		set -e #abort on failure
		iptables -t nat -D PREROUTING $RULE
		set +e #no longer abort (for trivial errors)
		RULE=$(iptables -t nat -n -L PREROUTING --line-numbers | grep "dpt:$PORT" | cut -d' ' -f1 | head -n 1)
	done;
done;

	

#Check for rules operating on the same target-device:port. 
PORTS="$CLIENT_AGENT_PORT $CLIENT_STATUS_PORT $CLIENT_TFTP_PORT $CLIENT_AGENT_MONITOR_PORT"
for PORT in $PORTS; do
	RULE=$(iptables -t nat -n -L PREROUTING --line-numbers | grep "to:$CLIENT_IP:$PORT" | cut -d' ' -f1 | head -n 1)
	while [ ! -z "$RULE" ]; do
		echo "Deleting PREROUTING rule to client device target $CLIENT_IP:$PORT"
		set -e
	        iptables -t nat -D PREROUTING $RULE
	        set +e
        	RULE=$(iptables -t nat -n -L PREROUTING --line-numbers | grep "to:$CLIENT_IP:$PORT" | cut -d' ' -f1 | head -n 1)
        done;
done;

echo "Enabling NAT rules..."
set -e
iptables -t nat -A PREROUTING -i $GATEWAY_BOX_WAN_INTERFACE -p tcp --dport $FWD_AGENT_PORT -j DNAT --to-destination $CLIENT_IP:$CLIENT_AGENT_PORT
iptables -t nat -A PREROUTING -i $GATEWAY_BOX_WAN_INTERFACE -p tcp --dport $FWD_STATUS_PORT -j DNAT --to-destination $CLIENT_IP:$CLIENT_STATUS_PORT
iptables -t nat -A PREROUTING -i $GATEWAY_BOX_WAN_INTERFACE -p udp --dport $FWD_TFTP_PORT -j DNAT --to-destination $CLIENT_IP:$CLIENT_TFTP_PORT
iptables -t nat -A PREROUTING -i $GATEWAY_BOX_WAN_INTERFACE -p tcp --dport $FWD_AGENT_MONITOR_PORT -j DNAT --to-destination $CLIENT_IP:$CLIENT_AGENT_MONITOR_PORT
iptables -t nat -A POSTROUTING -j MASQUERADE -o $GATEWAY_BOX_WAN_INTERFACE 
echo "Done."
