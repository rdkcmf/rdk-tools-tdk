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

import java.util.List;
import java.util.zip.ZipOutputStream

import com.google.gson.JsonArray;
import com.google.gson.JsonObject
import grails.converters.JSON
import groovy.xml.MarkupBuilder
import org.springframework.dao.DataIntegrityViolationException
import org.springframework.util.StringUtils;
import org.apache.shiro.SecurityUtils
import com.comcast.rdk.Category

/**
 * Class to create Modules, Functions and Parameters
 * @author sreejasuma
 *
 */

class ModuleController {

	def utilityService
	def moduleService
	def logZipService
	
	def rootPath = null
	static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

	def index() {
		redirect(action: "list", params: params)
	}
	
	/**
	 * List modules
	 * @param max
	 * @return
	 */
	def list(Integer max) {
		params.max = Math.min(max ?: 10, 100)
		def groupsInstance = utilityService.getGroup()
		def category = getCategory(params?.category)
	
		def moduleInstanceList = getModuleList(groupsInstance, params)
		def moduleInstanceListCnt = getModuleCount(groupsInstance, category)
		[moduleInstanceList: moduleInstanceList, moduleInstanceTotal: moduleInstanceListCnt, category:params?.category]
	}

	def crashlog(){
		//def moduleInstanceList = Module.findAllByGroupsOrGroupsIsNull(utilityService.getGroup(), [order: 'asc', sort: 'name'])
		def moduleInstanceList = getModuleList(utilityService.getGroup(), params)
		[moduleInstanceList: moduleInstanceList, category : params?.category]
	}
	
	/**
	 * Method to get the file list based on module
	 * @param max
	 * @return
	 */
	def getFileList(){
		Module module = Module.findById(params?.moduleid)
		render(template:"crashfilelist", model:[ crashfiles : module?.logFileNames])
	}
	
	def saveCrashLogs(){
		List lst = []
		if(params?.logFileNames){
			if((params?.logFileNames) instanceof String){
				lst.add(params?.logFileNames)
			}
			else{
				(params?.logFileNames).each{ logfilename ->
					if(StringUtils.hasText(logfilename)){
						lst.add(logfilename)
					}
				}
			}
			Module module = Module.findById(params?.module.id)
			module.logFileNames = lst
			if(module.save(flush:true)){
				flash.message = "Updated Log Files to the Module "+module?.name
			}
			else{
				flash.message = "Error in saving. Please retry "
			}
		}
		redirect(action: "crashlog", params:[category:params?.category])
	}
	/**
	 * Function transfer the moduleList to the view page
	 *
	 */
	def logFileNames(){
		def moduleInstanceList = getModuleList(utilityService.getGroup(), params)
		[moduleInstanceList: moduleInstanceList, category: params?.category]
	}

	/**
	 *The Function transfer the stbLogFiles in view page configureStbLogs
	 * @return
	 */
	def getLogList(){
		Module module = Module.findById(params?.moduleid)
		render(template:"configureStbLogs", model:[ stbLogFiles : module?.stbLogFiles])
	}
	
	/**
	 * The function used to save the current StbLogFiles in database
	 * @return
	 */
	
	def saveLogsFiles(){
		List lst = []
		if(params?.stbLogFiles){
			if((params?.stbLogFiles) instanceof String){
				lst.add(params?.stbLogFiles)
			}
			else{
				params?.stbLogFiles.each{ stblogfilename ->
					if(StringUtils.hasText(stblogfilename)){
						lst.add(stblogfilename)
					}
				}
			}
			Module module = Module.findById(params?.module.id)
			module.stbLogFiles = lst
			if(module.save(flush:true)){
				flash.message = "Updated Log Files to the Module "+module?.name
			}
			else{
				flash.message = "Error in saving. Please retry "
			}
		}
		redirect(action: "logFileNames", params:[category: params?.category])
	}
	
	
	
	
	
	
	
	def configuration() {
		// Redirect to show page without any parameters
	}
	
	def setExecutionWaitTime(final int executiontime, final String moduleName){
//		def c = Script.createCriteria()
//		def scriptList = c.list {
//			primitiveTest{
//				module{
//					eq("name", moduleName)
//				}
//			}
//		}
//		scriptList.each{script ->
//			script.executionTime = executiontime
//			script.save(flush:true)
//		}
	}
	
	/**
	 * Create Module, Function and parameter types
	 * @return
	 */
	def create() {
		def modules = getModuleList(utilityService.getGroup(), params)
		[moduleInstance: new Module(params), functionInstance : new Function(params), parameterTypeInstance : new ParameterType(params),category:params?.category, modules:modules]
	}
	
	/**
	 * create  function
	 */
	def createFunction(){
		def modules = getModuleList(utilityService.getGroup(), params)
		[  moduleInstance: new Module(params),functionInstance : new Function(params), category:params?.category , modules:modules]
		
		
	}
	/**
	 * Create parameters
	 */
	def createParameter(){
		def modules = getModuleList(utilityService.getGroup(), params)
		[parameterTypeInstance  : new ParameterType(params),  category:params?.category , modules:modules]
		
	}
	def save() {
		  /*   def moduleInstance = new Module(params)
		moduleInstance.groups = utilityService.getGroup()
		Category category = getCategory(params?.category)
		def savedEntity = true
		def createdFile = true
		Module.withTransaction { status ->
			if (!moduleInstance.save(flush: true)) {
				savedEntity = false
			}
			if(savedEntity){
				def created = moduleService.createModule(moduleInstance, getRootPath(), category, params?.testGroup)
				if(!created){
					status.setRollbackOnly()
					createdFile = false
				}
			}
		}
		setExecutionWaitTime(moduleInstance.executionTime, moduleInstance.name)
		if(!savedEntity){
			def map = create()
			map.put('moduleInstance', moduleInstance)
			render(view: "create", model: map)
			return
		}
		if(!createdFile){
			flash.message =  "Failed to save ${moduleInstance}. Error occured while creating primitivetest for ${moduleInstance} in fileStore."
			render(view: "create", model: [category: params?.category])
			return
		}
		flash.message = message(code: 'default.created.message', args: [message(code: 'module.label', default: 'Module'), moduleInstance.name])
		redirect(action: "create",  params:[category:params?.category])*/
		def module  = Module?.findByName(params.name)
		if(module){
			flash.message ="${params?.name} module name is alredy exist "
		}else{
			def moduleInstance = new Module(params)
			moduleInstance.groups = utilityService.getGroup()
			if (!moduleInstance.save(flush: true)) {
				flash.message = message(code: 'default.not.created.message', args: [message(code: 'module.label', default: 'Module'), moduleInstance.name])
			}else{
				flash.message = message(code: 'default.created.message', args: [message(code: 'module.label', default: 'Module'), moduleInstance.name])
			}
		}
		redirect(action: "create", params:[category:params?.category])
	}
	/**
	 * Save function corresponding to the selected modules
	 * @return
	 */
	def saveFunction() {/*
		Function.withTransaction { status ->
			def functionInstance = new Function(params)
			if (!functionInstance.save(flush: true)) {
				def map = create()
				map.put('functionInstance', functionInstance)
				render(view: "create", model: map)
				return
			}
			try{
				moduleService.addFunction(params, getRootPath(), getCategory(params?.category))
				flash.message = message(code: 'default.created.message', args: [message(code: 'function.label', default: 'Function'), functionInstance.name])
			}
			catch(Exception e){
				status.setRollbackOnly()
				e.printStackTrace()
				flash.message = message(code: 'default.not.created.message', args: [message(code: 'function.label', default: 'Function'), functionInstance.name])
			}
		}
		redirect(action: "create", params:[category:params?.category])
	*/
	def functionInstance = new Function(params)
	Function.withTransaction { status ->
		try{
			if (!functionInstance.save(flush: true)) {
				flash.message = message(code: 'default.not.created.message', args: [message(code: 'function.label', default: 'Function'), functionInstance.name])
				return
			}else{
			flash.message = message(code: 'default.created.message', args: [message(code: 'function.label', default: 'Function'), functionInstance.name])
			}
		}
		catch(Exception e){
			status.setRollbackOnly()
			e.printStackTrace()
			flash.message = message(code: 'default.not.created.message', args: [message(code: 'function.label', default: 'Function'), functionInstance.name])
		}
	}
	redirect(action: "createFunction", params:[category:params?.category])
	}
	
	/**
	 * Save parameter corresponding to the selected modules
	 * and functions
	 * @return
	 */
	def saveParameter() {/*
		ParameterType.withTransaction{ status ->
			def parameterTypeInstance = new ParameterType(params)
			if (!parameterTypeInstance.save(flush: true)) {
				def map = create()
				map.put('parameterTypeInstance', parameterTypeInstance)
				render(view: "create", model:map)
				return
			}
			def result = moduleService.addParameter(params, getRootPath(), getCategory(params?.category))
			if(result.success){
				flash.message = message(code: 'default.created.message', args: [message(code: 'parameterType.label', default: 'ParameterType'), parameterTypeInstance.name])
			}
			else{
				flash.error = result.message
				status.setRollbackOnly()
			}
		}
		redirect(action: "create", params:[category:params?.category])
	*/
			try{
				def parameterTypeInstance = new ParameterType(params)
				if (!parameterTypeInstance.save(flush: true)) {
					flash.message = message(code: 'default.not.created.message', args: [message(code: 'parameterType.label', default: 'ParameterType'), parameterTypeInstance.name])
				render(view: "create", model:['parameterTypeInstance': parameterTypeInstance, category: params?.category])
					return
				}else{
				flash.message = message(code: 'default.created.message', args: [message(code: 'parameterType.label', default: 'ParameterType'), parameterTypeInstance.name])
				}
			}catch(Exception e){
				e.printStackTrace()
				println "ERROR "+e.getMessage()
			}
		redirect(action: "createParameter", params:[category:params?.category])
		}
	def updateTimeOut(){
		try{
			Module moduleInstance = Module.findById(params?.moduleId)
			moduleInstance.executionTime = Integer.parseInt(params?.timeout)
			if(moduleInstance.save(flush:true)){
				setExecutionWaitTime(moduleInstance.executionTime, moduleInstance.name)
				render "Updated TimeOut"
			}
			else{
				render "TimeOut not updated. Try Again!!"
			}
		}catch(Exception e){
		}
	}
	

	/**
	 * Show Modules, Functions and Parameters
	 * @param id
	 * @return
	 */
	def show(Long id) {
		def moduleInstance = Module.get(id)
		def functionInstance
		def parameterInstance
		def parameteInstanceList = []
		if (!moduleInstance) {
			flash.message = message(code: 'default.not.found.message', args: [message(code: 'module.label', default: 'Module'), id])
			redirect(action: "list")
			return
		}
		else{
			functionInstance = Function.findAllByModule( moduleInstance )
			def parameterTypeTnstance
			functionInstance.each{ fn ->
				parameterInstance = ParameterType.findAllByFunction(fn)
				parameterInstance.each{ parameter ->
					parameterTypeTnstance = ParameterType.get( parameter.id )
					parameteInstanceList.add(parameterTypeTnstance)
				}
			}
		}
		[params : params , moduleInstance : moduleInstance, functionInstanceList : functionInstance, functionInstanceCount : functionInstance.size(), parameteInstanceList : parameteInstanceList, parameteInstanceListTotal : parameteInstanceList.size(), category:moduleInstance?.category]
	}


	/**
	 * TODO : If required
	 * @param id
	 * @return
	 */
	def edit(Long id) {
		def moduleInstance = Module.get(id)
		if (!moduleInstance) {
			flash.message = message(code: 'default.not.found.message', args: [message(code: 'module.label', default: 'Module'), id])
			redirect(action: "list")
			return
		}

		[moduleInstance: moduleInstance]
	}

	/**
	 * TODO : If required
	 * @param id
	 * @return
	 */
	def update(Long id, Long version) {
		def moduleInstance = Module.get(id)
		if (!moduleInstance) {
			flash.message = message(code: 'default.not.found.message', args: [message(code: 'module.label', default: 'Module'), id])
			redirect(action: "list")
			return
		}

		if (version != null) {
			if (moduleInstance.version > version) {
				moduleInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
						  [message(code: 'module.label', default: 'Module')] as Object[],
						  "Another user has updated this Module while you were editing")
				render(view: "edit", model: [moduleInstance: moduleInstance])
				return
			}
		}

		moduleInstance.properties = params

		if (!moduleInstance.save(flush: true)) {
			render(view: "edit", model: [moduleInstance: moduleInstance])
			return
		}

		flash.message = message(code: 'default.updated.message', args: [message(code: 'module.label', default: 'Module'), moduleInstance.name])
		redirect(action: "show", id: moduleInstance.id)
	}

	/**
	 * Deletes the module and the corresponding
	 * functions and parameters
	 * @param id
	 * @return
	 */
	def delete(Long id) {
		def moduleInstance = Module.get(id)
		if (!moduleInstance) {
			flash.message = message(code: 'default.not.found.message', args: [message(code: 'module.label', default: 'Module'),  moduleInstance.name])
			redirect(action: "list")
			return
		}
		try {
			def path=request.getSession().getServletContext().getRealPath("")
			moduleService.deleteFunctionandParameters(moduleInstance, getCategory(params?.category), path)
			
					   
			moduleInstance.delete(flush: true)
			flash.message = message(code: 'default.deleted.message', args: [message(code: 'module.label', default: 'Module'),  moduleInstance.name])
			redirect(action: "list", params:[category:params?.category])
		}
		catch (DataIntegrityViolationException e) {
			flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'module.label', default: 'Module'),  moduleInstance.name])
			redirect(action: "show", id: id, params:[category:params?.category])
		}
	}
	
   
	
	/**
	 * Deletes the selected function/s
	 */
	def deleteFunction = {
		Function functionInstance
		def unDeletedList = []
		def fnList = []
		def selectedFunctions = params.findAll { it.value == KEY_ON }
		try{
			selectedFunctions.each{
				def key = it.key
				try {
					Function.withTransaction { resultstatus ->
						functionInstance = Function.findById(key)
						fnList.add(functionInstance?.name)
						try{
							if(!functionInstance.delete(flush:true)){
								if(functionInstance?.errors?.allErrors?.size() > 0){
									unDeletedList.add(functionInstance?.name)
								}
							}
						}
						catch (org.springframework.dao.DataIntegrityViolationException e) {
							unDeletedList.add(functionInstance?.name)
							
						}
						resultstatus.flush()
					}
				} catch (Exception e) {
					unDeletedList.add(functionInstance?.name)
				}
			}
			flash.message = "Function/s deleted"
		}
		catch (Exception e) {
			log.trace e.printStackTrace()
			flash.message = "${message(code: 'default.not.deleted.message', args: [message(code: 'function.label', default: 'Function'), unDeletedList.toString() ])}"
 		}
		if(unDeletedList.size() > 0){
			flash.message = "${message(code: 'default.not.deleted.message', args: [message(code: 'function.label', default: 'Function'), unDeletedList.toString() ])}"
		}
	//	fnList.removeAll(unDeletedList)
	//	if(!fnList.isEmpty()){
	//		moduleService.removeFunction(params, getRootPath(), getCategory(params?.category), fnList)
	//	}
		redirect(action: "show", id : params?.moduleid, params:[category:params?.category])
	} 

	/**
	 * Deletes the selected parameter/s
	 */
	def deleteParameterType = {
		def parameterTypeInstance
		def unDeletedList = []
		def paramsList = []
		def selectedParameters = params.findAll { it.value == KEY_ON }
		try{
			selectedParameters.each{
				def key = it.key
				try {
					ParameterType.withTransaction { resultstatus ->
						parameterTypeInstance = ParameterType.findById(key)
						paramsList.add(parameterTypeInstance?.name)
						try{
							if(!parameterTypeInstance.delete(flush:true)){
								if(parameterTypeInstance?.errors?.allErrors?.size() > 0){
									unDeletedList.add(parameterTypeInstance?.name)
								}
							}
						}
						catch (org.springframework.dao.DataIntegrityViolationException e) {
							unDeletedList.add(parameterTypeInstance?.name)
						}
						resultstatus.flush()
					}
				} catch (Exception e) {
					unDeletedList.add(parameterTypeInstance?.name)
				}
			}
			flash.message = "Parameter/s deleted"
		}

		catch (Exception e) {
			flash.message = "${message(code: 'default.not.deleted.message', args: [message(code: 'parameter.label', default: 'Parameter'), parameterTypeInstance?.name])}"
		}
		//paramsList.removeAll(unDeletedList)
		if(unDeletedList.size() > 0){
			flash.message = "${message(code: 'default.not.deleted.message', args: [message(code: 'parameter.label', default: 'Parameter'), unDeletedList.toString() ])}"
		}
	//	if(!paramsList.isEmpty()){
	//		moduleService.removeParameters(params, getRootPath(),getCategory(params?.category), paramsList)
	//	}
		redirect(action: "show", id : params?.moduleid, params:[category:params?.category])
	}		
	
	/**
	 * Get the functions under the specific modules
	 * @return
	 */
	def getFunctions() {
		if(! params.moduleId) {
			render "No module id found"
			return
		}
		
		def module = Module.get(params.moduleId as Long)
		
		if(! module) {
			render "No module found with id : ${params.moduleId}"
			return
		}
		
		def functions = Function.findAllByModule(module)
		render functions as JSON
	}
	
	/**
	 * REST method to get the time out values configured for  modules
	 * @param moduleName
	 * @return
	 */
	def getModuleScriptTimeOut(final String moduleName) {
		JsonObject moduleObj = new JsonObject()
		if(moduleName){
			try{
				def moduleInstance= Module.findByName(moduleName)
				if(moduleInstance){
					moduleObj.addProperty("module",moduleInstance?.name?.toString())
					moduleObj.addProperty("timeout",moduleInstance?.executionTime)
				}else{
					moduleObj.addProperty("status", "failure")
					moduleObj.addProperty("remarks", "invalid module name ")
				}
			}
			catch(Exception e){
				println e.getMessage()
				log.error("Invalid module name ")
			}
		}else{
			def mList = Module.findAll()
			JsonArray mArray = new JsonArray()
			mList?.each { module ->
				JsonObject mObject = new JsonObject()
				mObject.addProperty("module",module?.name?.toString())
				mObject.addProperty("timeout",module?.executionTime)
				mArray.add(mObject)
			}
			moduleObj.add("timeoutlist", mArray)
		}

		render moduleObj
	}
	
	private List getModuleList(def groups, def params){
		return  Module.createCriteria().list(max:params.max, offset:params.offset ){
			or{
				isNull("groups")
				if(groups != null){
					eq("groups",groups)
				}
			}
			and{
				eq("category", Utility.getCategory(params?.category))
				
			}
			order params.sort?params.sort:'name', params.order?params.order:'asc'
		}
	}
	
	private int getModuleCount(def groups, def category){
		return  Module.createCriteria().count{
			or{
				isNull("groups")
				if(groups != null){
					eq("groups",groups)
				}
			}
			and{
				eq("category", category)
			}
		}
	}
	private Category getCategory(def category){
		return Category.valueOf(category)
	}
	
	private String getRootPath(){
		return request.getSession().getServletContext().getRealPath(Constants.FILE_SEPARATOR)
	}
	
	
	/**
	 * Function for download module details as XML with selected functions
	 * @return
	 */
	
	def downloadSelectedXml(){
		Function functionInstance 
		def unDeletedList = []
		def functions = []
		def selectedFunctions = params.findAll { it.value == KEY_ON }
		
		try{
			selectedFunctions.each{
				def key = it.key
				try {
					Function.withTransaction { resultstatus ->
						functionInstance = Function.findById(key)
						functions.add(functionInstance)
						
						resultstatus.flush()
					}
				} catch (Exception e) {
					
				}
			}
		
		}
		catch (Exception e) {
			log.trace e.printStackTrace()
			
		}
		def moduleName  = Module?.findById(params?.id)
		String moduleData = ""
		def writer = new StringWriter()
		def xml = new MarkupBuilder(writer)
		if(moduleName){
			try{
				xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
				xml.xml(){
				xml.module(){
					mkp.yield "\r\n  "
					mkp.comment "Module Name "
					xml.moduleName(moduleName)
					mkp.yield "\r\n  "
					mkp.comment "Category of the module "
					xml.category(params.category)
					mkp.yield "\r\n  "
					mkp.comment "Excecution time out of module"
					xml.executionTimeOut(moduleName?.executionTime)
					mkp.yield "\r\n  "
					mkp.comment "Excecution time out of module"
					xml.testGroup(moduleName?.testGroup)
					mkp.yield "\r\n  "
					mkp.comment "Logs File Names of module"
					xml.logFileNames(moduleName?.stbLogFiles)
					mkp.yield "\r\n  "
					mkp.comment "Crash File Names of the module"
					xml.crashFileNames(moduleName?.logFileNames)
					if(functions){
						mkp.yield "\r\n  "
						mkp.comment "Total functions corresponding module "
						xml.functions(){
							functions?.each{ funName ->
								xml.function(name:funName?.toString())
							}
						}
						mkp.yield "\r\n  "
						mkp.comment "Total parameters corresponding module "
						xml.parameters(){
							functions?.each{ funName ->
								def parameterInstance =  ParameterType?.findAllByFunction(funName)
								if(parameterInstance){
									parameterInstance?.each{ parameterName->
										xml.parameter(funName:funName,parameterName:parameterName,parameterType:parameterName?.parameterTypeEnum ,range:parameterName?.rangeVal)
									}
								}
							}
						}
					}
				}
			}
			moduleData = writer?.toString()
			}catch(Exception e){
				println " ERROR "+ e.printStackTrace()
			}
			if(moduleData){
				params.format = "text"
				params.extension = "xml"
				response.setHeader("Content-Type", "application/octet-stream;")
				response.setHeader("Content-Disposition", "attachment; filename=\""+ moduleName?.toString()+"-module.xml\"")
				response.outputStream << moduleData.getBytes()
			}else{
				flash.message = "Download failed as XML file was not created.Try again."
				redirect(action: "show")
			}
		}else{
			flash.message ="Module does not exist"
			redirect(action:"show")
		}
	}
	
	/**
	 * Function for download all module details as XML as zip
	 * @return
	 */
	def downloadAllModule(){
		String category = params?.category
		try {
			def moduleList = Module.findAllByCategory(category)
			if(moduleList?.size() > 0){
				ZipOutputStream zos = new ZipOutputStream(response.outputStream);
				params.format = EXPORT_ZIP_FORMAT
				params.extension = EXPORT_ZIP_EXTENSION
				response.contentType = grailsApplication.config.grails.mime.types[params.format]
				response.setHeader("Content-Type", "application/zip")
				response.setHeader("Content-disposition", "attachment; filename=ModuleXMLs_"+ category +".${params.extension}")
				moduleList?.each{ moduleObj ->
					def moduleXmlData = getModuleXMLData(moduleObj, category)
					logZipService.writeZipEntry(moduleXmlData , "${moduleObj?.name}.xml" , zos)
				}
				zos.closeEntry();
				zos.close();
			}else{
				flash.message ="Modules do not exist"
				redirect(action:"show")
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	/**
	 * Function for download module details as XML
	 * @return
	 */
	def downloadXml(){
		def moduleObj  = Module?.findById(params?.id)
		String moduleData = ""
		def writer = new StringWriter()
		def xml = new MarkupBuilder(writer)
		if(moduleObj){
			try{
				moduleData = getModuleXMLData(moduleObj,params?.category)
			}catch(Exception e){
				println " ERROR "+ e.printStackTrace()
			}
			if(moduleData){
				params.format = "text"
				params.extension = "xml"
				response.setHeader("Content-Type", "application/octet-stream;")
				response.setHeader("Content-Disposition", "attachment; filename=\""+ moduleObj?.toString()+"-module.xml\"")
				response.outputStream << moduleData.getBytes()
			}else{
				flash.message = "Download failed due to module information not available."
				redirect(action: "show")
			}
		}else{
			flash.message ="Module does not exist"
			redirect(action:"show")
		}
	}
	
	/**
	 * Function to fetch the module details in XML format
	 * @return
	 */
	def getModuleXMLData(def moduleObj , def category){
		String moduleData = ""
		def writer = new StringWriter()
		def xml = new MarkupBuilder(writer)
		try{
			xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
			xml.xml(){
			xml.module(){
				mkp.yield "\r\n  "
				mkp.comment "Module Name "
				xml.moduleName(moduleObj?.name)
				mkp.yield "\r\n  "
				mkp.comment "Category of the module "
				xml.category(category)
				mkp.yield "\r\n  "
				mkp.comment "Excecution time out of module"
				xml.executionTimeOut(moduleObj?.executionTime)
				mkp.yield "\r\n  "
				mkp.comment "Excecution time out of module"
				xml.testGroup(moduleObj?.testGroup)
				mkp.yield "\r\n  "
				mkp.comment "Logs File Names of module"
				xml.logFileNames(moduleObj?.stbLogFiles)
				mkp.yield "\r\n  "
				mkp.comment "Crash File Names of the module"
				xml.crashFileNames(moduleObj?.logFileNames)
				def functions = Function.findAllByModuleAndCategory(moduleObj,category)
				if(functions){
					mkp.yield "\r\n  "
					mkp.comment "Total functions corresponding module "
					xml.functions(){
						functions?.each{ funName ->
							xml.function(name:funName?.toString())
						}
					}
					mkp.yield "\r\n  "
					mkp.comment "Total parameters corresponding module "
					xml.parameters(){
						functions?.each{ funName ->
							def parameterInstance =  ParameterType?.findAllByFunction(funName)
							if(parameterInstance){
								parameterInstance?.each{ parameterName->
									xml.parameter(funName:funName,parameterName:parameterName,parameterType:parameterName?.parameterTypeEnum ,range:parameterName?.rangeVal)
								}
							}
						}
					}
				}
			}
		}
		moduleData = writer?.toString()
		}catch(Exception e){
			println " ERROR "+ e.printStackTrace()
		}
		return moduleData
	}


	/**
	 * Function for uploading the module details
	 * @return
	 */
	def uploadModule(){
			def category
			def uploadedFile = request?.getFile("file")
			if( uploadedFile?.originalFilename?.endsWith(".xml")) {
				InputStreamReader reader = new InputStreamReader(uploadedFile?.getInputStream())
				def fileContent = reader?.readLines()
				if(fileContent){
					def moduleName
					def executionTimeOut
					def testGroup
					String moduleXmlContent = ""
					def logFileNames
					def crashFileName
					List crashFile = []
					List logFile =[]
					def node
					def parameters
					def functions
					fileContent?.each{ xmlData->
						moduleXmlContent += xmlData +"\n"
					}
					boolean moduleSaveStatus  = true
					try{
						XmlParser parser = new XmlParser();
						node = parser.parseText(moduleXmlContent)
						if(node){
							moduleName = node?.module?.moduleName?.text()?.trim()
							category = node?.module?.category?.text()?.trim()
							executionTimeOut  = node?.module?.executionTimeOut?.text()?.trim()
							testGroup =  node?.module?.testGroup?.text()?.trim()
							def testGrpStatus = com.comcast.rdk.TestGroup?.values()?.toString()?.contains(testGroup)
							logFileNames = node?.module?.logFileNames?.text()?.trim()
							crashFileName = node?.module?.crashFileNames?.text()?.trim()
							if(!moduleName){
								flash.message = "Module name is blank"
							}else if(!category){
								flash.message = "Category is blank"
							}else if(!(category?.toString()?.equals(params?.category?.toString()))){
								flash.message =  " The category not matching with accoding the user  "+params?.category
							}else if(!(executionTimeOut.toString().isInteger())){
								flash.message = "Excecution time out is not valid"
							}else if(!testGroup){
								flash.message =	"The test group is blank "
							}else if(testGrpStatus?.toString()?.equals("false")){
								flash.message =	"The test group value is invalid "
							}else{
								 int newExcutionTimeOut =Integer?.parseInt(node?.module?.executionTimeOut?.text()?.trim())
								if(logFileNames){
									logFileNames = logFileNames?.toString()?.replace("[", "")
									logFileNames = logFileNames?.toString()?.replace("]", "")
									def	logFileNamesList = logFileNames?.split(",")
									logFileNamesList?.each{
										logFile?.add(it)
									}
								}
								if(crashFileName){
									crashFileName = crashFileName?.toString()?.replace("[", "")
									crashFileName = crashFileName?.toString()?.replace("]", "")
									def	crashFileNamesList = crashFileName?.split(",")
									crashFileNamesList?.each{
										crashFile?.add(it)
									}
								}
								functions = []
								def parameterTotalList = []
								node?.module?.functions?.function?.each{
									functions?.add(it?.@name)
								}
								def parameterList = [:]
								node?.module?.parameters?.parameter?.each{
									parameterList = [:]
									parameterList?.put("funName",it?.@funName)
									parameterList?.put("paramsName",it?.@parameterName)
									parameterList?.put("parameterType",it?.@parameterType)
									parameterList?.put("paramRange",it?.@range)
									parameterTotalList.add(parameterList)
								}
								def moduleInstance =  Module?.findByName(moduleName)
								if(!moduleInstance){
									Module newModuleInstance = new Module()
									newModuleInstance?.name = moduleName
									newModuleInstance?.category = category
									newModuleInstance?.executionTime = newExcutionTimeOut
									newModuleInstance?.testGroup = testGroup
									newModuleInstance?.logFileNames = crashFile
									newModuleInstance?.stbLogFiles = logFile
									newModuleInstance.groups = utilityService.getGroup()
									if(newModuleInstance?.save(flush:true)){
										moduleSaveStatus = true
									}else{
										moduleSaveStatus = false
									}
								}
								if(moduleSaveStatus){
									def newFunList = []
									def moduleInstance1 =  Module?.findByName(moduleName)
									if(functions)	{
										functions?.each { funName->
											if(!(Function?.findByNameAndModule(funName,moduleInstance1))){
												newFunList.add(funName)
											}
										}
										try{
											newFunList?.each { newFunName ->
												def functionInstance  = new Function()
												functionInstance?.name = newFunName
												functionInstance?.module = moduleInstance1
												functionInstance?.category =  category?.toString()
												if(functionInstance?.save(flush:true)){
												}
											}
										}catch(Exception e){
											println " Error "+ e.getMessage()
											e.printStackTrace()
										}
									}
									if(parameterTotalList){
										parameterTotalList?.each{ parameter ->
											def functionInstance = Function?.findByNameAndModule(parameter?.funName, moduleInstance1)
											if(functionInstance){
												if(!(ParameterType?.findByNameAndFunction(parameter?.paramsName?.toString(),functionInstance ))){
													try{
														def parameterInstance = new ParameterType()
														parameterInstance.name = parameter?.paramsName
														parameterInstance.parameterTypeEnum = parameter?.parameterType
														parameterInstance?.rangeVal = parameter?.paramRange
														parameterInstance?.function = functionInstance
														if(parameterInstance?.save(flush:true)){
														}
													}catch(Exception e){
														e.printStackTrace()
													}
												}else{
												}
											}
										}
									}
									flash.message ="Module details uploaded successfully "
								}else{
									flash.message =" Module details not saved"
								}
							}
						}
					}catch (Exception e){
						flash.message ="XML tags not in correct format "
						println e.printStackTrace()
					}
				}else{
					flash.message ="File content is empty"
				}
			}else{
				flash.message="Error, The file extension is not in .xml format"
			}
			redirect(action:"list", params:[category:params?.category])
	}
	
}
