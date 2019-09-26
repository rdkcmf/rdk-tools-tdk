/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2016 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/


#ifndef __SysUtil_STUB_H__
#define __SysUtil_STUB_H__

#include <json/json.h>
#include <stdlib.h>
#include <iostream>
#include <string.h>
#include <algorithm>
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>

#include "rdkteststubintf.h"
#include "rdktestagentintf.h"

#define IN
#define OUT

#define BUFF_LENGTH 512
#define IFCONFIG ("ifconfig ")
#define TOUCH ("touch ")
#define PING ("ping -c 2")
#define PING6 ("ping6 -c 2")
#define CMTS ("-I pci0 xre.ccp.xcal.tv ")
#define IPCMD ("ip ")
#define IP6CMD ("ip -6 ")
#define ROUTE (" route show")

#define TEST_SUCCESS true
#define TEST_FAILURE false

using namespace std;

class RDKTestAgent;
class SystemUtilAgent : public RDKTestStubInterface, public AbstractServer<SystemUtilAgent>
{
        public:
               SystemUtilAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <SystemUtilAgent>(ptrRpcServer)
               {
                  this->bindAndAddMethod(Procedure("TestMgr_GetifconfigValue", PARAMS_BY_NAME, JSON_STRING,"interface",JSON_STRING,NULL), &SystemUtilAgent::SystemUtilAgent_GetifconfigValue);                
                   this->bindAndAddMethod(Procedure("TestMgr_TouchFile", PARAMS_BY_NAME, JSON_STRING,"fileinfo",JSON_STRING,NULL), &SystemUtilAgent::SystemUtilAgent_TouchFile);
                   this->bindAndAddMethod(Procedure("TestMgr_GetpingValue", PARAMS_BY_NAME, JSON_STRING,"address",JSON_STRING,"ping6enable",JSON_INTEGER,NULL), &SystemUtilAgent::SystemUtilAgent_GetpingValue);
                   this->bindAndAddMethod(Procedure("TestMgr_GetrouteInfo", PARAMS_BY_NAME, JSON_STRING,"ip6enable",JSON_INTEGER,NULL), &SystemUtilAgent::SystemUtilAgent_GetrouteInfo);
                   this->bindAndAddMethod(Procedure("TestMgr_ExecuteCmd", PARAMS_BY_NAME, JSON_STRING,"command",JSON_STRING,NULL), &SystemUtilAgent::SystemUtilAgent_ExecuteCmd);
                   this->bindAndAddMethod(Procedure("TestMgr_Getoutput_json_file", PARAMS_BY_NAME, JSON_STRING,NULL), &SystemUtilAgent::SystemUtilAgent_Getoutput_json_file);
                   this->bindAndAddMethod(Procedure("TestMgr_ExecuteBinary", PARAMS_BY_NAME, JSON_STRING,"shell_script",JSON_STRING,"log_file",JSON_STRING,NULL), &SystemUtilAgent::SystemUtilAgent_ExecuteBinary);
               }

                /*Inherited functions*/
                bool initialize(IN const char* szVersion);
                bool cleanup(const char*);
		std::string testmodulepre_requisites();
		bool testmodulepost_requisites();
		void SystemUtilAgent_GetifconfigValue(IN const Json::Value& req, OUT Json::Value& response);
		void SystemUtilAgent_GetpingValue(IN const Json::Value& req, OUT Json::Value& response);
		void SystemUtilAgent_GetrouteInfo(IN const Json::Value& req, OUT Json::Value& response);
		void SystemUtilAgent_TouchFile(IN const Json::Value& req, OUT Json::Value& response);
		void SystemUtilAgent_ExecuteCmd(IN const Json::Value& req, OUT Json::Value& response);
		void SystemUtilAgent_Getoutput_json_file(IN const Json::Value& req, OUT Json::Value& response);
                void SystemUtilAgent_ExecuteBinary(IN const Json::Value& req, OUT Json::Value& response);
	

};

#endif 
