/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2020 RDK Management
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

#include "DSHalAgent.h"
/***************************************************************************
 *Function name : testmodulepre_requisites
 *Description   : testmodulepre_requisites will be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/
std::string DSHalAgent::testmodulepre_requisites()
{
    DEBUG_PRINT(DEBUG_TRACE, "DSHal testmodule pre_requisites --> Entry\n");
    /*initializing IARMBUS library */
    IARM_Result_t ret;
    ret = IARM_Bus_Init("agent");
    if(ret == 0)
    {
        DEBUG_PRINT(DEBUG_LOG,"\n Application Successfully initializes the IARMBUS library\n");
    }
    else
    {
        DEBUG_PRINT(DEBUG_LOG,"\n Application failed to initializes the IARMBUS library\n");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal testmodule pre_requisites --> Exit\n");
        return "FAILURE";
    }
    DEBUG_PRINT(DEBUG_LOG,"\n Calling IARM_BUS_Connect\n");
    /*connecting application with IARM BUS*/
    ret = IARM_Bus_Connect();
    if(ret == 0)
    {
        DEBUG_PRINT(DEBUG_LOG,"\n Application Successfully connected with IARMBUS\n");

        dsMgr_init();
        dsAudioPortInit();
        dsVideoPortInit();

        DEBUG_PRINT(DEBUG_TRACE, "DSHal testmodule pre_requisites --> Exit\n");
        return "SUCCESS";
    }
    else
    {
        DEBUG_PRINT(DEBUG_LOG,"\n Application failed to connect with IARMBUS\n");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal testmodule pre_requisites --> Exit\n");
        return "FAILURE";
    }
}
/***************************************************************************
 *Function name : testmodulepost_requisites
 *Description    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool DSHalAgent::testmodulepost_requisites()
{
    DEBUG_PRINT(DEBUG_TRACE, "DSHal testmodule post_requisites --> Entry\n");
 
    IARM_Result_t ret;
    dsMgr_term();
    dsAudioPortTerm();
    dsVideoPortTerm();
    
    ret = IARM_Bus_Disconnect();
    if(ret == 0)
    {
        DEBUG_PRINT(DEBUG_LOG,"\n Application Disconnected from IARMBUS \n");
    }
    else
    {
        DEBUG_PRINT(DEBUG_ERROR,"\n Application failed to Disconnect from IARMBUS \n");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal testmodule post_requisites --> Exit\n");
        return TEST_FAILURE;
    }

    ret = IARM_Bus_Term();
    if(ret == 0)
    {
        DEBUG_PRINT(DEBUG_LOG,"\n Application terminated from IARMBUS \n");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal testmodule post_requisites --> Exit\n");
        return TEST_SUCCESS;
    }
    else
    {
        DEBUG_PRINT(DEBUG_ERROR,"\n Application failed to terminate from IARMBUS \n");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal testmodule post_requisites --> Exit\n");
        return TEST_FAILURE;
    }
}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "DSHalAgent".
**************************************************************************/

extern "C" DSHalAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
        return new DSHalAgent(ptrtcpServer);
}

/***************************************************************************
 *Function name : initialize
 *Description    : Initialize Function will be used for registering the wrapper method
 *                with the agent so that wrapper functions will be used in the
 *                script
 *****************************************************************************/

bool DSHalAgent::initialize(IN const char* szVersion)
{
    DEBUG_PRINT (DEBUG_TRACE, "DSHal Initialization Entry\n");
    DEBUG_PRINT (DEBUG_TRACE, "DSHal Initialization Exit\n");
    return TEST_SUCCESS;
}
/***************************************************************************
 *Function name : DSHal_GetVideoPort
 *Description    : This function is to get the video port handle
 *****************************************************************************/
void DSHalAgent::DSHal_GetVideoPort(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "DSHal_GetVideoPort --->Entry\n");
    if(&req["portType"] == NULL || &req["index"] == NULL)
    {
        return;
    }

    dsVideoPortType_t portType = (dsVideoPortType_t) req["portType"].asInt();
    int index = req["index"].asInt();
    dsError_t ret = dsERR_NONE;
    ret = dsGetVideoPort(portType, index, &vpHandle);

    if (ret == dsERR_NONE and vpHandle)
    {
        response["result"] = "SUCCESS";
        response["details"] = "Video port handle retrieved";
        DEBUG_PRINT(DEBUG_LOG, "DSHal_GetVideoPort call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal_GetVideoPort -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        response["details"] = "Videoport handle not retrieved";
        DEBUG_PRINT(DEBUG_ERROR, "DSHal_GetVideoPort call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal_GetVideoPort -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : DSHal_GetAudioPort
 *Description    : This function is to get the audio port handle
 *****************************************************************************/
void DSHalAgent::DSHal_GetAudioPort(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "DSHal_GetAudioPort --->Entry\n");
    if(&req["portType"] == NULL || &req["index"] == NULL)
    {
        return;
    }

    dsAudioPortType_t portType = (dsAudioPortType_t) req["portType"].asInt();
    int index = req["index"].asInt();


    dsError_t ret = dsERR_NONE;
    ret = dsGetAudioPort(portType, index, &apHandle);

    if (ret == dsERR_NONE and apHandle)
    {
        response["result"] = "SUCCESS";
        response["details"] = "Audioport handle retrieved";
        DEBUG_PRINT(DEBUG_LOG, "DSHal_GetAudioPort call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal_GetAudioPort -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        response["details"] = "Audioport handle not retrieved";
        DEBUG_PRINT(DEBUG_ERROR, "DSHal_GetAudioPort call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal_GetAudioPort -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : DSHal_GetSurroundMode
 *Description    : This function is to get the surround mode of the video port
 *****************************************************************************/
void DSHalAgent::DSHal_GetSurroundMode(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "DSHal_GetSurroundMode --->Entry\n");

    dsError_t ret = dsERR_NONE;
    int surroundMode = dsSURROUNDMODE_NONE;
    ret = dsGetSurroundMode(vpHandle, &surroundMode);

    if (ret == dsERR_NONE)
    {
        response["result"] = "SUCCESS";
        response["details"] = surroundMode;
        DEBUG_PRINT(DEBUG_LOG, "DSHal_GetSurroundMode call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal_GetSurroundMode -->Exit\n");
        return;
    }
    if (ret != dsERR_NONE) {
        response["result"] = "FAILURE";
        response["details"] = dsSURROUNDMODE_NONE;
        DEBUG_PRINT(DEBUG_ERROR, "DSHal_GetSurroundMode call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal_GetSurroundMode -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : DSHal_GetStereoMode
 *Description    : This function is to get the stereo mode of the audio port
 *****************************************************************************/
void DSHalAgent::DSHal_GetStereoMode(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "DSHal_GetStereoMode --->Entry\n");

    dsError_t ret = dsERR_NONE;
    dsAudioStereoMode_t stereoMode;

    ret = dsGetStereoMode(apHandle, &stereoMode);

    if (ret == dsERR_NONE)
    {
        response["result"] = "SUCCESS";
        response["details"] = stereoMode;
        DEBUG_PRINT(DEBUG_LOG, "DSHal_GetStereoMode call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal_GetStereodMode -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        response["details"] = "StereoMode not retrieved";
        DEBUG_PRINT(DEBUG_ERROR, "DSHal_GetStereoMode call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal_GetStereoMode -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : DSHal_SetStereoMode
 *Description    : This function is to set the stereo mode of the audio port
 *****************************************************************************/
void DSHalAgent::DSHal_SetStereoMode(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "DSHal_GetStereoMode --->Entry\n");
    if(&req["stereoMode"] == NULL)
    {
        return;
    }

    dsAudioStereoMode_t stereoMode = (dsAudioStereoMode_t) req["stereoMode"].asInt();
    dsError_t ret = dsERR_NONE;

    ret = dsSetStereoMode(apHandle, stereoMode);

    if (ret == dsERR_NONE)
    {
        response["result"] = "SUCCESS";
        response["details"] = "SetStereoMode call success";
        DEBUG_PRINT(DEBUG_LOG, "DSHal_SetStereoMode call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal_SetStereodMode -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        response["details"] = "SetStereoMode call failed";
        DEBUG_PRINT(DEBUG_ERROR, "DSHal_SetStereoMode call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal_SetStereoMode -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : DSHal_GetAudioEncoding
 *Description    : This function is to get the current audio encoding setting for the audio port
 *****************************************************************************/
void DSHalAgent::DSHal_GetAudioEncoding(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "DSHal_GetAudioEncoding --->Entry\n");

    dsError_t ret = dsERR_NONE;
    dsAudioEncoding_t encoding;

    ret = dsGetAudioEncoding(apHandle, &encoding);

    if (ret == dsERR_NONE)
    {
        response["result"] = "SUCCESS";
        response["details"] = encoding;
        DEBUG_PRINT(DEBUG_LOG, "DSHal_GetAudioEncoding call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal_GetAudioEncoding -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        response["details"] = "Encoding setting not retrieved";
        DEBUG_PRINT(DEBUG_ERROR, "DSHal_GetAudioEncoding call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal_GetAudioEncoding -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : DSHal_IsAudioPortEnabled
 *Description    : This function is to indicate whether the specified Audio port is enabled or not
 *****************************************************************************/
void DSHalAgent::DSHal_IsAudioPortEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "DSHal_IsAudioPortEnabled --->Entry\n");

    dsError_t ret = dsERR_NONE;
    bool enabled;

    ret = dsIsAudioPortEnabled(apHandle, &enabled);

    if (ret == dsERR_NONE)
    {
        response["result"] = "SUCCESS";
        response["details"] = enabled;
        DEBUG_PRINT(DEBUG_LOG, "DSHal_IsAudioPortEnabled call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal_IsAudioPortEnabled -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        response["details"] = "Audio port enable status not retrieved";
        DEBUG_PRINT(DEBUG_ERROR, "DSHal_IsAudioPortEnabled call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal_IsAudioPortEnabled -->Exit\n");
        return;
    }
}
/***************************************************************************
 *Function name : DSHal_EnableAudioPort
 *Description    : This function is to enable or disable the specified Audio port
 *****************************************************************************/
void DSHalAgent::DSHal_EnableAudioPort(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "DSHal_EnableAudioPort--->Entry\n");
    if(&req["enable"] == NULL)
    {
        return;
    }

    bool enable = req["enable"].asInt();
    dsError_t ret = dsERR_NONE;

    ret = dsEnableAudioPort(apHandle, enable);

    if (ret == dsERR_NONE)
    {
        response["result"] = "SUCCESS";
        response["details"] = "EnableAudioPort call success";
        DEBUG_PRINT(DEBUG_LOG, "DSHal_EnableAudioPort call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal_EnableAudioPort -->Exit\n");
        return;
    }
    else
    {
        response["result"] = "FAILURE";
        response["details"] = "EnableAudioPort call failed";
        DEBUG_PRINT(DEBUG_ERROR, "DSHal_EnableAudioPort call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "DSHal_EnableAudioPort -->Exit\n");
        return;
    }
}
/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool DSHalAgent::cleanup(IN const char* szVersion)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaning up\n");
    DEBUG_PRINT(DEBUG_TRACE,"\ncleanup ---->Exit\n");

    return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is DSHalAgent Object

Description   : This function will be used to destory the DSHalAgent object.
**************************************************************************/
extern "C" void DestroyObject(DSHalAgent *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG, "Destroying DSHal Agent object\n");
        delete stubobj;
}
