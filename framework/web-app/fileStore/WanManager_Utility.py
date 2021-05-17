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

from time import sleep;
from tdkbVariables import *;

#The Expected Wan Manager Policies
ExpectedPolicyList = "FIXED_MODE_ON_BOOTUP, FIXED_MODE, PRIMARY_PRIORITY, PRIMARY_PRIORITY_ON_BOOTUP, MULTIWAN_MODE";
#The Expected Wan Manager interface names
interfaceName = ["dsl0", "eth3", "veip0"];
#The Expected Wan Manager Display Names
displayName =["DSL","WANOE","GPON"];
#################################################################################
# A utility function to check if the policy is from ExpectedPolicyList
#
# Syntax       : is_policy_expected(policy, step)
# Parameter    : tdkTestObj, policy, step
# Return Value : status
#################################################################################
def is_policy_expected(tdkTestObj, policy, step):
    status = 1;
    if policy in ExpectedPolicyList :
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP %d :Check  if the policy is one from ExpectedPolicyList" %step;
        print "EXPECTED RESULT %d: policy value should be within the expected list" %step;
        print "ACTUAL RESULT %d: policy value is within the expected list" %step;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS";
        status = 0;
        return status;
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "TEST STEP %d :Check the check the policy is one from ExpectedPolicyList" %step;
        print "EXPECTED RESULT %d: policy value should be within the expected list" %step;
        print "ACTUAL RESULT %d: policy value is not within the expected list" %step;
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : FAILURE";
        return status;

#################################################################################
# A utility function to set the required policy
#
# Syntax       : set_policy(new_policy, policy_initial, tdkTestObj1, revert)
# Parameter    : new_policy, policy_initial, tdkTestObj1, revert
# Return Value : return to the invoking script
#################################################################################
def set_policy(new_policy, policy_initial, obj1, revert):
    if revert == 1 :
        if policy_initial != new_policy :
            print "Revert Operation is required";
            policy_set = policy_initial;
        else:
            print "Revert operation is not required";
            return;
    else:
        policy_set = new_policy;
    expectedresult="SUCCESS";
    #save device's current state before it goes for reboot
    obj1.saveCurrentState();
    tdkTestObj1 = obj1.createTestStep('ExecuteCmdReboot');
    query="sleep 2 && dmcli eRT setv Device.X_RDK_WanManager.Policy string \"%s\" &"%policy_set;
    print "query:%s" %query;
    tdkTestObj1.addParameter("command", query);
    #Execute the test case in DUT
    tdkTestObj1.executeTestCase(expectedresult);
    sleep(300);
    print "Set operation completed";
    #Restore previous state after reboot
    obj1.restorePreviousStateAfterReboot();
    sleep(60);
    return;

#################################################################################
# A utility function to get the policy
#
# Syntax       : get_policy(tdkTestObj, step)
# Parameter    : tdkTestObj, step
# Return Value : status, policy
#################################################################################
def get_policy(tdkTestObj, step) :
    expectedresult= "SUCCESS";
    status = 1;
    tdkTestObj.addParameter("ParamName","Device.X_RDK_WanManager.Policy");
    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    policy = details.strip().replace("\\n", "");
    if expectedresult in actualresult and policy != "":
        tdkTestObj.setResultStatus("SUCCESS");
        print "TEST STEP %d :Check the value of wanmanager policy " %step;
        print "EXPECTED RESULT %d: Should get wanmanager policy" %step;
        print "ACTUAL RESULT %d: The value received is %s" %(step, policy);
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : SUCCESS";
        status = 0;
        return status,policy;
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "TEST STEP %d :Check the value of wanmanager policy" %step;
        print "EXPECTED RESULT %d: Should get wanmanager policy" %step;
        print "ACTUAL RESULT %d: The value received is %s" %(step, policy);
        #Get the result of execution
        print "[TEST EXECUTION RESULT] : FAILURE";
        return status,policy;
