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
package com.comcast.rdk;

/**
 * Class that holds all constants for this application.
 * 
 * @author ajith, sreejasuma, praveenkp
 * 
 */
public final class Constants
{
    /**
     * Ensure that no instance of this class is created.
     */
    private Constants()
    {

    }

    public static final String ID_DEFAULT           = "1";
    public static final String KEY_ID               = "id";
    public static final String KEY_JSONRPC          = "jsonrpc";
    public static final String KEY_METHOD           = "method";
    public static final String KEY_MODULE           = "module";
    public static final String KEY_PARAMS           = "params";
    public static final String KEY_LOCATOR          = "locator";
    public static final String KEY_FREQUENCY        = "frequency";
    public static final String VAL_JSONRPC          = "2.0";
    public static final String DATE_FORMAT          = "yyyy/MM/dd HH:mm:ss";
    public static final String DATE_FORMAT1         = "yyyyMMddHHmmss";
    public static final String SEARCH_DATE_FORMAT   = "yyyy-MM-dd HH:mm:ss";
    public static final String SCHEDULE_DATEFORMAT  = "EEE MMM d HH:mm:ss z yyyy";
    public static final String STRING_QUOTES        = "\"";
    public static final String CLIENTLIST           = "<clientlist>";
    public static final String IP_ADDRESS           = "<ipaddress>";
    public static final String PORT                 = "<port>";
    public static final String LOCALFILE            = "<localfile>";
    public static final String HTML_BR              = "<br/>";
    public static final String VERSIONTRANSFER_FILE = "versiontransfer.py";
    public static final String SLASH_VERSION_TXT_FILE = "/version.txt";
    public static final String TEMP_VERSIONFILE_NAME= "Version_File.py";
    public static final String RESULT_TOKEN         = "[SCRIPTSTATUSRESULT]";
    public static final String PYTHON_EXTENSION     = ".py";
    public static final String JAVASCRIPT_EXTENSION = ".js";
    public static final String JAVASCRIPT           = "js";
    public static final String TEXT                 = "text";
    public static final String EXECUTION_LOG        = "Execution.log";
    public static final String FULLLOG_LOG          = "fullLog.log";
    public static final String TCL_EXTENSION        = ".tcl";
    public static final String FILE_STARTS_WITH     = "/script_";
    public static final String FAILURE_STATUS       = "FAILURE";
    public static final String SUCCESS_STATUS       = "SUCCESS";
    public static final String UNDEFINED_STATUS     = "UNDEFINED";
    public static final String INPROGRESS_STATUS    = "IN-PROGRESS";
    public static final String SKIPPED_STATUS    	= "SKIPPED";
    public static final String OVERALL_PASS_PERCENTAGE = "Overall Pass %";
    public static final String ABORTED_STATUS    	= "ABORTED";
    public static final String COMPLETED_STATUS    	= "COMPLETED";
    public static final String NOT_APPLICABLE_STATUS= "N/A";
    public static final String SCRIPT_TIME_OUT      = "SCRIPT TIME OUT";
    public static final String FILE_TRANSFER_SCRIPT_RDKSERVICE = "//fileStore//transfer_thunderdevice_logs.py";
    public static final String FILE_TRANSFER_SCRIPT = "//fileStore//filetransfer.py";
    public static final String FILE_UPLOAD_SCRIPT   = "//fileStore//fileupload.py";
    public static final String CONSOLE_FILE_TRANSFER_SCRIPT = "//fileStore//callConsoleLogTransfer.py";
    public static final String CONSOLE_FILE_UPLOAD_SCRIPT   = "//fileStore//callConsoleLogUpload.py";
    
    public static final String ERROR_STATUS         = "error";
    public static final String KEY_GROUP            = "Suite";
    public static final String URL_SEPERATOR        = "/";
    public static final String DOUBLE_FWD_SLASH     = "//";
    public static final String TEST_SUITE           = "TestSuite";
    public static final String SINGLE_SCRIPT        = "SingleScript";
    public static final String METHOD_TOKEN         = "configureTestCase";
    public static final String REPLACE_TOKEN        = "configureTestCase(ip,port,";
    public static final String REPLACE_BY_TOKEN     = ",ip,port,";
    public static final String LEFT_PARANTHESIS     = "(";
    public static final String RIGHT_PARANTHESIS    = ")";
    public static final String CURLY_BRACKET_OPEN   = "{";
    public static final String CURLY_BRACKET_CLOSE  = "}";
    public static final String SQUARE_BRACKET_OPEN  = "[";
    public static final String SQUARE_BRACKET_CLOSE = "]";
    public static final String KEY_GATEWAYIP        = "gatewayip";
    public static final String KEY_CHANNELTYPE      = "channeltype";
    public static final String KEY_OCAPID           = "ocapid";
    public static final String KEY_RECORDERID       = "recorderid";
    public static final String COMMA_SEPERATOR      = ",";
	public static final String SINGLE_QUOTES        = "'";
	public static final String UNDERSCORE           = "_";
	public static final String KEY_AUDIOFORMAT      = "audioformat";
	public static final String KEY_VIDEOFORMAT      = "videoformat";
	public static final String BOXTYPE_CLIENT       = "client";
	public static final String BOXTYPE_GATEWAY      = "gateway";
	public static final String BOXTYPE_STANDALONE_CLIENT  = "stand-alone-client";
	public static final int EXEC_EXITCODE_SUCCESS   = 0;
	public static final String NEW_LINE             = "\n";
	public static final String TAB					= "\t";
	public static final String LINE_STRING          = "======";
	public static final String LOG_SEPARATION_LINE_STRING = "========================";
	public static final int INDEX_ZERO              = 0;
	public static final int INDEX_ONE               = 1;
	public static final int INDEX_TWO               = 2;
	public static final int INDEX_THREE             = 3;
	public static final String KEY_ON               = "on";
	public static final String KEY_FNID             = "fnid";
	public static final String KEY_FNCHKBOX         = "fnchkbox";
	public static final String KEY_CHKBOX           = "chkbox";
	public static final String STATUS_NONE          = "none";	
	public static final String SEMI_COLON           = ";";
	public static final String COLON          		= ":";
	public static final String PERCENTAGE           = "%";
    public static final String KEY_DAILY            = "Daily";
    public static final String KEY_WEEKLY           = "Weekly";
    public static final String KEY_MONTHLY          = "Monthly";
    public static final String KEY_DAILYDAYS        = "dailyDays";
    public static final String KEY_DAILYWEEKDAY     = "dailyWeekday";
    public static final String KEY_MONTHLYDAYS      = "monthlyDays";
    public static final String KEY_MONTHLYCOMPLEX   = "monthlyComplex";
    public static final String KEY_JOB              = "Job";
    public static final String KEY_TIGGER           = "Trigger";
    public static final String KEY_RECCURENCE       = "ReccurenceSchedule";
    public static final String KEY_ONETIME          = "OnetimeSchedule";
    public static final String MULTIPLESCRIPT       = "Multiple Scripts";
    public static final String MULTIPLESCRIPTGROUPS = "Multiple Scriptgroups";
    public static final String KEY_EXISTING         = "Existing";
    public static final String KEY_EXPECT           = "expect";
    public static final String KEY_BINARYTRANSFER   = "Binaries Transferred";
    public static final String KEY_LASTDAY          = "L";
    public static final String KEY_ENTERNEW_LINE          = "\r\n";
    public static final String GREATERTHAN                = ">";
    public static final String LESSTHAN                   = "<";
    public static final String HTML_GREATERTHAN           = "&gt;";
    public static final String HTML_LESSTHAN              = "&lt;";
    public static final String HTML_REPLACEBR             = "</?br\\b[^>]*>";
    public static final String HTML_PATTERN             = "<span(.*?)</span>";
    public static final String HTML_PATTERN_AFTERSPAN   = "</?span\\b[^>]*>";
    
    public static final String PYTHON_COMMAND     = "python";
    public static final String ROOT_STRING        = "root";
    public static final String NONE_STRING        = "None";
    public static final String HYPHEN             = "-";
    public static final String XI3_BOX            = "IPClient-3"; //"Xi3";
    public static final String FOUND_MACID        = "DEVICES=";
    
	public static final String NO_DEVICES_MSG 	   = "NO_DEVICES";
	public static final String AGENT_NOT_FOUND_MSG = "AGENT_NOT_FOUND";
	public static final String FAILURE_MSG 		   = "FAILURE";
	public static final String BLANK_SPACE         = "";
	public static final String SPACE               = " ";
	public static final String GATEWAY_BOX         = "gateway";
	public static final String DEFAULT_BOX_MANUFACTURER =  "Pace";
	public static final String DEFAULT_SOCVENDOR   = "Px001bn";
    
    
    public static final int customStbPort = 10000;
    public static final	int customStatusPort = 20000;
    public static final	int customLogTransferPort = 30000;
    public static final	int customAgentMonitorPort = 40000;
    public static final String CI_EXECUTION = "CI_";
    
    public static final String THUNDER_DEFAULT_PORT = "80";
    public static final String RDKSERVICE_DEFAULT_PORT = "9998";
    
    public static final String RERUN = "_RERUN";
    public static final String MULTIPLE = "Multiple";
    
    public static final String SCRIPT_OUTPUT_FILE_PATH = "//fileStore//opFolder//";
    public static final String SCRIPT_OUTPUT_FILE_PATH_STORM = "/fileStore/opFolder/";
    public static final String SCRIPT_OUTPUT_FILE_EXTN = ".txt";
    
    public static final String TDK_ERROR = "#TDK_@error-";
    
    public static final String TRUE = "true";
    public static final String FALSE = "false";
    public static final String KEY_BENCHMARK = "BENCHMARK";
    public static final String KEY_SYSTEMDIAGNOSTICS = "SYSTEMDIAGNOSTICS";
    public static final String KEY_SCRIPTEND = "SCRIPTEND#!@~";
    public static final String PENDING = "PENDING";
    public static final String PAUSED = "PAUSED";
    public static final String SKIPPED = "SKIPPED";
    public static final String KEY_PERFORMANCE_BM = "performanceBenchMarking";
    public static final String KEY_DIAGNOSTICS = "diagnosticsTest";
    public static final String KEY_PERFORMANCE_SD ="performanceSystemDiagnostics";
    public static final String DEVICE_DIAGNOSTICS_LOG = "device_diagnostics.log";
    
    public static final String COMPONENT ="component";
    public static final String INTEGRATION ="integration";
    public static final String CERTIFICATION ="certification";
    public static final String NO_OS_SUITE = "_NO_OS";
    
    public static final String SYSTEMDIAGNOSTICS_CPU = "SYSTEMDIAGNOSTICS_CPU";
    public static final String SYSTEMDIAGNOSTICS_MEMORY = "SYSTEMDIAGNOSTICS_MEMORY";
    public static final String CPU_STARTING = "%CPU_STARTING";
    public static final String CPU_ENDING = "%CPU_ENDING";
    public static final String CPU_PEAK = "%CPU_PEAK";
    public static final String CPU_AVG = "%CPU_AVG";
    
    public static final String  MEMORY_AVAILABLE_PEAK = "%MEMORY_AVAILABLE_PEAK";
    public static final String  MEMORY_USED_PEAK = "%MEMORY_USED_PEAK";
    public static final String  MEMORY_PERC_PEAK = "%MEMORY_PERC_PEAK";
    
    public static final String  MEMORY_AVAILABLE_AVG = "%MEMORY_AVAILABLE_AVG";
    public static final String  MEMORY_USED_AVG = "%MEMORY_USED_AVG";
    public static final String  MEMORY_PERC_AVG = "%MEMORY_PERC_AVG";
    
    
    public static final String  MEMORY_AVAILABLE_START = "%MEMORY_AVAILABLE_START";
    public static final String  MEMORY_USED_START = "%MEMORY_USED_START";
    public static final String  MEMORY_PERC_START = "%MEMORY_PERC_START";
    
    public static final String  MEMORY_AVAILABLE_END = "%MEMORY_AVAILABLE_END";
    public static final String  MEMORY_USED_END = "%MEMORY_USED_END";
    public static final String  MEMORY_PERC_END = "%MEMORY_PERC_END";
    public static final int STAND_ALONE_DEVICE = 0;
    
    public static final String OS_WINDOWS = "Windows";
    public static final String OS_NAME = "os.name";
    
    public static final String FILE_SEPARATOR = System.getProperty("file.separator"); 
    
    public static final Object LOCK = new Object();
    
    public static final String SOCKET_CLIENT = "com.comcast.rdk.TclSocketExecutor";
    
    public static final String WEBPA_CLIENT = "com.comcast.rdk.WebPAClient";
    
    // classpaths to help TCL script find the necessary classes from jar files
    public static final String JAR_PATH = "WEB-INF/lib/*";
    
    public static final String CLASS_PATH = "WEB-INF/classes/";
    
    public static final String TCL_FAILED = "FAILED";
    
    public static final String STORM_FRAMEWORK_LOCATION = "storm.framework.location";
    
    public static final String STORM_TIME_OUT = "storm.time.out";
    
    public static final String TCL_FAILED_RESPONSE = "FailureReason";
    
    public static final String REQUEST_FAILED = "HTTP request failed";
    
    public static final String SERVICE_UNKNOWN = "Name or service not known";
    
    public static final String UNREACHABLE_NETWORK = "Network is unreachable";
    
    private static final int TCL_TIMEOUT = 12;
    private static final String RDKV="RDKV";
    private static final String RDKB="RDKB";
    private static final String RDKC="RDKC";
    private static final String RDKB_TCL = "RDKB_TCL";
    private static final String RDKV_THUNDER = "RDKV_THUNDER";
    private static final String RDKV_RDKSERVICE = "RDKV_RDKSERVICE";
    
    private static final String  TESTSCRIPTS_RDKV="testscriptsRDKV";
    private static final String  TESTSCRIPTS_RDKB="testscriptsRDKB"; 
    private static final String  TESTSCRIPTS_RDKC="testscriptsRDKC";
    private static final String  TESTSCRIPTS_RDKV_ADV="testscriptsRDKVAdvanced";
    private static final String  TESTSCRIPTS_RDKB_ADV="testscriptsRDKBAdvanced";
    private static final String  RDKSERVICES="rdkservices";
    private static final String  RDKV_PERFORMANCE="rdkv_performance";
    private static final String  RDKV_STABILITY="rdkv_stability";    
	private static final String  RDKV_MEDIA="rdkv_media";
	private static final String  RDKV_SECURITY="rdkv_security";
	private static final String  RDKV_PROFILING="rdkv_profiling";
	private static final String  RDKV_MEDIAVALIDATION="rdkv_mediavalidation";
	private static final String  CURRENT_FW_VERSION="currentFWVersion";
    
	private static final String SUCCESS ="SUCCESS";
	private static final String FAILED ="FAILED";
	private static final String REMARKS ="Remarks";
    private static final String STATUS ="Status";
	//for test case doc details 
	private static final String TESTCASE ="TestCase_";
	private static final String TESTCASES ="testcases";
	private static final String STORM_JSONRPC_URL = "storm.jsonrpc.url";
	private static final String STORM_TESTCASES ="Storm-Testcases";
	private static final String TESTS ="tests";
	private static final String THUNDER ="thunder";
    private static final String FILESTORE ="fileStore";
    private static final String SRC = "src";
    private static final String LOGS = "logs";
    private static final String TEST_SCRIPTS="testscripts";
    private static final String XML =".xml";
    private static final String SUITE ="suite";
    private static final String MULTIPLE_STORM ="multiple";
    private static final String EXECUTING_SCRIPT="Executing script : ";
    
    private static final String TC_ID ="Test Case ID";
    private static final String TC_OBJ ="Test Objective";
    private static final String TC_TYPE ="Test Type";
    private static final String TC_SETUP ="Supported Box Type";
    private static final String TC_SKIP="Skipped";
    private static final String TC_PRE_REQUISITES ="Test Prerequisites";
    private static final String TC_INTERFACE ="RDK Interface";
    private static final String TC_IOPARAMS ="Input Parameters";
    private static final String TC_AUTOAPROCH ="Automation Approach";
    private static final String TC_EX_OUTPUT ="Expected Output";
    private static final String TC_PRIORITY ="Priority";
    private static final String TC_TSI ="Test Stub Interface";
    private static final String TC_SCRIPT ="Test Script";
    private static final String TC_RELEASE_VERSION ="Update Release Version";
  
    private static final String T_C_ID ="testCaseId";
    private static final String T_C_OBJ ="testObjective";    
    private static final String T_C_TYPE ="testType";
    private static final String T_C_SETUP ="testSetup"; 
    private static final String T_C_SKIP="tcskip";
    private static final String T_C_PRE_REQUISITES ="preRequisites";
    private static final String T_C_INTERFACE ="interfaceUsed";
    private static final String T_C_IOPARAMS ="inputParameters";
    private static final String T_C_AUTOAPROCH ="automationApproch";
    private static final String T_C_EX_OUTPUT ="expectedOutput";
    private static final String T_C_PRIORITY ="priority";
    private static final String T_C_TSI ="testStubInterface";
    private static final String T_C_SCRIPT ="testScript";
    private static final String T_C_RELEASE_VERSION ="releaseVersion";
    private static final String T_C_REMARKS ="remarks";
    private static final String T_C_DETAILS ="testCaseDetails";
    
    
    private static final String YES ="Yes";
    private static final String NO ="No";
    private static final String HIGH ="High";
    private static final String LOW ="Low";
    private static final String MEDIUM ="Medium";
    private static final String POSITIVE ="Positive";
    private static final String NEGATIVE ="Negative";
	
	private static final String FAILURE ="FAILURE";
    private static final String STATUS_C= "STATUS";
    private static final String REMARKS_C = "REMARKS";
    
	public static final String IPV6_INTERFACE ="ipv6.interface";
    public static final String IPV4_INTERFACE ="interface";
    public static final String EXECUTION_NAME  ="ExecutionName";
    public static final String EXECUTED ="Executed";
    public static final String DEVICE_NAME= "DeviceName";
   	public static final String SCRIPT="Script";
   	public static final String SCRIPT_GROUP="ScriptGroup";
   	public static final String EXECUTION_STATUS="ExecutionStatus";
   	public static final String RESULT="Result";
   	public static final String DATE="Date";
   	public static final String DATATMAP="DataMap";
   	public static final String DETAIL_DATA_MAP ="DetailDataMap";
   	public static final String PASS_RATE= "PassRate";
   	public static final String PASS_RATE_SMALL= "passrate";
   	public static final String OVERALL_PASS_RATE= "OverallPassRate";
   	public static final String LOG_UPLOAD_IPV4= "log.upload.ipv4"; 
   	public static final String LOG_UPLOAD_IPV6= "log.upload.ipv6"; 
   	public static final String REST_AUTH_ENABLED = "rest.authentication.enabled";
   	public static final String TM_CONFIG_FILE= "/fileStore/tm.config";
   	public static final String STORM_CONFIG_FILE= "/fileStore/storm.config";
   	public static final String STORM_DEFAULT_TIME_OUT= "2";
   	public static final String STORM_TESTS_TIME_OUT_CONFIG_FILE= "/fileStore/storm_tests_time_out.config";
	public static final String TFTP_MECHANISM= "tftp";
	public static final String REST_MECHANISM= "REST";
	public static final String FILE_NOT_FOUND= "File not found.";
	public static final String DEFAULT    = "Default";
	public static final String NO_LOGS    = "No logs available.";
	public static final String TDKB_DEVICE_CONFIG    = "tdkbDeviceConfig";
	public static final String PY_DEVICE_CONFIG  	 = "PythonE2E";
	public static final String TCL_DEVICE_CONFIG     = "TCLE2E";
	public static final String TXT_EXTN     = ".txt";
	public static final String CONFIG_EXTN     = ".config";
	public static final String EXPORT_ZIP_FORMAT 			= "zip";
	public static final String EXPORT_EXCEL_EXTENSION 		= "xls";
	public static final String EXPORT_ZIP_EXTENSION 		= "zip";
	
	public static final String ALL_LOGS ="ALL";
	public static final String FAILURE_LOGS ="FAILURE";
	
	public static final String SCRIPT_ISSUE = "Script Issue";
	public static final String ENVIRONMENT_ISSUE = "Environment Issue";
	public static final String RDK_ISSUE = "RDK Issue";
	public static final String INTERFACE_CHANGE = "Interface Change";
	public static final String NEW_ISSUE = "New Issue";
	public static final String ANALYZED = "analyzed";
	
	public static final String TOTAL_ANALYZED_DATA = "totalAnalyzedData";
	public static final String MODULE_DATA = "moduleData";
	public static final String DEFECT_DATA = "defectData";
	
	public static final String GRAFANA_DATA = "GrafanaData";
	public static final String PROFILING_SYSTEM = "PROFILING_SYSTEM_";
	public static final String PROFILING_PROCESSES = "PROFILING_";
	public static final String PROFILING_THRESHOLD = "_THRESHOLD";
}
