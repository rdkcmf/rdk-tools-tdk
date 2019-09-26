/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2017 RDK Management
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

#include "BluetoothAgent.h"
/***************************************************************************
 *Function name : testmodulepre_requisites
 *Description   : testmodulepre_requisites will be used for setting the
 *                pre-requisites that are necessary for this component
 *                
 *****************************************************************************/

std::string BluetoothAgent::testmodulepre_requisites()
{
    DEBUG_PRINT(DEBUG_TRACE, "Bluetooth testmodule pre_requisites --> Entry\n");
    rc = BTRMGR_Init();
    if (BTRMGR_RESULT_SUCCESS != rc)
    {
        DEBUG_PRINT(DEBUG_TRACE, "Failed to init Bluetooth Manager... Quiting..\n");
        DEBUG_PRINT(DEBUG_TRACE, "Bluetooth testmodule pre_requisites --> Exit\n");
        return "FAILURE";
    }
    else
    {
        DEBUG_PRINT(DEBUG_TRACE, "Bluetooth testmodule pre_requisites --> Exit\n");
        return "SUCCESS";
    }

}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool BluetoothAgent::testmodulepost_requisites()
{
        DEBUG_PRINT(DEBUG_TRACE, "Bluetooth testmodule post_requisites --> Entry\n");
        rc = BTRMGR_DeInit();
        if (BTRMGR_RESULT_SUCCESS != rc)
        {
            DEBUG_PRINT(DEBUG_TRACE, "Failed to Deinit Bluetooth Manager... Quiting..\n");
            DEBUG_PRINT(DEBUG_TRACE, "Bluetooth testmodule pre_requisites --> Exit\n");
            return false;
        }
        else
        {
            DEBUG_PRINT(DEBUG_TRACE, "Bluetooth testmodule pre_requisites --> Exit\n");
            return true;
        }
}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "BluetoothAgent".
**************************************************************************/

extern "C" BluetoothAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
        return new BluetoothAgent(ptrtcpServer);
}

bool BluetoothAgent::initialize(IN const char* szVersion)
{    
        DEBUG_PRINT (DEBUG_TRACE, "Bluetooth Initialization Entry\n");
        DEBUG_PRINT (DEBUG_TRACE, "Bluetooth Initialization Exit\n");
        return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : Bluetooth_GetNumberOfAdapters
 *Descrption    : This function is to get the number of bluetooth adapters
 *****************************************************************************/
void BluetoothAgent::Bluetooth_GetNumberOfAdapters(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetNumberOfAdapters --->Entry\n");
     
   unsigned char numOfAdapters = 0;
   rc = BTRMGR_GetNumberOfAdapters(&numOfAdapters);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       response["details"] = numOfAdapters;
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetNumberOfAdapters call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetNumberOfAdapters --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetNumberOfAdapters call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetNumberOfAdapters -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_GetAdapterName
 *Descrption    : This function is to get the bluetooth adapter name
 *****************************************************************************/
void BluetoothAgent::Bluetooth_GetAdapterName(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetAdapterName --->Entry\n");
   char adapterName[DEVICE_NAME_BUFFER]= {'\0'};
   rc = BTRMGR_GetAdapterName(0, adapterName);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       response["details"] = adapterName;
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetAdapterName call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetAdapterName --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetAdapterName call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetAdapterName -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_SetAdapterName
 *Descrption    : This function is to set the bluetooth adapter name
 *****************************************************************************/
void BluetoothAgent::Bluetooth_SetAdapterName(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterName --->Entry\n");
   char nameAdapter[DEVICE_NAME_BUFFER]= {'\0'};
   strcpy(nameAdapter, req["name"].asCString());
   rc = BTRMGR_SetAdapterName(0, nameAdapter);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       response["details"] = nameAdapter;
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_SetAdapterName call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterName --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_SetAdapterName call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterName -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_GetAdapterPowerStatus
 *Descrption    : This function is to get the bluetooth adapter power status
 *****************************************************************************/
void BluetoothAgent::Bluetooth_GetAdapterPowerStatus(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetAdapterPowerStatus --->Entry\n");
   unsigned char powerStatus;
   rc = BTRMGR_GetAdapterPowerStatus(0, &powerStatus);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       response["details"] = powerStatus;
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetAdapterPowerStatus call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetAdapterPowerStatus --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetAdapterPowerStatus call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetAdapterPowerStatus -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_SetAdapterPowerStatus
 *Descrption    : This function is to set the bluetooth adapter power status
 *****************************************************************************/
void BluetoothAgent::Bluetooth_SetAdapterPowerStatus(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterPowerStatus --->Entry\n");
   unsigned char powerStatus;
   powerStatus = req["powerstatus"].asInt();
   rc = BTRMGR_SetAdapterPowerStatus(0,powerStatus);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_SetAdapterPowerStatus call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterPowerStatus --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_SetAdapterPowerStatus call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterPowerStatus -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_IsAdapterDiscoverable
 *Descrption    : This function is to get the bluetooth discoverable status
 *****************************************************************************/
void BluetoothAgent::Bluetooth_IsAdapterDiscoverable(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_IsAdapterDiscoverable --->Entry\n");
   unsigned char discoverableStatus;
   rc = BTRMGR_IsAdapterDiscoverable(0,&discoverableStatus);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       response["details"] = discoverableStatus;
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_IsAdapterDiscoverable call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_IsAdapterDiscoverable --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_IsAdapterDiscoverable call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_IsAdapterDiscoverable -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_SetAdapterDiscoverable
 *Descrption    : This function is to set the bluetooth discoverable status
 *****************************************************************************/
void BluetoothAgent::Bluetooth_SetAdapterDiscoverable(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterDiscoverable --->Entry\n");
   unsigned char discoverableStatus;
   unsigned char Timeout;
   discoverableStatus = req["discoverablestatus"].asInt();
   Timeout = req["timeout"].asInt();
   rc = BTRMGR_SetAdapterDiscoverable(0,discoverableStatus,Timeout);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_SetAdapterDiscoverable call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterDiscoverable --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_SetAdapterDiscoverable call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterDiscoverable -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_StartDeviceDiscovery
 *Descrption    : This function is to start the device discovery
 *****************************************************************************/
void BluetoothAgent::Bluetooth_StartDeviceDiscovery(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StartDeviceDiscovery --->Entry\n");
   int deviceType;
   BTRMGR_DeviceOperationType_t BT_DEVICE_TYPE;
   deviceType = req["devicetype"].asInt();
   BT_DEVICE_TYPE = (BTRMGR_DeviceOperationType_t) deviceType;
   rc = BTRMGR_StartDeviceDiscovery(0,BT_DEVICE_TYPE);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_StartDeviceDiscovery call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StartDeviceDiscovery --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_StartDeviceDiscovery call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StartDeviceDiscovery -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_StopDeviceDiscovery
 *Descrption    : This function is to stop the device discovery
 *****************************************************************************/
void BluetoothAgent::Bluetooth_StopDeviceDiscovery(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StopDeviceDiscovery --->Entry\n");
   int deviceType;
   BTRMGR_DeviceOperationType_t BT_DEVICE_TYPE;
   deviceType = req["devicetype"].asInt();
   BT_DEVICE_TYPE = (BTRMGR_DeviceOperationType_t) deviceType;
   rc = BTRMGR_StopDeviceDiscovery(0,BT_DEVICE_TYPE);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_StopDeviceDiscovery call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StopDeviceDiscovery --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_StopDeviceDiscovery call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StopDeviceDiscovery -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_GetDiscoveredDevices
 *Descrption    : This function is to get the discovered devices
 *****************************************************************************/
void BluetoothAgent::Bluetooth_GetDiscoveredDevices(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetDiscoveredDevices --->Entry\n");
   BTRMGR_DiscoveredDevicesList_t discoveredDevices;
   rc = BTRMGR_GetDiscoveredDevices(0, &discoveredDevices);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       int j = 0;
       DEBUG_PRINT(DEBUG_TRACE, "Number of Discovered Devices is (%d)  \n", discoveredDevices.m_numOfDevices);
       int deviceNameArraySize = discoveredDevices.m_numOfDevices*DISCOVERED_DEVICE_BUFFER;
       if (deviceNameArraySize)
       {
           char deviceName[deviceNameArraySize]= {'\0'};
           char *deviceNameAddr = deviceName;
           for (; j< discoveredDevices.m_numOfDevices; j++)
           {
               deviceNameAddr += sprintf(deviceNameAddr,"%s:%llu;",discoveredDevices.m_deviceProperty[j].m_name,discoveredDevices.m_deviceProperty[j].m_deviceHandle);
           }
           response["details"] = deviceName;
       }
       else
       {
          response["details"] = "NO_DEVICES_AVAILABLE";
       }
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetDiscoveredDevices call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetDiscoveredDevices --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetDiscoveredDevices call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetDiscoveredDevices -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_ConnectToDevice
 *Descrption    : This function is to connect to a device
 *****************************************************************************/
void BluetoothAgent::Bluetooth_ConnectToDevice(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_ConnectToDevice --->Entry\n");
   unsigned long long int handle;
   int deviceType;
   char handleString[DEVICE_HANDLE_BUFFER]= {'\0'};
   char * pEnd;
   BTRMGR_DeviceOperationType_t BT_DEVICE_TYPE;
   deviceType = req["devicetype"].asInt();
   BT_DEVICE_TYPE = (BTRMGR_DeviceOperationType_t) deviceType;
   strcpy(handleString,req["devicehandle"].asCString());
   handle = strtoull (handleString, &pEnd, 10);
   rc = BTRMGR_ConnectToDevice(0, handle,BT_DEVICE_TYPE);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_ConnectToDevice call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_ConnectToDevice --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_ConnectToDevice call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_ConnectToDevice -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_DisconnectFromDevice
 *Descrption    : This function is to connect to a device
 *****************************************************************************/
void BluetoothAgent::Bluetooth_DisconnectFromDevice(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_DisconnectFromDevice --->Entry\n");
   unsigned long long int handle;
   char handleString[DEVICE_HANDLE_BUFFER]= {'\0'};
   char * pEnd;
   strcpy(handleString,req["devicehandle"].asCString());
   handle = strtoull (handleString, &pEnd, 10);
   rc = BTRMGR_DisconnectFromDevice(0, handle);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_DisconnectFromDevice call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_DisconnectFromDevice --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_DisconnectFromDevice call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_DisconnectFromDevice -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_GetConnectedDevices
 *Descrption    : This function is to get the connected devices
 *****************************************************************************/
void BluetoothAgent::Bluetooth_GetConnectedDevices(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetConnectedDevices --->Entry\n");
   BTRMGR_ConnectedDevicesList_t connectedDevices;
   rc = BTRMGR_GetConnectedDevices(0, &connectedDevices);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       int j = 0;
       DEBUG_PRINT(DEBUG_TRACE, "Number of connected devices is (%d)  \n", connectedDevices.m_numOfDevices);
       int connectedDeviceNameArraySize = connectedDevices.m_numOfDevices*CONNECTED_DEVICE_BUFFER;
       if (connectedDeviceNameArraySize)
       {
           char connectedDeviceName[connectedDeviceNameArraySize]= {'\0'};
           char *connectedDeviceNameAddr = connectedDeviceName;
           for (; j< connectedDevices.m_numOfDevices; j++)
           {
               connectedDeviceNameAddr += sprintf(connectedDeviceNameAddr,"%s;",connectedDevices.m_deviceProperty[j].m_name);
           }
           response["details"] = connectedDeviceName;
       }
       else
       {
          response["details"] = "NO_DEVICES_AVAILABLE";
       }
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetConnectedDevices call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetConnectedDevices --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetConnectedDevices call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetConnectedDevices -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_PairDevice
 *Descrption    : This function is to pair a device
 *****************************************************************************/
void BluetoothAgent::Bluetooth_PairDevice(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_PairDevice --->Entry\n");
   unsigned long long int handle;
   char handleString[DEVICE_HANDLE_BUFFER]= {'\0'};
   char * pEnd;
   strcpy(handleString,req["devicehandle"].asCString());
   handle = strtoull (handleString, &pEnd, 10); 
   rc = BTRMGR_PairDevice(0, handle);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_PairDevice call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_PairDevice --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_PairDevice call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_PairDevice -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_UnpairDevice
 *Descrption    : This function is to unpair a device
 *****************************************************************************/
void BluetoothAgent::Bluetooth_UnpairDevice(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_UnpairDevice --->Entry\n");
   unsigned long long int handle;
   char handleString[DEVICE_HANDLE_BUFFER]= {'\0'};
   char * pEnd;
   strcpy(handleString,req["devicehandle"].asCString());
   handle = strtoull (handleString, &pEnd, 10);
   rc = BTRMGR_UnpairDevice(0, handle);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_UnpairDevice call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_UnpairDevice --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_UnpairDevice call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_UnpairDevice -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_GetPairedDevices
 *Descrption    : This function is to get the paired devices list
 *****************************************************************************/
void BluetoothAgent::Bluetooth_GetPairedDevices(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetPairedDevices --->Entry\n");
   BTRMGR_PairedDevicesList_t pairedDevices;
   rc = BTRMGR_GetPairedDevices(0, &pairedDevices);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       int j = 0;
       DEBUG_PRINT(DEBUG_TRACE, "Number of paired devices is (%d)  \n", pairedDevices.m_numOfDevices);
       int pairedDeviceNameArraySize = pairedDevices.m_numOfDevices*PAIRED_DEVICE_BUFFER;
       if (pairedDeviceNameArraySize)
       {
           char pairedDeviceName[pairedDeviceNameArraySize]= {'\0'};
           char *pairedDeviceNameAddr = pairedDeviceName;
           for (; j< pairedDevices.m_numOfDevices; j++)
           {
               pairedDeviceNameAddr += sprintf(pairedDeviceNameAddr,"%s:%llu;",pairedDevices.m_deviceProperty[j].m_name,pairedDevices.m_deviceProperty[j].m_deviceHandle);
           }
           response["details"] = pairedDeviceName;
       }
       else
       {
          response["details"] = "NO_DEVICES_AVAILABLE";
       }
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetPairedDevices call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetPairedDevices --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetPairedDevices call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetPairedDevices -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_GetDeviceProperties
 *Descrption    : This function is to get the discovered devices properties
 *****************************************************************************/
void BluetoothAgent::Bluetooth_GetDeviceProperties(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetDeviceProperties --->Entry\n");
   BTRMGR_DevicesProperty_t deviceProperty;
   unsigned long long int handle;
   char handleString[DEVICE_HANDLE_BUFFER]= {'\0'};
   char * pEnd;
   strcpy(handleString,req["devicehandle"].asCString());
   handle = strtoull (handleString, &pEnd, 10); 
   rc = BTRMGR_GetDeviceProperties(0, handle, &deviceProperty);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       char deviceProperties[DEVICE_PROPERTIES_BUFFER]= {'\0'};
       char *devicePropertiesAddr = deviceProperties;
       devicePropertiesAddr += sprintf(devicePropertiesAddr,"{'handle':'%llu','name':'%s','paired':'%d','connected':'%d'}",deviceProperty.m_deviceHandle,deviceProperty.m_name,deviceProperty.m_isPaired,deviceProperty.m_isConnected);
       response["details"] = deviceProperties;
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetDeviceProperties call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetDeviceProperties --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetDeviceProperties call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetDeviceProperties -->Exit\n");
       return ;
   }
}

/****************************************************************************************************************************
 *Function name :  Bluetooth_StartAudioStreamingOut
 *Descrption    : This function is to start audio streaming out
 ****************************************************************************************************************************/
void BluetoothAgent::Bluetooth_StartAudioStreamingOut(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StartAudioStreamingOut --->Entry\n");
   unsigned long long int handle;
   int deviceType;
   char handleString[DEVICE_HANDLE_BUFFER]= {'\0'};
   char * pEnd;
   BTRMGR_DeviceOperationType_t BT_DEVICE_TYPE;
   deviceType = req["devicetype"].asInt();
   BT_DEVICE_TYPE = (BTRMGR_DeviceOperationType_t) deviceType;
   strcpy(handleString,req["devicehandle"].asCString());
   handle = strtoull (handleString, &pEnd, 10);
   rc = BTRMGR_StartAudioStreamingOut(0, handle,BT_DEVICE_TYPE);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_StartAudioStreamingOut call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StartAudioStreamingOut --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_StartAudioStreamingOut call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StartAudioStreamingOut -->Exit\n");
       return ;
   }
}

/****************************************************************************************************************************
 *Function name :  Bluetooth_StopAudioStreamingOut
 *Descrption    : This function is to stop the audio streaming out
 ****************************************************************************************************************************/
void BluetoothAgent::Bluetooth_StopAudioStreamingOut(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StopAudioStreamingOut --->Entry\n");
   unsigned long long int handle;
   char handleString[DEVICE_HANDLE_BUFFER]= {'\0'};
   char * pEnd;
   strcpy(handleString,req["devicehandle"].asCString());
   handle = strtoull (handleString, &pEnd, 10);
   rc = BTRMGR_StopAudioStreamingOut(0, handle);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_StopAudioStreamingOut call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StopAudioStreamingOut --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_StopAudioStreamingOut call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StopAudioStreamingOut -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_IsAudioStreamingOut
 *Descrption    : This function is to get the audio streaming status
 *****************************************************************************/
void BluetoothAgent::Bluetooth_IsAudioStreamingOut(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_IsAudioStreamingOut --->Entry\n");
   unsigned char audioStreamingStatus;
   rc = BTRMGR_IsAudioStreamingOut(0,&audioStreamingStatus);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       response["details"] = audioStreamingStatus;
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_IsAudioStreamingOut call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_IsAudioStreamingOut --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_IsAudioStreamingOut call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_IsAudioStreamingOut -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_ResetAdapter
 *Descrption    : This function is to reset the bluetooth adapter
 *****************************************************************************/
void BluetoothAgent::Bluetooth_ResetAdapter(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_ResetAdapter --->Entry\n");
    rc = BTRMGR_ResetAdapter(0);
    if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_ResetAdapter call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_ResetAdapter --->Exit\n");
       return ;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_ResetAdapter call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_ResetAdapter -->Exit\n");
       return ;
   }
}

/***************************************************************************
 *Function name : Bluetooth_SendRequest
 *Descrption    : This function is a dummy test funtion
 *****************************************************************************/

void BluetoothAgent::Bluetooth_SendRequest(IN const Json::Value& request, OUT Json::Value& response)
{
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth SendRequest ---> Entry\n");
       response["result"] = "SUCCESS";
       response["details"] = "SUCCESS";
       DEBUG_PRINT(DEBUG_TRACE,"Bluetooth SendRequest ---> Exit\n");
       return ;
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool BluetoothAgent::cleanup(IN const char* szVersion)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaning up\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is BluetoothAgent Object

Description   : This function will be used to destory the BluetoothAgent object.
**************************************************************************/
extern "C" void DestroyObject(BluetoothAgent *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG, "Destroying Bluetooth Agent object\n");
        delete stubobj;
}
