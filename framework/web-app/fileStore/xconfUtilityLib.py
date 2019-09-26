#!/usr/bin/python
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
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
#
#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------

from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.requester import Requester
import requests
from ConfigParser import SafeConfigParser
from jenkinsapi.custom_exceptions import JenkinsAPIException, UnknownJob,  NoBuildData, NotFound
import os
from random import randint
from xconfVariables import *
#--------------------------------------------------------------------------------
# To get the latest TDK build for the given Job.
# Syntax       : getLatestTDKBuild(jobName,branch_name)
# Description  : Get Latest TDK build from jenkins
# Parameters   : jobname - Job name for build
#                branch_name - Branch name for build
#
# Return Value : Latest TDK build 
#---------------------------------------------------------------------------------
def getLatestTDKBuild(jobName,branch_name='master'):

  requests.packages.urllib3.disable_warnings()

  try:
    parser = SafeConfigParser()
    parser.read( os.path.dirname(os.path.abspath(__file__))+'/Configure_Jenkins.ini')
    print "Connecting to Jenkins..."
    # Fetching the credentials from configuration file
    username = parser.get('credentials','username')
    url =  parser.get('credentials','url')
    password =  parser.get('credentials','password')
    # Logging into Jengins
    J = Jenkins(url,requester=Requester(username,password,baseurl=url,ssl_verify=False))

  except  requests.exceptions.HTTPError  as e:
    print "Login to Jenkins failed. Check your url, username or password"

  else:
    print "Fetching the latest build..."

    try:
     job =  J[jobName]

    except UnknownJob:
     print "Unknown Job Name. Please Check and retry."

    else:

     try:
      # Fetching the build ids of the given Job
      build_ids = job.get_build_ids()
      image_file_dir = os.path.dirname(os.path.abspath(__file__))+ '/build-images'+str(randint(0, 100000))
      image_path =  image_file_dir+'/build-images.txt'
      remove_command = 'rm -rf ' + image_file_dir
      make_dir_command = 'mkdir ' + image_file_dir

      for buildid in build_ids:
        # Fetching the build names
        build_name=job.get_build(buildid)
        if os.path.isfile(image_path):
         os.system(remove_command)
        if build_name.is_good():
         all_artifacts = build_name.get_artifact_dict()
         os.system( make_dir_command)
         all_artifacts.get('build-images.txt').save_to_dir( image_file_dir)
         file = open(image_path, "r")
         if os.path.isfile(image_path):
          image_line = file.readline()
          file.close()
          os.system(remove_command)
          image_name_split= image_line.split()
          if image_name_split[0] == VALID_KEYWORD :
                image_name = image_name_split[2]
                if image_name.find(branch_name) != -1 and image_name.find(INVALID_KEYWORD) == -1:
                        image_name_required =image_name
                        print "The latest TDK build is successfully fetched."
                        return image_name_required

      return  null
     #Fetching the Latest TDK build of the given job and branch
     except  requests.exceptions.HTTPError  as e:
      print "Unable to fetch TDK build as no build available for this job in Jenkins"

     except NoBuildData as e:
       print "Some error in fetching the TDK  build of the given job. No build data available for this job"

########## End of Function ##########


# To locate tdk_platform.properties file and fetch value of the given variable
#
# Syntax       : GetPlatformProperties(obj, param)
#
# Parameters   : obj, param. (where param is the name of the variable to be fetcehd)
#
# Return Value : Value of param in properties file

def GetPlatformProperties(obj, param):

    #locate tdk_platform.properties in the device
    tdkTestObj = obj.createTestStep('ExecuteCmd');
    tdkTestObj.addParameter("command", "find / -iname 'tdk_platform.properties' | head -n 1 | tr \"\n\" \" \"");

    expectedresult = "SUCCESS";
    propVal = "";
    tdkTestObj.executeTestCase(expectedresult);

    actualresult= tdkTestObj.getResult();
    fileName = tdkTestObj.getResultDetails().strip();

    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS");
        #extract the value of the given 'param'
        tdkTestObj.addParameter("command", "cat " + fileName + " | grep \"" + param + "\" | cut -d \"=\" -f2 | tr \"\n\" \" \"");
        tdkTestObj.executeTestCase(expectedresult);

        actualresult= tdkTestObj.getResult();
        propVal = tdkTestObj.getResultDetails().strip();

        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            tdkTestObj.setResultStatus("FAILURE");

        return(actualresult, propVal);
    else:
        tdkTestObj.setResultStatus("FAILURE");

    return(actualresult, fileName);

########## End of function ##########


# Get the firmware name either from jenkins or config file
#
# Syntax       : getFirmwareDetails(obj)
#
# Parameters   : obj
#
# Return Value : FirmwareVersion, FirmwareFilename

def getFirmwareDetails(obj):

    actualresult, suffix = GetPlatformProperties(obj, "FW_NAME_SUFFIX")

    tdkTestObj = obj.createTestStep('ExecuteCmd');
    #Parsing the JENKINS_JOB details
    tdkTestObj.addParameter("command","cat /version.txt |grep JENKINS_JOB |cut -d= -f 2");
    tdkTestObj.executeTestCase("SUCCESS");
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();

    if "SUCCESS" in result:
        tdkTestObj.setResultStatus("SUCCESS");
        JENKINS_JOB = details[:-2]
        print "TEST STEP 1: fetch Jenkins job from Version file"
        print "EXPECTED RESULT 1: Should fetch Jenkins job from Version file"
        print "ACTUAL RESULT 1: Jenkins job %s " %JENKINS_JOB
        print "[TEST EXECUTION RESULT] : SUCCESS";

        ###Check if firmware name is to be fetched from jenkins or is available in config file
        if (AUTO_SEARCH_IN_JENKINS =='TRUE'):
             print "Enabled AUTO_SEARCH_IN_JENKINS"

             #validate whether Master image is to be searched in Jenkins or not
             if (SEARCH_MASTER_IN_JENKINS=='TRUE'):
                     print "Enabled SEARCH_MASTER_IN_JENKINS"
                     FirmwareVersion=getLatestTDKBuild(JENKINS_JOB)
                     print "Got Latest Master Image Name ",FirmwareVersion
		     FirmwareFilename =FirmwareVersion + suffix
                     print "Latest Master FirmwareFilename is ",FirmwareFilename;
             else:
                     print "Diabled SEARCH_MASTER_IN_JENKINS"
                     #Searching Latest Stable2 image in Jenkins
                     FirmwareVersion=getLatestTDKBuild(JENKINS_JOB,'stable2')
                     print "Got Latest Stable2 Image Name ",FirmwareVersion
		     FirmwareFilename =FirmwareVersion + suffix
                     print "Latest Stable2 FirmwareFilename is ",FirmwareFilename;
        else:
            print "Disabled AUTO_SEARCH_IN_JENKINS"
            JENKINS_JOB=JENKINS_JOB.replace("-","_")
            exec ("FirmwareVersion=%s"%(JENKINS_JOB))
            print "Success :Got FirmwareVersion",FirmwareVersion
	    FirmwareFilename =FirmwareVersion + suffix
            print "FirmwareFilename is ",FirmwareFilename;

        return(FirmwareVersion, FirmwareFilename);
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "TEST STEP 1: fetch Jenkins job from Version file"
        print "EXPECTED RESULT 1: Should fetch Jenkins job from Version file"
        print "ACTUAL RESULT 1: Jenkins job %s " %details
        print "[TEST EXECUTION RESULT] : SUCCESS";
        print "Unable to fetch Jenkins job from Version file";

########## End of function ##########


# Constructs a curl command to configure xconf server
#
# Syntax       : getXCONFServerConfigCmd(obj, FirmwareVersion, FirmwareFilename, Protocol)
#
# Parameters   : obj, FirmwareVersion, FirmwareFilename, Protocol
#
# Return Value : Curl command for configuration

def getXCONFServerConfigCmd(obj, FirmwareVersion, FirmwareFilename, Protocol):

    ######get MAC details from device
    expectedresult = "SUCCESS"
    actualresult, propVal = GetPlatformProperties(obj, "INTERFACE_FOR_ESTB_MAC");
    if expectedresult in actualresult:
        interface = propVal

        tdkTestObj = obj.createTestStep('ExecuteCmd');
        tdkTestObj.addParameter("command","ifconfig " + interface + "| grep HWaddr | awk '{ print $NF }' | tr \"\n\" \" \"")
        tdkTestObj.executeTestCase(expectedresult)
        #Get the result of execution
        result = tdkTestObj.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        estbMAC = tdkTestObj.getResultDetails().strip();
        print "[TEST EXECUTION DETAILS] : %s" %estbMAC;

        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");
            print "TEST STEP 2: fetch ESTB_MAC from device"
            print "EXPECTED RESULT 2: Should fetch ESTB_MAC from device"
            print "ACTUAL RESULT 2: ESTB_MAC is %s " %estbMAC
            print "[TEST EXECUTION RESULT] : SUCCESS";

        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "TEST STEP 2: fetch ESTB_MAC from device"
            print "EXPECTED RESULT 2: Should fetch ESTB_MAC from device"
            print "ACTUAL RESULT 2: ESTB_MAC is %s " %estbMAC
            print "[TEST EXECUTION RESULT] : FAILURE";
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "Failed to fetch Interface from device"

    Curl_CMD="curl -X PUT -H 'Content-Type: application/json'  -d  '{\"eStbMac\": \""+estbMAC+"\",\"xconfServerConfig\": {\"firmwareDownloadProtocol\": \""+Protocol+"\",\"firmwareFilename\": \""+FirmwareFilename+"\",\"firmwareVersion\": \""+FirmwareVersion+"\",\"firmwareLocation\": \""+FIRMWARELOCATION+"\",\"rebootImmediately\": false}}' '" +CDN_MOC_SERVER +"'"

    return Curl_CMD;

########## End of function ##########


# Gets the name of the current image in the device
#
# Syntax       : getCurrentFirmware(obj)
#
# Parameters   : obj
#
# Return Value : Current image name

def getCurrentFirmware(obj):

    actualresult,suffix = GetPlatformProperties(obj, "FW_NAME_SUFFIX")

    ###get details of the current firmware in the device
    expectedresult = "SUCCESS"
    tdkTestObj = obj.createTestStep('ExecuteCmd');
    tdkTestObj.addParameter("command","cat /version.txt | grep -i imagename | cut -c 11- | tr \"\n\" \" \"");
    tdkTestObj.executeTestCase("SUCCESS");

    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails().strip();

    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP 1: fetch device's current firmware name"
        print "EXPECTED RESULT 1: Should fetch device's current firmware name"
        print "ACTUAL RESULT 1: Image name %s " %details
        print "[TEST EXECUTION RESULT] : SUCCESS";

        FirmwareVersion = details;
	FirmwareFilename =FirmwareVersion + suffix
	return (FirmwareVersion, FirmwareFilename);
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "TEST STEP 1: fetch device's current firmware name"
        print "EXPECTED RESULT 1: Should fetch device's current firmware name"
        print "ACTUAL RESULT 1: Image name %s " %details
        print "[TEST EXECUTION RESULT] : FAILURE";

########## End of function ##########



# Remove a given log file from the  device
#
# Syntax       : removeLog(obj, cdnLog)
#
# Parameters   : obj, cdnLog
#
# Return Value : execution status

def removeLog(obj, cdnLog):

    #Remove the exsisting logs
    tdkTestObj = obj.createTestStep('ExecuteCmd');
    tdkTestObj.addParameter("command","rm " + cdnLog)
    tdkTestObj.executeTestCase("SUCCESS");

    #Get the result of execution
    result = tdkTestObj.getResult();
    print "[TEST EXECUTION RESULT] : %s" %result;
    details = tdkTestObj.getResultDetails();
    print "[TEST EXCEUTION DETAILS] : %s"%details;
    if "SUCCESS" in result:
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP 4: Remove the logfiles"
        print "EXPECTED RESULT 4: Should Remove the logfiles"
        print "ACTUAL RESULT 4: is %s " %details
        print "[TEST EXECUTION RESULT] : SUCCESS"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "TEST STEP 4: Remove the logfiles"
        print "EXPECTED RESULT 4: Should Remove the logfiles"
        print "ACTUAL RESULT 4: is %s " %details
        print "[TEST EXECUTION RESULT] : FAILURE"
    return result;
########## End of function ##########


# To override the default xconf server url used by xconf client
#
# Syntax       : overrideServerUrl(obj, overrideUrl)
#
# Parameters   : obj, overrideUrl
#
# Return Value : Execution status and override file name

def overrideServerUrl(obj, overrideUrl):

    ################get xconf url override file name from tdk_platform.properties
    expectedresult = "SUCCESS"
    actualresult, propVal = GetPlatformProperties(obj, "XCONF_OVERRIDE_FILE")
    if expectedresult in actualresult:
        print "SUCCESS:get xconf override file name"
        xconfFile = propVal
    else:
        print "FAILURE:failed to get xconf override file name"

    ########create a back_up of override file by renaming. Then add the override url
    tdkTestObj = obj.createTestStep('ExecuteCmd');
    tdkTestObj.addParameter("command"," touch " + xconfFile + "; mv " + xconfFile + " " + xconfFile + "_bck ; echo " + overrideUrl + " > " + xconfFile)
    tdkTestObj.executeTestCase("SUCCESS");

    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();

    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP 1: Set new xconf override url"
        print "EXPECTED RESULT 3: Should Set new xconf override url"
        print "ACTUAL RESULT 3: Status: %s " %details
        print "[TEST EXECUTION RESULT] : SUCCESS";
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "TEST STEP 1: Set new xconf override url"
        print "EXPECTED RESULT 3: Should Set new xconf override url"
        print "ACTUAL RESULT 3: Status: %s " %details
        print "[TEST EXECUTION RESULT] : FAILURE";
    return actualresult, xconfFile;
########## End of function ##########


# To restore the contents of xconf override file used by xconf client
#
# Syntax       : restoreOverrideFile(obj, xconfFile)
#
# Parameters   : obj, xconfFile
#
# Return Value : Execution status

def restoreOverrideFile(obj, xconfFile):

    #######restore the override file
    expectedresult = "SUCCESS"
    tdkTestObj = obj.createTestStep('ExecuteCmd');
    tdkTestObj.addParameter("command","mv " + xconfFile + "_bck " + xconfFile)
    tdkTestObj.executeTestCase("SUCCESS");

    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();

    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP 1: restore the override file"
        print "EXPECTED RESULT 3: Should restore the override file"
        print "ACTUAL RESULT 3: Status: %s " %details
        print "[TEST EXECUTION RESULT] : SUCCESS";
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "TEST STEP 1: restore the override file"
        print "EXPECTED RESULT 3: Should restore the override file"
        print "ACTUAL RESULT 3: Status: %s " %details
        print "[TEST EXECUTION RESULT] : FAILURE";
    return actualresult;
########## End of function ##########
