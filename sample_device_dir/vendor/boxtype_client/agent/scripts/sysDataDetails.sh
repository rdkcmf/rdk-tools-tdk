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

echo "Executing sysDetailsData.sh"
RESULT=`ps -eaf | grep -v grep | grep -i tr69hostif`

if [ "${RESULT:-null}" = null ]; then
    echo "tr69hostif not running"
    echo "Result: -1 Value: ${RESULT}"
else
    echo "tr69hostif is running"
    echo "Executing each parameter requests"
    echo "#Manufacturer START"
    curl -d '{"paramList" : [{"name" : "Device.DeviceInfo.Manufacturer"}]}' http://127.0.0.1:10999
    echo ""
    echo "#Manufacturer END"
    echo "#ModelName START"
    curl -d '{"paramList" : [{"name" : "Device.DeviceInfo.ModelName"}]}' http://127.0.0.1:10999
    echo ""
    echo "#ModelName END"
    echo "#SerialNumber START"
    curl -d '{"paramList" : [{"name" : "Device.DeviceInfo.SerialNumber"}]}' http://127.0.0.1:10999
    echo ""
    echo "#SerialNumber END"
    echo "#HardwareVersion START"
    curl -d '{"paramList" : [{"name" : "Device.DeviceInfo.HardwareVersion"}]}' http://127.0.0.1:10999
    echo ""
    echo "#HardwareVersion END"
    echo "#SoftwareVersion START"
    curl -d '{"paramList" : [{"name" : "Device.DeviceInfo.SoftwareVersion"}]}' http://127.0.0.1:10999
    echo ""
    echo "#SoftwareVersion END"
    echo "#kernelversion START"
    cat /proc/version 
    echo "#kernelversion END"
    echo "#NumberOfProcessor START"
    curl -d '{"paramList" : [{"name" : "Device.DeviceInfo.ProcessorNumberOfEntries"}]}' http://127.0.0.1:10999 
    echo ""
    echo "#NumberOfProcessor END"
    echo "#Architecture START"
    curl -d '{"paramList" : [{"name" : "Device.DeviceInfo.Processor.1.Architecture"}]}' http://127.0.0.1:10999 
    echo ""
    echo "#Architecture END"
    echo "#UpTime START"
    curl -d '{"paramList" : [{"name" : "Device.DeviceInfo.UpTime"}]}' http://127.0.0.1:10999 
    echo ""
    echo "#UpTime END"
    echo "#Bootagrs START"
    cat /proc/cmdline
    echo "#Bootagrs END"
    echo "#NumberOfProcessRunning START"
    curl -d '{"paramList" : [{"name" : "Device.DeviceInfo.ProcessStatus.ProcessNumberOfEntries"}]}' http://127.0.0.1:10999 
    echo ""
    echo "#NumberOfProcessRunning END"
    echo "#NumberOfInterface START"
    curl -d '{"paramList" : [{"name" : "Device.Ethernet.InterfaceNumberOfEntries"}]}' http://127.0.0.1:10999 
    echo ""
    echo "#NumberOfInterface END"
    echo "#MemoryTotal START"
    curl -d '{"paramList" : [{"name" : "Device.DeviceInfo.MemoryStatus.Total"}]}' http://127.0.0.1:10999 
    echo ""
    echo "#MemoryTotal END"
    echo "#MemoryFree START"
    curl -d '{"paramList" : [{"name" : "Device.DeviceInfo.MemoryStatus.Free"}]}' http://127.0.0.1:10999
    echo ""
    echo "#MemoryFree END"
    echo "#Driversloaded START"
    cat /proc/modules
    echo "#Driversloaded END"
    echo "#Partitions START"
    cat /proc/partitions
    echo "#Partitions END"
    echo "#mounts START"
    cat /proc/mounts
    echo "#mounts END"

fi
