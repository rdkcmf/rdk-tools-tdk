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
package com.comcast.rdk

import static com.comcast.rdk.Constants.*

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

/**
 * Service to handle the log download in zip format.
 */
class LogZipService {

	def executionService
	
	def scriptService
	
	/**
	 * Method to zip the logs available as part of execution as zip file.
	 */
	def zipLogs(def realPath , def outputStream , def executionId , def type) {
		Execution exec = Execution.get(executionId)
		if(exec){
			ExecutionDevice exDevice = ExecutionDevice.findByExecution(exec)
			ZipOutputStream zos = new ZipOutputStream(outputStream);
			def exResultList = ExecutionResult.findAllByExecution(exec)
			
			exResultList.each { executionResult ->
				
				try {
					if( (type == ALL_LOGS && (executionResult?.status?.equals(SUCCESS) || executionResult?.status?.equals(FAILURE))) || (type == FAILURE_LOGS && executionResult?.status?.equals(FAILURE)) ){
						/*preparing the script name and the module name to make the file structure for ZIP */
						String scriptName = executionResult?.script
						String moduleName = getModuleName(realPath,scriptName)
						scriptName = scriptName.replaceAll("[^a-zA-Z0-9.-]", "_");
						moduleName = moduleName.replaceAll("[^a-zA-Z0-9.-]", "_");

						/* writing the agent console log*/
						String agentConsoleFileData = executionService.getAgentConsoleLogData( realPath , executionResult?.execution?.id?.toString(), executionResult?.executionDevice?.id?.toString(),executionResult?.id?.toString())
						writeZipEntry(agentConsoleFileData , "${moduleName}\\${scriptName}\\${scriptName}_AgentConsoleLog.txt" , zos)
						/* writing the python script log*/
						writeZipEntry(executionResult?.executionOutput , "${moduleName}\\${scriptName}\\${scriptName}_ScriptLog.txt" , zos)

						/* handling the stb logs associates with the execution if any */
						def logFiles = executionService.getLogFileNames(realPath ,exec?.id?.toString() , exDevice?.id?.toString(), executionResult?.id?.toString() )
						logFiles?.keySet().each { key ->
							def logFile = logFiles.get(key)
							if(logFile){
								String stbLog = getStbLogs(realPath, executionId,  exDevice?.id, executionResult?.id, logFile)
								writeZipEntry(stbLog , "${moduleName}\\${scriptName}\\${scriptName}_DeviceLog_${logFile}.txt" , zos)
							}
						}
					}
				} catch (Exception e) {
					e.printStackTrace()
				}
				
			}
			zos.closeEntry();
			zos.close();
		}
	}
	
	/**
	 *Method to write the zip entry into the outputstream.
	 */
	def writeZipEntry(def data , def fileName , def zos ){
		try {
			if(data == null || data?.trim()?.equals("")){
				data = NO_LOGS
			}
			data = convertScriptFromHTMLToText(data)
			ZipEntry zee = new ZipEntry(fileName);
			zos.putNextEntry(zee);
			int len = data.size()
			zos.write(data.getBytes(), 0, len);
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
	/**
	 * Method to fetch the stb log file contents
	 */
	def getStbLogs(def realPath , def execId , def execDeviceId , def execResultId , def name ){
		String filePath = "${realPath}//logs//stblogs//${execId}//${execDeviceId}//${execResultId}//${name}"
		String fileContents = ""
		try {
			File file = new File(filePath)
			if(file.exists() && file.isFile()){
				file.eachLine { line ->
					fileContents = fileContents + KEY_ENTERNEW_LINE + line
				}
			}else{
				fileContents = FILE_NOT_FOUND
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		return fileContents
	}
	
	/**
	 * Method to convert html data to text format
	 */
	def convertScriptFromHTMLToText(final String script){
		def afterspan =removeAllSpan(script)
		def afterBr = afterspan.replaceAll(HTML_REPLACEBR, KEY_ENTERNEW_LINE)
		afterBr = afterBr.replaceAll(HTML_LESSTHAN,LESSTHAN);
		afterBr = afterBr.replaceAll(HTML_GREATERTHAN, GREATERTHAN)
		return afterBr;
	}
	
	/**
	 * Method to convert span element data to text format
	 */
	def removeAllSpan(String script) {
		Matcher m = Pattern.compile(HTML_PATTERN).matcher(script)
		while(m.find()){
			String match = m.group(1);
			script =script.replace(match, "");
		}
		String afterspan =script.replaceAll(HTML_PATTERN_AFTERSPAN, "")
		return afterspan
	}
	
	/**
	 * Method to fetch the module name corresponding to a script
	 */
	def getModuleName(String realPath , def scriptName){
		def sMap = scriptService.getScriptNameModuleNameMapping(realPath)
		def moduleName = sMap.get(scriptName)
		if(moduleName == null){
			moduleName = DEFAULT
		}
		return moduleName
	}
}
