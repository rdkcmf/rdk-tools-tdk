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
import static org.quartz.CronScheduleBuilder.*
import static org.quartz.DateBuilder.*
import static org.quartz.JobKey.*
import static org.quartz.TriggerBuilder.*
import static org.quartz.TriggerKey.*
import grails.converters.JSON

import java.text.DateFormat
import java.text.SimpleDateFormat
import java.util.Map;
import java.util.date.*
import java.util.zip.ZipEntry
import java.util.zip.ZipOutputStream

import org.codehaus.groovy.grails.web.json.JSONObject
import org.codehaus.groovy.grails.web.json.JSONArray
import org.custommonkey.xmlunit.*
import org.quartz.JobBuilder
import org.quartz.JobDetail
import org.quartz.Trigger
import org.quartz.impl.triggers.SimpleTriggerImpl

import rdk.test.tool.*

import com.google.gson.Gson;
import com.google.gson.JsonArray
import com.google.gson.JsonObject
import org.codehaus.groovy.grails.validation.routines.InetAddressValidator;
import org.springframework.util.StringUtils;
/**
 * A class that handles the Execution of scripts.
 * @author sreejasuma
 */
class ExecutionController {

	def scriptexecutionService
	/**
	 * Injects quartz scheduler
	 */
	def quartzScheduler
	/**
	 * Injects the executionSerice.
	 */
	def executionService
	/**
	 * Injects the scriptService.
	 */
	def scriptService
	/**
	 * Injects the thunderService.
	 */
	def thunderService
	/**
	 * Injects the grailsApplication.
	 */
	def grailsApplication

	def utilityService

	def exportService   // Export service provided by Export plugin

	def deviceStatusService

	def primitivetestService

	def executedbService

	def executescriptService

	def tclExecutionService
	/**
	 * Injects the excelExportService
	 */
	def excelExportService
	
	/**
	 * Injects the service for downloading logs in Zip format.
	 */
	
	def logZipService

	public static volatile Object  lock = new Object()
	private static int execIdCounter = 0
	public static final String EXPORT_SCRIPT_LABEL 			= "Script"
	public static final String EXPORT_STATUS_LABEL 			= "Status"
	public static final String EXPORT_DEVICE_LABEL 			= "Device"
	public static final String EXPORT_DEVICE_DETAILS_LABEL 	= "Device Details"
	public static final String EXPORT_LOGDATA_LABEL			= "Log Data"
	public static final String EXPORT_FUNCTION_LABEL 		= "Function: "
	public static final String EXPORT_FUNCTION_STATUS_LABEL = "Function Status: "
	public static final String EXPORT_EXPECTED_RESULT_LABEL = "Expected Result: "
	public static final String EXPORT_ACTUAL_RESULT_LABEL 	= "Actual Result: "
	public static final String EXPORT_IPADDRESS_LABEL 		= "IP Address"
	public static final String EXPORT_EXECUTION_TIME_LABEL 	= "Time taken for execution(min)"
	public static final String EXPORT_COLUMN1_LABEL 		= "C1"
	public static final String EXPORT_COLUMN2_LABEL 		= "C2"
	public static final String EXPORT_SHEET_NAME 			= "Execution_Results"
	public static final String EXPORT_FILENAME 				= "ExecutionResults-"
	public static final String COMBINED_EXPORT_FILENAME 	= "CombinedExecutionResults-"
	public static final String COMPARISON_EXPORT_FILENAME 	= "ComparisonExecutionResults-"
	public static final String EXPORT_COMPARE_FILENAME 		= "ExecutionResultsComparison-"
	public static final String EXPORT_EXCEL_FORMAT 			= "excel"
	public static final String EXPORT_ZIP_FORMAT 			= "zip"
	public static final String EXPORT_EXCEL_EXTENSION 		= "xls"
	public static final String EXPORT_ZIP_EXTENSION 		= "zip"
	public static final String MARK_ALL_ID1 				= "markAll1"
	public static final String MARK_ALL_ID2 				= "markAll2"
	public static final String UNDEFINED					= "undefined"


	def index() {
		redirect(action: "create")
	}

	/**
	 * Method to unschedule a quartz job
	 */
	def unScheduleJob(){
		def countVariable = 0
		def jobDetailInstance
		if(params?.listCount){ // to delete record(s) from list.gsp
			for (iterateVariable in params?.listCount){
				countVariable++
				if(params?.("chkbox"+countVariable) == KEY_ON){
					def idDb = params?.("id"+countVariable).toLong()
					jobDetailInstance = JobDetails.get(idDb)
					def triggname = jobDetailInstance?.triggerName
					def jobname = jobDetailInstance?.triggerName
					quartzScheduler.unscheduleJob(triggerKey(triggname));
					quartzScheduler.deleteJob(jobKey(jobname));
					if (jobDetailInstance) {
						jobDetailInstance.delete(flush: true)
					}
				}
			}
		}
		render(template: "scheduleTable", model: [jobDetailList : JobDetails.list()])
	}


	def deleteJob(){
		def jobDetailsInstance = JobDetails.findById(params?.jobId)
		if (jobDetailsInstance) {

			def date = new Date()
			def endDate = jobDetailsInstance?.endDate
			def time
			if(endDate){
				time = date.getTime() - endDate.getTime()
			}
			else{
				time = date.getTime() - jobDetailsInstance?.startDate?.getTime()
			}
			if(time > 0 ){
				jobDetailsInstance.delete(flush: true)
			}
		}
		render(template: "scheduleTable", model: [jobDetailList : JobDetails.list()])
	}

	/**
	 * Method to create a cron tab based on the selection of
	 * schedule type in the gsp page by the user
	 */    
	def createCronScheduleTab(def params) {

		String status = SUCCESS_STATUS
		String cronschedule = ""
		String queryString = ""
		String weekDay = params?.weekDay
		String weekDays = ""
		switch ( params?.reccurGroup ) {
			case KEY_DAILY:
				switch(params?.reccurDaily){
					case KEY_DAILYDAYS:
					if((params?.dailyDaysCount).isEmpty()){
						cronschedule = message(code: 'schedule.novalue.dailydays')
						status = ERROR_STATUS
					}
					else{
						queryString = "Every ${params?.dailyDaysCount} days"
						cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} */${params?.dailyDaysCount} * ?"
					}
					break
					case KEY_DAILYWEEKDAY:
					queryString = "All Weekdays"
					cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ? * 2-6"
					break
					default:
					cronschedule = message(code: 'schedule.error.dailydays')
					status = ERROR_STATUS
					break
				}
				break

			case KEY_WEEKLY:
				if(weekDay){
					if(weekDay instanceof String){
						queryString = "Weekly on ${weekDay}"
						cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ? * ${weekDay}"
					}
					else{
						weekDay.each{ it->
							weekDays = weekDays+it+COMMA_SEPERATOR
						}
						weekDays = weekDays.substring( 0, (weekDays.size()-1) )
						queryString = "Weekly on ${weekDays}"
						cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ? * ${weekDays}"
					}
				}
				else{
					cronschedule = message(code: 'schedule.error.weekly')
					status = ERROR_STATUS
				}
				break

			case KEY_MONTHLY:

				switch(params?.reccurMonthly){
					case KEY_MONTHLYDAYS:
					if((params?.monthlyMonthCount).isEmpty() || (params?.monthlyDaysCount).isEmpty() ){
						cronschedule = message(code: 'schedule.novalue.monthly')
						status = ERROR_STATUS
					}
					else{
						queryString = "Day ${params?.monthlyDaysCount} of every ${params?.monthlyMonthCount} month"
						cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ${params?.monthlyDaysCount} */${params?.monthlyMonthCount} ?"
					}
					break
					case KEY_MONTHLYCOMPLEX:
					if((params?.monthlyMonthCnt).isEmpty()){
						cronschedule = message(code: 'schedule.empty.monthly')
						status = ERROR_STATUS
					}
					else{
						if((params?.daytype).equals( KEY_LASTDAY )){
							queryString = "Last  ${executionService.getDayName(params?.dayName)} of every ${(params?.monthlyMonthCnt)} month"
							cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ? */${params?.monthlyMonthCnt} ${params?.dayName}${params?.daytype}"
						}
						else{
							queryString = "${executionService.getOptionName(params?.daytype)} ${executionService.getDayName(params?.dayName)} of every ${params?.monthlyMonthCnt} month"
							cronschedule = "0 ${params?.startdate_minute} ${params?.startdate_hour} ? */${params?.monthlyMonthCnt} ${params?.dayName}#${params?.daytype}"
						}
					}
					break

					default:
					cronschedule = message(code: 'schedule.error.monthly')
					status = ERROR_STATUS
					break
				}
				break

			default: break
		}
		return [status,cronschedule,queryString]
	}

	/**
	 * Schedule a quartz job
	 * @return
	 */
	def scheduleOneOff() {
		String cronschedule
		String startDateString = (params?.startdate).toString()
		String endDateString = (params?.enddate).toString()
		Date startDate = new SimpleDateFormat(SCHEDULE_DATEFORMAT).parse(startDateString)
		Date endDate = new SimpleDateFormat(SCHEDULE_DATEFORMAT).parse(endDateString)
		String status
		String resultString
		String queryString
		String jobName = KEY_JOB+System.currentTimeMillis().toString()
		String triggerName = KEY_TIGGER+System.currentTimeMillis().toString()
		
		List<String> scriptList = new ArrayList<String>()
		String scheduleDate = (params?.testdate).toString()
		java.util.Date date = new SimpleDateFormat(SCHEDULE_DATEFORMAT).parse(scheduleDate)
		if( Date.getMillisOf( date ) < System.currentTimeMillis() && (params?.scheduleGroup.equals( KEY_ONETIME )) ){
			render message(code: 'schedule.valid.date')
			return
		}
		else if(Date.getMillisOf( startDate ) < System.currentTimeMillis() && (params?.scheduleGroup.equals( KEY_RECCURENCE ))){
			render message(code: 'schedule.valid.startdate')
			return
		}
		else if((endDate < startDate) && (params?.scheduleGroup.equals( KEY_RECCURENCE ))){
			render message(code: 'schedule.valid.startenddate')
			return
		}
		else{

			String[] scriptIdArray = (params?.scriptlist).split(COMMA_SEPERATOR)
			scriptIdArray.each{ scriptid ->
				if(!(scriptid.isEmpty()))
				{
					scriptList.add(scriptid)
				}
			}
			def scriptgroupObject
			def scriptgroupId
			if(params?.scriptGroup){
				scriptgroupObject = ScriptGroup.findByName(params?.scriptGroup)
				scriptgroupId = scriptgroupObject?.id
			}
			
			JobDetail job = JobBuilder.newJob(JobSchedulerService.class)
					.withIdentity(jobName).build();

			Trigger trigger
			if(params?.scheduleGroup.equals( KEY_ONETIME )){
				queryString = KEY_ONETIME
				startDate = date
				endDate = null
				trigger = new SimpleTriggerImpl(triggerName, date)
			}
			else if(params?.scheduleGroup.equals( KEY_RECCURENCE )){

				(status, resultString, queryString) = createCronScheduleTab(params)
				if(status.equals(ERROR_STATUS)){
					render resultString
					return
				}
				else{
					cronschedule = resultString
				}

				trigger = newTrigger()
						.withIdentity(triggerName)
						.withSchedule(cronSchedule(cronschedule))
						.startAt(startDate)
						.endAt(endDate)
						.forJob(jobName)
						.build();
			}
			def jobSheduled = JobDetails?.findAllByDeviceAndStartDate( params?.deviceId,startDate)
			//To avoid scheduling if the device already scheduled for that time
			if(jobSheduled)
			{
				render message(code: 'Another test execution is scheduled in this device for the specified time.')
				return	
			}
			else{
				
				try{
					quartzScheduler.scheduleJob(job, trigger)
				}
				catch(Exception qEx){
					render message(code: 'schedule.invalid.dates')
					return
				}
			
				int repeatCount = (params?.repeatCount).toInteger()


				JobDetails jobDetails = new JobDetails()
				jobDetails.jobName = jobName
				jobDetails.triggerName = triggerName
				jobDetails.script = scriptList
				jobDetails.scriptGroup = scriptgroupId
				jobDetails.device = params?.deviceId
				jobDetails.deviceGroup = null
				jobDetails.realPath = getRealPath()
				jobDetails.appUrl = getApplicationUrl()
				jobDetails.filePath = "${request.getRealPath('/')}//fileStore"
				jobDetails.queryString = queryString
				jobDetails.startDate = startDate
				jobDetails.endDate = endDate
				jobDetails.oneTimeScheduleDate = date
				jobDetails.isSystemDiagnostics = params?.isSystemDiagnostics
				jobDetails.isBenchMark = params?.isBenchMark
				jobDetails.isStbLogRequired=params?.isStbLogRequired
				jobDetails.rerun = params?.rerun
				jobDetails.repeatCount = repeatCount
				jobDetails.rerunOnFailure= FALSE
				jobDetails.isAlertEnabled= params?.isAlertEnabled
				jobDetails.groups = utilityService.getGroup()
				jobDetails.category = Utility.getCategory(params?.category)
				if(!jobDetails.save(flush:true)){
					jobDetails.errors.each{
						println "error : "+it
					}
				}
			}
			def jobDetailList = JobDetails.findAllByGroupsOrGroupsIsNull(utilityService.getGroup())
			render(template: "scheduleTable", model: [jobDetailList : jobDetailList])
			return
		}

	}

	/**
	 * Method to display the schedule page with previously scheduled job details
	 * @param max
	 * @return
	 */
	def showSchedular(Integer max){
		params.max = Math.min(max ?: 10, 100)
		def repeatCount = (params?.repeatId)
		def rerun = params?.rerun

		// identifying the category of job

		def category = null
		if(params?.scriptGroup){
			def val = params?.scriptGroup.split(',')
			def scriptGrp = ScriptGroup.findByName(val[0]?.trim())
			category = scriptGrp?.category?.toString()
		}
		if(params?.scripts){
			def val = params?.scripts.split(',')
			def script = ScriptFile.findByScriptName(val[0]?.trim())
			category = script?.category?.toString()
		}
		if(category == null){
			category = params?.category
		}
		[scripts : params?.scripts, devices : params?.devices, device : params?.deviceId, scriptGroup : params?.scriptGroup, jobDetailList : JobDetails.list(),
			jobInstanceTotal : JobDetails.count(), isSystemDiagnostics : params?.systemDiagnostics, isBenchMark : params?.benchMarking, rerun : rerun,
			repeatCount : repeatCount,isStbLogRequired : params?.isLogReqd, category : params?.category, isAlertEnabled: params?.isAlertChecked]
	}

	/**
	 * Creates the execution page with the listing of devices 
	 * @param max
	 * @return
	 */
	def create(Integer max) {
		params.max = Math.min(max ?: 10, 100)

		def groups = utilityService.getGroup()
		def category
		def executionInstanceList
		def executionInstanceListCnt
		def jobDetailList
		def deviceInstanceListV
		def deviceInstanceListB
		def deviceInstanceListC
		def deviceInstanceList

		deviceInstanceListV = Device.findAllByGroupsAndCategory(groups, Category.RDKV,[sort:'stbName',order:'asc'])
		deviceInstanceListB = Device.findAllByGroupsAndCategory(groups, Category.RDKB,[sort:'stbName', order:'asc'])
		deviceInstanceListC = Device.findAllByGroupsAndCategory(groups, Category.RDKC,[sort:'stbName', order:'asc'])
		category = params?.category
		if(params?.devicestatustable) {
			// This is called from execution-resolver.js loadXmlDoc. This is for automatic page refresh.
			def result1
			if(category){
				if(Category.RDKV.toString().equals(category)){
					deviceInstanceList = deviceInstanceListV
				}
				else if(Category.RDKB.toString().equals(category)){
					deviceInstanceList = deviceInstanceListB
				}else if(Category.RDKC.toString().equals(category)){
					deviceInstanceList = deviceInstanceListC
				}

				result1 = [url: getApplicationUrl(), deviceList : deviceInstanceList, deviceInstanceTotal: deviceInstanceList?.size()]
				render view:"devicelist", model:result1
				return
			}
		}
		else if(params?.category && !"All".equals(params?.category)){
			category = Utility.getCategory(params?.category)
			executionInstanceListCnt = Execution.countByGroupsAndCategory(groups, category)
			executionInstanceList = Execution.findAllByGroupsAndCategory(groups, category,[max:params.max, offset:params?.offset,sort:params?.sort,order:params?.order])
			jobDetailList = JobDetails.findAllByGroupsAndCategory(groups, category,[max:params.max, offset:params?.offset])
		}else{
			executionInstanceListCnt = Execution.countByGroups(groups)
			executionInstanceList = Execution.findAllByGroups(groups, [max:params.max, offset:params?.offset,sort:params?.sort,order:params?.order])
			jobDetailList = JobDetails.findAllByGroups(groups, [max:params.max, offset:params?.offset])
		}

		if(params?.devicetable) {
			// This is called from execution-resolver.js loadXmlDoc. This is for automatic page refresh.
			def result = [executionInstanceList : executionInstanceList, executorInstanceTotal: executionInstanceListCnt, category:params?.category]
			render view:"executionhistorytable", model:result
			return
		}
		else{
			try{
				DeviceStatusUpdater.updateDeviceStatus(grailsApplication,deviceStatusService,executescriptService);
			}catch(Exception e){
				e.printStackTrace();
			}
		}

		[url : getApplicationUrl(), deviceListV : deviceInstanceListV, deviceListB : deviceInstanceListB,  error: params.error, executionInstanceList : executionInstanceList, executorInstanceTotal: executionInstanceListCnt,
			jobDetailList : jobDetailList, jobInstanceTotal: jobDetailList.size(), deviceInstanceTotalV: deviceInstanceListV?.size(), deviceInstanceTotalB: deviceInstanceListB?.size(), category : params?.category ,
			deviceListC : deviceInstanceListC,deviceInstanceTotalC: deviceInstanceListC?.size() ]
	}
	
	/**
	 * Show the device IP and the scripts based on the selection
	 * of device name from the list
	 * @return
	 */
	def showDevices(){
		def category = params?.category?.trim()
		def rdkServiceCategory = Category.RDKV
		def device = Device.get( params?.id )
		def scripts = []
		def scriptListRdkService = []
		def newScripts = []
		def scriptListStorm = []
		if(category?.toString()?.equals('RDKB_TCL') ){
			newScripts = scriptService.getTotalTCLScriptList(getRealPath())
			newScripts?.each { it ->
				if(it){
					scripts?.add(it)
				}  
			}	
		}
		else{
			scripts = scriptService.getScriptNameFileList(getRealPath(), category)
			scriptListRdkService = scriptService.getScriptNameFileListRdkService(getRealPath(), Category.RDKV_RDKSERVICE.toString())
			scriptListStorm = scriptService.getScriptNameFileListStorm()
		}
		def sList = scripts?.clone()
		sList?.sort{a,b -> a?.scriptName <=> b?.scriptName}
		def sRdkList = scriptListRdkService?.clone()
		def groups =  utilityService.getGroup()? utilityService.getGroup() : null
		def devices = getDeviceList(category)
		if(device.isThunderEnabled == 1){
			category = Category.RDKV_THUNDER.toString()
			devices = Device.findAllByIsThunderEnabled(device?.isThunderEnabled)
		}
		def scriptGrp = ScriptGroup.withCriteria {
			eq('category',Utility.getCategory(category))
			or{
				eq('groups',groups)
				isNull('groups')
			}
			order('name')
		}
		def scriptGrpRdkService = ScriptGroup.withCriteria {
			eq('category',Utility.getCategory(Category.RDKV_RDKSERVICE.toString()))
			or{
				eq('groups',groups)
				isNull('groups')
			}
			order('name')
		}
		DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
		Calendar cal = Calendar.getInstance()
		[datetime :  dateFormat.format(cal.getTime()).toString(), device : device, scriptGrpList : scriptGrp, scriptList : sList, sRdkList : sRdkList, scriptGrpRdkService : scriptGrpRdkService, scriptListStorm: scriptListStorm, category:category, devices:devices, grailsUrl: getApplicationUrl(), rdkServiceCategory : rdkServiceCategory]
	}

	def getDeviceList(def category){
		category = Utility.getCategory(category)
		def devices = null
		switch(category){
			case Category.RDKB:
			case Category.RDKB_TCL:
				devices = Device.findAllByCategory(Category.RDKB)
				break
			case Category.RDKV:
				devices = Device.findAllByCategory(Category.RDKV)
				break
			case Category.RDKC:
				devices = Device.findAllByCategory(Category.RDKC)
				break
			default: break
		}
		devices
	}
	def getScriptList(){
		List scriptList = []
		Map scriptGroupMap = [:]
		List dirList = [
			Constants.COMPONENT,
			Constants.INTEGRATION
		]
		dirList.each{ directory ->
			File scriptsDir = new File( "${request.getRealPath('/')}//fileStore//testscripts//"+directory+"//")
			if(scriptsDir.exists()){
				def modules = scriptsDir.listFiles()
				modules.each { module ->

					File [] files = module.listFiles(new FilenameFilter() {
								@Override
								public boolean accept(File dir, String name) {
									return name.endsWith(".py");
								}
							});


					files.each { file ->
						String name = file?.name?.replace(".py", "")
						scriptList.add(name)
					}

				}
			}
		}

		scriptList.sort();

		return scriptList
	}

	/**
	 * Method to get the current date and time from server
	 * to display in execution name field of execution page
	 * @return
	 */
	def showDateTime(){
		def listdate = []
		DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
		Calendar cal = Calendar.getInstance()
		listdate << dateFormat.format(cal.getTime()).toString()
		render listdate as JSON
	}

	/**
	 * Method to get the current url and to create
	 * new url upto the application name
	 * @return
	 */
	def String getApplicationUrl(){
		String currenturl = request.getRequestURL().toString();
		String[] urlArray = currenturl.split( URL_SEPERATOR );
		String serverAddr = urlArray[INDEX_TWO]
		if(serverAddr.contains("localhost:")){
			String localAddr = request.getProperties().get("localAddr")
			String localPort = request.getProperties().get("localPort")
			if((!localAddr.startsWith("0:0:0:0:0:0:0:1")) && (!localAddr.startsWith("0.0.0.0"))){
				serverAddr = ""+localAddr+":"+localPort
			}
		}
		String url = urlArray[INDEX_ZERO] + DOUBLE_FWD_SLASH + serverAddr + URL_SEPERATOR + urlArray[INDEX_THREE]
		return url
	}

	/**
	 * Method to return the real path of the application both windows and linux pc
	 * @return
	 */
	def String getRealPath(){
		/*String osName = System.getProperty(OS_NAME)
		 if(osName?.startsWith(OS_WINDOWS)){
		 String s = request.getSession().getServletContext().getRealPath("/")
		 s = s.replace( '\\', '/' )
		 return s
		 }*/
		return request.getSession().getServletContext().getRealPath(Constants.FILE_SEPARATOR)
	}


	/**
	 * REST interface to support script execution with the parameters passed.
	 * @param stbName
	 * @param boxType
	 * @param suiteName
	 * @return
	 */
	def thirdPartyTest(final String executionName,final String stbName, final String boxType, final String imageName, final String suiteName, final String test_request, final String callbackUrl, final String timeInfo,final String  performance, final String isLogReqd, final String reRunOnFailure , final String isAlert){
		JsonObject jsonOutData = new JsonObject()
		try {
			String htmlData = ""
			String outData = ""
			String  url = getApplicationUrl()
			def execName = ""
			def isBenchMark1 = FALSE
			def isSystemDiagnostics1 = FALSE
			def isLogReqd1 = FALSE
			def isAlertEnabled = FALSE
			def rerun1 = FALSE
			def deviceInstanceIsThunder = Device.findByStbName(stbName)
			if(deviceInstanceIsThunder?.isThunderEnabled != 1){
				if(timeInfo != null ){
					isBenchMark1 = timeInfo
				}
				if(performance != null  ){
					isSystemDiagnostics1 = performance
				}
				if(reRunOnFailure != null ){
					rerun1 = reRunOnFailure
				}
			}
			if(!executionName){
			if(isLogReqd != null ){
				isLogReqd1  = isLogReqd

			}
			if(isAlert != null && deviceInstanceIsThunder?.isThunderEnabled == 1){
				isAlertEnabled  = isAlert
			}
			String filePath = "${request.getRealPath('/')}//fileStore"
			if(test_request && deviceInstanceIsThunder?.isThunderEnabled != 1){
				String status = scriptexecutionService.generateResultBasedOnTestRequest(test_request,callbackUrl,filePath, url, imageName, boxType,getRealPath())
				if(status){
					jsonOutData.addProperty("status", "SUCCESS");
					jsonOutData.addProperty("result", "Result will be send with callback url");
				}
				else{
					jsonOutData.addProperty("status", "FAILED");
					jsonOutData.addProperty("result", "Error! Please try again");
				}
			}
			else{

				ScriptGroup scriptGroup = ScriptGroup.findByName(suiteName)
				def scriptStatusFlag
				def scriptVersionFlag
				Device deviceInstance
				def deviceNotExistStatus = ""
				def deviceNotExistCnt = 0
				def deviceList = stbName.split(',')
				def executionNameForCheck
				def validTclScripts = []
				deviceList.each{

					String stbname = it.toString().trim()
					deviceInstance = Device.findByStbName(stbname)
					if(deviceInstance){

						if(deviceInstance?.boxType?.name.equals(boxType.trim())){

							if(scriptGroup){
								def category = scriptGroup?.category
								String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
								scriptGroup?.scriptList?.each{ scrpt ->
									if(scriptGroup.category != Category.RDKB_TCL){
										def script
										if(deviceInstance?.isThunderEnabled != 1){
											script = scriptService.getScript(getRealPath(), scrpt?.moduleName, scrpt?.scriptName, category?.toString())
										}else{
											script = scriptService.getScript(getRealPath(), scrpt?.moduleName, scrpt?.scriptName, Category.RDKV.toString())
										}

										if(script){
											/**
											 * Checks whether atleast one script matches with the box type of device.
											 * If so execution will proceed with that one script
											 */
											if(executionService.validateScriptBoxTypes(script,deviceInstance)){
												scriptStatusFlag = true
												if(executionService.validateScriptRDKVersions(script,rdkVersion)){
													scriptVersionFlag = true
												}
											}
										}
									}
									else{
										def scriptExists = Utility.isTclScriptExists(getRealPath(), scrpt?.scriptName)
										def deviceConfigExists = Utility.isConfigFileExists(getRealPath(), deviceInstance?.stbName)
										if(scriptExists && deviceConfigExists){
											validTclScripts << Boolean.TRUE
										}
									}
								}
								def totalStatus = scriptStatusFlag && scriptVersionFlag
								if(totalStatus || !validTclScripts.isEmpty()){
									String status = ""
									try {
										status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)

										synchronized (lock) {
											if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
												status = "BUSY"
											}else{
												if((status.equals( Status.FREE.toString() ))){
													if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
														executionService.deviceAllocatedList.add(deviceInstance?.id)

														Thread.start{
															deviceStatusService.updateOnlyDeviceStatus(deviceInstance, Status.BUSY.toString())
														}
													}
												}
											}
										}
									}
									catch(Exception eX){
									}
									status = status.trim()
									if((status.equals( Status.FREE.toString() ))){
										if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
											executionService.deviceAllocatedList.add(deviceInstance?.id)
										}
										def scriptname
										def deviceName
										ExecutionDevice executionDevice
										def execution
										def executionSaveStatus = true

										/**
										 * Even if there is multiple devices, the execution instance need to be created only once.
										 * 'executionNameForCheck' is used to bypass the creation of execution instance
										 */
										if(!executionNameForCheck){
											DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
											Calendar cal = Calendar.getInstance()
											deviceName = deviceInstance?.stbName
											execName = CI_EXECUTION+deviceName+dateFormat.format(cal.getTime()).toString()

											if(deviceList.size() > 1 ){
												executionNameForCheck = execName
												deviceName = MULTIPLE
											}

											try {
												
												// for saving the execution details includes the performance information
												//executionSaveStatus = executionService.saveExecutionDetails(execName, scriptname, deviceName, scriptGroup,url,isBenchMark1,isSystemDiagnostics1,rerun1,isLogReqd1)
												if(deviceInstance?.isThunderEnabled != 1){
													executionSaveStatus = executionService.saveExecutionDetails(execName,[scriptName:scriptname, deviceName:deviceName, scriptGroupInstance:scriptGroup,
														appUrl:url, isBenchMark:isBenchMark1, isSystemDiagnostics:isSystemDiagnostics1, rerun:rerun1, isLogReqd:isLogReqd1,category:category.toString(), rerunOnFailure:FALSE , isAlertEnabled:FALSE ])
												}else{
												    executionSaveStatus = executionService.saveExecutionDetails(execName,[scriptName:scriptname, deviceName:deviceName, scriptGroupInstance:scriptGroup,
													    appUrl:url, isBenchMark:isBenchMark1, isSystemDiagnostics:isSystemDiagnostics1, rerun:rerun1, isLogReqd:isLogReqd1,category:Category.RDKV.toString(), rerunOnFailure:FALSE ,isAlertEnabled:isAlertEnabled ])
												}
												//
												//	executionSaveStatus = scriptexecutionService.saveExecutionDetails(execName, scriptname, deviceName, scriptGroup,url, category)
											} catch (Exception e) {
												executionSaveStatus = false
											}
										}
										if(executionSaveStatus){
											execution = Execution.findByName(execName)
											try{
												executionDevice = new ExecutionDevice()
												executionDevice.execution = execution
												executionDevice.dateOfExecution = new Date()
												executionDevice.device = deviceInstance?.stbName
												executionDevice.boxType = deviceInstance?.boxType?.name
												executionDevice.deviceIp = deviceInstance?.stbIp
												executionDevice.buildName = executionService.getBuildName( deviceInstance?.stbName )
												executionDevice.status = UNDEFINED_STATUS
												executionDevice.category = category
												if(executionDevice.save(flush:true)){
													String getRealPathString  = getRealPath()
													if(deviceInstance?.isThunderEnabled != 1){
														executionService.executeVersionTransferScript(getRealPathString,filePath,execName, executionDevice?.id, deviceInstance?.stbName, deviceInstance?.logTransferPort,url)
													}else{
														StormExecuter.createThunderVersionFile(getRealPathString, execution?.id, executionDevice?.id, executionDevice?.deviceIp)
													}
													//	scriptexecutionService.executeScriptGroup(scriptGroup, boxType, execName, executionDevice?.id.toString(), deviceInstance,url, filePath, getRealPathString, callbackUrl, imageName, category )
													def rerun = null
													if(rerun1?.equals(TRUE)){
														rerun = "on"
													}
													if(category == Category.RDKB_TCL){
														tclExecutionService.executeScriptGroup(scriptGroup, boxType, execName, executionDevice?.id.toString(), deviceInstance, url, filePath, getRealPathString, callbackUrl, imageName, isBenchMark1,isSystemDiagnostics1,rerun,isLogReqd1, category?.toString())
													}
													else{
														if(deviceInstance?.isThunderEnabled != 1){
															scriptexecutionService.executeScriptGroup(scriptGroup, boxType, execName, executionDevice?.id.toString(), deviceInstance, url, filePath, getRealPathString, callbackUrl, imageName, isBenchMark1,isSystemDiagnostics1,rerun,isLogReqd1, category?.toString(), FALSE)
														}else{
														    scriptexecutionService.executeScriptGroup(scriptGroup, boxType, execName, executionDevice?.id.toString(), deviceInstance, url, filePath, getRealPathString, callbackUrl, imageName, isBenchMark1,isSystemDiagnostics1,rerun,isLogReqd1, Category.RDKV.toString(), isAlertEnabled)
														}
													}
												}
											}
											catch(Exception e){
											}
										}
										else{
											deviceNotExistCnt++
											outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
										}
									}
									else if(status.equals( Status.ALLOCATED.toString() )){
										deviceNotExistCnt++
										outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
									}
									else if(status.equals( Status.NOT_FOUND.toString() )){
										deviceNotExistCnt++
										outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
									}
									else if(status.equals( Status.HANG.toString() )){
										deviceNotExistCnt++
										outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
									}
									else if(status.equals( Status.BUSY.toString() )){
										deviceNotExistCnt++
										outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
									}else if(status.equals( Status.TDK_DISABLED.toString() )){
										deviceNotExistCnt++
										outData = outData + "TDK is not enabled  in the Device to execute scripts"

									}
									else{
										deviceNotExistCnt++
										outData = outData + " Device ${deviceInstance?.stbName} is not free to execute Scripts"
									}
								}
								else{
									deviceNotExistCnt++
									if(!scriptStatusFlag){
										outData = outData +" BoxType of Scripts in ScriptGroup is not matching with BoxType of Device ${deviceInstance?.stbName}"
									}else if(!scriptVersionFlag){
										outData = outData +" RDK Version of Scripts in ScriptGroup is not matching with RDK Version of Device ${deviceInstance?.stbName}"
									}
								}
							}
							else{
								deviceNotExistCnt++
								outData = outData + " Script Group does not exist"
							}
						}
						else{
							deviceNotExistCnt++
							outData = outData + " Mismatch between the device ${stbname} and box type ${boxType}"
						}
					}
					else{
						deviceNotExistCnt++
						outData = outData + " - Device ${it} not found"
					}
				}

				if(deviceNotExistCnt < deviceList.size()){
					//  url = url + "/execution/showResult?execName=${execName}&scrGrp=${scriptGroup?.id}"
					url = url + "/execution/thirdPartyJsonResult?execName=${execName}"
					jsonOutData.addProperty("status", "RUNNING"+outData)
					jsonOutData.addProperty("result", url)
				}
			
				else{
					url = outData
					jsonOutData.addProperty("status", "FAILURE")
					jsonOutData.addProperty("result", url)
				}
			}
			}else {

					if(rerun1?.equals(TRUE) || executionName!=null){
					try{
						String filePath = "${request.getRealPath('/')}//fileStore"
						def executionInstance = Execution?.findByName(executionName)
						String uniqueName = executionInstance?.toString()+"12"
						if(!(executionInstance?.category?.toString()?.equals(RDKB_TCL)) && !(executionInstance?.category?.toString()?.equals(RDKV_THUNDER))){
							executescriptService?.reRunOnFailure(getRealPath()?.toString(), filePath?.toString() ,executionName?.toString(),uniqueName?.toString(), url?.toString(), executionInstance?.category?.toString() )
						}else if(executionInstance?.category?.toString()?.equals(RDKV_THUNDER)){
							thunderService?.runFailedScriptsManually(params, executionName?.toString() ,  getRealPath()?.toString(),url?.toString())
						}else{
							tclExecutionService?.reRunOnFailure(getRealPath()?.toString(), filePath?.toString() ,executionName?.toString(),uniqueName?.toString(), url?.toString(), executionInstance?.category?.toString())
						}
						url = url + "/execution/thirdPartyTest?executionName=${executionName}"
						jsonOutData.addProperty("Status", "Triggered Execution For Rerun Of Failure Scripts")
						jsonOutData.addProperty("result", url)
					}catch (Exception e) {
					}
				}
			}
			
		} catch (Exception e) {
		}
		render jsonOutData
	}
	
	/** 
	 * REST method to retrieve the device status list
	 * @param boxType
	 * @return
	 */
	def getDeviceStatusList(String boxType){
		JsonObject devices = new JsonObject()
		try {
			if(boxType == null){
				def deviceList = Device.list()
				deviceList?.each{ device ->
					//devices.addProperty(device.stbName.toString()+LEFT_PARANTHESIS+device.stbIp.toString()+RIGHT_PARANTHESIS+LEFT_PARANTHESIS+device.boxType.toString()+RIGHT_PARANTHESIS, device.deviceStatus.toString())
					// ISSUE - FIX: Adding device category to the JSON
					devices.addProperty(device?.stbName.toString()+LEFT_PARANTHESIS+device?.stbIp.toString()+RIGHT_PARANTHESIS+LEFT_PARANTHESIS+device.boxType.toString()+RIGHT_PARANTHESIS+LEFT_PARANTHESIS+device?.category?.toString()+RIGHT_PARANTHESIS,device.deviceStatus.toString())
				}
			} else {
				JsonArray devArray = new JsonArray()
				def devList
				BoxType	boxTypeObj = BoxType.findByName(boxType)
				if(boxTypeObj){
					devList = Device.findAllByBoxType(boxTypeObj)
				}
				if(boxType && !boxTypeObj){
					devices.addProperty("status", "failure")
					devices.addProperty("remarks", "no box type found with name "+boxType)
				} else{
					if(devList){
						devList?.each{ dev ->
							JsonObject device = new JsonObject()
							device.addProperty("name", dev?.stbName)
							device.addProperty("boxtype", dev?.boxType?.name)
							//adding category of device - broadband or video
							device.addProperty("category", dev?.category?.toString())
							if(dev?.boxType?.type?.equals("Client")){
								if(dev?.gatewayIp){
									device.addProperty("gateway", dev?.gatewayIp)
								}
								if(dev?.isChild == 1){
									device.addProperty("macid", dev?.macId)
									device.addProperty("mocachild", "true")
								}else{
									device.addProperty("mocachild", "false")
									device.addProperty("ip", dev?.stbIp)
								}
							}else{
								device.addProperty("ip", dev?.stbIp)
							}
							device.addProperty("status", dev?.deviceStatus.toString())
							devArray.add(device)
						}
					}
					devices.add("devices",devArray)
				}
			}
		} catch (Exception e) {

		}
		render devices
	}

	def getDeviceStatus(final String stbName, final String boxType){
		JsonObject device = new JsonObject()
		try {
			if(stbName && boxType)	{
				def deviceInstance = Device.findByStbName(stbName)//,BoxType.findByName(boxType.trim()))
				device.addProperty(deviceInstance.stbName.toString()+LEFT_PARANTHESIS+deviceInstance.stbIp.toString()+RIGHT_PARANTHESIS, deviceInstance.deviceStatus.toString())
			}
		} catch (Exception e) {
		}
		render device
	}
	
	/**
	 * Method to fetch device status
	 * @param stbName
	 * @return
	 */
	def fetchDeviceStatus(){
		def stbName = params?.device
		def status
		try {
			if(stbName){
				def deviceInstance = Device.findByStbName(stbName)
				status = deviceInstance?.deviceStatus
			}
		}catch(Exception e) {
			e.printStackTrace()
		}
		render status
	}

	def getRealtimeDeviceStatus(final String stbName, final String boxType){
		JsonObject device = new JsonObject()
		try {
			def deviceInstance = Device.findByStbName(stbName)
			def status = Status.NOT_FOUND?.toString()
			if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
				status = Status.BUSY?.toString()
			}
			else{
				status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
			}

			if(stbName && boxType)	{
				device.addProperty(deviceInstance.stbName.toString()+LEFT_PARANTHESIS+deviceInstance.stbIp.toString()+RIGHT_PARANTHESIS, status)
			}
			if(!deviceInstance?.deviceStatus.equals(status)){
				Thread.start{
					deviceStatusService.updateOnlyDeviceStatus(deviceInstance, status)
				}
			}
		} catch (Exception e) {

		}
		render device
	}

	def thirdPartyJsonResult(final String execName, final String appurl ){
		JsonObject executionNode = scriptexecutionService.thirdPartyJsonResultFromController(execName, getApplicationUrl() ,getRealPath())
		render executionNode
	}

	def thirdPartyJsonPerformanceResult(final String execName, final String appurl ){
		Execution executionInstance = Execution.findByName(execName)
		if(executionInstance?.script && executionInstance?.executionStatus?.equals(COMPLETED_STATUS)){
			executionService.setPerformance(executionInstance,request.getRealPath('/'))
		}else{
			executionService.setPerformance(executionInstance,request.getRealPath('/'))
		}
		JsonObject executionNode = scriptexecutionService.thirdPartyJsonPerformanceResultFromController(execName, getApplicationUrl() ,getRealPath())
		render executionNode
	}


	/**
	 * Execute the script
	 * @return
	 */
	def executeScriptMethod() {
		boolean thunderPythonExecution = false
		if(params?.thunderExecutionType == "rdkservice"){
			thunderPythonExecution = true
		}
		def scriptType
		def paramsScripts
		def paramsScriptGrp
		if(!thunderPythonExecution){
			scriptType = params?.myGroup
			paramsScripts = params?.scripts
			paramsScriptGrp = params?.scriptGrp
		}else{
			scriptType = params?.myGroupThunder
			paramsScripts = params?.scriptsThunderPython
			paramsScriptGrp = params?.scriptGrpThunderPython
		}
		boolean aborted = false
		def exId
		def scriptGroupInstance
		def scriptGroupList = []
		def scriptStatus = true
		def scriptVersionStatus = true
		Device deviceInstance //= Device.findById(params?.id, [lock: true])
		String htmlData = ""
		def deviceId
		def executionName
		
		def deviceList = []
		def deviceName
		String boxType
		boolean allocated = false
		boolean singleScript = false
		boolean singleScriptGroup = false
		String rerunOnFailure =FALSE

		ExecutionDevice executionDevice = new ExecutionDevice()
		int  scriptCountMultipleSuite = 0
		def scriptListMultipleSuite = []
		if(!(paramsScriptGrp instanceof String)){
			for(scrptGrp in paramsScriptGrp){
				def scrptGroupInstance = ScriptGroup.findByName(scrptGrp,[fetch : [scriptList : "eager"]])
				scrptGroupInstance?.scriptList?.each{scrpt->
					scriptListMultipleSuite.add(scrpt?.scriptName)
				}
			}
			def Set<ScriptFile> scriptFileObjectSet = new HashSet(scriptListMultipleSuite)
			scriptCountMultipleSuite = scriptFileObjectSet?.size()
		}
		if(params?.devices instanceof String){
			deviceList << params?.devices
			deviceInstance = Device.findById(params?.devices, [lock: true])
			deviceName = deviceInstance?.stbName
		}
		else{
			(params?.devices).each{ deviceid ->
				deviceList << deviceid
			}
			deviceName = MULTIPLE
		}

		if(params?.execName){
			executionName = params.execName
		}
		else{
			executionName = params?.name
		}

		int repeatCount = 1
		int repeatBackToBackCount = 1
		if(params?.repeatType == "full"){
			repeatCount = (params?.repeatNo)?.toInteger()
		}else{
		    repeatBackToBackCount = (params?.individualRepeatNo)?.toInteger()
		}

		def executionInstance = Execution.findByName(executionName)
		if(!(params?.name)){
			htmlData = message(code: 'execution.name.blank')
		}
		else if(executionInstance){
			htmlData = message(code: 'execution.name.duplicate')
		}
		else if(!(params?.devices)){
			htmlData = message(code: 'execution.nodevice.selected')
		}
		else if(!paramsScriptGrp && !paramsScripts){
			htmlData = message(code: 'execution.noscript.selected')
		}
		else if(deviceInstance?.deviceStatus.toString().equals(Status.BUSY.toString())){
			htmlData =deviceName+ " : "+message(code: 'execution.device.notfree')
		}
		else if(deviceInstance?.deviceStatus.toString().equals(Status.NOT_FOUND.toString())){
			htmlData =deviceName+" : "+ message(code: 'execution.device.notfree')
		}
		else if(deviceInstance?.deviceStatus.toString().equals(Status.HANG.toString())){
			htmlData = deviceName+ " : "+message(code: 'execution.device.notfree')
		}else if(deviceInstance?.deviceStatus.toString().equals(Status.TDK_DISABLED.toString()))	{
			htmlData= deviceName+ " : "+message(code: 'execution.device.notfree')
		}
		else if(repeatCount == 0 || repeatBackToBackCount == 0){
			htmlData = "Give a valid entry in repeat"
		}
		else{
			StringBuilder output = new StringBuilder();

			if(deviceList.size() > 1){
				output.append("Multiple Device Execution ")
			}
			def category = params?.category?.trim()
			if(!"RDKB_TCL".equals(category)){
				try{
					def isBenchMark = FALSE
					def isSystemDiagnostics = FALSE
					def isLogReqd = FALSE
					def isAlertEnabled = FALSE
					def rerun = FALSE
					if(params?.systemDiagnostics.equals(KEY_ON) || params?.rdkCertificationDiagnosis?.equals(KEY_ON)){
						isSystemDiagnostics = TRUE
					}
					if(params?.benchMarking.equals(KEY_ON) || params?.rdkCertificationPerformance?.equals(KEY_ON)){
						isBenchMark = TRUE
					}
					if(params?.rdkCertificationStbLogTransfer?.equals(KEY_ON) || params?.transferLogs?.equals(KEY_ON)){
						isLogReqd = TRUE
					}
					if(params?.rdkProfilingAlertCheckBox?.equals(KEY_ON)){
						isAlertEnabled = TRUE
					}
					if(params?.rerun.equals(KEY_ON)){
						rerun = TRUE
					}
					def scriptName = null
					String url = getApplicationUrl()
					String filePath = "${request.getRealPath('/')}//fileStore"
					def execName
					def executionNameForCheck


					Map deviceDetails = [:]
					for(int i = 0; i < repeatCount; i++ ){
						executionNameForCheck = null
						deviceList.each{ device ->
							deviceInstance = Device.findById(device)
							boolean validScript = false
							deviceName = deviceInstance?.stbName
							if(scriptType == SINGLE_SCRIPT){
								def scripts = paramsScripts
								if(scripts instanceof String){
									singleScript = true
									def moduleName= scriptService.scriptMapping.get(paramsScripts)
									if(moduleName){
										def scriptInstance1 = scriptService.getScript(getRealPath(),moduleName, paramsScripts, params?.category)
										if(scriptInstance1){
											if(executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
												String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
												if(executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)){
													validScript = true
												}else{
													htmlData = "<br>"+deviceName +"  : RDK Version supported by the script is not matching with the RDK Version of selected Device "+deviceInstance?.stbName+"<br>"
												}
											}else{
												htmlData = "<br>"+deviceName +" : "+ message(code: 'execution.boxtype.nomatch')
											}
										}else{
											htmlData = "<br>"+deviceName +"  : No Script is available with name ${paramsScripts} in module ${moduleName}"
										}
									}else{ 
										htmlData = "<br>"+deviceName +" : No module associated with script ${paramsScripts}"
									}
								}
								else{
									scripts.each { script ->
										def moduleName= scriptService.scriptMapping.get(script)
										def scriptInstance1 = scriptService.getScript(getRealPath(),moduleName, script, params?.category)
										if(scriptInstance1){
											if(executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
												String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
												if(executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)){
													validScript = true
												}
											}
										}
									}

								}
							}else{
								def scriptGroups = paramsScriptGrp
								if(scriptGroups instanceof String){
									singleScriptGroup = true
									def scriptGroup = ScriptGroup.findByName(scriptGroups)
									scriptGroupList.add(scriptGroup)
								}else{
								    for(scrptGrp in scriptGroups){
										def scriptGroup = ScriptGroup.findByName(scrptGrp)
										scriptGroupList.add(scriptGroup)
									}
								}
								scriptGroupList?.each{eachScriptGroup ->
								String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
								try{
									eachScriptGroup?.scriptList?.each{ script ->
										def scriptInstance1 = scriptService.getMinimalScript(getRealPath(),script?.moduleName, script?.scriptName, params?.category)

										/**
										 * Checks whether atleast one script matches with the box type of device.
										 * If so execution will proceed with that one script
										 */
										if(scriptInstance1 && executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
											if(executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)){
												validScript = true
												throw new Exception("return from closure")
											}
										}
									}
								}catch(Exception e ){
									if(e.getMessage() == "return from closure" ){

									}else{
										validScript = false
									}
								}
							}
                        }

							if(validScript){
								if(deviceList.size() > 1){
									executionNameForCheck = null
								}
								boolean paused = false
								int pending = 0
								int currentExecutionCount = -1
								Map statusMap = deviceDetails.get(device)
								if(statusMap){
									paused = ((boolean)statusMap.get("isPaused"))
									pending = ((int)statusMap.get("pending"))
									currentExecutionCount = ((int)statusMap.get("currentExecutionCount"))
								}
								String status = ""

								deviceInstance = Device.findById(device)
								try {
									status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
									synchronized (lock) {
										if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
											status = "BUSY"
										}else{
											if((status.equals( Status.FREE.toString() ))){
												if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
													allocated = true
													executionService.deviceAllocatedList.add(deviceInstance?.id)
													Thread.start{
														deviceStatusService.updateOnlyDeviceStatus(deviceInstance, Status.BUSY.toString())
													}
												}
											}
										}
									}

								}
								catch(Exception eX){
								}

								if( !paused && (status.equals( Status.FREE.toString() ))){
									if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
										allocated = true
										executionService.deviceAllocatedList.add(deviceInstance?.id)
									}

									deviceInstance = Device.findById(device)
									def executionSaveStatus = true
									def execution = null
									def scripts = null
									deviceId = deviceInstance?.id
									if(scriptType == SINGLE_SCRIPT){
										scripts = paramsScripts
										if(scripts instanceof String){
											//							scriptInstance = Script.findById(params?.scripts,[lock: true])
											def moduleName= scriptService.scriptMapping.get(paramsScripts)
											def scriptInstance1 = scriptService.getScript(getRealPath(),moduleName, paramsScripts, params?.category)
											//							def scriptInstance1 = executionService.getScript(getRealPath(),"ClosedCaption", scripts)
											scriptStatus = executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)
											String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
											scriptVersionStatus = executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)
											scriptName = scripts
										}
										else{
											scriptName = MULTIPLESCRIPT
										}
									}else{
										if(singleScriptGroup){
											scriptGroupInstance = ScriptGroup.findByName(paramsScriptGrp)
										}else{
										    scriptName = MULTIPLESCRIPTGROUPS
										}
									}
									if(scriptStatus && scriptVersionStatus){
										if(!executionNameForCheck){
											String exName = executionName
											if(deviceList.size() > 1){
												deviceName = deviceInstance?.stbName
												exName = deviceInstance?.stbName +"-"+executionName
											}
											if(i > 0){
												execName = exName + UNDERSCORE +i
											}
											else{
												execName = exName
											}
											if(repeatBackToBackCount > 1){
												execName = execName + "(R"+repeatBackToBackCount+")"
											}
											// Test case count include in the multiple scripts executions
											if(scriptName.equals(MULTIPLESCRIPT)){
												def  scriptCount = paramsScripts?.size()
												executionSaveStatus = executionService.saveExecutionDetailsOnMultipleScripts(execName, scriptName, deviceName, scriptGroupInstance,url,isBenchMark,isSystemDiagnostics,rerun,isLogReqd,scriptCount, params?.category,rerunOnFailure,isAlertEnabled)
											}else if(scriptName.equals(MULTIPLESCRIPTGROUPS)){
												executionSaveStatus = executionService.saveExecutionDetailsOnMultipleScriptgroups(execName,[scriptName:scriptName, deviceName:deviceName, scriptGroupInstance:scriptGroupInstance,
													appUrl:url, isBenchMark:isBenchMark, isSystemDiagnostics:isSystemDiagnostics, rerun:rerun, isLogReqd:isLogReqd,category:params?.category , rerunOnFailure:rerunOnFailure, scriptCount:scriptCountMultipleSuite, isAlertEnabled:isAlertEnabled])
											}else{
												//executionSaveStatus = executionService.saveExecutionDetails(execName, scriptName, deviceName, scriptGroupInstance,url,isBenchMark,isSystemDiagnostics,rerun,isLogReqd)
												executionSaveStatus = executionService.saveExecutionDetails(execName,[scriptName:scriptName, deviceName:deviceName, scriptGroupInstance:scriptGroupInstance,
													appUrl:url, isBenchMark:isBenchMark, isSystemDiagnostics:isSystemDiagnostics, rerun:rerun, isLogReqd:isLogReqd,category:params?.category , rerunOnFailure:rerunOnFailure,isAlertEnabled:isAlertEnabled])
											}

											//	executionSaveStatus = executionService.saveExecutionDetails(execName, [scriptName:scriptName, deviceName:deviceName, scriptGroupInstance:scriptGroupInstance, url : url, isBenchMark : isBenchMark, isSystemDiagnostics: isSystemDiagnostics,, rerun : rerun, isLogReqd:isLogReqd, category: params?.category])

											if(deviceList.size() > 0 ){
												executionNameForCheck = execName
											}
										}
										else{
											execution = Execution.findByName(executionNameForCheck)
											execName = executionNameForCheck
										}
										if(executionSaveStatus){
											try{
												executionDevice = new ExecutionDevice()
												executionDevice.execution = Execution.findByName(execName)
												executionDevice.dateOfExecution = new Date()
												executionDevice.device = deviceInstance?.stbName
												executionDevice.boxType = deviceInstance?.boxType?.name
												executionDevice.deviceIp = deviceInstance?.stbIp
												executionDevice.status = UNDEFINED_STATUS
												executionDevice.category = Utility.getCategory(params?.category)
												executionDevice.buildName = executionService.getBuildName( deviceInstance?.stbName )
												executionDevice.save(flush:true)
											}
											catch(Exception e){
												e.printStackTrace()
											}
											def scriptId
											if((!(paramsScriptGrp)) && (!(paramsScripts))){
												render ""
												return
											}
											else{
												if(thunderPythonExecution){
													try{
														def executionObject = Execution.findByName(execName)
														def executionId = executionObject?.id
														StormExecuter.createThunderVersionFile(request.getRealPath('/'), executionId, executionDevice?.id, executionDevice?.deviceIp)
													}catch(Exception e){
														e.printStackTrace()
													}
												}else{
													executionService.executeVersionTransferScript(request.getRealPath('/'),filePath,execName, executionDevice?.id, deviceInstance?.stbName, deviceInstance?.logTransferPort,url)
												}
											}
											if(deviceList.size() > 1){
												    executescriptService.executeScriptInThread(singleScriptGroup, execName, device, executionDevice, paramsScripts, paramsScriptGrp, executionName,
														filePath, getRealPath(), scriptType, url, isBenchMark, isSystemDiagnostics, params?.rerun,isLogReqd, params?.category, repeatBackToBackCount,isAlertEnabled)
												    htmlData=" <br> " + deviceName+"  :   Execution triggered "
												    output.append(htmlData)


											}else{
												    htmlData = executescriptService.executescriptsOnDevice(singleScriptGroup, execName, device, executionDevice, paramsScripts, paramsScriptGrp, executionName,
														filePath, getRealPath(), scriptType, url, isBenchMark, isSystemDiagnostics, params?.rerun,isLogReqd, params?.category, repeatBackToBackCount,isAlertEnabled)
												    output.append(htmlData)
												    Execution exe = Execution.findByName(execName)
												    if(exe){
													    def executionList = Execution.findAllByExecutionStatusAndName("PAUSED",execName);
													    paused = (executionList.size() > 0)
												    }
											}

											if(paused){
												currentExecutionCount = i
												statusMap = deviceDetails.get(device)
												if(statusMap == null){
													statusMap = [:]
													deviceDetails.put(device,statusMap)
												}

												if(statusMap != null){
													statusMap.put("isPaused", true)
													statusMap.put("currentExecutionCount", i)
													statusMap.put("pending", pending)
												}

											}
										}
									}

									else{
										def devcInstance = Device.findById(device)
										if(!scriptStatus){
											htmlData ="<br>"+deviceName+"  :  "+ message(code: 'execution.boxtype.nomatch')
										}else{
											htmlData ="<br>"+deviceName+ " :  RDK Version supported by the script is not matching with the RDK Version of selected Device "+devcInstance?.stbName+"<br>"
										}


										if(executionService.deviceAllocatedList.contains(devcInstance?.id)){
											executionService.deviceAllocatedList.remove(devcInstance?.id)
										}
										output.append(htmlData)
									}
									htmlData = ""
								}else{

									if(paused){
										try {
											pending ++

											statusMap = deviceDetails.get(device)

											if(statusMap != null){
												statusMap.put("pending", pending)
											}

											if(i == repeatCount -1){
												executionService.saveRepeatExecutionDetails(execName, deviceInstance?.stbName,currentExecutionCount, pending, params?.category)
											}

										} catch (Exception e) {
											e.printStackTrace()
										}
									}else{

										if(i > 0){
											def execName1 = executionName + UNDERSCORE +i

											try {

												Execution execution = new Execution()
												execution.name = execName1
												if(scriptName!="Multiple Scriptgroups"){
												    execution.script = scriptName
												}
												execution.device = deviceName
												if(singleScriptGroup){
													execution.scriptGroup = scriptGroupInstance?.name
												}else if(scriptName!="Multiple Scripts"){
												    execution.scriptGroup = "Multiple Scriptgroups"
												}
												execution.result = FAILURE_STATUS
												execution.executionStatus = FAILURE_STATUS
												execution.dateOfExecution = new Date()
												execution.category = Utility.getCategory(params?.category)
												execution.groups = executionService.getGroup()
												execution.applicationUrl = url
												execution.isRerunRequired = rerun?.equals(TRUE)
												execution.isBenchMarkEnabled = isBenchMark?.equals(TRUE)
												execution.isSystemDiagnosticsEnabled = isSystemDiagnostics?.equals(TRUE)
												execution.isStbLogRequired = isLogReqd?.equals(TRUE)
												execution.isAlertEnabled = isAlertEnabled?.equals(TRUE)
												execution.rerunOnFailure = rerunOnFailure?.equals(TRUE)
												execution.outputData = "Execution failed due to the unavailability of box"
												if(! execution.save(flush:true)) {
													log.error "Error saving Execution instance : ${execution.errors}"
												}
											}
											catch(Exception th) {
												th.printStackTrace()
											}
										}

										htmlData = "<br>"+deviceName+" : "+message(code: 'execution.device.notfree')
										output.append(htmlData)
									}
								}
							}else{
								if(!singleScript){
									htmlData = "<br>"+deviceName+ "  :  No valid script available to execute."
								}
								output.append(htmlData)
							}
						}
					}
				}finally{
					if(deviceList.size() == 1){
						deviceList.each{ device ->
							def devInstance = Device.findById(device)
							if(allocated && executionService.deviceAllocatedList.contains(devInstance?.id)){
								executionService.deviceAllocatedList.remove(devInstance?.id)
							}
						}

						String devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
						Thread.start{
							deviceStatusService.updateOnlyDeviceStatus(deviceInstance, devStatus)
						}

					}
				}
				htmlData = output.toString()
			}
			else{
				htmlData = tclExecutionService.executeTclScripts(params, getRealPath(), getApplicationUrl())
			}
		}
		render htmlData
	}
	/**
	 * show execution result via link 
	 * @return
	 */
	def showExecutionResult(){
		String data = ""
		if(params?.execResult){
			ExecutionResult exResult = ExecutionResult.get(params?.execResult)
			data = exResult?.executionOutput
		}else{
			data = "Log data not available"
		}
		render data
	}


	def showAgentLogFiles(){
		def consoleFileData = executionService.getAgentConsoleLogData( request.getRealPath('/'), params?.execId, params?.execDeviceId,params?.execResId)
		ExecutionDevice execDeviceInstance = ExecutionDevice.findById(params?.execDeviceId)
		if(consoleFileData.isEmpty() && !(execDeviceInstance?.category?.toString().equals(RDKV_THUNDER))){
			consoleFileData = "Unable to fetch Agent Console Log"
		}else if(consoleFileData.isEmpty() && (execDeviceInstance?.category?.toString().equals(RDKV_THUNDER))){
		    consoleFileData = "Server Console Log Empty"
		}
		render(template: "agentConsoleLog", model: [agentConsoleFileData : consoleFileData])
	}
	
	/**
	 * Method to fetch the execution details
	 * @return
	 */
	def getExecutionDetails(){
		def exRes = ExecutionResult.get(params?.execResId)
		render(template: "executionDetails", model: [executionResultInstance : exRes])
	}

	/**
	 * Function to fetch the profiling details of show link is clicked corresponding to each Profiling Metrics row
	 */
	def getProfilingDetails(){
		String realPathForLogs = getRealPathForLogs()
		def executionResultId = params?.execResId
		def exRes = ExecutionResult.get(params?.execResId)
		def executionId = exRes.execution.id
		def executionDeviceId = exRes.executionDevice.id
		def device = Device.findByStbName(exRes?.device)
		Map alertMapForExecRes = [:]
		String macAddress = ""
		if(device){
			macAddress = device?.serialNo
		}
		def alertMap = [:]
		Date fromDate = exRes.dateOfExecution
		String executionTime = exRes.totalExecutionTime
		def logPath = realPathForLogs + "logs//${executionId}//${executionDeviceId}//${executionResultId}//"
		if(executionTime != null && executionTime != ""){
			Double totalExecutionTime =  Double.parseDouble(executionTime)
			totalExecutionTime = totalExecutionTime * 1000
			long totalExecutionTimeInLong = (long)totalExecutionTime;
			Date toDate = new Date(fromDate.getTime() + totalExecutionTimeInLong);
			List alertListFromService = executescriptService.fetchAlertDataForExecResult(executionId,logPath);
			if(!alertListFromService?.isEmpty()){
				alertListFromService.each{ alert ->
					List metricList = []
					def metric =  alert?.get('metric')
					if(alertMapForExecRes.containsKey(metric)){
						metricList = alertMapForExecRes.get(metric)
					}
					metricList?.add(alert)
					alertMapForExecRes.put(metric, metricList)
				}
			}
		}
		
		def finalLogparserFileName = ""
		File logDir  = new File(logPath)
		Map smemFileMap = [:]
		Map pmapFileMap = [:]
		Map systemdanalysisFileMap = [:]
		Map systemdBootchartFileMap = [:]
		Map lmbenchFileMap = [:]
		if(logDir?.exists() &&  logDir?.isDirectory()){
			logDir.eachFile{ file->
				def currentFileName = file?.getName()
				if(file?.getName()?.contains("smemData")){
					String fileContents = ""
					file.eachLine { line ->
						String lineData = line?.replaceAll("<","&lt;")
						lineData = lineData?.replaceAll(">","&gt;")
						fileContents = fileContents + "<br>"+ lineData
					}
					currentFileName = currentFileName?.substring(currentFileName?.indexOf("_") + 1,currentFileName?.length())
					smemFileMap?.put(currentFileName,fileContents)
				}
				if(file?.getName()?.contains("pmapData")){
					String fileContents = ""
					currentFileName = currentFileName?.substring(currentFileName?.indexOf("_") + 1,currentFileName?.length())
					pmapFileMap?.put(currentFileName,fileContents)
				}
				if(file?.getName()?.contains("systemdAnalyze")){
					currentFileName = currentFileName?.substring(currentFileName?.indexOf("_") + 1,currentFileName?.length())
					if(file?.getName()?.contains("svg")){
						String systemdAnalysisFilePath = "..//logs//${executionId}//${executionDeviceId}//${executionResultId}//"+file?.getName()
						systemdanalysisFileMap?.put(currentFileName,systemdAnalysisFilePath)
					}else{
						String fileContents = ""
						file.eachLine { line ->
							String lineData = line?.replaceAll("<","&lt;")
							lineData = lineData?.replaceAll(">","&gt;")
							fileContents = fileContents + "<br>"+ lineData
						}
						systemdanalysisFileMap?.put(currentFileName,fileContents)
					}
				}
				if(file?.getName()?.contains("systemdBootchart")){
					currentFileName = currentFileName?.substring(currentFileName?.indexOf("_") + 1,currentFileName?.length())
					String systemdBootchartFilePath = "..//logs//${executionId}//${executionDeviceId}//${executionResultId}//"+file?.getName()
					systemdBootchartFileMap?.put(currentFileName,systemdBootchartFilePath)
				}
				if(file?.getName()?.contains("lmbench")){
					String fileContents = ""
					file.eachLine { line ->
						String lineData = line?.replaceAll("<","&lt;")
						lineData = lineData?.replaceAll(">","&gt;")
						fileContents = fileContents + "<br>"+ lineData
					}
					currentFileName = currentFileName?.substring(currentFileName?.indexOf("_") + 1,currentFileName?.length())
					lmbenchFileMap?.put(currentFileName,fileContents)
				}
			}
		}
		render(template: "profilingDetails", model: [executionResultInstance : exRes,alertListMap:alertMapForExecRes,k:params?.k,i:params?.i,smemFileMap:smemFileMap,execId:executionId,execDeviceId:executionDeviceId,profilingDetails:true,pmapFileMap:pmapFileMap,systemdanalysisFileMap:systemdanalysisFileMap,systemdBootchartFileMap:systemdBootchartFileMap,lmbenchFileMap:lmbenchFileMap])
	}
	
	/**
	 * Function to download smem file from UI
	 * @return
	 */
	def downloadFileContents()  {
		try {
			String realPathForLogs = getRealPathForLogs()
			String fileName = params?.id
			String filePath = realPathForLogs + "//logs//${params?.execId}//${params?.execDeviceId}//${params?.execResultId}//"+params?.id
			def file = new File(filePath)
			response.setContentType("html/text")
			response.setHeader("Content-disposition", "attachment;filename=${file.getName()}")
			response.outputStream << file.newInputStream()
		} catch (FileNotFoundException fnf) {
			response.sendError 404
		}
	}
	
	/**
	 * Function to display smem file contents in UI
	 * @return
	 */
	def showFileContents(){
		String realPathForLogs = getRealPathForLogs()
		def consoleFileData = ""
		String filePath = realPathForLogs + "//logs//${params?.execId}//${params?.execDeviceId}//${params?.execResultId}//"+params?.fileName
		def file = new File(filePath)
		try{
			if(file?.exists()){
				def currentFileName = params?.fileName
				if(currentFileName?.contains("smemData") || currentFileName?.contains("pmapData") || currentFileName?.contains("systemdAnalyze") || currentFileName?.contains("lmbench")){
					file.eachLine { line ->
						String lineData = line?.replaceAll("<","&lt;")
						lineData = lineData?.replaceAll(">","&gt;")
						consoleFileData = consoleFileData + "<br>"+ lineData
					}
				}
			}
		} catch (FileNotFoundException fnf) {
			
		}
		if(consoleFileData.isEmpty() || consoleFileData == ""){
			consoleFileData = "No Data"
		}
		render(template: "profilingDetails", model: [consoleFileData:consoleFileData,profilingDetails:false])
	}
	
	/**
	 * Method to get pmap contents to display in UI
	 * @return
	 */
	def getPmapContents(){
	    String realPathForLogs = getRealPathForLogs()
		def pmapFileData = ""
		String filePath = realPathForLogs + "//logs//${params?.execId}//${params?.execDeviceId}//${params?.execResultId}//"+params?.fileName
		def file = new File(filePath)
		try{
			if(file?.exists()){
				def currentFileName = params?.fileName
				if(currentFileName?.contains("pmapData")){
					file.eachLine { line ->
						String lineData = line?.replaceAll("<","&lt;")
						lineData = lineData?.replaceAll(">","&gt;")
						pmapFileData = pmapFileData + "<br>"+ lineData
					}
				}
			}
		} catch (FileNotFoundException fnf) {
			
		}
		if(pmapFileData.isEmpty() || pmapFileData == ""){
			pmapFileData = "No Data"
		}
		render pmapFileData
	}
	
	def showLogFiles(){

		def logFileNames = executionService.getLogFileNames(request.getRealPath('/'), params?.execId, params?.execDeviceId, params?.execResId )
		render(template: "logFileList", model: [execId : params?.execId, execDeviceId : params?.execDeviceId, execResId : params?.execResId, logFileNames : logFileNames])
	}

	def showCrashLogFiles(){
		def crashlogFileNames = executionService.getCrashLogFileNames(request.getRealPath('/'), params?.execId, params?.execDeviceId, params?.execResId)
		render(template: "crashLogFileList", model: [execId : params?.execId, execDeviceId : params?.execDeviceId, execResId : params?.execResId, logFileNames : crashlogFileNames])
	}

    /**
     * Method to fetch the result of an execution
     * @param execResId
     * @return
     */
	def showMethodResult(){
		def execResId = params?.execResId
		ExecutionResult executionResult
		try{
			executionResult = ExecutionResult.findById(execResId)
		}catch(Exception e){
			e.printStackTrace()
		}
		render(template: "methodResults", model: [executionResultInstance : executionResult])
	}

	/**
	 * Method to fetch the result of 5 previous executions having the same box type
	 * @param execResId
	 * @return
	 */
	def showScriptTrend(){
		def execResId = params?.execResId
		Map dataMap = [:]
		def execResults = []
		ExecutionResult executionResult = ExecutionResult.findById(execResId)
		if(executionResult){
			def scriptName = executionResult?.script
			def execId = executionResult?.execution?.id
			def boxType = executionResult.executionDevice.boxType
			if(boxType){
				execResults = ExecutionResult.findAll("from ExecutionResult as executionResult WHERE executionResult.executionDevice.boxType='${boxType}' and executionResult.script like '${scriptName}' and executionResult.execution.id<'${execId}' and (executionResult.status = 'SUCCESS' or executionResult.status = 'FAILURE' or executionResult.status = 'SCRIPT TIME OUT') order by id desc" , [max: 5])
			}
			else{
				BoxType boxTypeObject = null
				Device device = Device.findByStbName(executionResult?.device)
				if(device){
					boxTypeObject = device?.boxType
					def deviceList = Device.findAllByBoxType(boxTypeObject)?.stbName
					def execCriteria = ExecutionResult.createCriteria()
					execResults = execCriteria {
						like ("script", scriptName)
						'in' ("device", deviceList)
						'in' ("status",['SUCCESS','FAILURE','SCRIPT TIME OUT'])
						maxResults(5)
						order("id", "desc")
						lt("execution.id", execId.toLong())
					}
				}
			}
			execResults = execResults.reverse();
			execResults?.each { def result->
				Execution execution = result?.execution
				dataMap.put(execution.name, result?.status)
			}
		}
		render(template: "showScriptTrend", model: [dataMap : dataMap])
	}
	
	/**
	 * Method to display the script execution details in the popup.
	 * @return
	 */
	def showLog(){
		String realPathForLogs = getRealPathForLogs()
		Execution executionInstance = Execution.findById(params?.id)
		String executionNameCheck = executionInstance?.name
        def repeatCount
        def repeatCountInt
		String repeatExecution = "false"
		def statusListForPopUpExecution = []
        if(executionNameCheck.contains("(R")){
	        def executionNameCheckList = executionNameCheck.split("\\(R")
	        if(executionNameCheckList[1].contains(")")){
		        def executionNameCheckListTwo = executionNameCheckList[1].split("\\)")
		        repeatCount = executionNameCheckListTwo[0]
	        }
	        repeatCountInt = Integer.parseInt(repeatCount)
        }
		if(repeatCountInt > 1){
			repeatExecution = "true"
		}
		//	if(!executionInstance.isPerformanceDone){
		executionService.setPerformance(executionInstance,request.getRealPath('/'))
		//}
		def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def device = Device.findByStbName(executionInstance?.device)
		def testGroup

		def executionResultMap = [:]
		def statusResultMap = [:]

		def totalStatus = ["ALL"]
		def totalStatusList = ["SUCCESS", "FAILURE", "N/A", "SKIPPED", "PENDING", "TIMED OUT", "UNDEFINED"]
		def listStatusCount = [:]

		executionDeviceList.each { executionDevice ->
			ArrayList executionList = new ArrayList(executionDevice.executionresults);
//			executionResultMap.put(executionDevice, executionList)

			listStatusCount = executedbService.getStatusList(executionInstance,executionDevice,executionList.size().toString())
			totalStatusList.each {
				def status = it;
				def statusCount = listStatusCount.get(status)
				if(status == "TIMED OUT"){
					status = "SCRIPT TIME OUT"
				}
				if(statusCount!= null && Integer.parseInt(statusCount) > 0) {
					if(totalStatus.indexOf(status) == -1) {
						totalStatus.add(status)
					}
				}
			}
			statusListForPopUpExecution = totalStatus.collect()
			if(statusListForPopUpExecution){
				if(statusListForPopUpExecution.contains("N/A")){
					def indexOfNA = statusListForPopUpExecution.indexOf("N/A")
					statusListForPopUpExecution.remove(indexOfNA)
				}
				if(statusListForPopUpExecution.contains("SKIPPED")){
					def indexOfSKIPPED = statusListForPopUpExecution.indexOf("SKIPPED")
					statusListForPopUpExecution.remove(indexOfSKIPPED)
				}
				if(statusListForPopUpExecution.contains("ALL")){
					def indexOfALL = statusListForPopUpExecution.indexOf("ALL")
					statusListForPopUpExecution.remove(indexOfALL)
				}
			}
			statusResultMap.put(executionDevice, listStatusCount)
		}

		if(executionInstance?.script){
			def script = Script.findByName(executionInstance?.script)
			testGroup = script?.primitiveTest?.module?.testGroup
		}
		def detailDataMap = executedbService.prepareDetailMap(executionInstance,request.getRealPath('/'))
		def tDataMap = [:]
		int total = 0
		detailDataMap?.keySet()?.each { k ->
			Map mapp = detailDataMap?.get(k)
			int tCount = 0
			mapp?.keySet()?.each { status ->
				def tStatusCounter = tDataMap.get(status)
				def statusCounter = mapp.get(status)
				if(!tStatusCounter){
					tStatusCounter = 0
				}
				if(!status.equals(Constants.PENDING)){
					tCount = tCount + statusCounter
					tStatusCounter = tStatusCounter + statusCounter
					tDataMap.put(status, tStatusCounter)
				}
			}
			int na = 0
			if(mapp?.keySet().contains(Constants.NOT_APPLICABLE_STATUS)){
				na = mapp?.get(Constants.NOT_APPLICABLE_STATUS)
			}
			mapp.put(Constants.EXECUTED, tCount)
			def success = mapp?.get(Constants.SUCCESS_STATUS)
			if(success){
				int rate = 0
				if(tCount > 0){
					if(mapp?.keySet().contains(Constants.NOT_APPLICABLE_STATUS)){
						na = mapp?.get(Constants.NOT_APPLICABLE_STATUS)
					}
					rate = ((success * 100)/(tCount - na))
				}
				mapp.put(Constants.PASS_RATE_SMALL,rate)
			}
			total = total + tCount
		}
		tDataMap.put(Constants.EXECUTED, total)
		int rate
		if(tDataMap?.get(Constants.SUCCESS_STATUS)){
			int success = tDataMap?.get(Constants.SUCCESS_STATUS)
			int na = 0
			if(tDataMap?.keySet().contains(Constants.NOT_APPLICABLE_STATUS)){
				na = tDataMap?.get(Constants.NOT_APPLICABLE_STATUS)
			}
			rate = ((success * 100)/(total - na))
		}
		tDataMap.put(Constants.PASS_RATE_SMALL,rate)
		
		boolean isProfilingDataPresent = false
		List executionResultList =  ExecutionResult.findAllByExecution(executionInstance)
		List profilingFileList = []
		List alertList = []
		executionResultList.each{ executionResult ->
			List performanceList = Performance.findAllByExecutionResultAndPerformanceType(executionResult,GRAFANA_DATA)
			if(!performanceList.isEmpty()){
				isProfilingDataPresent = true
			}
			
			def executionDeviceId = executionResult.executionDevice.id
			def logPath = realPathForLogs + "/logs//${executionInstance.id}//${executionDeviceId}//${executionResult.id}//"
			List alertListFromFile = executescriptService.fetchAlertDataForExecResult(executionInstance.id,logPath);
			if(!alertListFromFile.isEmpty()){
				alertList?.add(executionResult.id)
			}
			
			def finalLogparserFileName = ""
			File logDir  = new File(logPath)
			if(logDir?.exists() &&  logDir?.isDirectory()){
				logDir.eachFile{ file->
					if(file?.getName()?.contains("smemData") || file?.getName()?.contains("pmapData") || file?.getName()?.contains("systemdAnalyze") || file?.getName()?.contains("systemdBootchart") || file?.getName()?.contains("lmbench")){
						profilingFileList?.add(executionResult.id)
					}
				}
			}
		}		
		[repeatExecution: repeatExecution, repeatCount: repeatCountInt, tDataMap : tDataMap, statusResults : statusResultMap, executionInstance : executionInstance, executionDeviceInstanceList : executionDeviceList, testGroup : testGroup,executionresults:executionResultMap , statusList: totalStatus, statusListForPopUpExecution : statusListForPopUpExecution,isProfilingDataPresent:isProfilingDataPresent,profilingFileList:profilingFileList,alertList:alertList, realPathForLogs : realPathForLogs]
	}

	/**
	 * Method to display the script execution details in the popup.
	 * @return
	 */
	def showResult(final String execName,final String scrGrp){
		String realPathForLogs = getRealPathForLogs()
		Execution executionInstance = Execution.findByName(execName)
		def executionDevice = ExecutionDevice.findAllByExecution(executionInstance)
		def device = Device.findByStbName(executionInstance?.device)
		def testGroup
		if(executionInstance?.script){
			def script = Script.findByName(executionInstance?.script)
			testGroup = script?.primitiveTest?.module?.testGroup
		}
		[executionInstance : executionInstance, executionDeviceInstanceList : executionDevice, testGroup : testGroup , realPathForLogs : realPathForLogs]
	}

	/**
	 * Show the log files
	 * @return
	 */
	def showExecutionLog()  {
		try {
			String fileName = params?.id
			int index = fileName.indexOf( UNDERSCORE )
			def executionId = fileName.substring( 0, index )
			String realPathForLogs = getRealPathForLogs()
			String filePath = realPathForLogs + "//logs//${params?.execId}//${params?.execDeviceId}//${params?.execResultId}//"+params?.id
			def file = new File(filePath)
			if(!file?.exists()){
				String name =  params?.id.substring(index+1, params?.id?.length())
				filePath = realPathForLogs + "//logs//stblogs//${params?.execId}//${params?.execDeviceId}//${params?.execResultId}//"+name
				file = new File(filePath)
			}
			response.setContentType("html/text")
			response.setHeader("Content-disposition", "attachment;filename=${file.getName()}")
			response.outputStream << file.newInputStream()
		} catch (FileNotFoundException fnf) {
			response.sendError 404
		}
	}


	/**
	 * Show the log files
	 * @return
	 */
	def showCrashExecutionLog()  {
		try {
			String fileName = params?.id
			int index = fileName.indexOf( UNDERSCORE )
			def executionId = fileName.substring( 0, index )
			String realPathForLogs = getRealPathForLogs()
			String filePath = realPathForLogs + "//logs//crashlogs//${params?.execId}//${params?.execDeviceId}//${params?.execResultId}//"+params?.id
			def file = new File(filePath)
			response.setContentType("html/text")
			response.setHeader("Content-disposition", "attachment;filename=${file.getName()}")
			response.outputStream << file.newInputStream()
		} catch (FileNotFoundException fnf) {
			response.sendError 404
		}
	}

	/**
	 * TO DO : Remove this once the device status checking is done.
	 * Reset the device status to FREE.
	 * Called only when the user is sure that the test execution ended
	 * without giving any result or the device is not reachable
	 * @param id
	 * @return
	 */
	def resetDevice(Long id) {
		def deviceInstance = Device.get(id)
		if (!deviceInstance) {
			flash.message = message(code: 'default.not.found.message', args: [message(code: 'device.label', default: 'Device'), deviceInstance.stbName])
			redirect(action: "list")
			return
		}
		else{
			Device.withTransaction { status ->
				try {
					deviceInstance.deviceStatus = Status.FREE
					deviceInstance.save(flush:true)
					status.flush()
				}
				catch(Throwable th) {
					status.setRollbackOnly()
				}
			}
		}
	}

	/**
	 * REST API : To set the execution result status as Not Applicable
	 * @param execResult
	 * @param resultStatus
	 * @param reason
	 */
	def setExecutionResultStatus(final String execResult, final String resultStatus, final String reason){
		try{
			if((resultStatus.equals(Constants.NOT_APPLICABLE_STATUS_NO_SLASH))){
				ExecutionResult.withTransaction { resultstatus ->
					try {
						ExecutionResult executionResult = ExecutionResult.findById(execResult)
						if(executionResult){
							executionResult.status = Constants.NOT_APPLICABLE_STATUS
							if(reason && reason != ""){
								executionResult.executionOutput = Constants.TEST_NOT_EXECUTED_REASON+reason
							}
							if(!executionResult.save(flush:true)) {
								log.error "Error saving executionResult instance : ${executionResult.errors}"
							}
							resultstatus.flush()
						}
					}
					catch(Throwable th) {
						resultstatus.setRollbackOnly()
					}
				}
			}
		}catch(Exception e){
			e.printStackTrace()
		}
	}

	/**
	 * Check device is enable or not
	 * 
	 */


	def resetDeviceStatus(Long id){

		def deviceInstance = Device.get(id)
		if (!deviceInstance) {
			flash.message = message(code: 'default.not.found.message', args: [message(code: 'device.label', default: 'Device'), deviceInstance.stbName])
			redirect(action: "list")
			return
		}
		else{
			Device.withTransaction { status ->
				try {
					deviceInstance.deviceStatus = Status.TDK_DISABLED
					deviceInstance.save(flush:true)
					status.flush()
				}
				catch(Throwable th) {
					status.setRollbackOnly()
				}
			}
		}
	}


	/**
	 * REST API : To save the load module status
	 * @param executionId
	 * @param resultData
	 * @return
	 */
	def saveLoadModuleStatus(final String execId, final String statusData, final String execDevice, final String execResult){
		//		executescriptService.saveLoadModuleStatus(execId, statusData, execDevice, execResult)

		try {
			Execution.withTransaction{
				Execution execution = Execution.findById(execId)
				if(execution && !(execution?.result?.equals( FAILURE_STATUS ))){
					execution?.result = statusData?.toUpperCase().trim()
					execution?.save(flush:true)
				}
				
				ExecutionDevice execDeviceInstance = ExecutionDevice.findByExecutionAndId(execution,execDevice)
				if(execDeviceInstance && !(execDeviceInstance?.status.equals( FAILURE_STATUS ))){
					execDeviceInstance?.status = statusData?.toUpperCase().trim()
					execDeviceInstance?.save(flush:true)
				}

				ExecutionResult executionResult = ExecutionResult.findById(execResult)
				if(executionResult && !(executionResult?.status.equals( FAILURE_STATUS ))  && !(executionResult?.status.equals( NOT_APPLICABLE_STATUS ))){
					executionResult?.status = statusData?.toUpperCase().trim()
					executionResult?.save(flush:true)
				}
				if(execution && execution?.result?.equals( FAILURE_STATUS )){
					def allExecutionResults = []
					def naExecutionResults = []
					def successExecutionResults = []
					def skippedExecutionResults = []
					int totalScriptsCount = 0
					int naScriptsCount = 0
					int successScriptsCount = 0
					int skippedScriptsCount = 0
					int naAndSkippedAndSuccessSum = 0
					allExecutionResults = ExecutionResult.findAllByExecution(execution)
					naExecutionResults = ExecutionResult.findAllByExecutionAndStatus(execution,NOT_APPLICABLE_STATUS)
					successExecutionResults = ExecutionResult.findAllByExecutionAndStatus(execution,SUCCESS_STATUS)
					skippedExecutionResults = ExecutionResult.findAllByExecutionAndStatus(execution,SKIPPED_STATUS)
					totalScriptsCount = allExecutionResults?.size()
					naScriptsCount = naExecutionResults?.size()
					successScriptsCount = successExecutionResults?.size()
					skippedScriptsCount = skippedExecutionResults?.size()
					boolean setAsSuccess = false
					naAndSkippedAndSuccessSum = naScriptsCount + skippedScriptsCount + successScriptsCount
					if( (successScriptsCount > 0) && (totalScriptsCount == naAndSkippedAndSuccessSum)){
						setAsSuccess = true
					}
					if(setAsSuccess == true){
						if(execDeviceInstance && execDeviceInstance?.status.equals( FAILURE_STATUS )){
							execDeviceInstance?.status = SUCCESS_STATUS
							execDeviceInstance?.save(flush:true)
						}
						execution?.result = SUCCESS_STATUS
						execution?.save(flush:true)
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	/**
	 * REST API : To save the result details
	 * @param executionId
	 * @param resultData
	 * @return
	 */
	def saveResultDetails(final String execId, final String resultData, final String execResult,
			final String expectedResult, final String resultStatus, final String testCaseName, final String execDevice)
	{
		try{
			if(resultData){
				String actualResult = resultData
				if(actualResult){
					ExecutionResult.withTransaction {
						ExecutionResult executionResult = ExecutionResult.findById(execResult)
						if(executionResult){
							ExecuteMethodResult executionMethodResult = new ExecuteMethodResult()
							if(resultStatus?.equals( STATUS_NONE ) || resultStatus == null ){
								executionMethodResult.status = actualResult
							}
							else{
								executionMethodResult.executionResult = executionResult
								executionMethodResult.expectedResult = expectedResult
								executionMethodResult.actualResult = actualResult
								executionMethodResult.status = resultStatus
							}
							executionMethodResult.functionName = testCaseName
							executionMethodResult.category = executionResult?.category
							executionMethodResult.save(flush:true)

							executionResult?.addToExecutemethodresults(executionMethodResult)
							executionResult?.save(flush:true)

							Execution execution = Execution.findById(execId)
							ExecutionDevice execDeviceInstance = ExecutionDevice.findById(execDevice)
							if(!executionResult?.status.equals( FAILURE_STATUS )){
								executionResult?.status = resultStatus
								executionResult?.save(flush:true)
								if(!execution.result.equals( FAILURE_STATUS )){
									execution.result = resultStatus
									execution.save(flush:true)
								}
								if(!execDeviceInstance.status.equals( FAILURE_STATUS )){
									execDeviceInstance?.addToExecutionresults(executionResult)
									execDeviceInstance?.status = resultStatus
									execDeviceInstance?.save(flush:true)
								}
							}
						}
					}
				}
			}
			else{
				Execution.withTransaction {
					Execution execution = Execution.findById(execId)
					if(execution){
						execution.result = FAILURE_STATUS
						execution.save(flush:true)
					}
				}
			}
		}catch(Exception ex){
			ex.printStackTrace()
		}
	}

	/**
	 * Search execution list based on the execution name
	 * @return
	 */
	def searchExecutionList(){
		def executionList = []
		def executions = Execution.findAllByNameLike("%${params?.searchName.trim()}%",[max: 1000])
		if(executions?.size() > 0){
			executions.each{ execution ->
				executionList.add(execution)
			}
		}else{
			executions = Execution.findAllByScriptGroupLike("%${params?.searchName.trim()}%",[max: 1000])
			if(executions?.size() >0){
				executions.each{ execution ->
					executionList.add(execution)
				}
			}
			def executionResultList = ExecutionResult.findAllByScriptLike("%${params?.searchName.trim()}%",[sort: 'id', order: 'desc',max: 1000])
			if(executionResultList?.size() >0){
				executionResultList.each{ executionResultInstance ->
					if(!executionList.contains(executionResultInstance.execution)){
						executionList.add(executionResultInstance.execution)
					}
				}
			}
			else{
				String searchString = params?.searchName.trim()
				if(searchString?.equalsIgnoreCase("SUCCESS")){
					searchString = "COMPLETED"
				}
				executions = Execution.findAllByExecutionStatusLike("%${searchString}%",[max: 1000])
				if(executions?.size() >0){
					executions.each{ execution ->
						executionList.add(execution)
					}
				}else{
				searchString = searchString?.trim()
				def executionDevices = ExecutionDevice.findAllByBuildNameLike("%${searchString}%",[max: 1000])
				if(executionDevices?.size() >0){
					executionDevices.each{ execDev ->
						executionList.add(execDev?.execution)
					}
				}
				}
			}

		}
		render(template: "searchList", model: [executionInstanceList : executionList])
	}

	/**
	 * Search execution list based on different search criterias of
	 * script, device, and execution from and to dates.
	 * @return
	 */
	def multisearch(){
		String fromDate = ""
		String toDate = ""
		if(params?.fromDate && params?.toDate){
			String fromDateString = params?.fromDate?.trim()
			def fromDateList = fromDateString.split("/")
			def year = fromDateList[2]
			def month = fromDateList[0]
			def day = fromDateList[1]
			fromDate = year + "-" + month + "-" +day + " 00:00:00"
			String toDateString = params?.toDate?.trim()
			def toDateList = toDateString.split("/")
			year = toDateList[2]
			month = toDateList[0]
			day = toDateList[1]
			toDate = year + "-" + month + "-" +day + " 23:59:59"
		}
		def executionList = executionService.multisearch( toDate, fromDate, params?.deviceName?.trim(), params?.resultStatus?.trim(),
				params?.scriptType?.trim(), params?.scriptVal?.trim() )
		render(template: "searchList", model: [executionInstanceList : executionList])
	}


	/**
	 * TO DO : Remove this once the port forwarding is automated via config file during reboot.
	 * It is called during free state
	 * Called only when the user is want to reset all rules.
	 * 
	 * @param id
	 * @return
	 */
	def resetIPRule(Long id) {
		def device = Device.get(id)
		if (!device) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'device.label', default: 'Device'),
				device.stbName
			])
			redirect(action: "list")
			return
		}
		else{
			deviceStatusService.resetIPRule(device)
		}
	}

	/**
	 * Method export the execution details to excel format.
	 * This method will be called upon clicking excel export button in execution page.
	 * The method will parse all the child attributes of the execution object to corresponding maps.
	 * Finally all this data will be pushed to excel sheet at a particular format.
	 * The resulting excel sheet will be available in downloads folder of running browser.
	 * 
	 * @param id - Id of execution object.
	 * 
	 */
	def exportToExcel = {

		if(!params.max) params.max = 100000
		List dataList = []
		List fieldLabels = []
		Map fieldMap = [:]
		Map parameters = [:]
		List columnWidthList =  [0.35, 0.5]

		Execution executionInstance = Execution.findById(params.id)
		try {
			if(executionInstance){
				dataList = executedbService.getDataForExcelExport(executionInstance, getRealPath())
				fieldMap = ["C1":"     ", "C2":"     "]
				parameters = [ title: EXPORT_SHEET_NAME, "column.widths": columnWidthList ]
			}
			else{
				log.error "Invalid excution instance......"
			}
		} catch (Exception e) {
			println "ee "+e.getMessage()
			e.printStackTrace()
		}

		params.format = EXPORT_EXCEL_FORMAT
		params.extension = EXPORT_EXCEL_EXTENSION
		response.contentType = grailsApplication.config.grails.mime.types[params.format]

		def fileName = executionInstance.name
		fileName = fileName?.replaceAll(" ","_")
		response.setHeader("Content-disposition", "attachment; filename="+EXPORT_FILENAME+ fileName +".${params.extension}")
		exportService.export(params.format, response.outputStream,dataList, null,fieldMap,[:], parameters)
		log.info "Completed excel export............. "

		/*********** csv support***************************/                                //TODO Use this if csv support needed
		def type = params.type
		if(type){
			params.format = "csv"
			response.contentType = 'text/csv'

			def filName = "ExecutionReport-"+ executionInstance.name + ".csv"
			response.setHeader("Content-disposition", "attachment; filename="+filName+";sheetname=MySheet")
			exportService.export(params.format, response.outputStream,dataList, fieldLabels,fieldMap,[:], [:])
		}
	}

	// For CGRTS-521
	def getExecutionOutput(final String execResId){
		ExecutionResult executionResult = ExecutionResult.findById(execResId)
		def data

		if(executionResult){
			data = executionResult?.executionOutput
		}
		render data
	}


	/**
	 * Method to export the consolidated report in excel format.
	 */
	def exportConsolidatedToExcel = {
		if(!params.max) params.max = 100000
		Map dataMap = [:]
		List fieldLabels = []
		Map fieldMap = [:]
		Map parameters = [:]
		List columnWidthList = [0.08,0.4,0.15,0.2,0.15,0.8,0.2,0.2,0.2,0.8]
		boolean isRDKServiceExecution
		boolean isPatternPresent = false
		Execution executionInstance = Execution.findById(params.id)
		String executionInstanceStatus ;
		executionInstanceStatus =executedbService?.isValidExecutionAvailable(executionInstance)
		if(executionInstanceStatus?.equals(Constants.SUCCESS_STATUS)){
			if(executionInstance){
				ExecutionDevice executionDevice  = ExecutionDevice.findByExecution(executionInstance)
				List executionResultList =  ExecutionResult.findAllByExecutionAndExecutionDevice(executionInstance,executionDevice)
				for(int i=0;i<executionResultList.size();i++){
					ScriptFile scriptfile = ScriptFile.findByScriptName(executionResultList[i]?.script)
					String executionResultOutput = executionResultList[i]?.executionOutput
					if(scriptfile){
						if(scriptfile?.category?.toString()?.equals(RDKV_RDKSERVICE?.toString())){
							if(scriptfile?.moduleName?.equals((RDKSERVICES?.toString()))) {
								isPatternPresent = true
							}
							isRDKServiceExecution = true
						}else{
							isRDKServiceExecution = false
							break;
						}
					}
				}
				if(isRDKServiceExecution && isPatternPresent){
					columnWidthList = [0.08,0.4,0.15,0.15,0.9]
					dataMap = executedbService.getDataForRDKServiceConsolidatedListExcelExport(executionInstance, getRealPath(),getApplicationUrl())
					fieldMap = ["C1":" Sl.No ", "C2":" Test Case Name ","C3":"Status","C4":"Executed On","C5":" Log Data ","C6":"Jira #","C7":"Issue Type","C8":"Remarks"]
				}else{
					dataMap = executedbService.getDataForConsolidatedListExcelExport(executionInstance, getRealPath(),getApplicationUrl())
					fieldMap = ["C1":" Sl.No ", "C2":" Script Name ","C3":"Executed","C4":" Status ", "C5":"Executed On ","C6":"Log Data","C7":"Jira #","C8":"Issue Type","C9":"Remarks","C10":" Agent Console Log"]
				}
				parameters = [ title: EXPORT_SHEET_NAME, "column.widths": columnWidthList]

			}
			else{
				log.error "Invalid excution instance......"
			}

			params.format = EXPORT_EXCEL_FORMAT
			params.extension = EXPORT_EXCEL_EXTENSION
			response.contentType = grailsApplication.config.grails.mime.types[params.format]
			def fileName = executionInstance.name
			fileName = fileName?.replaceAll(" ","_")
			response.setHeader("Content-disposition", "attachment; filename="+EXPORT_FILENAME+ fileName +".${params.extension}")
			if(isRDKServiceExecution && isPatternPresent){
				excelExportService.exportRDKService(params.format, response.outputStream,dataMap, null,fieldMap,[:], parameters)
			}else{
				excelExportService.export(params.format, response.outputStream,dataMap, null,fieldMap,[:], parameters)
			}
			log.info "Completed excel export............. "
		}
		else{
			redirect(action: "create");
			flash.message= "No valid execution reports are available."
			return
		}

	}
	
	/**
	 * Method to export profiling data to excel
	 */
	def exportProfilingMetricsToExcel = {
		if(!params.max) params.max = 100000
		Map dataMap = [:]
		List fieldLabels = []
		Map fieldMap = [:]
		Map parameters = [:]
		List columnWidthList = [0.2,0.5,0.5,0.15,0.15,0.15,0.15,0.2,0.2,0.2]
		Execution executionInstance = Execution.findById(params.id)
		String executionInstanceStatus ;
		executionInstanceStatus =executedbService?.isValidExecutionAvailable(executionInstance)
		if(executionInstanceStatus?.equals(Constants.SUCCESS_STATUS)){
			if(executionInstance){
					dataMap = executedbService.getDataForProfilingMetricsExcelReportGeneration(executionInstance, getRealPath(),getApplicationUrl())
					fieldMap = ["C1":" Sl.No ", "C2":" Script Name ","C3":"Executed","C4":" Status ", "C5":"Executed On ","C6":"Log Data","C7":"Jira #","C8":"Issue Type","C9":"Remarks","C10":" Agent Console Log"]
					parameters = [ title: EXPORT_SHEET_NAME, "column.widths": columnWidthList]
			}
			else{
				log.error "Invalid excution instance......"
			}

			params.format = EXPORT_EXCEL_FORMAT
			params.extension = EXPORT_EXCEL_EXTENSION
			response.contentType = grailsApplication.config.grails.mime.types[params.format]
			def fileName = executionInstance.name
			fileName = fileName?.replaceAll(" ","_")
			response.setHeader("Content-disposition", "attachment; filename=ProfilingMetricsData-"+ fileName +".${params.extension}")
			excelExportService.exportProfilingMetrics(params.format, response.outputStream,dataMap, null,fieldMap,[:], parameters)
			log.info "Completed excel export............. "
		}
		else{
			redirect(action: "create");
			flash.message= "No valid execution reports are available."
			return
		}
	}
	
	/**
	 * Method used to populate individual execution result
	 */
	def resultSummary = {
		String realPathForLogs = getRealPathForLogs()
		Execution executionInstance = Execution.findById(params?.executionId)
		def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def device = Device.findByStbName(executionInstance?.device)
		def testGroup

		def executionResultMap = [:]
		def statusResultMap = [:]

		def logData = "Could not find the logs"
		def listStatusCount = [:]

		executionDeviceList.each { executionDevice ->
			ArrayList executionList = new ArrayList(executionDevice.executionresults);
			listStatusCount = executedbService.getStatusList(executionInstance,executionDevice,executionList.size().toString())

			statusResultMap.put(executionDevice, listStatusCount)
		}
		
		if(executionInstance?.script){
			def script = Script.findByName(executionInstance?.script)
			testGroup = script?.primitiveTest?.module?.testGroup
		}
		[statusResults : statusResultMap, executionInstance : executionInstance, executionDeviceInstanceList : executionDeviceList, testGroup : testGroup,executionresults:executionResultMap, baseUrl:params?.baseUrl, realPathForLogs:realPathForLogs]
	}

	/**
	 * Method to export the consolidated report in zip format.
	 */	
	def exportConsolidatedToZip = {

		String url =  "${request.getRequestURL()}"
		String hostname = url.split("://")[1].split(":")[0];
		String portnumber = url.split("://")[1].split(":")[1].split("/")[0];
		String protocol = url.split("://")[0]
		String appName = url.split("://")[1].split(":")[1].split("/")[1]

		String baseUrl = protocol + "://" +hostname + ":" + portnumber + "/" + appName + "/"
		String idVal = params?.id


		def executionId = idVal.replace("_zip", "")

		def urlNew = (baseUrl + "execution/resultSummary?executionId=" + executionId+"&baseUrl=" +baseUrl).toURL()
		def data = ""

		def result = []
		urlNew.eachLine {
			result << it
		}


		try {
			Execution exec = Execution.get(executionId)
			String fileName = exec?.name
			if(exec){
				ZipOutputStream zipFile = new ZipOutputStream(new FileOutputStream("result"))
				zipFile.putNextEntry(new ZipEntry(fileName + ".html"))
				def buffer = new byte[1024]
				
				for(int i=0; i< result.size(); i++){
					data = result[i] + "\n"
					zipFile.write(data.bytes, 0, data.bytes.size())
				}
				
				zipFile.closeEntry()
				zipFile.close()


				params.format = EXPORT_ZIP_FORMAT
				params.extension = EXPORT_ZIP_EXTENSION
				response.contentType = grailsApplication.config.grails.mime.types[params.format]
				fileName = fileName?.replaceAll(" ","_")
				def file = new File("result")
				response.setHeader("Content-Type", "application/zip")
				response.setHeader("Content-disposition", "attachment; filename=ExecutionLogs_"+ fileName +".zip")
				response.outputStream << file.newInputStream()
				response.outputStream.flush()
				flash.message = "Exported successfully"
			} else {
				flash.message =  "Couldn't find exceution!!"
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
	/**
	 * Method to export the consolidated report in excel format.
	 */
	def exportConsolidatedPerfToExcel = {
		if(!params.max) params.max = 100000
		Map dataMap = [:]
		List fieldLabels = []
		Map fieldMap = [:]
		Map parameters = [:]
		List columnWidthList = [0.08,0.4,0.15,0.2,0.2,0.2,0.8,0.15,0.2,0.2,0.8]

		Execution executionInstance = Execution.findById(params.id)
		String executionInstanceStatus ;
		executionInstanceStatus =executedbService?.isValidExecutionAvailable(executionInstance)
		if(executionInstanceStatus?.equals(Constants.SUCCESS_STATUS)){

			if(executionInstance){
				dataMap = executedbService.getDataForConsolidatedListPerformanceExcelExport(executionInstance, getRealPath(),getApplicationUrl())
				fieldMap = ["C1":" Sl.No ", "C2":" Script Name ","C3":"Executed","C4":" Status ","C5":"Script Execution Time","C6":"Executed On ","C7":"Log Data","C8":"Jira #","C9":"Issue Type","C10":"Remarks","C11":" Agent Console Log"]

				parameters = [ title: EXPORT_SHEET_NAME, "column.widths": columnWidthList]
			}
			else{
				log.error "Invalid excution instance......"
			}

			params.format = EXPORT_EXCEL_FORMAT
			params.extension = EXPORT_EXCEL_EXTENSION
			response.contentType = grailsApplication.config.grails.mime.types[params.format]
			def fileName = executionInstance.name
			fileName = fileName?.replaceAll(" ","_")
			response.setHeader("Content-disposition", "attachment; filename="+EXPORT_FILENAME+ fileName +".${params.extension}")
			excelExportService.export(params.format, response.outputStream,dataMap, null,fieldMap,[:], parameters)
			log.info "Completed excel export............. "
		}
		else{
			redirect(action: "create");
			flash.message= "No valid execution reports are available."
			return
		}

	}
	
	/**
	 * To download the test result comparison report
	 */
	def exportComparisonReport = {
		if(!params.max) params.max = 100000
		Map dataMap = [:]
		List fieldLabels = []
		Map fieldMap = [:]
		Map parameters = [:]
		List columnWidthList = [0.08,0.4,0.2]

		Execution executionInstance = Execution.findById(params.id)
		Execution [] executionList = Execution.findAllByScriptGroupAndNameNotEqualAndExecutionStatusNotEqual(executionInstance.scriptGroup,executionInstance?.name,Constants.ABORTED_STATUS,[max: 5, sort: "id", order: "desc"])
		def nameList = executionList?.name
		def colNameList = ["C4","C5","C6","C7","C8"]
		def fieldList = ["C1","C2","C3"]
		String executionInstanceStatus ;
		executionInstanceStatus =executedbService?.isValidExecutionAvailable(executionInstance)
		if(executionInstanceStatus?.equals(Constants.SUCCESS_STATUS)){

			if(executionInstance){
				int i = 0
				fieldMap = ["C1":" Sl.No ", "C2":" Script Name ","C3":executionInstance?.name]
				nameList?.each{ name ->
					fieldMap.put(colNameList.get(i), name)
					fieldList.add(colNameList.get(i))
					columnWidthList.add(0.2)
					i++
				}
				
				dataMap = executedbService.getDataForComparisonExcelExport(executionList, executionInstance , getRealPath(),getApplicationUrl(),fieldList)
				parameters = [ title: EXPORT_SHEET_NAME, "column.widths": columnWidthList]
			}
			else{
				log.error "Invalid excution instance......"
			}

			params.format = EXPORT_EXCEL_FORMAT
			params.extension = EXPORT_EXCEL_EXTENSION
			response.contentType = grailsApplication.config.grails.mime.types[params.format]
			def fileName = executionInstance.name
			fileName = fileName?.replaceAll(" ","_")
			response.setHeader("Content-disposition", "attachment; filename="+EXPORT_COMPARE_FILENAME+ fileName +".${params.extension}")
			excelExportService.export(params.format, response.outputStream,dataMap, null,fieldMap,[:], parameters)
			log.info "Completed excel export............. "
		}
		else{
			redirect(action: "create");
			flash.message= "No valid execution reports are available."
			return
		}

		
	}
	
	/**
	 * Method to perform delete operation for marked results.
	 * This method will be invoked by an ajax call.
	 * It removes all the child objects of given execution instance.
	 * 
	 * @param - Ids of checked execution results.
	 * @return - JSON message
	 * 
	 */
	def deleteExecutioResults = {

		List executionResultList = []
		List executionMethodResultInstanceList = []
		def selectedRows
		List returnMsg = []
		int deleteCount = 0
		String message

		if(params?.checkedRows != UNDEFINED && params?.checkedRows != BLANK_SPACE && params?.checkedRows != null){

			selectedRows = params?.checkedRows.split(COMMA_SEPERATOR)
			deleteCount =  executedbService.deleteSelectedRowOfExecutionResult(selectedRows,getRealPath())

			if(deleteCount == 1){
				message = deleteCount+" Result Deleted"
			}
			else if (deleteCount > 1){
				message =  deleteCount+" Results Deleted"
			}
			else{
				message = "Delete failed"
				flash.message="Delete failed due to the pending execution"
			}

			returnMsg.add( message)
			render returnMsg as JSON
		}
		else{
			log.info "Invalid marking of results for deletion"
		}
	}
	
	/**
	 * Method which filters executions based on FromDate, ToDate, boxType, Category and script type
	 */

	def filterExecutions(){
		def validate = params?.validate
		def checker = 0
		String messageDiv = ""
		List executionList =[]
		List executionIdList = []
		SimpleDateFormat myFormat = new SimpleDateFormat("MM/dd/yyyy");
		String dateBeforeString = params?.generateFromDate?.trim()
		String dateAfterString = params?.generateToDate?.trim()
		Date dateBefore = myFormat.parse(dateBeforeString);
		Date dateAfter = myFormat.parse(dateAfterString);
		long difference = dateAfter.getTime() - dateBefore.getTime();
		float daysBetween = (difference / (1000*60*60*24));
		daysBetween=(int)daysBetween;
		if(daysBetween > 30){
			checker = 1;
			messageDiv = "Maximum number of days allowed is 30"
		}
		else{
			String fromDateString = params?.generateFromDate?.trim()
			def fromDateList = fromDateString.split("/")
			def year = fromDateList[2]
			def month = fromDateList[0]
			def day = fromDateList[1]
			String fromDate = year + "-" + month + "-" +day + " 00:00:00"
			String toDateString = params?.generateToDate?.trim()
			def toDateList = toDateString.split("/")
			year = toDateList[2]
			month = toDateList[0]
			day = toDateList[1]
			String toDate = year + "-" + month + "-" +day + " 23:59:59"
			executionList = executionService.filterExecutions( fromDate, toDate, params?.boxType?.trim(), params?.category?.trim(),params?.scriptTypeValue?.trim(),params?.scriptValue?.trim())		
			executionList.each {eachExecution ->
				executionIdList.add(eachExecution.id)
			}
		}
		render(template: "combinedExcelList", model: [executionInstanceList : executionList,executionIdList : executionIdList,checker:checker,messageDiv:messageDiv,validate:validate])
	}	
	
	/**
	 * Method to check whether the selected executions have the same device type. 
	 * The list of all the selected executions is passed as params from the gsp page. This method is invoked 
	 * from the execution_resolver.js
	 */
	def checkValidExecutions(){
		def selectedRows
		def selectedRowsDefined = []
		String sameType
		if(params?.checkedRows != UNDEFINED && params?.checkedRows != BLANK_SPACE && params?.checkedRows != null){
			selectedRows = params?.checkedRows.split(COMMA_SEPERATOR)
			if((selectedRows.size() > 10) || (selectedRows.size() < 2)){
				sameType = "overFlow"
			}
			else{
				sameType = "true"
			}
		}
		render sameType
		return
	}
	
	/**
	 * Method to export the combined report of the selected executions in excel format. The selected executions
	 * must of the same device type. This method is called from execution_resolver.js
	 */

	def combinedExcelReportGeneration = {
		def selectedRows
		def selectedRowsDefined = []
		def executionInstance
		def executionDevice
		Map dataMap = [:]
		Map fieldMap = [:]
		Map parameters = [:]
		List fieldLabels = []
		List columnWidthList = [0.08,0.4,0.15,0.2,0.15,0.8,0.2,0.2,0.2,0.8]
		if(params?.checkedRows != UNDEFINED && params?.checkedRows != BLANK_SPACE && params?.checkedRows != null){
			selectedRows = params?.checkedRows.split(COMMA_SEPERATOR)
			for(int i=0;i<selectedRows.size();i++){
				if(selectedRows[i] != UNDEFINED){
					selectedRowsDefined.add(selectedRows[i])
				}
			}
			dataMap = executedbService.getDataForCombinedExcelReportGeneration(selectedRowsDefined ,getApplicationUrl(), getRealPath())
			//For excel generation
			fieldMap = ["C1":" Sl.No ", "C2":" Script Name ","C3":"Executed","C4":" Status ", "C5":"Executed On ","C6":"Log Data","C7":"Jira #","C8":"Issue Type","C9":"Remarks","C10":" Agent Console Log","C11":"Rerun/Repeat"]
			parameters = [ title: EXPORT_SHEET_NAME, "column.widths": columnWidthList]

			params.format = EXPORT_EXCEL_FORMAT
			params.extension = EXPORT_EXCEL_EXTENSION
			response.contentType = grailsApplication.config.grails.mime.types[params.format]
			def executionInstanceId = selectedRowsDefined.get(0)
			executionInstance = Execution.findById(executionInstanceId)
			def fileName = ""
			if(executionInstance){
				fileName = executionInstance.name
			}
			fileName = fileName?.replaceAll(" ","_")
			response.setHeader("Content-disposition", "attachment; filename="+COMBINED_EXPORT_FILENAME+ fileName +".${params.extension}")
			excelExportService.export(params.format, response.outputStream,dataMap, null,fieldMap,[:], parameters)
			log.info "Completed excel export............. "
		}
	}
	
	/**
	 * Method to export the comparison report of the selected executions in excel format.
	 * 
	 */
	def comparisonExcelReportGeneration = {
		Map dataMap = [:]
		Map fieldMap = [:]
		Map parameters = [:]
		List fieldLabels = []
		List columnWidthList = [0.08,0.2,0.4,0.08,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2]
		if(params?.comparisonExecutionNames != UNDEFINED && params?.comparisonExecutionNames != BLANK_SPACE && params?.comparisonExecutionNames != null && params?.baseExecutionName != null){
			def baseExecutionName = params?.baseExecutionName
			def comparisonExecutionNames = params?.comparisonExecutionNames
			List comparisonExecutionNameList = comparisonExecutionNames?.split(",")
			dataMap = executedbService.getDataForComparisonReportGeneration(baseExecutionName, comparisonExecutionNameList,getApplicationUrl(), getRealPath())
			if(!(dataMap.isEmpty())){
				parameters = [ title: EXPORT_SHEET_NAME, "column.widths": columnWidthList]
	
				params.format = EXPORT_EXCEL_FORMAT
				params.extension = EXPORT_EXCEL_EXTENSION
				response.contentType = grailsApplication.config.grails.mime.types[params.format]
				def fileName = baseExecutionName
				response.setHeader("Content-disposition", "attachment; filename="+COMPARISON_EXPORT_FILENAME+ fileName +".${params.extension}")
				excelExportService.exportComparison(params.format, response.outputStream,dataMap, null,fieldMap,[:], parameters)
				log.info "Completed excel export............. "
			}
			else{
			    redirect(controller:'trends' , action:'chart');
				flash.message= "No valid execution reports are available."
				return
			}
		}
	}
	/**
	 * Ajax call to update the isMarked status of execution instance.
	 * This will be called during mark operation of corresponding checkbox of execution results.
	 */
	def updateMarkStatus = {
		int markStatus
		markStatus = Integer.parseInt(params?.markStatus)
		try {
			Execution.withTransaction {
				Execution executionInstance = Execution.findById(params?.id)
				if(executionInstance){
					executionInstance.isMarked = markStatus
					executionInstance.save(flush:true)
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	/**
	 * Download the execution result details in xml format
	 * @return
	 */
	def writexmldata(){
		String writer = executedbService.getExecutionDataInXmlFormat(params?.execName)
		response.setHeader "Content-disposition", "attachment; filename=${params?.execName}.xml"
		response.contentType = 'text/xml'
		response.outputStream << writer.toString()
		response.outputStream.flush()
	}

	def readOutputFileData(String executionName){
		String output = "";
		try{
			String pathName = Constants.SCRIPT_OUTPUT_FILE_PATH+executionName+Constants.SCRIPT_OUTPUT_FILE_EXTN
			File opFile = grailsApplication.parentContext.getResource(pathName).file
			List opList ;
			if(opFile.exists()){
				opList = opFile.readLines();
			}else{
				opList = []
				String opFolderName = Constants.SCRIPT_OUTPUT_FILE_PATH
				File opFolder = grailsApplication.parentContext.getResource(opFolderName).file
				if(opFolder.exists()){
					File[] files = opFolder.listFiles(new CustomFileNameFilter(executionName));
					for (int i=0; i< files.length;i++) {
						List opList1 = files[i].readLines();
						if(opList1 != null && opList1.size() > 0){
							opList.addAll(opList1);
						}
					}
				}
			}

			for (var in opList) {
				output = output + var
			}
		}catch(Exception e){
		}
		render output as String
	}

	/**
	 * REST Api : Get the detailed result based on a execution Result
	 * @param execResId
	 * @return
	 */
	def getDetailedTestResult(final String execResId){
		JsonObject resultNode = new JsonObject()
		if(execResId){
			ExecutionResult executionResult = ExecutionResult.findById(execResId)
			JsonArray jsonArray = new JsonArray()
			JsonObject functionNode = new JsonObject()

			resultNode.addProperty("ExecutionName",executionResult?.execution?.name.toString())
			resultNode.addProperty("Device",executionResult?.device.toString())
			resultNode.addProperty("Script",executionResult?.script.toString())
			resultNode.addProperty("Status",executionResult?.status.toString())
			executionResult?.executemethodresults.each{ execMethdRslt ->
				functionNode = new JsonObject()
				functionNode.addProperty("FunctionName", execMethdRslt?.functionName.toString())
				functionNode.addProperty("ExpectedResult", execMethdRslt?.expectedResult.toString())
				functionNode.addProperty("ActualResult", execMethdRslt?.actualResult.toString())
				functionNode.addProperty("Status", execMethdRslt?.status.toString())
				jsonArray.add(functionNode)
			}
			resultNode.add("Functions",jsonArray)
			resultNode.addProperty("LogData",executionResult?.executionOutput.toString())
			//agent console link added
			def executionInstance = Execution.findById(executionResult?.execution?.id)
			def deviceInstance
			if(executionResult?.device.toString()){
				deviceInstance = Device.findByStbName(executionResult?.device.toString())
			}
			if(deviceInstance?.isThunderEnabled != 1){
				resultNode.addProperty("agentConsoleLogURL",executionInstance?.applicationUrl+"/execution/getAgentConsoleLog?execResId="+executionResult?.id)
			}
		}
		render resultNode
	}

	def getAgentConsoleLog(final String execResId){

		ExecutionResult executionResult = ExecutionResult.findById(execResId)

		def agentConsoleFileData = "No AgentConsoleLog available"

		if(executionResult){

			try {
				agentConsoleFileData = executionService.getAgentConsoleLogData( request.getRealPath('/'), executionResult?.execution?.id?.toString(), executionResult?.executionDevice?.id?.toString(),executionResult?.id?.toString())
				if(agentConsoleFileData){
					agentConsoleFileData =agentConsoleFileData.trim()
					if(agentConsoleFileData.length() == 0){
						agentConsoleFileData = "No AgentConsoleLog available"
					}
				}else{
					agentConsoleFileData = "No AgentConsoleLog available"
				}
			} catch (Exception e) {
				e.printStackTrace()
			}
		}else{
			agentConsoleFileData = "No execution result available with the given execResId"
		}
		render agentConsoleFileData
	}

	/**
	 * REST Api : Get the detailed result based on a execution Result
	 * @param execResId
	 * @return
	 */

	def getClientPort(final String deviceIP,final String agentPort){
		JsonObject resultNode = null
		if(deviceIP && agentPort){
			Device device = Device.findByStbIpAndStbPort(deviceIP,agentPort)
			if(device){
				resultNode = new JsonObject()
			//	resultNode.addProperty("logTransferPort",device?.logTransferPort.toString())
				resultNode.addProperty("logTransferPort",device?.agentMonitorPort?.toString())
				resultNode.addProperty("statusPort",device?.statusPort.toString())
			}
		}
		render resultNode
	}
	/**
	 * check the box is enabled/disabled
	 */
	def getTDKDeviceStatus()
	{
		try{
			File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//setTDKStatus.py").file
			def absolutePath = layoutFolder.absolutePath
			Device device = Device.get(params?.select)
			def option = params?.option
			String[] cmd= [
				"python",
				absolutePath,
				device,
				device?.statusPort,
				option
			]

			ScriptExecutor scriptExecutor = new ScriptExecutor()
			def outputData = scriptExecutor.executeScript(cmd,1)
		}

		catch(Exception e){
			println e.getMessage()
			e.printStackTrace()
		}
	}
	
	/**
	 * Returns IP address of a device 
	 * @return
	 */
	def copyDeviceIp()
	{
		String deviceIp
		try{
			Device device = Device.findById(params?.deviceId)
			deviceIp = device?.stbIp
		}catch(Exception e){
			e.printStackTrace()
		}
		render deviceIp
	}

	/**
	 * method to stop the execution through ui request
	 */
	def stopExecution(){
		Execution execution = Execution.findById(params?.execid)
		def listdate = []
		if(execution?.executionStatus.equals(INPROGRESS_STATUS)){
			def executionId = params?.execid?.toString()
			if(!executionService.abortList.contains(executionId)){
				executionService.abortList.add(executionId)
			}else{
				listdate.add("Request to stop already in progress")
			}
		}else if(execution?.executionStatus.equals("PAUSED")){
			executionService.saveExecutionStatus(true, execution?.id)
		}

		render listdate as JSON
	}
	
/**
 * REST API to change device IP dynamically
 * @param deviceName
 * @param newDeviceIP
 * @return
 */
	def changeDeviceIP(final String deviceName, final String newDeviceIP){
		JsonObject result = new JsonObject()
		if(deviceName && newDeviceIP && deviceName!=null && newDeviceIP!=null){
			try{
				Device?.withTransaction{
					Device deviceInstance = Device.findByStbName(deviceName)
					if(deviceInstance){
						def stbIps = Device.findAllByStbIp(newDeviceIP)
						if(stbIps){
							result.addProperty("Status", "FAILURE")
							result.addProperty("Remarks", "Device IP "+newDeviceIP+" already exists")
						}else{
							deviceInstance.stbIp = newDeviceIP
							if(!deviceInstance.save(flush:true)){
								result.addProperty("Status", "FAILURE")
								result.addProperty("Remarks", "Unable to change device IP")
								deviceInstance.errors.each{
									println it
								}
							}else{
								result.addProperty("Status", "SUCCESS")
								result.addProperty("Remarks", "Changed device IP to "+newDeviceIP)
							}
						}
					}else{
						result.addProperty("Status", "FAILURE")
						result.addProperty("Remarks", "Device not found")
					}
				}
			}catch(Exception e){
				e.printStackTrace()
			}
		}else{
			result.addProperty("Status", "FAILURE")
			result.addProperty("Remarks", "Device name or IP empty")
		}
		render result
	}

	/**
	 * REST API to request for stopping the test execution 
	 * @param executionName
	 * @return
	 */
	def stopThirdPartyTestExecution(final String executionName){
		JsonObject result = new JsonObject()
		result.addProperty("ExecutionName", executionName)
		try {
			Execution execution = Execution.findByName(executionName)
			if(execution?.executionStatus.equals(INPROGRESS_STATUS)){

				if(execution?.script && !execution?.script?.equals(MULTIPLESCRIPT) ){
					try {

						if(!executionService.abortList.contains(execution?.id?.toString())){
							executionService.abortList.add(execution?.id?.toString())
							result.addProperty("Status", "Requested for abort")
						}else{
							result.addProperty("Status", "Request to stop already in progress")
						}

						if(executionService.executionProcessMap.containsKey(executionName)){
							Process process = executionService.executionProcessMap.get(executionName)
							if(process){
								process.waitForOrKill(1)
								process.destroy()
							}
						}
					} catch (Exception e) {
						println " Execption "+e.getMessage()
						e.printStackTrace()
					}

				}else{
					if(!executionService.abortList.contains(execution?.id?.toString())){
						executionService.abortList.add(execution?.id?.toString())
						result.addProperty("Status", "Requested for abort")
					}else{
						result.addProperty("Status", "Request to stop already in progress")
					}
					if(executionService.executionProcessMap.containsKey(executionName)){
						Process process = executionService.executionProcessMap.get(executionName)
						if(process){
							process.waitForOrKill(1)
							process.destroy()
						}
					}

				}
			}else if(execution?.executionStatus.equals("PAUSED")){
				executionService.saveExecutionStatus(true, execution?.id)
				result.addProperty("Status", "Requested for abort")
			} else{
				if(execution != null){
					result.addProperty("Status", "Error. No execution found in this name in IN-PROGRESS / PAUSED state to stop")
				}else{
					result.addProperty("Status", "Error. No execution found in this name")
				}
			}
			render result
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	/**
	 * Method to fetch the device status of the selected device
	 * @return
	 */
	def updateDeviceStatus(){
		def device = Device.get( params?.id )
		try {
			String status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, device)
			deviceStatusService.updateOnlyDeviceStatus(device, status);
			def result1
			def deviceInstanceList = null
			def category = params?.category?.trim()
			if(Category.RDKV.toString().equals(category)){
				deviceInstanceList = Device.findAllByGroupsAndCategory(utilityService.getGroup(), Category.RDKV, [order: 'asc', sort: 'stbName'])
			}
			else if(Category.RDKB.toString().equals(category)){
				deviceInstanceList = Device.findAllByGroupsAndCategory(utilityService.getGroup(), Category.RDKB, [order: 'asc', sort: 'stbName'])
			}else if(Category.RDKC.toString().equals(category)){
				deviceInstanceList = Device.findAllByGroupsAndCategory(utilityService.getGroup(), Category.RDKC, [order: 'asc', sort: 'stbName'])
			}
			result1 = [url: getApplicationUrl(), deviceList : deviceInstanceList, deviceInstanceTotal: deviceInstanceList?.size()]

			render view:"devicelist", model:result1
		} catch (Exception e) {
		}
	}

	def getDeviceStatusListData(){
		try {
			//def deviceInstanceList = Device.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(),[order: 'asc', sort: 'stbName'])
			def deviceInstanceListV = Device.findAllByGroupsAndCategory(utilityService.getGroup(), Category.RDKV, [order: 'asc', sort: 'stbName'])
			def deviceInstanceListB = Device.findAllByGroupsAndCategory(utilityService.getGroup(), Category.RDKB, [order: 'asc', sort: 'stbName'])
			def result1 = [url: getApplicationUrl(), deviceListV : deviceInstanceListV, deviceListB:deviceInstanceListB, deviceInstanceTotalV: deviceInstanceListV?.size(), deviceInstanceTotalB: deviceInstanceListB?.size()]

			render view:"devicelist", model:result1
		} catch (Exception e) {
		}
	}
	/*
	 * Date based execution History table clean up
	 */

	def deleteExecutions(){

		def deleteCount = 0
		try {

			List<Execution> executionList = Execution.findAll("from Execution as b where DATE_FORMAT(b.dateOfExecution,'%m/%d/%Y') between '${params?.cleanFromDate}' and '${params?.cleanToDate}' ")
			List executionResultList = []
			List executionMethodResultInstanceList = []
			List performanceList = []
			executionList?.each{ executionInstance ->

				if(!executionInstance?.executionStatus?.equals(INPROGRESS_STATUS) ){
					if( !executionInstance?.executionStatus?.equals(PAUSED)){
						if(executionInstance){
							executionResultList  = ExecutionResult.findAllByExecution(executionInstance)

							executionResultList.each { executionResultInstance ->

								if(executionResultInstance){
									executionMethodResultInstanceList = ExecuteMethodResult.findAllByExecutionResult(executionResultInstance)
									if(executionMethodResultInstanceList){
										executionMethodResultInstanceList.each { executionMethodResultInstance ->
											executionMethodResultInstance.delete(flush:true)
										}
									}
									performanceList = Performance.findAllByExecutionResult(executionResultInstance)
									performanceList.each{ performance ->
										performance.delete(flush:true)
									}
									executionResultInstance.delete(flush:true)
								}
							}


							if(executionInstance?.thirdPartyExecutionDetails){
								executionInstance?.thirdPartyExecutionDetails = null;
								executionInstance?.save();
							}

							def thirdPartyExecutionDetailsList = ThirdPartyExecutionDetails.findAllByExecution(executionInstance)
							thirdPartyExecutionDetailsList.each{ thirdPartyExecution ->
								thirdPartyExecution.delete(flush:true)
							}

							def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
							executionDeviceList.each{ executionDeviceInstance ->
								executionDeviceInstance.delete(flush:true)
							}

							def execId = executionInstance?.id.toString()
							executionInstance.delete(flush:true)
							deleteCount ++
							log.info "Deleted "+executionInstance
							/**
							 * Deletes the log files, crash files
							 */
							String realPathForLogs = getRealPathForLogs()
							String logFilePath = realPathForLogs + "//logs//"+execId
							def logFiles = new File(logFilePath)
							if(logFiles.exists()){
								logFiles?.deleteDir()
							}
							String crashFilePath = realPathForLogs + "//logs//crashlogs//"

							new File(crashFilePath).eachFileRecurse { file->
								if((file?.name).startsWith(execId)){
									file?.delete()
								}
							}
							String versionFilePath = realPathForLogs + "//logs//version//"+execId
							def versionFiles = new File(versionFilePath)
							if(versionFiles.exists()){
								versionFiles?.deleteDir()
							}

							String agentLogFilePath = realPathForLogs + "//logs//consolelog//"+execId
							def agentLogFiles = new File(agentLogFilePath)
							if(agentLogFiles.exists()){
								agentLogFiles?.deleteDir()
							}

						}
						else{
							log.info "Invalid executionInstance"
						}
					}
				}
			}


		} catch (Exception e) {
			e.printStackTrace()
		}

		render deleteCount.toString()+" execution entries deleted"
	}

	def pushData(String exName,String moduleType){
		def realPath = getRealPath()
		ThirdPartyExecutionDetails.withTransaction {
			ThirdPartyExecutionDetails  thirdPartyExecutionDetails = ThirdPartyExecutionDetails.findByExecName(exName)
			if(thirdPartyExecutionDetails){
				scriptexecutionService.executeCallBackUrl(thirdPartyExecutionDetails.execName,thirdPartyExecutionDetails.url,thirdPartyExecutionDetails.callbackUrl,thirdPartyExecutionDetails.filePath,thirdPartyExecutionDetails.executionStartTime,thirdPartyExecutionDetails.imageName,thirdPartyExecutionDetails.boxType,realPath)
			}
		}
	}

	/**
	 * REST API for single test execution .
	 * @param stbName - name of the STB configured in Test Manager
	 * @param boxType - boxType of the STB like Hybrid-1, IPClient-3
	 * @param scriptName - Name if the script to be executed
	 * @return - Return JSON with status of REST call
	 */

	def thirdPartySingleTestExecution(final String stbName, final String boxType, final String scriptName , final String executionCount, final String reRunOnFailure, final String timeInfo,final String performance,final String isLogRequired, final String isAlert){
		int exeCount = 1
		if(executionCount ){
			try {
				exeCount = Integer.parseInt(executionCount)
			} catch (Exception e) {
				e.printStackTrace()
			}
		}

		String rerun = FALSE
		if(reRunOnFailure && reRunOnFailure?.equals(TRUE)){
			rerun = TRUE
		}

		String time = FALSE
		if(timeInfo && timeInfo?.equals(TRUE)){
			time = TRUE
		}

		String perfo = FALSE
		if(performance && performance?.equals(TRUE)){
			perfo = TRUE
		}

		String isLog = FALSE
		if(isLogRequired && isLogRequired?.equals(TRUE)){
			isLog = TRUE
		}
		
		String isAlertEnabled = FALSE
		if(isAlert && isAlert?.equals(TRUE)){
			isAlertEnabled = TRUE
		}
		def deviceInstance = Device.findByStbName(stbName)
		if(deviceInstance && deviceInstance?.isThunderEnabled == 1){
			singleTestRestExecutionRdkService(stbName,boxType,scriptName,exeCount,rerun,isLog,isAlertEnabled)
		}else{
			singleTestRestExecution(stbName,boxType,scriptName,exeCount,rerun,time,perfo,isLog)
		}
	}

	//	def thirdPartySingleTestExecution(final String stbName, final String boxType, final String scriptName ){
	//		singleTestRestExecution(stbName,boxType,scriptName,1,FALSE,FALSE,FALSE)
	//	}

	def singleTestRestExecution(final String stbName, final String boxType, final String scriptName , final int repeat, final String reRunOnFailure, final String timeInfo,final String performance,final String isLog){
		def deviceInstance = Device.findByStbName(stbName)
		String  url = getApplicationUrl()
		String htmlData = ""
		def execName = ""
		def newExecName = ""
		String filePath = "${request.getRealPath('/')}//fileStore"
		boolean executed = false
		JsonObject jsonOutData = new JsonObject()
		String  sName = scriptName
		int i =0;
		boolean valid = false;
		boolean TCL = false;
		try {
			if(deviceInstance){
				def category = deviceInstance.category
				if(("RDKB".equals(category?.toString()))){
					if((scriptService?.tclScriptsList?.toString()?.contains(scriptName?.trim()))  ){
						TCL = true
					}
					if(!TCL){
					boolean compoundTCL = false
					def combainedTclScript =  scriptService?.combinedTclScriptMap
					combainedTclScript?.each{
						if(it?.value?.toString().contains(scriptName?.toString())){
							compoundTCL = true
						}
					}
					if((scriptService?.totalTclScriptList?.toString()?.contains(scriptName?.toString())) && compoundTCL ){
						combainedTclScript?.each{
							if(it?.value?.toString()?.contains(scriptName?.toString())){
								TCL = true
							}
						}
					}
					}
				}
				if(!TCL ){
					def moduleName= scriptService.scriptMapping.get(scriptName)
					if(moduleName){
						def scriptInstance1 = scriptService.getScript(getRealPath(),moduleName, scriptName, category.toString())
						if(scriptInstance1){
							//check whether the script is valid for this execution
							if(executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
								String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
								if(executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)){
									valid = true
								}else{
									htmlData = "RDK Version supported by the script is not matching with the RDK Version of selected Device "+deviceInstance?.stbName+"<br>"
								}
							}else{
								htmlData = message(code: 'execution.boxtype.nomatch')
							}
						}else{
							htmlData = "No Script is available with name ${scriptName} in module ${moduleName}"
						}
					}else{
						htmlData = "No module associated with script ${scriptName}"
					}

				}else{

					def scriptInstance1 = [:]
					boolean compoundTCL = false
					def combainedTclScript =  scriptService?.combinedTclScriptMap
					combainedTclScript?.each{
						if(it?.value?.toString().contains(sName)){
							compoundTCL = true
						}
					}
					if((scriptService?.totalTclScriptList?.toString()?.contains(sName)) && compoundTCL ){
						combainedTclScript?.each{
							if(it?.value?.toString()?.contains(sName)){
								sName = it.key?.toString()
							}
						}
					}
					def scriptValid = Utility.isTclScriptExists(realPath,  sName)
					if(scriptValid) {
						if(Utility.isConfigFileExists(realPath, deviceInstance?.stbName)){
							scriptInstance1.put('scriptName',sName )
							valid = true
						}
						else{
							htmlData = "<br>"+stbName +"  : No Config file is available with name Config_${deviceInstance?.stbName}.txt"
						}

					}else{
						htmlData = "<br>"+stbName +"  : No TCL Script is available with name ${scriptName}"
					}
				}
				String status = ""
				if(valid){
					try {
						status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)

						synchronized (lock) {
							if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
								status = "BUSY"
							}else{
								if(!status.equals( Status.FREE.toString() )){
									status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
								}
								if((status.equals( Status.FREE.toString() ))){
									if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
										executionService.deviceAllocatedList.add(deviceInstance?.id)
										Thread.start{
											deviceStatusService.updateOnlyDeviceStatus(deviceInstance, Status.BUSY.toString())
										}
									}
								}
							}
						}
					}
					catch(Exception eX){
					}
			
				status = status.trim()
				//execute script only if the device is free
				if((status.equals( Status.FREE.toString() ))){
					if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
						executionService.deviceAllocatedList.add(deviceInstance?.id)
					}

					def deviceName
					ExecutionDevice executionDevice
					def execution
					def executionSaveStatus = true
					DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
					Calendar cal = Calendar.getInstance()
					deviceName = deviceInstance?.stbName


					execName = CI_EXECUTION+deviceName+dateFormat.format(cal.getTime()).toString()
					newExecName = execName
					//execName = CI_EXECUTION+deviceName+dateFormat.format(cal.getTime()).toString()

					try {
						//									executionSaveStatus = scriptexecutionService.saveExecutionDetails(execName, scriptName, deviceName, null,url)
						//executionSaveStatus =  executionService.saveExecutionDetails(execName, scriptName, deviceName, null,url,timeInfo,performance,reRunOnFailure,FALSE)
						executionSaveStatus =  executionService.saveExecutionDetails(execName,[scriptName:scriptName, deviceName:deviceName, scriptGroupInstance:null,
							appUrl:url, isBenchMark:timeInfo, isSystemDiagnostics:performance, rerun:reRunOnFailure, isLogReqd:FALSE,category:category?.toString(),rerunOnFailure:FALSE,isAlertEnabled:FALSE])
					} catch (Exception e) {
						executionSaveStatus = false
					}

					if(executionSaveStatus){
						execution = Execution.findByName(execName)
						try{
							executionDevice = new ExecutionDevice()
							executionDevice.execution = execution
							executionDevice.dateOfExecution = new Date()
							executionDevice.device = deviceInstance?.stbName
							executionDevice.boxType = deviceInstance?.boxType?.name
							executionDevice.deviceIp = deviceInstance?.stbIp
							executionDevice.buildName = executionService.getBuildName( deviceInstance?.stbName )
							executionDevice.status = UNDEFINED_STATUS
							executionDevice.category = category
							if(executionDevice.save(flush:true)){
								String getRealPathString  = getRealPath()
								executionService.executeVersionTransferScript(getRealPathString,filePath,execName, executionDevice?.id, deviceInstance?.stbName, deviceInstance?.logTransferPort,url)
								def rerun = null
								if(reRunOnFailure?.equals(TRUE)){
									rerun = "on"
								}

								if(repeat > 1){

								}else{
									if(!TCL ){
										htmlData = executescriptService.executeScriptInThread(true,execName, ""+deviceInstance?.id, executionDevice, scriptName, "", execName,
												filePath, getRealPath(), SINGLE_SCRIPT, url, timeInfo, performance, rerun,isLog,category?.toString(),1,FALSE)

										// The Execution is done through only one device
										//											htmlData = executescriptService.executescriptsOnDevice(execName, ""+deviceInstance?.id, executionDevice, scriptName, "", execName,
										//													filePath, getRealPath(), SINGLE_SCRIPT, url, timeInfo, performance, rerun,FALSE)

										executed = true
										println " singleTestRestExecution [stbName="+stbName+"] [scriptName="+scriptName+"]"+" [execName="+execName+"] [Triggered Execution]"
										url = url + "/execution/thirdPartyJsonResult?execName=${execName}"
										jsonOutData.addProperty("status", "RUNNING")
										jsonOutData.addProperty("result", url)

									}else{
										tclExecutionService.executeScriptInThread(execName, ""+deviceInstance?.id, executionDevice, scriptName, "", execName,
												filePath, getRealPath(), SINGLE_SCRIPT, url, timeInfo, performance, rerun,isLog,category?.toString())
										executed = true
										url = url + "/execution/thirdPartyJsonResult?execName=${execName}"
										jsonOutData.addProperty("status", "RUNNING")
										jsonOutData.addProperty("result", url)
									}

								}
							}
						}
						catch(Exception e){
							println " ERROR "+e.getMessage()
						}
					}
					else{
						htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
					}
				}
				else if(status.equals( Status.ALLOCATED.toString() )){
					htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
				}
				else if(status.equals( Status.NOT_FOUND.toString() )){
					htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
				}
				else if(status.equals( Status.HANG.toString() )){
					htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
				}
				else if(status.equals( Status.BUSY.toString() )){
					htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
				}else if(status.equals( Status.TDK_DISABLED.toString() )){
					htmlData = htmlData + "TDK is not enabled  in the Device to execute scripts"

				}
				else{
					htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
				}

							
				}

			}else{
				htmlData = "No device found with this name "+stbName
			}
		} finally {
			if(!executed){
				println " singleTestRestExecution [stbName="+stbName+"] [scriptName="+scriptName+"] not executed "
				if(deviceInstance){
					if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
						executionService.deviceAllocatedList.removeAll(deviceInstance?.id)
					}

					String devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
					Thread.start{
						deviceStatusService.updateOnlyDeviceStatus(deviceInstance, devStatus)
					}

					Thread.sleep(1000);

					Device devv = Device.get(deviceInstance?.id)					
						println "**["+ deviceInstance?.stbName+"] ["+  devStatus + "] ["+devv?.deviceStatus+"]"
					if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
						println " Device instance is still there in the allocated list :  "+deviceInstance?.stbName + " id "+ deviceInstance?.id
						executionService.deviceAllocatedList.removeAll(deviceInstance?.id)
						println " Again checking the device lock  for "+deviceInstance?.stbName + " status =  "+executionService.deviceAllocatedList.contains(deviceInstance?.id)
					}
				}else{
					htmlData = "No device found with this name "+stbName
				}

					jsonOutData.addProperty("status", "FAILURE")
					jsonOutData.addProperty("result", htmlData)
				
			}
		}
		println " singleTestRestExecution [stbName="+stbName+"] [scriptName="+scriptName+"] [jsonOutData="+jsonOutData+"]"
		render jsonOutData
	}
	
	/**
	 * Function to handle REST API single script execution of rdkservice scripts
	 * @param stbName
	 * @param boxType
	 * @param scriptName
	 * @param repeat
	 * @param reRunOnFailure
	 * @return - Return JSON with status of REST call
	 */
	
	def singleTestRestExecutionRdkService(final String stbName, final String boxType, final String scriptName , final int repeat, final String reRunOnFailure, final String isLog,final String isAlert){
		String timeInfo = FALSE
		String performance = FALSE
		def deviceInstance = Device.findByStbName(stbName)
		String  url = getApplicationUrl()
		String htmlData = ""
		def execName = ""
		def newExecName = ""
		String filePath = "${request.getRealPath('/')}//fileStore"
		boolean executed = false
		JsonObject jsonOutData = new JsonObject()
		String  sName = scriptName
		int i =0;
		boolean valid = false;
		boolean TCL = false;
		try {
			if(deviceInstance){
				def category = deviceInstance.category
				if(!TCL ){
					def moduleName= scriptService.scriptMapping.get(scriptName)
					if(moduleName){
						def scriptInstance1 = scriptService.getScript(getRealPath(),moduleName, scriptName, category.toString())
						if(scriptInstance1){
							if(executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
								String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
								if(executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)){
									valid = true
								}else{
									htmlData = "RDK Version supported by the script is not matching with the RDK Version of selected Device "+deviceInstance?.stbName+"<br>"
								}
							}else{
								htmlData = message(code: 'execution.boxtype.nomatch')
							}
						}else{
							htmlData = "No Script is available with name ${scriptName} in module ${moduleName}"
						}
					}else{
						htmlData = "No module associated with script ${scriptName}"
					}

				}else{

					def scriptInstance1 = [:]
					boolean compoundTCL = false
					def combainedTclScript =  scriptService?.combinedTclScriptMap
					combainedTclScript?.each{
						if(it?.value?.toString().contains(sName)){
							compoundTCL = true
						}
					}
					if((scriptService?.totalTclScriptList?.toString()?.contains(sName)) && compoundTCL ){
						combainedTclScript?.each{
							if(it?.value?.toString()?.contains(sName)){
								sName = it.key?.toString()
							}
						}
					}
					def scriptValid = Utility.isTclScriptExists(realPath,  sName)
					if(scriptValid) {
						if(Utility.isConfigFileExists(realPath, deviceInstance?.stbName)){
							scriptInstance1.put('scriptName',sName )
							valid = true
						}
						else{
							htmlData = "<br>"+stbName +"  : No Config file is available with name Config_${deviceInstance?.stbName}.txt"
						}

					}else{
						htmlData = "<br>"+stbName +"  : No TCL Script is available with name ${scriptName}"
					}
				}
				String status = ""
				if(valid){
					try {
						status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)

						synchronized (lock) {
							if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
								status = "BUSY"
							}else{
								if(!status.equals( Status.FREE.toString() )){
									status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
								}
								if((status.equals( Status.FREE.toString() ))){
									if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
										executionService.deviceAllocatedList.add(deviceInstance?.id)
										Thread.start{
											deviceStatusService.updateOnlyDeviceStatus(deviceInstance, Status.BUSY.toString())
										}
									}
								}
							}
						}
					}
					catch(Exception eX){
					}
			
				status = status.trim()
				if((status.equals( Status.FREE.toString() ))){
					if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
						executionService.deviceAllocatedList.add(deviceInstance?.id)
					}

					def deviceName
					ExecutionDevice executionDevice
					def execution
					def executionSaveStatus = true
					DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
					Calendar cal = Calendar.getInstance()
					deviceName = deviceInstance?.stbName


					execName = CI_EXECUTION+deviceName+dateFormat.format(cal.getTime()).toString()
					newExecName = execName

					try {
						executionSaveStatus =  executionService.saveExecutionDetails(execName,[scriptName:scriptName, deviceName:deviceName, scriptGroupInstance:null,
							appUrl:url, isBenchMark:timeInfo, isSystemDiagnostics:performance, rerun:reRunOnFailure, isLogReqd:FALSE,category:category?.toString(),rerunOnFailure:FALSE,isAlertEnabled:isAlert])
					} catch (Exception e) {
						executionSaveStatus = false
					}

					if(executionSaveStatus){
						execution = Execution.findByName(execName)
						try{
							executionDevice = new ExecutionDevice()
							executionDevice.execution = execution
							executionDevice.dateOfExecution = new Date()
							executionDevice.device = deviceInstance?.stbName
							executionDevice.boxType = deviceInstance?.boxType?.name
							executionDevice.deviceIp = deviceInstance?.stbIp
							executionDevice.buildName = executionService.getBuildName( deviceInstance?.stbName )
							executionDevice.status = UNDEFINED_STATUS
							executionDevice.category = category
							if(executionDevice.save(flush:true)){
								String getRealPathString  = getRealPath()
								StormExecuter.createThunderVersionFile(getRealPathString, execution?.id, executionDevice?.id, executionDevice?.deviceIp)
								def rerun = null
								if(reRunOnFailure?.equals(TRUE)){
									rerun = "on"
								}

								if(repeat > 1){

								}else{
									if(!TCL ){
										htmlData = executescriptService.executeScriptInThread(true,execName, ""+deviceInstance?.id, executionDevice, scriptName, "", execName,
												filePath, getRealPath(), SINGLE_SCRIPT, url, timeInfo, performance, rerun,isLog,category?.toString(),1,isAlert)
                                        executed = true
										url = url + "/execution/thirdPartyJsonResult?execName=${execName}"
										jsonOutData.addProperty("status", "RUNNING")
										jsonOutData.addProperty("result", url)

									}else{
										tclExecutionService.executeScriptInThread(execName, ""+deviceInstance?.id, executionDevice, scriptName, "", execName,
												filePath, getRealPath(), SINGLE_SCRIPT, url, timeInfo, performance, rerun,isLog,category?.toString())
										executed = true
										url = url + "/execution/thirdPartyJsonResult?execName=${execName}"
										jsonOutData.addProperty("status", "RUNNING")
										jsonOutData.addProperty("result", url)
									}

								}
							}
						}
						catch(Exception e){
							println " ERROR "+e.getMessage()
						}
					}
					else{
						htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
					}
				}
				else if(status.equals( Status.ALLOCATED.toString() )){
					htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
				}
				else if(status.equals( Status.NOT_FOUND.toString() )){
					htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
				}
				else if(status.equals( Status.HANG.toString() )){
					htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
				}
				else if(status.equals( Status.BUSY.toString() )){
					htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
				}else if(status.equals( Status.TDK_DISABLED.toString() )){
					htmlData = htmlData + "TDK is not enabled  in the Device to execute scripts"

				}
				else{
					htmlData = htmlData + "Device ${deviceInstance?.stbName} is not free to execute Scripts"
				}

							
				}

			}else{
				htmlData = "No device found with this name "+stbName
			}
		} finally {
			if(!executed){
				if(deviceInstance){
					if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
						executionService.deviceAllocatedList.removeAll(deviceInstance?.id)
					}

					String devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
					Thread.start{
						deviceStatusService.updateOnlyDeviceStatus(deviceInstance, devStatus)
					}

					Thread.sleep(1000);

					Device devv = Device.get(deviceInstance?.id)
					if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
						executionService.deviceAllocatedList.removeAll(deviceInstance?.id)
					}
				}else{
					htmlData = "No device found with this name "+stbName
				}

					jsonOutData.addProperty("status", "FAILURE")
					jsonOutData.addProperty("result", htmlData)
				
			}
		}
		println " singleTestRestExecution [stbName="+stbName+"] [scriptName="+scriptName+"] [jsonOutData="+jsonOutData+"]"
		render jsonOutData
	}

	def clearDeviceAllocatedList(final String stbName){
		JsonObject result = new JsonObject()
		result.addProperty("stbName", stbName)
		
		def deviceInstance = Device.findByStbName(stbName)
		if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
			executionService.deviceAllocatedList.remove(deviceInstance?.id)
			result.addProperty("status", "cleared device allocation")
		}else{
			result.addProperty("status", "nothing to clear")
		}
		render result
	}

	/**
	 * Method to get the module wise execution status
	 */
	def executionStatus(){
		String realPathForLogs = getRealPathForLogs()
		Execution executionInstance = Execution.findById(params?.id)

		def detailDataMap = executedbService.prepareDetailMap(executionInstance,request.getRealPath('/'))

		def tDataMap = [:]
		def  chartModuleDataList = []
		def barColors = []
		
		int total = 0
		detailDataMap?.keySet()?.each { k ->
			Map mapp = detailDataMap?.get(k)
			int tCount = 0
			mapp?.keySet()?.each { status ->

				def tStatusCounter = tDataMap.get(status)
				def statusCounter = mapp.get(status)
				if(!tStatusCounter){
					tStatusCounter = 0
				}
				if(!status.equals("PENDING")){
					tCount = tCount + statusCounter
					tStatusCounter = tStatusCounter + statusCounter
					tDataMap.put(status, tStatusCounter)
				}
			}
			
			int na = 0
			if(mapp?.keySet().contains("N/A")){
				na = mapp?.get("N/A")
			}
			
			mapp.put("Executed", tCount)
			def success = mapp?.get("SUCCESS")
			if(success){
				int rate = 0
				if(tCount > 0){
					if(mapp?.keySet().contains("N/A")){
						na = mapp?.get("N/A")
					}
					rate = ((success * 100)/(tCount - na))
				}
				mapp.put("passrate",rate)
				def statusData = []
				statusData.add("'"+k+"'")
				statusData.add(rate)
				chartModuleDataList.add(statusData)
				barColors.add("'"+getBarChartColors(rate)+"'")
			}
			total = total + tCount
		}
		
		tDataMap.put("Executed", total)
		int rate
		if(tDataMap?.get("SUCCESS")){
			int success = tDataMap?.get("SUCCESS")
			int na = 0
			if(tDataMap?.keySet().contains("N/A")){
				na = tDataMap?.get("N/A")
			}
			rate = ((success * 100)/(total - na))
		}

		tDataMap.put("passrate",rate)

		def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def device = Device.findByStbName(executionInstance?.device)
		def testGroup

		if(executionInstance?.script){
			def script = Script.findByName(executionInstance?.script)
			testGroup = script?.primitiveTest?.module?.testGroup
		}

		[statusResults : [:], executionInstance : executionInstance, executionDeviceInstanceList : executionDeviceList, testGroup : testGroup,executionresults:[:],detailDataMap:detailDataMap,tDataMap:tDataMap,chartModuleDataList:chartModuleDataList,barColors:barColors, realPathForLogs : realPathForLogs]

	}

	def File [] getFilesArray(def moduleObj ){
		List fileList = []
		File [] files = moduleObj?.listFiles();
		files?.each { ff ->
			if(ff?.name?.endsWith(".py")){
				fileList.add(ff)
			}
		}
		return files
	}

	/**
	 * Utility method to fetch the module wise script count details 
	 */
	def getScriptsDetails(){

		JsonObject scripts = new JsonObject()

		JsonArray jsonArray = new JsonArray()
		List scriptList = []

		List dirList = [
			Constants.COMPONENT,
			Constants.INTEGRATION
		]
		def start = System.currentTimeMillis()
		int moduleCount = 0;
		int total = 0
		dirList.each{ directory ->
			File scriptsDir = new File( "${realPath}//fileStore//testscripts//"+directory+"//")
			if(scriptsDir.exists()){
				File [] moduleArray = scriptsDir.listFiles()

				Arrays.sort(moduleArray);

				moduleArray.each { moduleObj ->
					moduleCount ++
					JsonObject jsonObj = new JsonObject()
					def start1 =System.currentTimeMillis()
					try {
						List files = getFilesArray(moduleObj)
						total = total + files?.size()
						jsonObj.addProperty(moduleObj?.name, ""+files?.size())
						jsonArray.add(jsonObj)
					}catch (Exception e) {
						println " Error  "+e.getMessage()
						e.printStackTrace()
					}
				}
			}
		}
		scripts.addProperty("modules", moduleCount)
		scripts.addProperty("total", total)
		scripts.add("details", jsonArray)
		String data = ""+scripts?.toString()
		render data
	}
	/**
	 * Function for using the repeat execution option in the show log page based on the  test suite / multiple script excution.
	 * params : -
	 * 		1) ExecutionName
	 * 		2) ScriptGroup
	 * 		3) Device
	 * 		4) Scripts
	 * 		5) BenchMark enabled 
	 * 		6) System Diagnostics enabled  
	 * 		7) Rerun 
	 * @return
	 */
	def repeatExecution(){	
		try{
			int execCnt = 0
			def executionInstance =  Execution.findByName(params?.executionName)			
			def  multipleScript = []
			def execName1 =  executionInstance?.name
			boolean singleScriptGroup = false
			if(!(execName1.toString().contains("RERUN"))){
				int executionCount=0
				int execCount = 0
				int testCount = 0
				def repeatCount
				def newExecutionName
				def executionList = Execution?.findAll()
				if(Execution?.findByName(execName1?.toString())){
					def tempExecName = execName1?.toString()
					def executionDevice = executionInstance?.device	
					if(execName1?.toString()?.contains(executionDevice))
					{
						tempExecName = execName1?.toString()?.substring(executionDevice.length())
					}
					
					if(tempExecName?.contains("_"))
					{
						
						def namePart = execName1?.substring(0,execName1.lastIndexOf("_") )
						executionCount = getExecutionCountFromName(execName1)
						executionCount++
						newExecutionName = namePart + "_"+executionCount
						if(Execution?.findByName(newExecutionName?.toString())){
							def execList = Execution?.findAllByNameLike(namePart+"%", [order: "desc"])
							if(execList && execList?.size() > 0){
								executionCount = getExecutionCountFromName(execList?.get(0)?.name)
								executionCount++
								newExecutionName = namePart+"_"+(executionCount)
							}
						}
					}	
					else{
						newExecutionName = execName1 +"_"+1
						//if(executionList?.toString().contains(newExecutionName?.toString())){
						if(Execution.findByName(newExecutionName.toString())){
							def execList = Execution?.findAllByNameLike(execName1+"_%" , [order: "desc"])
							if(execList && execList?.size() > 0){
								executionCount = getExecutionCountFromName(execList?.get(0)?.name)
								executionCount++
								newExecutionName = execName1 +"_"+executionCount
							}
						}else{
							newExecutionName = newExecutionName
						}
					}
				}
				def executionInstance1 =  Execution.findByName(params?.executionName)
				def deviceInstance = Device?.findByStbName(params.device)
				String execName = newExecutionName
				def executionName =  execName
				def executionNameForCheck
				def isBenchMark = FALSE
				def isSystemDiagnostics = FALSE
				def isLogReqd = FALSE
				String isAlertEnabled = FALSE
				def rerun = FALSE
				boolean aborted = false
				def scriptGroupInstance
				if( executionInstance?.isBenchMarkEnabled){
					isBenchMark = TRUE
				}
				if(executionInstance?.isSystemDiagnosticsEnabled){
					isSystemDiagnostics =TRUE
				}
				if(executionInstance?.isStbLogRequired){
					isLogReqd = TRUE
				}
				if(executionInstance?.isAlertEnabled){
					if(deviceInstance?.isThunderEnabled == 1){
						isAlertEnabled = TRUE
					}
				}
				String url = getApplicationUrl()
				String filePath = "${request.getRealPath('/')}//fileStore"
				boolean validScript = false
				def deviceId
				deviceId = deviceInstance?.id
				String devStatus = ""
				def scriptGroup
				boolean allocated = false
				if(executionInstance1?.category?.toString().equals(RDKV_THUNDER)){
					thunderService.executeScriptsRepeat(params, execName, getRealPath(), url?.toString())
				}
				else{
					try {
						devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
						synchronized (lock) {
							if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
								devStatus = Status.BUSY.toString()
							}else{
								if((devStatus.equals( Status.FREE.toString() ))){
									if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
										allocated = true
										executionService.deviceAllocatedList.add(deviceInstance?.id)
										Thread.start{
											deviceStatusService.updateOnlyDeviceStatus(deviceInstance, Status.FREE.toString())
										}
									}
								}
							}
						}
					}
					catch(Exception eX){
						log.error "Error "+eX.getMessage()
						eX.printStackTrace()
					}
					if(params?.scriptGroup && params?.scriptGroup!="Multiple Scriptgroups"){
						scriptGroupInstance  =  ScriptGroup?.findByName(params?.scriptGroup,[lock: true])
						singleScriptGroup = true
					}
					def scripts = null
					if(params?.scriptGroup == "Multiple Scriptgroups"){
						scripts = "Multiple Scriptgroups"
					}else if((params?.scriptGroup != "Multiple Scriptgroups") && ((params?.scriptGroup != null) || (params?.scriptGroup != ""))){
						scripts = params?.scriptGroup
					}else if(params?.script == "Multiple Scripts"){
						scripts = "Multiple Scripts"
					}else if(params?.script){
					    scripts = params?.script
					}
					def saveExecutionDetails = true
					if( devStatus.equals( Status.FREE.toString())){
						if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
							allocated = true
							executionService.deviceAllocatedList.add(deviceInstance?.id)
						}
						int scriptCnt = 0
						if(scriptGroupInstance?.scriptList?.size() > 0){
							scriptCnt= scriptGroupInstance?.scriptList?.size()
						}
						def executionDevice
						def execResult
						execResult = ExecutionResult?.findAllByExecution(executionInstance)
						if(params?.script?.toString().equals(MULTIPLESCRIPT)){
							int scriptCount  = execResult?.size()
							
							//For multiple script execution
							//saveExecutionDetails = executionService.saveExecutionDetailsOnMultipleScripts(execName?.toString(), MULTIPLESCRIPT, deviceInstance?.toString(), scriptGroupInstance,url?.toString(),isBenchMark?.toString(),isSystemDiagnostics?.toString(),rerun?.toString(),isLogReqd?.toString(),scriptCount,)
							saveExecutionDetails= executionService.saveExecutionDetails(execName?.toString(),[scriptName:MULTIPLESCRIPT, deviceName:deviceInstance?.toString(), scriptGroupInstance:scriptGroupInstance,
														appUrl:url?.toString(), isBenchMark:isBenchMark?.toString(), isSystemDiagnostics:isSystemDiagnostics?.toString(), rerun:rerun?.toString(), isLogReqd:isLogReqd?.toString(),category:executionInstance1?.category?.toString(), rerunOnFailure : FALSE,isAlertEnabled:isAlertEnabled])
						}else if(params?.scriptGroup?.toString().equals(MULTIPLESCRIPTGROUPS)){
							int scriptCount  = execResult?.size()
							saveExecutionDetails= executionService.saveExecutionDetails(execName?.toString(),[scriptName:MULTIPLESCRIPTGROUPS, deviceName:deviceInstance?.toString(), scriptGroupInstance:scriptGroupInstance,
								appUrl:url?.toString(), isBenchMark:isBenchMark?.toString(), isSystemDiagnostics:isSystemDiagnostics?.toString(), rerun:rerun?.toString(), isLogReqd:isLogReqd?.toString(),category:executionInstance1?.category?.toString(), rerunOnFailure : FALSE,isAlertEnabled:isAlertEnabled])
						}else{
							//saveExecutionDetails = executionService.saveExecutionDetails(execName?.toString(), scripts, deviceInstance?.toString(), scriptGroupInstance ,url?.toString(),isBenchMark?.toString(),isSystemDiagnostics?.toString(),rerun?.toString(),isLogReqd?.toString())
						saveExecutionDetails= executionService.saveExecutionDetails(execName?.toString(),[scriptName:scripts, deviceName:deviceInstance?.toString(), scriptGroupInstance:scriptGroupInstance,
							appUrl:url?.toString(), isBenchMark:isBenchMark?.toString(), isSystemDiagnostics:isSystemDiagnostics?.toString(), rerun:rerun?.toString(), isLogReqd:isLogReqd?.toString(),category:executionInstance1?.category?.toString(), rerunOnFailure:FALSE,isAlertEnabled:isAlertEnabled])
						}
						if(saveExecutionDetails){
							try {
								executionDevice = new ExecutionDevice()
								executionDevice.execution = Execution.findByName(execName)
								executionDevice.dateOfExecution = new Date()
								executionDevice.device = deviceInstance?.stbName
								executionDevice.boxType = deviceInstance?.boxType?.name
								executionDevice.deviceIp = deviceInstance?.stbIp
								executionDevice.status = UNDEFINED_STATUS
								executionDevice.category = Utility.getCategory(deviceInstance?.category?.toString())
								executionDevice.save(flush:true)
							}catch (Exception e ){
								log.error "Error "+e.getMessage()
								e.printStackTrace()
							}
							if(saveExecutionDetails){
								String myGroup = ""
									myGroup = SINGLE_SCRIPT
									scripts = execResult?.script
		                        if(executionInstance1?.category?.toString().equals(RDKB_TCL)){
									tclExecutionService?.executescriptsOnDevice(execName?.toString(), deviceId?.toString(), executionDevice, scripts, scriptGroupInstance?.id.toString(), executionName?.toString(),
										filePath, getRealPath(),myGroup?.toString(), url?.toString(), isBenchMark?.toString(), isSystemDiagnostics?.toString(),rerun?.toString(),isLogReqd?.toString(),executionInstance1?.category?.toString())
								}else{
									executescriptService.executescriptsOnDevice(singleScriptGroup, execName?.toString(), deviceId?.toString(), executionDevice, scripts, scriptGroupInstance?.name, executionName?.toString(),
										filePath, getRealPath(),myGroup?.toString(), url?.toString(), isBenchMark?.toString(), isSystemDiagnostics?.toString(),rerun?.toString(),isLogReqd?.toString(),executionInstance1?.category?.toString(),1,isAlertEnabled)
								}
								/*executescriptService.executescriptsOnDevice(execName?.toString(), deviceId?.toString(), executionDevice, scripts, scriptGroupInstance?.id.toString(), executionName?.toString(),
										filePath, getRealPath(),myGroup?.toString(), url?.toString(), isBenchMark?.toString(), isSystemDiagnostics?.toString(),rerun?.toString(),isLogReqd?.toString(),deviceInstance.category?.toString())*/
	
							}else{
								flash.message =  " Save Execution status is null  "
							}
						}else{
							flash.message = "Execution Details not saved  properly "
						}
					}else {
						flash.message= " Device Status is BUSY  so not possible trigger the execution "
					}
				}
			}else{
				flash.message = " Execution name contains the RERUN"
			}
		} catch(Exception e){
			println "ERROR "+ e.getMessage()
			e.printStackTrace()
		}
		redirect( view:"create")
	}
	
	/**
	 * Function for getting the next repeat count
	 * @return executionCount
	 */
	def getExecutionCountFromName(String execName){
		int executionCount = 0
		if(execName?.toString()?.contains("_")){
			def countPart = execName?.substring(execName.lastIndexOf("_") + 1, execName.length())
			if(countPart){
				try {
					executionCount =Integer.parseInt(countPart)
				} catch (Exception e) {
					e.printStackTrace()
				}
			}
		}
		return executionCount
	}
	
	/**
	 * Function for rerun on failure option in the show log page 
	 * Execute failure scripts according to the test suite which user selection.
	 * @return
	 */

	def rerunOnFailure(){
		try{
			String devStatus = ""
			def deviceInstance
			String url = getApplicationUrl()
			String filePath = "${request.getRealPath('/')}//fileStore"
			def executionInstance = Execution?.findByName(params?.executionName)
			if(params.device){
				deviceInstance = Device.findByStbName(params.device)
				//issue fixing for device status not updated properly 
				//devStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
				//if(devStatus.equals( Status.FREE.toString())){
				if(deviceInstance?.deviceStatus?.toString()?.equals(Status.FREE.toString())){					
					def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
					def executionResultList
					executionDeviceList.each {  execDeviceInstance ->
						ExecutionResult.withTransaction {
							executionResultList = ExecutionResult.findAllByExecutionAndExecutionDeviceAndStatusNotEqual(executionInstance,execDeviceInstance,SUCCESS_STATUS)
						}
					}
					boolean value  = false
					executionResultList.each{ executionResultInstance ->
						if(executionResultInstance?.status.equals("FAILURE") || executionResultInstance?.status.equals("SCRIPT TIME OUT")){
							value = true
						}
					}
					if(value ==  true ){
						String uniqueName = executionInstance?.toString()+"12"
						//ISSUE fix
						//executescriptService?.reRunOnFailure(getRealPath()?.toString(), filePath?.toString() , params?.executionName?.toString(),uniqueName?.toString(), url?.toString(), deviceInstance?.category?.toString() )
						if(!(executionInstance?.category?.toString()?.equals(RDKB_TCL)) && !(executionInstance?.category?.toString()?.equals(RDKV_THUNDER))){
							executescriptService?.reRunOnFailure(getRealPath()?.toString(), filePath?.toString() , params?.executionName?.toString(),uniqueName?.toString(), url?.toString(), executionInstance?.category?.toString() )
						}else if(executionInstance?.category?.toString()?.equals(RDKV_THUNDER)){
						    thunderService?.runFailedScriptsManually(params, params?.executionName?.toString() ,  getRealPath()?.toString(),url?.toString())
						}else{
							tclExecutionService?.reRunOnFailure(getRealPath()?.toString(), filePath?.toString() , params?.executionName?.toString(),uniqueName?.toString(), url?.toString(), executionInstance?.category?.toString())
						}
					}else{
						flash.message = "Failue script list not found in the suite"
					}
				}else {
					flash.message =" Device is not free to execute"
				}
			}
		}catch(Exception e){
			println "ERROR "+ e.getMessage()
			e.printStackTrace()
		}
		redirect(view : "create")
	}
	def failureScriptCheck(){
		def executionInstance = Execution?.findByName(params?.executionName)
		def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def executionResultList
		executionDeviceList.each {  execDeviceInstance ->
			ExecutionResult.withTransaction {
				executionResultList = ExecutionResult.findAllByExecutionAndExecutionDeviceAndStatusNotEqual(executionInstance,execDeviceInstance,SUCCESS_STATUS)
			}
		}
		boolean value  = false
		executionResultList.each{ executionResultInstance ->
			if(executionResultInstance?.status.equals("FAILURE") || executionResultInstance?.status.equals("SCRIPT TIME OUT")){
				value = true
			}
		}
		render value
	}	
	/**
	 * REST API :- for fetching execution id with execution name , include the following
	 * - Execution Name
	 * - Execution Id
	 * - If Status  failed  display message  like "no executions found with name "
	 *
	 */
	def getExecutionId(final String executionName){
		JsonObject executionObj = new JsonObject()
			if(executionName)	{
				def executionInstance = Execution?.findByName(executionName)
				if(executionInstance){
					executionObj?.addProperty("ExecutionName ",executionInstance?.name)
					executionObj.addProperty("ExecutionId",executionInstance?.id)
				}else{
					executionObj?.addProperty("Status","FAILURE")
					executionObj.addProperty("Remarks ", "no executions found with name "+ executionName)
				}
			}
		render executionObj
	}
	
	/**
	 * REST API :- fetching image name using execution name . It will include the following
	 * - Execution Name
	 * - Execution Device
	 * - Image Name
	 */
	def getImageName(final String executionName){
		JsonObject executionObj = new JsonObject()
		if(executionName){
			def executionInstance = Execution?.findByName(executionName)
			if(executionInstance){
				executionObj?.addProperty("ExecutionName ",executionInstance?.name)
				executionObj.addProperty("DeviceName",executionInstance?.device)
				def device =  ExecutionDevice?.findByExecution(executionInstance)
				String realPathForLogs = getRealPathForLogs()
				def versionFilePath = realPathForLogs + "//logs//version//${executionInstance?.id}//${device.id.toString()}"
				String fileName  = versionFilePath+"//"+device?.id+"_version.txt"
				def file = new File( fileName)
				if(file?.isFile()){
					def  lines = file?.readLines()
					def imageNameDetails
					if(lines?.size() > 0){
						lines?.each{
							if(it?.toString()?.contains("imagename")){
								imageNameDetails = it?.toString()
								imageNameDetails = imageNameDetails.replace("=",":")
							}
						}
						if(imageNameDetails){
							def imageName = imageNameDetails?.split(":")
							if(imageName.size() > 1 && imageName[0]?.toString()?.equals("imagename")){
								executionObj?.addProperty("ImageName",imageName[1])
							}else{
								executionObj?.addProperty("ImageName","Image name not available")
							}
						}else{
							executionObj?.addProperty("ImageName","Image name not available")
						}
					}
				}else{
					executionObj?.addProperty("ImageName","Image name not available")
				}
			}else{
				executionObj?.addProperty("Status","FAILURE")
				executionObj.addProperty("Remarks ", "no executions found with name "+ executionName)
			}
		}
		render executionObj
	}
	
	/**
	 * REST API :- For fetching all execution names greater than the perticular date of execution
	 * - Return execution name
	 * - date of execution
	 * - Execution Status
	 * - Failure status
	 * - All  execution list
	 * @param dateOfExecution
	 * @return
	 */
	def getExecutionList(final String dateOfExecution){
		JsonArray totalExecutionList = new JsonArray()
		if(dateOfExecution){
		try{
			SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd hh:mm:SS.s");
			Date dateObj = new Date().parse("yyyy-MM-dd hh:mm:SS.s", dateOfExecution)
			def executionList = Execution.withCriteria{
				ge("dateOfExecution", dateObj)
			}
			executionList.each{execution->
				JsonObject executionObj = new JsonObject()
				executionObj.addProperty("ExecutionName",execution?.name?.toString())
				executionObj.addProperty("DateOfExecution",execution?.dateOfExecution?.toString())
				executionObj.addProperty("ExecutionStatus",execution?.executionStatus)
				totalExecutionList.add(executionObj)
			}
		}catch(Exception e){
			JsonObject errorObj =  new JsonObject()
			errorObj.addProperty("Status","FAILURE")
			errorObj.addProperty("Remarks "," Invalid date format ")
			totalExecutionList.add(errorObj)
		}
		}else{
			def executionList = Execution.findAll()
			executionList.each{  execution ->
				JsonObject executionObj = new JsonObject()
				executionObj.addProperty("ExecutionName",execution?.name?.toString())
				executionObj.addProperty("DateOfExecution",execution?.dateOfExecution?.toString())
				executionObj.addProperty("ExecutionStatus",execution?.executionStatus)
				totalExecutionList.add(executionObj)
			}
		}
		render totalExecutionList
	}
	
/**
	 * REST API : for executing multiple script
	 *  Input parameter
	 *  	- scripts : script list
	 *  	- stbName :  device name
	 *  	- reRunOnFailure
	 *  	- timeInfo
	 *  	- performance
	 *  	- isLogRequired
	 */

	def thirdPartyMultipleScriptExecution(final String scripts, final String stbName ,final String reRunOnFailure, final String timeInfo,final String performance,final String isLogRequired, final String isAlert){
		String rerun = FALSE
		if(reRunOnFailure && reRunOnFailure?.equals(TRUE)){
			rerun = TRUE
		}
		def deviceInstanceIsThunder = Device.findByStbName(stbName)
		String time = FALSE
		String perfo = FALSE
		String isLog = FALSE
		String isAlertEnabled = FALSE
		if(deviceInstanceIsThunder?.isThunderEnabled != 1){
			if(timeInfo && timeInfo?.equals(TRUE)){
				time = TRUE
			}
			if(performance && performance?.equals(TRUE)){
				perfo = TRUE
			}
		}
		if(isLogRequired && isLogRequired?.equals(TRUE)){
			isLog = TRUE
		}
		if(isAlert && isAlert?.equals(TRUE) && deviceInstanceIsThunder?.isThunderEnabled == 1){
			isAlertEnabled = TRUE
		}
		JsonObject jsonOutData = new JsonObject()
		boolean validScript = false
		boolean  scriptStatusFlag = false
		boolean  scriptVersionFlag = false
		String outData = ""
		def executionNameForCheck
		String filePath = "${request.getRealPath('/')}//fileStore"
		String htmlData = ""
		def scriptList  = scripts.tokenize(",")
		def deviceInstance = Device.findByStbName(stbName)
		def newScriptList = []
		boolean executed = false
		boolean valid = false;
		boolean TCL = false;
		def category
		def newCategory
		if(deviceInstance){
			category = deviceInstance.category
			if(scriptList?.size() > 0){
				int i =0;
				String scriptType  = MULTIPLESCRIPT
				def moduleInstance
				scriptList.each { script ->
					
					if(category?.toString()?.equals(RDKB)){
						def scriptName
						if((scriptService?.tclScriptsList?.toString()?.contains(script?.trim()))  ){
							TCL = true
						}
						scriptName = script?.toString()
						boolean compoundTCL = false
						def combainedTclScript =  scriptService?.combinedTclScriptMap
						combainedTclScript?.each{
							if(it?.value?.toString().contains(script)){
								compoundTCL = true
							}
						}
						if((scriptService?.totalTclScriptList?.toString()?.contains(script)) && compoundTCL ){
							combainedTclScript?.each{
								if(it?.value?.toString()?.contains(script)){
									scriptName= script?.toString()
									script = it.key?.toString()
									TCL = true
								}
							}
						}
						if(Utility.isTclScriptExists(realPath,  script)) {
							if(Utility.isConfigFileExists(realPath, deviceInstance?.stbName)){
								if(compoundTCL){
									newScriptList << scriptName
								}else{
									newScriptList << script
								}
								validScript = true
								valid =true
								TCL = true
							}
							else{
								outData = "   No Config file is available with name Config_${deviceInstance?.stbName}.txt"
							}
						}else{
							outData = "   No TCL Script is available with name ${script}"
						}
					}					
					if(TCL?.toString()?.equals(FALSE)){
						def moduleName= scriptService.scriptMapping.get(script)
						if( moduleName){
							moduleInstance= Module?.findByName(moduleName)
							def scriptInstance1 = scriptService?.getScript(getRealPath()?.toString(),moduleInstance?.toString(), script?.toString(), moduleInstance?.category?.toString())
							if(scriptInstance1){
								if(executionService.validateScriptBoxTypes(scriptInstance1,deviceInstance)){
									scriptStatusFlag = true
									String rdkVersion = executionService.getRDKBuildVersion(deviceInstance);
									if(executionService.validateScriptRDKVersions(scriptInstance1,rdkVersion)){
										scriptVersionFlag = true
										validScript = true
										newScriptList << script
									}
								}
							}
						}
					}
				}
				if(validScript && newScriptList?.size() > 0 ){
					if(!TCL){
						if(scriptStatusFlag && scriptVersionFlag){
							valid = true
						}else {
							valid = false
						}
					}
					if(valid){
						String status = ""
						try {
							status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
							synchronized (lock) {
								if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
									status = "BUSY"
								}else{
									if((status.equals( Status.FREE.toString() ))){
										if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
											executionService.deviceAllocatedList.add(deviceInstance?.id)
											Thread.start{
												deviceStatusService.updateOnlyDeviceStatus(deviceInstance, Status.BUSY.toString())
											}
										}
									}
								}
							}
						}
						catch(Exception eX){
						}
						if((status.equals( Status.FREE.toString() ))){
							try{
								if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
									executionService.deviceAllocatedList.add(deviceInstance?.id)
								}
								//	def newCategory
								if(!TCL){
									newCategory = moduleInstance?.category
								}else{
									newCategory = RDKB_TCL
								}
								
								def execution
								def executionSaveStatus = true
								DateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT1)
								Calendar cal = Calendar.getInstance()
								def deviceName = deviceInstance?.stbName
								String  url = getApplicationUrl()
								def execName = CI_EXECUTION+deviceName+dateFormat.format(cal.getTime()).toString()
								def newExecName = execName
								if(scriptType.equals(MULTIPLESCRIPT)){
									def  scriptCount = newScriptList?.size()
									executionSaveStatus = executionService.saveExecutionDetailsOnMultipleScripts(execName?.toString(), MULTIPLESCRIPT, deviceName, null,url,time,perfo,rerun,isLog,scriptCount, newCategory?.toString(),FALSE,isAlertEnabled)
								}
								if(executionSaveStatus){
									try{
										execution = Execution.findByName(execName)
										def executionDevice = new ExecutionDevice()
										executionDevice.execution = execution
										executionDevice.dateOfExecution = new Date()
										executionDevice.device = deviceInstance?.stbName
										executionDevice.boxType = deviceInstance?.boxType?.name
										executionDevice.deviceIp = deviceInstance?.stbIp
										executionDevice.status = UNDEFINED_STATUS
										executionDevice.buildName = executionService.getBuildName( deviceInstance?.stbName )
										//executionDevice.category = moduleInstance?.category
										executionDevice.category =Utility.getCategory(newCategory?.toString())
										if(executionDevice.save(flush:true)){
											String getRealPathString  = getRealPath()
											if(deviceInstance?.isThunderEnabled != 1){
												executionService.executeVersionTransferScript(getRealPathString,filePath,execName, executionDevice?.id, deviceInstance?.stbName, deviceInstance?.logTransferPort, url)
											}else{
												StormExecuter.createThunderVersionFile(getRealPathString, execution?.id, executionDevice?.id, executionDevice?.deviceIp)
											}
											if(!TCL){
												htmlData = executescriptService.executeScriptInThread(true,execName, ""+deviceInstance?.id, executionDevice, newScriptList, "", execName,
														filePath, getRealPath(), SINGLE_SCRIPT, url, time, perfo, rerun,isLog,newCategory?.toString(),1,isAlertEnabled)
												executed = true
												url = url + "/execution/thirdPartyJsonResult?execName=${execName}"
												jsonOutData.addProperty("Status", "RUNNING")
												jsonOutData.addProperty("Remarks", url)
											}else{
												htmlData = tclExecutionService.executeScriptInThread(execName,""+deviceInstance?.id, executionDevice, newScriptList, "", execName,
														filePath, getRealPath(), SINGLE_SCRIPT, url, time, perfo, rerun,isLog,newCategory?.toString())
												executed = true
												url = url + "/execution/thirdPartyJsonResult?execName=${execName}"
												jsonOutData.addProperty("Status", "RUNNING")
												jsonOutData.addProperty("Remarks", url)

											}
										}
									}catch(Exception e){
										println " ERROR "+e.getMessage()
									}
								}else{
									outData= "Error while saving execution parameters "
								}
							}
							catch(Exception e){
								println " ERROR"+e.getMessage()
							}
						}else if(status.equals( Status.ALLOCATED.toString() )){
							outData = " Device ${deviceInstance?.stbName} is not free to execute Scripts"
						}
						else if(status.equals( Status.NOT_FOUND.toString() )){

							outData =  " Device ${deviceInstance?.stbName} is not free to execute Scripts"
						}
						else if(status.equals( Status.HANG.toString() )){
							outData =  " Device ${deviceInstance?.stbName} is not free to execute Scripts"
						}
						else if(status.equals( Status.BUSY.toString() )){
							outData =  " Device ${deviceInstance?.stbName} is not free to execute Scripts"

						}else if(status.equals( Status.TDK_DISABLED.toString() )){

							outData =  "TDK is not enabled  in the Device to execute scripts"
						}
						else{
							outData =  " Device ${deviceInstance?.stbName} is not free to execute Scripts"
						}
					}else{
						if(!scriptStatusFlag){
							outData = " BoxType of Scripts in ScriptGroup is not matching with BoxType of Device ${deviceInstance?.stbName}"
						}else if(!scriptVersionFlag){
							outData = " RDK Version of Scripts in ScriptGroup is not matching with RDK Version of Device ${deviceInstance?.stbName}"
						}
					}
				}else{
					if(TCL){
						outData = outData
					}else{
						outData = "No valid script list found for execution  "
					}
				}
			}else{
				outData = " script list empty   "
			}
		}else{
			outData = "No device found with this name "+stbName
		}
		if(!executed){
			jsonOutData.addProperty("Status", "FAILURE")
			jsonOutData.addProperty("Remarks", outData)
		}
		render jsonOutData
	}

	/**
	 * REST API : for getting the image name on a particular device
	 * - Accessing the getimagename_cmndline file
	 * - send command through TM ( python getimagename_cmndline.py Device_IP_Address PortNumber )
	 * @param stbName
	 * @return
	 */
	def getDeviceImageName(String stbName){
		JsonObject jsonOutData = new JsonObject()
		Device device = Device.findByStbName(stbName)
		if(device){
			try{
				File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//getimagename_cmndline.py").file
				println layoutFolder
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
					jsonOutData.addProperty("Status", "SUCCESS")
					jsonOutData.addProperty("DeviceIp", device?.stbIp)
					jsonOutData?.addProperty("ImageName",outputData.toString()?.trim())
				}
				else{
					jsonOutData.addProperty("Status", "FAILURE")
					jsonOutData?.addProperty("Remarks", "Image name not available")
				}
			}catch(Exception e ){
				println  "ERROR "+ e.getMessage()
				jsonOutData.addProperty("Status", "FAILURE")
				jsonOutData?.addProperty("Remarks", "Image name not available")
			}
		}else{
			jsonOutData.addProperty("Status", "FAILURE")
			jsonOutData.addProperty("Remarks", "No device found with this name "+stbName)
		}
		render jsonOutData
	}
	
		
	/**
	 * REST API : invoked by devices to upload the logs to TM
	 */
	def uploadLogs(String fileName){
		String data = "";
		try {
			if(params?.logFile){
				def uploadedFile = request.getFile("logFile")
				if(uploadedFile){
					InputStreamReader reader = new InputStreamReader(uploadedFile?.getInputStream())
					def fileContent = reader?.readLines()
					String realPathForLogs = getRealPathForLogs()
					def logPath = realPathForLogs + "/logs//logs"
					File logFile = new File(logPath+"//${fileName}")
					logFile.write ""
					fileContent?.each { logg ->
						data = data + logg+"\n";
						logFile << logg+"\n"
					}
				}
			}
		}catch(Exception e ){
			println  "uploadLogs ERROR "+ e.getMessage()
		}
		render data;
	}
	
	/**
	 * REST API : invoked by devices to upload the logs to TM which will append if the file exists
	 */
	def securedUploadLogs(String fileName){
		String data = "";
			try {
				String deviceStreams , deviceOcapId
				def node
				if(params?.logFile){
					def uploadedFile = request.getFile("logFile")
					if(uploadedFile){
						InputStreamReader reader = new InputStreamReader(uploadedFile?.getInputStream())
						def fileContent = reader?.readLines()
						String realPathForLogs = getRealPathForLogs()
						def logPath = realPathForLogs + "/logs//logs"
						File logFile = new File(logPath+"//${fileName}")
						fileContent?.each { logg ->
							data = data + logg+"\n";
							logFile << logg+"\n"
						}
					}
				}
			}catch(Exception e ){
				println  "uploadLogs ERROR "+ e.getMessage()
			}
			render data;
	}
	
	/**
	 * REST API : Method to get the module wise execution status
	 */
	def getExecutionStatus(String execName){
		def jsonObjMap = [:]
		Execution executionInstance = Execution.findByName(execName)
		if(executionInstance){
		jsonObjMap.put(EXECUTION_NAME, execName)
		def detailDataMap = executedbService.prepareDetailMap(executionInstance,request.getRealPath('/'))
		def tDataMap = [:]
		int total = 0
		detailDataMap?.keySet()?.each { k ->
			Map mapp = detailDataMap?.get(k)
			int tCount = 0
			mapp?.keySet()?.each { status ->
				def tStatusCounter = tDataMap.get(status)
				def statusCounter = mapp.get(status)
				if(!tStatusCounter){
					tStatusCounter = 0
				}
				if(!status.equals(PENDING)){
					tCount = tCount + statusCounter
					tStatusCounter = tStatusCounter + statusCounter
					tDataMap.put(status, tStatusCounter)
				}
			}
			mapp.put(EXECUTED, tCount)
			def success = mapp?.get(SUCCESS)
			if(success){
				int rate = 0
				if(tCount > 0){
					int na = 0
					if(mapp?.keySet().contains(NOT_APPLICABLE_STATUS)){
						na = mapp?.get(NOT_APPLICABLE_STATUS)
					}
					rate = ((success * 100)/(tCount - na))
				}
				mapp.put(PASS_RATE,rate)
			}
			total = total + tCount
		}
		tDataMap.put(EXECUTED, total)
		int rate
		if(tDataMap?.get(SUCCESS)){
			int success = tDataMap?.get(SUCCESS)
			int na = 0
			if(tDataMap?.keySet().contains(NOT_APPLICABLE_STATUS)){
				na = tDataMap?.get(NOT_APPLICABLE_STATUS)
			}
			rate = ((success * 100)/(total - na))
		}
		tDataMap.put(PASS_RATE,rate)
		def executionDeviceList = ExecutionDevice.findAllByExecution(executionInstance)
		def device = Device.findByStbName(executionInstance?.device)
		jsonObjMap.put(DEVICE_NAME, executionInstance?.device)
		if(executionInstance?.script){
			jsonObjMap.put(SCRIPT, executionInstance?.script)
		}else if(executionInstance?.scriptGroup){
			jsonObjMap.put(SCRIPT_GROUP, executionInstance?.scriptGroup)
		}
		jsonObjMap.put(EXECUTION_STATUS, executionInstance?.executionStatus)
		jsonObjMap.put(RESULT, executionInstance?.result)
		jsonObjMap.put(DATE, executionInstance?.dateOfExecution?.toString())
		jsonObjMap.put(DATATMAP, tDataMap)
		jsonObjMap.put(DETAIL_DATA_MAP,detailDataMap)
		}else{
			jsonObjMap.put(STATUS,FAILED)
			jsonObjMap.put(REMARKS, "No execution found with this name "+execName)
		}
		render jsonObjMap as JSON
	}
	
	/**
	 * REST API : Method to get the TM IP Address
	 */
	def getTMIPAddress(String type, String preference){
		def jsonObjMap = [:]
		String ipAddress = null
		String ipAddressFromUrl = null
		File configFile = grailsApplication.parentContext.getResource("/fileStore/tm.config").file
		String currenturl = request.getRequestURL().toString();
		String[] urlArray = currenturl.split( URL_SEPERATOR );
		String url = urlArray[INDEX_TWO]
		ipAddressFromUrl = url.split( ":" )[0];
		
		if(type?.equals(IPV6_INTERFACE)){
			jsonObjMap.put(STATUS,SUCCESS)
			if(preference?.equals("dns")){
				InetAddressValidator validator = InetAddressValidator.getInstance();
				if (validator.isValidInet4Address(ipAddressFromUrl)) {
					ipAddress = InetUtility.getIPAddress(configFile, Constants.IPV6_INTERFACE)
					ipAddress = "["+ipAddress+"]"
				}else{
					ipAddress = ipAddressFromUrl
				}
			}else{
				ipAddress = InetUtility.getIPAddress(configFile, Constants.IPV6_INTERFACE)
				ipAddress = "["+ipAddress+"]"
			}
		}
		else if(type?.equals(IPV4_INTERFACE)){
			jsonObjMap.put(STATUS,SUCCESS)
			if(preference?.equals("dns")){
				InetAddressValidator validator = InetAddressValidator.getInstance();
				if (validator.isValidInet4Address(ipAddressFromUrl)) {
					ipAddress = InetUtility.getIPAddress(configFile, Constants.IPV4_INTERFACE)
				}else{
					ipAddress = ipAddressFromUrl
				}
			}else{
				ipAddress = InetUtility.getIPAddress(configFile, Constants.IPV4_INTERFACE)
			}
		}else{
			jsonObjMap.put(STATUS,FAILED)
			jsonObjMap.put(REMARKS, "Not a supported IP Type "+type)
		}
		if(ipAddress != null){
			jsonObjMap.put("IP",ipAddress)
		}
		jsonObjMap.put("type",type)
		render jsonObjMap as JSON
	}
	
	
	/*To handle the complete log download request*/
	def downloadLogs(){
		String executionId = params?.id
		
		String logType = ALL_LOGS
		if(params?.logType && params?.logType?.equals("FAILURE")){
			logType = FAILURE_LOGS
		}
		try {
			Execution exec = Execution.get(executionId)
			String fileName = exec?.name
			if(exec){
				params.format = EXPORT_ZIP_FORMAT
				params.extension = EXPORT_ZIP_EXTENSION
				response.contentType = grailsApplication.config.grails.mime.types[params.format]
				fileName = fileName?.replaceAll(" ","_")
				response.setHeader("Content-Type", "application/zip")
				response.setHeader("Content-disposition", "attachment; filename=ExecutionLogs_"+ fileName +".${params.extension}")
				logZipService.zipLogs(getRealPath() , response.outputStream , executionId , logType)
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
	
	
	/**
	 * Method to define the bar color based on pass %
	 */
	def getBarChartColors(final def passPer){

		def color ="#18c561"
		try {
			int perc = passPer
			if ( perc == 100){
				color = "#10bf4d"
			}else if ( perc >=80 && perc < 100){
				color = "#67e84d"
			}else if ( perc >50 && perc < 80){
				color = "#f19e0e"
			}else if (perc <= 50){
				color = "#f63c0a"
			}
		} catch (Exception e) {
			e.printStackTrace()
		}

		return color
	}
	
	/*
	 * Function to dynamically get Thunder logs until thunder script execution gets finished
	 */
	def readOutputFileDataThunder(){
        File configFile = grailsApplication.parentContext.getResource(Constants.STORM_CONFIG_FILE).file
        String STORM_FRAMEWORK_LOCATION = StormExecuter.getConfigProperty(configFile,Constants.STORM_FRAMEWORK_LOCATION) + Constants.URL_SEPERATOR
        String folderName = Constants.SCRIPT_OUTPUT_FILE_PATH_STORM
		String fullLogFilePath = folderName+params?.executionName+Constants.UNDERSCORE+Constants.FULLLOG_LOG
		File fullLogFile = grailsApplication.parentContext.getResource(fullLogFilePath).file
		String fullLogFileAbsolutePath = fullLogFile.getAbsolutePath()
		String STORM_FRAMEWORK_LOG_LOCATION_SINGLE = STORM_FRAMEWORK_LOCATION+Constants.SRC+File.separator+Constants.LOGS+File.separator
		String LOG_FILE_LOCATION
		BufferedReader reader
		if(params?.suiteName == SUITE || params?.suiteName == MULTIPLE_STORM){
			LOG_FILE_LOCATION = fullLogFileAbsolutePath
		}else{
		    LOG_FILE_LOCATION = STORM_FRAMEWORK_LOG_LOCATION_SINGLE+params?.scriptName+Constants.JAVASCRIPT_EXTENSION+Constants.UNDERSCORE+params?.executionName+Constants.UNDERSCORE+Constants.EXECUTION_LOG
		}
        File log_file = new File(LOG_FILE_LOCATION)
        String output= ""
        try{
            if(log_file.exists()){
                reader = new BufferedReader(new FileReader(LOG_FILE_LOCATION));
            }
            String line = reader?.readLine();
            while(line != null){
                output = output + line + HTML_BR
                line = reader?.readLine()
            }
            reader?.close()
        }catch(Exception e){
            e.printStackTrace()
        }
        render output as String
	}
	
	/**
	 * Function to get the execution name according to execution id
	 * @return
	 */
	def getExecutionName(){
		Execution executionInstance = Execution.findById(params?.id)
		render executionInstance?.name
	}
	
	/**
	 * Function to return list of execution names according to execution id's
	 * @return
	 */
	def getExecutionNamesAsList(){
		def selectedRows = []
		def selectedRowsDefined = []
		def executionNameList = ""
		if(params?.checkedRows != UNDEFINED && params?.checkedRows != BLANK_SPACE && params?.checkedRows != null){
			selectedRows = params?.checkedRows.split(COMMA_SEPERATOR)
			for(int i=0;i<selectedRows.size();i++){
				if(selectedRows[i] != UNDEFINED){
					selectedRowsDefined.add(selectedRows[i])
				}
			}
		}
		for(int i=0;i<selectedRowsDefined.size();i++){
			Execution executionInstance = Execution.findById(selectedRowsDefined[i])
			executionNameList = executionInstance?.name + "," + executionNameList
		}
		executionNameList = executionNameList.substring(0, executionNameList.length() - 1);
		render executionNameList
	}
	
	/**
	 * Function to check if the list of executions are valid
	 * @return
	 */
	def checkValidMultipleExecutions(){
		def execNames = params?.execNames
		List executionNameList = execNames?.split(",")
		def validCheck
		for(int i=0;i<executionNameList.size();i++){
			Execution executionInstance = Execution.findByName(executionNameList[i])
			if(executionInstance){
				validCheck =  true
			}else{
				validCheck =  false
				break
			}
		}
		if(validCheck){
			render "valid"
		}else{
			render "invalid"
		}
	}
	
	/**
	 * Get the list of scripts of an execution
	 * @param executionName
	 * @return
	 */
	def getScriptsByExecution(String executionName){
		def rdkScriptList = []
		Execution execution = Execution.findByName(executionName)
		if(execution){
			ExecutionDevice executionDevice  = ExecutionDevice.findByExecution(execution)
			List executionResultList =  ExecutionResult.findAllByExecutionAndExecutionDevice(execution,executionDevice)
			for(int i=0;i<executionResultList.size();i++){
				List performanceList = Performance.findAllByExecutionResult(executionResultList[i])
				if(!(performanceList.isEmpty())){
					rdkScriptList.add(executionResultList[i]?.script)
				}
			}
		}
		render rdkScriptList as JSON
	}
	
	/**
	 * Method to fetch the result of an execution
	 * @param execResId
	 * @return
	 */
	def triggerNewExecution(){
		def execId = params?.execId
		def ex
		def category
		def deviceList
		List freeDeviceNameList = []
		def scriptCategory
		try{
			if(execId){
				ex = Execution.findById(execId)
				if(ex){
					def execRes = ExecutionResult.findByExecution(ex)
					def script = ScriptFile.findByScriptName(execRes?.script)
					scriptCategory = script?.category?.toString()
				}
			}
			if(ex?.category){
				deviceList = Device.findAllByCategory(ex?.category)
				if(deviceList){
					deviceList?.each{
						if(it?.deviceStatus == Status.FREE){
							if(ex?.category.toString() == Constants.RDKV && scriptCategory && (scriptCategory == Constants.RDKV_THUNDER || scriptCategory == Constants.RDKV_RDKSERVICE)){
								if(it?.isThunderEnabled == 1){
									freeDeviceNameList.add(it?.stbName)
								}
							}else{
								if(it?.isThunderEnabled == 0){
									freeDeviceNameList.add(it?.stbName)
								}
							}
						}
					}
				}
			}
			category = ex?.category
		}catch(Exception e){
			e.printStackTrace()
		}
		render(template: "triggerNewExecution", model: [execId : ex?.id, category : category, freeDeviceList : freeDeviceNameList])
	}

	/**
	 * Method to fetch the devices that are FREE at present 
	 * @return
	 */
	def getFreeDevicesList(){
		def execId = params?.exId
		def ex
		def category
		def deviceList
		List freeDeviceNameList = []
		def scriptCategory
		try{
			if(execId){
				ex = Execution.findById(execId)
				if(ex){
					def execRes = ExecutionResult.findByExecution(ex)
					def script = ScriptFile.findByScriptName(execRes?.script)
					scriptCategory = script?.category?.toString()
					category = ex?.category
				}
				if(category){
					deviceList = Device.findAllByCategory(category)
					if(deviceList){
						deviceList?.each{
							if(it?.deviceStatus == Status.FREE){
								if(ex?.category?.toString() == Constants.RDKV && scriptCategory && (scriptCategory == Constants.RDKV_THUNDER || scriptCategory == Constants.RDKV_RDKSERVICE)){
									if(it?.isThunderEnabled == 1){
										freeDeviceNameList.add(it?.stbName)
									}
								}else{
									if(it?.isThunderEnabled == 0){
										freeDeviceNameList.add(it?.stbName)
									}
								}
							}
						}
					}
				}
			}
		}catch(Exception e){
			e.printStackTrace()
		}
		render freeDeviceNameList as JSON
	}
	
	/**
	 * Method to execute scripts from execution result pop-up
	 * @return
	 */
	def triggerExecutionFromPopUp(){
		def executionResultIdString = params?.exResults
		List executionResultIdList = []
		executionResultIdList = executionResultIdString.split(",")
		executionResultIdList.remove(0)
		def scriptList = []
		def executionResultObjectList = []
		def baseExecution
		def executionName = params?.executionName
		executionResultIdList?.each{
			def exRes = ExecutionResult.findById(it)
			baseExecution = exRes?.execution
			def scriptName = exRes?.script 
			if(!scriptList?.contains(scriptName)){
				scriptList.add(scriptName)
				executionResultObjectList.add(exRes)
			}
		}
		def deviceInstance = Device.findByStbName(params?.device)
		String category = deviceInstance?.category?.toString()
		String status = ""
		boolean allocated = false
		if(deviceInstance){
			try {
				status = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
				if(executionService.deviceAllocatedList.contains(deviceInstance?.id)){
					status = "BUSY"
				}else{
					if((status.equals( Status.FREE.toString() ))){
						if(!executionService.deviceAllocatedList.contains(deviceInstance?.id)){
							allocated = true
							executionService.deviceAllocatedList.add(deviceInstance?.id)
							Thread.start{
								deviceStatusService.updateOnlyDeviceStatus(deviceInstance, Status.BUSY.toString())
							}
						}
					}
				}
			}catch(Exception e){
				e.printStackTrace()
			}
		}
		def executionSaveStatus
		def scriptName = ""
		def executionInstance
		def realPath = getRealPath()
		def filePath = "${request.getRealPath('/')}//fileStore"
		def appUrl = getApplicationUrl()
		def scriptInstance
		boolean aborted = false
		boolean pause = false
		def htmlData
		List pendingScripts = []
		if(scriptList?.size() == 1){
			scriptName = scriptList[0]
		}else{
			scriptName = MULTIPLESCRIPT
		}
		def isAlertEnabled = FALSE
		if(baseExecution?.isAlertEnabled && deviceInstance?.isThunderEnabled == 1){
			isAlertEnabled  = TRUE
		}
		try{
			executionSaveStatus = executionService.saveExecutionDetails(executionName,[scriptName:scriptName, deviceName:params?.device, scriptGroupInstance:null, appUrl:appUrl, isBenchMark:"false", isSystemDiagnostics:"false", rerun:"false", isLogReqd:"false", category:category, rerunOnFailure:FALSE, groups:baseExecution?.groups, isAlertEnabled:isAlertEnabled])
			if(executionSaveStatus){
				Execution.withTransaction{
					executionInstance = Execution.findByName(executionName)
				}
				def deviceBoxType = deviceInstance?.boxType
				def deviceBoxTypeName = deviceBoxType.name
				ExecutionDevice executionDevice = null
				ExecutionDevice.withTransaction {
					executionDevice = new ExecutionDevice()
					executionDevice.execution = executionInstance
					executionDevice.device = deviceInstance?.stbName
					executionDevice.boxType = deviceBoxTypeName
					executionDevice.deviceIp = deviceInstance?.stbIp
					executionDevice.dateOfExecution = new Date()
					executionDevice.status = UNDEFINED_STATUS
					executionDevice.category = Utility.getCategory(category)
					executionDevice.buildName = executionService.getBuildName( deviceInstance?.stbName )
					executionDevice.save(flush:true)
				}
				if(deviceInstance?.isThunderEnabled != 1){
					executionService.executeVersionTransferScript(realPath, filePath, executionName, executionDevice?.id, deviceInstance?.stbName, deviceInstance?.logTransferPort, appUrl)
				}else{
					try{
						def executionObjectId = executionInstance?.id
						StormExecuter.createThunderVersionFile(realPath, executionObjectId, executionDevice?.id, executionDevice?.deviceIp)
					}catch(Exception e){
						e.printStackTrace()
					}
				}
				try{
					if(scriptList?.size() > 0 && deviceInstance?.isThunderEnabled != 1){
						LogTransferService.transferLog(executionName, deviceInstance)
					}
				}catch(Exception e){
					e.printStackTrace()
				}
				executionResultObjectList.each{ executionResult ->
					def scriptFile = ScriptFile.findByScriptName(executionResult?.script)
					scriptInstance = scriptService.getScript(realPath,scriptFile?.moduleName,scriptFile?.scriptName, category)
					def deviceStatus = " "
					try{
						deviceStatus = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceInstance)
					}catch (Exception e){
						e.printStackTrace()
					}
					if(scriptInstance){
						String rdkVersion = executionService.getRDKBuildVersion(deviceInstance)
						if(executionService.validateScriptBoxTypes(scriptInstance,deviceInstance) && executionService.validateScriptRDKVersions(scriptInstance,rdkVersion) ){
							def startExecutionTime = new Date()
							aborted = executionService.abortList?.toString().contains(executionInstance?.id?.toString())
							if(!aborted && !(deviceStatus?.toString().equals(Status.NOT_FOUND.toString()) || deviceStatus?.toString().equals(Status.HANG.toString())) && !pause){
								htmlData = executescriptService.executeScript(executionName, executionDevice, scriptInstance, deviceInstance, appUrl, filePath, realPath,"false","false",executionName,FALSE,null,"false", category,isAlertEnabled)
							}else{
								if(!aborted && (deviceStatus.equals(Status.NOT_FOUND.toString()) ||  deviceStatus.equals(Status.HANG.toString()))){
									pause = true
								}
								if(!aborted && pause) {
									try{
										pendingScripts.add(scriptInstance)
										ExecutionResult.withTransaction { resultstatus ->
											try {
												def executionResult1 = new ExecutionResult()
												executionResult1.execution = executionInstance
												executionResult1.executionDevice = executionDevice
												executionResult1.script = scriptInstance?.name
												executionResult1.device = deviceInstance?.stbName
												executionResult1.execDevice = null
												executionResult1.deviceIdString = deviceInstance?.id?.toString()
												executionResult1.status = PENDING
												executionResult1.dateOfExecution = new Date()
												executionResult1.category=Utility.getCategory(executionDevice?.category?.toString())
												if(! executionResult1.save(flush:true)) {
												}
												resultstatus.flush()
											}
											catch(Throwable th) {
												resultstatus.setRollbackOnly()
											}
										}
									}catch(Exception e){
										e.printStackTrace()
									}
								}
							}
							def endExecutionTime = new Date()
							executescriptService.executionTimeCalculation(executionName,startExecutionTime,endExecutionTime)
						}
					}
				}
				try{
					if(scriptList.size() > 0 && deviceInstance?.isThunderEnabled != 1){
						LogTransferService.closeLogTransfer(executionName)
					}
				}catch(Exception e){
					e.printStackTrace()
				}
				if(aborted && executionService.abortList.contains(executionInstance?.id?.toString())){
					executionService.abortList.remove(executionInstance?.id?.toString())
					executionService.saveExecutionStatus(aborted, executionInstance?.id)
				}
				if(!aborted && pause && pendingScripts.size() > 0 ){
					executionService.savePausedExecutionStatus(executionInstance?.id)
					executionService.saveExecutionDeviceStatusData(PAUSED, executionDevice?.id)
				}
				if(!aborted && !pause){
					executionService.saveExecutionStatus(aborted,executionInstance?.id)
				}
			}
			if(allocated && executionService.deviceAllocatedList.contains(deviceInstance?.id)){
				executionService.deviceAllocatedList.remove(deviceInstance?.id)
			}
		}catch(Exception e){
			e.printStackTrace()
		}
	}
	
	/**
	 * Function to fetch data from grafana
	 * @param executionResultId
	 * @param parameter
	 * @return
	 */
	def fetchDataFromGrafana(String executionResultId,String parameter,String actualUnit,String preferredUnit, boolean isSystemMetric){
		List dataArrayList = []
		String basicUrl = getGrafanaConfigurations("grafanaUrl")
		String prefix = getGrafanaConfigurations("prefix")
		String datasourceId = getGrafanaConfigurations("datasourceId")
		def insecure = getGrafanaConfigurations("insecure")
		def curlTimeout = getGrafanaConfigurations("curlTimeOutInSeconds")
		if(basicUrl != null && prefix != null && datasourceId != null ){
			ExecutionResult execResult = ExecutionResult.findById(executionResultId)
			if(execResult){
				Date fromDate = execResult?.dateOfExecution
				Device dev =  Device.findByStbName(execResult?.device?.toString())
				String macAddress = dev?.serialNo
				if(macAddress != null){
					try{
						boolean unitsSame = true
						if(!actualUnit?.equals(preferredUnit)){
							unitsSame = false
						}
						if(macAddress?.contains(":")){
							macAddress = macAddress?.replace(":","")
						}	
						if(macAddress?.contains("_")){
							macAddress = macAddress?.replace("_","")
						}
						macAddress = macAddress?.toUpperCase()
						long fromEpoch = fromDate?.getTime() / 1000;
						Date toDate = new Date()
						long toEpoch = System?.currentTimeMillis() / 1000;
						String fromEpochTime = fromEpoch?.toString()
						String toEpochTime = toEpoch?.toString()
						
						
						String prefixLastChar = prefix?.charAt(prefix?.length()-1)
						if(!prefixLastChar?.equals(".")){
							prefix = prefix + "."
						}
						String host = prefix + macAddress
						String basicUrlLastChar = basicUrl?.charAt(basicUrl?.length()-1)
						if(!basicUrlLastChar?.equals("/")){
							basicUrl = basicUrl + "/"
						}
						basicUrl = basicUrl + "api/datasources/proxy/" + datasourceId +"/render?"
						List parameterList = []
						String targetString = ""
						parameterList = parameter?.split(",")
						parameterList?.each{ param ->
							targetString = targetString + "&target="+host+"."+param
						}
						
						String insecureString = ""
						def curlTimeoutString = "10"
						if(curlTimeout != null){
							curlTimeoutString = curlTimeout
						}
						if(insecure != null){
							if(insecure == "true"){
								insecureString = " --insecure"
							}
						}
						String url = basicUrl + "from="+fromEpochTime+"&until="+toEpochTime+""+targetString+"&format=json"
						String command = "curl" +insecureString+ " --connect-timeout "+ curlTimeoutString+ " \""+url+"\""
						ProcessBuilder pb;
						Process p;
						pb = new ProcessBuilder("bash", "-c", command);
						p = pb.start();
						String line;
						BufferedReader input = new BufferedReader(new InputStreamReader(p.getInputStream()));
						line = input.readLine();
						if((line != null) && (!line?.contains("message"))){
							JSONArray dataArray = new JSONArray(line)
							if(dataArray?.size() != 0){
								JsonArray writeDataArray = new JsonArray()
								for(int i = 0;i < dataArray?.size();i++){
									Map dataMap = [:]
									JsonObject dataNode = new JsonObject()
									List dataList = []
									List dataListForLogFile = []
									String dataValue = dataArray[i]
									if(dataValue != null && !dataValue?.isEmpty()){
										JSONObject jsonObj = new JSONObject(dataValue);
										
										String target
										if(jsonObj.has('target')){
											target = jsonObj.get('target')
										}
										if(jsonObj.has('datapoints')){
											String displayUnit = ""
											if((preferredUnit != null) && (!preferredUnit?.equals(""))){
												displayUnit = " ("+preferredUnit +")"
											}
											List datapoints = jsonObj.get('datapoints')
											datapoints.each{ dataPoint ->
												if(!(JSONObject.NULL?.equals(dataPoint[0]))){
													List eachDataList = []
													long epochTime = dataPoint[1]
													epochTime = epochTime * 1000
													SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
													def convertedTime = sdf.format(new Date(epochTime))
													float dataPointFloat = (float)dataPoint[0];
													if(unitsSame){
														dataPointFloat = dataPointFloat.round(3)
														dataList.add(dataPointFloat)
														eachDataList.addAll(convertedTime,dataPointFloat)
													}else{
														int divideNumber =  1
														if((actualUnit?.equals("Bytes") && preferredUnit?.equals("MB"))){
															divideNumber = 1000000
														}else if((actualUnit?.equals("Bytes") && preferredUnit?.equals("KB"))){
															divideNumber = 1000
														}else if((actualUnit?.equals("KB") && preferredUnit?.equals("MB"))){
															divideNumber = 1000
														}
														def result = dataPointFloat / divideNumber
														result = result.round(2)
														dataList.add(result)
														eachDataList.addAll(convertedTime,result)
													}
													dataListForLogFile?.add(eachDataList)
												}
											}
											if(!dataListForLogFile.isEmpty()){
												String parameterForLog = target?.toString() + displayUnit
												dataNode.addProperty("parameter", parameterForLog)
												dataNode.addProperty("datapoints", dataListForLogFile?.toString())
												writeDataArray.add(dataNode)
											}
											if(!dataList.isEmpty()){
												float sum = 0.0
												for(int j = 0; j<dataList.size();j++ ){
													sum =  sum + dataList[j]
												}
												def avg = 0.0
												if(dataList.size() != 0){
													avg = sum / dataList.size()
												}
												avg = avg.round(2)

												String parameterForRest = target?.toString() + displayUnit
												dataMap.put("parameter", parameterForRest)
												dataMap.put("min",dataList.min())
												dataMap.put("max",dataList.max())
												dataMap.put("avg",avg)
												dataArrayList.add(dataMap)
												String processName = target?.split(host+".")[1]
												List processNameSplit = processName?.split("\\.")
												String processValueList = "min:"+dataList.min()+", max:"+dataList.max()+", avg:"+avg
												String thresholdVariable = ""
												
												def performanceInstanceForMin = new Performance()
												performanceInstanceForMin.executionResult = execResult
												performanceInstanceForMin.performanceType = GRAFANA_DATA
												if(isSystemMetric){
													performanceInstanceForMin.processName = "system " + processNameSplit[0]
													thresholdVariable = PROFILING_SYSTEM + processNameSplit[0] + PROFILING_THRESHOLD
												}else{
													if(target?.contains("exec-")){
														String processNameForExec = processNameSplit[0]
														processNameForExec = processNameForExec?.replace("exec-","processes-")
														performanceInstanceForMin.processName = processNameForExec
														thresholdVariable = PROFILING_PROCESSES + processNameForExec
													}else{
														performanceInstanceForMin.processName = processNameSplit[0]
														thresholdVariable = PROFILING_PROCESSES + processNameSplit[0]
													}
												}
												performanceInstanceForMin.processValue = processValueList
												String processType = ""
												if(target?.contains("exec-")){
													String processTypeInitial = processNameSplit[processNameSplit.size() - 1]
													processType = processTypeInitial?.split("-")[1]  
													processType = processType?.split("_")[1]  
												}else{
													if(processNameSplit.size() == 3){
														if(!processNameSplit[0]?.equals(processNameSplit[1])){
															processType = processNameSplit[1]+"." + processNameSplit[2] 
														}else{
															processType = processNameSplit[processNameSplit.size() - 1]
														}
													}else{
														processType = processNameSplit[processNameSplit.size() - 1]
													}
												}
												if(!isSystemMetric){
													thresholdVariable = thresholdVariable +UNDERSCORE + processType+ PROFILING_THRESHOLD
												}
												thresholdVariable = thresholdVariable?.replace("-","_")
												thresholdVariable = thresholdVariable?.replace(".","_")
												thresholdVariable = thresholdVariable?.toUpperCase()
												String finalConfigFile = ""
												File deviceConfigFile = new File( "${realPath}//fileStore//tdkvRDKServiceConfig//"+dev?.stbName+".config")
												File boxTypeConfigFile = new File( "${realPath}//fileStore//tdkvRDKServiceConfig//"+dev?.boxType?.name+".config")
												if(deviceConfigFile?.exists()){
													finalConfigFile = dev?.stbName+".config"
												}else if(boxTypeConfigFile?.exists()){
													finalConfigFile = dev?.boxType?.name+".config"
												}
												if(finalConfigFile != ""){
													String thresholdValue = getThresholdFromConfigFile(thresholdVariable,finalConfigFile)
													if(thresholdValue == null){
														thresholdValue = ""
													}
													performanceInstanceForMin.processValue1 = thresholdValue?.trim()
												}
												processType = processType + displayUnit
												performanceInstanceForMin.processType = processType
												performanceInstanceForMin.category = "RDKV"
												performanceInstanceForMin.save(flush:true)
				
											}
										}
									}
								}
								if(writeDataArray?.size() != 0){
									def execId = execResult?.execution?.id
									def execDeviceId = execResult?.executionDevice?.id
									String realPathForLogs = getRealPathForLogs()
									def logTransferFilePath = realPathForLogs + "/logs/"+execId+"/"+execDeviceId+"/"+execResult?.id
									new File(logTransferFilePath?.toString()).mkdirs()
									FileWriter file = new FileWriter(logTransferFilePath+"/"+execId+"_profilingData.json",true)
									BufferedWriter buffWriter = new BufferedWriter(file)
									for(int i = 0;i < writeDataArray?.size();i++){
										String dataValue = writeDataArray[i]
										buffWriter.write(dataValue+NEW_LINE);
										buffWriter.write(NEW_LINE);
									}
									buffWriter.flush()
									buffWriter.close()
									file.close();
								}
							}
						}
						input.close();
					}catch(Exception ex){
						ex.printStackTrace();
					}
				}
			}
		}
		render dataArrayList as JSON
	}
	
	/**
	 * Function to read grafana configurations from config file
	 * @param key
	 * @return
	 */
	def getGrafanaConfigurations(String key){
		File configFile = grailsApplication.parentContext.getResource("/fileStore/grafana.config").file
		Properties prop = new Properties();
		InputStream is
		try{
			if (configFile.exists()) {
				is = new FileInputStream(configFile);
				prop.load(is);
				String value = prop.getProperty(key);
				if (value != null && !value.isEmpty()) {
					return value;
				}
			}
		}catch(Exception e){
			e.printStackTrace()
		}finally{
			if(is){
				try{
					is.close()
				}catch(Exception e){
					e.printStackTrace()
				}
			}
		}
		return null;
	}
	
	/**
	 * Function to read threshold values from device config file for rdk profiling
	 * @param key
	 * @return
	 */
	def getThresholdFromConfigFile(String key, String fileName){
		File configFile = grailsApplication.parentContext.getResource("/fileStore/tdkvRDKServiceConfig/"+fileName).file
		Properties prop = new Properties();
		InputStream is
		try{
			if (configFile.exists()) {
				is = new FileInputStream(configFile);
				prop.load(is);
				String value = prop.getProperty(key);
				if (value != null && !value.isEmpty()) {
					return value;
				}
			}
		}catch(Exception e){
			e.printStackTrace()
		}finally{
			if(is){
				try{
					is.close()
				}catch(Exception e){
					e.printStackTrace()
				}
			}
		}
		return null;
	}
	
	/**
	 * Function to receive alert notification from Grafana
	 * @return
	 */
	def getAlertNotification(){
		try{
			String realPathForLogs = getRealPathForLogs()
			BufferedReader reader = new BufferedReader(new InputStreamReader(request.getInputStream()))
			String dataFromSocket = reader.readLine()
			reader.close()
			if(dataFromSocket != null && !dataFromSocket?.isEmpty()){			
				SimpleDateFormat formatForSystemTime = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
				String systemTime = formatForSystemTime.format(new Date())
				SimpleDateFormat formatForLogFile = new SimpleDateFormat("yyyy-MM-dd");
				String systemTimeForLogFile = formatForLogFile.format(new Date())
				JSONObject dataJsonObject = new JSONObject(dataFromSocket);
				if(dataJsonObject.has('state') && dataJsonObject.has('evalMatches')){
					def evalMatches = dataJsonObject.get('evalMatches')
					def state = dataJsonObject.get('state')
					def ruleId = dataJsonObject.get('ruleId')
					Map alertMapFromRest =  executionService.getAlertMapFromRest(realPath, ruleId)
					Double threshold = alertMapFromRest?.get('threshold')
					JSONObject evalMatchJson =  new JSONObject()
					String metric = ""
					if(state?.equals('alerting')){
						evalMatchJson = evalMatches[0]
						metric = evalMatchJson.get('metric')
					}else{
						metric = alertMapFromRest?.get('fullMetric')
					}
					if(metric != null && metric != ""){
						def metricList = metric?.split("\\.")
						if(metric?.contains("exec-")){
							String processName = metric?.substring(0,metric?.lastIndexOf("."));
							processName = processName?.replace("exec-","processes-")
							String lastMetricString = metric?.substring(metric?.lastIndexOf("_") + 1,metric?.length())
							metric = processName +"." +lastMetricString
						}
						Device dev =  Device.findBySerialNo(metricList[1])
						String finalConfigFile = ""
						File deviceConfigFile = new File( "${realPath}"+TDKV_RDKSERVICE_CONFIG_FOLDER_LOCATION+dev?.stbName+CONFIG_EXTN)
						File boxTypeConfigFile = new File( "${realPath}"+TDKV_RDKSERVICE_CONFIG_FOLDER_LOCATION+dev?.boxType?.name+CONFIG_EXTN)
						if(deviceConfigFile?.exists()){
							finalConfigFile = dev?.stbName+CONFIG_EXTN
						}else if(boxTypeConfigFile?.exists()){
							finalConfigFile = dev?.boxType?.name+CONFIG_EXTN
						}
						if(finalConfigFile == ""){
							finalConfigFile = "sample"+CONFIG_EXTN
						}
						if(finalConfigFile != ""){
							String unitVariable = metricList[2]
							String actualUnitVariable = RDKV_PROFILING_ACTUAL_UNIT 
							String preferredUnitVariable = RDKV_PROFILING_PREFERRED_UNIT 
							if(!unitVariable?.contains("-")){
								actualUnitVariable = actualUnitVariable + unitVariable?.toUpperCase()
								preferredUnitVariable = preferredUnitVariable + unitVariable?.toUpperCase()
							}else{
								if(unitVariable?.contains("exec-")){
									unitVariable = metricList[3]
									unitVariable = unitVariable?.substring(unitVariable?.lastIndexOf("_") + 1,unitVariable?.length())
									actualUnitVariable = actualUnitVariable + unitVariable?.toUpperCase()
									preferredUnitVariable = preferredUnitVariable + unitVariable?.toUpperCase()
								}else{
									unitVariable = metricList[3]
									actualUnitVariable = actualUnitVariable + unitVariable?.toUpperCase()
									preferredUnitVariable = preferredUnitVariable + unitVariable?.toUpperCase()
								}
							}
							String actualUnitValue = getThresholdFromConfigFile(actualUnitVariable,finalConfigFile)
							String preferredUnitValue = getThresholdFromConfigFile(preferredUnitVariable,finalConfigFile)
							if(actualUnitValue != null && preferredUnitValue != null){
								actualUnitValue = actualUnitValue?.trim()
								preferredUnitValue = preferredUnitValue?.trim()
								if(!actualUnitValue?.equals(preferredUnitValue)){
									int divideNumber =  1
									if((actualUnitValue?.equals("Bytes") && preferredUnitValue?.equals("MB"))){
										divideNumber = 1000000
									}else if((actualUnitValue?.equals("Bytes") && preferredUnitValue?.equals("KB"))){
										divideNumber = 1000
									}else if((actualUnitValue?.equals("KB") && preferredUnitValue?.equals("MB"))){
										divideNumber = 1000
									}
									if(state?.equals('alerting')){
										Double value = evalMatchJson.get('value')
										def result = value / divideNumber
										result = result.round(3)
										evalMatchJson.put('value',result)
									}
									if(divideNumber == 1){
										evalMatchJson.put('metric',metric)
									}else{
										evalMatchJson.put('metric',metric+ " " +LEFT_PARANTHESIS+preferredUnitValue+RIGHT_PARANTHESIS)
									}
									if(threshold != null){
										def thresholdAfterConversion = threshold / divideNumber
										thresholdAfterConversion = thresholdAfterConversion.round(3)
										dataJsonObject.put('threshold',thresholdAfterConversion)
									}
									if(state?.equals('ok') || state?.equals('no_data')){
										evalMatches.add(evalMatchJson)
									}
								}else{
									if(state?.equals('alerting')){
										Double value = evalMatchJson.get('value')
										value = value?.round(3)
										evalMatchJson.put('value',value)
									}
									evalMatchJson.put('metric',metric+ " " +LEFT_PARANTHESIS+preferredUnitValue+RIGHT_PARANTHESIS)
									if(threshold != null){
										threshold = threshold.round(3)
										dataJsonObject.put('threshold',threshold)
									}
									if(state?.equals('ok') || state?.equals('no_data')){
										evalMatches.add(evalMatchJson)
									}
								}
							}else{
								evalMatchJson.put('metric',metric)
								if(threshold != null){
									dataJsonObject.put('threshold',threshold)
								}
								if(state?.equals('ok') || state?.equals('no_data')){
									evalMatches.add(evalMatchJson)
								}
							}
						}
					}
				}				
				JSONObject jsonObj = new JSONObject();
				jsonObj.put("system_time",systemTime);
				jsonObj.put("alert_json",dataJsonObject);
				def logTransferFilePath = realPathForLogs + "/logs/grafanaAlerts"
				new File(logTransferFilePath?.toString()).mkdirs()
				FileWriter file = new FileWriter(logTransferFilePath+"/"+systemTimeForLogFile+"_alertData.json",true)
				BufferedWriter buffWriter = new BufferedWriter(file)
				buffWriter.write(jsonObj?.toString());
				buffWriter.write(NEW_LINE);
				buffWriter.flush()
				buffWriter.close()
				file.close();
			}
		}catch(Exception ex){
			ex.printStackTrace();
		}
		render "Received request in getAlertNotification"
	}
	
	/**
	 * Fetch the list of alerts received for a device between the timeframe
	 * @param fromDateString
	 * @param toDateString
	 * @param macAddress
	 * @return
	 */
	def fetchAlertDataForMemoryProfiling(String executionResultId){
		List alertList = []
		try{
			ExecutionResult execResult = ExecutionResult.findById(executionResultId)
			if(execResult){
				Date fromDate = execResult?.dateOfExecution
				Date toDate = new Date()
				def device = Device.findByStbName(execResult?.device)
				String macAddress = ""
				if(device){
					macAddress = device?.serialNo
				}
				alertList = executionService.fetchAlertData(fromDate,toDate,macAddress,realPath)
			}
			
		}catch(Exception ex){
			ex.printStackTrace();
		}
		render alertList as JSON
	}
	
	/**
	 * Function to fetch data from grafana using from and to dates
	 * @param executionResultId
	 * @param parameter
	 * @param fromDateString
	 * @param toDateString
	 * @return
	 */
	def fetchDataFromGrafanaMultiple(String executionResultId,String parameter, String fromDateString, String toDateString){
		List dataArrayList = []
		String basicUrl = getGrafanaConfigurations("grafanaUrl")
		String prefix = getGrafanaConfigurations("prefix")
		String datasourceId = getGrafanaConfigurations("datasourceId")
		def insecure = getGrafanaConfigurations("insecure")
		def curlTimeout = getGrafanaConfigurations("curlTimeOutInSeconds")
		if(basicUrl != null && prefix != null && datasourceId != null ){
			ExecutionResult execResult = ExecutionResult.findById(executionResultId)
			if(execResult){
				Device dev =  Device.findByStbName(execResult?.device?.toString())
				String macAddress = dev?.serialNo
				if(macAddress != null){
					try{
						if(macAddress?.contains(":")){
							macAddress = macAddress?.replace(":","")
						}
						if(macAddress?.contains("_")){
							macAddress = macAddress?.replace("_","")
						}
						macAddress = macAddress?.toUpperCase()
						DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
						Date fromDate = dateFormat.parse(fromDateString);
						Date toDate = dateFormat.parse(toDateString);
						
						long fromEpoch = fromDate?.getTime() / 1000;
						long toEpoch = toDate?.getTime() / 1000;
						String fromEpochTime = fromEpoch?.toString()
						String toEpochTime = toEpoch?.toString()
						
						
						String prefixLastChar = prefix?.charAt(prefix?.length()-1)
						if(!prefixLastChar?.equals(".")){
							prefix = prefix + "."
						}
						String host = prefix + macAddress
						String basicUrlLastChar = basicUrl?.charAt(basicUrl?.length()-1)
						if(!basicUrlLastChar?.equals("/")){
							basicUrl = basicUrl + "/"
						}
						basicUrl = basicUrl + "api/datasources/proxy/" + datasourceId +"/render?"
						List parameterList = []
						String targetString = ""
						parameterList = parameter?.split(",")
						parameterList?.each{ param ->
							targetString = targetString + "&target="+host+"."+param
						}
						
						String insecureString = ""
						def curlTimeoutString = "10"
						if(curlTimeout != null){
							curlTimeoutString = curlTimeout
						}
						if(insecure != null){
							if(insecure == "true"){
								insecureString = " --insecure"
							}
						}
						String url = basicUrl + "from="+fromEpochTime+"&until="+toEpochTime+""+targetString+"&format=json"
						String command = "curl" +insecureString+ " --connect-timeout "+ curlTimeoutString+ " \""+url+"\""
						ProcessBuilder pb;
						Process p;
						pb = new ProcessBuilder("bash", "-c", command);
						p = pb.start();
						String line;
						BufferedReader input = new BufferedReader(new InputStreamReader(p.getInputStream()));
						line = input.readLine();
						if((line != null) && (!line?.contains("message"))){
							line = line?.substring(1, line?.length() - 1);
							List dataArray = line?.split("},")
							if(dataArray?.size() != 0){
								for(int i = 0;i < dataArray?.size();i++){
									Map dataMap = [:]
									JsonObject dataNode = new JsonObject()
									List dataList = []
									String dataValue = dataArray[i]
									if(dataValue != null && !dataValue?.isEmpty()){
										String lastChar = dataValue?.charAt(dataValue?.length()-1)
										if(!lastChar?.equals("}")){
											dataValue = dataValue + "}"
										}
										JSONObject jsonObj = new JSONObject(dataValue);
										String target
										if(jsonObj.has('target')){
											target = jsonObj.get('target')
										}
										if(jsonObj.has('datapoints')){
											def metricList = target?.toString()?.split("\\.")
											String finalConfigFile = ""
											File deviceConfigFile = new File( "${realPath}"+TDKV_RDKSERVICE_CONFIG_FOLDER_LOCATION+dev?.stbName+CONFIG_EXTN)
											File boxTypeConfigFile = new File( "${realPath}"+TDKV_RDKSERVICE_CONFIG_FOLDER_LOCATION+dev?.boxType?.name+CONFIG_EXTN)
											if(deviceConfigFile?.exists()){
												finalConfigFile = dev?.stbName+CONFIG_EXTN
											}else if(boxTypeConfigFile?.exists()){
												finalConfigFile = dev?.boxType?.name+CONFIG_EXTN
											}
											if(finalConfigFile == ""){
												finalConfigFile = "sample"+CONFIG_EXTN
											}
											String actualUnit = ""
											String preferredUnit = ""
											if(finalConfigFile != ""){
												String unitVariable = metricList[2]
												String actualUnitVariable = RDKV_PROFILING_ACTUAL_UNIT
												String preferredUnitVariable = RDKV_PROFILING_PREFERRED_UNIT
												if(!unitVariable?.contains("-")){
													actualUnitVariable = actualUnitVariable + unitVariable?.toUpperCase()
													preferredUnitVariable = preferredUnitVariable + unitVariable?.toUpperCase()
												}else{
													if(unitVariable?.contains("exec-")){
														unitVariable = metricList[3]
														unitVariable = unitVariable?.substring(unitVariable?.lastIndexOf("_") + 1,unitVariable?.length())
														actualUnitVariable = actualUnitVariable + unitVariable?.toUpperCase()
														preferredUnitVariable = preferredUnitVariable + unitVariable?.toUpperCase()
													}else{
														unitVariable = metricList[3]
														actualUnitVariable = actualUnitVariable + unitVariable?.toUpperCase()
														preferredUnitVariable = preferredUnitVariable + unitVariable?.toUpperCase()
													}
												}
												actualUnit = getThresholdFromConfigFile(actualUnitVariable,finalConfigFile)
												preferredUnit = getThresholdFromConfigFile(preferredUnitVariable,finalConfigFile)
											}
											actualUnit = actualUnit?.trim()
											preferredUnit = preferredUnit?.trim()						
											boolean unitsSame = true
											if(!actualUnit?.equals(preferredUnit)){
												unitsSame = false
											}
											String displayUnit = ""
											if((preferredUnit != null) && (!preferredUnit?.equals("")) && (actualUnit != null) && (!actualUnit?.equals(""))){
												displayUnit = " ("+preferredUnit +")"
											}
											List datapoints = jsonObj.get('datapoints')
											datapoints.each{ dataPoint ->
												if(!(JSONObject.NULL?.equals(dataPoint[0]))){
													long epochTime = dataPoint[1]
													epochTime = epochTime * 1000
													SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
													def convertedTime = sdf.format(new Date(epochTime))
													float dataPointFloat = (float)dataPoint[0];
													if(unitsSame){
														dataPointFloat = dataPointFloat.round(3)
														dataList.add(dataPointFloat)
													}else{
														int divideNumber =  1
														if((actualUnit?.equals("Bytes") && preferredUnit?.equals("MB"))){
															divideNumber = 1000000
														}else if((actualUnit?.equals("Bytes") && preferredUnit?.equals("KB"))){
															divideNumber = 1000
														}else if((actualUnit?.equals("KB") && preferredUnit?.equals("MB"))){
															divideNumber = 1000
														}
														def result = dataPointFloat / divideNumber
														result = result.round(2)
														dataList.add(result)
													}
												}
											}
											if(!dataList.isEmpty()){
												float sum = 0.0
												for(int j = 0; j<dataList.size();j++ ){
													sum =  sum + dataList[j]
												}
												def avg = 0.0
												if(dataList.size() != 0){
													avg = sum / dataList.size()
												}
												avg = avg.round(2)

												String parameterForRest = target?.toString() + displayUnit
												dataMap.put("parameter", parameterForRest)
												dataMap.put("min",dataList.min())
												dataMap.put("max",dataList.max())
												dataMap.put("avg",avg)
												dataArrayList.add(dataMap)
											}
										}
									}
								}
							}
						}
						input.close();
					}catch(Exception ex){
						ex.printStackTrace();
					}
				}
			}
		}
		render dataArrayList as JSON
	}
	
	/**
	 * Function to show SVG file contents
	 * @return
	 */
	def showSVGContents(){
		def consoleFileData = ""
		String logPath = "..//logs//${params?.execId}//${params?.execDeviceId}//${params?.execResultId}//"+params?.fileName
		render(template: "profilingDetails", model: [svgDetails:true,logPath:logPath])
	}
	
	/**
	 * Method that returns the path to logs folder	
	 * @return
	 */
	def String getRealPathForLogs(){
		String returnValue = request.getSession().getServletContext().getRealPath(Constants.FILE_SEPARATOR)
		File configFile = grailsApplication.parentContext.getResource(Constants.TM_CONFIG_FILE).file
		String logsLocation= Constants.NO_LOCATION_SPECIFIED
		logsLocation = executionService.getConfigProperty(configFile,Constants.LOGS_PATH)
		if(logsLocation != null){
			File logsLocationTestDirectory = new File(logsLocation)
			if(logsLocationTestDirectory?.isDirectory()){
				String logsLocationLastChar = logsLocation?.charAt(logsLocation?.length()-1)
				if(!logsLocationLastChar?.equals(Constants.URL_SEPERATOR)){
					logsLocation = logsLocation + Constants.URL_SEPERATOR
				}
				returnValue = logsLocation
			}
		}
		return returnValue
	}
	
	/**
	 * Function to create and write into file
	 * @param execId
	 * @param execDevId
	 * @param resultId
	 * @param test
	 * @return
	 */
	def createFileAndWrite(final Integer execId ,final Integer execDevId,final Integer resultId,final String test){
		JsonObject result = new JsonObject()
		BufferedReader reader
		if(execId!=null && execDevId!=null && resultId!=null){
			try{

				String realPathForLogs = getRealPathForLogs()
				def versionFilePath = realPathForLogs + "logs/logs/${execId}"
				String fileName  = versionFilePath+"/"+execId+"_"+execDevId+"_"+resultId+"_mvs_applog.txt"
				def file = new File( fileName)
				if (!file.getParentFile().exists())
					file.getParentFile().mkdirs();
				if (!file.exists()){
					file.createNewFile();

					file.append(System.getProperty("line.separator")+test);

					result.addProperty("Status", "SUCCESS")
					result.addProperty("Remarks", "Created file Name: "+fileName)

				}else if(file.exists()){
					reader = new BufferedReader(new FileReader(file));
					String line = reader?.readLine();
					while(line != null){
						line = reader?.readLine()
					}
					file.append(System.getProperty("line.separator")+test);

					result.addProperty("Status", "SUCCESS")
					result.addProperty("Remarks", "Updated Existing file: "+fileName)

				}

				else{

					result.addProperty("Status", "FAILURE")
					result.addProperty("Remarks", "Unable to create file: "+fileName)

				}

			}catch (Exception e) {
				e.printStackTrace()
			}
		}
		else{
			result.addProperty("Status", "FAILURE")
			result.addProperty("Remarks", "Unable to create a file execId and resultId empty")
		}
		render result
	}
}
