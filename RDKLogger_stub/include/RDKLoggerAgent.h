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

#ifndef __RDKLOGGER_STUB_H__
#define __RDKLOGGER_STUB_H__

#include <json/json.h>
#include <string.h>
#include <stdlib.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include "rdk_debug.h"
#include "rdk_utils.h"
#include <fstream>
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

#define TDKAGENT_LOG		"AgentConsole.log"
#define DEBUG_CONF		"debug.ini"
#define SIZE    		256

using namespace std;

class RDKTestAgent;
class RDKLoggerAgent : public RDKTestStubInterface , public AbstractServer<RDKLoggerAgent>
{
        public:
                //Constructor
                RDKLoggerAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <RDKLoggerAgent>(ptrRpcServer)
                {
                    this->bindAndAddMethod(Procedure("TestMgr_RDKLogger_Init", PARAMS_BY_NAME, JSON_STRING,NULL), &RDKLoggerAgent::RDKLoggerAgent_Init);
                    this->bindAndAddMethod(Procedure("TestMgr_RDKLogger_Log", PARAMS_BY_NAME, JSON_STRING,"module",JSON_STRING,"level",JSON_STRING,NULL), &RDKLoggerAgent::RDKLoggerAgent_Log);
                    this->bindAndAddMethod(Procedure("TestMgr_RDKLogger_Dbg_Enabled_Status", PARAMS_BY_NAME, JSON_STRING,"module",JSON_STRING,"level",JSON_STRING,NULL), &RDKLoggerAgent::RDKLoggerAgent_Dbg_Enabled_Status);
                    this->bindAndAddMethod(Procedure("TestMgr_RDKLogger_EnvGet", PARAMS_BY_NAME, JSON_STRING,"module",JSON_STRING,NULL), &RDKLoggerAgent::RDKLoggerAgent_EnvGet);
                    this->bindAndAddMethod(Procedure("TestMgr_RDKLogger_EnvGetNum", PARAMS_BY_NAME, JSON_STRING,"module",JSON_STRING,NULL), &RDKLoggerAgent::RDKLoggerAgent_EnvGetNum);
                    this->bindAndAddMethod(Procedure("TestMgr_RDKLogger_EnvGetValueFromNum", PARAMS_BY_NAME, JSON_STRING,"number",JSON_INTEGER,NULL), &RDKLoggerAgent::RDKLoggerAgent_EnvGetValueFromNum);
                    this->bindAndAddMethod(Procedure("TestMgr_RDKLogger_EnvGetModFromNum", PARAMS_BY_NAME, JSON_STRING,"number",JSON_INTEGER,NULL), &RDKLoggerAgent::RDKLoggerAgent_EnvGetModFromNum);
                    this->bindAndAddMethod(Procedure("TestMgr_RDKLogger_CheckMPELogEnabled", PARAMS_BY_NAME, JSON_STRING,NULL), &RDKLoggerAgent::RDKLoggerAgent_CheckMPELogEnabled);
                    this->bindAndAddMethod(Procedure("TestMgr_RDKLogger_Log_All", PARAMS_BY_NAME, JSON_STRING,"module",JSON_STRING,NULL), &RDKLoggerAgent::RDKLoggerAgent_Log_All);
                    this->bindAndAddMethod(Procedure("TestMgr_RDKLogger_Log_None", PARAMS_BY_NAME, JSON_STRING,"module",JSON_STRING,NULL), &RDKLoggerAgent::RDKLoggerAgent_Log_None);
                    this->bindAndAddMethod(Procedure("TestMgr_RDKLogger_Log_Trace", PARAMS_BY_NAME, JSON_STRING,"module",JSON_STRING,NULL), &RDKLoggerAgent::RDKLoggerAgent_Log_Trace);
                    this->bindAndAddMethod(Procedure("TestMgr_RDKLogger_Log_InverseTrace", PARAMS_BY_NAME, JSON_STRING,"module",JSON_STRING,NULL), &RDKLoggerAgent::RDKLoggerAgent_Log_InverseTrace);
                    this->bindAndAddMethod(Procedure("TestMgr_RDKLogger_Log_Msg", PARAMS_BY_NAME, JSON_STRING,"module",JSON_STRING,"level",JSON_STRING,"msg",JSON_STRING,NULL), &RDKLoggerAgent::RDKLoggerAgent_Log_Msg);
                    this->bindAndAddMethod(Procedure("TestMgr_RDKLogger_SetLogLevel", PARAMS_BY_NAME, JSON_STRING,NULL), &RDKLoggerAgent::RDKLoggerAgent_SetLogLevel);
                    this->bindAndAddMethod(Procedure("TestMgr_RDKLogger_GetLogLevel", PARAMS_BY_NAME, JSON_STRING,NULL), &RDKLoggerAgent::RDKLoggerAgent_GetLogLevel);
                }

                //Inherited functions
                bool initialize(IN const char* szVersion);

                bool cleanup(const char*);
		std::string testmodulepre_requisites();
                bool testmodulepost_requisites();

                //RDKLoggerAgent Wrapper functions
		void RDKLoggerAgent_Init(IN const Json::Value& req, OUT Json::Value& response);
		void RDKLoggerAgent_Log(IN const Json::Value& req, OUT Json::Value& response);
		void RDKLoggerAgent_Dbg_Enabled_Status(IN const Json::Value& req, OUT Json::Value& response);
		void RDKLoggerAgent_EnvGet(IN const Json::Value& req, OUT Json::Value& response);
		void RDKLoggerAgent_EnvGetNum(IN const Json::Value& req, OUT Json::Value& response);
		void RDKLoggerAgent_EnvGetValueFromNum(IN const Json::Value& req, OUT Json::Value& response);
		void RDKLoggerAgent_EnvGetModFromNum(IN const Json::Value& req, OUT Json::Value& response);
		void RDKLoggerAgent_CheckMPELogEnabled(IN const Json::Value& req, OUT Json::Value& response);
		void RDKLoggerAgent_Log_All(IN const Json::Value& req, OUT Json::Value& response);
		void RDKLoggerAgent_Log_None(IN const Json::Value& req, OUT Json::Value& response);
		void RDKLoggerAgent_Log_Trace(IN const Json::Value& req, OUT Json::Value& response);
		void RDKLoggerAgent_Log_InverseTrace(IN const Json::Value& req, OUT Json::Value& response);
		void RDKLoggerAgent_Log_Msg(IN const Json::Value& req, OUT Json::Value& response);
		void RDKLoggerAgent_SetLogLevel(IN const Json::Value& req, OUT Json::Value& response);
		void RDKLoggerAgent_GetLogLevel(IN const Json::Value& req, OUT Json::Value& response);
};

#endif //__RDKLOGGER_STUB_H__

