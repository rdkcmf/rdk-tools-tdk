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

#ifndef TRM_HELPER_H_
#define TRM_HELPER_H_

#include "rdktestagentintf.h"
#include <arpa/inet.h>
#include <fcntl.h>
#include <errno.h>
#include <stdlib.h>
#include <uuid/uuid.h>
#include <unistd.h>

#include <vector>
#include <map>
#include <string>

#include "trm/Messages.h"
#include "trm/MessageProcessor.h"
#include "trm/Activity.h"
#include "trm/JsonEncoder.h"
#include "trm/JsonDecoder.h"

#define OUTPUT_LEN 2040 // max limit in TDK framework is 2048
#define GUID_LEN   64
#define MAX_RETRY  10

enum Type {
    REQUEST = 0x1234,
    RESPONSE = 0x1800,
    NOTIFICATION = 0x1400,
    UNKNOWN,
};

class TRMClient
{
public:
    bool getAllTunerStates(char *output);
    bool getAllTunerIds(void);
    bool getAllReservations(std::string filterDevice, char *output);
    bool getVersion(void);
    bool validateTunerReservation(std::string device, std::string locator, int activityType);
    std::string reserveTunerForRecord( std::string device, std::string recordingId, std::string locator, uint64_t startTime=0, uint64_t duration=0,
                                bool hot = false, std::string token = "", bool conflict = false);
    std::string reserveTunerForLive( std::string device, std::string locator, uint64_t startTime=0, uint64_t duration=0, std::string token = "", bool conflict = false);
    bool cancelRecordingReservation(std::string reservationToken); // To be called during conflict resolution
    bool cancelLiveReservation(TRM::TunerReservation resrv); // To be called during conflict resolution
    bool releaseTunerReservation(std::string device, std::string locator, int activityType);
    bool cancelledRecording(std::string reservationToken); /*This function shall be called by the application once cancelRecording event is handled*/
    bool cancelRecording(std::string locator);

    static void init();

    TRMClient();
    ~TRMClient();

    static std::string addToReservationDb(TRM::TunerReservation resv);
    static bool removeFromReservationDb(const std::string token);

private:
    TRMClient* impl;
    static bool inited;
    char guid[GUID_LEN];
    static std::map<int,TRM::TunerReservation> tunerReservationDb;
};

class CTRMMonitor : public TRM::MessageProcessor
{
public :
    CTRMMonitor();
    void operator() (const TRM::ReserveTunerResponse &msg) ;
    void operator() (const TRM::CancelRecording &msg);
    void operator() (const TRM::CancelLive &msg);
    void operator() (const TRM::NotifyTunerReservationRelease &msg);
    void operator() (const TRM::ReleaseTunerReservationResponse &msg);
    void operator() (const TRM::ValidateTunerReservationResponse &msg);
    void operator() (const TRM::CancelRecordingResponse &msg);
    void operator() (const TRM::CancelLiveResponse &msg);
    void operator() (const TRM::GetAllTunerIdsResponse &msg);
    void operator() (const TRM::GetAllTunerStatesResponse &msg);
    void operator() (const TRM::GetAllReservationsResponse &msg);
    void operator() (const TRM::GetVersionResponse &msg);
    void operator() (const TRM::NotifyTunerReservationUpdate &msg);
    void operator() (const TRM::NotifyTunerReservationConflicts &msg);
    void operator() (const TRM::NotifyTunerStatesUpdate &msg);
    void operator() (const TRM::NotifyTunerPretune &msg);
};
#endif
