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

import java.text.SimpleDateFormat
import java.util.List;


/**
 * Service class used to migrate database from new db to the existing db.
 */

class MigrationService {


	static transactional = true

	static datasource = 'DEFAULT'
	
	Map moduleNameChanges = [:]  
	/**
	 * FUnction to start migration
	 * @return
	 */
	def doMigration() {		
		println " migration "
		//		backup()	
		
		long time = System.currentTimeMillis()
		Role.withSession{ Role.findAll() }
		try {
			boolean flag = false
			Role.temp.withSession{
				def listr = Role?.temp?.findAll()
				if(listr?.size() > 0){
					flag=true
				}
			}
			if(flag){
				migrateToolData()
				migrateScriptData()
				cleanData()
			}
		} catch (Throwable e) {
		println " ERRORRSS "+e.getMessage();
			e.printStackTrace()
		}
		println "MIGRATION COMPLETED" + (System.currentTimeMillis() - time )
	}

	def cleanData(){
		cleanDB()
		cleanToolData()
	}

	/**
	 * Migrate general data
	 * @return
	 */
	def migrateToolData(){
		migrateRole()
		migrateSocVendor()
		migrateBoxManufacturers()
		migrateBoxModel()
		migrateBoxType()
		migrateRDKVersion()
		migrateScriptTag()
	}

	/**
	 * Migrate data corresponding to RDK
	 * @return
	 */
	def migrateScriptData(){
		migrateGroups()
		migrateModules()
		migrateFunctions()
		migrateParameterTypes()
		
//		migrateParameters()
//		migratePrimitiveTests()
//		migrateScripts()
		migrateScriptFile()
		migrateScriptGroup()
	}

	/**
	 * Migrate data from Role table
	 * @return
	 */
	def migrateRole(){

		def tempList = []
		Role.temp.withSession {
			tempList = Role.temp.findAll();
		}

		List migrationList = []
		tempList.each {tempEntry ->
			Role.withSession {
				def object = Role.findByName(tempEntry?.name)
				if(!object){
					migrationList.add(tempEntry)
				}
			}
		}
		migrationList.each{ mObject ->
			Role.withSession {
				Role obj
				try{
					obj  = new Role()
					obj.properties = mObject.getProperties()
					obj.properties.put("users", [:])
					obj.properties.put("permissions", [:])

					obj.save(flush:true)
				}catch(Exception e ){
				}

				def permissions = mObject?.permissions
				permissions.each { perm ->

					Role.withSession {
						if(perm){
							obj.addToPermissions(""+perm)
						}
					}
				}

			}
		}
	}

	/**
	 * Migrate data from SocVendor table
	 * @return
	 */
	def migrateSocVendor(){
		def tempList = []
		SoCVendor.temp.withSession {
			tempList = SoCVendor.temp.findAll();
		}

		List migrationList = []
		tempList.each {entry ->
			SoCVendor.withSession {
				def soCVendor = SoCVendor.findByNameAndCategory(entry?.name,entry?.category)
				if(!soCVendor){
					migrationList.add(entry)
				}
			}
		}

		migrationList.each{ mObject ->
			def groups
			Groups.withSession {
				groups = Groups.findByName(mObject?.groups?.name)
			}
			SoCVendor.withSession {
				try{
					SoCVendor socVendor  = new SoCVendor()
					socVendor.properties = mObject.getProperties()

					if(groups){
						socVendor.groups = groups
					}
					
					if(!mObject?.category){
						socVendor.category = Category.RDKV
					}
					
					if(!socVendor.save(flush:true)){
						println " save error "+socVendor?.errors
					}
				}catch(Exception e ){
				println " Err : "+e.getMessage()
				}
			}
		}
	}

	/**
	 * Migrate data from StreamingDetails
	 * @return
	 */
	def migrateStreamingDetails(){
		def tempList = []
		StreamingDetails.temp.withSession {
			tempList = StreamingDetails.temp.findAll();
		}

		List migrationList = []
		tempList.each {entry ->
			StreamingDetails.withSession {
				def streamingDetails = StreamingDetails.findByName(entry?.name)
				if(!streamingDetails){
					migrationList.add(entry)
				}
			}
		}
		migrationList.each{ mObject ->
			def groups
			Groups.withSession {
				groups = Groups.findByName(mObject?.groups?.name)
			}
			StreamingDetails.withSession {
				try{
					StreamingDetails obj  = new StreamingDetails()
					obj.properties = mObject.getProperties()

					if(groups){
						obj.groups = groups
					}
					obj.save(flush:true)
				}catch(Exception e ){
				}
			}
		}
	}
	
	/**
	 * Migrate data from BoxManufacturers
	 * @return
	 */
	def migrateBoxManufacturers(){
		def boxManufacturerTempList = []
		BoxManufacturer.temp.withSession {
			boxManufacturerTempList = BoxManufacturer.temp.findAll();
		}

		List migrationList = []
		boxManufacturerTempList.each {tempEntry ->
			BoxManufacturer.withSession {
				def boxManufacturer = BoxManufacturer.findByNameAndCategory(tempEntry?.name,tempEntry?.category)
				if(!boxManufacturer){
					migrationList.add(tempEntry)
				}
			}
		}
		migrationList.each{ mObject ->
			def groups
			Groups.withSession {
				groups = Groups.findByName(mObject?.groups?.name)
			}
			BoxManufacturer.withSession {
				try{
					BoxManufacturer boxManufacturer  = new BoxManufacturer()
					boxManufacturer.properties = mObject.getProperties()

					if(groups){
						boxManufacturer.groups = groups
					}
					
					if(!mObject?.category){
						boxManufacturer.category = Category.RDKV
					}
					
					boxManufacturer.save(flush:true)
				}catch(Exception e ){
				}
			}
		}
	}

	/**
	 * Migrate data from BoxModel
	 * @return
	 */
	def migrateBoxModel(){
		def tempList = []
		BoxModel.temp.withSession {
			tempList = BoxModel.temp.findAll();
		}

		List migrationList = []
		tempList.each {tempEntry ->
			BoxModel.withSession {
				def newDbObject = BoxModel.findByName(tempEntry?.name)
				if(!newDbObject){
					migrationList.add(tempEntry)
				}
			}
		}
		migrationList.each{ migrateObj ->
			def groups
			Groups.withSession {
				groups = Groups.findByName(migrateObj?.groups?.name)
			}
			BoxModel.withSession {
				try{
					BoxModel newObject  = new BoxModel()
					newObject.properties = migrateObj.getProperties()

					if(groups){
						newObject.groups = groups
					}
					newObject.save(flush:true)
				}catch(Exception e ){
				}
			}
		}
	}

	/**
	 * Migrate data from BoxType
	 * @return
	 */
	def migrateBoxType(){
		def tempList = []
		BoxType.temp.withSession {
			tempList = BoxType.temp.findAll();
		}

		List migrationList = []
		tempList.each {tempEntry ->
			BoxType.withSession {
				def newDbObject = BoxType.findByNameAndCategory(tempEntry?.name,tempEntry?.category)
				if(!newDbObject){
					migrationList.add(tempEntry)
				}
			}
		}
		migrationList.each{ migrateObj ->
			BoxType.withSession {
				try{
					BoxType newObject  = new BoxType(migrateObj.getProperties())
					
					if(!migrateObj?.category){
						newObject.category = Category.RDKV
					}
					newObject.save(flush:true)
				}catch(Exception e ){
				}
			}
		}

	}
	
	/**
	 * Migrate data from RDK Version
	 * @return
	 */
	def migrateRDKVersion(){
		def rdkVersionTempList = []
		RDKVersions.temp.withSession {
			rdkVersionTempList = RDKVersions.temp.findAll();
		}

		List migrationList = []
		rdkVersionTempList.each {tempEntry ->
			RDKVersions.withSession {
				def rdkVersion = RDKVersions.findByBuildVersionAndCategory(tempEntry?.buildVersion,tempEntry?.category)
				if(!rdkVersion){
					migrationList.add(tempEntry)
				}
			}
		}
		migrationList.each{ mObject ->
			def groups
			Groups.withSession {
				groups = Groups.findByName(mObject?.groups?.name)
			}
			RDKVersions.withSession {
				try{
					RDKVersions rdkVersion  = new RDKVersions()
					rdkVersion.properties = mObject.getProperties()

					if(groups){
						rdkVersion.groups = groups
					}
					if(!mObject?.category){
						rdkVersion.category = Category.RDKV
					}
					if(!rdkVersion.save(flush:true)){
					//	println "Error saving rdkVersion instance : ${rdkVersion.errors}"
					}
				}catch(Exception e ){
				}
			}
		}

	}
	
	
	/**
	 * Migrate data from Script Tag
	 * @return
	 */
	def migrateScriptTag(){
		def scriptTagTempList = []
		ScriptTag.temp.withSession {
			scriptTagTempList = ScriptTag.temp.findAll();
		}

		List migrationList = []
		scriptTagTempList.each {tempEntry ->
			RDKVersions.withSession {
				def scriptTag = ScriptTag.findByNameAndCategory(tempEntry?.name,tempEntry?.category)
				if(!scriptTag){
					migrationList.add(tempEntry)
				}
			}
		}
		migrationList.each{ mObject ->
			def groups
			Groups.withSession {
				groups = Groups.findByName(mObject?.groups?.name)
			}
			ScriptTag.withSession {
				try{
					ScriptTag scriptTag  = new ScriptTag()
					scriptTag.properties = mObject.getProperties()

					if(groups){
						scriptTag.groups = groups
					}
					if(!mObject?.category){
						scriptTag.category = Category.RDKV
					}
					if(!scriptTag.save(flush:true)){
					//	println "Error saving rdkVersion instance : ${rdkVersion.errors}"
					}
				}catch(Exception e ){
				}
			}
		}

	}
	
	

	def migrateScriptFile(){
		try {
			def tempList = []
					ScriptFile.temp.withSession {
				tempList = ScriptFile.temp.findAll();
			}
			println " size>> "+tempList?.size()
			List migrationList = []
					tempList.each {tempEntry ->
					ScriptFile.withSession {
						def newDbObject = ScriptFile.findByScriptNameAndModuleNameAndCategory(tempEntry?.scriptName,tempEntry?.moduleName,tempEntry?.category)
								if(!newDbObject){
									migrationList.add(tempEntry)
								}
					}
			}
			
			migrationList?.each{ migrateObj ->
				println "  migrate "+migrateObj
			ScriptFile.withSession {
				try{
					def sObject  = new ScriptFile()
					sObject.setScriptName(migrateObj?.scriptName)
					sObject.setModuleName(migrateObj?.moduleName)
					if(!migrateObj?.category){
						sObject.category = Category.RDKV
					}
					sObject.save(flush:true)
				}catch(Exception e ){
				println "EEE "+e.getMessage()
				}
			}
			}
		} catch (Exception e) {
		println "err "+e.getMessage() + "  eee "+e
			e.printStackTrace()
		}

	}
	/**
	 * Migrate data from ScriptGroup
	 * @return
	 */
	def migrateScriptGroup(){
		def tempList = []
		ScriptGroup.temp.withSession {
			tempList = ScriptGroup.temp.findAll();
		}
		List migrationList = tempList
//		tempList.each {tempEntry ->
//			ScriptGroup.withSession {
//				def newDbObject = ScriptGroup.findByName(tempEntry?.name)
//				if(!newDbObject){
//					migrationList.add(tempEntry)
//				}
//			}
//		}
		migrationList.each{ migrateObj ->
			ScriptGroup sgObject
			ScriptGroup.withSession {
				try{
					if(migrateObj?.scriptList?.size() > 0){
						def sproperties = migrateObj.getProperties()
						def oldModuleName = migrateObj?.name
//						if(moduleNameChanges.containsKey(oldModuleName)){
//							oldModuleName = moduleNameChanges.get(oldModuleName)
//						}

						sgObject = ScriptGroup.findByNameAndCategory(oldModuleName,migrateObj?.category)
						if(!sgObject){
							sgObject  = new ScriptGroup()
						}
						sgObject.properties = sproperties
						if(!migrateObj?.category){
							sgObject.category = Category.RDKV
						}
						sgObject.scripts =  []
						sgObject.scriptsList =  []
						sgObject.scriptList =  []
						if(!sgObject.save(flush:true)){
							println " Error in save "+sgObject?.errors
						}
					}
				}catch(Exception e ){
				println " Errors "+e.getMessage()
				}

			}
			def scriptList = migrateObj?.scriptList
			scriptList.each { script ->
				def scrpt
				ScriptFile.withSession{
					scrpt = ScriptFile.findByScriptNameAndModuleName(script?.scriptName,script?.moduleName)
				}
				ScriptGroup.withSession {
					if(scrpt){
						if(!sgObject?.scriptList?.contains(script)){
							sgObject?.addToScriptList(scrpt)
						}else{
						}
					}
				}
			}
			
//			def scripts = migrateObj?.scripts
//			scripts.each { script ->
//				def scrpt
//				if(!migrateObj?.scriptsList?.contains(script)){
//				Script.withSession{
//					scrpt = Script.findByName(script?.name)
//				}
//				ScriptGroup.withSession {
//					if(scrpt){
//						newObject.addToScriptsList(scrpt)
//					}
//				}
//				}
//			}
		}
	}

	/**
	 * clean the temp database
	 * @return
	 */
	private boolean cleanDB(){
		clearScriptGroups()
		cleanScriptFiles()
//		cleanScripts()
//		cleanPrimitiveTests()
//		cleanParameters()
		cleanParameterTypes()
		cleanFunctions()
		cleanModules()
		cleanGroups()
	}

	/**
	 * clean the tool specific table data from temp database
	 * @return
	 */
	def cleanToolData(){
		cleanBoxManufacturers()
		cleanBoxModel()
		cleanBoxType()
		cleanSocVendors()
		//		cleanRole()
		cleanStreamingDetails()
	}

	/**
	 * Removing box types that are migrated or available in the existing DB
	 */
	private void cleanBoxType(){

		def funTempList = []
		BoxType.temp.withSession {
			funTempList = BoxType.temp.findAll();
		}

		List migrationList = []
		funTempList.each {testEntry ->
			BoxType.withSession {
				def test = BoxType.findByName(testEntry?.name)
				if(test){
					migrationList.add(testEntry)
				}
			}
		}

		migrationList.each{ mObject -> deleteBoxType(mObject) }
	}

	/**
	 * Removing box models that are migrated or available in the existing DB
	 */
	private void cleanBoxModel(){
		def funTempList = []
		BoxModel.temp.withSession {
			funTempList = BoxModel.temp.findAll();
		}

		List migrationList = []
		funTempList.each {testEntry ->
			BoxModel.withSession {
				def test = BoxModel.findByName(testEntry?.name)
				if(test){
					migrationList.add(testEntry)
				}
			}
		}

		migrationList.each{ mObject -> deleteBoxModel(mObject) }
	}
	
	/**
	 * Removing box Manufacturers that are migrated or available in the existing DB
	 */
	private void cleanBoxManufacturers(){
		def funTempList = []
		BoxManufacturer.temp.withSession {
			funTempList = BoxManufacturer.temp.findAll();
		}

		List migrationList = []
		funTempList.each {testEntry ->
			BoxManufacturer.withSession {
				def test = BoxManufacturer.findByName(testEntry?.name)
				if(test){
					migrationList.add(testEntry)
				}
			}
		}

		migrationList.each{ mObject -> deleteBoxManufacturer(mObject) }
	}
	
	/**
	 * Removing box RDKVersions that are migrated or available in the existing DB
	 */
	private void cleanRDKVersions(){
		def rdkVersionTempList = []
		RDKVersions.temp.withSession {
			rdkVersionTempList = RDKVersions.temp.findAll();
		}

		List migrationList = []
		rdkVersionTempList.each {testEntry ->
			RDKVersions.withSession {
				def test = RDKVersions.findByBuildVersion(testEntry?.buildVersion)
				if(test){
					migrationList.add(testEntry)
				}
			}
		}

		migrationList.each{ mObject -> deleteRDKVersions(mObject) }
	}

	/**
	 * Removing StreamingDetails that are migrated or available in the existing DB
	 */
	private void cleanStreamingDetails(){
		def tempList = []
		StreamingDetails.temp.withSession {
			tempList = StreamingDetails.temp.findAll();
		}

		List migrationList = []
		tempList.each {testEntry ->
			StreamingDetails.withSession {
				def test = StreamingDetails.findByStreamId(testEntry?.streamId)
				if(test){
					migrationList.add(testEntry)
				}
			}
		}

		migrationList.each{ mObject -> deleteStreamingDetails(mObject) }
	}

	/**
	 * Removing Roles that are migrated or available in the existing DB
	 */
	private void cleanRole(){
		def tempList = []
		Role.temp.withSession {
			tempList = Role.temp.findAll();
		}

		List migrationList = []
		tempList.each {testEntry ->
			Role.withSession {
				def test = Role.findByName(testEntry?.name)
				if(test){
					migrationList.add(testEntry)
				}
			}
		}

		migrationList.each{ mObject -> deleteRole(mObject) }
	}

	/**
	 * Removing SocVendors that are migrated or available in the existing DB
	 */
	private void cleanSocVendors(){
		def tempList = []
		SoCVendor.temp.withSession {
			tempList = SoCVendor.temp.findAll();
		}

		List migrationList = []
		tempList.each {testEntry ->
			SoCVendor.withSession {
				def test = SoCVendor.findByName(testEntry?.name)
				if(test){
					migrationList.add(testEntry)
				}
			}
		}

		migrationList.each{ mObject -> deleteSocVendor(mObject) }
	}

	/**
	 * Removing Groups that are migrated or available in the existing DB
	 */
	private void cleanGroups(){
		def funTempList = []
		Groups.temp.withSession {
			funTempList = Groups.temp.findAll();
		}

		List migrationList = []
		funTempList.each {testEntry ->
			Groups.withSession {
				def test = Groups.findByName(testEntry?.name)
				if(test){
					migrationList.add(testEntry)
				}
			}
		}
		migrationList.each{ mObject -> deleteGroups(mObject) }
	}

	/**
	 * Removing Modules that are migrated or available in the existing DB
	 */
	private void cleanModules(){
		def funTempList = []
		Module.temp.withSession {
			funTempList = Module.temp.findAll();
		}

		List migrationList = []
		funTempList.each {testEntry ->
			Module.withSession {
				def test = Module.findByName(testEntry?.name)
				if(test){
					migrationList.add(testEntry)
				}
			}
		}
		migrationList.each{ mObject -> deleteModules(mObject) }
	}

	/**
	 * Removing Functions that are migrated or available in the existing DB
	 */
	private void cleanFunctions(){
		def funTempList = []
		Function.temp.withSession {
			funTempList = Function.temp.findAll();
		}

		List migrationList = []
		funTempList.each {testEntry ->
			
			Module mod
			Module.withSession{
			 mod = Module.findByName(testEntry?.module?.name)
			}
			
			Function.withSession {
				def test = Function.findByNameAndModule(testEntry?.name,mod)
				if(test){
					migrationList.add(testEntry)
				}
			}
		}
		migrationList.each{ mObject -> deleteFunction(mObject) }
	}

	/**
	 * Removing ParameterTypes that are migrated or available in the existing DB
	 */
	private void cleanParameterTypes(){
		def paramTypeTempList = []
		ParameterType.temp.withSession {
			paramTypeTempList = ParameterType.temp.findAll();
		}

		List migrationList = []
		paramTypeTempList.each {testEntry ->
			ParameterType.withSession {
				String  name = testEntry?.function?.name
				
				Module mod 
				Module.withSession{
				 mod = Module.findByName(testEntry?.function?.module?.name)
				}
				
				Function fun
				Function.withSession{
					fun = Function.findByNameAndModule(name,mod)
				}
				
				def test = ParameterType.findByNameAndFunction(testEntry?.name,fun)
				if(test){
					migrationList.add(testEntry)
				}
			}
		}
		migrationList.each{ mObject -> deleteParameterType(mObject) }
	}

	/**
	 * Removing PrimitiveTests that are migrated or available in the existing DB
	 */
	private void cleanPrimitiveTests(){
		try {
			def primitiveTempList = []
			PrimitiveTest.temp.withSession {
				primitiveTempList = PrimitiveTest.temp.findAll();
			}

			List migrationList = []
			primitiveTempList.each {testEntry ->

				def module
				Module.withSession{
					module = Module.findByName(testEntry?.module?.name)
				}

				def function
				Function.withSession{
					function = Function.findByNameAndModule(testEntry?.function?.name,module)
				}


				PrimitiveTest.withSession {
					def test = PrimitiveTest.findByNameAndFunctionAndModule(testEntry?.name,function,module)
//					def test = PrimitiveTest.findByName(testEntry?.name)
					if(test){
						migrationList.add(testEntry)
					}
				}
			}
			migrationList.each{ mObject -> deletePrimitiveTest(mObject) }
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	/**
	 * Removing Parameters that are migrated or available in the existing DB
	 */
	private void cleanParameters(){
		def parameterTempList = []
		Parameter.temp.withSession {
			parameterTempList = Parameter.temp.findAll();
		}

		List migrationList = []
		List paramList = []
		parameterTempList.each {parameterEntry ->
			def pType
			def fn
			
			Module mod
			Module.withSession{
			 mod = Module.findByName(parameterEntry?.parameterType?.function?.module?.name)
			}
			
			Function.withSession {
				fn = Function.findByNameAndModule(parameterEntry?.parameterType?.function?.name,mod)
			}
			
			if(fn){
				ParameterType.withSession {
					pType = ParameterType.findByNameAndFunction(parameterEntry?.parameterType?.name,fn)
				}
				if(pType){
					Parameter.withSession {
						def parameter = Parameter.findByParameterTypeAndValue(pType,parameterEntry?.value)
						if(parameter){
							migrationList.add(parameterEntry)
						}
					}
				}
			}
		}

		migrationList.each{ mObject ->
			deleteParameter(mObject)
		}
	}

	
	private void clearScriptGroups(){
		
		try {
			ScriptGroup.temp.withSession{
				def sgList = ScriptGroup.temp.findAll()
				sgList.each { sg ->
					sg?.scriptsList?.clear()
					sg?.scripts?.clear()
					sg?.scriptList?.clear()
					sg?.temp.save()
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	/**
	 * Removing Scripts that are migrated or available in the existing DB
	 */
	private void cleanScripts(){
		def scriptTempList = []
		Script.temp.withSession {
			scriptTempList = Script.temp.findAll();
		}

		List migrationList = []
		scriptTempList.each {scriptEntry ->
			Script.withSession {
				def script = Script.findByName(scriptEntry?.name)
				
				if(script){
					migrationList.add(scriptEntry)
				}
			}
		}
		
		
		
		migrationList.each{ mObject -> deleteScripts(mObject) }
	}
	
	/**
	 * Removing Scripts that are migrated or available in the existing DB
	 */
	private void cleanScriptFiles(){
		try {
			def scriptTempList = []
					ScriptFile.temp.withSession {
				scriptTempList = ScriptFile.temp.findAll();
			}
			
			List migrationList = []
					scriptTempList.each {scriptEntry ->
					ScriptFile.withSession {
						def script = ScriptFile.findByScriptNameAndModuleName(scriptEntry?.scriptName,scriptEntry?.moduleName)
								if(script){
									migrationList.add(scriptEntry)
								}
					}
			}
			
			
			
			migrationList.each{ mObject -> deleteScriptFiles(mObject) }
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	/**
	 * Removing Script groups that are migrated or available in the existing DB
	 */
	private void cleanScriptGroup(){


		try {
			def sgTempList = []
			ScriptGroup.temp.withSession {
				sgTempList = ScriptGroup.temp.findAll();
			}

			List migrationList = []
			sgTempList.each {sgEntry ->
				ScriptGroup.withSession {
					def scriptGroup = ScriptGroup.findByName(sgEntry?.name)
					if(scriptGroup){
						migrationList.add(sgEntry)
					}
				}
			}

			migrationList.each{ mObject -> deleteScriptGroup(mObject) }
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	/**
	 * Method to delete the script from temp db
	 * @param mObject
	 * @return
	 */
	def deleteScripts(def mObject){
		try {

			boolean flag = true //removeFromScriptSuite(mObject)
			if(flag){
				if(mObject.temp.delete()){
				//	println "Error saving function instance : ${mObject.errors}"
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
	
	def deleteScriptFiles(def mObject){
		try {

			boolean flag = true 
			if(flag){
				if(mObject.temp.delete()){
				//	println "Error saving function instance : ${mObject.errors}"
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	/**
	 * Method to delete the script group from temp db
	 * @param mObject
	 * @return
	 */
	def deleteScriptGroup(def mObject){

		ScriptGroup.temp.withSession{
			try {
				mObject.temp.delete()
			} catch (Exception e) {
				e.printStackTrace()
			}
		}
	}
	
	/**
	 * Method to remove the script from script suite in temp db
	 * @param mObject
	 * @return
	 */
	private boolean removeFromScriptSuite(def script){
		def timee = System.currentTimeMillis()
		/**
		 * Selecting ScriptGroups where the given script is present
		 *
		 */
		ScriptGroup.temp.withSession{

			def idList = []
			idList.add(script.id)
			def scriptGroups = ScriptGroup.temp.createCriteria().list {
				ScriptGroup.temp.withSession{
					scriptsList{
						Script.temp.withSession{ 'in'('id',idList) }
					}
				}
			}
			
			
			
			def scriptInstance
			def time2 = System.currentTimeMillis()
			scriptGroups?.each{ scriptGrp ->
				scriptInstance = scriptGrp.scriptsList.find { it.id == script.id }
				if(scriptInstance){
					scriptGrp.removeFromScriptsList(scriptInstance)
				}
			}
		}

		return true
	}

	/**
	 * Method to migrate parameter types
	 */
	def migrateParameterTypes(){
		def parameterList =[]
		ParameterType.withSession {
			parameterList = ParameterType.findAll();
		}

		def parameterTempList = []
		ParameterType.temp.withSession {
			parameterTempList = ParameterType.temp.findAll();
		}

		List migrationList = parameterTempList

		migrationList.each{ mParam ->

			try{
				
				Module mod
				Module.withSession{
				 mod = Module.findByName(mParam?.function?.module?.name)
				}
				
				def function
				Function.withSession {
					function = Function.findByNameAndModule(mParam?.function?.name,mod)
				}
				ParameterType.withSession {

					ParameterType paramType = ParameterType.findByNameAndFunction(mParam?.name,function)
					if(paramType == null){
						paramType  = new ParameterType()
					}
					paramType.properties = mParam.getProperties()
					if(function){
						paramType.function = function
					}
					paramType.save(flush:true)
				}
			}catch(Exception e ){
			}
		}
	}

	/**
	 * Method to migrate primitive tests
	 */
	def migratePrimitiveTests(){
		def primitiveList =[]
		PrimitiveTest.withSession {
			primitiveList = PrimitiveTest.findAll();
		}

		def primitiveTempList = []
		PrimitiveTest.temp.withSession {
			primitiveTempList = PrimitiveTest.temp.findAll();
		}

		List migrationList = primitiveTempList
		
		PrimitiveTest.withSession {
			migrationList.each{ mPrimitive ->
				try{
					
					def module = Module.findByName(mPrimitive?.module?.name)
					
					
					def function = Function.findByNameAndModule(mPrimitive?.function?.name,module)
					

					
					
					PrimitiveTest primitiveTest
					PrimitiveTest.withSession {

						primitiveTest = PrimitiveTest.findByNameAndFunctionAndModule(mPrimitive?.name,function,module)
					}
					
					if(primitiveTest == null){
						primitiveTest  = new PrimitiveTest()
					}
						
					primitiveTest.properties = mPrimitive.getProperties()
					primitiveTest.properties.put("parameters", [:])
					
					if(module){
						primitiveTest.module = module
					}
					
					if(function){
						primitiveTest.function = function
					}
					def groups = Groups.findByName(mPrimitive?.groups?.name)
					
					if(groups){
						primitiveTest.groups = groups
					}
					
					
					if(!primitiveTest.save(flush:true)){
					//	println "Error saving primitiveTest instance : ${primitiveTest.errors}"
					}
					
					
					def paramList = mPrimitive?.parameters
					paramList.each { param ->
						def paramType = ParameterType.findByNameAndFunction(param?.parameterType?.name,function)
						if(paramType){
							def ppp
							Parameter parameter = null
							Parameter.withSession {
								
								if(paramType){
									def paramtrList = Parameter.findAllByParameterTypeAndValue(paramType,param?.value)
									paramtrList.each { p ->
										if(parameter == null && p.primitiveTest == null){
											parameter =p;
										}
										
									}
									
								}
							}
							
							if(parameter){
								PrimitiveTest.withSession {
									primitiveTest.addToParameters(parameter)
								}
							}
						}
					}
				}catch(Exception e ){
			//	println " errorr "+e.getMessage()
				}
			}
		}
	}

	/**
	 * Method to migrate parameters
	 */
	def migrateParameters(){

		def parameterList = []
		Parameter.withSession {
			parameterList = Parameter.list();
		}

		def parameterTempList = []
		Parameter.temp.withSession {
			parameterTempList = Parameter.temp.list();
		}
		List migrationList = parameterTempList
		int counter = 0;
		List paramList = []
		migrationList.each{ mParam ->

			try{
				
				Module mod
			Module.withSession{
			 mod = Module.findByName(mParam?.parameterType?.function?.module?.name)
			}
				
				def fn
				Function.withSession {
					fn = Function.findByNameAndModule(mParam?.parameterType?.function?.name,mod)
				}
				
				def parameterType
				ParameterType.withSession {
					parameterType = ParameterType.findByNameAndFunction(mParam?.parameterType?.name,fn)
				}


				if(fn){
					Parameter.withSession {
						Parameter parameter
						if(parameterType){
							parameter = Parameter.findByParameterTypeAndValue(parameterType,mParam?.value)
						}
						if(parameter == null){
							parameter  = new Parameter()
						}
						parameter.properties = mParam.getProperties()
						parameterType = ParameterType.findByNameAndFunction(mParam?.parameterType?.name,fn)
						if(parameterType){
							parameter.parameterType = parameterType
						parameter.primitiveTest = null
						parameter.save(flush:true)
						}
					}
				}
			}catch(Exception e ){
			}
		}
	}

	/**
	 * Method to migrate groups
	 */
	def migrateGroups(){
		def groupList =[]
		Groups.withSession {
			groupList = Groups.findAll();
		}

		def groupTempList = []
		Groups.temp.withSession {
			groupTempList = Groups.temp.findAll();
		}

		List migrationList = []

		groupTempList.each {groupEntry ->
			Groups.withSession {
				def group = Groups.findByName(groupEntry.name)
				if(!group){
					migrationList.add(groupEntry)
				}
			}
		}

		List savedList = []

		Groups.withSession {
			migrationList.each{ migrateObject ->
				try{
					Groups group  = new Groups()
					group.properties = migrateObject.getProperties()
					savedList.add(migrateObject?.id)
					group.save(flush:true)
				}catch(Exception e ){
				}
			}
		}
	}

	/**
	 * Method to migrate modules
	 */
	def migrateModules(){
		def moduleTempList = []
		Module.temp.withSession {
			moduleTempList = Module.temp.findAll();
		}

		List migrationList = moduleTempList
		List savedList = []
		migrationList.each{ mModule ->
	if(!(mModule?.toString()?.equals("tcl"))){
			def groups
			Groups.withSession {
				groups = Groups.findByName(mModule?.groups?.name)
			}
			Module module
			Module.withSession {
				try{
					def oldModuleName = mModule?.name
//					if(moduleNameChanges.containsKey(oldModuleName)){
//						oldModuleName = moduleNameChanges.get(oldModuleName)
//					}
					
					module = Module.findByNameAndCategory(oldModuleName,mModule?.category)
					if(module == null){
						module  = new Module()
					}
					module.properties = mModule.getProperties()
					module.properties.put("logFileNames", [:])
					module.properties.put("stbLogFiles", [:])
					module.groups = null
					if(groups){
						module.groups = groups
					}
					if(!mModule?.category){
						module.category = Category.RDKV
					}
					
					if(!module.save(flush:true)){
						println " Error "+module?.errors
					}
				}catch(Exception e ){
				}
			}

			def logFileNames = mModule?.logFileNames
			logFileNames.each { logFileName ->
				Module.withSession {
					module?.addToLogFileNames(""+logFileName)
				}
			}

			}
		}
	}

	/**
	 * Method to migrate functions
	 */
	def migrateFunctions(){
		def funTempList = []
		Function.temp.withSession {
			funTempList = Function.temp.findAll();
		}

		List migrationList = funTempList
		
		migrationList.each{ mObject ->
			
			Module mod
			Module.withSession{
			 mod = Module.findByName(mObject?.module?.name)
			}
			
			Function.withSession {
				try{

					Function ff = Function.findByNameAndModuleAndCategory(mObject.name,mod,mObject?.category)

					if(ff == null){
						ff  = new Function()
					}
					
					ff.properties = mObject.getProperties()
					def mod1 = Module.findByName(mObject?.module?.name)
					//					ff.name = mObject?.name
					if(mod1){
						ff.module = mod1
					}
					if(!mObject?.category){
						ff.category = Category.RDKV
					}
					
					if(!ff.save(flush:true)){
					//	println "Error saving function instance : ${ff.errors}"
					}
				}catch(Exception e ){
					e.printStackTrace()
				}
			}
		}
	}

	/**
	 * Method to delete box type from temp db
	 */
	def deleteBoxType(def boxType){
		BoxType.temp.withSession{

			try {
				boxType.temp.delete();
			} catch (Exception e) {
				e.printStackTrace()
			}
		}
	}

	def List getBoxTypeTempList(){
		def funTempList = []
		BoxType.temp.withSession {
			funTempList = BoxType.temp.findAll();
		}
		return funTempList
	}

	/**
	 * Method to delete streaming details from temp db
	 */
	def deleteStreamingDetails(def mObject){

		StreamingDetails.temp.withSession{
			try {
				mObject.temp.delete()
			} catch (Exception e) {
				e.printStackTrace()
			}
		}
	}

	/**
	 * Method to delete box manufactures from temp db
	 */
	def deleteBoxManufacturer(def mObject){

		BoxManufacturer.temp.withSession{
			try {
				mObject.temp.delete()
			} catch (Exception e) {
				e.printStackTrace()
			}
		}
	}
	
	/**
	 * Method to delete rdk versions from temp db
	 */
	def deleteRDKVersions(def mObject){

		RDKVersions.temp.withSession{
			try {
				mObject.temp.delete()
			} catch (Exception e) {
				e.printStackTrace()
			}
		}
	}

	
	/**
	 * Method to delete box model from temp db
	 */
	def deleteBoxModel(def mObject){
		BoxModel.temp.withSession{
			try {
				mObject.temp.delete()
			} catch (Exception e) {
				e.printStackTrace()
			}
		}
	}

	/**
	 * Method to delete primitive test from temp db
	 */
	def deletePrimitiveTest(def mObject){
		PrimitiveTest.temp.withSession{
			try {
				mObject.temp.delete()
			} catch (Exception e) {
				e.printStackTrace()
			}
		}
	}

	/**
	 * Method to delete parameter from temp db
	 */
	def deleteParameter(def mObject){
		Parameter.temp.withSession{
			try {
				mObject.temp.delete()
			} catch (Exception e) {
			//	println "Error in delete"+e.getMessage()
				e.printStackTrace()
			}
		}
	}

	/**
	 * Method to delete parameter type from temp db
	 */
	def deleteParameterType(def mObject){
		ParameterType.temp.withSession{
			try {
				mObject.temp.delete()
			} catch (Exception e) {
				e.printStackTrace()
			}
		}
	}

	/**
	 * Method to delete function from temp db
	 */
	def deleteFunction(def mObject){
		Function.temp.withSession{
			try {
				mObject.temp.delete()
			} catch (Exception e) {
				e.printStackTrace()
			}
		}
	}

	/**
	 * Method to delete modules from temp db
	 */
	def deleteModules(def mObject){
		Module.temp.withSession{
			try {
				mObject.temp.delete()
			} catch (Exception e) {
				e.printStackTrace()
			}
		}
	}
	
	/**
	 * Method to delete groups from temp db
	 */
	def deleteGroups(def mObject){
		Groups.temp.withSession{
			try {
				mObject.temp.delete()
			} catch (Exception e) {
				e.printStackTrace()
			}
		}
	}

	/**
	 * Method to delete soc vendor from temp db
	 */
	def deleteSocVendor(def mObject){
		SoCVendor.temp.withSession{
			try {
				mObject.temp.delete()
			} catch (Exception e) {
				e.printStackTrace()
			}
		}
	}

	/**
	 * Method to delete role from temp db
	 */
	def deleteRole(def mObject){
		Role.temp.withSession{
			try {
				mObject.temp.delete()
			} catch (Exception e) {
				e.printStackTrace()
			}
		}
	}
}
