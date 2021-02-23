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

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_RegisterAgent: Executing BTRCore_RegisterAgent() with input (agent capability %d)\n", agentCapabilities);
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

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapter: Executing BTRCore_SetAdapter() with input(adapter number - %d)\n", adapterNumber);
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

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterPower : Executing BTRCore_GetAdapterPower() with input (adapter path - %s)\n", adapterPath);
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

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapterPower : Executing BTRCore_SetAdapterPower() with input (adapter path - %s, power status - %d)\n", adapterPath, powerStatus);
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

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterAddr: Executing BTRCore_GetAdapterAddr() with input(adapter number - %d)\n", adapterNumber);
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

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapterDiscoverable : Executing BTRCore_SetAdapterDiscoverable() with input (adapter path - %s, discoverable  status - %d)\n", adapterPath, discoverableStatus);
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

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapterDiscoverableTimeout : Executing BTRCore_SetAdapterDiscoverableTimeout() with input (adapter path - %s, timeout - %d)\n", adapterPath, timeout);
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

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterDiscoverableStatus : Executing BTRCore_GetAdapterDiscoverableStatus() with input (adapter path - %s)\n", adapterPath);
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

/***************************************************************************
 *Function name : BluetoothHal_GetAdapterName
 *Descrption    : This function is to get the bluetooth adapter name
 *****************************************************************************/
void BluetoothHalAgent::BluetoothHal_GetAdapterName (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterName --->Entry\n");

   char adapterPath [BT_ADAPTER_STR_LEN] = {'\0'};
   char adapterName [BT_ADAPTER_STR_LEN] = {'\0'};
   strcpy (adapterPath, req["adapter_path"].asCString ());

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterName : Executing BTRCore_GetAdapterName() with input (adapter path - %s)\n", adapterPath);
   gBTRCoreRet = BTRCore_GetAdapterName (gBTRCoreHandle, adapterPath, adapterName);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       response["details"] = adapterName;
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterName call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterName : Adapter Name is : %s", adapterName);
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterName --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetAdapterName call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetAdapterName -->Exit\n");
   }

   return;
}


/***************************************************************************
 *Function name : BluetoothHal_SetAdapterName
 *Descrption    : This function is to set the bluetooth adapter name
 *****************************************************************************/
void BluetoothHalAgent::BluetoothHal_SetAdapterName (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapterName --->Entry\n");

   char adapterPath [BT_ADAPTER_STR_LEN] = {'\0'};
   char adapterName [BT_ADAPTER_STR_LEN] = {'\0'};
   strcpy (adapterPath, req["adapter_path"].asCString ());
   strcpy (adapterName, req["adapter_name"].asCString ());

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapterName : Executing BTRCore_SetAdapterName() with input (adapter path - %s, adapter name - %s)\n", adapterPath, adapterName);
   gBTRCoreRet = BTRCore_SetAdapterName (gBTRCoreHandle, adapterPath, adapterName);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapterName call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapterName --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_SetAdapterName call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_SetAdapterName -->Exit\n");
   }

   return;
}

/***************************************************************************
 *Function name : BluetoothHal_GetVersionInfo
 *Descrption    : This function is to get the bluetooth version
 *****************************************************************************/
void BluetoothHalAgent::BluetoothHal_GetVersionInfo (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetVersionInfo --->Entry\n");

   char versionInfo [BT_ADAPTER_STR_LEN] = {'\0'};

   gBTRCoreRet = BTRCore_GetVersionInfo (gBTRCoreHandle, versionInfo);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       response["details"] = versionInfo;
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetVersionInfo call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetVersionInfo : Bluetooth version is : %s", versionInfo);
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetVersionInfo --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetVersionInfo call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetVersionInfo -->Exit\n");
   }

   return;
}

/********************************************************************************************************
 *Function name : BluetoothHal_StartDiscovery
 *Descrption    : This function is to start the device discovery session for a bluetooth adapter
 ********************************************************************************************************/
void BluetoothHalAgent::BluetoothHal_StartDiscovery (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_StartDiscovery --->Entry\n");

   char adapterPath [BT_ADAPTER_STR_LEN] = {'\0'};
   enBTRCoreDeviceType deviceType;
   unsigned int timeout = 0;
   strcpy (adapterPath, req["adapter_path"].asCString ());
   timeout = req["timeout"].asInt ();
   deviceType = (enBTRCoreDeviceType) req["device_type"].asInt ();

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_StartDiscovery : Executing BTRCore_StartDiscovery() with input (adapter path - %s, device type - %d, timeout - %d)\n", adapterPath, deviceType, timeout);
   gBTRCoreRet = BTRCore_StartDiscovery (gBTRCoreHandle, adapterPath, deviceType, timeout);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_StartDiscovery call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_StartDiscovery --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_StartDiscovery call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_StartDiscovery -->Exit\n");
   }

   return;
}

/********************************************************************************************************
 *Function name : BluetoothHal_StopDiscovery
 *Descrption    : This function is to cancel any previous device discovery session for a bluetooth adapter
 ********************************************************************************************************/
void BluetoothHalAgent::BluetoothHal_StopDiscovery (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_StopDiscovery --->Entry\n");

   char adapterPath [BT_ADAPTER_STR_LEN] = {'\0'};
   enBTRCoreDeviceType deviceType;
   strcpy (adapterPath, req["adapter_path"].asCString ());
   deviceType = (enBTRCoreDeviceType) req["device_type"].asInt ();

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_StopDiscovery : Executing BTRCore_StopDiscovery() with input (adapter path - %s, device type - %d)\n", adapterPath, deviceType);
   gBTRCoreRet = BTRCore_StopDiscovery (gBTRCoreHandle, adapterPath, deviceType);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_StopDiscovery call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_StopDiscovery --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_StopDiscovery call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_StopDiscovery -->Exit\n");
   }

   return;
}

/***************************************************************************************************************************
 *Function name : BluetoothHal_GetListOfScannedDevices
 *Descrption    : This function is to get the list of scanned devices along with their device name, device ID, address and path
 ****************************************************************************************************************************/
void BluetoothHalAgent::BluetoothHal_GetListOfScannedDevices (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetListOfScannedDevices --->Entry\n");

   int deviceCount = 0;
   Json::Value jdeviceList;
   Json::Value jdevice;
   stBTRCoreScannedDevicesCount listOfScannedDevices;
   memset (&listOfScannedDevices, 0, sizeof (listOfScannedDevices));

   gBTRCoreRet = BTRCore_GetListOfScannedDevices (gBTRCoreHandle, &listOfScannedDevices);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       //response["details"] = listOfAdapters.number_of_adapters;
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetListOfScannedDevices call is SUCCESS");
       if (listOfScannedDevices.numberOfDevices)
       {
           DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetListOfScannedDevices : Number of devices found : %d", listOfScannedDevices.numberOfDevices);
           DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetListOfScannedDevices : Device details :\n");
           for (;deviceCount < listOfScannedDevices.numberOfDevices; deviceCount++)
           {
               // Retrieve the device details from the device structure list to a json object 
               jdevice ["deviceName"] = listOfScannedDevices.devices[deviceCount].pcDeviceName;
               jdevice ["deviceID"] = listOfScannedDevices.devices[deviceCount].tDeviceId;
               jdevice ["deviceAddress"] = listOfScannedDevices.devices[deviceCount].pcDeviceAddress;
               jdevice ["devicePath"] = listOfScannedDevices.devices[deviceCount].pcDevicePath;

               // Add the json object with device details to the json array
               jdeviceList [deviceCount] = jdevice;
               DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetListOfScannedDevices : Device %d:\n\tDevice Name: %s\n\tDevice ID: %llu\n\tDevice Address: %s\n\tDevice Path: %s\n", deviceCount, listOfScannedDevices.devices[deviceCount].pcDeviceName, listOfScannedDevices.devices[deviceCount].tDeviceId, listOfScannedDevices.devices[deviceCount].pcDeviceAddress, listOfScannedDevices.devices[deviceCount].pcDevicePath);
           }
           response["details"] = jdeviceList;
       }
       else
       {
           response["details"] = "NO_DEVICES_FOUND";
           DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetListOfScannedDevices: No devices found in scanned devices list\n");
       }
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetListOfScannedDevices --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetListOfScannedDevices call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetListOfScannedDevices -->Exit\n");
   }

   return;
}

/********************************************************************************************************
 *Function name : BluetoothHal_PairDevice
 *Descrption    : This function is to initiate the pairing of the device 
 ********************************************************************************************************/
void BluetoothHalAgent::BluetoothHal_PairDevice (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_PairDevice --->Entry\n");

   char deviceIDString [BT_ADAPTER_STR_LEN] = {'\0'};
   unsigned long long int deviceID;
   strcpy (deviceIDString, req["device_id"].asCString ());
   deviceID = strtoull (deviceIDString, NULL, 10);

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_PairDevice : Executing BTRCore_PairDevice() with input (device ID - %llu)\n", deviceID);
   gBTRCoreRet = BTRCore_PairDevice (gBTRCoreHandle, deviceID);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_PairDevice call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_PairDevice --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_PairDevice call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_PairDevice -->Exit\n");
   }

   return;
}

/********************************************************************************************************
 *Function name : BluetoothHal_UnPairDevice
 *Descrption    : This function is to remove the remote device object with given deviceID
 ********************************************************************************************************/
void BluetoothHalAgent::BluetoothHal_UnPairDevice (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_UnPairDevice --->Entry\n");

   char deviceIDString [BT_ADAPTER_STR_LEN] = {'\0'};
   unsigned long long int deviceID;
   strcpy (deviceIDString, req["device_id"].asCString ());
   deviceID = strtoull (deviceIDString, NULL, 10);

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_UnPairDevice : Executing BTRCore_UnPairDevice() with input (device ID - %llu)\n", deviceID);
   gBTRCoreRet = BTRCore_UnPairDevice (gBTRCoreHandle, deviceID);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_UnPairDevice call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_UnPairDevice --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_UnPairDevice call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_UnPairDevice -->Exit\n");
   }

   return;
}

/***************************************************************************************************************************
 *Function name : BluetoothHal_GetListOfPairedDevices
 *Descrption    : This function is to get the list of paired devices along with their device name, device ID, address and path
 ****************************************************************************************************************************/
void BluetoothHalAgent::BluetoothHal_GetListOfPairedDevices (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetListOfPairedDevices --->Entry\n");

   int deviceCount = 0;
   Json::Value jdeviceList;
   Json::Value jdevice;
   stBTRCorePairedDevicesCount listOfPairedDevices;
   memset (&listOfPairedDevices, 0, sizeof (listOfPairedDevices));

   gBTRCoreRet = BTRCore_GetListOfPairedDevices (gBTRCoreHandle, &listOfPairedDevices);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       //response["details"] = listOfAdapters.number_of_adapters;
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetListOfPairedDevices call is SUCCESS");
       if (listOfPairedDevices.numberOfDevices)
       {
           DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetListOfPairedDevices : Number of devices found : %d", listOfPairedDevices.numberOfDevices);
           DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetListOfPairedDevices : Device details :\n");
           for (;deviceCount < listOfPairedDevices.numberOfDevices; deviceCount++)
           {
               // Retrieve the device details from the device structure list to a json object 
               jdevice ["deviceName"] = listOfPairedDevices.devices[deviceCount].pcDeviceName;
               jdevice ["deviceID"] = listOfPairedDevices.devices[deviceCount].tDeviceId;
               jdevice ["deviceAddress"] = listOfPairedDevices.devices[deviceCount].pcDeviceAddress;
               jdevice ["devicePath"] = listOfPairedDevices.devices[deviceCount].pcDevicePath;

               // Add the json object with device details to the json array
               jdeviceList [deviceCount] = jdevice;
               DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetListOfPairedDevices : Device %d:\n\tDevice Name: %s\n\tDevice ID: %llu\n\tDevice Address: %s\n\tDevice Path: %s\n", deviceCount, listOfPairedDevices.devices[deviceCount].pcDeviceName, listOfPairedDevices.devices[deviceCount].tDeviceId, listOfPairedDevices.devices[deviceCount].pcDeviceAddress, listOfPairedDevices.devices[deviceCount].pcDevicePath);
           }
           response["details"] = jdeviceList;
       }
       else
       {
           response["details"] = "NO_DEVICES_PAIRED";
           DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetListOfPairedDevice: No devices available in the paired devices list\n");
       }
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetListOfPairedDevices --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetListOfPairedDevices call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetListOfPairedDevices -->Exit\n");
   }

   return;
}



/********************************************************************************************************
 *Function name : BluetoothHal_IsDeviceConnectable
 *Descrption    : This function is to check if the device is connectable
 ********************************************************************************************************/
void BluetoothHalAgent::BluetoothHal_IsDeviceConnectable (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_IsDeviceConnectable --->Entry\n");

   char deviceIDString [BT_ADAPTER_STR_LEN] = {'\0'};
   unsigned long long int deviceID;
   strcpy (deviceIDString, req["device_id"].asCString ());
   deviceID = strtoull (deviceIDString, NULL, 10);

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_IsDeviceConnectable : Executing BTRCore_IsDeviceConnectable() with input (device ID - %llu)\n", deviceID);
   gBTRCoreRet = BTRCore_IsDeviceConnectable (gBTRCoreHandle, deviceID);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_IsDeviceConnectable call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_IsDeviceConnectable --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_IsDeviceConnectable call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_IsDeviceConnectable -->Exit\n");
   }

   return;
}

/********************************************************************************************************
 *Function name : BluetoothHal_ConnectDevice
 *Descrption    : This function is to connect any profile the remote device supports
 ********************************************************************************************************/
void BluetoothHalAgent::BluetoothHal_ConnectDevice (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_ConnectDevice --->Entry\n");

   char deviceIDString [BT_ADAPTER_STR_LEN] = {'\0'};
   unsigned long long int deviceID;
   enBTRCoreDeviceType deviceType;
   strcpy (deviceIDString, req["device_id"].asCString ());
   deviceID = strtoull (deviceIDString, NULL, 10);
   deviceType = (enBTRCoreDeviceType) req["device_type"].asInt ();

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_ConnectDevice : Executing BTRCore_ConnectDevice() with input (device ID - %llu, device type - %d)\n", deviceID, deviceType);
   gBTRCoreRet = BTRCore_ConnectDevice (gBTRCoreHandle, deviceID, deviceType);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_ConnectDevice call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_ConnectDevice --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_ConnectDevice call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_ConnectDevice -->Exit\n");
   }

   return;
}

/****************************************************************************************************************
 *Function name : BluetoothHal_DisconnectDevice
 *Descrption    : This function is to gracefully disconnect all connected profiles and then terminates connection
 *****************************************************************************************************************/
void BluetoothHalAgent::BluetoothHal_DisconnectDevice (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_DisconnectDevice --->Entry\n");

   char deviceIDString [BT_ADAPTER_STR_LEN] = {'\0'};
   unsigned long long int deviceID;
   enBTRCoreDeviceType deviceType;
   strcpy (deviceIDString, req["device_id"].asCString ());
   deviceID = strtoull (deviceIDString, NULL, 10);
   deviceType = (enBTRCoreDeviceType) req["device_type"].asInt ();

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_DisconnectDevice : Executing BTRCore_DisconnectDevice() with input (device ID - %llu, device type - %d)\n", deviceID, deviceType);
   gBTRCoreRet = BTRCore_DisconnectDevice (gBTRCoreHandle, deviceID, deviceType);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_DisconnectDevice call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_DisconnectDevice --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_DisconnectDevice call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_DisconnectDevice -->Exit\n");
   }

   return;
}

/****************************************************************************************************************
 *Function name : BluetoothHal_GetDeviceConnected
 *Descrption    : This function is to check if the current device is connected
 *****************************************************************************************************************/
void BluetoothHalAgent::BluetoothHal_GetDeviceConnected (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetDeviceConnected --->Entry\n");

   char deviceIDString [BT_ADAPTER_STR_LEN] = {'\0'};
   unsigned long long int deviceID;
   enBTRCoreDeviceType deviceType;
   strcpy (deviceIDString, req["device_id"].asCString ());
   deviceID = strtoull (deviceIDString, NULL, 10);
   deviceType = (enBTRCoreDeviceType) req["device_type"].asInt ();

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetDeviceConnected : Executing BTRCore_GetDeviceConnected() with input (device ID - %llu, device type - %d)\n", deviceID, deviceType);
   gBTRCoreRet = BTRCore_GetDeviceConnected (gBTRCoreHandle, deviceID, deviceType);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetDeviceConnected call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetDeviceConnected --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetDeviceConnected call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetDeviceConnected -->Exit\n");
   }

   return;
}

/****************************************************************************************************************
 *Function name : BluetoothHal_GetDeviceDisconnected
 *Descrption    : This function is to check if the current device is disconnected
 *****************************************************************************************************************/
void BluetoothHalAgent::BluetoothHal_GetDeviceDisconnected (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetDeviceDisconnected --->Entry\n");

   char deviceIDString [BT_ADAPTER_STR_LEN] = {'\0'};
   unsigned long long int deviceID;
   enBTRCoreDeviceType deviceType;
   strcpy (deviceIDString, req["device_id"].asCString ());
   deviceID = strtoull (deviceIDString, NULL, 10);
   deviceType = (enBTRCoreDeviceType) req["device_type"].asInt ();

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetDeviceDisconnected : Executing BTRCore_GetDeviceDisconnected() with input (device ID - %llu, device type - %d)\n", deviceID, deviceType);
   gBTRCoreRet = BTRCore_GetDeviceDisconnected (gBTRCoreHandle, deviceID, deviceType);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetDeviceDisconnected call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetDeviceDisconnected --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetDeviceDisconnected call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetDeviceDisconnected -->Exit\n");
   }

   return;
}

/********************************************************************************************************
 *Function name : BluetoothHal_FindDevice
 *Descrption    : This function is to check the device entry in the scanned device list
 ********************************************************************************************************/
void BluetoothHalAgent::BluetoothHal_FindDevice (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_FindDevice --->Entry\n");

   char deviceIDString [BT_ADAPTER_STR_LEN] = {'\0'};
   unsigned long long int deviceID;
   strcpy (deviceIDString, req["device_id"].asCString ());
   deviceID = strtoull (deviceIDString, NULL, 10);

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_FindDevice : Executing BTRCore_FindDevice() with input (device ID - %llu)\n", deviceID); 
   gBTRCoreRet = BTRCore_FindDevice (gBTRCoreHandle, deviceID);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_FindDevice call is SUCCESS");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_FindDevice --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_FindDevice call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_FindDevice -->Exit\n");
   }

   return;
}


/********************************************************************************************************
 *Function name : BluetoothHal_FindService
 *Descrption    : This function is to confirm if a given service exists on a device
 ********************************************************************************************************/
void BluetoothHalAgent::BluetoothHal_FindService (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_FindService --->Entry\n");

   char deviceIDString [BT_ADAPTER_STR_LEN] = {'\0'};
   unsigned long long int deviceID;
   char UUID [BT_ADAPTER_STR_LEN] = {'\0'};
   char XMLdata [BT_ADAPTER_STR_LEN] = {'\0'};
   int serviceStatus;
   strcpy (deviceIDString, req["device_id"].asCString ());
   deviceID = strtoull (deviceIDString, NULL, 10);
   strcpy (UUID, req["uuid"].asCString ());
   strcpy (XMLdata, req["xml_data"].asCString ());

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_FindService : Executing BTRCore_FindService() with input (device ID - %llu, UUID - %s, XMLData - %s)\n", deviceID, UUID, XMLdata);
   gBTRCoreRet = BTRCore_FindService (gBTRCoreHandle, deviceID, UUID, XMLdata, &serviceStatus);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       response["details"] = serviceStatus;
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_FindService call is SUCCESS");
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_FindService : Service %s is %s in the device", XMLdata, serviceStatus?"Available":"Not Available");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_FindService --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_FindService call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_FindService -->Exit\n");
   }

   return;
}

/***************************************************************************************************************************
 *Function name : BluetoothHal_GetSupportedServices
 *Descrption    : This function is to get the list of services supported by the device
 ****************************************************************************************************************************/
void BluetoothHalAgent::BluetoothHal_GetSupportedServices (IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetSupportedServices --->Entry\n");

   int serviceCount = 0;
   Json::Value jserviceList;
   Json::Value jservice;
   char deviceIDString [BT_ADAPTER_STR_LEN] = {'\0'};
   unsigned long long int deviceID;
   strcpy (deviceIDString, req["device_id"].asCString ());
   deviceID = strtoull (deviceIDString, NULL, 10);
   stBTRCoreSupportedServiceList listOfServices;
   memset (&listOfServices, 0, sizeof (listOfServices));

   DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetSupportedServices : Executing BTRCore_GetSupportedServices() with input (device ID - %llu)\n", deviceID);
   gBTRCoreRet = BTRCore_GetSupportedServices (gBTRCoreHandle, deviceID, &listOfServices);
   if (enBTRCoreSuccess == gBTRCoreRet)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetSupportedServices call is SUCCESS");
       if (listOfServices.numberOfService)
       {
           DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetSupportedServices : Number of services supported in the devices : %d", listOfServices.numberOfService);
           DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetSupportedServices: Service Details:\n");
           for (;serviceCount < listOfServices.numberOfService; serviceCount++)
           {
               // Retrieve the service details from the service structure list to a json object 
               jservice ["uuid"] = listOfServices.profile[serviceCount].uuid_value;
               jservice ["profileName"] = listOfServices.profile[serviceCount].profile_name;

               // Add the json object with service details to the json array
               jserviceList [serviceCount] = jservice;
               DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetSupportedServices: Service %d:\n\tUUID: %d\n\tProfile Name: %s\n", serviceCount, listOfServices.profile[serviceCount].uuid_value, listOfServices.profile[serviceCount].profile_name);
           }
           response["details"] = jserviceList;
       }
       else
       {
           response["details"] = "NO_SERVICE_AVAILABLE";
           DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetSupportedServices: No services available in the device\n");
       }
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetSupportedServices --->Exit\n");
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT (DEBUG_ERROR, "BluetoothHal_GetSupportedServices call is FAILURE");
       DEBUG_PRINT (DEBUG_TRACE, "BluetoothHal_GetSupportedServices -->Exit\n");
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
