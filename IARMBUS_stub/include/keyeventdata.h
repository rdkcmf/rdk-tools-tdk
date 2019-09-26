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

#ifndef __KEYEVENT_H__
#define __KEYEVENT_H__
#include <time.h>

#ifdef __cplusplus
extern "C"
{
#endif

#define BILLION 1000000000L
/*! Key Event Data */
typedef struct _IRMgr_EventData_tp 
{
	union 
	{
		struct _IRKEY_DATA{
		   /* Declare Event Data structure for IRMGR_EVENT_DUMMY0 */
			int keyType;              /*!< Key type (UP/DOWN/REPEAT) */
			int keyCode;              /*!< Key code */
			struct timespec clock_when_event_sent;   /*!< clock val at send */
        } irkey, fpkey;
	} data;
}IRMgr_EventData_tp; 

typedef struct _IARM_Bus_EventData_tp 
{
	int resrcType;              /*!< resrcType type */
	int width;              /*!< width */
	int height;              /*!height */
	struct timespec clock_when_event_sent;   /*!< clock val at send */
}IARM_Bus_EventData_tp,IARM_Bus_ResolutionChange_EventData_tp; 

typedef struct _IARM_Bus_PWRMgr_EventData_tp 
{
	union 
	{
		struct _PWRMGR_DATA{
			int curState;
			int newState;
			struct timespec clock_when_event_sent;   /*!< clock val at send */
		} state;
	} data;
}IARM_Bus_PWRMgr_EventData_tp; 

#ifdef __cplusplus
}
#endif
#endif //__KEYEVENT_H__
