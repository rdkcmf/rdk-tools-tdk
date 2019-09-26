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

#ifndef __DTCP_STUB_H__
#define __DTCP_STUB_H__

#include <json/json.h>
#include <string.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include "dtcpmgr.h"
#include <fstream>
#include <cstdlib>
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>
#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false
#define IPADDR_LEN 15


using namespace std;

class RDKTestAgent;
class DTCPAgent : public RDKTestStubInterface , public AbstractServer <DTCPAgent>
{
        public:
	        DTCPAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <DTCPAgent>(ptrRpcServer)
        	{
			this->bindAndAddMethod(Procedure("TestMgr_DTCP_Test_Execute", PARAMS_BY_NAME, JSON_STRING,"funcName",JSON_STRING,"strParam1",JSON_STRING,"intParam2",JSON_INTEGER,"intParam3",JSON_INTEGER,"intParam4",JSON_INTEGER,NULL), &DTCPAgent::DTCPAgent_Test_Execute);

		}

                //Inherited functions
                bool initialize(IN const char* szVersion);

                bool cleanup(const char* szVersion);
		std::string testmodulepre_requisites();
                bool testmodulepost_requisites();

                //DTCPAgent Wrapper functions
		void DTCPAgent_Test_Execute(IN const Json::Value& req, OUT Json::Value& response);
};
        extern "C" DTCPAgent* CreateObject(TcpSocketServer &ptrtcpServer);

#endif //__DTCP_STUB_H__

