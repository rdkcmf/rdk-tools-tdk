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

#ifndef __DUMMYEVENT_H__
#define __DUMMYEVENT_H__

#include <stdbool.h>
#include <time.h>

#ifdef __cplusplus
extern "C"
{
#endif

#define IARM_BUS_DUMMYMGR_NAME		     "DUMMYMgr"
#define IARM_BUS_DUMMYMGR_API_HANDLER_READY  "HandlerReady"
#define IARM_BUS_DUMMYMGR_API_DummyAPI0      "DummyAPI0"
#define IARM_BUS_DUMMYMGR_API_DummyAPI1      "DummyAPI1"
#define DATA_LEN                             128

char dummydata_x[DATA_LEN];
char dummydata_y[DATA_LEN];
char dummydata_z[DATA_LEN];

/*
 * Declare Published Events
 */
typedef enum _DUMMYMGR_EventId_t {
    IARM_BUS_DUMMYMGR_EVENT_DUMMYX,
    IARM_BUS_DUMMYMGR_EVENT_DUMMYY,
    IARM_BUS_DUMMYMGR_EVENT_DUMMYZ,
    IARM_BUS_DUMMYMGR_EVENT_MAX,
} IARM_Bus_DUMMYMGR_EventId_t;

/*
 * Declare Event Data
 */
typedef struct _DUMMYMGR_EventData_t {
    union {
        struct _EventData_DUMMY_0{
                /* Declare Event Data structure for DUMMYMGR_EVENT_DUMMY0 */
                char dummyData[DATA_LEN];
                struct timespec clock_when_event_sent;   /*!< clock val at send */
        } dummy0;
        struct _EventData_DUMMY_1{
                /* Declare Event Data structure for DUMMYMGR_EVENT_DUMMY1 */
                char dummyData[DATA_LEN];
                struct timespec clock_when_event_sent;   /*!< clock val at send */
        } dummy1;
        struct _EventData_DUMMY_2{
                /* Declare Event Data structure for DUMMYMGR_EVENT_DUMMY2 */
                char dummyData[DATA_LEN];
                struct timespec clock_when_event_sent;   /*!< clock val at send */
        } dummy2;
    } data;
} IARM_Bus_DUMMYMGR_EventData_t;

/*
 * Declare RPC API names and their arguments
 */
typedef struct _IARM_Bus_DUMMYMGR_HandlerReady_Param_t {
    	bool stopped;
}IARM_Bus_DUMMYMGR_HandlerReady_Param_t;

typedef struct _IARM_Bus_DUMMYMGR_DummyAPI0_Param_t {
	int iData0;
	int iRet0;
} IARM_Bus_DUMMYMGR_DummyAPI0_Param_t;

typedef struct _IARM_Bus_DUMMYMGR_DummyAPI1_Param_t {
	int iData1;
	int iRet1;
} IARM_Bus_DUMMYMGR_DummyAPI1_Param_t;

#ifdef __cplusplus
}
#endif
#endif //__DUMMYEVENT_H__
