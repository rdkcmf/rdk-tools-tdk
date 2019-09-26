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
#include "libIBus.h"
#include "irMgr.h"
#include "pwrMgr.h"
#include "rdktestagentintf.h"
#include "IARMBUSAgent.h"

int main(int argc,char **argv)
{
    DEBUG_PRINT(DEBUG_TRACE,"[gen_multiple_events pid=%d] <-----------SECOND APPLICATION---Entry-------------->\n", getpid());

    int i = 0;
    int type = 0x0000, code = 0x000;
    int eventId=0;
    char *ownerName = NULL;
    int newState = 0, resrcType = 0;

    if(argc < 3)
    {
        DEBUG_PRINT(DEBUG_TRACE,"[gen_multiple_events pid=%d] Usage: -o ownername -e eventID -t type -c keycode -n newstate -r resrctype\n",getpid());
        DEBUG_PRINT(DEBUG_TRACE,"[gen_multiple_events pid=%d] <-----------SECOND APPLICATION---Exit-------------->\n", getpid());
        exit(0);
    }

    for (i = 1; i < argc; i++)  /* Skip argv[0] (program name). */
    {
        /*
         * Use the 'strcmp' function to compare the argv values
         * to a string of your choice (here, it's the optional
         * argument "-q").  When strcmp returns 0, it means that the
         * two strings are identical.
         */

        if (strcmp(argv[i], "-o") == 0)  /* Process optional arguments. */
        {
            if (argv[i+1] != NULL)
            {
                ownerName = argv[i+1];
                DEBUG_PRINT(DEBUG_TRACE,"[gen_multiple_events pid=%d] ownerName is %s\n",getpid(),ownerName);
            }
        }
        else if (strcmp(argv[i], "-e") == 0)
        {
            if (argv[i+1] != NULL)
            {
                eventId = atoi(argv[i+1]);
                DEBUG_PRINT(DEBUG_TRACE,"[gen_multiple_events pid=%d] eventId is %d\n",getpid(),eventId);
            }
        }
        else if (strcmp(argv[i], "-t") == 0)  /* Process optional arguments. */
        {
            if (argv[i+1] != NULL)
            {
                type = atoi(argv[i+1]);
                DEBUG_PRINT(DEBUG_TRACE,"[gen_multiple_events pid=%d] Type is %d\n",getpid(),type);
            }
        }
        else if (strcmp(argv[i], "-c") == 0)
        {
            if (argv[i+1] != NULL)
            {
                code = atoi(argv[i+1]);
                DEBUG_PRINT(DEBUG_TRACE,"[gen_multiple_events pid=%d] Code is %d\n",getpid(),code);
            }
        }
        else if (strcmp(argv[i], "-n") == 0)  /* Process optional arguments. */
        {
            if (argv[i+1] != NULL)
            {
                newState = atoi(argv[i+1]);
                DEBUG_PRINT(DEBUG_TRACE,"[gen_multiple_events pid=%d] newState is %d\n",getpid(),newState);
            }
        }
        else if (strcmp(argv[i], "-r") == 0)
        {
            if (argv[i+1] != NULL)
            {
                resrcType = atoi(argv[i+1]);
                DEBUG_PRINT(DEBUG_TRACE,"[gen_multiple_events pid=%d] resrcType is %d\n",getpid(),resrcType);
            }
        }
    }

    IARM_Result_t retCode = IARM_RESULT_SUCCESS;
    retCode = IARM_Bus_Init(IARM_BUS_DUMMYMGR_NAME);
    DEBUG_PRINT(DEBUG_LOG,"[gen_multiple_events pid=%d] IARM_Bus_Init ret status = %d\n",getpid(), retCode);
    if (IARM_RESULT_SUCCESS == retCode)
    {
        retCode = IARM_Bus_Connect();
        DEBUG_PRINT(DEBUG_LOG,"[gen_multiple_events pid=%d] IARM_Bus_Connect ret status = %d\n",getpid(), retCode);
        if (IARM_RESULT_SUCCESS == retCode)
        {
            _IARM_Bus_PWRMgr_EventData_tp eventData_pwr;
            /*Broadcasting PWR event*/
            eventData_pwr.data.state.newState = (IARM_Bus_PWRMgr_PowerState_t) newState;
            DEBUG_PRINT(DEBUG_LOG,"[gen_multiple_events pid=%d] Broadcasting PWR event\n",getpid());
            if( clock_gettime( CLOCK_MONOTONIC, &eventData_pwr.data.state.clock_when_event_sent) == -1)
            {
               DEBUG_PRINT(DEBUG_ERROR, "[gen_multiple_events pid=%d] clock gettime error",getpid());
            }
            retCode = IARM_Bus_BroadcastEvent(IARM_BUS_PWRMGR_NAME,IARM_BUS_PWRMGR_EVENT_MODECHANGED,(void*)&eventData_pwr, sizeof(eventData_pwr));
            DEBUG_PRINT(DEBUG_LOG,"[gen_multiple_events pid=%d] IARM_Bus_BroadcastEvent ret status = %d\n",getpid(), retCode);
          
            IRMgr_EventData_tp eventData_ir;
            /*Broadcasting IRKey event*/
            eventData_ir.data.irkey.keyType = type;
            eventData_ir.data.irkey.keyCode = code;
            DEBUG_PRINT(DEBUG_TRACE,"[gen_multiple_events pid=%d] Broadcasting IR event %d %d\n",getpid(),type,code);
            if( clock_gettime( CLOCK_MONOTONIC, &eventData_ir.data.irkey.clock_when_event_sent) == -1)
            {
                DEBUG_PRINT(DEBUG_ERROR, "[gen_multiple_events pid=%d] clock gettime error",getpid());
            }
            retCode = IARM_Bus_BroadcastEvent(IARM_BUS_IRMGR_NAME, IARM_BUS_IRMGR_EVENT_IRKEY, (void*)&eventData_ir, sizeof(eventData_ir));
            DEBUG_PRINT(DEBUG_LOG,"[gen_multiple_events pid=%d] IARM_Bus_BroadcastEvent ret status = %d\n",getpid(), retCode);
          
            /*Broadcasting Bus event-ResolutionChange*/
            DEBUG_PRINT(DEBUG_LOG,"[gen_multiple_events pid=%d] Broadcasting ResolutionChange event\n",getpid());
            IARM_Bus_ResolutionChange_EventData_tp eventData_bus1;
            eventData_bus1.width=1;
            eventData_bus1.height=2;
            if( clock_gettime( CLOCK_MONOTONIC, &eventData_bus1.clock_when_event_sent) == -1)
            {
                DEBUG_PRINT(DEBUG_ERROR, "[gen_multiple_events pid=%d] clock gettime error",getpid());
            }
            retCode = IARM_Bus_BroadcastEvent(IARM_BUS_DAEMON_NAME,IARM_BUS_EVENT_RESOLUTIONCHANGE, (void*) &eventData_bus1, sizeof(eventData_bus1));
            DEBUG_PRINT(DEBUG_LOG,"[gen_multiple_events pid=%d] IARM_Bus_BroadcastEvent ret status = %d\n",getpid(), retCode);
          
            sleep(1);

            retCode = IARM_Bus_Disconnect();
            DEBUG_PRINT(DEBUG_LOG,"[gen_multiple_events pid=%d] IARM_Bus_Disconnect ret status = %d\n",getpid(), retCode);
        }
        retCode = IARM_Bus_Term();
        DEBUG_PRINT(DEBUG_LOG,"[gen_multiple_events pid=%d] IARM_Bus_Term ret status = %d\n",getpid(), retCode);
    }
    DEBUG_PRINT(DEBUG_TRACE,"[gen_multiple_events pid=%d] <-----------SECOND APPLICATION---Exit-------------->\n",getpid());
}
