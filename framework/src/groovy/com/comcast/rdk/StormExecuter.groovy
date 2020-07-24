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
package com.comcast.rdk
import java.io.FileWriter;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.File;

import static com.comcast.rdk.Constants.*
import org.apache.shiro.SecurityUtils
import org.codehaus.groovy.grails.web.json.JSONObject
import org.junit.After;
import grails.converters.JSON

import java.io.FileInputStream;
import java.io.InputStream;
import java.text.SimpleDateFormat;
import java.util.List;
import java.util.Properties;
import java.util.concurrent.FutureTask
import java.util.regex.Matcher
import java.util.regex.Pattern
import com.google.gson.JsonObject
import java.nio.charset.StandardCharsets;

class StormExecuter {
	
	/**
	 * Method to execute a thunder script
	 * @param application
	 * @param scriptname
	 * @param stbIp
	 * @param executionId
	 */
	public static void executeThunderScript(def application, String scriptname, String stbIp, String executionId){
		try
		{
			if(!isNodeAvailable()){
				startNode(application)
			}
			File configFile = application.parentContext.getResource(Constants.STORM_CONFIG_FILE).file
			String STORM_JSONRPC_URL = getConfigProperty(configFile, Constants.STORM_JSONRPC_URL)
			URL url = new URL(STORM_JSONRPC_URL);
			URLConnection con = url.openConnection();
			HttpURLConnection http = (HttpURLConnection)con;
			http.setRequestMethod("POST");
			http.setDoOutput(true);	
			String deviceIP = stbIp
			String execId = executionId
			String fullScriptName = scriptname + ".js"
			String jsonStr = "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"execute_testcase\",\"params\":{\"test\":\""+fullScriptName+"\",\"execid\":\""+execId+"\",\"device\":{\"host\":\""+deviceIP+"\"}}}"
			byte[] out = jsonStr.getBytes(StandardCharsets.UTF_8);
			int length = out.length;
			http.setFixedLengthStreamingMode(length);
			http.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
			http.setRequestProperty("Accept", "application/json");
			con.getOutputStream().write(out);
			http.connect();
			InputStream iStream = new BufferedInputStream(con.getInputStream());
				String result = org.apache.commons.io.IOUtils.toString(iStream, "UTF-8");
				JSONObject jsonObject = new JSONObject(result);
				iStream.close();
		}
		catch(Exception e){
			e.printStackTrace();
		}
	}	
	
	/**
	 * Method to parse thunder test result
	 * @param grailsApplication
	 * @param scriptname
	 * @param executionId
	 * @return
	 */
	public static boolean parseThunderResult(def grailsApplication, String scriptname,String executionId){
		boolean resultThunder = false
		File configFile = grailsApplication.parentContext.getResource(Constants.STORM_CONFIG_FILE).file
		String STORM_FRAMEWORK_LOCATION = getConfigProperty(configFile, Constants.STORM_FRAMEWORK_LOCATION) + Constants.URL_SEPERATOR
		String STORM_FRAMEWORK_LOG_LOCATION = STORM_FRAMEWORK_LOCATION+Constants.SRC+File.separator+Constants.LOGS+File.separator
		String LOG_FILE = STORM_FRAMEWORK_LOG_LOCATION+scriptname+Constants.JAVASCRIPT_EXTENSION+Constants.UNDERSCORE+executionId+Constants.UNDERSCORE+Constants.EXECUTION_LOG
		File log_file = new File(LOG_FILE)
		String osName = System.getProperty(Constants.OS_NAME)
		BufferedReader reader
		try{
		    if(osName?.startsWith(Constants.OS_WINDOWS)){
				if(log_file.exists()){
					reader = new BufferedReader(new FileReader(LOG_FILE));
				}
				String line = reader?.readLine();
				while(line != null){
					if(line.contains("Success")){
						resultThunder = true
						break
					}
					line = reader?.readLine()
				}
				reader?.close()
				
		    }else{
			    if(log_file.exists()){
				    reader = new BufferedReader(new FileReader(LOG_FILE));
			    }
			    String line = reader?.readLine();
			    while(line != null){
					if(line.contains("Success")){
						line = reader?.readLine()
						if(line?.contains("finished running")){
							resultThunder = true
							break
						}
					}
				    line = reader?.readLine()
			    }
				reader?.close()
		    }

		}
		catch(Exception e){
			e.printStackTrace()
		}
		return resultThunder
	}
	
	/**
	 * Method to check if a thunder execution has finished running or not
	 * @param grailsApplication
	 * @param scriptname
	 * @param executionId
	 * @return
	 */
	public static boolean checkThunderExecution(def grailsApplication, String scriptname,String executionId){
		boolean resultThunder = false
		File configFile = grailsApplication.parentContext.getResource(Constants.STORM_CONFIG_FILE).file
		String STORM_FRAMEWORK_LOCATION = getConfigProperty(configFile, Constants.STORM_FRAMEWORK_LOCATION) + Constants.URL_SEPERATOR
		String STORM_FRAMEWORK_LOG_LOCATION = STORM_FRAMEWORK_LOCATION+Constants.SRC+File.separator+Constants.LOGS+File.separator
		String LOG_FILE = STORM_FRAMEWORK_LOG_LOCATION+scriptname+Constants.JAVASCRIPT_EXTENSION+Constants.UNDERSCORE+executionId+Constants.UNDERSCORE+Constants.EXECUTION_LOG
		File log_file = new File(LOG_FILE)
		String osName = System.getProperty(Constants.OS_NAME)
		BufferedReader reader
		try{
			if(osName?.startsWith(Constants.OS_WINDOWS)){
				if(log_file.exists()){
					reader = new BufferedReader(new FileReader(LOG_FILE));
				}
				String line = reader?.readLine();
				while(line != null){
					if(line.contains("finished running")){
						resultThunder = true
						break
					}
					line = reader?.readLine()
				}
				reader?.close()
				
			}else{
				if(log_file.exists()){
					reader = new BufferedReader(new FileReader(LOG_FILE));
				}
				String line = reader?.readLine();
				while(line != null){
					if(line.contains("finished running")){
						resultThunder = true
						break
					}
					line = reader?.readLine()
				}
				reader?.close()
			}

		}
		catch(Exception e){
			e.printStackTrace()
		}
		return resultThunder
	}

	/**
	 * Method to return thunder log file
	 * @param grailsApplication
	 * @param scriptname
	 * @param executionId
	 * @return
	 */	
	static String returnThunderLogFile(def grailsApplication, String scriptname,String executionId){
		File configFile = grailsApplication.parentContext.getResource(Constants.STORM_CONFIG_FILE).file
		String STORM_FRAMEWORK_LOCATION = getConfigProperty(configFile, Constants.STORM_FRAMEWORK_LOCATION) + Constants.URL_SEPERATOR
		String STORM_FRAMEWORK_LOCATION_LOG_LOCATION_WINDOWS = STORM_FRAMEWORK_LOCATION+"src\\logs\\"
		String STORM_FRAMEWORK_LOCATION_LOG_LOCATION_LINUX = STORM_FRAMEWORK_LOCATION+"src/logs/"
		String LOG_FILE_LINUX_GRAILS = STORM_FRAMEWORK_LOCATION_LOG_LOCATION_LINUX+scriptname+".js_"+executionId+"_Execution.log"
		String LOG_FILE_WINDOWS_GRAILS = STORM_FRAMEWORK_LOCATION_LOG_LOCATION_WINDOWS+scriptname+".js_"+executionId+"_Execution.log"
		File log_file_linux = new File(LOG_FILE_LINUX_GRAILS)
		File log_file_windows = new File(LOG_FILE_WINDOWS_GRAILS)
		String htmlData = ""
		BufferedReader reader
		String osName = System.getProperty(Constants.OS_NAME)
		try{
			if(osName?.startsWith(Constants.OS_WINDOWS)){
				if(log_file_windows.exists()){
					reader = new BufferedReader(new FileReader(LOG_FILE_WINDOWS_GRAILS));
				}
				String line = reader?.readLine();
				while(line != null){
					htmlData = htmlData+ HTML_BR + line
					line = reader?.readLine()
				}
				reader?.close()
			}else{
			    if(log_file_linux.exists()){
				    reader = new BufferedReader(new FileReader(LOG_FILE_LINUX_GRAILS));
			    }
			    String line = reader?.readLine();
			    while(line != null){
					htmlData = htmlData + line + HTML_BR
				    line = reader?.readLine()
			    }
			    reader?.close()
		    }
		}catch(Exception e){
		    e.printStackTrace()
		}
		return htmlData
	}
	
	/**
	 * Method which writes server console log file for thunder executions
	 * @param grailsApplication
	 * @param realPath
	 * @param executionId
	 * @param executionDeviceId
	 * @param executionResultId
	 * @param scriptname
	 * @param executionName
	 * @return
	 */
	def static boolean writeServerConsoleLogFileData(def grailsApplication, def realPath, def executionId, def executionDeviceId, def executionResultId, String scriptname, def executionName){
		BufferedReader reader
		String serverlogData = ""
		File configFile = grailsApplication.parentContext.getResource(Constants.STORM_CONFIG_FILE).file
		String STORM_FRAMEWORK_LOCATION = getConfigProperty(configFile, Constants.STORM_FRAMEWORK_LOCATION) + Constants.URL_SEPERATOR
		String STORM_FRAMEWORK_LOCATION_LOG_LOCATION_WINDOWS = STORM_FRAMEWORK_LOCATION+"src\\logs\\"
		String STORM_FRAMEWORK_LOCATION_LOG_LOCATION_LINUX = STORM_FRAMEWORK_LOCATION+"src/logs/"
		String SERVER_CONSOLE_LOG_FILE_LINUX_GRAILS = STORM_FRAMEWORK_LOCATION_LOG_LOCATION_LINUX+scriptname+".js_"+executionName+"_Serverconsole.log"
		String SERVER_CONSOLE_LOG_FILE_WINDOWS_GRAILS = STORM_FRAMEWORK_LOCATION_LOG_LOCATION_WINDOWS+scriptname+".js_"+executionName+"_Serverconsole.log"
		File server_console_log_file_linux = new File(SERVER_CONSOLE_LOG_FILE_LINUX_GRAILS)
		File server_console_log_file_windows = new File(SERVER_CONSOLE_LOG_FILE_WINDOWS_GRAILS)
		String osName = System.getProperty(Constants.OS_NAME)
        if(osName?.startsWith(Constants.OS_WINDOWS)){
			try{
				if(server_console_log_file_windows.exists()){
					reader = new BufferedReader(new FileReader(SERVER_CONSOLE_LOG_FILE_WINDOWS_GRAILS));
				}
				String line = reader?.readLine();
				while(line != null){
					serverlogData = serverlogData+line+"\n"
					line = reader?.readLine()
				}
				reader?.close()
			}catch(Exception e){
			    e.printStackTrace()
			}
		}else{
		    try{
				if(server_console_log_file_linux.exists()){
					reader = new BufferedReader(new FileReader(SERVER_CONSOLE_LOG_FILE_LINUX_GRAILS));
				}
				String line = reader?.readLine();
				while(line != null){
					serverlogData = serverlogData+line+"\n"
					line = reader?.readLine()
				}
				reader?.close()
            }catch(Exception e){
			    e.printStackTrace()
	        }
		}
		String folderPath = realPath+File.separator+"logs"
		String consoleLogPath = folderPath+File.separator+"consolelog"
		File consoleLogPathDir = new File(consoleLogPath)
		if(!consoleLogPathDir.exists()){
			consoleLogPathDir.mkdir()
		}
		String executionInstanceDirPath = consoleLogPath+File.separator+executionId
		boolean serverConsoleLogFilecreationSuccess = false
		File executionInstanceDir = new File(executionInstanceDirPath)
		if(!executionInstanceDir.exists()){
			executionInstanceDir.mkdir()
		}
			String executionDeviceInstanceDirPath = executionInstanceDirPath+File.separator+executionDeviceId
			File executionDeviceInstanceDir = new File(executionDeviceInstanceDirPath)
			if(!executionDeviceInstanceDir.exists()){
				executionDeviceInstanceDir.mkdir()
			}
					String executionResultInstanceDirPath = executionDeviceInstanceDirPath+File.separator+executionResultId
					File executionResultInstanceDir = new File(executionResultInstanceDirPath)
					if(!executionResultInstanceDir.exists()){
						executionResultInstanceDir.mkdir()
					}
						String serverConsoleLogFileName = "ServerConsoleLog.txt"
						String serverConsoleLogFileAbsolutePath = executionResultInstanceDirPath +File.separator+serverConsoleLogFileName
						File serverConsoleLogFile = new File(serverConsoleLogFileAbsolutePath)
						if(serverConsoleLogFile.createNewFile()){
							FileWriter fr = new FileWriter(serverConsoleLogFile)
							fr.write(serverlogData)
							fr.close()
							serverConsoleLogFilecreationSuccess = true
						}
					
		return serverConsoleLogFilecreationSuccess
	}
	
	/**
	 * Method which checks whether a node server is running or not
	 * @return
	 */
	static boolean isNodeAvailable () {
		boolean isFound = false;
		try {
			String line;
			Process p;
			ProcessBuilder pb;
			String command = "ps -ef"
			pb = new ProcessBuilder("bash", "-c", command)
			p = pb.start()
			BufferedReader input = new BufferedReader(new InputStreamReader(p.getInputStream()));
			while ((line = input.readLine()) != null) {
				if(line.contains("node") && line.contains("storm_jsonrpc")){
					isFound = true;
					break;
				}
			}
			input.close();
		} catch (Exception err) {
			err.printStackTrace();
		}
		return isFound;
	}
	
	/**
	 * Method which will start a node server if it is not available
	 * @param application
	 * @return
	 */
	def static boolean startNode (def application) {
		boolean nodeInitialized
		if( !(isNodeAvailable())){
			nodeInitialized = initializeNodeServer(application)
		}
		return nodeInitialized
	}

	/**
	 * Method to initialize a node server
	 * @param application
	 * @return
	 */
	def static boolean initializeNodeServer (def application) {
		File configFile = application.parentContext.getResource(Constants.STORM_CONFIG_FILE).file
		String STORM_FRAMEWORK_LOCATION = getConfigProperty(configFile, Constants.STORM_FRAMEWORK_LOCATION) + Constants.URL_SEPERATOR
		String STORM_FRAMEWORK_LOCATION_SRC_WINDOWS = STORM_FRAMEWORK_LOCATION+"src\\"
		String STORM_FRAMEWORK_LOCATION_SRC_LINUX = STORM_FRAMEWORK_LOCATION+"src/"
		String command = "node -r esm storm_jsonrpc.js"
		ProcessBuilder pb;
		String osName = System.getProperty(Constants.OS_NAME)
		Process p
		if(osName?.startsWith(Constants.OS_WINDOWS)){
			pb = new ProcessBuilder("cmd.exe", "/C", command)
			pb.directory(new File(STORM_FRAMEWORK_LOCATION_SRC_WINDOWS))
			p = pb.start();
		}else{
		    pb = new ProcessBuilder("bash", "-c", command)
			pb.directory(new File(STORM_FRAMEWORK_LOCATION_SRC_LINUX))
			p = pb.start();
		}
		String line
		BufferedReader input = new BufferedReader(new InputStreamReader(p.getInputStream()));
		boolean isRunning = false
		while ((line = input.readLine()) != null) {
			if(line.contains("JSON RPC server is listening at")){
				isRunning = true;
				break;
			}
		}
		input.close()
		return isRunning
	}
	
	/**
	 * Method which creates a thunder version file
	 * @param realPath
	 * @param executionInstanceId
	 * @param executionDeviceInstanceId
	 * @param stbIP
	 * @return
	 */
	def static boolean createThunderVersionFile(def realPath, def executionInstanceId, def executionDeviceInstanceId, def stbIP){
		boolean versionFilecreationSuccess = false
		String folderPath = realPath+File.separator+"logs"+File.separator+"version"
		String executionInstanceDirPath = folderPath+File.separator+executionInstanceId
		File executionInstanceDir = new File(executionInstanceDirPath)
		if(!executionInstanceDir.exists()){
			if(executionInstanceDir.mkdir()){
				String executionDeviceInstanceDirPath = executionInstanceDirPath+File.separator+executionDeviceInstanceId
				File executionDeviceInstanceDir = new File(executionDeviceInstanceDirPath)
				if(!executionDeviceInstanceDir.exists()){
					if(executionDeviceInstanceDir.mkdir()){
						String versionFileName = executionDeviceInstanceId+"_version.txt"
						String versionFileAbsolutePath = executionDeviceInstanceDirPath +File.separator+versionFileName
						File versionFile = new File(versionFileAbsolutePath)
						String thunderversionDetails = retrieveThunderVersionDetails(stbIP)
						if(versionFile.createNewFile()){
							FileWriter fr = new FileWriter(versionFile)
							fr.write(thunderversionDetails)
							fr.close()
							versionFilecreationSuccess = true
						}
					}
				}
			}
		}
		return versionFilecreationSuccess
	}
	
	/**
	 * Method which retrieves thunder version details
	 * @param stbIP
	 * @return
	 */
	def static String retrieveThunderVersionDetails(def stbIP){
		String thunderVersionDetails = ""
		Process p
		boolean connectionSuccess = true
		String[] thunderArray
		String uptime
		String devicename
		String deviceid
		String thunderVersionDetailsFormatted = ""
		try
		{
			String urlString = "http://"+stbIP+":80/jsonrpc"
			URL url = new URL(urlString);
			URLConnection con = url.openConnection();
			HttpURLConnection http = (HttpURLConnection)con;
			http.setRequestMethod("POST");
			http.setDoOutput(true);
			byte[] out = "{\"jsonrpc\": \"2.0\",\"id\": 1234567890,\"method\": \"DeviceInfo.1.systeminfo\"}" .getBytes(StandardCharsets.UTF_8);
			int length = out.length;
			http.setFixedLengthStreamingMode(length);
			http.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
			http.setRequestProperty("Accept", "application/json");
			con.getOutputStream().write(out);
			http.connect();
			InputStream iStream = new BufferedInputStream(con.getInputStream());
				String result = org.apache.commons.io.IOUtils.toString(iStream, "UTF-8");
				JSONObject jsonObject = new JSONObject(result);
				iStream.close();
			JSONObject resultJsonObject = new JSONObject(jsonObject.get('result'))
			if(resultJsonObject?.has('uptime')){
			    uptime = resultJsonObject.get('uptime')
			}else{
			    uptime = "Uptime not available"
			}
			if(resultJsonObject?.has('devicename')){
				devicename = resultJsonObject.get('devicename')
			}else{
			    devicename = "Devicename not avaialble"
			}
			if(resultJsonObject?.has('deviceid')){
				deviceid = resultJsonObject.get('deviceid')
			}else{
			    deviceid = "Device id not available"
			}
			thunderVersionDetailsFormatted = "uptime : "+uptime+"\ndevicename : "+devicename+"\ndeviceid : "+deviceid
		}
		catch(Exception e){
			e.printStackTrace();
		}
		return thunderVersionDetailsFormatted
	}
	
	/**
	 * Method to return the value of a property after reading from a config file
	 * @param configFile
	 * @param key
	 * @return
	 */
	public static String getConfigProperty(File configFile, String key) {
		try {
			Properties prop = new Properties()
			if (configFile.exists()) {
				InputStream is = new FileInputStream(configFile);
				prop.load(is)
				String value = prop.getProperty(key)
				if (value != null && !value.isEmpty()) {
					return value
				}
			}else{
				println "No Config File !!! "
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		return null
	}
	
	/**
	 * Method which will kill the node server
	 * @param application
	 * @return
	 */
	def static boolean killNode(application) {
			try{
			    String line
			    Process p;
			    ProcessBuilder pb
				String command = "pkill -9 -f storm_jsonrpc"
			    pb = new ProcessBuilder("bash", "-c", command)
			    p = pb.start()
				if( !(isNodeAvailable())){
					return true
				}else{
					return false
				}
			}catch(Exception e){
			    e.printStackTrace()
			}
	}
	
	/**
	 * Method which will restart the node server
	 * @param application
	 * @return
	 */
	def static boolean reStartNode (application){
		boolean nodeRestarted = false
		try{
		    if( !(isNodeAvailable())){
			    nodeRestarted = startNode(application)
		    }else{
                killNode()
			    nodeRestarted = startNode(application)
		    }
		} catch(Exception e){
		    e.printStackTrace()
		}
		return nodeRestarted
	}
}