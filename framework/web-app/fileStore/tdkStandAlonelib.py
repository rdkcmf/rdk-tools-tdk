##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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

import tdkvRDKServicesTestlib
import json
import importlib
import urllib
import sys

# Description : Get the details of the device configured in test manager
# Parameters  : None
# Return Value: Return the device details like IP,Name,MAC,BoxType etc

def getDeviceDetails(self):
    url = self.url + '/deviceGroup/getDeviceDetails?deviceIp='+self.ip
    try:
        response = urllib.urlopen(url).read()
        deviceDetails = json.loads(response)
    except:
        print "Unable to get Device Details from REST !!!"
        exit()

    sys.stdout.flush()
    return deviceDetails

# Description : Get the thunder port details
# Parameters  : None
# Return Value: Return the thunder port

def getThunderPortDetails(self):
    url = self.url + '/deviceGroup/getThunderDevicePorts?stbIp='+self.ip
    try:
        data = urllib.urlopen(url).read()
        thunderPortDetails = json.loads(data)
    except:
        print "Unable to get Thunder Port from REST !!!"
        exit()

    sys.stdout.flush()
    return thunderPortDetails

# Description : To execute the stand alone tests
# Parameters  : None
# Return Value: Return the test status and details

def executeTest (self) :
    executeJson = json.loads(self.jsonMsgValue)
    params = executeJson["params"]
    method = params["method"] 
    thunderPortDetails = getThunderPortDetails(self)
    thunderPort = thunderPortDetails["thunderPort"]

    if method == "TestMgr_RdkService_Test" :
        deviceInfo = getDeviceDetails(self);
        deviceName = deviceInfo["devicename"]
        deviceType = deviceInfo["boxtype"]
        testXMLName = params["params"]["xml_name"]
        details = "SUCCESS"
        result =  tdkvRDKServicesTestlib.executePluginTests(self.ip, thunderPort, deviceName, deviceType, self.realpath, testXMLName) 
    else:
        #This variable is hardcoded for now. This will be replaced by componentName in future.
        performancecomponent="performance"
        #The library name will be componentName+lib. eg:rdkserviceslib
        module=performancecomponent+"lib";
        """
        This is to import the module which is stored in a variable.
        Now "lib" contains all the function definitions in the imported module.
        """
        lib = importlib.import_module(module)
        """
        The function 'init_method' helps to initialise the module with ip and port. User can use this function
        if they want ip/port in library.
        """
        if "init_module" in dir(lib):
            init_module_method = getattr(lib,"init_module")
            init_module_method(self,thunderPort,getDeviceDetails(self))
        """
        The variable "method" contains the name of the function we need to invoke from "lib".
        getattr is used to fetch the given method name from lib.
        This is because the method name is stored as a string in the variable.
        """
        method_to_call = getattr(lib, method)
        """
        The variable "args" contains all the arguments we need to pass to the method.
        This will be in the form of a dictionary(key:value pair). 
        Keys are the argument name, values are the argument value.
        """
        args = {}
        if "params" in params:
            args = params["params"]
        details = method_to_call(**args)
        if details or details == None:
            result = "SUCCESS"
    return result,details; 
     
