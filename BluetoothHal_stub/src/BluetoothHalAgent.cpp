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
stBTRCoreAdapter gdefaultAdapter;
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
    std::string returnValue = "SUCCESS";
    DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal testmodule pre_requisites --> Entry\n");

    gBTRCoreRet = BTRCore_Init (&gBTRCoreHandle);
    if ((enBTRCoreSuccess != gBTRCoreRet) || (!gBTRCoreHandle))
    {
        DEBUG_PRINT (DEBUG_TRACE, "Failed to initialize Bluetooth Hal... Quiting..\n");
        DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal testmodule pre_requisites --> Exit\n");
        returnValue = "FAILURE";
    }
    else
    {
        DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal testmodule pre_requisites --> Exit\n");
    }

    return returnValue;

}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool BluetoothHalAgent::testmodulepost_requisites ()
{
    bool returnValue = true;
    DEBUG_PRINT(DEBUG_TRACE, "BluetoothHal testmodule post_requisites --> Entry\n");
    if (gBTRCoreHandle) 
    {
        gBTRCoreRet = BTRCore_DeInit (gBTRCoreHandle);
        if (enBTRCoreSuccess != gBTRCoreRet)
        {
            DEBUG_PRINT (DEBUG_TRACE, "Failed to Deinitialize Bluetooth Hal... Quiting..\n");
            DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal testmodule pre_requisites --> Exit\n");
            returnValue = false;
        }
        else
        {
            gBTRCoreHandle = NULL;
            DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal testmodule pre_requisites --> Exit\n");
            returnValue = true;
        }
    }
    return returnValue;
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
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetListOfAdapters call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetListOfAdapters -->Exit\n");
   }

   return;
}

/***************************************************************************
 *Function name : BluetoothHal_RegisterAgent
 *Descrption    : This function is to register an agent handler
 *****************************************************************************/
void BluetoothHalAgent::BluetoothHal_RegisterAgent (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_RegisterAgent --->Entry\n");

   unsigned char agentCapabilities;
   agentCapabilities = req["capabilities"].asInt();

   gBTRCoreRet = BTRCore_RegisterAgent (gBTRCoreHandle, agentCapabilities);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_RegisterAgent call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_RegisterAgent --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_RegisterAgent call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_RegisterAgent -->Exit\n");
   }

   return;
}

/******************************************************************************************
 *Function name : BluetoothHal_UnregisterAgent
 *Descrption    : This function is to un register an agent that was previously registered
 ******************************************************************************************/
void BluetoothHalAgent::BluetoothHal_UnregisterAgent (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_UnregisterAgent --->Entry\n");

   gBTRCoreRet = BTRCore_UnregisterAgent (gBTRCoreHandle);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_UnregisterAgent call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_UnregisterAgent --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_UnregisterAgent call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_UnregisterAgent -->Exit\n");
   }

   return;
}

/***************************************************************************
 *Function name : BluetoothHal_GetAdapter
 *Descrption    : This function is to get the default bluetooth adapter path
 *****************************************************************************/
void BluetoothHalAgent::BluetoothHal_GetAdapter (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapter --->Entry\n");

   //Initialise the adapter handler before retrieving the value
   memset (&gdefaultAdapter, 0, sizeof(gdefaultAdapter));

   gBTRCoreRet = BTRCore_GetAdapter (gBTRCoreHandle, &gdefaultAdapter);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       response["details"] = gdefaultAdapter.pcAdapterPath;
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetAdapter call is SUCCESS");
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetAdapter : Default adapter path : %s", gdefaultAdapter.pcAdapterPath);
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapter --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetAdapter call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapter -->Exit\n");
   }

   return;
}

/******************************************************************************
 *Function name : BluetoothHal_SetAdapter
 *Descrption    : This function is to set the current bluetooth adapter to use
 *******************************************************************************/
void BluetoothHalAgent::BluetoothHal_SetAdapter (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapter --->Entry\n");

   unsigned char adapterNumber;
   adapterNumber = req["adapter_number"].asInt ();

   gBTRCoreRet = BTRCore_SetAdapter (gBTRCoreHandle, adapterNumber);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_SetAdapter call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapter --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_SetAdapter call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapter -->Exit\n");
   }

   return;
}

/***************************************************************************
 *Function name : BluetoothHal_GetAdapters
 *Descrption    : This function is to get the value of org.bluez.Manager.Getadapters
 *****************************************************************************/
void BluetoothHalAgent::BluetoothHal_GetAdapters (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapters --->Entry\n");

   stBTRCoreGetAdapters getAdapters;
   memset (&getAdapters, 0, sizeof(getAdapters));

   gBTRCoreRet = BTRCore_GetAdapters (gBTRCoreHandle, &getAdapters);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       response["details"] = getAdapters.number_of_adapters;
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetAdapters call is SUCCESS");
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetAdapters : Number of adapters : %d", getAdapters.number_of_adapters);
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapters --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetAdapters call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapters -->Exit\n");
   }

   return;
}

/***************************************************************************
 *Function name : BluetoothHal_GetAdapterPower
 *Descrption    : This function is to get the power status of bluetooth adapter
 *****************************************************************************/
void BluetoothHalAgent::BluetoothHal_GetAdapterPower (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterPower --->Entry\n");

   char adapterPath [BT_ADAPTER_STR_LEN] = {'\0'};
   unsigned char powerStatus = 0;
   strcpy (adapterPath, req["adapter_path"].asCString ());

   gBTRCoreRet = BTRCore_GetAdapterPower (gBTRCoreHandle, adapterPath, &powerStatus);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       response["details"] = powerStatus;
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetAdapterPower call is SUCCESS");
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetAdapterPower : Adapter power status is : %x", powerStatus);
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterPower --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetAdapterPower call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterPower -->Exit\n");
   }

   return;
}

/****************************************************************************************
 *Function name : BluetoothHal_SetAdapterPower
 *Descrption    : This function is to set the power status of bluetooth adapter to OFF/ON
 ****************************************************************************************/
void BluetoothHalAgent::BluetoothHal_SetAdapterPower (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapterPower --->Entry\n");

   char adapterPath [BT_ADAPTER_STR_LEN] = {'\0'};
   unsigned char powerStatus = 0;
   strcpy (adapterPath, req["adapter_path"].asCString ());
   powerStatus = req["power_status"].asInt ();

   gBTRCoreRet = BTRCore_SetAdapterPower (gBTRCoreHandle, adapterPath, powerStatus);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_SetAdapterPower call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapterPower --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_SetAdapterPower call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapterPower -->Exit\n");
   }

   return;
}

/***************************************************************************
 *Function name : BluetoothHal_EnableAdapter
 *Descrption    : This function is to enable the bluetooth adapter
 *****************************************************************************/
void BluetoothHalAgent::BluetoothHal_EnableAdapter (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_EnableAdapter --->Entry\n");

   gBTRCoreRet = BTRCore_EnableAdapter (gBTRCoreHandle, &gdefaultAdapter);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       response["details"] = gdefaultAdapter.enable;
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_EnableAdapter call is SUCCESS");
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_EnableAdapter : Adapter is : %s", gdefaultAdapter.enable?"Enabled":"Disabled");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_EnableAdapter --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_EnableAdapter call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_EnableAdapter -->Exit\n");
   }
   
   return;
}

/***************************************************************************
 *Function name : BluetoothHal_DisableAdapter
 *Descrption    : This function is to disable the bluetooth adapter
 *****************************************************************************/
void BluetoothHalAgent::BluetoothHal_DisableAdapter (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_DisableAdapter --->Entry\n");

   gBTRCoreRet = BTRCore_DisableAdapter (gBTRCoreHandle, &gdefaultAdapter);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       response["details"] = gdefaultAdapter.enable;
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_DisableAdapter call is SUCCESS");
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_DisableAdapter : Adapter is : %s", gdefaultAdapter.enable?"Enabled":"Disabled");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_DisableAdapter --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_DisableAdapter call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_DisableAdapter -->Exit\n");
   }

   return;
}

/******************************************************************************
 *Function name : BluetoothHal_GetAdapterAddr
 *Descrption    : This function is to get the address of bluetooth adapter
 *******************************************************************************/
void BluetoothHalAgent::BluetoothHal_GetAdapterAddr (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterAddr --->Entry\n");

   unsigned char adapterNumber;
   char adapterAddress [BT_ADAPTER_STR_LEN] = {'\0'};
   adapterNumber = req["adapter_number"].asInt ();

   gBTRCoreRet = BTRCore_GetAdapterAddr (gBTRCoreHandle, adapterNumber, adapterAddress);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       response["details"] = adapterAddress;
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetAdapterAddr call is SUCCESS");
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetAdapterAddr : Address for bluetooth adapter %d : %s", adapterNumber, adapterAddress);
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterAddr --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetAdapterAddr call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterAddr -->Exit\n");
   }

   return;
}

/****************************************************************************************
 *Function name : BluetoothHal_SetAdapterDiscoverable
 *Descrption    : This function is to set the discoverable status of bluetooth adapter
 ****************************************************************************************/
void BluetoothHalAgent::BluetoothHal_SetAdapterDiscoverable (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapterDiscoverable --->Entry\n");

   char adapterPath [BT_ADAPTER_STR_LEN] = {'\0'};
   unsigned char discoverableStatus = 0;
   strcpy (adapterPath, req["adapter_path"].asCString ());
   discoverableStatus = req["discoverable_status"].asInt ();

   gBTRCoreRet = BTRCore_SetAdapterDiscoverable (gBTRCoreHandle, adapterPath, discoverableStatus);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_SetAdapterDiscoverable call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapterDiscoverable --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_SetAdapterDiscoverable call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapterDiscoverable -->Exit\n");
   }

   return;
}

/********************************************************************************************************
 *Function name : BluetoothHal_SetAdapterDiscoverableTimeout
 *Descrption    : This function is to set the time (in seconds) during which the adapter is discoverable
 ********************************************************************************************************/
void BluetoothHalAgent::BluetoothHal_SetAdapterDiscoverableTimeout (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapterDiscoverableTimeout --->Entry\n");

   char adapterPath [BT_ADAPTER_STR_LEN] = {'\0'};
   unsigned char timeout = 0;
   strcpy (adapterPath, req["adapter_path"].asCString ());
   timeout = req["timeout"].asInt ();

   gBTRCoreRet = BTRCore_SetAdapterDiscoverableTimeout (gBTRCoreHandle, adapterPath, timeout);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_SetAdapterDiscoverableTimeout call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapterDiscoverableTimeout --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_SetAdapterDiscoverableTimeout call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapterDiscoverableTimeout -->Exit\n");
   }

   return;
}

/***********************************************************************************
 *Function name : BluetoothHal_GetAdapterDiscoverableStatus
 *Descrption    : This function is to get the bluetooth adapter discoverable status
 ***********************************************************************************/
void BluetoothHalAgent::BluetoothHal_GetAdapterDiscoverableStatus (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterDiscoverableStatus --->Entry\n");

   char adapterPath [BT_ADAPTER_STR_LEN] = {'\0'};
   unsigned char discoverableStatus;
   strcpy (adapterPath, req["adapter_path"].asCString ());

   gBTRCoreRet = BTRCore_GetAdapterDiscoverableStatus (gBTRCoreHandle, adapterPath, &discoverableStatus);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       response["details"] = discoverableStatus;
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetAdapterDiscoverableStatus call is SUCCESS");
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetAdapterDiscoverableStatus : Discoverable status of bluetooth adapter %s : %s", adapterPath, discoverableStatus?"Discoverable":"Not Discoverable");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterDiscoverableStatus --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetAdapterDiscoverableStatus call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterDiscoverableStatus -->Exit\n");
   }

   return;
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
