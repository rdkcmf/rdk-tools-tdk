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

#ifndef __NETSRVMGR_STUB_H__
#define __NETSRVMGR_STUB_H__

#include <json/json.h>
#include <fstream>
#include <unistd.h>
#include <sstream>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"

#include "wifiSrvMgrIarmIf.h"
#include "libIBus.h"
#include "irMgr.h"
#include "libIBusDaemon.h"
//#include "authserviceIARM.h"
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

/*
 *Maximum value for Wifi Manager 
 *Parameter and Parameter List
 */
#define WIFI_MGR_PARAM_LIST_BUFFER_SIZE  10000
#define WIFI_MGR_PARAM_BUFFER_SIZE 100
#define WIFI_MAX_DATA_LEN           8192
#define WIFI_MAX_STATUS_CODE     7
#define WIFI_MAX_LNF_STATUS_CODE 7
#define WIFI_SSID_SIZE		33

/*
 *Macros for Wifi Mgr EventHandling
 */
#define PRE_REQUISITE_LOG_PATH "logs/netsrvmgr_testmodule_prereq_details.log"
#define PRE_REQUISITE_FILE "scripts/netsrvmgr_test_module_pre-script.sh"
#define NM_LOG_FILE 	 "/opt/logs/netsrvmgr.log"


using namespace std;

class RDKTestAgent;
class NetSrvMgrAgent : public RDKTestStubInterface , public AbstractServer<NetSrvMgrAgent>
{
public:
    NetSrvMgrAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <NetSrvMgrAgent>(ptrRpcServer)
    {
        this->bindAndAddMethod(Procedure("TestMgr_NetSrvMgr_WifiMgrGetAvailableSSIDs", PARAMS_BY_NAME, JSON_STRING,NULL), &NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_GetAvailableSSIDs);
        this->bindAndAddMethod(Procedure("TestMgr_NetSrvMgr_WifiMgrGetCurrentState", PARAMS_BY_NAME, JSON_STRING,NULL), &NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_GetCurrentState);
        this->bindAndAddMethod(Procedure("TestMgr_NetSrvMgr_WifiMgrGetLAFState", PARAMS_BY_NAME, JSON_STRING,NULL), &NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_GetLAFState);
        this->bindAndAddMethod(Procedure("TestMgr_NetSrvMgr_WifiMgrGetPairedSSID", PARAMS_BY_NAME, JSON_STRING,NULL), &NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_GetPairedSSID);
        this->bindAndAddMethod(Procedure("TestMgr_NetSrvMgr_WifiMgrSetEnabled", PARAMS_BY_NAME, JSON_STRING,"enable",JSON_BOOLEAN,NULL), &NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_SetEnabled);
        this->bindAndAddMethod(Procedure("TestMgr_NetSrvMgr_WifiMgrSetGetParameters", PARAMS_BY_NAME,JSON_STRING,"method_name",JSON_STRING,"new_mode",JSON_INTEGER,"enable",JSON_INTEGER,"ssid",JSON_STRING,"passphrase",JSON_STRING,"security_mode",JSON_INTEGER,NULL), &NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_SetGetParameters);
        this->bindAndAddMethod(Procedure("TestMgr_NetSrvMgrAgent_WifiMgr_BroadcastEvent", PARAMS_BY_NAME, JSON_STRING,"owner",JSON_STRING,"event_id",JSON_INTEGER,"event_log",JSON_STRING,"key_code",JSON_INTEGER,"key_type",JSON_INTEGER,"isFP",JSON_INTEGER,"value",JSON_INTEGER, NULL), &NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_BroadcastEvent);
    }

private:
    string aWifiStatus[WIFI_MAX_STATUS_CODE] = {"Wifi Uninstalled",
			   "Wifi disabled",
			   "Wifi disconnected",
			   "Wifi pairing",
			   "Wifi connecting",
			   "Wifi connected",
			   "Wifi failed"};
    string aWifiLAFStatus[WIFI_MAX_LNF_STATUS_CODE] = {"LNF Uninitialised",
			    "LNF in progress",
			    "LNF connected",
			    "LNF connected to private network",
			    "Disconnected no LNF gateway detected",
			    "Disconnected get LFAT failed",
			    "Disconnected cant connect to private network"};
    		
public:
    /*
     *Constructor
     */
//    NetSrvMgrAgent ();

    /*
     *Inherited functions
     */
    bool initialize (IN const char* szVersion);
    bool cleanup(IN const char* szVersion);
    std::string testmodulepre_requisites ();
    bool testmodulepost_requisites ();

    /*
     *NetSrvMgrAgent Wrapper functions
     */
    void NetSrvMgrAgent_WifiMgr_GetAvailableSSIDs (IN const Json::Value& req, OUT Json::Value& response);
    void NetSrvMgrAgent_WifiMgr_GetCurrentState (IN const Json::Value& req, OUT Json::Value& response);
    void NetSrvMgrAgent_WifiMgr_GetLAFState (IN const Json::Value& req, OUT Json::Value& response);
    void NetSrvMgrAgent_WifiMgr_GetPairedSSID (IN const Json::Value& req, OUT Json::Value& response);
    void NetSrvMgrAgent_WifiMgr_SetEnabled (IN const Json::Value& req, OUT Json::Value& response);
    void NetSrvMgrAgent_WifiMgr_SetGetParameters (IN const Json::Value& req, OUT Json::Value& response);
    void NetSrvMgrAgent_WifiMgr_BroadcastEvent (IN const Json::Value& req, OUT Json::Value& response);
};

//extern "C" NetSrvMgrAgent* CreateObject();

#endif //__NETSRVMGR_STUB_H__
