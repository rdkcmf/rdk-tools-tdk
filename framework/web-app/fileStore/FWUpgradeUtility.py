##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
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

#Firmware Location URL : To be updated with the Location URL
FirmwareLocationURL = " "

#Firmware Filename : To be updated with the filename for download
FirmwareFilename = " "

# Get the firmware name
#
# Syntax       : get_FirmwareFilename(obj)
#
# Parameters   : obj
#
# Return Value : tdkTestObj, actualresult, FirmwareFilename

def get_FirmwareFilename(obj):
    #Get the location of platfrom properties file
    tdkTestObj = obj.createTestStep('ExecuteCmd');
    tdkTestObj.addParameter("command", "find / -iname 'tdk_platform.properties' | head -n 1 | tr \"\n\" \" \"");
    expectedresult = "SUCCESS";
    FirmwareFilename = "";
    tdkTestObj.executeTestCase(expectedresult);
    actualresult= tdkTestObj.getResult();
    fileName = tdkTestObj.getResultDetails().strip();

    if expectedresult in actualresult and fileName != " ":
        tdkTestObj.setResultStatus("SUCCESS");
        #Get the Suffix
        tdkTestObj.addParameter("command", "cat " + fileName + " | grep \"" + "FW_NAME_SUFFIX" + "\" | cut -d \"=\" -f2 | tr \"\n\" \" \"");
        tdkTestObj.executeTestCase(expectedresult);
        actualresult= tdkTestObj.getResult();
        suffix = tdkTestObj.getResultDetails().strip();

        if expectedresult in actualresult and suffix != " ":
            tdkTestObj.setResultStatus("SUCCESS");
            tdkTestObj.addParameter("command", "cat /version.txt | grep -i imagename");
            tdkTestObj.executeTestCase(expectedresult);
            actualresult= tdkTestObj.getResult();
            image_details = tdkTestObj.getResultDetails().replace("\\n","");

            if expectedresult in actualresult and image_details != " ":
                tdkTestObj.setResultStatus("SUCCESS");
                imageName = image_details.split(":")[1];
                FirmwareFilename = imageName + suffix;
            else:
                tdkTestObj.setResultStatus("FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
    else:
        tdkTestObj.setResultStatus("FAILURE");

    return(tdkTestObj, actualresult, FirmwareFilename);

