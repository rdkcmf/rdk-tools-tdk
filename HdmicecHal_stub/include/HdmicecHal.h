/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2020 RDK Management
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

#ifndef __HDMICECHAL_H__
#define __HDMICECHAL_H__

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
using namespace std;

// CEC Frame Decoding
const int HEADER_OFFSET = 0;
const int OPCODE_OFFSET = 1;
const int OPRAND_OFFSET = 2;

// Src & Destination
static const char *address_[] = {
        "TV",
        "Recording Device 1",
        "Recording Device 2",
        "Tuner 1",
        "Playback Device 1",
        "Audio System",
        "Tuner 2",
        "Tuner 3",
        "Playback Device 2",
        "Recording Device 3",
        "Tuner 4",
        "Playback Device 3",
        "Reserved 12",
        "Reserved 13",
        "Specific Use",
        "Broadcast/Unregistered",
};

// OPCODES
enum
{
        GET_CEC_VERSION                 = 0x9F,
        CEC_VERSION                     = 0x9E,
        DEVICE_VENDOR_ID                = 0x87,
        GIVE_DEVICE_VENDOR_ID           = 0x8C,
        GET_MENU_LANGUAGE               = 0X91,
        SET_MENU_LANGUAGE               = 0X32,
        GIVE_DEVICE_POWER_STATUS        = 0x8F,
        REPORT_POWER_STATUS             = 0x90,
        FEATURE_ABORT                   = 0x00,
        ABORT                           = 0xFF
};

// OPERANDS INFO
static const char *version_[] = {
	"Reserved",
	"Reserved",
	"Reserved",
	"Reserved",
	"Version 1.3a",
	"Version 1.4",
};

static const char *power_modes_[] = {
        "On",
        "Standby",
        "In transition Standby to On",
        "In transition On to Standby",
};

const int MAX_LEN_LANG = 3;
const int MAX_LEN_VENDOR_ID = 3;


#endif //__HDMICECHAL_H__
