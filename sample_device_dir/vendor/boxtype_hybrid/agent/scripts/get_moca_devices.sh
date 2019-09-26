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
HOME_NETWORK_INTERFACE=<moca_network_interface> #interface on gateway device corresponding to the MoCA network.
#echo "Generating list of MoCA device MACs..."
if [ $# -lt 1 ]; then
	echo "Error! Insufficient arguments. Format is $0 <output file path>"
	exit 1
fi
arp -n -i $HOME_NETWORK_INTERFACE | grep "?" | awk '{print $4}' > $TDK_PATH/$1
#echo "Done"
