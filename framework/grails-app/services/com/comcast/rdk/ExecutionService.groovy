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

import org.apache.shiro.SecurityUtils
import org.codehaus.groovy.grails.web.json.JSONObject
import org.junit.After;
import grails.converters.JSON

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.text.SimpleDateFormat;
import java.util.List;
import java.util.Properties;
import java.util.concurrent.FutureTask
import java.util.regex.Matcher
import java.util.regex.Pattern
import com.google.gson.JsonObject
/**
 * Service class for the Execution domain.
 * @author sreejasuma, praveenkp
 */

class ExecutionService {
    
    /**
     * Injects the grailsApplication.
     */
    def grailsApplication
	
	/**
	 * Injects the scriptService
	 */
	def scriptService
	/**
	 * transient variable to keep the list of execution to be aborted
	 */
	public static volatile List abortList = []
	
	public static volatile List pauseList = []
	
	public static volatile List deviceAllocatedList = [].asSynchronized()
	
	public static volatile Map executionProcessMap = [:]
	
	public static transient Process tftpProcess
	
    
    /**
     * Get the name of the day from the number used in cronschedule
     * to denote days
     * @param day
     * @return
     */
    def String getDayName(final String day){
        String dayName
        switch(day){
            case "1":
                dayName = "Sunday"
                break
            case "2":
                dayName = "Monday"
                break
            case "3":
                dayName = "Tuesday"
                break
            case "4":
                dayName = "Wednesday"
                break
            case "5":
                dayName = "Thursday"
                break
            case "6":
                dayName = "Friday"
                break
            case "7":
                dayName = "Saturday"
                break
            default:
                dayName = "Invalid day"
                break
        }        
    }
    
    /**
     * Get the option name from the number used in cronschedule for 
     * monthly options
     * @param day
     * @return
     */
    def String getOptionName(final String optionVal){
        String optionName
        switch(optionVal){
            case "1":
                optionName = "First"
                break
            case "2":
                optionName = "Second"
                break
            case "3":
                optionName = "Third"
                break
            case "4":
                optionName = "Fourth"
                break         
            default:
                optionName = "Invalid option"
                break
        }
        
    }
	
	def getAgentConsoleLogData(final String realPath, final String executionId, final String executionDeviceId, final String execResId){
		def summaryFilePath = "${realPath}//logs//consolelog//${executionId}//${executionDeviceId}//${execResId}"
		String fileContents = ""
		try{
			File directory = new File(summaryFilePath)
			directory.eachFile { file ->
				if (file.isFile()) {
					String fileName = file.getName()
					if(fileName.startsWith( "AgentConsole" )){
						ExecutionResult execRes = ExecutionResult.findById(execResId)
						Execution execution = Execution.findById(executionId)
						fileContents = fileContents + "<br>"+ "Execution Name: "+execution.name
						fileContents = fileContents + "<br>"+ "Script : "+execRes.script
						fileContents = fileContents + "<br>"+ "======================================="
						file.eachLine { line ->
							String lineData = line?.replaceAll("<","&lt;")
							lineData = lineData?.replaceAll(">","&gt;")
							fileContents = fileContents + "<br>"+ lineData
						}						
					}else if(fileName.startsWith( "ServerConsole" )){//ServerConsole logs
					    file.eachLine { line ->
							fileContents = fileContents + line + HTML_BR
					    }
					}
				}
			}
		}
		catch(Exception ex){
		}
		return fileContents
	}
	
	
	def getLogFileNames(final String realPath, final String executionId, final String executionDeviceId, final String executionResId){
		def mapVals = [:]
		def summaryFilePath = "${realPath}//logs//${executionId}//${executionDeviceId}//${executionResId}"//_TestSummary"
		try{
			File directory = new File(summaryFilePath);
			List<File> foundFiles = new ArrayList<File>()
			
			if(directory?.exists()){
			directory.eachFile {
				if (it.isFile()) {
					String fileName = it.getName()
					if(fileName.startsWith( "${executionId}_TestSummary" )){
						foundFiles << new File("${realPath}//logs//${executionId}//${executionDeviceId}//${executionResId}//${fileName}")
					}
				}
			}
			}
			if(foundFiles?.size() > 0){
			   def fileAppendTimestamp
			   def summaryFileName
				
			   for (File filename : foundFiles) {
				   summaryFileName = filename.getName()
				   int index = summaryFileName.lastIndexOf( UNDERSCORE )
				   fileAppendTimestamp = summaryFileName.substring( index )
				   String[] lineArray
				   filename.eachLine { line ->
					   lineArray = null
					   lineArray = line.split( SEMI_COLON );
					   if(lineArray.length >= INDEX_TWO){
						   if(lineArray[INDEX_TWO] != null){
							   String fileNameString = lineArray[INDEX_TWO]
							   int indexFlag = fileNameString.lastIndexOf( URL_SEPERATOR )
							   String fileName = fileNameString.substring( ++indexFlag )
							   mapVals.put( fileName.trim()+fileAppendTimestamp, lineArray[INDEX_ONE] )
						   }
					   }
				   }
			   }
			}
			else{
			  String filePath = "${realPath}//logs//${executionId}//${executionDeviceId}//${executionResId}"
				def dir = new File(filePath)
				dir.eachFile {
					if (it.isFile()) {
						String fileName = it.getName()
						if(fileName.startsWith( executionId )){
							fileName = fileName.replaceFirst( executionId+UNDERSCORE, "" )
							mapVals.put( fileName.trim(), "" )
						}
					}
				}
			}
		}catch(FileNotFoundException fnf){
			mapVals = [:]
		}
		catch(Exception ex){
			mapVals = [:]
		}
		
		try{
			
			List<File> foundFiles = new ArrayList<File>()
			def summaryFilePath1 = "${realPath}//logs//stblogs//${executionId}//${executionDeviceId}//${executionResId}"
			File directory = new File(summaryFilePath1);
			if(directory?.exists()){
			directory.eachFile {
				if (it.isFile()) {
					String fileName = it.getName()
						foundFiles << new File("${realPath}//logs//stblogs//${executionId}//${executionDeviceId}//${executionResId}//${fileName}")
				}
			}
			}
			
			
	
			if(foundFiles?.size() > 0){
			   def fileAppendTimestamp
			   def summaryFileName
				
				for (File filename : foundFiles) {
					summaryFileName = filename.getName()
					mapVals.put( summaryFileName.trim(), summaryFileName.trim() )
				}
			}
			else{
			  String filePath = "${realPath}//logs//${executionId}//${executionDeviceId}//${executionResId}"
				def dir = new File(filePath)
				dir.eachFile {
					if (it.isFile()) {
						String fileName = it.getName()
						if(fileName.startsWith( executionId )){
							fileName = fileName.replaceFirst( executionId+UNDERSCORE, "" )
							mapVals.put( fileName.trim(), "" )
						}
					}
				}
			}
		}catch(FileNotFoundException fnf){
		println "ee> "+fnf.getMessage()
		}
		catch(Exception ex){
			println "eee> "+ex.getMessage()
		}
		return mapVals
	}

	
	
	def getCrashLogFileNames(final String realPath, final String executionId, final String executionDeviceId, final String executionResId){
		def mapVals = [:]
		try{
			  String filePath = "${realPath}//logs//crashlogs//${executionId}//${executionDeviceId}//${executionResId}"
				def dir = new File(filePath)
				dir.eachFile {
					if (it.isFile()) {
						String fileName = it.getName()
						if(fileName.startsWith( "${executionId}_${executionDeviceId}" )){
							fileName = fileName.replaceFirst( executionId+UNDERSCORE+executionDeviceId+UNDERSCORE, "" )
							mapVals.put( fileName.trim(), "" )
						}
					}
				}
			
		}catch(FileNotFoundException fnf){
			mapVals = []
		}
		catch(Exception ex){
			mapVals = []
		}
		return mapVals
	}
	
    
    /**
     * Get the list of log file names generated after the
     * script execution
     * @param executionId
     * @return
     */
    def getLogFileNames(final String realPath, final String executionId){
        def mapVals = [:]
        def summaryFilePath = "${realPath}//logs//${executionId}"//_TestSummary"
        try{
            File directory = new File(summaryFilePath);
            List<File> foundFiles = new ArrayList<File>()
            
            directory.eachFile {
                if (it.isFile()) {
                    String fileName = it.getName()
                    if(fileName.startsWith( "${executionId}_TestSummary" )){
                        foundFiles << new File("${realPath}//logs//${executionId}//${fileName}")
                    }
                }
            }
        
            if(foundFiles?.size() > 0){
               def fileAppendTimestamp
               def summaryFileName
                
               for (File filename : foundFiles) {
                   summaryFileName = filename.getName()
                   int index = summaryFileName.lastIndexOf( UNDERSCORE )
                   fileAppendTimestamp = summaryFileName.substring( index )
                   String[] lineArray
                   filename.eachLine { line ->
                       lineArray = null
                       lineArray = line.split( SEMI_COLON );
                       if(lineArray.length >= INDEX_TWO){
                           if(lineArray[INDEX_TWO] != null){
                               String fileNameString = lineArray[INDEX_TWO]
                               int indexFlag = fileNameString.lastIndexOf( URL_SEPERATOR )
                               String fileName = fileNameString.substring( ++indexFlag )
                               mapVals.put( fileName.trim()+fileAppendTimestamp, lineArray[INDEX_ONE] )
                           }
                       }
                   }
               }
            }
            else{
              String filePath = "${realPath}//logs//${executionId}"
                def dir = new File(filePath)
                dir.eachFile {
                    if (it.isFile()) {
                        String fileName = it.getName()
                        if(fileName.startsWith( executionId )){
                            fileName = fileName.replaceFirst( executionId+UNDERSCORE, "" )
                            mapVals.put( fileName.trim(), "" )
                        }
                    }
                }
            }
        }catch(FileNotFoundException fnf){
            mapVals = []
        }
        catch(Exception ex){
            mapVals = []
        }
        return mapVals
    }

    
    
    /**
     * Method to call the script executor to execute the script
     * @param executionData
     * @return
     */
    public String executeScript(final String executionData) {
        new ScriptExecutor().execute( getCommand( executionData ),1)
    }
	
	public String executeScript(final String executionData , final String executionName, final String scriptName) {
		String opFile = prepareOutputfile(executionName, scriptName)
		String output = NEW_LINE+getCurrentTime()+NEW_LINE+"Executing script : "+scriptName+NEW_LINE
		output += "======================================="+NEW_LINE
		output += new ScriptExecutor(opFile).execute( getCommand( executionData ))
		return output
	}
	
	private String prepareOutputfile(final String executionName, final String scriptName){
		try {
			def folderName = Constants.SCRIPT_OUTPUT_FILE_PATH
			File folder = grailsApplication.parentContext.getResource(folderName).file
			folder.mkdirs();

			def fileName = folderName+executionName+Constants.SCRIPT_OUTPUT_FILE_EXTN

			File opFile = grailsApplication.parentContext.getResource(fileName).file


			boolean append = true
			FileWriter fileWriter = new FileWriter(opFile, append)
			BufferedWriter buffWriter = new BufferedWriter(fileWriter)
			buffWriter.write(NEW_LINE+getCurrentTime())
			buffWriter.write("<br/>Executing script : "+scriptName+"<br/>"+NEW_LINE);
			buffWriter.write("======================================<br/>"+NEW_LINE);
			buffWriter.flush()
			buffWriter.close()
			return opFile.getAbsolutePath();
		} catch(Exception ex) {
		}
		
		return null
	}
    
	 /**
     * Method to call the script executor to execute the script
     * @param executionData
     * @return
     */
    public String executeScript(final String executionData, int execTime, final String executionName, final String scriptName) {
		String opFile = prepareOutputfile(executionName, scriptName)
		String output = NEW_LINE+getCurrentTime()+NEW_LINE+"Executing script : "+scriptName+NEW_LINE;
		output += "======================================="+NEW_LINE
//		output += new ScriptExecutor(opFile).execute( getCommand( executionData ), execTime)
		output += new ScriptExecutor(opFile).execute( getCommand( executionData ), execTime,executionName,executionProcessMap)
		return output
    }
	
	
	/**
	 * Execute tclscript from command line
	 * @param executionData
	 * @param execTime
	 * @param executionName
	 * @param scriptName
	 * @return
	 */
	public String executeTclScript(final String tclExecutableFile, final String configFile, int execTime, final String executionName, final String scriptName, final String scriptDir, final String combainedTclScriptName) {
		String opFile = prepareOutputfile(executionName, scriptName)
		String output = NEW_LINE+getCurrentTime()+NEW_LINE+"Executing script : "+scriptName+NEW_LINE;
		output += "======================================="+NEW_LINE
		def tclFilePath = ""		
		def command		
		boolean combine = false 
		if(combainedTclScriptName){
			combine = true
		}else{
			combine = false 
		}
		if(combine &&  combainedTclScriptName && scriptService?.tclScriptsList?.toString().contains(scriptName?.toString()) && scriptService?.totalTclScriptList?.toString()?.contains(combainedTclScriptName?.toString())){
			command =  "tclsh $tclExecutableFile $configFile $combainedTclScriptName"
		}else if( !combainedTclScriptName && scriptService?.tclScriptsList?.toString().contains(scriptName?.toString()) && !scriptService?.totalTclScriptList?.toString()?.contains(scriptName?.toString())){
			def startScriptName =  scriptName?.toString().split("_to_")
			def firstName
			if(startScriptName?.length > 0 ){
				firstName = startScriptName[0]
				command =  "tclsh $tclExecutableFile $configFile $firstName"
			}
		}else{
		
			command = "tclsh $tclExecutableFile $configFile"
		}	
		output += new ScriptExecutor(opFile).execute( command, execTime,executionName,executionProcessMap, scriptDir)		
		return output
	}
	
	
    /**
     * Method to validate script
     * @param executionData
     * @return
     */
    public String validateScript(final String executionData) {
        new ScriptExecutor().validateScript( getCommand( executionData ))
    }
    
    /**
     * Method to get the python script execution command.
     * @param command
     * @return
     */
    public String getCommand(final String command) {                
        String actualCommand = grailsApplication.config.python.execution.path +" "+ command    
        return actualCommand
    }
    
    /**
     * Converts the script that is given in textarea to 
     * python format
     * @param script
     * @return
     */
	def convertScriptFromHTMLToPython(final String script){
		def output
		if(script){
			def afterspan =removeAllSpan(script)
			def afterBr = afterspan.replaceAll(HTML_REPLACEBR, KEY_ENTERNEW_LINE)
			afterBr = afterBr.replaceAll(HTML_LESSTHAN,LESSTHAN);
			afterBr = afterBr.replaceAll(HTML_GREATERTHAN, GREATERTHAN)
			output =  afterBr;
		}else{
			output = script
		}
		return output
	}

    
    /**
     * Removes all span from the script 
     * @param script
     * @return
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
     * Validates whether the boxtype of device is same as that 
     * of the boxtype specified in the script
     * @param scriptInstance
     * @param deviceInstance
     * @return
     */
//    public boolean validateScriptBoxType(final Script scriptInstance, final Device deviceInstance){
//        boolean scriptStatus = true
//		Script.withTransaction { trns ->
//			def scriptInstance1 = Script.findById(scriptInstance?.id)			
//			def deviceInstance1 = Device.findById(deviceInstance?.id)
//	        if(!(scriptInstance1?.boxTypes?.find { it?.id == deviceInstance1?.boxType?.id })){   
//	            scriptStatus = false
//	        }
//		}
//        return scriptStatus
//    }
	
	public boolean validateScriptBoxTypes(final Map script, final Device deviceInstance){
		boolean scriptStatus = true
		def deviceInstance1 = Device.findById(deviceInstance?.id)
		//For Test suite issue fixing 
		if(!(script?.boxTypes?.find { it?.toString()?.equals(deviceInstance1?.boxType?.toString()) })){
		//if(!(script?.boxTypes?.find { it?.id == deviceInstance1?.boxType?.id })){
			scriptStatus = false
		}
		return scriptStatus
	}
	
	/**
	 * Validates whether the RDK version of device is same as that
	 * of the RDK versions specified in the script
	 * @param scriptInstance
	 * @param device rdkVersion
	 * @return
	 */
//	public boolean validateScriptRDKVersion(final Script scriptInstance, final String rdkVersion){
//		boolean scriptStatus = true
//		String versionText = rdkVersion
//		if(rdkVersion){
//			versionText = rdkVersion.trim()
//		}
//		if(versionText && !(versionText?.equals("NOT_AVAILABLE") || versionText?.equals("NOT_VALID") || versionText?.equals("")) ){
//			Script.withTransaction { trns ->
//				def scriptInstance1 = Script.findById(scriptInstance?.id)
//				if(scriptInstance1?.rdkVersions?.size() > 0 && !(scriptInstance1?.rdkVersions?.find { 
//					it?.buildVersion?.equals(versionText) 
//					})){
//					scriptStatus = false
//				}
//			}
//		}
//		return scriptStatus
//	}
	
	public boolean validateScriptRDKVersions(final Map script, final String rdkVersion){
		boolean scriptStatus = true
		String versionText = rdkVersion
		if(rdkVersion){
			versionText = rdkVersion.trim()
		}
		if(versionText && !(versionText?.equals("NOT_AVAILABLE") || versionText?.equals("NOT_VALID") || versionText?.equals("")) ){
				if(script?.rdkVersions?.size() > 0 && !(script?.rdkVersions?.find {
					it?.buildVersion?.equals(versionText)
					})){
					scriptStatus = false
				}
		}
		return scriptStatus
	}
    
    /**
     * Validates whether the boxtype of device is same as that
     * of the boxtype specified in the script
     * @param scriptInstance
     * @param deviceInstance
     * @return
     */
    public boolean validateBoxTypeOfScript(final Script scriptInstance, final String boxType){
        boolean scriptStatus = true
        if(!(scriptInstance.boxTypes.find { (it.name).equalsIgnoreCase( boxType ) })){
            scriptStatus = false
        }
        return scriptStatus
    }
    
	
	/**
	 * TO DO : Create a folder with executionDevice name when transfering script
	 * 
	 * Method to execute the versiontransfer.py script stored in filestore folder of webapps
	 * @param realPath
	 * @param filePath
	 * @param executionName
	 * @param stbIp
	 * @param logTransferPort
	 * @return
	 */
    def executeVersionTransferScript(final String realPath, final String filePath, final String executionName, def exectionDeviceId, final String stbName, final String logTransferPort,def url){
        try{
	        def executionInstance = Execution.findByName(executionName)
	      /*  String fileContents = new File(filePath+DOUBLE_FWD_SLASH+VERSIONTRANSFER_FILE).text
	        
	        fileContents = fileContents.replace(IP_ADDRESS, STRING_QUOTES+stbIp+STRING_QUOTES)
			
			fileContents = fileContents.replace(PORT, logTransferPort)
			
	        String versionFilePath = "${realPath}//logs//version//${executionInstance?.id}//${exectionDeviceId?.toString()}//${exectionDeviceId?.toString()}_version.txt"
	        fileContents = fileContents.replace(LOCALFILE, STRING_QUOTES+versionFilePath+STRING_QUOTES)
	        
	        String versionFile = TEMP_VERSIONFILE_NAME
		//	new File("${realPath}//logs//version//${executionInstance?.id}//${exectionDeviceId?.toString()}").mkdirs()
	        File versnFile = new File(filePath, versionFile)
	        boolean isVersionFileCreated = versnFile.createNewFile()
	        if(isVersionFileCreated) {
	            versnFile.setExecutable(true, false )
	        }
	        PrintWriter versnNewPrintWriter = versnFile.newPrintWriter()
	        versnNewPrintWriter.print( fileContents )
	        versnNewPrintWriter.flush()
			versnNewPrintWriter.close()
	        executeScript( versnFile.getPath() )
	        versnFile.delete()*/
			Device device = Device.findByStbName(stbName)
			String versionFileName = "${executionInstance?.id}_${exectionDeviceId?.toString()}_version.txt"
			def versionFilePath = "${realPath}//logs//version//${executionInstance?.id}//${exectionDeviceId?.toString()}"
			String scriptName = getFileTransferScriptName(device)
			File layoutFolder = grailsApplication.parentContext.getResource(scriptName).file
			def absolutePath = layoutFolder.absolutePath
			
			def cmdList = [
				PYTHON_COMMAND,
				absolutePath,
				device.stbIp,
				device.agentMonitorPort,
				"/version.txt",
				versionFileName
			]
			
			if(scriptName?.equals(FILE_UPLOAD_SCRIPT)){
				url = updateTMUrl(url,device)
				def urlFromConfigFile = getTMUrlFromConfigFile()
				if(urlFromConfigFile != null){
					url = urlFromConfigFile
				}
				cmdList.push(url)
			}
			
			String [] cmd = cmdList.toArray()
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def outputData = scriptExecutor.executeScript(cmd,1)
			copyVersionLogsIntoDir(realPath, versionFilePath, executionInstance?.id , exectionDeviceId?.toString())
			
			def devName
			ExecutionDevice.withTransaction {
				devName = ExecutionDevice.get(exectionDeviceId)?.device
	        }
			def dev = device
			if(devName){
				dev = Device.findByStbName(devName)
			}
			if(dev?.boxType?.type?.equalsIgnoreCase(BOXTYPE_CLIENT)){
				getDeviceDetails(dev,device.agentMonitorPort,realPath,url)
			}
			
        }
		catch(Exception ex){	
			println " Error "+ex.getMessage()		
		}		
    }
	
	
	/**
	 * Function for copy the version file into  logs directory using TFTP Server
	 * @param realPath
	 * @param logTransferFilePath
	 * @return
	 */
	def copyVersionLogsIntoDir(def realPath, def logTransferFilePath,  def executionId , def executionDeviceId){
		try {
			String logsPath = realPath.toString()+"/logs/logs/"
			File logDir  = new File(logsPath)
			if(logDir.isDirectory()){
				logDir.eachFile{ file->
					if(file?.toString().contains("version.txt")){
						def logFileName =  file.getName().split("_")
						if(logFileName?.length > 0){
							if(executionId?.toString()?.equals(logFileName[0]?.toString()) && executionDeviceId?.toString()?.equals(logFileName[1]?.toString())){
								def  versionFileName = logFileName[1]+"_"+logFileName.last()
								new File(logTransferFilePath?.toString()).mkdirs()
								File logTransferPath  = new File(logTransferFilePath)
								if(file.exists()){
									boolean fileMoved = file.renameTo(new File(logTransferPath, versionFileName));
								}
							}
						}
					}
				}
			}
		} catch (Exception e) {
			log.error  " Error"+e.getMessage()
			e.printStackTrace()
		}
	}

	/**
	 * Copy the device logs file into devicelog directory using TFTP server.
	 * @param realPath
	 * @param logTransferFilePath
	 * @return
	 */
	def copyDeviceLogIntoDir(def realPath, def logTransferFilePath){
		try {
			String logsPath = realPath.toString()+"/logs/logs/"
			File logDir  = new File(logsPath)
			if(logDir.isDirectory()){
				logDir.eachFile{ file->
					def logFileName =  file.getName().split("_")
					if(logFileName?.length > 0){
					new File(logTransferFilePath?.toString()).mkdirs()
					File logTransferPath  = new File(logTransferFilePath)
					if(file.exists()){
						boolean fileMoved = file.renameTo(new File(logTransferPath, logFileName.last()));
						}
					}
				}
			}
		} catch (Exception e) {
			log.error  " Error"+e.getMessage()
			e.printStackTrace()
		}
	}
	
	
	/**
	 * method to fetch the name of the file transfer script
	 */
	
	def getFileTransferScriptName(Device device){
		String scriptName = FILE_TRANSFER_SCRIPT
		
		if(InetUtility.isIPv6Address(device?.stbIp)){
			scriptName = FILE_UPLOAD_SCRIPT
		}else{
			if(getIPV4LogUploadMechanism()?.equals(Constants.REST_MECHANISM)){
				scriptName = FILE_UPLOAD_SCRIPT
			}
			
		}
		return scriptName
	}
	
	

	def getDeviceDetails(Device device, def logTransferPort, def realPath,def url){
		
		try {
			//new File("${realPath}//logs//devicelogs//${device?.stbName}").mkdirs()

		String scriptName = getFileTransferScriptName(device)
		File layoutFolder = grailsApplication.parentContext.getResource(scriptName).file
		def absolutePath = layoutFolder.absolutePath
		def filePath = "${realPath}//logs//devicelogs//${device?.stbName}//"
		
		def cmdList = [
			"python",
			absolutePath,
			device?.stbIp,
			device?.agentMonitorPort,		
			"/opt/TDK/trDetails.log",
			"${device?.stbName}"+"_"+"${device?.stbName}.txt" 
		]

		if(scriptName?.equals(FILE_UPLOAD_SCRIPT)){
			url = updateTMUrl(url,device)
			def urlFromConfigFile = getTMUrlFromConfigFile()
			if(urlFromConfigFile != null){
				url = urlFromConfigFile
			}
			cmdList.push(url)
		}
				
		String [] cmd = cmdList.toArray()
		
	    ScriptExecutor scriptExecutor = new ScriptExecutor()
	    def outputData = scriptExecutor.executeScript(cmd,1)
		copyDeviceLogIntoDir(realPath,filePath)
		
		parseAndSaveDeviceDetails(device, filePath)		
		} catch (Exception e) {
			e.printStackTrace()
		}		
	}

	/**
	 * Method to return the Test Manager URl if the url is configured in tm.config file
	 * @return
	 */
	def getTMUrlFromConfigFile(){
		File configFile = grailsApplication.parentContext.getResource("/fileStore/tm.config").file
		Properties prop = new Properties();
		if (configFile.exists()) {
			InputStream is = new FileInputStream(configFile);
			prop.load(is);
			String value = prop.getProperty("tmURL");
			if (value != null && !value.isEmpty()) {
				return value;
			}
		}
		return null;
	}

	/**
	 * For getting the image name on a particular device
	 * - Accessing the getimagename_cmndline file
	 * - send command through TM ( python getimagename_cmndline.py Device_IP_Address PortNumber )
	 * @param stbName
	 * @return buildName
	 */
	 
	 
	def getBuildName(String stbName){
		String buildName
		JsonObject jsonOutData = new JsonObject()
		Device device = Device.findByStbName(stbName)
		if(device){
			try{
				File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//getimagename_cmndline.py").file
				def absolutePath = layoutFolder.absolutePath
				String[] cmd = [
					PYTHON_COMMAND,
					absolutePath,
					device.stbIp,
					device.stbPort
				]
				ScriptExecutor scriptExecutor = new ScriptExecutor()
				def outputData = scriptExecutor.executeScript(cmd,1)
				if(outputData && !(outputData?.toString()?.contains("METHOD_NOT_FOUND") || outputData?.toString()?.contains("AGENT_NOT_FOUND") )){
					buildName = outputData.toString()?.trim()
				}
				else{
					buildName =  "Image name not available"
					
				}
			}catch(Exception e ){
				println  "ERROR "+ e.getMessage()
				buildName =  "Image name not available"
				
			}
		}else{
			buildName =  "Image name not available"
		}
		return buildName
	}
	
	
	def parseAndSaveDeviceDetails(Device device, def filePath){

		try {
			File file = new File(filePath+"${device?.stbName}.txt")

			def map = [:]
			def bootargs = false

			def driversloaded = false
			def driversLoaded = ""

			def partitions = false
			def partition = ""

			def mounts = false
			def mount = ""

			file.eachLine { line ->
				if(line.startsWith("{\"paramList\"")){
					JSONObject userJson = JSON.parse(line)
					userJson.each { id, data ->
						data.each{ val ->

							switch ( val.name.toString().trim() ) {

								case "Device.DeviceInfo.Manufacturer":
									map["Manufacturer"] = val.value.toString()

								case "Device.DeviceInfo.ModelName":
									map["ModelName"] = val.value.toString()

								case "Device.DeviceInfo.SerialNumber":
									map["SerialNumber"] = val.value.toString()

								case "Device.DeviceInfo.HardwareVersion":
									map["HardwareVersion"] = val.value.toString()

								case "Device.DeviceInfo.SoftwareVersion":
									map["SoftwareVersion"] = val.value.toString()

								case "Device.DeviceInfo.ProcessorNumberOfEntries":
									map["NumberOfProcessor"] = val.value.toString()

								case "Device.DeviceInfo.Processor.1.Architecture":
									map["Architecture"] = val.value.toString()

								case "Device.DeviceInfo.UpTime":
									map["UpTime"] = val.value.toString()

								case "Device.DeviceInfo.ProcessStatus.ProcessNumberOfEntries":
									map["NumberOfProcessRunning"] = val.value.toString()

								case "Device.Ethernet.InterfaceNumberOfEntries":
									map["NumberOfInterface"] = val.value.toString()

								case "Device.DeviceInfo.MemoryStatus.Total":
									map["TotalMemory"] = val.value.toString()

								case "Device.DeviceInfo.MemoryStatus.Free":
									map["FreeMemory"] = val.value.toString()

								default:
									log.info("Default")
							}
						}
					}
				}

				if(bootargs){
					map["BootArgs"] = line
					bootargs = false
				}

				if(line.startsWith("#Bootagrs START")){
					bootargs = true
				}

				if(line.startsWith("#Driversloaded END")){
					map["Driversloaded"] = driversLoaded
					driversloaded = false
				}

				if(driversloaded){
					driversLoaded = driversLoaded + line + "<br>"
				}

				if(line.startsWith("#Driversloaded")){
					driversloaded = true
				}

				if(line.startsWith("#Partitions END")){
					map["Partitions"] = partition
					partitions = false
				}

				if(partitions){
					partition = partition + line + "<br>"
				}

				if(line.startsWith("#Partitions START")){
					partitions = true
				}

				if(line.startsWith("#mounts END")){
					map["Mount"] = mount
					mounts = false
				}

				if(mounts){
					mount = mount + line + "<br>"
				}

				if(line.startsWith("#mounts START")){
					mounts = true
				}
			}

			def deviceDetailsList = DeviceDetails.findAllByDevice(device)

			if(deviceDetailsList?.size() > 0){
				DeviceDetails.executeUpdate("delete DeviceDetails d where d.device = :instance1",[instance1:device])
			}

			DeviceDetails deviceDetails = new DeviceDetails()

			map?.each{ k,v ->
				deviceDetails = new DeviceDetails()
				deviceDetails.device = device
				deviceDetails.deviceParameter = k
				deviceDetails.deviceValue = v
				deviceDetails.save(flush:true)
			}

		} catch (Exception e) {
		}

	}

	/**
	 * Method which filters executions based on FromDate, ToDate, boxType, Category and script type
	 * @param fromDate
	 * @param toDate
	 * @param boxType
	 * @param category
	 * @param scriptTypeValue
	 * @param scriptValue
	 * @return
	 */
	public List filterExecutions( final String fromDate, final String toDate, final String boxType, final String category,final String scriptTypeValue,final String scriptValue){
		List executionList =[]
		def completedStatus = Constants.COMPLETED_STATUS
		if(fromDate && toDate && category && boxType){
			if((scriptTypeValue)){
				if((scriptTypeValue).equals( TEST_SUITE )){
					if(scriptValue){
						executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.category='${category}' and b.executionStatus='${completedStatus}' and b.scriptGroup like '%${scriptValue}%' order by id desc ")
					}
					else{
						if(category == Constants.RDKV_THUNDER){
							executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.category='${category}' and b.executionStatus='${completedStatus}' and b.scriptGroup is not ''  order by id desc")
						}else{
						    executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.category='${category}' and b.executionStatus='${completedStatus}' and b.scriptGroup is not null  order by id desc")
						}
					}
				}
				else{
					if(scriptValue){
						executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.category='${category}' and b.executionStatus='${completedStatus}'and (b.script like '%Multiple%' or b.script like '%${scriptValue}%' ) order by id desc")
					}
					else{
						if(category == Constants.RDKV_THUNDER){
							executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.category='${category}' and b.executionStatus='${completedStatus}' and b.script is not '' order by id desc")
						}else{
						    executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.category='${category}' and b.executionStatus='${completedStatus}' and b.script is not null order by id desc")
						}
					}
				}
			}
			else{
				executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.category='${category}' and b.executionStatus='${completedStatus}' order by id desc")
			}
			if(!executionList.isEmpty()){
				for (Iterator<Execution> iterator = executionList.iterator(); iterator.hasNext();) {
					Execution executionInstance = iterator.next();
					def executionDeviceInstance = ExecutionDevice.findByExecution(executionInstance)
					String boxTypeOfExecutionDevice = executionDeviceInstance?.boxType
					if(!boxTypeOfExecutionDevice.equals(boxType)){
						def executionInstanceIndex = executionList.indexOf(executionInstance)
						iterator.remove();
					}
				}
			}
		}
		return executionList
	}

    /**
     * Search execution list based on different search criterias of
     * script, device, and execution from and to dates.
     * @return
     */
    public List multisearch(final String toDate, final String fromDate, final String deviceName, final String resultStatus,
        final String scriptType, final String scriptVal){
        
        def executionList = []
        def executionResult
        if( toDate && fromDate ){
           
            if((!deviceName) && (!resultStatus) && (!scriptType)){
                executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' ")
            }
            else{
             if((scriptType)){
                
                if((scriptType).equals( TEST_SUITE )){
                    if(scriptVal){
                        if((!deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.scriptGroup like '%${scriptVal}%' ")
                        }
                        else if((deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.scriptGroup like '%${scriptVal}%' and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.scriptGroup like '%${scriptVal}%' and b.result='${resultStatus}'")
                        }
                        else if((deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.scriptGroup like '%${scriptVal}%' and b.device like '%${deviceName}%'")
                        }
                    }
                    else{
                        if((!deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.scriptGroup is not null ")
                        }
                        else if((deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.scriptGroup is not null and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.scriptGroup is not null and b.result='${resultStatus}'")
                        }
                        else if((deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.scriptGroup is not null and b.device like '%${deviceName}%'")
                        }
                    }
                }
                else{
                    if(scriptVal){
                        if((!deviceName) && (!resultStatus)){
                            executionResult = Execution.findAll("from Execution b, ExecutionResult c where b.id=c.execution and c.script like '%${scriptVal}%' and b.dateOfExecution between '${fromDate}' and '${toDate}'")
                        }
                        else if((deviceName) && (resultStatus)){
                            executionResult = Execution.findAll("from Execution b, ExecutionResult c where b.id=c.execution and c.script like '%${scriptVal}%' and b.dateOfExecution between '${fromDate}' and '${toDate}' and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (resultStatus)){
                            executionResult = Execution.findAll("from Execution b, ExecutionResult c where b.id=c.execution and c.script like '%${scriptVal}%' and b.dateOfExecution between '${fromDate}' and '${toDate}' and b.result='${resultStatus}'")
                        }
                        else if((deviceName) && (!resultStatus)){
                            executionResult = Execution.findAll("from Execution b, ExecutionResult c where b.id=c.execution and c.script like '%${scriptVal}%' and b.dateOfExecution between '${fromDate}' and '${toDate}' and b.device like '%${deviceName}%'")
                        }
                        executionResult.each{
                            executionList.add(it[INDEX_ZERO])
                        }
                    }
                    else{
                        if((!deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.script is not null ")
                        }
                        else if((deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.script is not null and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.script is not null and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.script is not null and b.device like '%${deviceName}%'")
                        }
                    }
                }
            }
            else{
                if((deviceName) && (resultStatus)){
                    executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                }
                else if((deviceName) && (!resultStatus)){
                    executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and '${toDate}' and b.device like '%${deviceName}%'")
                }
                else if((!deviceName) && (resultStatus)){
                    executionList = Execution.findAll("from Execution as b where b.dateOfExecution between '${fromDate}' and '${toDate}' and b.result='${resultStatus}'")
                }
            }
            
          }
        }
        else{
            if((scriptType)){
                
                if((scriptType).equals( TEST_SUITE )){
                    if(scriptVal){
                        if((!deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.scriptGroup like '%${scriptVal}%' ")
                        }
                        else if((deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.scriptGroup like '%${scriptVal}%' and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.scriptGroup like '%${scriptVal}%' and b.result='${resultStatus}'")
                        }
                        else if((deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.scriptGroup like '%${scriptVal}%' and b.device like '%${deviceName}%'")
                        }
                    }
                    else{
                        if((!deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.scriptGroup is not null ")
                        }
                        else if((deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.scriptGroup is not null and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.scriptGroup is not null and b.result='${resultStatus}'")
                        }
                        else if((deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.scriptGroup like is not null and b.device like '%${deviceName}%'")
                        }
                    }
                }
                else{
                    if(scriptVal){
                        if((!deviceName) && (!resultStatus)){
                            executionResult = Execution.findAll("from Execution b, ExecutionResult c where b.id=c.execution and c.script like '%${scriptVal}%'")
                        }
                        else if((deviceName) && (resultStatus)){
                            executionResult = Execution.findAll("from Execution b, ExecutionResult c where b.id=c.execution and c.script like '%${scriptVal}%' and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (resultStatus)){
                            executionResult = Execution.findAll("from Execution b, ExecutionResult c where b.id=c.execution and c.script like '%${scriptVal}%' and b.result='${resultStatus}'")
                        }
                        else if((deviceName) && (!resultStatus)){
                            executionResult = Execution.findAll("from Execution b, ExecutionResult c where b.id=c.execution and c.script like '%${scriptVal}%' and b.device like '%${deviceName}%' ")
                        }
                        executionResult.each{
                            executionList.add(it[INDEX_ZERO])
                        }
                    }
                    else{
                        if((!deviceName) && (!resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.script is not null ")
                        }
                        else if((deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.script is not null and b.device like '%${deviceName}%' and b.result='${resultStatus}'")
                        }
                        else if((!deviceName) && (resultStatus)){
                            executionList = Execution.findAll("from Execution as b where b.script is not null and b.result='${resultStatus}'")
                        }
                        else if((deviceName) && (!resultStatus)){
                            executionList =  Execution.findAll("from Execution as b where b.script is not null and b.device like '%${deviceName}%'")
                        }
                    }
                }
            }
            else {
                    if((deviceName) && (resultStatus)){
                        executionList = Execution.findAll("from Execution as b where b.device like '%${deviceName}%' and b.result='${resultStatus}' ")
                    }
                    else if((!deviceName) && (resultStatus)){
                        executionList = Execution.findAllByResult( resultStatus )
                    }
                    else if((deviceName) && (!resultStatus)){
                        executionList = Execution.findAllByDeviceIlike( deviceName )
                    }
                }
        }
        return executionList
    }
		
	/**
	 * Method to execute callgetdevices.py script with required parameters.
	 * eg: python callgetdevices.py 192.168.160.130 8088
	 * It will return execution result of callgetdevices.py.
	 * 
	 * @param device
	 * @return outputData
	 */
	def executeGetDevices(Device device){
		def outputArray
		def executionResult
		def outputData = ""
		def macIdList = []
		def absolutePath
		def boxIp = device?.stbIp
		def port = device?.statusPort

		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callgetdevices.py").file
		absolutePath = layoutFolder.absolutePath

		try {
			if(boxIp != null && port != null ){
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				boxIp,
				port
			]

			ScriptExecutor scriptExecutor = new ScriptExecutor()
			outputData = scriptExecutor.executeScript(cmd,1)
			//	 outputData = "DEVICES=<incomplete>,bb:cc:EE:dd:24,bb:cc:EE:dd:26,"  // Dummy data for testing purpose
		}

		} catch (Exception e) {
			e.printStackTrace()
		}

		return outputData
	}
	
	/**
	 * Method to fetch the RDK version of the device
	 * @param device
	 * @return
	 */
	def getRDKBuildVersion(Device device){
		def outputData
		def absolutePath
		def boxIp = device?.stbIp
		def port = device?.agentMonitorPort
		boolean isThunderEnabled = device?.isThunderEnabled
		String rdkVersion = ""
		if(!isThunderEnabled){
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callGetRDKVersion.py").file
			absolutePath = layoutFolder.absolutePath

			try {
				if(boxIp != null && port != null ){
					String[] cmd = [
				                	PYTHON_COMMAND,
									absolutePath,
									boxIp,
									port
				                	]
				                		
					ScriptExecutor scriptExecutor = new ScriptExecutor()
					outputData = scriptExecutor.executeScript(cmd,1)
				}
			} catch (Exception e) {
				e.printStackTrace()
			}
			if(outputData){
				outputData = outputData.trim()
			}else{
				outputData = ""
			}
		
			if(outputData.equals("METHOD_NOT_FOUND") || outputData.equals("AGENT_NOT_FOUND") || outputData.equals("NOT_DEFINED")){
				rdkVersion = "NOT_AVAILABLE"
			}else if(outputData.contains("DOT")){
				rdkVersion = outputData.replace("DOT",".")
			}else if(!outputData.equals("") && !outputData.startsWith("RDK")){
				rdkVersion = "RDK"+outputData.replace("DOT",".")
			}else{
				rdkVersion = outputData
			}
		
			if(rdkVersion && rdkVersion.contains(" ")){
				rdkVersion.replaceAll(" ", "")
			}
		}
		return rdkVersion
	}


	/**
	 * Method to parse the results obtained after the execution of callgetdevices.py script.
	 * @param executionResult
	 * @return macIdList - List of valid macIds if exists.
	 */
	def parseExecutionResult(final String executionResult){

		List macIdList = []
		def outputData
		def deviceResponse
		def outputArray		
		//macIdList.removeAll(macIdList)
		macIdList.clear()
		outputData = executionResult.toString().trim()
		if(outputData){
			if( outputData != NO_DEVICES_MSG && outputData != "AGENT_NOT_FOUND"  && outputData != "FAILURE" && outputData != "" && outputData != " " && outputData != null){
				deviceResponse = outputData.split("=")
				if(deviceResponse.length > 1){
					if(deviceResponse[1]){
						outputArray =  deviceResponse[1].split(',')
						if(outputArray.length > 0 ){
							for(int i=0; i<outputArray.length; i++){
								if(outputArray[i] != "<incomplete>" && outputArray[i] != "" && outputArray[i] != " "){									
									if(outputArray[i] != "\""){
										macIdList << outputArray[i]
									}																										
								}
							}
						}
					}
				}
			}
		}		
		return macIdList
	}


	/**
	 * Method to execute callsetroute.py script with required parameters.
	 * It will return execution result of callsetroute.py.
	 * 
	 * eg: python callsetroute.py 192.168.160.130 8088 b4:f2:e8:de:1b:0e 10001 20001 30001
	 * @param device
	 * @return outputData
	 */
	def executeSetRoute(final Device parentDevice, final Device childDevice){

		def outputData
		def absolutePath
		def deviceIP = parentDevice?.stbIp
		def devicePort = parentDevice?.statusPort
		def clientMAC
		def clientAgentPort
		def clientStatusPort
		def clientLogTransferPort
		def clientAgentMonitorPort

		clientMAC = childDevice?.macId
		clientAgentPort = childDevice?.stbPort
		clientStatusPort = childDevice?.statusPort
		clientLogTransferPort = childDevice?.logTransferPort
		clientAgentMonitorPort = childDevice?.agentMonitorPort

		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callsetroute.py").file
		absolutePath = layoutFolder.absolutePath

		try {
			if(clientMAC != null && clientAgentPort != null && clientStatusPort != null && clientLogTransferPort != null && 
					clientAgentMonitorPort  != null ){
				String[] cmd = [
				                PYTHON_COMMAND,
				                absolutePath,
				                deviceIP,
				                devicePort,
				                clientMAC,
				                clientAgentPort,
				                clientStatusPort,
				                clientLogTransferPort,
				                clientAgentMonitorPort
				                ]
				                		
				                		ScriptExecutor scriptExecutor = new ScriptExecutor()
				outputData = scriptExecutor.executeScript(cmd,1)
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
	/**
	 * Method to update the execution report for each test script execution.
	 * This method will update the ExecutionResult and Execution tables with new execution output.
	 * 
	 * @param outputData
	 * @param executionResultId
	 * @param executionId
	 * @param timeDiff
	 */
	public void updateExecutionResults(final String outputData, final long executionResultId, final long executionId, final long executionDeviceId, 
		final String timeDiff, final String singleScriptExecTime){
		ExecutionResult executionResult = ExecutionResult.findById(executionResultId)
		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput, c.executionTime = :newTime  where c.id = :execId",
				[newOutput: outputData, newTime: singleScriptExecTime, execId: executionResultId])		
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.executionTime = :newTime where c.id = :execId",
				[newStatus: outputData, newTime: timeDiff, execId: executionId.toLong()])
		ExecutionDevice.executeUpdate("update ExecutionDevice c set c.executionTime = :newTime where c.id = :execDevId",
				[newTime: timeDiff, execDevId: executionDeviceId.toLong()])		
	}
	
	public void updateExecutionStatus(final String status, final long executionId){
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus where c.id = :execId",
				[newStatus: status, execId: executionId.toLong()])
	}
	public def  getExecutionStatus(def executionId){
		def status = ""
		try {
			Execution.withTransaction {
			String statusData = Execution.executeQuery("select result from Execution  where id = :execId",[execId : executionId ]);
			if(statusData?.contains("SUCCESS")){
				status = "SUCCESS"
				}else if(statusData?.contains("FAILURE")){
					status = "FAILURE"
				}else{
					if(statusData.contains("[")){
						status = statusData.substring(statusData.indexOf("[")+1, statusData.indexOf("]"))
					}else{
						status = statusData
					}
				}
			}
		} catch (Exception e) {
			println " ERROR HERE "+e.getMessage()
			e.printStackTrace()
		}
		return status
	} 
	public void updateExecutionSkipStatusWithTransaction(final String status, final long executionId){
		Execution.withTransaction {
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.result = :reslt where c.id = :execId",
				[newStatus: status, reslt: status, execId: executionId.toLong()])
		}
	}
	
	public void updateExecutionDeviceSkipStatusWithTransaction(final String status, final long executionId){
		ExecutionDevice.withTransaction {
		ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStat where c.id = :execDevId",
				[newStat: status, execDevId: executionId])
		}
	}
	
	public void updateExecutionTime(final String totalTime, final long executionResultId){
		ExecutionResult.executeUpdate("update ExecutionResult c set c.totalExecutionTime = :time where c.id = :execId",
				[time: totalTime, execId: executionResultId])
	}
	
	public void updateTotalExecutionTime(final String totalTime, final long executionId){
		Execution.executeUpdate("update Execution c set c.realExecutionTime = :time where c.id = :execId",
				[time: totalTime, execId: executionId])
	}
	
	
	public void updateExecutionStatusData(final String status, final long executionId){
		Execution.withTransaction {
		Execution.executeUpdate("update Execution c set c.executionStatus = :newStatus where c.id = :execId",
				[newStatus: status, execId: executionId.toLong()])
		}
	}
	
	/**
	 * Method to update the execution report for each test script execution.
	 * This method will update the ExecutionResult and Execution tables with new execution output.
	 *
	 * @param outputData
	 * @param executionResultId
	 * @param executionId
	 * @param timeDiff
	 */
	public void updateExecutionResultsTimeOut(final String outputData, final long executionResultId, final long executionId, final long executionDeviceId, 
		final def timeDiff, final String singleScriptExecTime){
		try{
		ExecutionResult executionResult = ExecutionResult.findById(executionResultId)
		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput , c.status = :newStatus, c.executionTime = :newTime where c.id = :execId",
				[newOutput: outputData, newStatus: "SCRIPT TIME OUT", newTime: singleScriptExecTime, execId: executionResultId])
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus,  c.result = :newStatus, c.executionTime = :newTime where c.id = :execId",
				[newStatus: outputData, newStatus: "FAILURE", newTime: timeDiff, execId: executionId.toLong()])
		ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStat, c.executionTime = :newTime where c.id = :execDevId",
				[newStat: "FAILURE", newTime: timeDiff, execDevId: executionDeviceId.toLong()])
		}
		catch(Exception e){
			e.printStackTrace()
		}
	}
	
	/**
	 * Method to update the execution report for each test script execution.
	 * This method will update the ExecutionResult and Execution tables with new execution output.
	 *
	 * @param outputData
	 * @param executionResultId
	 * @param executionId
	 * @param timeDiff
	 */
	public void updateExecutionResultsError(final String resultData,final long executionResultId, final long executionId, final long executionDeviceId,
		final String timeDiff, final String singleScriptExecTime){
		ExecutionResult executionResult = ExecutionResult.findById(executionResultId)
		ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput, c.status = :newStatus, c.executionTime = :newTime where c.id = :execId",
				[newOutput: resultData, newStatus: "FAILURE", newTime: singleScriptExecTime, execId: executionResultId])
		Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.executionTime = :newTime, c.result = :newStatus where c.id = :execId",
				[newStatus: resultData, newTime: timeDiff, newStatus: "FAILURE", execId: executionId.toLong()])
		ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStat, c.executionTime = :newTime where c.id = :execDevId",
				[newStat: "FAILURE", newTime: timeDiff, execDevId: executionDeviceId.toLong()])
		
	}
	
	def Groups getGroup(){
		def user = User.findByUsername(SecurityUtils.subject.principal)
		def group = Groups.findById(user?.groupName?.id)
		return group
	}
	
	/**
	 * Method saving the multiple scripts execution details
	 *
	 * @param realPath
	 * @param execName
	 * @param scriptName
	 * @param deviceName
	 * @param scriptGroupInstance
	 * @param appUrl
	 * @param isBenchMark
	 * @param isSystemDiagnostics
	 * @param rerun
	 * @param isLogReqd
	 * @param scriptCount
	 * @return
	 */
	public boolean saveExecutionDetailsOnMultipleScripts(final String execName, String scriptName, String deviceName,
		String scriptGroupInstance , String appUrl,String isBenchMark , String isSystemDiagnostics,String rerun,String isLogReqd, final int scriptCount, final String category, final String rerunOnFailure){
		   def executionSaveStatus = true
		   try {
			   Execution execution = new Execution()
			   execution.name = execName
			   execution.script = scriptName
			   execution.device = deviceName
			   execution.scriptGroup = scriptGroupInstance
			   execution.result = UNDEFINED_STATUS
			   execution.executionStatus = INPROGRESS_STATUS
			   execution.dateOfExecution = new Date()
			   execution.groups = getGroup()
			   execution.applicationUrl = appUrl
			   execution.isRerunRequired = rerun?.equals("true")
			   execution.isBenchMarkEnabled = isBenchMark?.equals("true")
			   execution.isStbLogRequired = isLogReqd?.equals("true")
			   execution.isSystemDiagnosticsEnabled = isSystemDiagnostics?.equals("true")
			   execution.rerunOnFailure=rerunOnFailure?.equals("true") 
			   execution.scriptCount = scriptCount
			   execution.category = Utility.getCategory(category)
			   if(! execution.save(flush:true)) {
				   log.error "Error saving Execution instance : ${execution.errors}"
				   executionSaveStatus = false
			   }
		   }
		   catch(Exception th) {
			   th.printStackTrace()
			   executionSaveStatus = false
		   }
		   return executionSaveStatus
	   }
	
		/**
		 * Method to save details of execution in Execution Domain For Multiple ScriptGroup execution
		 * @param execName
		 * @param scriptName
		 * @param deviceName
		 * @param scriptGroupInstance
		 * @return
		 */
		/*public boolean saveExecutionDetails(final String execName, String scriptName, String deviceName,
		 ScriptGroup scriptGroupInstance , String appUrl,String isBenchMark , String isSystemDiagnostics,String rerun,String isLogReqd){*/
		public boolean saveExecutionDetailsOnMultipleScriptgroups(final String execName, def map){
			def executionSaveStatus = true
			try {
				Execution execution = new Execution()
				execution.name = execName
				execution.script = null
				execution.scriptGroup = map.scriptName
				execution.device = map.deviceName
				execution.result = UNDEFINED_STATUS
				execution.executionStatus = INPROGRESS_STATUS
				execution.dateOfExecution = new Date()
				if(map.containsKey("groups")){
					execution.groups = map.groups
				}
				else{
					execution.groups = getGroup()
				}
				execution.applicationUrl = map.appUrl
				execution.isRerunRequired = map.rerun?.equals("true")
				execution.isBenchMarkEnabled = map.isBenchMark?.equals("true")
				execution.isStbLogRequired = map.isLogReqd?.equals("true")
				execution.isSystemDiagnosticsEnabled = map.isSystemDiagnostics?.equals("true")
				execution.rerunOnFailure= map.rerunOnFailure?.equals("true")
				execution.scriptCount = map.scriptCount
				execution.category = Utility.getCategory(map.category)
				if(! execution.save(flush:true)) {
					log.error "Error saving Execution instance : ${execution.errors}"
					executionSaveStatus = false
				}
			}
			catch(Exception th) {
				th.printStackTrace()
				executionSaveStatus = false
			}
			return executionSaveStatus
		}
	
	
	
	
	
	/**
	 * Method to save details of execution in Execution Domain
	 * @param execName
	 * @param scriptName
	 * @param deviceName
	 * @param scriptGroupInstance
	 * @return
	 */
	/*public boolean saveExecutionDetails(final String execName, String scriptName, String deviceName,
	 ScriptGroup scriptGroupInstance , String appUrl,String isBenchMark , String isSystemDiagnostics,String rerun,String isLogReqd){*/
	public boolean saveExecutionDetails(final String execName, def map){
		def executionSaveStatus = true
		int scriptCnt = 0
	/*	if(map?.scriptGroupInstance?.scriptList?.size() > 0){
			scriptCnt = map.scriptGroupInstance?.scriptList?.size()
		} */		
		try {
			ScriptGroup.withTransaction {
				def scriptGroupInstance1 = ScriptGroup.get(map.scriptGroupInstance?.id)
				if(scriptGroupInstance1?.scriptList?.size() > 0){
					scriptCnt = scriptGroupInstance1?.scriptList?.size()
				}
			}
			Execution execution = new Execution()
			execution.name = execName
			if(map.scriptName == MULTIPLESCRIPTGROUPS){
				execution.script = null
				execution.scriptGroup = map.scriptName
			}else{
			    execution.script = map.scriptName
				execution.scriptGroup = map.scriptGroupInstance?.name
			}
			execution.device = map.deviceName
			execution.result = UNDEFINED_STATUS
			execution.executionStatus = INPROGRESS_STATUS
			execution.dateOfExecution = new Date()
			if(map.containsKey("groups")){
				execution.groups = map.groups
			}
			else{
				execution.groups = getGroup()
			}
			execution.applicationUrl = map.appUrl
			execution.isRerunRequired = map.rerun?.equals("true")
			execution.isBenchMarkEnabled = map.isBenchMark?.equals("true")
			execution.isStbLogRequired = map.isLogReqd?.equals("true")
			execution.isSystemDiagnosticsEnabled = map.isSystemDiagnostics?.equals("true")
			execution.rerunOnFailure= map.rerunOnFailure?.equals("true")			
			execution.scriptCount = scriptCnt
			execution.category = Utility.getCategory(map.category)
			if(! execution.save(flush:true)) {				
				log.error "Error saving Execution instance : ${execution.errors}"
				executionSaveStatus = false
			}
		}
		catch(Exception th) {
			th.printStackTrace()
			executionSaveStatus = false
		}
		return executionSaveStatus
	}
	 
	 public void saveRepeatExecutionDetails(String execName , String deviceName , int currentExecutionCount, int pending, String category){
		 
		try {
			Execution exe = Execution.findByName(execName)
			RepeatPendingExecution.withTransaction{
				RepeatPendingExecution rExecution = new RepeatPendingExecution()
				rExecution.deviceName = deviceName
				rExecution.completeExecutionPending = pending
				rExecution.currentExecutionCount = currentExecutionCount
				rExecution.executionName = execName
				rExecution.category = Utility.getCategory(category)
				rExecution.status = "PENDING"
				if(!rExecution.save(flush:true)){
				}
			}

		} catch (Exception e) {
		
			 e.printStackTrace()
		 }
	 }
	 
	public void setPerformance(final Execution executionInstance, final String filePath){
		try{
			Execution execution = executionInstance
			def executionDevice = ExecutionDevice.findAllByExecution(executionInstance)
			def executionResult
			def benchmarkPerformanceFile
			def memoryPerfomanceFile
			def cpuPerformanceFile
			Performance performanceInstance
			def stringArray
			executionDevice.each{ executiondevice ->
				executionResult = ExecutionResult.findAllByExecutionDevice(executiondevice)
				executionResult.each { executionresult ->
					benchmarkPerformanceFile = new File(filePath+"//logs//performance//${executionInstance?.id}//${executiondevice?.id}//${executionresult?.id}//benchmark.log")
					cpuPerformanceFile = new File(filePath+"//logs//performance//${executionInstance?.id}//${executiondevice?.id}//${executionresult?.id}//cpu.log")
					memoryPerfomanceFile = new File(filePath+"//logs//performance//${executionInstance?.id}//${executiondevice?.id}//${executionresult?.id}//memused.log")
					if(memoryPerfomanceFile.exists() || cpuPerformanceFile.exists() || benchmarkPerformanceFile.exists()){
						execution.isPerformanceDone = true
						execution.save(flush:true)
					}
					if(benchmarkPerformanceFile.exists()){
						int count = 0
						benchmarkPerformanceFile?.eachLine { line ->
							if(!line?.isEmpty()){
								if(count < 6){
									stringArray = line.split("~")
									if(stringArray.size() >= 2){
										if(stringArray[0] && stringArray[1]){
											performanceInstance = new Performance()
											performanceInstance.executionResult = executionresult
											performanceInstance.performanceType = "BENCHMARK"
											performanceInstance.processName = stringArray[0].trim()
											performanceInstance.processValue = stringArray[1].trim()
											performanceInstance.category = execution.category
											performanceInstance.save(flush:true)
											executionresult.addToPerformance(performanceInstance)
										}
									}
								}
								count++;
							}
						}
						benchmarkPerformanceFile.delete()
					}
					if(cpuPerformanceFile.exists()){
						
						List cpuValue = []
						cpuPerformanceFile?.eachLine { line ->
							if(!line?.isEmpty()){
								String input = line?.trim() 
								try {
									float val = Float.parseFloat(input)
									cpuValue.add(100.00 - val)
								} catch (Exception e) {
									e.printStackTrace()
								}
							}
						}
						
						float starting = cpuValue.first()
						float ending = cpuValue.last()
						float sumVal = cpuValue.sum()
						float avg = sumVal / cpuValue.size()
						cpuValue = cpuValue?.sort()
						float peak = cpuValue?.last() 
						
						addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_CPU, Constants.CPU_STARTING, starting)
						addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_CPU, Constants.CPU_ENDING, ending)
						addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_CPU, Constants.CPU_AVG, avg)
						addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_CPU, Constants.CPU_PEAK, peak)
						
						cpuPerformanceFile?.delete()
					}
					if(memoryPerfomanceFile?.exists()){
						memoryFileParser(memoryPerfomanceFile,executionresult)
						memoryPerfomanceFile?.delete()
					}
				}
				
				

			}
			new File(filePath+"//logs//performance//${executionInstance?.id}")?.deleteDir()
		}catch(Exception e){
				e.printStackTrace()
			try{
				new File(filePath+"//logs//performance//${executionInstance?.id}")?.deleteDir()
			}catch(Exception ex){
			}

		}
	}	
	
	public void saveSkipStatus(def executionInstance , def executionDevice , def scriptInstance , def deviceInstance,def category){
		ExecutionResult.withTransaction { resultstatus ->
			try {
				ExecutionResult executionResult = new ExecutionResult()
				executionResult.execution = executionInstance
				executionResult.executionDevice = executionDevice
				executionResult.script = scriptInstance.name
				executionResult.device = deviceInstance.stbName
				executionResult.dateOfExecution = new Date()
				executionResult.status = SKIPPED_STATUS
				executionResult.category = Utility.getCategory(category)
				executionResult.executionOutput = "Test skipped , Reason :"+scriptInstance.remarks
				if(! executionResult.save(flush:true)) {
					log.error "Error saving executionResult instance : ${executionResult.errors}"
				}
				resultstatus.flush()
			}
			catch(Throwable th) {
				resultstatus.setRollbackOnly()
			}
		}
		
		try {
			Execution.withTransaction {
				Execution execution = Execution.findById(executionInstance?.id)
						if(!execution.result.equals( FAILURE_STATUS )){
							execution.result = FAILURE_STATUS
									execution.save(flush:true)
						}
			}
			
			ExecutionDevice.withTransaction {
				ExecutionDevice execDeviceInstance = ExecutionDevice.findById(executionDevice?.id)
						if(!execDeviceInstance.status.equals( FAILURE_STATUS )){
							execDeviceInstance.status = FAILURE_STATUS
									execDeviceInstance.save(flush:true)
						}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
	public void saveNotApplicableStatus(def executionInstance , def executionDevice , def scriptInstance , def deviceInstance, String reason, def category){
		try{
		ExecutionResult.withTransaction { resultstatus ->
			try {
				ExecutionResult executionResult = new ExecutionResult()
				executionResult.execution = executionInstance
				executionResult.executionDevice = executionDevice
				executionResult.script = scriptInstance?.name
				executionResult.device = deviceInstance?.stbName
				executionResult.status = Constants.NOT_APPLICABLE_STATUS
				executionResult.dateOfExecution = new Date()
				executionResult.category = Utility.getCategory(category)
				executionResult.executionOutput = "Test not executed. Reason : "+reason
				if(! executionResult.save(flush:true)) {
					log.error "Error saving executionResult instance : ${executionResult.errors}"
				}
				resultstatus.flush()
			}
			catch(Throwable th) {
				resultstatus.setRollbackOnly()
			}
		}
		}catch(Exception ee){
		}
	}
	
	public void saveNoScriptAvailableStatus(def executionInstance , def executionDevice , def scriptName , def deviceInstance, String reason, def category){
		try{
		ExecutionResult.withTransaction { resultstatus ->
			try {
				ExecutionResult executionResult = new ExecutionResult()
				executionResult.execution = executionInstance
				executionResult.executionDevice = executionDevice
				executionResult.script = scriptName
				executionResult.device = deviceInstance?.stbName
				executionResult.status = Constants.SKIPPED_STATUS
				executionResult.dateOfExecution = new Date()
				executionResult.executionOutput = "Test not executed. Reason : "+reason
				executionResult.category = Utility.getCategory(category)
				if(! executionResult.save(flush:true)) {
					log.error "Error saving executionResult instance : ${executionResult.errors}"
				}
				resultstatus.flush()
			}
			catch(Throwable th) {
				resultstatus.setRollbackOnly()
			}
		}
		}catch(Exception ee){
		}
	}
	
	public boolean isAborted(def executionName){
		Execution.withTransaction {
			def ex = Execution.findByName(executionName)
			if(ex){
				return ex?.isAborted
			}
		}
		return false;
	}
	
	public void abortExecution(def executionId){
		Long exId = Long.parseLong(""+executionId)
		try {
			Execution.withTransaction {
				Execution.executeUpdate("update Execution c set c.executionStatus = :newStatus , c.isAborted = :abort where c.id = :execId",
						[newStatus: ABORTED_STATUS, abort: true, execId: exId?.toLong()])
			}
		} catch (Exception e) {
		}

	}
	
	public void saveExecutionStatus(boolean isAborted, def exId){
				
		String status = ""
		if(isAborted){
			status = ABORTED_STATUS
		}else{
			status = COMPLETED_STATUS
		}
		try {
			Execution.executeUpdate("update Execution c set c.executionStatus = :newStatus , c.isAborted = :abort where c.id = :execId",
					[newStatus: status, abort: isAborted, execId: exId?.toLong()])

		} catch (Exception e) {
			e.printStackTrace()
		}

	}
	
	public void saveExecutionDeviceStatus(boolean isAborted, def exDevId){

		String status = ""
		if(isAborted){
			status = ABORTED_STATUS
		}else{
			status = COMPLETED_STATUS
		}
		try {
			ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStatus  where c.id = :execId",
					[newStatus: status, abort: isAborted, execId: exDevId?.toLong()])

		} catch (Exception e) {
			e.printStackTrace()
		}

}
	
	public void savePausedExecutionStatus(def exId){
		try {
			Execution.executeUpdate("update Execution c set c.executionStatus = :newStatus where c.id = :execId",
					[newStatus: "PAUSED", execId: exId?.toLong()])

		} catch (Exception e) {
			e.printStackTrace()
		}

}
	
	public void saveExecutionDeviceStatusData(String status, def exDevId){
		
				try {
					ExecutionDevice.executeUpdate("update ExecutionDevice c set c.status = :newStatus  where c.id = :execId",
							[newStatus: status, execId: exDevId?.toLong()])
		
				} catch (Exception e) {
					e.printStackTrace()
				}
		
		}
	
	/**
	 * Refreshes the status in agent as it is called with flag false
	 * @param deviceInstance
	 * @return
	 */
	def resetAgent(def deviceInstance,String hardReset){
		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
		def absolutePath = layoutFolder.absolutePath
		String[] cmd = [
			PYTHON_COMMAND,
			absolutePath,
			deviceInstance?.stbIp,
			deviceInstance?.agentMonitorPort,
			hardReset
		]
		ScriptExecutor scriptExecutor = new ScriptExecutor()
		def resetExecutionData = scriptExecutor.executeScript(cmd,1)
		callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
		Thread.sleep(4000)
	}
	
	/**
	 * Refreshes the status in agent as it is called with flag false
	 * @param deviceInstance
	 * @return
	 */
	def resetAgent(def deviceInstance){
		try {
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callResetAgent.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.agentMonitorPort,
				FALSE
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def resetExecutionData = scriptExecutor.executeScript(cmd,1)
			callRebootOnAgentResetFailure(resetExecutionData, deviceInstance)
			Thread.sleep(4000)
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
	
	/**
	 * Method to check whether the agent reset failed. If the agent reset failed it will request to reboot the box.
	 * @param output
	 * @param device
	 * @return
	 */
	def callRebootOnAgentResetFailure(String output,Device device){
		if(output?.contains("Failed to reset agent") || output?.contains("Unable to reach agent")){
			rebootBox(device)
		}
	}
	
	/**
	 * Method to reboot the box by invoking the python script.
	 * @param deviceInstance
	 * @return
	 */
	def rebootBox(Device deviceInstance ){
		println "Reboot Box "+deviceInstance
		try {
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//callRebootOnCrash.py").file
			def absolutePath = layoutFolder.absolutePath
			String[] cmd = [
				PYTHON_COMMAND,
				absolutePath,
				deviceInstance?.stbIp,
				deviceInstance?.stbPort
			]
			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def resetData = scriptExecutor.executeScript(cmd,1)
			Thread.sleep(10000)
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
	def memoryFileParser(File memFile, def executionresult){
		def memUsed = []
		def memAvailable = []
		def memPer = []
		
		memFile?.eachLine { line ->
			StringTokenizer st = new StringTokenizer(line)
			if(st.countTokens() == 3){
				memAvailable.add(getLongValue(st?.nextToken()))
				memUsed.add(getLongValue(st?.nextToken()))
				memPer.add(getFloatValue(st?.nextToken()))
			}
		}
		
		try {
			
			
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_USED_START, memUsed.first())
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_USED_END, memUsed.last())
			memUsed = memUsed?.sort()
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_USED_PEAK, memUsed.last())
			
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_AVAILABLE_START, memAvailable.first())
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_AVAILABLE_END, memAvailable.last())
			memAvailable = memAvailable?.sort()
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_AVAILABLE_PEAK, memAvailable.last())
			
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_PERC_START, memPer.first())
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_PERC_END, memPer.last())
			memPer = memPer?.sort()
			addPerformanceParam(executionresult, Constants.SYSTEMDIAGNOSTICS_MEMORY, Constants.MEMORY_PERC_PEAK, memPer.last())
			
		} catch (Exception e) {
		println " ERROR >>> "+e.getMessage() + "ee "+e.getCause()
			e.printStackTrace()
		}
		
		
		
	}
	
	def getLongValue(String val){
		try {
			return Long.parseLong(val)
		} catch (Exception e) {
			e.printStackTrace()
		}
		return 0
	}
	
	def getFloatValue(String val){
		try {
			return Float.parseFloat(val)
		} catch (Exception e) {
			e.printStackTrace()
		}
		return 0.0
	}
	
	def addPerformanceParam(def executionresult , def performanceType , def processName , def value){
		Performance performanceInstance = new Performance()
		performanceInstance.executionResult = executionresult
		performanceInstance.performanceType = performanceType
		performanceInstance.processName = processName
		performanceInstance.processValue = value
		performanceInstance.category = executionresult.category
		performanceInstance.save(flush:true)
		executionresult.addToPerformance(performanceInstance)
	}
	boolean isOlderExecutionValid(Date now, Date prev){
		try {
			int daysDiff = (int)(((now?.getTime()  - prev?.getTime())) / (1000*60*60*24l));
			if (daysDiff <= 10){
				return true
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		return false
	}
	
	def handleInprogressExecutionOnStartup(){
		try {
			String device
			String exName
			int scriptGrpSize = 0
			def scriptGroupInstance
			def scriptGrp
			def execInstance
			def deviceInstanceObj
			def executionStatus = Execution.findAllByExecutionStatus(INPROGRESS_STATUS)
			Date now = new Date()
			executionStatus.each { execution ->
				List validScriptsList = new ArrayList()
				if (isOlderExecutionValid(now, execution?.dateOfExecution)){
					exName = execution?.name
					device =execution?.device?.toString()
					def deviceInstance = Device?.findByStbName(device)
					scriptGrp =execution?.scriptGroup
					if( scriptGrp != null){
						def scriptGrpName= ScriptGroup.findByName(scriptGrp)
						def scriptGrpScriptList = scriptGrpName?.scriptList
						//scriptGrpScriptList?.scriptName.each{scriptName-> validScriptsList << scriptName }
						execInstance = Execution.findByName(exName)
						deviceInstanceObj = Device.findById(deviceInstance?.id)
						def excutionDev=ExecutionDevice.findByExecution(execution)
						def execResult =ExecutionResult.findAllByExecution(execution)
						def executionResultList
						def notExecutedScripts = []
						def actualExecutedScript = []
						if(exName.contains("_RERUN_")){ 
							ExecutionResult.withTransaction {
								executionResultList = ExecutionResult.findAllByExecutionAndExecutionDeviceAndStatusNotEqual(execInstance,excutionDev,SUCCESS_STATUS)
							}
							executionResultList.each{ executionResultInstance ->
								if((executionResultInstance?.status.equals("FAILURE")) || (executionResultInstance?.status.equals("SCRIPT TIME OUT"))){
									notExecutedScripts.add(executionResultInstance?.script)
								}
							}
							int execCount
							def exNameSplitList =  exName?.split("_RERUN_")
							def previousExecName
							execCount = Integer?.parseInt(exNameSplitList[1])
							if(execCount?.toString()?.equals("1")){
								previousExecName = exNameSplitList[0]?.toString()
							} else {
								execCount= execCount - 1
								previousExecName  = exNameSplitList[0]+"_RERUN_"+execCount?.toString()
							}
							def  executionInstance =  Execution?.findByName(previousExecName?.toString())
							def exResultList = ExecutionResult?.findAllByExecutionAndStatusNotEqual(executionInstance,SUCCESS_STATUS)
							exResultList?.each{obj->
								if((obj?.status.equals("FAILURE")) || (obj?.status.equals("SCRIPT TIME OUT"))){
									if(!(notExecutedScripts?.toString()?.contains(obj?.script))){
										validScriptsList.add(obj?.script)
									}
								}
							}
						}else {
							scriptGrpScriptList?.scriptName.each{scriptName-> validScriptsList << scriptName }
							execResult?.script?.each{ result ->
								if(validScriptsList?.contains(result)){
									validScriptsList.remove(result)
								}
							}
						}				
						validScriptsList?.each{ script ->
							ExecutionResult?.withTransaction { resultstatus ->
								try {
									def executionResult = new ExecutionResult()
									executionResult.execution = execInstance
									executionResult.executionDevice = excutionDev
									executionResult.script = script
									executionResult.device = deviceInstance
									executionResult.execDevice = null
									executionResult.deviceIdString = deviceInstanceObj?.id?.toString()
									executionResult.status = "PENDING"
									executionResult.dateOfExecution = new Date()// for new 
									executionResult.category =Utility.getCategory(deviceInstance?.category?.toString())
									if(!executionResult.save(flush:true)) {
										println "error"+executionResult?.errors
									}
									resultstatus.flush()
								}
								//catch(Throwable th) {
								//	resultstatus.setRollbackOnly()
							//	}
								catch(Exception e){
									println e.getMessage()
								}
							}
						}
						if(scriptGrp ){
							savePausedExecutionStatus(execution?.id)
							saveExecutionDeviceStatusData("PAUSED", excutionDev?.id)
						}
					}else{
						saveExecutionStatus(true, execution?.id)
					}
				}else{
					saveExecutionStatus(true, execution?.id)
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
	def getCurrentTime(){
		SimpleDateFormat format = new SimpleDateFormat("dd-MMM-yyyy HH:mm:ss")
		String timeString = format.format(new Date())
		return timeString
	}
	
	public void updateTclExecutionResults(def params){
		try { 
			
			//updateExecutionResults(params.outputData, params.execResult,  params.execId, params.execDevice, params.timeDiff, params.singleScriptExecTime)
			
			
			//updateExecutionResults(final String outputData, final long executionResultId, final long executionId, final long executionDeviceId,
			//	final String timeDiff, final String singleScriptExecTime)
			
			/*ExecutionResult executionResult2 = ExecutionResult.findById(params.execResult)
			ExecutionResult.executeUpdate("update ExecutionResult c set c.executionOutput = :newOutput, c.executionTime = :newTime  where c.id = :execId",
					[newOutput: params.outputData, newTime: params.singleScriptExecTime, execId: params.execResult])
			Execution.executeUpdate("update Execution c set c.outputData = :newStatus , c.executionTime = :newTime, c.result = :result where c.id = :execId",
					[newStatus: params.outputData, newTime: params.timeDiff, result:params.resultStatus, execId: params.execId.toLong()])
			ExecutionDevice.executeUpdate("update ExecutionDevice c set c.executionTime = :newTime where c.id = :execDevId",
					[newTime: params.timeDiff, execDevId: params.execDevice.toLong()])*/
			
			            
			/*Execution.withTransaction{
				Execution execution = Execution.findById(params.execId)
				
						if(execution && !(execution?.result?.equals( FAILURE_STATUS ))){
							execution?.result = params.statusData?.toUpperCase().trim()
									execution?.save(flush:true)
						}
				
				ExecutionDevice execDeviceInstance = ExecutionDevice.findByExecutionAndId(execution,params.execDeviceId)
						if(execDeviceInstance && !(execDeviceInstance?.status.equals( FAILURE_STATUS ))){
							execDeviceInstance?.status = params.statusData?.toUpperCase().trim()
									execDeviceInstance?.save(flush:true)
						}
				
				ExecutionResult executionResult = ExecutionResult.findById(params.execResult)
						if(executionResult && !(executionResult?.status.equals( FAILURE_STATUS ))){
							executionResult?.status = params.statusData?.toUpperCase().trim()
									executionResult?.save(flush:true)
					}
			}*/
		
				String actualResult = params.resultData
				if(actualResult){
					ExecutionResult.withTransaction {
						ExecutionResult executionResult = ExecutionResult.findById(params.execResult)
						if(executionResult){
							ExecuteMethodResult executionMethodResult = new ExecuteMethodResult()
							if(params.resultStatus?.equals( STATUS_NONE ) || params.resultStatus == null ){
								executionMethodResult.status = actualResult
							}
							else{
								executionMethodResult.executionResult = executionResult
								executionMethodResult.expectedResult = params.expectedResult
								executionMethodResult.actualResult = actualResult
								executionMethodResult.status = params.resultStatus
							}
							executionMethodResult.functionName = params.testCaseName
							executionMethodResult.category = executionResult?.category
							executionMethodResult.save(flush:true)
	 
							executionResult?.addToExecutemethodresults(executionMethodResult)
							executionResult.executionOutput = params.outputData
							executionResult.executionTime = params.singleScriptExecTime
							executionResult?.save(flush:true)
	 
							Execution execution = Execution.findById(params.execId)
							ExecutionDevice execDeviceInstance = ExecutionDevice.findById(params.execDevice)
							if(!executionResult?.status.equals( FAILURE_STATUS )){
								executionResult?.status = params.resultStatus
								executionResult?.save(flush:true)
								String status = getExecutionStatus(params.execId)
								if(!status.equals( FAILURE_STATUS )){
									execution.result = params.resultStatus
									execution.outputData = params.outputData
									execution.executionTime = params.singleScriptExecTime
									execution.save(flush:true)
								}
								if(!execDeviceInstance.status.equals( FAILURE_STATUS )){
									execDeviceInstance?.addToExecutionresults(executionResult)
									execDeviceInstance?.status = params.resultStatus
									execDeviceInstance.executionTime = params.singleScriptExecTime
									execDeviceInstance?.save(flush:true)
								}
							}
						}
					}
				}
		}catch(Exception ex){
			ex.printStackTrace()
		}
	}
	
	/**
	 * Function for start up the  tftp server in Test manager side
	 * @return
	 */
	
	def tftpServerStartUp(def realPath){
		try{
			def filePath = realPath?.toString()+"/fileStore/"
			String fileName = realPath?.toString()+"/fileStore/tftp_server.py"
			File file = new File(fileName)
			boolean value=file.setExecutable(true)

			String logFilePath = realPath+"/logs/logs/"
			File logdir = new File(logFilePath)

			try {
				if(!logdir?.exists()){
					logdir?.mkdirs()
				}
			} catch (Exception e) {
				e.printStackTrace()
			}

			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//tftp_server.py").file
			def absolutePath = layoutFolder.absolutePath
			

			
			Thread.start{	
				//log.info("TDK TM : Starting TFTP Server...");
				println "TDK TM : Starting TFTP Server..."
				try {
					def outputData					
					if(absolutePath != null){
						
						String[] cmdd = [
							"sudo",
							PYTHON_COMMAND,
							absolutePath,
							"69",
							logFilePath
						]

						Process process = null;
						try {
							ProcessBuilder processBuilder = new ProcessBuilder(cmdd);
							process = processBuilder.start();
							InputStream inputStream = process.getInputStream();
							setUpStreamGobbler(inputStream, System.out);

							InputStream errorStream = process.getErrorStream();
							setUpStreamGobbler(errorStream, System.err);
							System.out.println("never returns");
							tftpProcess = process
						   
							process.waitFor();
						} catch (IOException e) {
							throw new RuntimeException(e);
						} catch (InterruptedException e) {
							throw new RuntimeException(e);
						}
					}

				} catch (Exception e) {
					e.printStackTrace()
				}
			}

		}catch(Exception e){
			println e.getMessage()
			e.printStackTrace()
		}
	}
	

 public static void setUpStreamGobbler(final InputStream is, final PrintStream ps) {
	final InputStreamReader streamReader = new InputStreamReader(is);
	new Thread(new Runnable() {
	   public void run() {
		  BufferedReader br = new BufferedReader(streamReader);
		  String line = null;
		  try {
			 while ((line = br.readLine()) != null) {
				ps.println("process stream: " + line);
			 }
		  } catch (IOException e) {
			 e.printStackTrace();
		  } finally {
			 try {
				br.close();
			 } catch (IOException e) {
				e.printStackTrace();
			 }
		  }
	   }
	}).start();
 }
  /**
  * Function for updating the TM ip[ipv6, ipv4] according to the  device selection
  * @param url
  * @param device
  * @return
  */ 
	def updateTMUrl(String url,Device device){
		try {
			if(InetUtility.isIPv6Address(device?.stbIp) && device?.category?.equals(Category.RDKV)){
				File configFile = grailsApplication.parentContext.getResource("/fileStore/tm.config").file
						String ipV6Address = InetUtility.getIPAddress(configFile, Constants.IPV6_INTERFACE)
						String ipV4Address = InetUtility.getIPAddress(configFile, Constants.IPV4_INTERFACE)
						if(ipV4Address &&ipV6Address && !ipV4Address.isEmpty() && !ipV6Address.isEmpty()){
							url = url.replace(ipV4Address, "[${ipV6Address}]")
						}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		return url
	}
	
	def getIPV4LogUploadMechanism(){
		String mechanism = Constants.TFTP_MECHANISM
		try {
			File configFile = grailsApplication.parentContext.getResource(Constants.TM_CONFIG_FILE).file
			mechanism = getConfigProperty(configFile, Constants.LOG_UPLOAD_IPV4)
		} catch (Exception e) {
			e.printStackTrace()
		}
		return mechanism
	}
 
	public static String getConfigProperty(File configFile, String key) {
		try {
			Properties prop = new Properties();
			if (configFile.exists()) {
				InputStream is = new FileInputStream(configFile);
				prop.load(is);
				String value = prop.getProperty(key);
				if (value != null && !value.isEmpty()) {
					return value;
				}
			}else{
				println "DBG :::: No Config File !!! "
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return null;
	}
 
	
}
