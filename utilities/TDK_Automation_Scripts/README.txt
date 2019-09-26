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
Prerequisite :
---------------
	1) TDK enabled RDK Image should be flashed in STB.
	2) TDK binaries and libraries should be flashed in STB.
	3) List of packages need to be installed before running automation scripts.
		1. python-MySQLdb: For Performing read and write operation in database using python script.
		2. python-matplotlib: For plotting functional(PieChart) and performance statistics of different components using python script.
		3. python-pip: To install 'xlutils' python library
		4. xlutils: Installing xlutils will install 'xlrd' and 'xlwt'. To perform read and write operations in excel sheet using python.
	4) User should have write permissions to "Test tool folder in webapps folder of apache setup (For collecting test logs)".
	5) Agent should be up and running in configured STB ( configured TARGET_IP) and loaded with all required stubs and tests.
		
Steps to run TDK automation scripts:
-----------------------------------------

1) TDK Automation scripts organization (Folder structure) :
	Test Automation scripts - @...../twc_automation
	Python libraries 	- @...../python-lib
        Customized tests scripts- @...../tests
        (Component Customized tests scripts are generated from Original tests scripts in the Test Manager web applcation file store)

2) Configure Environment part of "TdkConfig.xml", as per the present Test Environment.
	2.1) Test Environment Configuration:
	   -------------------------------
		TARGET_IP - STB/Target IP address, where the tests need to be executed
		BUILD_VER - RDK build version in  STB (Test results will be updated for this build version in Reports)
		TEST_MANAGER_URL - Host machine Test manager URL
		LOG_PATH - Configure corresponding webapps path of rdk test tool. 
			  (Logs will be transfered to this location with corresponding Execution IDs)
		DEV_NAME  - STB device name
		RESRC_PUBLISHER_LINK - URL in which all the test resource files are hosted. (Optional parameter, it is necessary if /var/tdk/tdk.conf is not defined in STB)

		Example configuration :
		------------------------
			<TestEnvironment>
			<TARGET_IP>10.143.32.85</TARGET_IP>
			<BUILD_VER>Release-1.36.0</BUILD_VER>
			<TEST_MANAGER_URL>http://10.143.32.70:8080/rdk-test-tool_M25</TEST_MANAGER_URL>
			<RESRC_PUBLISHER_LINK>http://192.168.0.40:8080/</RESRC_PUBLISHER_LINK>
			<LOG_PATH>/home/rdktest/apache-tomcat-6.0.39/webapps/rdk-test-tool_M25/</LOG_PATH>
			<!-- LOG_PATH : Path where logs will be stored -->
			<COMMON_XML_LOGS_PATH enabled="true">./TDKLOGS</COMMON_XML_LOGS_PATH>	
			<!-- COMMON_XML_LOGS_PATH : All xml logs will be copied (**duplicated**) to this COMMON_XML_LOGS_PATH -->
			<DEV_NAME>HUMAX_IPSTB0</DEV_NAME>
			<PORT_ID>8087</PORT_ID>
			</TestEnvironment>

	2.2) Test Suite Configuration:
	   --------------------------
		Enable the tests, which need to be executed using the configuration flags in the component tag of TdkConfig.xml.
		TestExecutionEnabled - true/false to enable/Disable Tests execution for the component respectively.
		ReportGenerationEnabled  - true/false to enable/Disable Tests execution for the component respectively.
		Test_Schedule - true/false to enable/disable Tests execution for the component respectively. If Test_Schedule is true then user has to give time for scheduling test cases in below format.
								dd-mm-yyyy HH:MM:SS - (24hr format)
		Other parameters like TestScripts location, ScriptName and  SharedObjectName can be configured based on requirement (if any change in environment).
			
		<TestSuite name="RDKLogger"  component="RDKLogger" testtype="functional">
			<Test_Schedule>false</Test_Schedule>
            <!-- Time in (dd-mm-yyyy HH:MM:SS - <24hr format>) format  -->
			<Time>13-07-2015 14:15:15</Time>
			<TestExecutionEnabled>true</TestExecutionEnabled>
			<ReportGenerationEnabled>true</ReportGenerationEnabled>
			<TestCaseReportName>RDKLoggerTestCaseReport</TestCaseReportName>
			<TestScripts location="../tests/RDKLogger/scripts/" runall="false" >
				 <ScriptName>twc_RDKLogger_CheckMPELogEnabled</ScriptName>
				 <ScriptName>twc_RDKLogger_Dbg_Enabled_Status</ScriptName>
			</TestScripts>
			<SharedObjectName>rdklogger</SharedObjectName>
			<Feature name="RDKLogger"/>
		</TestSuite>

3) Run the tests by executing "TdkTestExecuter.py" script present in "twc_automation" folder by using below command.
	********************************************************
	python TdkTestExecuter.py TdkConfig.xml <STB_IP_ADDRESS>
	********************************************************	
	NOTE:	STB_IP_ADDRESS is an optional argument. If not given it will take TARGET_IP from TdkConfig.xml and proceed test execution.

	On successful execution :
	- Test result XML logs will be updated in COMMON_XML_LOGS_PATH ("./TDKLOGS") configured as per Test Environment.
	- STB logs will be updated in configured COMMON_XML_LOGS_PATH("./TDKLOGS/<COMPONENT_NAME>/AgentConsoleLogs/") configured as per Test Environment.
	- Test execution logs will be updated in configured LOG_PATH inside a directory named as ExecutionId ("/home/rdktest/apache-tomcat-6.0.39/webapps/rdk-test-tool_M25/logs/2554"). Here 2554 is the ExecutionId
	- Test manager UI will be updated with test execution details.

4) There are different internal calls in TdkTestExecuter.py
	Report Generation in XLS format. (XLS report with result of different build versions)
	Plot Graph of funtional test cases statistics for different components.(PieChart)
	Plot Graph of performance test cases for WEBKIT and GSTREAMER.(Display different readings of test cases from successive build versions)
	-----------------------------------------
	4.1)	If ReportGenerationEnabled flag is true a test case report will generate in XLS format from XML logs after complete execution of component. Below is the command used for generation of report:
	
		*******************************************************************************************************************************************
		python generateXLSfile.py <XML_LOG_PATH> <RELEVANCE_NUMBER> <TEST_SUITE_EXECUTION_TIME> <TDK_CONFIG_FILE> <TEST_REPORT_NAME>
		*******************************************************************************************************************************************
		The XLS report will get generated in current directory (twc_automation/)
		
	4.2)	Once the test case report in XLS format is generated it will generate a graph(Pie Chart) for functional test case execution to display the test statistics for different component. Below is the command used for generation of fucntional plot:
	
		***************************************************************************
		python plotPieChart.py <TEST_REPORT_NAME> <TEST_SUMMARY_SHEET_NAME>
		***************************************************************************		
		The PieChart for test cases will get generated in directory "./TDK_FunctionalGraph/<COMPONENT_NAME>__FunctionalTestsGraph/"
		 
	4.3)	Once the test case report in XLS format is generated it will generate a graph of performance test case execution to display the performance data of successive build versions for WEBKIT and GSTREAMER. Below is the command used for generation of performance plot:
	
		*********************************************************************************************************
		python plotGraph.py <PLOT_CONFIG_FILE> <TEST_SUITE_NAME> <TEST_REPORT_NAME> <TEST_SHEET_NAME>
		*********************************************************************************************************		
	a) Configure plotConfig.xml for groupPlot and plot flag as shown below:
		<TestGroupName name="HTMLPageLoad" groupPlot="true">
			<TestFunctionName plot="true">htmlPerfLoadLocalPageTime</TestFunctionName>
			<TestFunctionName plot="true">htmlPerfLoadInternetPageTime</TestFunctionName>
			<TestFunctionName plot="true">htmlPerfReloadLocalPageTime</TestFunctionName>
			<TestFunctionName plot="true">htmlPerfReloadInternetPageTime</TestFunctionName>
		</TestGroupName>	

	b) This will plot graph for each test group and test function present in plotConfig.xml file from Build/Release version mentioned in plotConfig.xml for different components. 
		(i)	If 'groupPlot' flag is true it will plot a single graph for all the test functions within that group having 'plot' flag as true with file name as group name.
		(ii)	If 'groupPlot' flag is false and 'plot' flag is true for test function then it will plot graph for individual test functions with file name as test function name.
		
	The graph for performance test cases will get generated in directory "./TDK_PerformanceGraph/<COMPONENT_NAME>_Graph/"

	4.4) Once the test case execution is completed and XML logs are generated, the script SWORD_Runner.py will push XML logs to SWORD system apply the flag "status" of tag 'SWORD_EnvironmentDetails' should set to "true" in TdkConfig.xml file. 
	For Example:	
			<SWORD_EnvironmentDetails status="false">
				<Test_Plan_Result_Id>70520</Test_Plan_Result_Id>
				<IP_Address>10.70.128.28</IP_Address>
				<PORT>80</PORT>
				<Authentication_Token>yeF8nQ1whH1guM48uNc7</Authentication_Token>
				<Test_Cycle_Id>7083</Test_Cycle_Id>
				<Product_Id>1329</Product_Id>
				<Hardware_Unit_Id>5074</Hardware_Unit_Id>
				<RelevanceNumber>1</RelevanceNumber>
				<Overwrite_Existing_Results_TF>0</Overwrite_Existing_Results_TF>
				<End_of_Job_URL>/automated_test_reporter</End_of_Job_URL>
			</SWORD_EnvironmentDetails>
	
		Below is the command used for pushing XML logs to SWORD system:
		**************************************************************************************
		python SWORD_Runner.py <SERVER_IP_ADDRESS> <TDK_LOG_PATH> <TDK_CONFIG_FILE>
		**************************************************************************************		

