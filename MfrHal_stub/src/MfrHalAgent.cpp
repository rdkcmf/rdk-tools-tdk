/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2021 RDK Management
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

/*
 * Header files
 */
#include "MfrHalAgent.h"

/*
 * Global Variables
 */
mfrError_t gMFRLibRet;
/*
 * Methods
 */

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Description   : testmodulepre_requisites will be used for setting the
 *                pre-requisites that are necessary for this component
 *                
 *****************************************************************************/

std::string MfrHalAgent::testmodulepre_requisites ()
{
    std::string returnValue = "SUCCESS";
    DEBUG_PRINT (DEBUG_TRACE, "MfrHal testmodule pre_requisites --> Entry\n");

    gMFRLibRet = mfr_init ();
    if (mfrERR_NONE != gMFRLibRet)
    {
        DEBUG_PRINT (DEBUG_TRACE, "Failed to initialize Bluetooth Hal... Quiting..\n");
        DEBUG_PRINT (DEBUG_TRACE, "MfrHal testmodule pre_requisites --> Exit\n");
        returnValue = "FAILURE";
    }
    else
    {
        DEBUG_PRINT (DEBUG_TRACE, "MfrHal testmodule pre_requisites --> Exit\n");
    }

    return returnValue;

}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool MfrHalAgent::testmodulepost_requisites ()
{
    bool returnValue = true;
    DEBUG_PRINT(DEBUG_TRACE, "MfrHal testmodule post_requisites --> Entry\n");
    /*
     * Nothing to be done now
     */
    DEBUG_PRINT (DEBUG_TRACE, "MfrHal testmodule pre_requisites --> Exit\n");
    return returnValue;
}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "MfrHalAgent".
**************************************************************************/

extern "C" MfrHalAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
        return new MfrHalAgent(ptrtcpServer);
}

bool MfrHalAgent::initialize(IN const char* szVersion)
{    
        DEBUG_PRINT (DEBUG_TRACE, "MfrHal Initialization Entry\n");
        DEBUG_PRINT (DEBUG_TRACE, "MfrHal Initialization Exit\n");
        return TEST_SUCCESS;
}


/***************************************************************************
 *Function name : MfrHal_GetSerializedData
 *Descrption    : This function retrieve serialized read-Only data from device
 *****************************************************************************/
void MfrHalAgent::MfrHal_GetSerializedData (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "MfrHal_GetSerializedData --->Entry\n");

   mfrSerializedType_t serializedDataType;
   mfrSerializedData_t serializedData;
   serializedDataType = (mfrSerializedType_t) req["data_type"].asInt ();

   gMFRLibRet = mfrGetSerializedData (serializedDataType, &serializedData);
#ifdef MFR_DEFAULT_DATA
   DEBUG_PRINT (DEBUG_TRACE, "MFR_DEFAULT_DATA defined as %s\n", MFR_DEFAULT_DATA);
   if (mfrERR_NONE == gMFRLibRet && (0 != strcmp(MFR_DEFAULT_DATA, serializedData.buf)))
#else
   DEBUG_PRINT (DEBUG_TRACE, "MFR_DEFAULT_DATA not defined\n");
   if (mfrERR_NONE == gMFRLibRet)
#endif
   {
       response["result"] = "SUCCESS";
       response["details"] = serializedData.buf;
       DEBUG_PRINT (DEBUG_TRACE, "MfrHal_GetSerializedData call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "MfrHal_GetSerializedData : Serialized Data : %s", serializedData.buf);
       if (serializedData.freeBuf)
       {
           serializedData.freeBuf (serializedData.buf);
       }
       DEBUG_PRINT (DEBUG_TRACE, "MfrHal_GetSerializedData --->Exit\n");
   }
   else
   {
#ifdef MFR_DEFAULT_DATA
       if (0 == strcmp(MFR_DEFAULT_DATA, serializedData.buf))
       {
           DEBUG_PRINT (DEBUG_ERROR, "MfrHal_GetSerializedData : Serialized Data : %s", serializedData.buf);
       }
#endif
       response["result"] = "FAILURE";
       response["details"] = gMFRLibRet;
       DEBUG_PRINT (DEBUG_ERROR, "MfrHal_GetSerializedData call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "MfrHal_GetSerializedData -->Exit\n");
   }

   return;
}


/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool MfrHalAgent::cleanup(IN const char* szVersion)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaning up\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is MfrHalAgent Object

Description   : This function will be used to destory the MfrHalAgent object.
**************************************************************************/
extern "C" void DestroyObject(MfrHalAgent *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG, "Destroying MfrHal Agent object\n");
        delete stubobj;
}
