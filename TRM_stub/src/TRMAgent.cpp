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

#include "TRMAgent.h"

static TRMClient *pTrmClient = NULL;

const char *deviceNames[TOTAL_DEVICE_NUMBER+1] = {
    "XiRoom1",
    "XiRoom2",
    "XiRoom3",
    "XiRoom4",
    "XiRoom5",
    "XiRoom6",
    "XiRoom7",
    "XiRoom8",
    "XiRoom9",
    "XiRoom10",
    "XiRoom11"
};

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "TRMAgent".
**************************************************************************/

extern "C" TRMAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
    return new TRMAgent(ptrtcpServer);
}

/**************************************************************************
Function name : TRMAgent::initialize

Arguments     : Input arguments are Version string and TRMAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
***************************************************************************/

bool TRMAgent::initialize(IN const char* szVersion)
{
    DEBUG_PRINT(DEBUG_ERROR, "TRMAgent Initialization\n");
    return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/

string TRMAgent::testmodulepre_requisites()
{
    DEBUG_PRINT(DEBUG_TRACE, "TRM testmodule pre_requisites --> Entry\n");

    char output[OUTPUT_LEN] = {'\0'};
    pTrmClient = new TRMClient();
    if (NULL == pTrmClient)
    {
        DEBUG_PRINT(DEBUG_ERROR, "Failed to create TRMClient instance\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRM testmodule pre_requisites --> Exit\n");
        return "FAILURE";
    }

    try
    {
        if (!pTrmClient->getAllTunerStates(output))
        {
            DEBUG_PRINT(DEBUG_ERROR,"TRM client not registered with recorder client id\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRM testmodule pre_requisites --> Exit\n");
            return "FAILURE";
        }
        else
        {
            DEBUG_PRINT(DEBUG_TRACE, "Tuner states = %s\n", output);

            struct timeval tv;
            gettimeofday( &tv, 0 );
            unsigned long long startTime = ((unsigned long long)tv.tv_sec) * 1000 + ((unsigned long long)tv.tv_usec) / 1000;

            try
            {
                std::string outToken = pTrmClient->reserveTunerForRecord("TestDevice", "TestRecordId", "ocap://0xCNN", startTime, 3000, 0, "", 0);
                if ("" == outToken)
                {
                    DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for record");
                    return "FAILURE";
                }
                else if ( (std::string::npos != outToken.find("-")) )
                {
                    //Valid token is of format aa-bb-cc-dd-ee
                    DEBUG_PRINT(DEBUG_TRACE, "output token = %s \n", outToken.c_str());
                    sleep(3);
                }
                else
                {
                    DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for record with error code = %s\n", outToken.c_str());
                    return "FAILURE";
                }
            }
            catch(...)
            {
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured while reserving tuner for recording\n");
                return "FAILURE";
            }
        }
    }
    catch(...)
    {
        DEBUG_PRINT(DEBUG_TRACE, "Error executing GetAllTunerStates\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRM testmodule pre_requisites --> Exit\n");
        return "FAILURE";
    }

    DEBUG_PRINT(DEBUG_TRACE, "TRM testmodule pre_requisites --> Exit\n");
    return "SUCCESS";
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/

bool TRMAgent::testmodulepost_requisites()
{
    if (NULL != pTrmClient)
    {
       delete pTrmClient;
    }
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_GetMaxTuners

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the max number of tuners.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
void  TRMAgent::TRMAgent_GetMaxTuners(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetMaxTuners --->Entry\n");
#ifdef NUM_OF_TUNERS
    DEBUG_PRINT(DEBUG_TRACE, "Max number of tuners supported by device = %d\n", NUM_OF_TUNERS);
    response["result"] = "SUCCESS";
    ostringstream details;
    details << NUM_OF_TUNERS;
    response["details"] = details.str();
#else
    DEBUG_PRINT(DEBUG_TRACE, "Max number of tuners supported by device unknown\n");
    response["result"] = "FAILURE";
    response["details"] = "0";
#endif
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetMaxTuners -->Exit\n");
    return;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_GetAllTunerIds

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to fetch Ids for all tuners.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
void  TRMAgent::TRMAgent_GetAllTunerIds(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerIds --->Entry\n");

    try
    {
        if (!pTrmClient->getAllTunerIds())
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to get all tuners Ids";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to get all tuners Ids\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerIds --->Exit\n");
            return;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while getting all tuner Ids";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while getting all tuner Ids\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerIds --->Exit\n");
        return;
    }

    response["result"] = "SUCCESS";
    response["details"] = "TRM get all tuner Ids success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerIds -->Exit\n");
    return;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_GetAllTunerStates

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to fetch states for all tuners.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
void TRMAgent::TRMAgent_GetAllTunerStates(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerStates --->Entry\n");
    char output[OUTPUT_LEN] = {'\0'};

    try
    {
        if (!pTrmClient->getAllTunerStates(output))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to get all tuners states";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to get all tuners states\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerStates --->Exit\n");
            return;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while getting all tuner states";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while getting all tuner states\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerStates --->Exit\n");
        return;
    }

    DEBUG_PRINT(DEBUG_TRACE, "output length = %d output value = %s\n", strlen(output),output);
    response["result"] = "SUCCESS";
    response["details"] = output;

    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerStates -->Exit\n");
    return;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_GetAllReservations

Arguments     : Input argument is deviceNo. If deviceNo is default value(-1) send NULL filter value
                to get reservations for all tuners.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to fetch reservation for all tuners.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
void TRMAgent::TRMAgent_GetAllReservations(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllReservations --->Entry\n");
    int deviceNo = req["deviceNo"].asInt();
    string filter = "";
    char output[OUTPUT_LEN] = {'\0'};

    if ((0 <= deviceNo) && (deviceNo <= TOTAL_DEVICE_NUMBER))
    {
	filter = deviceNames[deviceNo];
    }

    try
    {
        if (!pTrmClient->getAllReservations(filter, output))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to get all tuners reservations";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to get all tuners reservations\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllReservations --->Exit\n");
            return;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while getting all reservations";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while getting all reservations\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllReservations --->Exit\n");
        return;
    }

    DEBUG_PRINT(DEBUG_TRACE, "output length = %d output value = %s\n", strlen(output),output);
    response["result"] = "SUCCESS";
    response["details"] = output;
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllReservations -->Exit\n");
    return;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_GetVersion

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to fetch tuner version.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
void TRMAgent::TRMAgent_GetVersion(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetVersion --->Entry\n");

    try
    {
        if (!pTrmClient->getVersion())
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to get tuner version";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to get tuner version\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetVersion --->Exit\n");
            return;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while getting version";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while getting version\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetVersion --->Exit\n");
        return;
    }

    response["result"] = "SUCCESS";
    response["details"] = "TRM get tuner version success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetVersion -->Exit\n");
    return ;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_TunerReserveForRecord

Arguments     : Input argument is deviceNo, recordingId, locator,
				  duration, startTime, hot.
		Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to reserve tuner for recording.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
void TRMAgent::TRMAgent_TunerReserveForRecord(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForRecord --->Entry\n");

    struct timeval tv;
    unsigned long long startTime = 0, duration = 0;

    int deviceNo = req["deviceNo"].asInt();
    string recordingId = req["recordingId"].asString();
    string locator = req["locator"].asString();
    duration = req["duration"].asDouble();
    unsigned long long startTimeAdd = req["startTime"].asDouble();
    bool hot = req["hot"].asInt();
    bool select= req["selectOnConflict"].asInt();
    std::string outToken = "";
    std::string inToken = "";
    if( NULL != &req["token"] )
    {
        inToken = req["token"].asString();
    }

    if (TOTAL_DEVICE_NUMBER < deviceNo)
    {
	response["result"] = "FAILURE";
	response["details"] = "Device Number out of range.";
	DEBUG_PRINT(DEBUG_ERROR,"Device Number out of range.\n");
	DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForRecord --->Exit\n");
	return;
    }

    gettimeofday( &tv, 0 );
    startTime = ((unsigned long long)tv.tv_sec + startTimeAdd) * 1000 + ((unsigned long long)tv.tv_usec) / 1000;

    try
    {
        outToken = pTrmClient->reserveTunerForRecord(deviceNames[deviceNo], recordingId, locator, startTime, duration, hot, inToken, select);
        if ("" == outToken)
        {
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for record\n");
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for record";
        }
        else if ( (std::string::npos != outToken.find("-")) )
        {
            //Valid token is of format aa-bb-cc-dd-ee
            DEBUG_PRINT(DEBUG_TRACE, "output token = %s \n", outToken.c_str());
            response["result"] = "SUCCESS";
            response["details"] = outToken;
        }
        else
        {
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for record with error code = %s\n", outToken.c_str());
            response["result"] = "FAILURE";
            response["details"] = outToken;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while reserving tuner for recording";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while reserving tuner for recording\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForRecord --->Exit\n");
        return;
    }

    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForRecord --->Exit\n");
    return;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_TunerReserveForLive

Arguments     : Input argument is deviceNo, locator, duration, startTime.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to reserve tuner for live viewing.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
void TRMAgent::TRMAgent_TunerReserveForLive(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForLive --->Entry\n");

    struct timeval tv;
    unsigned long long startTime = 0, duration = 0;

    int deviceNo = req["deviceNo"].asInt();
    string locator = req["locator"].asString();
    duration = req["duration"].asDouble();
    unsigned long long startTimeAdd = req["startTime"].asDouble();
    bool select= req["selectOnConflict"].asInt();
    std::string outToken = "";
    std::string inToken = "";
    if( NULL != &req["token"] )
    {
        inToken = req["token"].asString();
    }

    if (TOTAL_DEVICE_NUMBER < deviceNo)
    {
        response["result"] = "FAILURE";
        response["details"] = "Device Number out of range.";
        DEBUG_PRINT(DEBUG_ERROR,"Device Number out of range.\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForLive --->Exit\n");
        return;
    }

    gettimeofday( &tv, 0 );
    startTime = ((unsigned long long)tv.tv_sec + startTimeAdd) * 1000 + ((unsigned long long)tv.tv_usec) / 1000;

    try
    {
        outToken = pTrmClient->reserveTunerForLive(deviceNames[deviceNo], locator, startTime, duration, inToken, select);
        if ("" == outToken)
        {
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for live\n");
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for live";
        }
        else if ( (std::string::npos != outToken.find("-")) )
        {
            //Valid token is of format aa-bb-cc-dd-ee
            DEBUG_PRINT(DEBUG_TRACE, "output token = %s \n", outToken.c_str());
            response["result"] = "SUCCESS";
            response["details"] = outToken;
        }
        else
        {
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for live with error code = %s\n", outToken.c_str());
            response["result"] = "FAILURE";
            response["details"] = outToken;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while reserving tuner for live";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while reserving tuner for live\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForLive --->Exit\n");
        return;
    }

    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForLive --->Exit\n");
    return;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_ReleaseTunerReservation

Arguments     : Input argument is deviceNo, locator and activityType(Live:1/Record:2).
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to release a reservation.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
void TRMAgent::TRMAgent_ReleaseTunerReservation(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ReleaseTunerReservation --->Entry\n");

    int activityType = req["activity"].asInt();
    string locator = req["locator"].asString();
    int deviceNo = req["deviceNo"].asInt();
    if (TOTAL_DEVICE_NUMBER < deviceNo)
    {
        response["result"] = "FAILURE";
        response["details"] = "Device Number out of range.";
        DEBUG_PRINT(DEBUG_ERROR,"Device Number out of range.\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ReleaseTunerReservation --->Exit\n");
        return;
    }

    try
    {
        if (!pTrmClient->releaseTunerReservation(deviceNames[deviceNo], locator, activityType))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to release tuner reservation";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to release tuner reservation\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ReleaseTunerReservation --->Exit\n");
            return;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while releasing tuner reservation";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while releasing tuner reservation\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ReleaseTunerReservation --->Exit\n");
        return;
    }

    response["result"] = "SUCCESS";
    response["details"] = "TRM release tuner reservation success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ReleaseTunerReservation --->Exit\n");
    return;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_ValidateTunerReservation

Arguments     : Input argument is deviceNo, locator and activityType(Live:1/Record:2).
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to validate a reservation.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
void TRMAgent::TRMAgent_ValidateTunerReservation(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ValidateTunerReservation --->Entry\n");

    int activityType = req["activity"].asInt();
    string locator = req["locator"].asString();
    int deviceNo = req["deviceNo"].asInt();
    if (TOTAL_DEVICE_NUMBER < deviceNo)
    {
        response["result"] = "FAILURE";
        response["details"] = "Device Number out of range.";
        DEBUG_PRINT(DEBUG_ERROR,"Device Number out of range.\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ValidateTunerReservation --->Exit\n");
        return;
    }

    try
    {
        if (!pTrmClient->validateTunerReservation(deviceNames[deviceNo], locator, activityType))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to validate tuner reservation";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to validate tuner reservation\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ValidateTunerReservation --->Exit\n");
            return;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while validating tuner reservation";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while validating tuner reservation\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ValidateTunerReservation --->Exit\n");
        return;
    }

    response["result"] = "SUCCESS";
    response["details"] = "TRM validate tuner reservation success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ValidateTunerReservation --->Exit\n");
    return;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_CancelRecording

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to cancel a recording.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
void TRMAgent::TRMAgent_CancelRecording(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelRecording --->Entry\n");

    string locator = req["locator"].asString();

    try
    {
	if (!pTrmClient->cancelRecording(locator))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to cancel recording";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to cancel recording\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelRecording --->Exit\n");
            return;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while cancelling recording";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while cancelling recording\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelRecording --->Exit\n");
        return;
    }

    response["result"] = "SUCCESS";
    response["details"] = "TRM cancel recording success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelRecording --->Exit\n");
    return;
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
**************************************************************************/

bool TRMAgent::cleanup(IN const char* szVersion)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaningup\n");
    return TEST_SUCCESS;
}
/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is TRMAgent Object

Description   : This function will be used to destory the TRMAgent object.
**************************************************************************/
extern "C" void DestroyObject(TRMAgent *stubobj)
{
    DEBUG_PRINT(DEBUG_LOG, "Destroying TRM Agent object\n");
    delete stubobj;
}
