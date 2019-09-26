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

#ifndef __TRM_STUB_H__
#define __TRM_STUB_H__

#include <json/json.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include <sstream>
#include "TRMAgentHelper.h"
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

#define TOTAL_DEVICE_NUMBER 10

using namespace std;

class RDKTestAgent;
class TRMAgent : public RDKTestStubInterface , public AbstractServer<TRMAgent>
{
public:

    TRMAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <TRMAgent>(ptrRpcServer)
    {
        this->bindAndAddMethod(Procedure("TestMgr_TRM_GetMaxTuners", PARAMS_BY_NAME, JSON_STRING,NULL), &TRMAgent::TRMAgent_GetMaxTuners);
        this->bindAndAddMethod(Procedure("TestMgr_TRM_GetAllTunerIds", PARAMS_BY_NAME, JSON_STRING,NULL), &TRMAgent::TRMAgent_GetAllTunerIds);
        this->bindAndAddMethod(Procedure("TestMgr_TRM_GetAllTunerStates", PARAMS_BY_NAME, JSON_STRING,NULL), &TRMAgent::TRMAgent_GetAllTunerStates);
        this->bindAndAddMethod(Procedure("TestMgr_TRM_GetAllReservations", PARAMS_BY_NAME, JSON_STRING,"deviceNo",JSON_INTEGER,NULL), &TRMAgent::TRMAgent_GetAllReservations);
        this->bindAndAddMethod(Procedure("TestMgr_TRM_GetVersion", PARAMS_BY_NAME, JSON_STRING,NULL), &TRMAgent::TRMAgent_GetVersion);
        this->bindAndAddMethod(Procedure("TestMgr_TRM_TunerReserveForRecord", PARAMS_BY_NAME,JSON_STRING,"deviceNo",JSON_INTEGER,"recordingId",JSON_STRING,"locator",JSON_STRING,"duration",JSON_INTEGER,"startTime",JSON_INTEGER,"hot",JSON_INTEGER,"selectOnConflict",JSON_INTEGER,"token",JSON_STRING,NULL), &TRMAgent::TRMAgent_TunerReserveForRecord);
        this->bindAndAddMethod(Procedure("TestMgr_TRM_TunerReserveForLive", PARAMS_BY_NAME, JSON_STRING,"deviceNo",JSON_INTEGER,"locator",JSON_STRING,"duration",JSON_INTEGER,"startTime",JSON_INTEGER,"selectOnConflict",JSON_INTEGER,"token",JSON_STRING,NULL), &TRMAgent::TRMAgent_TunerReserveForLive);
        this->bindAndAddMethod(Procedure("TestMgr_TRM_ReleaseTunerReservation", PARAMS_BY_NAME, JSON_STRING,"activity",JSON_INTEGER,"locator",JSON_STRING,"deviceNo",JSON_INTEGER,NULL), &TRMAgent::TRMAgent_ReleaseTunerReservation);
        this->bindAndAddMethod(Procedure("TestMgr_TRM_ValidateTunerReservation", PARAMS_BY_NAME, JSON_STRING,"activity",JSON_INTEGER,"locator",JSON_STRING,"deviceNo",JSON_INTEGER,NULL), &TRMAgent::TRMAgent_ValidateTunerReservation);
        this->bindAndAddMethod(Procedure("TestMgr_TRM_CancelRecording", PARAMS_BY_NAME, JSON_STRING,"locator",JSON_STRING,NULL), &TRMAgent::TRMAgent_CancelRecording);
    }
    //Inherited functions
    bool initialize(IN const char* szVersion);
    bool cleanup(IN const char* szVersion);
    string testmodulepre_requisites();
    bool testmodulepost_requisites();

    //TRMAgent Wrapper functions
    void TRMAgent_GetMaxTuners(IN const Json::Value& req, OUT Json::Value& response);
    void TRMAgent_GetAllTunerIds(IN const Json::Value& req, OUT Json::Value& response);
    void TRMAgent_GetAllTunerStates(IN const Json::Value& req, OUT Json::Value& response);
    void TRMAgent_GetAllReservations(IN const Json::Value& req, OUT Json::Value& response);
    void TRMAgent_GetVersion(IN const Json::Value& req, OUT Json::Value& response);
    void TRMAgent_TunerReserveForRecord(IN const Json::Value& req, OUT Json::Value& response);
    void TRMAgent_TunerReserveForLive(IN const Json::Value& req, OUT Json::Value& response);
    void TRMAgent_ReleaseTunerReservation(IN const Json::Value& req, OUT Json::Value& response);
    void TRMAgent_ValidateTunerReservation(IN const Json::Value& req, OUT Json::Value& response);
    void TRMAgent_CancelRecording(IN const Json::Value& req, OUT Json::Value& response);

};

#endif //__TRM_STUB_H__
