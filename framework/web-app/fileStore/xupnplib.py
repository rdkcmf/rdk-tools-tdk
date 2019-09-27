##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2019 RDK Management
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

#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import os
import json
import re
import ConfigParser

# LogParser

# Syntax      : LogParser(message,parameter)
# Description : Function to parse output.json file
# Parameters  : message - the data retrieved from output.json file
#             : parameter  - the parameter to be searched in output.json file
# Return Value: dictionary - returns a dictionary with key(parameter):value(corresponding value) pairs

def LogParser(message,parameter) :
    output = json.loads(message);
    values = output.values()[0];
    dictionary = {};
    for (index,value) in enumerate(values):
        key = value.get("bcastMacAddress");
        value = value.get(parameter);
        dictionary[key] = value;
    print "\n\n\n**************XUPNP bcastMacAddress:%s MAPPING - BEGIN*************\n\n"%parameter
    print "bcastMacAddress:%s parameters mapping retrieved after parsing: %s"%(parameter,dictionary);
    print "\n\n\n**************XUPNP bcastMacAddress:%s MAPPING - END*************\n\n"%parameter
    return dictionary;

########## End of Function ##########

# GetParsedParamsList

# Syntax      : GetParsedParamsList(data,param,flag)
# Description : Function to parse and remove extra characters from details retrieved from stub function
# Parameters  : data - parsed details retrieved from stub function
#             : param - parameter to be validated from output.json
#               flag - to differentiate if the parameter to be queried comes as part of another paramter
#               (Eg : If the parameter to be queried is "DevType" the we get "Devtype" and "recvDevType",then flag=1 for "DevType" and 0 for"recvDevType"
# Return Value: params_list - List of Parsed parameters

def GetParsedParamsList(data,param,flag) :
    punctuation = [":",".","-"];
    if flag == 1 :
        getVals = list([val for val in data if val.isalpha() or val.isdigit()])
        res = "".join(getVals).replace(param,"");
        res = " ".join(re.split("[^A-Z0-9]*",res)).split(" ");
        params_list = list(filter(None, res));
    else :
        getVals = list([val for val in data if val.isalpha() or val.isdigit() or val in punctuation]);
        params_list = "".join(getVals).split(param);
        params_list = [i for i in params_list if i];
        params_list = [e[1:] for e in params_list];
    return params_list;

########## End of Function ##########

# TransferLogsParser

# Syntax      : TransferLogsParser(obj)
# Description : Function to read the logfile path and client ip from xupnp.config file
# Parameters  : obj - object to get the realpath
# Return Value: dictionary - returns a dictionary wit key(client ip):value(logfile path) pairs

def TransferLogsParser(obj) :
    #Get the device name configured in test manager
    deviceDetails = obj.getDeviceDetails()
    deviceName = deviceDetails["devicename"]

    #Get the device configuration file name
    deviceConfig = deviceName + ".config"

    #Get the current directory path
    configFilePath = os.path.dirname(os.path.realpath(__file__))
    configFilePath = configFilePath + "/xupnpDeviceConfig"
    xupnpConfigFile = configFilePath+'/'+deviceConfig

    print "Device config file:", xupnpConfigFile

    configParser = ConfigParser.ConfigParser()
    configParser.read(r'%s' % xupnpConfigFile)

    NO_OF_CLIENTS = configParser.get('xupnp-config', 'NO_OF_CLIENTS')
    NO_OF_CLIENTS = int(NO_OF_CLIENTS)
    count = 1;
    xupnp_log_list = []
    clients_ip_list = []
    while (count <= NO_OF_CLIENTS) :
        #Testrunner output log file
        LOG_FILE_CLIENT = "LOG_FILE_CLIENT_" + str(count);
        xupnp_log = configParser.get('xupnp-config', LOG_FILE_CLIENT)
        xupnp_log_list.append(xupnp_log)

        #Retrieve Client Ips
        IP_CLIENT = "IP_CLIENT_"+ str(count);
        clients_ip = configParser.get('xupnp-config', IP_CLIENT);
        clients_ip_list.append(clients_ip)
        count +=1;
    clientip_logfile_dic = dict(zip(clients_ip_list,xupnp_log_list));
    return clientip_logfile_dic,NO_OF_CLIENTS;

########## End of Function ##########
