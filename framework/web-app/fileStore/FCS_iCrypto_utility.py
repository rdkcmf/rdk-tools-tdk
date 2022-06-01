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
#########################################################################

import re
import os
import tdklib;
import ConfigParser

#Define the search term:
pattern1 = "========"
pattern2 = "FAILED|ERROR"

#TestApps predefined
TESTAPP = {"interfaceTest":"cgfacetests","implementationTest":"cgimptests","nfSecurityTest":"cgnfsecuritytests"}

#Define Module Tests
Tests = {"Vault":[" Vault::ImportExport", " Vault::SetGet"], "Hash" : [" Hash::Hash", " Hash::HMAC"], "Cipher" : [" Cipher::AES"], "DH" : [" DH::Generate"]};

#Create an empty list:
tests = []
expectedResult="SUCCESS";

def getLogFile(obj):
    #Get iCrypto configuration file
    try:
        iCryptoConfigFile = obj.realpath+'fileStore/iCrypto_log.config'
        configParser = ConfigParser.ConfigParser()
        configParser.read(r'%s' % iCryptoConfigFile )
        #iCrypto execution log file
        iCrypto_log = configParser.get('iCryptoTestApp-config', 'logfile')
        logFile = iCrypto_log.split('/')
        logFile = logFile[-1]
        print "iCrypto Execution Log File Name : " , logFile
        return logFile,iCrypto_log
    except:
        print "\nUnable to acquire log file from iCrypto_log.config\nConfigure the log file in iCrypto_log.config to proceed with the testcase"
        exit()

#Prints the given string in title format
def PrintTitle(string=" ",title=0):
    print "#"*50
    print string
    if title:
        print "#"*50

#Filters the test name from the parsed line
def getTestName(line):
    testName = line.split('-')[0].strip(pattern1).strip()
    return testName

#Lists the list of tests performed along with number of PASSED and FAILED testcases

################################ Sample Output ####################################
##################################################
#Summary of Test Results
##################################################
#Vault::ImportExport - 5 PASSED, 5 FAILED
#Vault::SetGet - 6 PASSED, 6 FAILED
#Hash::Hash - 9 PASSED, 0 FAILED
##################################################
###################################################################################
def Summary(fileName):
    PrintTitle("Summary of Test Results",1)
    for line in open(fileName):
        if line !='':
            word = re.findall(pattern1, line)
            if word:
                if "PASSED" and "FAILED" in line:
                    print line.strip(pattern1).strip()

#Lists the number of failures observed as part of the execution
#Parses the output from the iCrypto test app and returns the total number of failures
def getNumberOfFailures(fileName,options=""):
    failed = 0
    Total = False
    for line in open(fileName):
        if line !='':
            word = re.findall("TOTAL", line)
            if "ModuleTest" in options:
                word = True;
            if word:
                try:
                    if "FAILED" in line and "PASSED" in line:
                       Total = line.split(',')[1]
                       failed = failed + int(filter(lambda x: x.isdigit(), Total))
                       print "Number of FAILED testcases:",failed
                except:
                    print "Unexpected error in parsing number of failures"
                    return "error"
    if Total:
        return failed
    else:
        print "Execution is not completed, due to unknown error"
        return "error"

#Lists the testcases performed as part of this execution
################# Sample Output ########################
#======== Vault::ImportExport
#======== Hash::Hash
########################################################
def testnames(fileName):
    for line in open(fileName):
        if line !='':
            word = re.findall(pattern1, line)
            if word:
                tests.append(getTestName(line))
    testlist = list(set(tests))
    return testlist

#Lists the failure details of the testcases performed in the execution
################################# Sample Output #####################################
##################################################
#======== Hash::HMAC
#FAILED: hashImpl->Ingest(sizeof(data) - 1, data) == sizeof(data) - 1, actual: 0
#FAILED: hashImpl->Calculate(128, output) == sizeof(hash_sha256), actual: 0
#FAILED: ::memcmp(output, hash_sha256, sizeof(hash_sha256)) == 0, actual: 4294967251
#FAILED: vault->Delete(keyId) != false, actual: 0
#======== Hash::HMAC - 4 PASSED, 4 FAILED
##################################################
#####################################################################################
def FailureSummary(fileName):
    for line in open(fileName):
        testNames = testnames(fileName)
        if line !='':
            word1 = re.findall(pattern1, line)
            word2 = re.findall(pattern2, line)
            if word1 and pattern1 in line and not word2:
                PrintTitle(line.strip('\n'))
            if word2:
                print line.strip('\n')
                if pattern1 in line:
                    PrintTitle();


#Deletes the logFile present in DUT
def deleteLogFile(obj,iCrypto_log,iCryptoExecutionStatus):
    logFile_in_TM = obj.logpath + '/resultFile'
    if (os.path.isfile(logFile_in_TM)):
        print "Deleting logFile in TM"
        os.remove(logFile_in_TM);
    print "\nDelete the iCrypto Execution log file from STB"
    tdkTestObj = obj.createTestStep('ExecuteCommand');
    cmd = "rm " + iCrypto_log
    print cmd;
    #configre the command
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    if expectedResult in actualResult:
        print "iCrypto Execution log file deleted from STB"
        tdkTestObj.setResultStatus("SUCCESS");
        if "FAILURE" in iCryptoExecutionStatus:
            PrintTitle("iCryptoExecution Status is FAILURE",1);
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print "Unable to delete iCrypto Execution log file from STB"
        tdkTestObj.setResultStatus("FAILURE");


#Executes the configured Test APP
def RunTest(obj,Test,logFile):
    #Test to be executed
    test = TESTAPP[Test];
    print "\nCheck if %s application is present or not"%(test)
    tdkTestObj = obj.createTestStep('ExecuteCommand');
    cmd  = "command -v " + test
    tdkTestObj.addParameter("command", cmd);
    #Execute the test case in STB
    tdkTestObj.executeTestCase("SUCCESS");
    #Get the result of execution
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if not details:
        print "%s application not found"%(test)
        print "Not Proceeding with test case"
        exit()

    #Prmitive test case which associated to this Script
    print "\nStarting iCrypto interface test Execution\n"
    tdkTestObj = obj.createTestStep('SystemUtilAgent_ExecuteBinary');
    tdkTestObj.addParameter("shell_script", "RunAppInBackground.sh");
    tdkTestObj.addParameter("log_file", logFile);
    tdkTestObj.addParameter("tool_path", test);
    tdkTestObj.addParameter("timeout", "3");
    #Execute the test case in STB
    tdkTestObj.executeTestCase("SUCCESS");
    #Get the result of execution
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "[TEST EXECUTION RESULT] : %s" %actualResult;
    if expectedResult not in actualResult:
        print "Unable to execute %s" %(test);
        tdkTestObj.setResultStatus("FAILURE");
    return details

###############################################################################################
# Parses Module Test Result
# Sample Input : GetTestResults(filepath,Cipher)
# Sample Output:
# ======== Cipher::AES
# SUCCESS: key128Id != 0
# SUCCESS: aes != nullptr
# 4c 6f 6f 6b 20 62 65 68 69 6e 64 20 79 6f 75 2c 20 61 20 54 68 72 65 65 2d
# 4d 6f 6e 6b 65 79 21
# ======== Cipher::AES - 8 PASSED, 0 FAILED
###############################################################################################

def GetTestResults(obj,fileName,Test):
    check_pattern=[]
    check_pattern = Tests[Test]
    check_Pattern = [pattern1 + pattern for pattern in check_pattern];
    TestScope = False
    ReturnFile = obj.logpath + '/resultFile'
    TestResult = open(ReturnFile, 'w')
    for checkPattern in check_Pattern:
        for line in open(fileName):
            if line.startswith(checkPattern):
               TestScope = True
            if TestScope:
               TestResult.write(line)
            if TestScope and "PASSED" in line:
               TestScope = False
    TestResult.close()
    return ReturnFile
