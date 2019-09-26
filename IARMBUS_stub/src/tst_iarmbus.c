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

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include "libIBus.h"
#include "libIBusDaemon.h"
#include "pwrMgr.h"
#include "irMgr.h"
#include "sysMgr.h"
#include <time.h>
#include <sys/time.h>

#define DEBUG_PRINT(pui8Debugmsg...)\
      do{\
                char buffer[30];\
                struct timeval tv;\
                time_t curtime;\
                gettimeofday(&tv, NULL); \
                curtime=tv.tv_sec;\
                strftime(buffer,30,"%m-%d-%Y %T.",localtime(&curtime));\
                fprintf(stdout,"%s%ld [%s [pid=%d] %s():%d] ",buffer, tv.tv_usec, "tst_iarmbus", getpid(),__FUNCTION__, __LINE__);\
                fprintf(stdout,pui8Debugmsg);\
                fflush(stdout);\
      }while(0)


/********************************************************
* Function Name : _ReleaseOwnership
* Description   : This the call back function used to rgister with
*                 registercall method
*
********************************************************/

static IARM_Result_t _ReleaseOwnership(void *arg)
{
    DEBUG_PRINT("############### Bus Client _ReleaseOwnership, CLIENT releasing stuff\r\n");
    IARM_Result_t retCode = IARM_RESULT_SUCCESS;
    return retCode;
}

int main(int argc, char *argv[] )
{
        DEBUG_PRINT("\n<-----------SECOND APPLICATION---Entry-------------->\n");

        IARM_Result_t retCode = IARM_RESULT_SUCCESS;

        retCode = IARM_Bus_Init("Bus_Client");
        DEBUG_PRINT("IARM_Bus_Init status = %d\n",retCode);
        if(IARM_RESULT_SUCCESS == retCode) {
                retCode = IARM_Bus_Connect();
                DEBUG_PRINT("IARM_Bus_Connect status = %d\n",retCode);
                if(IARM_RESULT_SUCCESS == retCode) {
                        retCode = IARM_Bus_RegisterCall(IARM_BUS_COMMON_API_ReleaseOwnership, _ReleaseOwnership);
                        DEBUG_PRINT("RegisterCall IARM_BUS_COMMON_API_ReleaseOwnership status = %d\n",retCode);
                        retCode = IARM_BusDaemon_RequestOwnership(IARM_BUS_RESOURCE_FOCUS);
                        DEBUG_PRINT("Requesting Resource focus status = %d\n",retCode);

                        /*Broadcasting Bus event-ResourceAvailable*/
                        IARM_Bus_EventData_t raEventData;
                        raEventData.resrcType = (IARM_Bus_ResrcType_t)0;
                        retCode = IARM_Bus_BroadcastEvent(IARM_BUS_DAEMON_NAME, IARM_BUS_EVENT_RESOURCEAVAILABLE, (void*) &raEventData, sizeof(raEventData));
                        DEBUG_PRINT("Broadcasting Daemon ResourceAvailable Event (id: %d) status=%d\n", IARM_BUS_EVENT_RESOURCEAVAILABLE, retCode);

                        /*Broadcasting Bus event-ResolutionChange*/
                        IARM_Bus_ResolutionChange_EventData_t rcEventData;
                        rcEventData.width=1;
                        rcEventData.height=2;
                        retCode = IARM_Bus_BroadcastEvent(IARM_BUS_DAEMON_NAME, IARM_BUS_EVENT_RESOLUTIONCHANGE, (void*) &rcEventData, sizeof(rcEventData));
                        DEBUG_PRINT("Broadcasting Daemon ResolutionChange Event (id: %d) status=%d\n", IARM_BUS_EVENT_RESOLUTIONCHANGE, retCode);

                        /*Broadcasting IRKey event*/
                        IARM_Bus_IRMgr_EventData_t eventData_ir0;
                        eventData_ir0.data.irkey.keyType = 0x00008000;
                        eventData_ir0.data.irkey.keyCode = 0x00000033;
                        retCode = IARM_Bus_BroadcastEvent(IARM_BUS_IRMGR_NAME, IARM_BUS_IRMGR_EVENT_IRKEY, (void*)&eventData_ir0, sizeof(eventData_ir0));
                        DEBUG_PRINT("Broadcasting Digit3 Key Press IR Event (id: %d) status=%d\n", IARM_BUS_IRMGR_EVENT_IRKEY,retCode);

                        IARM_Bus_IRMgr_EventData_t eventData_ir1;
                        eventData_ir1.data.irkey.keyType = 0x00008100;
                        eventData_ir1.data.irkey.keyCode = 0x00000033;
                        retCode = IARM_Bus_BroadcastEvent(IARM_BUS_IRMGR_NAME, IARM_BUS_IRMGR_EVENT_IRKEY, (void*)&eventData_ir1, sizeof(eventData_ir1));
                        DEBUG_PRINT("Broadcasting Digit3 Key Release IR Event (id: %d) status=%d\n", IARM_BUS_IRMGR_EVENT_IRKEY,retCode);

                        /*Broadcasting PWR event*/
                        IARM_Bus_PWRMgr_EventData_t eventData_pwr;
                        eventData_pwr.data.state.newState = (IARM_Bus_PWRMgr_PowerState_t)IARM_BUS_PWRMGR_POWERSTATE_ON;
                        retCode = IARM_Bus_BroadcastEvent(IARM_BUS_PWRMGR_NAME, IARM_BUS_PWRMGR_EVENT_MODECHANGED,(void*)&eventData_pwr, sizeof(eventData_pwr));
                        DEBUG_PRINT("Broadcasting PWRMgr Mode Changed Event (id: %d) status=%d\n", IARM_BUS_PWRMGR_EVENT_MODECHANGED,retCode);

                        /*Broadcasting SYSMGR event*/
                        IARM_Bus_SYSMgr_EventData_t eventData_sys;
                        eventData_sys.data.xupnpData.deviceInfoLength = 0;
                        retCode = IARM_Bus_BroadcastEvent(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_EVENT_XUPNP_DATA_REQUEST,(void*)&eventData_sys,sizeof(eventData_sys));
                        DEBUG_PRINT("Broadcasting SYSMgr Xupnp Data Request Event (id: %d) status=%d\n", IARM_BUS_SYSMGR_EVENT_XUPNP_DATA_REQUEST,retCode);
                        retCode = IARM_Bus_BroadcastEvent(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_EVENT_XUPNP_DATA_UPDATE,(void*)&eventData_sys,sizeof(eventData_sys));
                        DEBUG_PRINT("Broadcasting SYSMgr Xupnp Data Update Event (id: %d) status=%d\n", IARM_BUS_SYSMGR_EVENT_XUPNP_DATA_UPDATE,retCode);
                        retCode = IARM_Bus_BroadcastEvent(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_EVENT_CARD_FWDNLD,(void*)&eventData_sys,sizeof(eventData_sys));
                        DEBUG_PRINT("Broadcasting SYSMgr CARD FW download Event (id: %d) status=%d\n", IARM_BUS_SYSMGR_EVENT_CARD_FWDNLD,retCode);
                        retCode = IARM_Bus_BroadcastEvent(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_EVENT_HDCP_PROFILE_UPDATE,(void*)&eventData_sys,sizeof(eventData_sys));
                        DEBUG_PRINT("Broadcasting SYSMgr HDCP Profile Update Event (id: %d) status=%d\n", IARM_BUS_SYSMGR_EVENT_HDCP_PROFILE_UPDATE,retCode);
                        retCode = IARM_Bus_BroadcastEvent(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_EVENT_SYSTEMSTATE,(void*)&eventData_sys,sizeof(eventData_sys));
                        DEBUG_PRINT("Broadcasting SYSMgr System State Event (id: %d) status=%d\n", IARM_BUS_SYSMGR_EVENT_SYSTEMSTATE, retCode);

                        sleep(1);

                        retCode = IARM_BusDaemon_ReleaseOwnership(IARM_BUS_RESOURCE_FOCUS);
                        DEBUG_PRINT("Releasing Resource focus status=%d\n",retCode);
                        retCode = IARM_Bus_Disconnect();
                        DEBUG_PRINT("IARM_Bus_Disconnect status = %d\n",retCode);
                }
                retCode = IARM_Bus_Term();
                DEBUG_PRINT("IARM_Bus_Term status = %d\n",retCode);
        }
        DEBUG_PRINT("\n<-----------SECOND APPLICATION---Exit-------------->\n");
}
