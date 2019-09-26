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

#ifndef __SNMP_STUB_H__
#define __SNMP_STUB_H__

#include <json/json.h>
#include <stdlib.h>
#include <iostream>
#include <string.h>
#include <sys/sysinfo.h>
#include <sys/utsname.h>
#include <ifaddrs.h>
#include <arpa/inet.h>
#include <net/if.h>
#include <errno.h>
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

#include "rdkteststubintf.h"
#include "rdktestagentintf.h"

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false


using namespace std;

class RDKTestAgent;
class SNMPProtocolAgent : public RDKTestStubInterface , public AbstractServer<SNMPProtocolAgent>
{
        public:
		/*Constructor*/
		SNMPProtocolAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <SNMPProtocolAgent>(ptrRpcServer)
                {
                 this->bindAndAddMethod(Procedure("TestMgr_GetCommString", PARAMS_BY_NAME, JSON_STRING,NULL), &SNMPProtocolAgent::GetCommString);
		}

		/*Inherited functions*/
		bool initialize(IN const char* szVersion);
		bool cleanup(IN const char* szVersion);
		std::string testmodulepre_requisites();
		bool testmodulepost_requisites();

                /*Retreive community string*/
                void GetCommString(IN const Json::Value& req, OUT Json::Value& response);
};

#endif

