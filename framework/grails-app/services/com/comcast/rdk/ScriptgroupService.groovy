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

import static com.comcast.rdk.Constants.KEY_GROUP

/**
 * A service class for ScriptGroups
 * @author sreejasuma
 *
 */

class ScriptgroupService {
	static datasource = 'DEFAULT'


	/**
	 * Method to save the script to a ScriptGroup, according to the module name and box type, rdk version combination.
	 * If the script group exists then add the script to that group.
	 * Else create a script group and add the script to the group.
	 * @param scriptInstance
	 * @return
	 */

	def saveToScriptGroups(final ScriptFile scriptInstance,final ScriptObject sObject, final String category){
		try {
			def moduleName = scriptInstance?.moduleName


			if(sObject.getLongDuration()){
				moduleName = moduleName + "_LD"
			}

			def scriptGrpInstance = ScriptGroup.findByName(moduleName)

			if(!scriptGrpInstance){
				scriptGrpInstance = new ScriptGroup()
				scriptGrpInstance.name = moduleName
				scriptGrpInstance.scriptList = []
				scriptGrpInstance.category = Utility.getCategory(category)
				scriptGrpInstance.save()
			}
			if(!scriptGrpInstance?.scriptList?.contains(scriptInstance)){
				scriptGrpInstance.addToScriptList(scriptInstance)
			}
		} catch (Exception e) {
			e.printStackTrace()
		}

		try {
			sObject?.boxTypes?.each{ bType ->

				sObject?.rdkVersions?.each{ vers ->

					//					String name = vers?.toString()+"_"+bType?.name
					def names = []

					Module module
					Module.withTransaction{
						module = Module.findByName(sObject?.module)
					}

					if(!sObject.getLongDuration()){
						names.add(vers?.toString()+"_"+bType?.name)
						removeScriptFromScriptGroup(scriptInstance, vers?.toString()+"_"+bType?.name+"_LD")
					}else{

						try {
							removeScriptFromScriptGroup(scriptInstance, vers?.toString()+"_"+bType?.name)
							removeScriptFromScriptGroup(scriptInstance, vers?.toString()+"_"+bType?.name+Constants.NO_OS_SUITE)
						} catch (Exception e) {
							e.printStackTrace()
						}
						names.add(vers?.toString()+"_"+bType?.name+"_LD")
					}

					names.each { name ->
						def scriptGrpInstance = ScriptGroup.findByName(name)
						if(!scriptGrpInstance){
							scriptGrpInstance = new ScriptGroup()
							scriptGrpInstance.name = name
							scriptGrpInstance.scriptList = []
							scriptGrpInstance.category = Utility.getCategory(category)
							scriptGrpInstance.save(flush:true)
						}
						if(scriptGrpInstance && !scriptGrpInstance?.scriptList?.contains(scriptInstance)){
							scriptGrpInstance.addToScriptList(scriptInstance)
						}
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}



	def updateScriptGroup(final ScriptFile scriptInstance,final ScriptObject scriptObj, final String category){
		try {
			String moduleName = scriptObj.getModule()
			if(scriptObj.getLongDuration()){
				removeScriptFromScriptGroup(scriptInstance, moduleName)
				moduleName = moduleName + "_LD"
			}else{
				removeScriptFromScriptGroup(scriptInstance, moduleName+"_LD")
			}

			def scriptGrpInstance = ScriptGroup.findByName(moduleName)
			if(!scriptGrpInstance){
				scriptGrpInstance = new ScriptGroup()
				scriptGrpInstance.name = moduleName
				scriptGrpInstance.category = Utility.getCategory(category)
				scriptGrpInstance.scriptList = []
			}
			if(!scriptGrpInstance.scriptList.contains(scriptInstance)){
				scriptGrpInstance.addToScriptList(scriptInstance)
				scriptGrpInstance.save(flush:true)
			}
		} catch (Exception e) {
			e.printStackTrace()
		}

	}

	/**
	 * Method to save the script to a script group, according to the library chosen for the script
	 * Creates two types of script groups.
	 * 1: Based on Test group of selected library.
	 * 2: Based on the boxType of script.
	 * @param scriptInstance
	 * @param boxTypeList
	 * @return
	 */

	def saveToDefaultGroups(final def scriptInstance, final ScriptObject scriptObject , final def boxTypeList, final String category){

		def moduleName = scriptInstance?.moduleName
		def module = Module.findByName(moduleName)
		String groupName = module?.testGroup?.toString() + KEY_GROUP
	

		//		 String groupName = scriptInstance.primitiveTest.module.testGroup.toString() + KEY_GROUP

		if(scriptObject.getLongDuration()){
			groupName = groupName + "_LD"
			removeScriptFromScriptGroup(scriptInstance, module?.testGroup?.toString() + KEY_GROUP)
		}else{
			removeScriptFromScriptGroup(scriptInstance, module?.testGroup?.toString() + KEY_GROUP+"_LD")
		}


		createOrUpdateScriptGroups(scriptInstance, groupName,category)

		boxTypeList.each { boxType ->

			BoxType box = BoxType.findById(boxType?.id);
			if(box){
				groupName = box.name + KEY_GROUP

				if(scriptObject.getLongDuration()){
					groupName = groupName + "_LD"
					removeScriptFromScriptGroup(scriptInstance, box?.name + KEY_GROUP)
				}else{
					removeScriptFromScriptGroup(scriptInstance, box?.name + KEY_GROUP+"_LD")
				}

				createOrUpdateScriptGroups(scriptInstance, groupName, category)
			}
		}

	}

	private boolean checkIsPresent(ScriptFile sFile , String scriptGroupName){
		ScriptGroup sg = ScriptGroup.findByName(scriptGroupName)
		return sg?.scriptList?.contains(sFile)
	}


	/**
	 * Method to create or update script group
	 * If the script group exists then add the script to that group.
	 * Else create a script group and add the script to the group.
	 * @param scriptInstance
	 * @param groupName
	 * @return
	 */
	def createOrUpdateScriptGroups(final def scriptInstance, final String groupName, final String category){

		def scriptGrpInstance = ScriptGroup.findByName(groupName)
		if(!scriptGrpInstance){
			scriptGrpInstance = new ScriptGroup()
			scriptGrpInstance.name = groupName
			scriptGrpInstance.category = Utility.getCategory(category)
			scriptGrpInstance.save(flush:true)
		}
		if(!scriptGrpInstance?.scriptList?.contains(scriptInstance)){
			scriptGrpInstance.addToScriptList(scriptInstance)
		}

	}


	/**
	 * Method to remove a particular script from all available box suites.
	 * This method is called during update operation of scripts.
	 * @param scriptInstance
	 * @return
	 */
	def removeScriptsFromBoxSuites(final def scriptInstance){

		int flag = 0
		def boxTypeList = BoxType.list()
		boxTypeList.each { boxType ->

			def groupNames = [boxType?.name + KEY_GROUP,boxType?.name + KEY_GROUP+"_LD"]

			groupNames.each { groupName ->

				def scriptGrpInstance = ScriptGroup?.findByName(groupName , [lock : true])
				if(scriptGrpInstance){
					scriptGrpInstance?.scriptList.each { script ->
						if(script?.name == scriptInstance?.scriptName){
							flag = 1
						}
					}

					if(flag){
						scriptGrpInstance.removeFromScriptList(scriptInstance)
					}
				}
			}
		}
	}

	def removeScriptsFromBoxSuites1(final def scriptInstance){

		String groupName
		int flag = 0
		def boxTypeList = BoxType?.list()
		boxTypeList?.each {boxType ->
			groupName = boxType.name + KEY_GROUP
			def scriptGrpInstance = ScriptGroup?.findByName(groupName , [lock : true])
			if(scriptGrpInstance){
				if(scriptInstance){
					scriptGrpInstance?.scriptList?.each { script ->
						if(script?.scriptName == scriptInstance?.scriptName){
							flag = 1
						}
					}

					if(flag){
						scriptGrpInstance?.removeFromScriptList(scriptInstance)
					}
				}
			}
		}
	}

	def removeScriptsFromBoxScriptGroup(final def scriptInstance,List boxTypes,List oldBoxTypes){
		String groupName
		try {
			oldBoxTypes?.each {boxType ->
				groupName = boxType.name + KEY_GROUP
				if(!boxTypes?.contains(boxType)){
					ScriptGroup.withTransaction {
						def scriptGrpInstance = ScriptGroup?.findByName(groupName)
						if(scriptGrpInstance){
							if(scriptInstance){
								if(scriptGrpInstance?.scriptList?.contains(scriptInstance)){
									scriptGrpInstance?.removeFromScriptList(scriptInstance)
									if(!scriptGrpInstance?.save(flush:true)){
										println " EEE "+scriptGrpInstance?.errors
									}
								}
							}
						}
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	/**
	 * Method to save the script to relevant script groups and remove from others.
	 * @param scriptInstance
	 * @return
	 */
	def updateScriptsFromRDKVersionBoxTypeTestSuites(final Script scriptInstance){

		try {
			def bTypeList = BoxType?.findAll()
			def rdkVersionList = RDKVersions?.findAll()

			bTypeList?.each { bType ->
				rdkVersionList.each { vers ->
					String groupName = vers?.toString()+"_"+bType?.name
					def scriptGrpInstance = ScriptGroup.findByName(groupName)
					if(scriptGrpInstance && scriptGrpInstance?.scriptsList?.contains(scriptInstance)){
						scriptGrpInstance.removeFromScriptsList(scriptInstance)
					}
				}
			}

			scriptInstance?.boxTypes?.each{ bType ->

				scriptInstance?.rdkVersions?.each{ vers ->

					String name = vers?.toString()+"_"+bType?.name

					def scriptGrpInstance = ScriptGroup.findByName(name)
					if(!scriptGrpInstance){
						scriptGrpInstance = new ScriptGroup()
						scriptGrpInstance.name = name
						scriptGrpInstance.save(flush:true)
					}
					if(scriptGrpInstance && !scriptGrpInstance?.scriptsList?.contains(scriptInstance)){
						scriptGrpInstance.addToScriptsList(scriptInstance)
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	def updateScriptsFromRDKVersionBoxTypeTestSuites1(final def scriptInstance,final ScriptObject sObject, final def category){
		try {
			def bTypeList = BoxType.findAllByCategory(category)
			def rdkVersionList = RDKVersions?.findAllByCategory(category)

			bTypeList?.each { bType ->
				rdkVersionList.each { vers ->
					def groupNames  = [vers?.toString()+"_"+bType?.name,vers?.toString()+"_"+bType?.name+Constants.NO_OS_SUITE,vers?.toString()+"_"+bType?.name+"_LD"]
					groupNames.each {  groupName ->
						def scriptGrpInstance = ScriptGroup.findByName(groupName)
						if(scriptGrpInstance && scriptGrpInstance?.scriptList?.contains(scriptInstance)){
							scriptGrpInstance.removeFromScriptList(scriptInstance)
						}
					}
				}
			}

			sObject?.getBoxTypes()?.each{ bType ->

				sObject?.getRdkVersions()?.each{ vers ->

					Module module
					Module.withTransaction{
						module = Module.findByName(sObject?.module)
					}

					def names = []
					if(!sObject?.getLongDuration()){
						names.add(vers?.toString()+"_"+bType?.name)
						if(module?.testGroup != TestGroup.OpenSource){
							names.add(vers?.toString()+"_"+bType?.name+Constants.NO_OS_SUITE)
						}
					}else{
						names.add(vers?.toString()+"_"+bType?.name+"_LD")
					}

					names.each {  name ->
						def scriptGrpInstance = ScriptGroup.findByName(name)
						if(!scriptGrpInstance){
							scriptGrpInstance = new ScriptGroup()
							scriptGrpInstance.name = name
							scriptGrpInstance.save()
						}
						if(scriptGrpInstance && !scriptGrpInstance?.scriptList?.contains(scriptInstance)){
							scriptGrpInstance.addToScriptList(scriptInstance)
						}
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}


	/**
	 * Method to convert boxType params to list of boxTypes.
	 * @param boxTypes
	 * @return
	 */
	def createBoxTypeList(def boxTypes){

		def boxTypesList = []
		if(boxTypes instanceof String){
			boxTypesList.add(boxTypes)
		}
		else{
			boxTypes.each { boxType ->
				boxTypesList.add(boxType)
			}
		}
		return boxTypesList
	}


	/**
	 * Delete script after checking whether the script is executing on a device
	 * or the script is present in a script group which is selected to execute
	 */

	public boolean checkScriptStatus(final ScriptFile scriptFile , final def script){
		//		Script script
		//		Script.withTransaction {
		//			script = Script.findById(scriptOrig?.id)
		//		}
		if(script == null || scriptFile == null){
			return false
		}
		boolean scriptInUse = false
		boolean isAllocatedScriptGrp = false
		try {
			if(script?.status.equals( Status.ALLOCATED.toString() )){
				scriptInUse = true
			}

			else{
				/**
				 * Selecting scriptGroups based on whether selected script exists
				 * in the script group's and status of the ScriptGroup is Allocated.
				 * In this case the script cannot be deleted.
				 */
				def scriptAllocated = ScriptGroup.where {
					scriptList { id == scriptFile.id } && status == Status.ALLOCATED.toString()
				}
				scriptAllocated.each{
					isAllocatedScriptGrp = true
					return true
				}
				if(isAllocatedScriptGrp){
					scriptInUse = true
				}
				else{
					/**
					 * Selecting ScriptGroups where the given script is present
					 */
					def scriptGroups = ScriptGroup.where {
						scriptList { id == scriptFile.id }
					}
					def scriptInstance
					scriptGroups?.each{ scriptGrp ->
						ScriptGroup.withTransaction {
							scriptInstance = scriptGrp?.scriptList?.find { it?.id == scriptFile?.id }
							if(scriptInstance){
								scriptGrp.removeFromScriptList(scriptInstance)
							}

							def scriptInstanceList = scriptGrp?.scriptList?.findAll { it?.id == scriptFile?.id }
							if(scriptInstanceList?.size() > 0){
								if(scriptInstance){
									scriptGrp?.scriptList?.removeAll(scriptInstance);
								}
							}
						}
					}
				}
			}
		} catch (Exception e) {
		}
		return scriptInUse
	}

	/**
	 * Get the list of scripts based on the scriptName, primitiveTest and selected box types.
	 * @param searchName
	 * @param primtest
	 * @param selboxTypes
	 * @return
	 */
	public List getAdvancedSearchResult(final String searchName, final String primtest, final String selboxTypes){
		def scriptList
		def boxTypeObjList = []
		PrimitiveTest ptest
		if((!searchName)){
			if((primtest) && (!selboxTypes)){
				scriptList = Script.findAll("from Script as b where b.primitiveTest='${primtest}'")
			}
			else if((!primtest) && (selboxTypes)){
				boxTypeObjList = getBoxTypes(selboxTypes)
				scriptList = Script.createCriteria().list {
					boxTypes{
						'in'('id',boxTypeObjList)
					}
				}
			}
			else{
				boxTypeObjList = getBoxTypes(selboxTypes)
				ptest = PrimitiveTest.findById(primtest)
				scriptList = Script.createCriteria().list {
					boxTypes{
						'in'('id',boxTypeObjList)
					}
					eq('primitiveTest', ptest)
				}
			}
		}
		else if((!primtest)){
			if((searchName) && (!selboxTypes)){
				scriptList = Script.findAll("from Script as b where b.name like '%${searchName}%'")
			}
			else if((!searchName) && (selboxTypes)){
				boxTypeObjList = getBoxTypes(selboxTypes)
				scriptList = Script.createCriteria().list {
					boxTypes{
						'in'('id',boxTypeObjList)
					}
				}
			}
			else{
				boxTypeObjList = getBoxTypes(selboxTypes)
				scriptList = Script.createCriteria().list {
					boxTypes{
						'in'('id',boxTypeObjList)
					}
					ilike("name", "%${searchName}%")
				}
			}
		}
		else if((!selboxTypes)){
			if((searchName) && (!primtest)){
				scriptList = Script.findAll("from Script as b where b.name like '%${searchName}%'")
			}
			else if((!searchName) && (primtest)){
				scriptList = Script.findAll("from Script as b where b.primitiveTest='${primtest}'")
			}
			else{
				scriptList = Script.findAll("from Script as b where b.name like '%${searchName}%' and primitiveTest='${primtest}'")
			}
		}
		else{
			boxTypeObjList = getBoxTypes(selboxTypes)
			ptest = PrimitiveTest.findById(primtest)
			scriptList = Script.createCriteria().list {
				boxTypes{
					'in'('id',boxTypeObjList)
				}
				eq('primitiveTest', ptest)
				ilike("name", "%${searchName}%")
			}
		}
		scriptList.unique()
		return scriptList
	}

	/**
	 * Method to get the id of boxtypes in a list
	 * @param selboxTypes
	 * @return
	 */
	def getBoxTypes(final def selboxTypes){
		def boxTypesList = []
		BoxType bt
		boxTypesList = createBoxTypeList(selboxTypes)
		def boxTypeObjList = []
		boxTypesList.each{
			bt = BoxType.findById(it)
			boxTypeObjList.add( bt?.id )
		}
		return boxTypeObjList
	}

	def removeScriptsFromSuites(final ScriptFile scriptInstance, final String sgName){

		int flag = 0

		def scriptGrpInstance = ScriptGroup.findByName(sgName)
		if(scriptGrpInstance){
			if(scriptInstance){

				scriptGrpInstance.scriptList.each { script ->
					if(script?.scriptName == scriptInstance?.scriptName){
						flag = 1
					}
				}

				if(flag == 1){
					scriptGrpInstance.removeFromScriptList(scriptInstance)
				}

				//					if(sg.scriptsList.contains(scriptInstance)){
				//						sg.removeFromScriptsList(scriptInstance)
				//					}

			}else{
				Thread.dumpStack()
			}
		}

	}
	def removeScriptFromScriptGroup(final ScriptFile scriptInstance, final String sgName){

		def scriptGrpInstance = ScriptGroup.findByName(sgName)
		if(scriptGrpInstance){
			if(scriptInstance){
				if(scriptGrpInstance.scriptList.contains(scriptInstance)){
					scriptGrpInstance.removeFromScriptList(scriptInstance)
				}
			}
		}

	}

	def removeFromScriptList(def final vers , def final bType , def final scriptInstance){
		def groupNames  = [
			bType?.name + KEY_GROUP,bType?.name + KEY_GROUP+ "_LD",
			vers?.toString()+"_"+bType?.name,
			vers?.toString()+"_"+bType?.name+Constants.NO_OS_SUITE,
			vers?.toString()+"_"+bType?.name+"_LD"
		]
		groupNames.each {  groupName ->
			def scriptGrpInstance = ScriptGroup.findByName(groupName)
			if(scriptGrpInstance && scriptGrpInstance?.scriptList?.contains(scriptInstance)){
				scriptGrpInstance.removeFromScriptList(scriptInstance)
			}
		}
	}

	def removeFromScriptTagList(def final scriptTag , def final bType , def final scriptInstance, def final category){
		def groupNames  = [
			scriptTag?.toString()+"SUITE_"+bType?.name,
		]
		groupNames.each {  groupName ->
			def scriptGrpInstance = ScriptGroup.findByName(groupName)
			if(scriptGrpInstance && scriptGrpInstance?.scriptList?.contains(scriptInstance)){
				scriptGrpInstance.removeFromScriptList(scriptInstance)
			}
		}
	}

	def updateScriptsFromRDKVersionBoxTypeTestGroup(final def scriptInstance,final ScriptObject sObject , final def oldRDKVersions, final def oldBoxTypes){
		def time1 = System.currentTimeMillis()
		try {
			def bTypeList = BoxType.findAll()
			def rdkVersionList = RDKVersions?.findAll()

			def bTypes = sObject?.getBoxTypes()
			def versions = sObject?.getRdkVersions()
			oldBoxTypes?.each { bt ->
				oldRDKVersions?.each { ver ->
					if(!bTypes?.contains(bt) || !versions?.contains(ver)){
						removeFromScriptList(ver, bt, scriptInstance)
					}
				}
			}

			sObject?.getBoxTypes()?.each{ bType ->

				sObject?.getRdkVersions()?.each{ vers ->

					Module module
					Module.withTransaction{
						module = Module.findByName(sObject?.module)
					}

					def names = []
					if(!sObject?.getLongDuration()){
						names.add(vers?.toString()+"_"+bType?.name)
						if(module?.testGroup != TestGroup.OpenSource){
							names.add(vers?.toString()+"_"+bType?.name+Constants.NO_OS_SUITE)
						}
					}else{
						names.add(vers?.toString()+"_"+bType?.name+"_LD")
					}

					names.each {  name ->
						def scriptGrpInstance = ScriptGroup.findByName(name)
						if(!scriptGrpInstance){
							scriptGrpInstance = new ScriptGroup()
							scriptGrpInstance.name = name
							scriptGrpInstance.save()
						}
						if(scriptGrpInstance && !scriptGrpInstance?.scriptList?.contains(scriptInstance)){
							scriptGrpInstance.addToScriptList(scriptInstance)
						}
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}


	def updateScriptsFromScriptTag(final def scriptInstance,final ScriptObject sObject , final def oldTags ,final def oldBoxTypes , final def category  ){
		
		def time1 = System.currentTimeMillis()
		try {
			def bTypeList = BoxType.findAllByCategory(category)
			def rdkVersionList = RDKVersions?.findAllByCategory(category)

			def bTypes = sObject?.getBoxTypes()
			def tags = sObject?.getScriptTags()
			oldBoxTypes?.each { bt ->
				oldTags?.each { tag ->
					if(!bTypes?.contains(bt) || !tags?.contains(tag)){
						removeFromScriptTagList(tag, bt, scriptInstance, category)
					}
				}
			}

			sObject?.getBoxTypes()?.each{ bType ->

				sObject?.getScriptTags()?.each{ tag ->

					Module module
					Module.withTransaction{
						module = Module.findByNameAndCategory(sObject?.module,category)
					}

					def names = []
					names.add(tag?.toString()+"SUITE_"+bType?.name)

					names.each {  name ->
						def scriptGrpInstance = ScriptGroup.findByNameAndCategory(name,category)
						if(!scriptGrpInstance){
							scriptGrpInstance = new ScriptGroup()
							scriptGrpInstance.name = name
							scriptGrpInstance?.category = category
							scriptGrpInstance.save()
						}
						if(scriptGrpInstance && !scriptGrpInstance?.scriptList?.contains(scriptInstance)){
							scriptGrpInstance.addToScriptList(scriptInstance)
						}
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
}
