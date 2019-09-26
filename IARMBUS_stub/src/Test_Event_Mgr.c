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
#include "iarmUtil.h"
#include "libIARM.h"
#include "libIBus.h"
#include "dummytestmgr.h"
#include "string.h"
#include <time.h>
#include <sys/time.h>
#include <pthread.h>

static pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
static bool stopped = false;

#define DEBUG_PRINT(pui8Debugmsg...)\
      do{\
                char buffer[30];\
                struct timeval tv;\
                time_t curtime;\
                gettimeofday(&tv, NULL); \
                curtime=tv.tv_sec;\
                strftime(buffer,30,"%m-%d-%Y %T.",localtime(&curtime));\
                fprintf(stdout,"%s%ld [%s pid=%d %s():%d] ", buffer, tv.tv_usec, IARM_BUS_DUMMYMGR_NAME, getpid(), __FUNCTION__, __LINE__);\
                fprintf(stdout,pui8Debugmsg);\
                fflush(stdout);\
      }while(0)

/**
 * These functions are invoked from other applications(test agent)
 */
static IARM_Result_t dummyAPI0(void *arg)
{
    DEBUG_PRINT("Enter dummyAPI0\n");
    IARM_Bus_DUMMYMGR_DummyAPI0_Param_t *param = (IARM_Bus_DUMMYMGR_DummyAPI0_Param_t *)arg;
    param->iRet0=(param->iData0)+0x10000000;
    DEBUG_PRINT("Input iData0=%d Output iRet0=%x\n",param->iData0,param->iRet0);
    DEBUG_PRINT("Exit dummyAPI0\n");
    return IARM_RESULT_SUCCESS;

}

static IARM_Result_t dummyAPI1(void *arg)
{
    DEBUG_PRINT("Enter dummyAPI1\n");
    IARM_Bus_DUMMYMGR_DummyAPI1_Param_t *param = (IARM_Bus_DUMMYMGR_DummyAPI1_Param_t *)arg;
    param->iRet1=(param->iData1)+0x10000000;
    DEBUG_PRINT("Input iData1=%d Output iRet1=%x\n",param->iData1,param->iRet1);
    DEBUG_PRINT("Exit dummyAPI1\n");
    return IARM_RESULT_SUCCESS;
}


static IARM_Result_t handlerReady(void *arg)
{
    DEBUG_PRINT("Enter handlerReady\n");
    IARM_Bus_DUMMYMGR_HandlerReady_Param_t *param = (IARM_Bus_DUMMYMGR_HandlerReady_Param_t *)arg;
    stopped = param->stopped;
    DEBUG_PRINT("stopped = %d\n", stopped);
    /* Unlocking on receiving handler */
    pthread_mutex_lock(&lock);
    pthread_cond_signal(&cond);
    pthread_mutex_unlock(&lock);
    DEBUG_PRINT("Exit handlerReady\n");
    return IARM_RESULT_SUCCESS;
}

int main(int argc, char **argv)
{
    IARM_Result_t retCode = IARM_RESULT_SUCCESS;

    DEBUG_PRINT("Starting Dummy Manager\n");

    retCode = IARM_Bus_Init(IARM_BUS_DUMMYMGR_NAME);
    DEBUG_PRINT("IARM_Bus_Init return status = %d\n", retCode);
    if (IARM_RESULT_SUCCESS == retCode)
    {
	    retCode = IARM_Bus_Connect();
            DEBUG_PRINT("IARM_Bus_Connect return status = %d\n", retCode);
            if (IARM_RESULT_SUCCESS == retCode)
            {
	        /* Register the RPC Calls */
	        retCode = IARM_Bus_RegisterEvent(IARM_BUS_DUMMYMGR_EVENT_MAX);
                DEBUG_PRINT("Registering Event IARM_BUS_DUMMYMGR_EVENT_MAX return status = %d\n", retCode);
		retCode = IARM_Bus_RegisterCall(IARM_BUS_DUMMYMGR_API_DummyAPI0, dummyAPI0);
		DEBUG_PRINT("Registering RPC Call dummyAPI0 return status = %d\n", retCode);
		retCode = IARM_Bus_RegisterCall(IARM_BUS_DUMMYMGR_API_DummyAPI1, dummyAPI1);
		DEBUG_PRINT("Registering RPC Call dummyAPI1 return status = %d\n", retCode);
		retCode = IARM_Bus_RegisterCall(IARM_BUS_DUMMYMGR_API_HANDLER_READY, handlerReady);
		DEBUG_PRINT("Registering RPC Call handlerReady return status = %d\n", retCode);

	        DEBUG_PRINT("Lock to get app synced\n");
		/* Lock to get app synced */
		pthread_mutex_lock(&lock);
		pthread_cond_wait(&cond,&lock);
		pthread_mutex_unlock(&lock);

		/* Populate Event Data Here */
        	IARM_Bus_DUMMYMGR_EventData_t eventXData , eventYData , eventZData;

        	memset(eventXData.data.dummy0.dummyData,'\0',DATA_LEN);
        	memset(eventXData.data.dummy0.dummyData,'x',DATA_LEN-1);
        	strncpy(eventXData.data.dummy0.dummyData,argv[1],strlen(argv[1]));

        	memset(eventYData.data.dummy1.dummyData,'\0',DATA_LEN);
        	memset(eventYData.data.dummy1.dummyData,'y',DATA_LEN-1);
        	strncpy(eventYData.data.dummy1.dummyData,argv[1],strlen(argv[1]));

        	memset(eventZData.data.dummy2.dummyData,'\0',DATA_LEN);
        	memset(eventZData.data.dummy2.dummyData,'z',DATA_LEN-1);
		strncpy(eventZData.data.dummy2.dummyData,argv[1],strlen(argv[1]));

		retCode = IARM_Bus_BroadcastEvent(IARM_BUS_DUMMYMGR_NAME,IARM_BUS_DUMMYMGR_EVENT_DUMMYX, &eventXData, sizeof(eventXData));
		DEBUG_PRINT("\nDummy Event X data: %s (size:%d)\n", eventXData.data.dummy0.dummyData, sizeof(eventXData.data.dummy0.dummyData));
		DEBUG_PRINT("IARM_Bus_BroadcastEvent Dummy Event X return status = %d\n", retCode);
		retCode = IARM_Bus_BroadcastEvent(IARM_BUS_DUMMYMGR_NAME,IARM_BUS_DUMMYMGR_EVENT_DUMMYY, &eventYData, sizeof(eventYData));
		DEBUG_PRINT("\nDummy Event Y data: %s (size:%d)\n", eventYData.data.dummy1.dummyData, sizeof(eventYData.data.dummy1.dummyData));
		DEBUG_PRINT("IARM_Bus_BroadcastEvent Dummy Event Y return status = %d\n", retCode);
		retCode = IARM_Bus_BroadcastEvent(IARM_BUS_DUMMYMGR_NAME,IARM_BUS_DUMMYMGR_EVENT_DUMMYZ, &eventZData, sizeof(eventZData));
		DEBUG_PRINT("\nDummy Event Z data: %s (size:%d)\n", eventZData.data.dummy2.dummyData, sizeof(eventZData.data.dummy2.dummyData));
		DEBUG_PRINT("IARM_Bus_BroadcastEvent Dummy Event Z return status = %d\n", retCode);

		DEBUG_PRINT("UnLock app\n");
		/* Lock to get app synced */
		pthread_mutex_lock(&lock);
		pthread_cond_wait(&cond,&lock);
		pthread_mutex_unlock(&lock);

		retCode = IARM_Bus_Disconnect();
                DEBUG_PRINT("IARM_Bus_Disconnect return status = %d\n", retCode);
            }
	    retCode = IARM_Bus_Term();
            DEBUG_PRINT("IARM_Bus_Term return status = %d\n", retCode);
    }
    DEBUG_PRINT("Exiting Dummy Manager\n");
}
