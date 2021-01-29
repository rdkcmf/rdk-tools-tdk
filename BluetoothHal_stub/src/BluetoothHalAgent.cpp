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
#include "BluetoothHalAgent.h"

/*
 * Global Variables
 */
tBTRCoreHandle gBTRCoreHandle = NULL;
enBTRCoreRet gBTRCoreRet = enBTRCoreSuccess;

/*
 * Methods
 */

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Description   : testmodulepre_requisites will be used for setting the
 *                pre-requisites that are necessary for this component
 *                
 *****************************************************************************/

std::string BluetoothHalAgent::testmodulepre_requisites ()
{
    DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal testmodule pre_requisites --> Entry\n");
    if (gBTRCoreHandle) 
    {
        DEBUG_PRINT(DEBUG_TRACE, "BluetoothHal already initialized\n");
        return "SUCCESS";
    }
    gBTRCoreRet = BTRCore_Init (&gBTRCoreHandle);
    if ((enBTRCoreSuccess != gBTRCoreRet) || (!gBTRCoreHandle))
    {
        DEBUG_PRINT (DEBUG_TRACE, "Failed to initialize Bluetooth Hal... Quiting..\n");
        DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal testmodule pre_requisites --> Exit\n");
        return "FAILURE";
    }
    else
    {
        DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal testmodule pre_requisites --> Exit\n");
        return "SUCCESS";
    }

}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool BluetoothHalAgent::testmodulepost_requisites ()
{
    DEBUG_PRINT(DEBUG_TRACE, "BluetoothHal testmodule post_requisites --> Entry\n");
    if (gBTRCoreHandle) 
    {
        gBTRCoreRet = BTRCore_DeInit (gBTRCoreHandle);
        if (enBTRCoreSuccess != gBTRCoreRet)
        {
            DEBUG_PRINT (DEBUG_TRACE, "Failed to Deinitialize Bluetooth Hal... Quiting..\n");
            DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal testmodule pre_requisites --> Exit\n");
            return false;
        }
        else
        {
            gBTRCoreHandle = NULL;
            DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal testmodule pre_requisites --> Exit\n");
            return true;
        }
    }
}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "BluetoothHalAgent".
**************************************************************************/

extern "C" BluetoothHalAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
        return new BluetoothHalAgent(ptrtcpServer);
}

bool BluetoothHalAgent::initialize(IN const char* szVersion)
{    
        DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal Initialization Entry\n");
        DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal Initialization Exit\n");
        return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : BluetoothHal_GetListOfAdapters
 *Descrption    : This function is to get the list of bluetooth adapters
 *****************************************************************************/
void BluetoothHalAgent::BluetoothHal_GetListOfAdapters (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetListOfAdapters --->Entry\n");

   stBTRCoreListAdapters listOfAdapters;
   memset (&listOfAdapters, 0, sizeof (listOfAdapters));

   gBTRCoreRet = BTRCore_GetListOfAdapters (gBTRCoreHandle, &listOfAdapters);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       response["details"] = listOfAdapters.number_of_adapters;
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetListOfAdapters call is SUCCESS");
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetListOfAdapters : Number of adapters : %d", listOfAdapters.number_of_adapters);
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetListOfAdapters --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetListOfAdapters call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetListOfAdapters -->Exit\n");
       return ;
   }
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool BluetoothHalAgent::cleanup(IN const char* szVersion)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaning up\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is BluetoothHalAgent Object

Description   : This function will be used to destory the BluetoothHalAgent object.
**************************************************************************/
extern "C" void DestroyObject(BluetoothHalAgent *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG, "Destroying BluetoothHal Agent object\n");
        delete stubobj;
}