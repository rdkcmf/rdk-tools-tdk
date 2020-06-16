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

#include "DeepSleepHalAgent.h"
std::chrono::time_point<std::chrono::high_resolution_clock> start;
std::chrono::time_point<std::chrono::high_resolution_clock> stop;
/***************************************************************************
 *Function name : testmodulepre_requisites
 *Description   : testmodulepre_requisites will be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/
std::string DeepSleepHalAgent::testmodulepre_requisites()
{
    DEBUG_PRINT(DEBUG_TRACE, "DeepSleepHal testmodule pre_requisites --> Entry\n");
#ifdef ENABLE_DEEP_SLEEP
    DEBUG_PRINT(DEBUG_TRACE, "DeepSleep init ....\n");
    int init = PLAT_DS_INIT();
    if (init == 0){
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_DS_INIT call success\n");
        DEBUG_PRINT(DEBUG_TRACE, "DeepSleepHal testmodule pre_requisites --> Exit\n");
        return "SUCCESS";
    }
    else{
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_DS_INIT call failed\n");
        DEBUG_PRINT(DEBUG_TRACE, "DeepSleepHal testmodule pre_requisites --> Exit\n");
        return "FAILURE";
    }
#else
    DEBUG_PRINT(DEBUG_TRACE, "DeepSleepHal Not Supported\n");
    DEBUG_PRINT(DEBUG_TRACE, "DeepSleepHal testmodule pre_requisites --> Exit\n");
    return "FAILURE";

#endif //ENABLE_DEEP_SLEEP

}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Description    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool DeepSleepHalAgent::testmodulepost_requisites()
{
    DEBUG_PRINT(DEBUG_TRACE, "DeepSleepHal testmodule post_requisites --> Entry\n");
#ifdef ENABLE_DEEP_SLEEP
    DEBUG_PRINT(DEBUG_TRACE, "DeepSleep term ...\n");
    PLAT_DS_TERM();
    DEBUG_PRINT(DEBUG_TRACE, "DeepSleepHal testmodule post_requisites --> Exit\n");
    return TEST_SUCCESS;
#else
    DEBUG_PRINT(DEBUG_TRACE, "DeepSleepHal Not Supported\n");
    DEBUG_PRINT(DEBUG_TRACE, "DeepSleepHal testmodule post_requisites --> Exit\n");
    return TEST_FAILURE;

#endif //ENABLE_DEEP_SLEEP

}

/**************************************************************************
Function Name   : CreateObject
Arguments       : NULL
Description     : This function is used to create a new object of the class "DSHalAgent".
**************************************************************************/
extern "C" DeepSleepHalAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
        return new DeepSleepHalAgent(ptrtcpServer);
}

/***************************************************************************
 *Function name : initialize
 *Description    : Initialize Function will be used for registering the wrapper method
 *                with the agent so that wrapper functions will be used in the
 *                script
 *****************************************************************************/
bool DeepSleepHalAgent::initialize(IN const char* szVersion)
{
    DEBUG_PRINT (DEBUG_TRACE, "DeepSleepHal Initialization Entry\n");
    DEBUG_PRINT (DEBUG_TRACE, "DeepSleepHal Initialization Exit\n");
    return TEST_SUCCESS;
}

/***************************************************************************
 *Function name  : DeepSleepHal_SetDeepSleep
 *Description    : This function is to invoke PLAT_DS_SetDeepSleep
 *****************************************************************************/
void DeepSleepHalAgent::DeepSleepHal_SetDeepSleep(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "DeepSleepHal_SetDeepSleep --->Entry\n");
    char details[100];
    if(&req["timeout"] == NULL)
    {
        response["result"] = "FAILURE";
        response["details"] = "Invalid Timeout Value";
        return;
    }
#ifdef ENABLE_DEEP_SLEEP
#ifdef ENABLE_DEEPSLEEP_WAKEUP_EVT
    bool isGPIOWakeup = 0;
#endif //ENABLE_DEEPSLEEP_WAKEUP_EVT
    uint32_t deep_sleep_timeout = (uint32_t)req["timeout"].asInt();
    DEBUG_PRINT(DEBUG_TRACE, "SetDeepSleep for %u seconds\n",(unsigned int)deep_sleep_timeout);

    start = std::chrono::high_resolution_clock::now();
#ifdef ENABLE_DEEPSLEEP_WAKEUP_EVT
    int ret = PLAT_DS_SetDeepSleep(deep_sleep_timeout, &isGPIOWakeup);
#else
    int ret = PLAT_DS_SetDeepSleep(deep_sleep_timeout);
#endif //ENABLE_DEEPSLEEP_WAKEUP_EVT
    stop = std::chrono::high_resolution_clock::now();

    int freezeDuration = std::chrono::duration_cast<std::chrono::seconds>(stop - start).count();
    if (ret == 0){
        DEBUG_PRINT(DEBUG_TRACE, "Resumed from DeepSleep\n");
#ifdef ENABLE_DEEPSLEEP_WAKEUP_EVT
        DEBUG_PRINT(DEBUG_TRACE, "CPU freeze duration : %d, isGPIOWakeup : %d\n",freezeDuration,isGPIOWakeup);
        sprintf(details,"CPU freeze duration : %d;isGPIOWakeup : %d;PLAT_DS_SetDeepSleep call is SUCCESS",freezeDuration,isGPIOWakeup);
#else
        DEBUG_PRINT(DEBUG_TRACE, "CPU freeze duration : %d\n",freezeDuration);
        sprintf(details,"CPU freeze duration : %d;PLAT_DS_SetDeepSleep call is SUCCESS",freezeDuration);
#endif //ENABLE_DEEPSLEEP_WAKEUP_EVT
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_DS_SetDeepSleep call success\n");
        response["result"]="SUCCESS";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE, "DeepSleepHal_SetDeepSleep --> Exit\n");
    }
    else{
        response["result"]="FAILURE";
        response["details"]="PLAT_DS_SetDeepSleep call failed";
        DEBUG_PRINT(DEBUG_TRACE, "PLAT_DS_SetDeepSleep call failed\n");
        DEBUG_PRINT(DEBUG_TRACE, "DeepSleepHal_SetDeepSleep --> Exit\n");
    }
#else
    response["result"]="FAILURE";
    response["details"]="DeepSleepHal Not Supported";
    DEBUG_PRINT(DEBUG_TRACE, "DeepSleepHal Not Supported\n");
    DEBUG_PRINT(DEBUG_TRACE, "DeepSleepHal_SetDeepSleep --> Exit\n");
#endif //ENABLE_DEEP_SLEEP

    return;
}

/**************************************************************************
Function Name   : cleanup
Arguments       : NULL
Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool DeepSleepHalAgent::cleanup(IN const char* szVersion)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaning up\n");
    DEBUG_PRINT(DEBUG_TRACE,"\ncleanup ---->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject
Arguments     : Input argument is DeepSleepHalAgent Object
Description   : This function will be used to destory the DSHalAgent object.
**************************************************************************/
extern "C" void DestroyObject(DeepSleepHalAgent *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG, "Destroying DeepSleepHal Agent object\n");
        delete stubobj;
}
