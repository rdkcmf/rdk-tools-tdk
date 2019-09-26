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

#ifndef __IARM_STUB_H__
#define __IARM_STUB_H__
#include <json/json.h>
#include <unistd.h>
#include <string.h>
#include <dlfcn.h>
#include <stdlib.h>
#include "rdkteststubintf.h"
#include "libIBus.h"
#include "rdktestagentintf.h"
#include "libIBusDaemon.h"
#include "libIARM.h"
#include "libIBus.h"
#include "irMgr.h"
#include "pwrMgr.h"
#include "sysMgr.h"
#include "mfrMgr.h"
#include "mfrTypes.h"
#include <sys/types.h>
#include <sys/wait.h>
#include "dummytestmgr.h"
#include "keyeventdata.h" /*Performance test include*/
#include <fstream>
#include <sstream>
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>
#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false
#define STR_LEN                128
#define LINE_LEN               1024
#define EVTDATA_MAX_SIZE 3
#define PRE_REQ_CHECK "pre_requisite_chk.txt"
#define DAEMON_EXE "IARMDaemonMain"
#define PWRMGR_EXE "pwrMgrMain"
#define IRMGR_EXE "irMgrMain"
#define MFRMGR_EXE "mfrMgrMain"
#define SYSMGR_EXE "sysMgrMain"

class RDKTestAgent;
class IARMBUSAgent : public RDKTestStubInterface, public AbstractServer<IARMBUSAgent>
{
	public:
	        IARMBUSAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <IARMBUSAgent>(ptrRpcServer)
	        {
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_Init", PARAMS_BY_NAME, JSON_STRING,"Process_name",JSON_STRING,NULL), &IARMBUSAgent::IARMBUSAgent_Init);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_Term", PARAMS_BY_NAME, JSON_STRING,NULL), &IARMBUSAgent::IARMBUSAgent_Term);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_Connect", PARAMS_BY_NAME, JSON_STRING,NULL), &IARMBUSAgent::IARMBUSAgent_BusConnect);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_Disconnect", PARAMS_BY_NAME, JSON_STRING,NULL), &IARMBUSAgent::IARMBUSAgent_BusDisconnect);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_IsConnected", PARAMS_BY_NAME, JSON_STRING,"member_name",JSON_STRING,NULL), &IARMBUSAgent::IARMBUSAgent_IsConnected);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_RequestResource", PARAMS_BY_NAME, JSON_STRING,"resource_type",JSON_INTEGER,NULL), &IARMBUSAgent::IARMBUSAgent_RequestResource);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_ReleaseResource", PARAMS_BY_NAME, JSON_STRING,"resource_type",JSON_INTEGER,NULL), &IARMBUSAgent::IARMBUSAgent_ReleaseResource);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_RegisterEventHandler", PARAMS_BY_NAME, JSON_STRING,"event_id",JSON_INTEGER,"owner_name",JSON_STRING,"evt_handler",JSON_STRING,NULL), &IARMBUSAgent::IARMBUSAgent_RegisterEventHandler);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_RemoveEventHandler", PARAMS_BY_NAME, JSON_STRING,"event_id",JSON_INTEGER,"owner_name",JSON_STRING,"evt_handler",JSON_STRING,NULL), &IARMBUSAgent::IARMBUSAgent_RemoveEventHandler);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_UnRegisterEventHandler", PARAMS_BY_NAME, JSON_STRING,"event_id",JSON_INTEGER,"owner_name",JSON_STRING,NULL), &IARMBUSAgent::IARMBUSAgent_UnRegisterEventHandler);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_RegisterEvent", PARAMS_BY_NAME, JSON_STRING,"max_event",JSON_INTEGER,NULL), &IARMBUSAgent::IARMBUSAgent_RegisterEvent);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_RegisterCall", PARAMS_BY_NAME, JSON_STRING,"owner_name",JSON_STRING,NULL), &IARMBUSAgent::IARMBUSAgent_RegisterCall);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_BroadcastEvent", PARAMS_BY_NAME, JSON_STRING,"event_id",JSON_INTEGER,"owner_name",JSON_STRING,"keyType",JSON_INTEGER,"keyCode",JSON_INTEGER,"newState",JSON_INTEGER,"resource_type",JSON_INTEGER,"state",JSON_INTEGER,"error",JSON_INTEGER,"payload",JSON_STRING,NULL), &IARMBUSAgent::IARMBUSAgent_BroadcastEvent);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_BusCall", PARAMS_BY_NAME, JSON_STRING,"method_name",JSON_STRING,"owner_name",JSON_STRING,"set_timeout",JSON_INTEGER,"newState",JSON_INTEGER,"resource_type",JSON_INTEGER,"mfr_param_type",JSON_INTEGER,"imagename",JSON_STRING,"imagepath",JSON_STRING,"testapp_API0_data",JSON_INTEGER,"testapp_API1_data",JSON_INTEGER,NULL), &IARMBUSAgent::IARMBUSAgent_BusCall);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_GetLastReceivedEventDetails", PARAMS_BY_NAME, JSON_STRING,NULL), &IARMBUSAgent::get_LastReceivedEventDetails);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_InvokeSecondApplication", PARAMS_BY_NAME, JSON_STRING,"appname",JSON_STRING,"argv1",JSON_STRING,"apptype",JSON_STRING,"iterationcount",JSON_INTEGER,NULL), &IARMBUSAgent::InvokeSecondApplication);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_SyncSecondApplication", PARAMS_BY_NAME, JSON_STRING,"lockenabled",JSON_STRING,NULL), &IARMBUSAgent::SyncSecondApplication);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_GetContext", PARAMS_BY_NAME, JSON_STRING,NULL), &IARMBUSAgent::IARMBUSAgent_GetContext);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_InvokeEventTransmitterApp", PARAMS_BY_NAME, JSON_STRING,"evttxappname",JSON_STRING,"event_id",JSON_INTEGER,"owner_name",JSON_STRING,"keyType",JSON_INTEGER,"keyCode",JSON_INTEGER,"newState",JSON_INTEGER,"resource_type",JSON_INTEGER,NULL), &IARMBUSAgent::InvokeEventTransmitterApp);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_GetLastReceivedEventPerformanceDetails", PARAMS_BY_NAME, JSON_STRING,NULL), &IARMBUSAgent::GetLastReceivedEventPerformanceDetails);
        	   this->bindAndAddMethod(Procedure("TestMgr_IARMBUS_RegisterMultipleEventHandlers", PARAMS_BY_NAME, JSON_STRING,"event_id",JSON_INTEGER,"owner_name",JSON_STRING,NULL), &IARMBUSAgent::RegisterMultipleEventHandlers);

        	}

		/*inherited functions*/
		bool initialize(IN const char* szVersion);

		bool cleanup(IN const char* szVersion);
		std::string testmodulepre_requisites();
                bool testmodulepost_requisites();
		/*IARM Wrapper functions*/
		void IARMBUSAgent_Init(IN const Json::Value& req, OUT Json::Value& response);
		void IARMBUSAgent_Term(IN const Json::Value& req, OUT Json::Value& response);
		void IARMBUSAgent_BusConnect(IN const Json::Value& req, OUT Json::Value& response);
		void IARMBUSAgent_BusDisconnect(IN const Json::Value& req, OUT Json::Value& response);
		void IARMBUSAgent_IsConnected(IN const Json::Value& req, OUT Json::Value& response);
		void IARMBUSAgent_RequestResource(IN const Json::Value& req, OUT Json::Value& response);
		void IARMBUSAgent_ReleaseResource(IN const Json::Value& req, OUT Json::Value& response);
		void IARMBUSAgent_RegisterEventHandler(IN const Json::Value& req, OUT Json::Value& response);
		void IARMBUSAgent_RemoveEventHandler(IN const Json::Value& req, OUT Json::Value& response);
		void IARMBUSAgent_UnRegisterEventHandler(IN const Json::Value& req, OUT Json::Value& response);
		void IARMBUSAgent_RegisterCall(IN const Json::Value& req, OUT Json::Value& response);
		void IARMBUSAgent_BusCall(IN const Json::Value& req, OUT Json::Value& response);
		void IARMBUSAgent_RegisterEvent(IN const Json::Value& req, OUT Json::Value& response);
		void IARMBUSAgent_GetContext(IN const Json::Value& req, OUT Json::Value& response);
		void IARMBUSAgent_BroadcastEvent(IN const Json::Value& req, OUT Json::Value& response);
		void get_LastReceivedEventDetails(IN const Json::Value& req, OUT Json::Value& response);
		void InvokeSecondApplication(IN const Json::Value& req, OUT Json::Value& response);
		void SyncSecondApplication(IN const Json::Value& req, OUT Json::Value& response);
		/*IARMBus Performance test Wrapper functions*/
                void RegisterMultipleEventHandlers (IN const Json::Value& req, OUT Json::Value& response);
                void GetLastReceivedEventPerformanceDetails(IN const Json::Value& req, OUT Json::Value& response);
                void InvokeEventTransmitterApp(IN const Json::Value& req, OUT Json::Value& response);
                std::string testenvPath;
                int keyCode, keyType;

};
#endif //__IARM_STUB_H__
