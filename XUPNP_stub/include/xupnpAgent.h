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

#ifndef __XUPNP_STUB_H__
#define __XUPNP_STUB_H__

#include <json/json.h>
#include "rdkteststubintf.h"
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>
#include "rdktestagentintf.h"

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

#define STR_LEN                128
#define LINE_LEN               1024
#define MAX_DATA_LEN           8192
#define XCALDEVICE             "xcal-device"
#define XDISCOVERY             "xdiscovery"
#define XDISC_LOG_FILE         "/opt/logs/xdiscovery.log"
#define XCALDEV_LOG_FILE       "/opt/logs/xdevice.log"
#define XDISCONFIG             "/etc/xupnp/xdiscovery.conf"
#define XDISCONFIG_EMULTR      "/etc/xdiscovery.conf"

using namespace std;

class RDKTestAgent;
class XUPNPAgent : public RDKTestStubInterface, public AbstractServer<XUPNPAgent>
{
public:
	XUPNPAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <XUPNPAgent>(ptrRpcServer)
	{
	   this->bindAndAddMethod(Procedure("TestMgr_XUPNP_GetUpnpResult", PARAMS_BY_NAME, JSON_STRING,"paramName",JSON_STRING,NULL), &XUPNPAgent::XUPNPAgent_GetUpnpResult);
	   this->bindAndAddMethod(Procedure("TestMgr_XUPNP_ReadXDiscOutputFile", PARAMS_BY_NAME, JSON_STRING,"paramName",JSON_STRING,NULL), &XUPNPAgent::XUPNPAgent_ReadXDiscOutputFile);
	   this->bindAndAddMethod(Procedure("TestMgr_XUPNP_CheckXDiscOutputFile", PARAMS_BY_NAME, JSON_STRING,NULL), &XUPNPAgent::XUPNPAgent_CheckXDiscOutputFile);
	   this->bindAndAddMethod(Procedure("TestMgr_XUPNP_BroadcastEvent", PARAMS_BY_NAME, JSON_STRING,"stateId",JSON_INTEGER,"eventLog",JSON_STRING,"state",JSON_INTEGER,"payload",JSON_STRING,"error", JSON_INTEGER,NULL), &XUPNPAgent::XUPNPAgent_BroadcastEvent);

	}

    //Inherited functions
    bool initialize(IN const char* szVersion);

    bool cleanup(const char* szVersion);
    std::string testmodulepre_requisites();
    bool testmodulepost_requisites();

    //XUPNPAgent Wrapper functions
    //Generic (common to Gateway + IPClient boxes)
    void XUPNPAgent_GetUpnpResult(IN const Json::Value& req, OUT Json::Value& response);
    void XUPNPAgent_ReadXDiscOutputFile(IN const Json::Value& req, OUT Json::Value& response);
    void XUPNPAgent_CheckXDiscOutputFile(IN const Json::Value& req, OUT Json::Value& response);
    //Only for Gateway boxes
    void XUPNPAgent_BroadcastEvent(IN const Json::Value& req, OUT Json::Value& response);
};

#endif //__XUPNP_STUB_H__
