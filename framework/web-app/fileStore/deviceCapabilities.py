##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
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
#########################################################################
import os
import shutil
from ConfigParser import SafeConfigParser
#####################################################################################################################################
#
# To fetch the stream details from configuration file
#
# Syntax       : getconfig(obj,capability,key)
#
# Parameters   : obj, key , value(where key specifies the field and value specifies the device capability in the corresponding field)
#
# Return Value : True/False(Based on device capability)
#
#####################################################################################################################################
def getconfig(obj,capability,key = ""):
    deviceDetails = obj.getDeviceDetails()
    deviceName = deviceDetails["devicename"]
    deviceConfig = deviceName + "_deviceCapability.ini"
    parser = SafeConfigParser()

    # Check if device configuration file exists , else create dummy config file for the DUT.
    configFile = os.path.dirname(os.path.abspath(__file__))+"/tdkvDeviceCapabilities/"+ deviceConfig;
    sampleFile = os.path.dirname(os.path.abspath(__file__))+"/tdkvDeviceCapabilities/"+ "sample_deviceCapability.ini";
    if not os.path.exists(configFile):
        print "\n\nConfiguration file not present under tdkvDeviceCapabilities \nCreated %s"%deviceConfig;
        shutil.copyfile(sampleFile,configFile)
        print "Please populate the deviceCapabilites in %s in order to proceed with the execution\n\n"%deviceConfig;
        return False;

    # Fetching the config details from configuration file
    parser.read( os.path.dirname(os.path.abspath(__file__))+"/tdkvDeviceCapabilities/"+ deviceConfig)
    print "Parsing Device Capabilities ..."
    ConfigValue = parser.get('deviceCapabilities',capability);
    # If getValue is passed , acquire the corresponding config and return the ConfigValue.
    if key == "getValue" and capability:
        print "Get %s from config file"%(capability);
        if ConfigValue:
            print "Obtained %s for %s from config File"%(ConfigValue,capability);
            return ConfigValue;
        else:
            print "%s not configured in Config File\n Not Proceeding with the execution"%(capability);
            exit();
    # If key is passed, check whether the key is supported by the device, if not setResult as Not Applicable.
    elif key and capability:
        if(key not in ConfigValue):
            print "%s %s is not supported by the device\n"%(key,capability);
            obj.setAsNotApplicable();
            return False
        else:
            return True
    # If key is not passed , check whether the capability is set as true/false, if false, setResult as Not Applicable.
    elif not key and capability:
        if "true" in ConfigValue:
            return True
        elif "false" in ConfigValue:
            print "%s is not supported in the device\n"%capability;
            obj.setAsNotApplicable();
            return False
        else:
            print "%s capability is not configured , not proceeding with the execution"%capability;
            exit()

    else:
        print "Capability not configured in config file,not proceeding with the testcase"
        exit()

########## End of Function ##########
