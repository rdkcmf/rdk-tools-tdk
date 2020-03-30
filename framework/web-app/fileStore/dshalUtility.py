#!/usr/bin/python
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
import tdklib;
from time import sleep; 
audioPortType = {"LR":0, "HDMI":1, "SPDIF":2, "INVALID":9};
videoPortType = {"RF":0, "BB":1, "SVIDEO":2, "1394":3, "DVI":4, "COMPONENT":5, "HDMI":6, "HDMI_INPUT":7, "INTERNAL":8, "SCART":9, "INVALID":15};
stereoModeType = {"UNKNOWN":0, "MONO":1, "STEREO":2, "SURROUND":3, "PASSTHRU":4, "INVALID":9};
audioEncodingType = {"NONE":0, "DISPLAY":1, "PCM":2, "AC3":3, "EAC3":4, "INVALID":9}
hdcpProtocolVersion = {"VERSION_1X":0, "VERSION_2X":1, "VERSION_MAX":2, "VERSION_INVALID":5};
surroundMode = {"DD":1, "DDPLUS":2};
aspectRatio = {"4x3":0, "16x9":1};
colorSpace = {"RGB":1, "YCbCr422":2, "YCbCr444":3, "YCbCr420":4, "AUTO":5};

def stopDsmgrService(obj):
    expectedResult="SUCCESS";
    status = False;
    tdkTestObj = obj.createTestStep('ExecuteCommand');
    #Check if dsmgr service is running
    cmd = "systemctl status dsmgr.service | grep \"Active:\"";

    #configure the command
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase(expectedResult);

    actualResult = tdkTestObj.getResult();
    print "Exceution result: ", actualResult;

    if expectedResult in actualResult:
        details = tdkTestObj.getResultDetails();
        print "Output: ", details;
        if "active (running)" in details:
            tdkTestObj = obj.createTestStep('ExecuteCommand');
            #Stop dsmgr service 
            cmd = "systemctl stop dsmgr.service";

            #configure the command
            tdkTestObj.addParameter("command", cmd);
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            print "Exceution result: ", actualResult;

            if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                print "Output: ", details;
                sleep(2);
                tdkTestObj.setResultStatus("SUCCESS");
                print "dsmgr service stopped";
                status = True;
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Failed to stop dsmgr service";
        else:
            tdkTestObj.setResultStatus("SUCCESS");
            print "dsmgr service is not running";
            status = True;
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "Command execution failed";
    
    return status;
 
def startDsmgrService(obj):
    expectedResult="SUCCESS";
    status = False;
    tdkTestObj = obj.createTestStep('ExecuteCommand');
    #Check if dsmgr service is running
    cmd = "systemctl status dsmgr.service | grep \"Active:\"";

    #configure the command
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase(expectedResult);

    actualResult = tdkTestObj.getResult();
    print "Exceution result: ", actualResult;

    if expectedResult in actualResult:
        details = tdkTestObj.getResultDetails();
        print "Output: ", details;
        if "active (running)" not in details:
            tdkTestObj = obj.createTestStep('ExecuteCommand');
            #Stop dsmgr service 
            cmd = "systemctl start dsmgr.service";

            #configure the command
            tdkTestObj.addParameter("command", cmd);
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            print "Exceution result: ", actualResult;

            if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                print "Output: ", details;
                sleep(2);
                tdkTestObj.setResultStatus("SUCCESS");
                print "dsmgr service started";
                status = True;
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Failed to start dsmgr service";
        else:
            tdkTestObj.setResultStatus("SUCCESS");
            print "dsmgr service is already running";
            status = True;
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "Command execution failed";
    return status;
