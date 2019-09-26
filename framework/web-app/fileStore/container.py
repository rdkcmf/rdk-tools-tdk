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

#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import tdklib;

def CheckProcessTree(obj, expectedState, psList):
	status = False;
        tdkTestObj = obj.createTestStep('ExecuteCommand');
        expectedResult="SUCCESS";
	
	cmd = "pstree | grep -o"; 

	for ps in psList:
		cmd += " -e " + ps ;
				
	cmd += " | tr \'\n\' \' \'";
	print cmd;
	
	#configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
	print "Exceution result: ", actualResult;
	
	if expectedResult in actualResult:
		details = tdkTestObj.getResultDetails();
		print "Output: ", details;
		for ps in psList:
			if ps not in details:
				if expectedState:
	                                tdkTestObj.setResultStatus("FAILURE");
        	                else:
                	                tdkTestObj.setResultStatus("SUCCESS");
                        	print "Containerization is not enabled";
				return status;

		if expectedState:
                	tdkTestObj.setResultStatus("SUCCESS");
                else:
                	tdkTestObj.setResultStatus("FAILURE");
		print "Containerization is enabled";
		status = True;
	else:
		tdkTestObj.setResultStatus("FAILURE");
		print "Command execution failed";
	return status;


def CheckContainerState(obj, containerName, expectedState):
	status = False;
        tdkTestObj = obj.createTestStep('ExecuteCommand');
        expectedResult="SUCCESS";
	
	cmd = "lxc-info -n " + containerName + " | grep State";
	
	#configure the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
	print "Exceution result: ", actualResult;
	
	if expectedResult in actualResult:
		details = tdkTestObj.getResultDetails();
		print "Output: ", details;
		if "RUNNING" in details:
			if expectedState:
				tdkTestObj.setResultStatus("SUCCESS");
			else:
				tdkTestObj.setResultStatus("FAILURE");
			print "%s Container is running" %containerName;
			status = True;
		else:
			if expectedState:
				tdkTestObj.setResultStatus("FAILURE");
			else:
				tdkTestObj.setResultStatus("SUCCESS");
			print "%s Container is not running" %containerName;
	else:
		tdkTestObj.setResultStatus("FAILURE");
		print "Command execution failed";
	return status;

def FindPatternFromFile(obj, fileName, field, pattern):
	status = False;
	value = "";
        tdkTestObj = obj.createTestStep('ExecuteCommand');
        expectedResult="SUCCESS";
	if field == "":
		cmd = "cat " + fileName + " | grep -o " + pattern;
	else:
		cmd = "cat " + fileName + " | grep " + field + " | tr \'\n\' \' \'";
	print cmd;
	
	#configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
	print "Exceution result: ", actualResult;
	
	if expectedResult in actualResult:
		details = tdkTestObj.getResultDetails();
		print "Output: ", details;
		if pattern == "":
			value = details.replace(field.strip("\""), '').strip("\\n");
			tdkTestObj.setResultStatus("SUCCESS");
			print value;
		else:
			pattern = pattern.replace("\*", "*");
			if pattern.strip("\"") in details:
				print "%s Pattern Found" %pattern;
				tdkTestObj.setResultStatus("SUCCESS");
				status = True;
			else:
				print "%s Pattern not Found" %pattern;
				tdkTestObj.setResultStatus("FAILURE");
	else:
		tdkTestObj.setResultStatus("FAILURE");
		print "Command execution failed";
	return (status, value);

def GetFilePermission(obj, fileName):
        status = False;
        tdkTestObj = obj.createTestStep('ExecuteCommand');
        expectedResult="SUCCESS";

        cmd = "stat -c \"%a %n\" "  + fileName + "| cut -d \" \" -f 1";
	print cmd;

        #configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                print "Output: ", details;
		permissionValue = details.strip('\\n');
                if  permissionValue == "770":
                        tdkTestObj.setResultStatus("SUCCESS");
			print "Permission satisfied for ", fileName;
                        status = True;
                else:
                        tdkTestObj.setResultStatus("FAILURE");
			print "Permission not satisfied for ", fileName;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Command execution failed";
        return status;

def GetOwnership(obj, fileName, owner, field):
        status = False;
	result = True;
        tdkTestObj = obj.createTestStep('ExecuteCommand');
        expectedResult="SUCCESS";

        cmd = "ls -al "  + fileName + " |  tr -s \" \" | cut -d \" \" -f " +field + " | tr \'\\n\' \',\'";
        print cmd;

        #configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                print "Output: ", details;
		output = details.split(',');
		for item in output:
			if owner not in item:
				print "Expected user owner for files in %s is %s, but recieved %s" %(fileName, owner, item); 
				result = False;	
		
                if result:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "User ownership as expected for ", fileName;
                        status = True;
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "User ownership not as expected for ", fileName;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Command execution failed";
        return status;

def StopContainer(obj, containerName):
        status = False;
        tdkTestObj = obj.createTestStep('ExecuteCommand');
        expectedResult="SUCCESS";

        cmd = "lxc-stop -n " + containerName + "&";
        print cmd;

        #configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
        	tdkTestObj.setResultStatus("SUCCESS");
                print "Container %s stopped" %containerName;
                status = True;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Command execution failed";
        return status;

def StartContainer(obj, filePath):
        status = False;
        tdkTestObj = obj.createTestStep('ExecuteCommand');
        expectedResult="SUCCESS";

        cmd = filePath + " > /tmp/start_status.log &"
        print cmd;

        #configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "Containers started";
                status = True;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Command execution failed";
        return status;



def AccessContainerShell(obj, containerName, expProcess, output):
        status = False;
        tdkTestObj = obj.createTestStep('ExecuteCommand');
        expectedResult="SUCCESS";

        cmd = "lxc-attach -n " + containerName + " -- ps | grep " + expProcess;
	print cmd;

        #configure the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                print "Output: ", details;

                if expProcess in details:
			if output:
                        	tdkTestObj.setResultStatus("SUCCESS");
			else:
                        	tdkTestObj.setResultStatus("FAILURE");
                        print "Accessed %s Container shell" %containerName;
                        status = True;
                else:
			cmd = "lxc-attach -n " + containerName + " -- ps -ef | grep " + expProcess;
			print cmd;
		 	#configure the command
			tdkTestObj.addParameter("command", cmd);
			tdkTestObj.executeTestCase(expectedResult);

			actualResult = tdkTestObj.getResult();
			print "Exceution result: ", actualResult;

			if expectedResult in actualResult:
				details = tdkTestObj.getResultDetails();
				print "Output: ", details;
				if expProcess in details:
					if output:
		                                tdkTestObj.setResultStatus("SUCCESS");
                		        else:
                                		tdkTestObj.setResultStatus("FAILURE");
                        		print "Accessed %s Container shell" %containerName;
                        		status = True;
				else:
					if output:
                		        	tdkTestObj.setResultStatus("FAILURE");
					else:
                        			tdkTestObj.setResultStatus("SUCCESS");
                        		print "%s Container shell not accessible" %containerName;
			else:
				tdkTestObj.setResultStatus("FAILURE");
		                print "Command execution failed";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Command execution failed";
        return status;

def UpdateFile(obj, command, fileName):
	status = False;
	tdkTestObj = obj.createTestStep('ExecuteCommand');
	expectedResult="SUCCESS";

	cmd = command + " " + fileName;
	print cmd;

	#configre the command
	tdkTestObj.addParameter("command", cmd);
	tdkTestObj.executeTestCase(expectedResult);

	actualResult = tdkTestObj.getResult();
	print "Exceution result: ", actualResult;

	if expectedResult in actualResult:
		tdkTestObj.setResultStatus("SUCCESS");
		print ("Command execution success");
		status = True;
	else:
		tdkTestObj.setResultStatus("FAILURE");
		print ("Command execution failed");
	return status;


def checkOrderCreation(obj, orderList):
        for index, item in enumerate(orderList):
                if item == "dbus--block":
                        orderList[index] = "dbus";
        tdkTestObj = obj.createTestStep('ExecuteCommand');
        expectedResult="SUCCESS";

        cmd = "cat \'/tmp/start_status.log\' | grep \'Name\' | tr -s \' \' | cut -d \' \' -f 2 | tr \'\n\' \' \'";
        print cmd;

        #configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                print "Output: ", details;
                containerList = details.strip('\\n').split();
                print "Expected container creation order", orderList;
                print "Actual container creation order", containerList;
                if containerList == orderList:
                         tdkTestObj.setResultStatus("SUCCESS");
                         print ("Container creation order is correct");
                else:
                         tdkTestObj.setResultStatus("FAILURE");
                         print ("Container creation order is wrong");
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Command execution failed";

def GetProcessList(obj, containerName, inside):
        processList = [];
        tdkTestObj = obj.createTestStep('ExecuteCommand');
        expectedResult="SUCCESS";

        if inside:
                field = "5";
                cmd = "lxc-attach -n " + containerName + " -- ps";
        else:
                field = "4";
                cmd = "ps -G " + containerName;

        cmd = cmd + "| tr -s \' \'| sed 's/^[ ]*//' | cut -d \' \' -f " + field + " | tr \'\n\' \' \'";
        print cmd;

        #configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                print "Output: ", details;
                processList = details.split();
                print processList;
                removeList1 = ['CMD', 'COMMAND', 'ps', '/bin/sh'];
                removeList2 = '[]{}';
                for item in removeList1:
                        if item in processList:
                                processList.remove(item);

                for i in removeList2:
                        for index, item in enumerate(processList):
                                if i in item:
                                        processList[index] = item.strip(i);

                for index, item in enumerate(processList):
                	if '/usr/bin/' in item:
                        	processList[index] = item.replace('/usr/bin/', '');

                tdkTestObj.setResultStatus("SUCCESS");
                print "Command execution success";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Command execution failed";
        return (tdkTestObj, processList);

def GetFileList(obj, containerName, folderPath, expFileList):
        fileList = [];
        tdkTestObj = obj.createTestStep('ExecuteCommand');
        expectedResult="SUCCESS";

        cmd = "lxc-attach -n " + containerName + " -- ls " + folderPath + " | tr \'\n\' \' \'";
        print cmd;

        #configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                print "Output: ", details;
                fileList = details.split();
                print fileList;
                print expFileList;
                #fileList = fileList.sort()
                #expFileList = expFileList.sort();
                if set(fileList) >= set(expFileList):
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "%s Contents are coherent" %folderPath;
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "%s Contents are not coherent" %folderPath;

        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Command execution failed";
        return;

def CheckFileExists(obj, folderPath, fileName):
        fileList = [];
	status = False;
        tdkTestObj = obj.createTestStep('ExecuteCommand');
        expectedResult="SUCCESS";

        cmd = "ls " + folderPath + " | tr \'\n\' \' \'";
        print cmd;

        #configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                print "Output: ", details;
                fileList = details.split();
                print fileList;
		if fileName in fileList:
			status = True;
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "File exists";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "File does not exist";

        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Command execution failed";
        return status;

