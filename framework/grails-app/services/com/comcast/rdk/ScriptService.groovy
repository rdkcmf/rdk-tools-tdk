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
import static Constants.*
import java.io.File;
import java.util.List;
import com.comcast.rdk.Category
import org.springframework.util.CollectionUtils
import org.springframework.util.StringUtils


/**
 * Service class to manage the script files in file store.
 *
 */
class ScriptService {

	public static volatile List scriptsList = []

	public static volatile List scriptNameList = []

	public static volatile Map scriptMapping = [:]

	public static volatile Map scriptGroupMap = [:]

	//public static volatile Set scriptSet = []

	public static volatile List scriptLockList = []


	public static volatile Map scriptsListMap = [:]

	public static volatile Map scriptNameListMap = [:]

	public static volatile Map scriptsListAdvanced = [:]

	//public static volatile Map scriptGroupMapB = [:]

	//public static volatile List scriptLockListB = []

	public static volatile List tclScriptsList = []

	public static volatile List tclNameList = []

	public static volatile Map combinedTclScriptMap = [:]

	public static volatile List testProfileSuite = []

	public static volatile List totalTclScriptList = []

	public static volatile Map newTestCaseMap  = [:]
	def primitiveService

	def scriptgroupService

	def grailsApplication

	def updateScript(def script){
		scriptsList.add(script)
		scriptNameList.add(script?.scriptName)
		def list = scriptGroupMap.get(script?.moduleName)
		if(list == null){
			list = []
			scriptGroupMap.put(script?.moduleName,list)

		}
		list.add(script?.scriptName)

		scriptMapping.put(script?.scriptName,script?.moduleName)
	}

	def updateScript(def script, def category){
		scriptsListMap.get(category)?.add(script)
		scriptNameListMap.get(category)?.add(script?.scriptName)
		def list = scriptGroupMap.get(script?.moduleName)
		if(list == null){
			list = []
			scriptGroupMap.put(script?.moduleName,list)
		}
		list.add(script?.scriptName)
		if(category?.toString().equals("RDKB_TCL")){
			def scriptFile
			ScriptFile.withTransaction {
				scriptFile  = ScriptFile.findByScriptNameAndCategory(script?.scriptName, Category.RDKB_TCL)
				if(scriptFile == null) {
					scriptFile = new ScriptFile(scriptName:script?.scriptName, category:Category.RDKB_TCL,moduleName:"tcl" )
					scriptFile.save()
				}
			}
			tclNameList.add(script?.scriptName)
			tclScriptsList.add(scriptFile)
		}
		scriptMapping.put(script?.scriptName,script?.moduleName)
	}

	def updateScriptNameChange(def oldName , def newScript){
		scriptNameList.add(oldName)
		scriptNameList.add(newScript?.scriptName)
		boolean removedOld = false
		Iterator<ScriptFile> iter = scriptsList.iterator()
		while(iter.hasNext()){
			def obj = iter.next()
			if(oldName.equals(obj.scriptName)){
				iter.remove()
				removedOld = true
			}
		}

		if(removedOld){
			scriptsList.add(newScript)
		}
		def list = scriptGroupMap.get(newScript?.moduleName)
		if(list == null){
			list = []
			scriptGroupMap.put(newScript?.moduleName,list)
		}
		list.remove(oldName)
		list.add(newScript?.scriptName)
		scriptMapping.remove(oldName)
		scriptMapping.put(newScript?.scriptName,newScript?.moduleName)
	}
	def updateScriptNameChange(def oldName , def newScript, def category){
		def scriptnamelist =  scriptNameListMap.get(category)
		scriptnamelist.add(newScript?.scriptName)
		scriptnamelist.remove(oldName)
		boolean removedOld = false
		Iterator<ScriptFile> iter = scriptsListMap.get(category)?.iterator()
		while(iter.hasNext()){
			def obj = iter.next()
			if(oldName.equals(obj.scriptName)){
				iter.remove()
				removedOld = true
			}
		}

		if(removedOld){
			scriptsListMap.get(category)?.add(newScript)
		}
		def list = scriptGroupMap.get(newScript?.moduleName)
		if(list == null){
			list = []
			scriptGroupMap.put(newScript?.moduleName,list)
		}
		list.remove(oldName)
		list.add(newScript?.scriptName)
		scriptMapping.remove(oldName)
		scriptMapping.put(newScript?.scriptName,newScript?.moduleName)
	}

	def deleteScript(def script){
		scriptsList.remove(script)
		scriptNameList.remove(script?.scriptName)
		def list = scriptGroupMap.get(script?.moduleName)
		if(list != null){
			list.remove(script?.scriptName)
		}
		scriptMapping.remove(script?.scriptName?.toString().trim())
	}

	def deleteScript(def script, def category){
		def scriptslist = scriptsListMap.get(category)
		if(!CollectionUtils.isEmpty(scriptslist)){
			scriptslist.remove(script)
		}
		def scriptNamelist = scriptNameListMap.get(category)
		if(!CollectionUtils.isEmpty(scriptNamelist)){
			scriptNamelist.remove(script?.scriptName)
		}
		def list = scriptGroupMap.get(script?.moduleName)
		if(!CollectionUtils.isEmpty(list)){
			list.remove(script?.scriptName)
		}
		if(category?.toString()?.equals("RDKB_TCL")){
			def scriptFile  = ScriptFile.findByScriptNameAndCategory(script?.scriptName, Category.RDKB_TCL)
			tclNameList.remove(script?.scriptName)
			tclScriptsList.remove(scriptFile)
		}
		scriptMapping.remove(script?.scriptName?.toString().trim())
	}

	def initializeScriptsData(def realPath){
		try {
			def list1 = scriptsList.collect()
			def scriptFileList = ScriptFile?.findAll()
			scriptsList.clear()
			List scriptList = []

			boolean updateReqd = isDefaultSGUpdateRequired(realPath)

			List dirList = [Constants.COMPONENT, Constants.INTEGRATION]
			def start = System.currentTimeMillis()
			[Constants.TESTSCRIPTS_RDKV, Constants.TESTSCRIPTS_RDKB, Constants.TESTSCRIPTS_RDKV_ADV, Constants.TESTSCRIPTS_RDKB_ADV].each{ fileStorePath ->
				dirList.each{ directory ->
					File scriptsDir = new File( "${realPath}//fileStore//$fileStorePath//"+directory+"//")
					if(scriptsDir.exists()){
						def modules = scriptsDir.listFiles()


						//Arrays.sort(modules);

						modules.each { module ->
							def category = null
							if(Constants.TESTSCRIPTS_RDKV.equals(fileStorePath) || Constants.TESTSCRIPTS_RDKV_ADV.equals(fileStorePath)){
								category = Constants.RDKV
							}else if(Constants.TESTSCRIPTS_RDKB.equals(fileStorePath) || Constants.TESTSCRIPTS_RDKB_ADV.equals(fileStorePath)){
								category = Constants.RDKB
							}
							initialize( module, updateReqd, realPath, category,fileStorePath)
						}
					}


				}
			}
			//removeOrphanScriptFile(realPath,scriptFileList, scriptsList)
			initializeTCLScripts("${realPath}//fileStore//"+FileStorePath.RDKTCL.value())
			//removeOrphanScriptFile(realPath,scriptFileList, scriptsListMap) // debug needed
		} catch (Exception e) {
			e.printStackTrace()
		}

		return scriptsList
	}

	private void initialize(def module, def updateReqd, def realPath, def category,def fileStorePath){

		def start1 =System.currentTimeMillis()
		try {
			File [] files = module.listFiles(new FilenameFilter() {
						@Override
						public boolean accept(File dir, String name) {
							return name.endsWith(".py");
						}
					});
			def start2 = System.currentTimeMillis()
			def sLst = []
			if(scriptGroupMap.keySet().contains(module?.getName())){
				sLst = scriptGroupMap.get(module?.getName())
			}
			files.each { file ->
				String name = ""+file?.name?.trim()?.replace(".py", "")
				def sFile
				ScriptFile.withTransaction {
					sFile = ScriptFile.findByScriptNameAndModuleName(name,module.getName())
					if(sFile == null){
						sFile = new ScriptFile()
						sFile.setModuleName(module?.getName())
						sFile.setScriptName(name)
					}
					sFile.category = Utility.getCategory(category)
					sFile.save(flush:true)
				}
				def scriptsListmap = scriptsListMap.get(category)
				if(scriptsListmap == null){
					scriptsListmap = []
					scriptsListMap.put(category, scriptsListmap)
				}
				if(!scriptsListmap.contains(sFile)){
					scriptsListmap.add(sFile)
					sLst.add(name)
					scriptMapping.put(name, module?.getName())
				}

				def scriptNameListmap = scriptNameListMap.get(category)
				if(scriptNameListmap == null){
					scriptNameListmap = []
					scriptNameListMap.put(category, scriptNameListmap)
				}

				scriptsListAdvanced.put(sFile?.id, fileStorePath)
				if(!scriptNameListmap.contains(name)){
					scriptNameListmap.add(name)
				}
				/*if(!scriptsList.contains(sFile)){
				 scriptsList.add(sFile)
				 sLst.add(name)
				 scriptMapping.put(name, module?.getName())
				 }*/

				/*if(!scriptNameList.contains(name)){
				 scriptNameList.add(name)
				 }*/

				if(updateReqd == true){
					updateDefaultScriptGroups(realPath,name,module?.getName(), category)
					//updateSuiteWithTestProfileScripts(realPath,name,module?.getName(), category)
				}
			}
			sLst?.sort()

			scriptGroupMap.put(module?.getName(), sLst)
		} catch (Exception e) {
			println " Error "+e.getMessage()
			e.printStackTrace()
		}

	}

	def removeOrphanScriptFile(String realPath,List oldList , Map newListMap){
		def rdkBlist = newListMap.get('RDKB')
		rdkBlist = rdkBlist?rdkBlist:[]
		def rdkVlist = newListMap.get('RDKV')
		rdkVlist = rdkVlist?rdkVlist:[]
		oldList.removeAll(rdkVlist)
		oldList.removeAll(rdkBlist)
		oldList.removeAll(tclScriptsList)
		int indx = 0;
		List deleteFiles = []
		Map sgMap = [:]
		oldList?.each { scriptFile ->
			def file = null
			if(scriptFile?.category != Category.RDKB_TCL){
				file = getScriptFileObj(realPath, scriptFile?.moduleName,scriptFile?.scriptName, scriptFile?.category)
			}
			else{
				def filePath = Utility.getTclFilePath(realPath, scriptFile?.scriptName)
				if(filePath){
					file = new File(filePath)
				}
			}
			if(file == null){
				indx ++
				def scriptGroups = ScriptGroup.where {
					scriptList { id == scriptFile.id }
				}

				def scriptInstance
				def sgId = []
				boolean flag = false
				scriptGroups?.each{ scriptGrp ->
					flag = true
					def sList = sgMap.get(scriptGrp?.name)
					if(sList == null){
						sList = []
						sgMap.put(scriptGrp?.name,sList)
					}
					sList.add(scriptFile)
				}
				if(!flag){
					deleteFiles.add(scriptFile?.id)
				}
			}
		}


		sgMap?.keySet().each { sname ->
			try {
				ScriptGroup.withTransaction {
					ScriptGroup sGroup = ScriptGroup.findByName(sname)
					if(sGroup){
						List sList = sgMap.get(sname)
						//						if(sList?.size() <= 7){
						//							println " SG<<>><<> "+sname
						//						sList?.each{ scriptInstance ->
						//							sGroup.removeFromScriptList(scriptInstance)
						//							sGroup?.scriptList?.removeAll(sList);
						//							sGroup?.save(flush:true)
						//						}
						//						}
					}
				}
			} catch (Exception e) {
				e.printStackTrace()
			}
		}

		deleteFiles?.each { sFileId ->
			ScriptFile.withTransaction {
				def sFile = ScriptFile.get(sFileId)
				if(sFile){
					sFile.delete()
				}
			}
		}
	}



	def removeFromSG(def sid , def scriptFile){
		def  scriptInstance
		ScriptGroup.withTransaction {
			ScriptGroup sGroup = ScriptGroup.get(sid)
			scriptInstance = sGroup?.scriptList?.find { it?.id == scriptFile?.id }
			if(scriptInstance){
				sGroup.removeFromScriptList(scriptInstance)
				sGroup.save(flush:true)
			}

			def scriptInstanceList = sGroup?.scriptList?.findAll { it?.id == scriptFile?.id }
			if(scriptInstanceList?.size() > 0){
				if(scriptInstance){
					sGroup?.scriptList?.removeAll(scriptInstance);
				}
			}
		}
	}
	def updateDefaultScriptGroups(def realPath, def name , def moduleName, category){
		try {
			def sFile
			ScriptFile.withTransaction{
				sFile= ScriptFile.findByScriptNameAndModuleName(name,moduleName)
			}
			if(sFile){
				def script = getMinimalScript(realPath,moduleName, name, category)
				if(script){
					def sObject = new ScriptObject()
					sObject.setBoxTypes(script?.boxTypes?.toSet())
					sObject.setRdkVersions(script?.rdkVersions.toSet())
					sObject.setName(name)
					sObject.setModule(moduleName)
					sObject.setScriptFile(sFile)
					sObject.setScriptTags(script?.scriptTags?.toSet())
					sObject.setLongDuration(script?.longDuration)
					ScriptGroup.withTransaction{
						scriptgroupService.saveToScriptGroups(sFile,sObject, category)
						scriptgroupService.saveToDefaultGroups(sFile,sObject, script?.boxTypes, category)
					}
					createDefaultGroupWithoutOS(sObject,sFile, category)
					scriptgroupService.updateScriptsFromScriptTag(sFile,sObject,[],[], category)
					updateSuiteWithTestProfileScript(sObject,sFile, category)
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}


	/**
	 * Method to update all the system created Test suites for the metnioned script if reqd.
	 */
	def updateDefaultScriptGroupsList(def realPath, def name , def moduleName, category){
		try {
			def sFile
			sFile= ScriptFile.findByScriptNameAndModuleName(name,moduleName)
			if(sFile){
				def script = getMinimalScript(realPath,moduleName, name, category)
				if(script){
					def sObject = new ScriptObject()
					sObject.setBoxTypes(script?.boxTypes?.toSet())
					sObject.setRdkVersions(script?.rdkVersions.toSet())
					sObject.setName(name)
					sObject.setModule(moduleName)
					sObject.setScriptFile(sFile)
					sObject.setScriptTags(script?.scriptTags?.toSet())
					sObject.setLongDuration(script?.longDuration)

					scriptgroupService.saveToScriptGroups(sFile,sObject, category)
					scriptgroupService.saveToDefaultGroups(sFile,sObject, script?.boxTypes, category)
					createDefaultGroupWithoutOS(sObject,sFile, category)
					scriptgroupService.updateScriptsFromScriptTag(sFile,sObject,[],[], category)
					updateSuiteWithTestProfileScript(sObject,sFile, category)
				}
			}
		} catch (Exception e) {
			println " ERROR "+e.getMessage()
			e.printStackTrace()
		}
	}
	/**
	 * Create suite with no open source script based on the box types and rdk_versions
	 * @param scriptObject
	 * @param scriptFile
	 * @param category
	 * @return
	 */

	def createDefaultGroupWithoutOS(def scriptObject , def scriptFile, def category){
		def sName = scriptObject.getModule()
		Module module
		Module.withTransaction{
			module = Module.findByName(sName)
		}
		if(module?.testGroup != TestGroup.OpenSource){
			scriptObject?.boxTypes?.each{ bType ->

				scriptObject?.rdkVersions?.each{ vers ->

					String name = vers?.toString()+"_"+bType?.name+Constants.NO_OS_SUITE
					ScriptGroup.withTransaction {
						def scriptGrpInstance = ScriptGroup.findByName(name)
						if(!scriptObject?.getLongDuration()){
							if(!scriptGrpInstance){
								scriptGrpInstance = new ScriptGroup()
								scriptGrpInstance.name = name
								scriptGrpInstance.category = Utility.getCategory(category)
								scriptGrpInstance.save(flush:true)
							}
							if(scriptGrpInstance && !scriptGrpInstance?.scriptList?.contains(scriptFile)){
								scriptGrpInstance.addToScriptList(scriptFile)
							}
						}else{
							if(scriptGrpInstance && scriptGrpInstance?.scriptList?.contains(scriptFile)){
								scriptGrpInstance.removeFromScriptList(scriptFile)
							}
						}
					}
					// For adding the emulator suite with out recording
					if(!(sName?.toString()?.equals("recorder")) && ( bType?.name.toString()?.equals("Emulator-HYB")|| bType?.name.toString()?.equals("Hybrid-1")) && vers?.toString()?.equals("RDK2.0")){
						String suiteName = vers?.toString()+"_"+bType?.name+Constants.NO_OS_SUITE+"_WOR"
						ScriptGroup.withTransaction {
							def scriptGrpInstance = ScriptGroup.findByName(suiteName)
							if(!scriptObject?.getLongDuration()){
								if(!scriptGrpInstance){
									scriptGrpInstance = new ScriptGroup()
									scriptGrpInstance.name = suiteName
									scriptGrpInstance.category = Utility.getCategory(category)
									scriptGrpInstance.save(flush:true)
								}
								if(scriptGrpInstance && !scriptGrpInstance?.scriptList?.contains(scriptFile)){
									scriptGrpInstance.addToScriptList(scriptFile)
								}
							}else{
								if(scriptGrpInstance && scriptGrpInstance?.scriptList?.contains(scriptFile)){
									scriptGrpInstance.removeFromScriptList(scriptFile)
								}
							}
						}
					}
				}
			}
		}
	}



	def createDefaultScriptTagGroup(def scriptObject , def scriptFile, def category){
		scriptObject?.boxTypes?.each{ bType ->

			scriptObject?.scriptTags?.each{ tag ->
				String name = tag?.toString()+"_"+bType?.name
				ScriptGroup.withTransaction {
					def scriptGrpInstance = ScriptGroup.findByName(name)
					if(!scriptGrpInstance){
						scriptGrpInstance = new ScriptGroup()
						scriptGrpInstance.name = name
						scriptGrpInstance.category = Utility.getCategory(category)
						scriptGrpInstance.save(flush:true)
					}
					if(scriptGrpInstance && !scriptGrpInstance?.scriptList?.contains(scriptFile)){
						scriptGrpInstance.addToScriptList(scriptFile)
					}
				}
			}
		}
	}

	private void initializeTCLScripts(final String path) {
		def tclPath = path?.trim()
		def tclFiles = new File(tclPath).listFiles(new FileFilter(){
					boolean accept(File file) {
						def fileName = file.name
						//return fileName.startsWith("TC") && fileName.endsWith(".tcl")
						if(!(fileName?.toString()?.equals("lib.tcl") || fileName?.toString()?.equals("proc.tcl"))){
							return fileName.endsWith(".tcl")
						}
					}
				})
		tclScriptsList = []
		tclNameList = []
		totalTclScriptList = []

		try{
			tclFiles.each { tclFile ->
				def fileName = tclFile.name.split(".tcl")[0]
				def scriptFile = null
				ScriptFile.withTransaction {
					scriptFile  = ScriptFile.findByScriptNameAndCategory(fileName, Category.RDKB_TCL)
					if(scriptFile == null) {
						def scriptFile1 = new ScriptFile()
						scriptFile1?.scriptName =fileName?.toString()
						scriptFile1?.category = Category.RDKB_TCL
						scriptFile1?.moduleName = "tcl"
						if(!(scriptFile1.save(flush:true))){
							println "Error "
						}
					}
				}
				def scriptName =ScriptFile.findByScriptNameAndCategory(fileName, Category.RDKB_TCL)
				def cmdTclScriptListFinal  = []
				if(scriptName){
					try{
						tclScriptsList.add(scriptName)
						if(scriptName?.toString()?.contains("_to_")){
							def splitScriptName = scriptName?.toString()?.split("_to_")
							if(splitScriptName?.size() > 1){
								def firstScriptName = splitScriptName[0]
								def lastScriptName = splitScriptName[1]
								def firstScriptNameSplit=  firstScriptName.split("_")
								int firstTestCaseId = Integer.parseInt(firstScriptNameSplit.last())
								def lastScriptNameSplit=  lastScriptName.split("_")
								int lastTestCaseId =Integer.parseInt(lastScriptNameSplit.last())
								def script
								int i
								def cmdTclScriptList = []
								for(i = firstTestCaseId ; i <= lastTestCaseId ; i++){
									script = firstScriptNameSplit[0]+"_"+firstScriptNameSplit[1]+"_0"+firstTestCaseId
									cmdTclScriptList.add(script)
									cmdTclScriptListFinal.add(script)
									firstTestCaseId++
								}
								combinedTclScriptMap.put(scriptName,cmdTclScriptList)
							}
						}
						else{
							totalTclScriptList.add(scriptName)
						}
						cmdTclScriptListFinal?.each{
							def scriptFile1 = ScriptFile.findByScriptNameAndCategory(it, Category.RDKB_TCL)
							def scriptFile2
							if(!scriptFile1){
								scriptFile2 = new ScriptFile()
								scriptFile2?.scriptName =it?.toString()
								scriptFile2?.category = Category.RDKB_TCL
								scriptFile2?.moduleName = "tcl"
								if(!(scriptFile2?.save(flush:true))){
									println "Error "
								}else{
									totalTclScriptList.add(scriptFile2)
								}
							}else{
								totalTclScriptList.add(scriptFile1)
							}
						}
					}catch(Exception e){
						println " ERROR "+ e.getMessage()
						e.printStackTrace()
					}
				}
				def realPath = path?.replace(FileStorePath.RDKTCL.value(),"")
				realPath=realPath?.replace("fileStore//","")
				if(realPath){
					boolean updateReqd = isDefaultSGUpdateRequired(realPath)
					if(updateReqd ){
						updateTclScriptSuite(scriptName ,"RDKB_TCL")
					}
				}
				tclNameList.add(fileName)
			}
		}catch(Exception e){
			println e?.getMessage()
		}
	}


	/**
	 * get Total TCL script List
	 */
	def getTotalTCLScriptList(def realPath){
		if(totalTclScriptList == null || totalTclScriptList.isEmpty()){
			initializeTCLScripts("${realPath}//fileStore//"+FileStorePath.RDKTCL.value())
		}
		return totalTclScriptList
	}



	/**
	 * Updating TCL script suite, when script.config value set as true
	 * @param scriptFileInstance
	 * @param category
	 * @return
	 */
	def updateTclScriptSuite(def ScriptFile scriptFileInstance , def String category){
		try{
			def moduleName =  "TCL_SCRIPTS"
			def cmdTclScriptListFinal
			def scriptGrpInstance = ScriptGroup.findByName(moduleName)
			if(!scriptGrpInstance){
				scriptGrpInstance = new ScriptGroup()
				scriptGrpInstance.name = moduleName
				scriptGrpInstance.scriptList = []
				scriptGrpInstance.category = Utility.getCategory(category)
				scriptGrpInstance.save()
			}

			if(scriptFileInstance?.toString()?.contains("_to_")){
				def splitScriptName = scriptFileInstance?.toString()?.split("_to_")
				if(splitScriptName?.size() > 1){
					def firstScriptName = splitScriptName[0]
					def lastScriptName = splitScriptName[1]
					def firstScriptNameSplit =  firstScriptName.split("_")
					int firstTestCaseId = Integer.parseInt(firstScriptNameSplit.last())
					def lastScriptNameSplit=  lastScriptName.split("_")
					int lastTestCaseId =Integer.parseInt(lastScriptNameSplit.last())
					def script
					int i
					def cmdTclScriptList = []
					for(i = firstTestCaseId ; i <= lastTestCaseId ; i++){
						script = firstScriptNameSplit[0]+"_"+firstScriptNameSplit[1]+"_0"+firstTestCaseId
						def scriptFile1 = ScriptFile.findByScriptNameAndCategory(script, Category.RDKB_TCL)

						if(!scriptFile1){
							scriptFile1 = new ScriptFile()
							scriptFile1?.scriptName =it?.toString()
							scriptFile1?.category = Category.RDKB_TCL
							scriptFile1?.moduleName = "tcl"
							if(!(scriptFile1?.save(flush:true))){

							}
						}
						if(!scriptGrpInstance?.scriptList?.contains(scriptFile1 )){
							scriptGrpInstance.addToScriptList(scriptFile1 )
						}
						firstTestCaseId++
					}

				}
			}
			else{
				if(!scriptGrpInstance?.scriptList?.contains(scriptFileInstance)){
					scriptGrpInstance.addToScriptList(scriptFileInstance)
				}
			}
		}catch(Exception e){
			println " Error "+ e.printStackTrace()
		}
	}

	def getTCLNameList(def path){
		if(tclNameList== null || tclNameList.isEmpty()){
			initializeTCLScripts("${path}//fileStore//"+FileStorePath.RDKTCL.value())
		}
		return tclNameList
	}


	def getScriptNameFileList(def realPath){
		if(scriptsList == null || scriptsList.size() == 0){
			initializeScriptsData(realPath)
		}
		return scriptsList
	}

	def getScriptNameFileList(def realPath, def category){
		if(scriptsListMap == null || scriptsListMap.size() == 0){
			initializeScriptsData(realPath)
		}
		return scriptsListMap.get(category)
	}

	def getScriptNameModuleNameMapping(def realPath){
		/*if(scriptMapping == null || scriptMapping.keySet().size() == 0){
		 initializeScriptsData(realPath)
		 }*/
		if(scriptMapping == null || scriptMapping.keySet().size() == 0){
			initializeScriptsData(realPath)
		}
		return scriptMapping
	}


	def Map getScriptsMap(def realPath){
		if(scriptGroupMap == null || scriptGroupMap.keySet().size() == 0){
			initializeScriptsData(realPath)
		}
		return scriptGroupMap
	}

	def Map getScriptsMap(def realPath, def category){
		getScriptsMap(realPath)
		def map = [:]
		map = getCategoryMap(realPath, category)
		return map
	}

	def getCategoryMap(def realPath, def category){
		def dir = []
		if("RDKV".equals(category)){
			def directories = ["testscriptsRDKV", "testscriptsRDKVAdvanced"]
			directories.each { dirName ->
				def path  = realPath+Constants.FILE_SEPARATOR+"fileStore"+Constants.FILE_SEPARATOR+dirName
				["component", "integration"].each{ directory ->
					dir.addAll(getDirectoryList(path+Constants.FILE_SEPARATOR+directory))
				}
			}
		}
		else if("RDKB".equals(category)){
			def directories = ["testscriptsRDKB", "testscriptsRDKBAdvanced"]
			directories.each { dirName ->
				def path = realPath+Constants.FILE_SEPARATOR+"fileStore"+Constants.FILE_SEPARATOR+dirName
				["component", "integration"].each{ directory ->
					dir.addAll(getDirectoryList(path+Constants.FILE_SEPARATOR+directory))
				}
			}
		}
		def map = [:]
		dir.each{
			map.put(it, scriptGroupMap.get(it))
		}
		map
	}

	def getDirectoryList(def path){
		File f = new File(path)
		def dirs = []
		if(f.exists() && f.isDirectory()){
			def directories = f.listFiles(new FilenameFilter(){
						boolean accept(File dir, String name){
							dir.isDirectory()
						}
					})
			directories.each{ it ->
				dirs << it.name
			}
		}
		return dirs
	}

	def getScriptNameList(def realPath){
		if(scriptNameList == null || scriptNameList.size() == 0){
			initializeScriptsData(realPath)
		}
		return scriptNameList
	}

	def getScriptNameList(def realPath, def category){
		if(StringUtils.hasText(category) ){
			if(scriptNameListMap == null || scriptNameListMap.size() == 0){
				initializeScriptsData(realPath)
			}
			return scriptNameListMap.get(category)
		}
		def list = []
		scriptNameListMap.each{ key, value ->
			list.addAll(value)
		}
		return list
	}


	def getScriptFileObj(realPath,dirName,fileName, def category){
		dirName = dirName?.trim()
		fileName = fileName?.trim()
		Map script = [:]
		try {

			def moduleObj = Module.findByName(dirName)
			def scriptDirName = Constants.COMPONENT
			if(moduleObj){
				if(moduleObj?.testGroup?.groupValue.equals(TestGroup.E2E.groupValue)){
					scriptDirName = Constants.INTEGRATION
				}
			}
			/*def path = realPath + FILE_SEPARATOR + "fileStore"
			 if(category == Category.RDKV){
			 path = path + FILE_SEPARATOR + FileStorePath.RDKV.value() + FILE_SEPARATOR +  scriptDirName + FILE_SEPARATOR + dirName + FILE_SEPARATOR +fileName+".py";
			 }
			 else if (category == Category.RDKB){
			 path = path + FILE_SEPARATOR + FileStorePath.RDKB.value() + FILE_SEPARATOR + scriptDirName + FILE_SEPARATOR + dirName + FILE_SEPARATOR + fileName+".py";
			 }else{
			 path = path + FILE_SEPARATOR + FileStorePath.RDKTCL.value() + FILE_SEPARATOR + scriptDirName + FILE_SEPARATOR + dirName + FILE_SEPARATOR + fileName+".tcl";
			 }*/
			//File file = new File( "${realPath}//fileStore//testscripts//"+scriptDirName+"//"+dirName+"//"+fileName+".py");
			def path = getFileFromPath( realPath, scriptDirName, dirName,  fileName,  category)
			File file = new File(path)

			if(file.exists()){
				return file;
			}else{
				println " File Not present "+file?.getName()
			}
		} catch (Exception e) {
			script = null
			e.printStackTrace()
		}
		return null;
	}
	def getScript(realPath,dirName,fileName, category){
		dirName = dirName?.trim()
		fileName = fileName?.trim()
		Map script = [:]
		try {

			def moduleObj = Module.findByName(dirName)
			if(moduleObj == null) {
				return script
			}
			def scriptDirName = Constants.COMPONENT
			if(moduleObj){
				if(moduleObj?.testGroup?.groupValue.equals(TestGroup.E2E.groupValue)){
					scriptDirName = Constants.INTEGRATION
				}
			}
			if(category == null){
				if(moduleObj){
					category = moduleObj?.category?.toString()
				}
			}
			File file = null
			/*if("RDKV".equals(category)){
			 //file = new File( "${realPath}//fileStore//testscriptsRDKV//"+scriptDirName+"//"+dirName+"//"+fileName+".py");
			 }
			 if("RDKB".equals(category)){
			 //file = new File( "${realPath}//fileStore//testscriptsRDKB//"+scriptDirName+"//"+dirName+"//"+fileName+".py");
			 }*/
			def filename = getFileFromPath(realPath, scriptDirName, dirName, fileName, Utility.getCategory(category))
			file = new File(filename)

			if(file.exists()){
				String s = ""
				List line = file.readLines()
				//int indx = 0
				int indx = line?.findIndexOf {  it.startsWith("'''")}
				String scriptContent = ""
				if(line.get(indx).startsWith("'''"))	{
					indx++
					while(indx < line.size() &&  !line.get(indx).startsWith("'''")){
						s = s + line.get(indx)+"\n"
						indx++
					}
					indx ++
					while(indx < line.size()){
						scriptContent = scriptContent + line.get(indx)+"\n"
						indx++
					}
				}


				String xml = s
				XmlParser parser = new XmlParser();
				def node = parser.parseText(xml)
				script.put("id", node.id.text())
				script.put("version", getIntegerValue(node.version.text()))
				script.put("name", node.name.text())
				def grpObj = null
				def grps = node?.groups_id?.text()
				if(grps){
					try {
						grpObj = Groups.findById(Integer.parseInt(grps))
					} catch (Exception e) {
						//						e.printStackTrace()
					}
				}
				script.put("groups",grpObj)
				script.put("skip", getBooleanValue(node.skip.text()))
				script.put("remarks",node?.remarks?.text())
				script.put("longDuration", getBooleanValue(node.long_duration.text()))
				boolean adv = getBooleanValue(node.advanced_script.text())
				if(!adv){
					adv = Utility.isAdvancedScript(fileName, dirName)
				}
				script.put("advScript",adv)

				def nodePrimitiveTestName = node.primitive_test_name.text()
				def primitiveMap = primitiveService.getPrimitiveModuleMap(realPath)
				def moduleName1 = primitiveMap.get(nodePrimitiveTestName)
				def moduleObj1 = Module.findByName(dirName)
				def primitiveDirName = Constants.COMPONENT
				if(moduleObj){
					if(moduleObj?.testGroup?.groupValue.equals(TestGroup.E2E.groupValue)){
						primitiveDirName = Constants.INTEGRATION
					}
				}

				def primitiveTest = null

				def directoryName = primitiveService.getDirectoryName(nodePrimitiveTestName)

				if("RDKV".equals(category) || "RDKB".equals(category)){
					primitiveTest = primitiveService.getPrimitiveTest(realPath+"/fileStore/"+directoryName+"//"+primitiveDirName+"//"+moduleName1+"/"+moduleName1+".xml",nodePrimitiveTestName)
				}

				script.put("primitiveTest",primitiveTest)
				def versList = []
				def sTagList = []
				def btList = []
				def testProfileList =[]
				Set btSet = node?.box_types?.box_type?.collect{ it.text() }
				Set versionSet = node?.rdk_versions?.rdk_version?.collect{ it.text() }
				Set scriptTagSet = node?.script_tags?.script_tag?.collect{ it.text() }
				Set testProfileSet =  node?.test_profiles?.test_profile?.collect{ it.text() }


				btSet.each { bt ->
					btList.add(BoxType.findByNameAndCategory(bt, category))
				}
				versionSet.each { ver ->
					versList.add(RDKVersions.findByBuildVersionAndCategory(ver, category))
				}
				scriptTagSet?.each { tag ->
					sTagList.add(ScriptTag.findByName(tag))
				}
				testProfileSet?.each{ tProfile ->
					testProfileList?.add(TestProfile?.findByName(tProfile))
				}

				script.put("rdkVersions", versList)
				script.put("scriptTags", sTagList)
				script.put("boxTypes", btList)
				def statusText = node?.status?.text()
				script.put("status",getStatus(statusText) )
				script.put("synopsis", node?.synopsis?.text())
				script.put("scriptContent", scriptContent)
				script.put("executionTime", getExecutionTime(node?.execution_time?.text()))
				script.put("category", category)
				script.put("testProfile",testProfileList)
				def testCaseDeatilsMap =[:]
				if(node?.test_cases){
					testCaseDeatilsMap?.put(T_C_ID,node?.test_cases?.test_case_id?.text())
					testCaseDeatilsMap?.put(T_C_OBJ,node?.test_cases?.test_objective?.text())
					testCaseDeatilsMap?.put(T_C_TYPE,node?.test_cases?.test_type?.text())
					testCaseDeatilsMap?.put(T_C_SETUP,node?.test_cases?.test_setup?.text())
					//testCaseDeatilsMap?.put(T_C_STREAM_ID,node?.test_cases?.steam_id?.text())
					testCaseDeatilsMap?.put(T_C_SKIP,node?.test_cases?.skipped?.text())
					testCaseDeatilsMap?.put(T_C_PRE_REQUISITES, node?.test_cases?.pre_requisite?.text())
					testCaseDeatilsMap?.put(T_C_INTERFACE,node?.test_cases?.api_or_interface_used?.text())
					testCaseDeatilsMap?.put(T_C_IOPARAMS, node?.test_cases?.input_parameters?.text())
					testCaseDeatilsMap?.put(T_C_AUTOAPROCH,node?.test_cases?.automation_approch?.text())
					if(node?.test_cases?.expected_output){
						testCaseDeatilsMap?.put(T_C_EX_OUTPUT,node?.test_cases?.expected_output?.text())
					}
					else{
						testCaseDeatilsMap?.put(T_C_EX_OUTPUT,node?.test_cases?.except_output?.text())
					}
					testCaseDeatilsMap?.put(T_C_PRIORITY,node?.test_cases?.priority?.text())
					testCaseDeatilsMap?.put(T_C_TSI, node?.test_cases?.test_stub_interface?.text())
					testCaseDeatilsMap?.put(T_C_SCRIPT,node?.test_cases?.test_script?.text())
					testCaseDeatilsMap?.put(T_C_RELEASE_VERSION,node?.test_cases?.release_version?.text())
					testCaseDeatilsMap?.put(T_C_REMARKS,node?.test_cases?.remarks?.text())
					script?.put(T_C_DETAILS,testCaseDeatilsMap)
				}else{
					testCaseDeatilsMap?.put(T_C_ID,"")
					testCaseDeatilsMap?.put(T_C_OBJ,"")
					testCaseDeatilsMap?.put(T_C_TYPE,"")
					testCaseDeatilsMap?.put(T_C_SETUP,"")
					testCaseDeatilsMap?.put(T_C_SKIP,"")
					testCaseDeatilsMap?.put(T_C_PRE_REQUISITES, "")
					testCaseDeatilsMap?.put(T_C_INTERFACE,"")
					testCaseDeatilsMap?.put(T_C_IOPARAMS, "")
					testCaseDeatilsMap?.put(T_C_AUTOAPROCH,"")
					testCaseDeatilsMap?.put(T_C_EX_OUTPUT,"")
					testCaseDeatilsMap?.put(T_C_PRIORITY,"")
					testCaseDeatilsMap?.put(T_C_TSI, "")
					testCaseDeatilsMap?.put(T_C_SCRIPT,"")
					testCaseDeatilsMap?.put(T_C_RELEASE_VERSION,"")
					testCaseDeatilsMap?.put(T_C_REMARKS,"")
					script?.put(T_C_DETAILS,testCaseDeatilsMap)

				}
			}else{
			}
		} catch (Exception e) {
			script = null
			println " Script "+ fileName + " Error "+e.getMessage()
			e.printStackTrace()
		}
		return script
	}



	/***
	 *  Retrieves tcl script from the fileStore
	 */
	def getTclScript(final String path, final String name){
		def tclPath = path + Constants.FILE_SEPARATOR + "fileStore" + Constants.FILE_SEPARATOR + FileStorePath.RDKTCL.value() +  Constants.FILE_SEPARATOR +name +".tcl"
		def content = new StringBuilder()
		def file = new File(tclPath)
		if(file.exists()){
			file.readLines().each{
				content.append(it).append('\n')
			}
		}
		content.toString()
	}

	def getTclScriptDetails(final String path, final String name){
		def tclPath = path + Constants.FILE_SEPARATOR + "fileStore" + Constants.FILE_SEPARATOR + FileStorePath.RDKTCL.value() +  Constants.FILE_SEPARATOR +name +".tcl"
		def content = new StringBuilder()
		def file = new File(tclPath)
		if(file.exists()){
			file.readLines().each{ content.append(it) }
		}
		content.toString()
	}


	def getMinimalScript(realPath,dirName,fileName,category){
		Map script = [:]
		try{
			dirName = dirName?.trim()
			fileName = fileName?.trim()

			def moduleObj = Module.findByName(dirName)
			def scriptDirName = Constants.COMPONENT
			if(moduleObj){
				if(moduleObj?.testGroup?.groupValue.equals(TestGroup.E2E.groupValue)){
					scriptDirName = Constants.INTEGRATION
				}
			}
			File file = null
			boolean isAdvanced = Utility.isAdvancedScript(fileName, moduleObj?.getName())
			if("RDKV".equals(category) ){
				String sDirName= ""
				if(isAdvanced){
					sDirName= "//" +FILESTORE+"//" + TESTSCRIPTS_RDKV_ADV +"//"
				}else{
					sDirName= "//" +FILESTORE+"//" + TESTSCRIPTS_RDKV +"//"
				}
				file = new File( "${realPath}"+sDirName+scriptDirName+"//"+dirName+"//"+fileName+".py");
			}
			else if("RDKB".equals(category)){
				String sDirName= ""
				if(isAdvanced){
					sDirName= "//" +FILESTORE+"//" + TESTSCRIPTS_RDKB_ADV +"//"
				}else{
					sDirName= "//" +FILESTORE+"//" + TESTSCRIPTS_RDKB +"//"
				}
				file = new File( "${realPath}"+sDirName+scriptDirName+"//"+dirName+"//"+fileName+".py");
			}

			if(file.exists()){
				String s = ""
				List line = file.readLines()
				//int indx = 0
				int indx = line?.findIndexOf {  it.startsWith("'''")}
				String scriptContent = ""
				if(line.get(indx).startsWith("'''"))	{
					indx++
					while(indx < line.size() &&  !line.get(indx).startsWith("'''")){
						s = s + line.get(indx)+"\n"
						indx++
					}
					indx ++
					while(indx < line.size()){
						scriptContent = scriptContent + line.get(indx)+"\n"
						indx++
					}
				}
				String xml = s
				XmlParser parser = new XmlParser();
				def node = parser.parseText(xml)
				script.put("id", node?.id?.text())
				script.put("version", getIntegerValue(node.version.text()))
				script.put("name", node.name.text())
				script.put("skip", getBooleanValue(node.skip.text()))
				script.put("longDuration", getBooleanValue(node.long_duration.text()))
				def versList = []
				def btList = []
				def tagList = []
				Set btSet = node?.box_types?.box_type?.collect{ it.text() }
				Set versionSet = node?.rdk_versions?.rdk_version?.collect{ it.text() }
				btSet.each { bt ->
					btList.add(BoxType.findByNameAndCategory(bt, Utility.getCategory(category)))
				}
				versionSet.each { ver ->
					versList.add(RDKVersions.findByBuildVersionAndCategory(ver,  Utility.getCategory(category)))
				}

				Set tagSet = node?.script_tags?.script_tag?.collect{ it.text() }
				tagSet.each { tag ->
					tagList.add(ScriptTag.findByNameAndCategory(tag, Utility.getCategory(category)))
				}

				script.put("rdkVersions", versList)
				script.put("boxTypes", btList)
				script.put("scriptTags", tagList)

			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		return script
	}

	def getStatus(def statusText){
		Status status = Status.NOT_FOUND
		if(statusText){
			if(statusText == Status.ALLOCATED){
				status = Status.ALLOCATED
			}else if(statusText == Status.BUSY){
				status = Status.BUSY
			}else if(statusText == Status.FREE){
				status = Status.FREE
			}else if(statusText == Status.HANG){
				status = Status.HANG
			}else if(statusText == Status.TDK_DISABLED){
				status =  Status.TDK_DISABLED
			}
			else{
				status = Status.NOT_FOUND
			}
		}
		return status
	}

	def getExecutionTime(String exTime){
		int execTime = 2
		if(exTime){
			execTime = Integer.parseInt(exTime?.trim())
		}

		return execTime
	}

	def getBooleanValue(String bText){
		if(bText){
			if(bText?.trim() == "true"){
				return true
			}
		}
		return false
	}

	def getIntegerValue(String iText){
		int intVal
		if(iText){
			intVal = Integer.parseInt(iText?.trim())
		}
		return intVal
	}

	def isDefaultSGUpdateRequired(def realPath){
		try {
			Properties prop = new Properties();
			String fileName = realPath+"/fileStore/script.config";
			File ff = new File(fileName)
			if(ff.exists()){
				InputStream is = new FileInputStream(fileName);
				prop.load(is);
				def value = prop.getProperty("defaultScriptGroup");
				if(value){
					if(value.equals("true")){
						return true
					}
				}

			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		return false
	}

	def scriptListRefresh(def realPath , def totalScriptList){

		boolean  value1 = false
		try {
			def list1 = scriptsList.collect()
			scriptsList.clear()
			List scriptList = []
			Map tempScriptGroupMap = [:]
			boolean updateReqd = isDefaultSGUpdateRequired(realPath)
			[FileStorePath.RDKB.value(), FileStorePath.RDKV.value(), FileStorePath.RDKBADVANCED.value(), FileStorePath.RDKVADVANCED.value()].each{  path ->

				def category
				if(path.equals(FileStorePath.RDKB.value()) || path.equals(FileStorePath.RDKBADVANCED.value())){
					category = Category.RDKB.toString()
				}
				else if(path.equals(FileStorePath.RDKV.value()) || path.equals(FileStorePath.RDKVADVANCED.value())){
					category = Category.RDKV.toString()
				}

				List dirList = [Constants.COMPONENT, Constants.INTEGRATION]
				def start = System.currentTimeMillis()
				dirList.each{ directory ->
					File scriptsDir = new File( "${realPath}//fileStore"+FILE_SEPARATOR+path+FILE_SEPARATOR+directory+FILE_SEPARATOR)

					if(scriptsDir.exists()){
						def modules = scriptsDir.listFiles()
						Arrays.sort(modules);
						modules.each { module ->
							def start1 =System.currentTimeMillis()
							try {
								File [] files = module.listFiles(new FilenameFilter() {
											@Override
											public boolean accept(File dir, String name) {
												return name.endsWith(".py");
											}
										});
								def start2 = System.currentTimeMillis()
								def sLst = []
								if(tempScriptGroupMap.keySet().contains(module?.getName())){
									sLst = tempScriptGroupMap.get(module?.getName())
								}
								files.each { file ->
									String name = ""+file?.name?.trim()?.replace(".py", "")
									def sFile
									if(!sLst.contains(name)){
										sLst.add(name)
									}
									ScriptFile.withTransaction {
										sFile = ScriptFile.findByScriptNameAndModuleName(name,module.getName())
										if(sFile == null){
											sFile = new ScriptFile()
											sFile.setModuleName(module?.getName())
											sFile.setScriptName(name)
										}
										sFile.category = Utility.getCategory(category)
										sFile.save(flush:true)
									}

									sFile = ScriptFile.findByScriptNameAndModuleName(name,module.getName())

									def scriptsListmap = scriptsListMap.get(category)
									if(scriptsListmap == null){
										scriptsListmap = []
										scriptsListMap.put(category, scriptsListmap)
									}
									if(!scriptsListmap.contains(sFile)){
										scriptsListmap.add(sFile)
										scriptMapping.put(name, module?.getName())
									}

									def scriptNameListmap = scriptNameListMap.get(category)
									if(scriptNameListmap == null){
										scriptNameListmap = []
										scriptNameListMap.put(category, scriptNameListmap)
									}
									if(!scriptNameListmap.contains(name)){
										scriptNameListmap.add(name)
									}
									if(!scriptsList.contains(sFile)){
										scriptsList.add(sFile)
										scriptMapping.put(name, module?.getName())
									}
									scriptsListAdvanced.put(sFile?.id, path)
									if(!scriptNameList.contains(name)){
										scriptNameList.add(name)
									}
									if(updateReqd == true){
										updateDefaultScriptGroups(realPath,name,module?.getName(), category)
									}
								}

								sLst?.sort()

								totalScriptList?.each{ key, value ->
									if( key.toString()  ==  module.getName()?.toString()){
										if(!(value?.equals(sLst))){
											scriptGroupMap.put(module?.getName(), sLst)
											tempScriptGroupMap.put(module?.getName(), sLst)
											value1 = false
										}else {
											value1 = true
										}
									}
								}
							} catch (Exception e) {
								e.printStackTrace()
							}

						}
					}
				}
			}

			initializeTCLScripts(realPath)

		} catch (Exception e) {
			log.error  "Error"+e.getMessage()
			e.printStackTrace()
		}
		return value1
	}

	def updateAdvScriptMap(String sName , String moduleName , Category category , boolean isAdvanced){

		ScriptFile sFile = ScriptFile.findByScriptNameAndModuleName(sName,moduleName)
		if(sFile){
			String path = ""
			switch(category){
				case Category.RDKV:
					if(!isAdvanced){
						path = FileStorePath.RDKV.value()
					}else{
						path = FileStorePath.RDKVADVANCED.value()
					}
					break;
				case Category.RDKB:
					if(!isAdvanced){
						path = FileStorePath.RDKB.value()
					}else{
						path = FileStorePath.RDKBADVANCED.value()
					}
					break;
				case Category.RDKB_TCL:
					path = FileStorePath.RDKTCL.value()
					break;
				default:
					break;
			}
			scriptsListAdvanced.put(sFile?.id, path)
		}
	}

	/***
	 * Returns the fileName
	 *
	 * @param realPath
	 * @param dirName
	 * @param moduleName
	 * @param fileName
	 * @param category
	 * @return
	 */
	def getFileFromPath(def realPath, def dirName, def moduleName, def fileName, def category){
		def path = new StringBuffer()

		path = path?.append(realPath).append(FILE_SEPARATOR).append(FILESTORE)

		boolean isAdvanced = Utility.isAdvancedScript(fileName, moduleName)

		String testDirName = ""
		String extn = ".py"
		switch(category){
			case Category.RDKV:
				testDirName =  FileStorePath.RDKV.value()
				if(isAdvanced){
					testDirName =  FileStorePath.RDKVADVANCED.value()
				}
				break;
			case Category.RDKB:
				testDirName =  FileStorePath.RDKB.value()
				if(isAdvanced){
					testDirName =  FileStorePath.RDKBADVANCED.value()
				}
				break;
			case Category.RDKB_TCL:
				testDirName = FileStorePath.RDKTCL.value()
				extn = ".tcl"
				break;
			default: break;
		}
		path = path?.append(FILE_SEPARATOR).append(testDirName).append(FILE_SEPARATOR).append(dirName).append(FILE_SEPARATOR).append(moduleName).append(FILE_SEPARATOR).append(fileName).append(extn)

		return path?.toString()
	}

	/***
	 * Retrieve tcl scripts list
	 * @param realPath
	 * @return
	 */

	def getTclFileList(def realPath){
		if(tclScriptsList == null){
			initializeTCLScripts("${realPath}//fileStore//"+FileStorePath.RDKTCL.value())
		}
		tclScriptsList
	}
	/**
	 * The test profile test suite name list
	 * @return
	 */
	def testProfileTestSuiteList(){
		try{
			Properties props = new Properties()
			def testSuiteConfig = 	props.load(grailsApplication.parentContext.getResource("/appConfig/testSuiteConfig.properties").inputStream)
			def rdkVersion = props.get("rdkversion")
			def boxType =  props.get("boxType")
			def testProfile = props.get("testProfile")
			if( rdkVersion &&  boxType && testProfile){
				def rdkVersionList =[]
				if(rdkVersion?.toString()?.contains(",")){
					rdkVersionList = rdkVersion?.split(",")
				}else {
					rdkVersionList?.add(rdkVersion)
				}
				def boxTypeList = []
				if(boxType?.toString()?.contains(",")){
					boxTypeList = boxType?.split(",")
				}else {
					boxTypeList?.add(boxType)
				}
				def testProfileList  = []
				if(testProfile?.toString()?.contains(",")){
					testProfileList	=  testProfile.split(",")
				}else{
					testProfileList?.add(testProfile)
				}
				rdkVersionList?.each{ rdkVer->
					boxTypeList.each{ bType->
						testProfileList?.each {tProile->
							if(RDKVersions?.findByBuildVersion(rdkVer?.toString()?.trim()) && BoxType?.findByName(bType.toString()?.trim()) && TestProfile?.findByName(tProile.toString()?.trim())){
								def suiteName = rdkVer?.toString()?.trim()+"_"+bType?.toString()?.trim()+"_"+tProile?.toString()?.trim()
								testProfileSuite?.add(suiteName)
							}
						}
					}
				}
			}
			return testProfileSuite
		}catch(Exception e ){
			println " ERROR "+e.getMessage()
			e.printStackTrace()
		}

	}

	/**
	 * Function for creating the  test suite based on the test profile.
	 * @param scriptInstance
	 * @param sObject
	 * @param category
	 * @return
	 */
	def updateScriptsFromTestProfile(final def scriptInstance, final ScriptObject sObject, final def category ){
		removeScriptsFromTestProfiles(scriptInstance, sObject,category)
		//removesScriptsFromAllTestProfileSuites(scriptInstance, sObject,category)
		try{
			def  rdkVersionsList = sObject?.getRdkVersions()
			def bTypes = sObject?.getBoxTypes()
			def testProfileList = sObject?.getTestProfile()
			boolean value = false
			testProfileList?.each{ testProfile->
				def testProfileName = TestProfile?.findByName(testProfile?.toString())
				bTypes?.each{ boxType ->
					rdkVersionsList?.each { rdkVersionName ->
						if(sObject?.getBoxTypes()?.toString()?.contains(boxType?.toString()) && sObject?.getRdkVersions()?.toString()?.contains(rdkVersionName?.toString())){
							def suiteName  =  rdkVersionName?.toString()+"_"+boxType?.toString()+"_"+testProfileName?.toString()
							def scriptGrpInstance = ScriptGroup.findByNameAndCategory(suiteName,category)
							if(testProfileSuite?.toString()?.contains(suiteName?.toString())){
								value = true
							}
							if(value){
								if(!scriptGrpInstance){
									scriptGrpInstance = new ScriptGroup()
									scriptGrpInstance.name = suiteName
									scriptGrpInstance?.category = category
									scriptGrpInstance.save()
									scriptGrpInstance?.addToScriptList(scriptInstance)
								}
								if(scriptGrpInstance && !scriptGrpInstance?.scriptList?.contains(scriptInstance)){
									scriptGrpInstance.addToScriptList(scriptInstance)
									scriptGrpInstance.save(flush:true)
								}
							}
						}
					}
				}
			}
		}catch(Exception e){
			println "ERROR "+e.getMessage()
			e.printStackTrace()
		}
	}
	/**
	 * Remove the scripts from test profile suite as per the configuration file entries
	 * @param scriptInstance
	 * @param sObject
	 * @param category
	 * @return
	 */
	def removeScriptsFromTestProfiles(final def scriptInstance,final def sObject, final def category){
		testProfileSuite?.each{ testSuite ->
			def scriptGroupInstance = ScriptGroup?.findByNameAndCategory(testSuite?.toString(),category )
			if(scriptGroupInstance){
				scriptGroupInstance?.removeFromScriptList(scriptInstance)
				scriptGroupInstance?.save()
			}
		}
	}

	/**
	 * Function for using removing the script from all test profile suites
	 * @param scriptInstance
	 * @param sObject
	 * @param category
	 * @return
	 */
	def removesScriptsFromAllTestProfileSuites(final def scriptInstance,final def sObject, final def category){
		def boxTypes = BoxType?.findAllByCategory(category)
		def rdkVersions = RDKVersions?.findAllByCategory(category)
		def testProfiles = TestProfile?.findAllByCategory(category)
		def totalTestSuiteList = []
		boxTypes?.each{ bType ->
			rdkVersions?.each{ rdkVersion->
				testProfiles?.each{ tProfile->
					def testSuiteName = rdkVersion?.toString()+"_"+bType?.toString()+"_"+tProfile?.toString()
					def scriptGroupInstance = ScriptGroup?.findByName(testSuiteName)
					if(scriptGroupInstance){
						totalTestSuiteList?.add(scriptGroupInstance)
					}
				}
			}
		}
		totalTestSuiteList?.each{ testSuite ->
			def scriptGroupInstance = ScriptGroup?.findByNameAndCategory(testSuite?.toString(),category )
			if(scriptGroupInstance){
				scriptGroupInstance?.removeFromScriptList(scriptInstance)
				scriptGroupInstance?.save()
			}
		}
	}
	/**
	 * The function used to adding test profile scripts in corresponding suite
	 * @param realPath
	 * @param name
	 * @param moduleName
	 * @param category
	 * @return
	 */
	def updateSuiteWithTestProfileScripts(def realPath, def name , def moduleName, category){
		try{
			def scriptFile = ScriptFile.findByScriptNameAndModuleName(name,moduleName)
			boolean value = false
			if(scriptFile){
				def script=getScript(realPath, moduleName,name,category )
				if (script?.testProfile){
					removeScriptsFromTestProfiles(scriptFile,[:],category)
					def boxTypeList = script?.boxTypes
					def rdkVersions =  script?.rdkVersions
					def testProfile =  script?.testProfile
					testProfile.each{ tProfile->
						rdkVersions?.each{ rdkVersion ->
							boxTypeList?.each{ bType->
								def suiteName  =  rdkVersion?.toString()+"_"+ bType?.toString()+"_"+ tProfile?.toString()
								def scriptGrpInstance = ScriptGroup?.findByName(suiteName)
								if(testProfileSuite?.toString()?.contains(suiteName?.toString())){
									value = true
								}
								if(value){
									if(!scriptGrpInstance){
										scriptGrpInstance = new ScriptGroup()
										scriptGrpInstance.name = suiteName
										scriptGrpInstance?.category = category
										scriptGrpInstance.save()
										scriptGrpInstance?.addToScriptList(scriptFile)
										scriptGrpInstance.save(flush:true)
									}
									if(scriptGrpInstance && !scriptGrpInstance?.scriptList?.contains(scriptFile)){
										scriptGrpInstance.addToScriptList(scriptFile)
									}
								}
							}
						}
					}
				}
			}
		}catch(Exception e){
			println " ERROR "+ e.getMessage()
			e.printStackTrace()
		}
	}
	/**
	 * Function return the test case map when adding the new script
	 * @param testCaseMap
	 * @return
	 */
	def addNewTestCaseDetails(def testCaseMap ,def uniqueId){
		newTestCaseMap.put(uniqueId, testCaseMap)
		return  testCaseMap
	}

	def getNewTestCaseDetails(def uniqueId){
		return newTestCaseMap.get(uniqueId)
	}

	/**
	 * Function return the test case map when adding the new script
	 * @param testCaseMap
	 * @return
	 */
	def clearTestCaseDetailsMap(def uniqueId){
		newTestCaseMap.remove(uniqueId)
	}



	/**
	 * function used return the file names in particular module
	 * @author nishab
	 *
	 */
	def getFileList(def moduleDir){
		def fileList = []
		File module =  new File(moduleDir?.toString())
		if(module?.exists()){
			File []  files = module.listFiles(new FilenameFilter() {
						@Override
						public boolean accept(File dir, String name) {
							return name.endsWith(".py");
						}
					});
			files?.each{file->
				String name = ""+file?.name.trim()?.replace(".py", "")
				fileList?.add(name)
			}
		}
		return fileList
	}

	/**
	 * To fetch the file directory object for the mentioned module name.
	 */
	def getModuleDirectory(def moduleName , def realPath , def category){
		String dirName = ""
		def path = null
		File module = null
		if(!category?.equals(Category.RDKB_TCL.toString())){

			def moduleObj = Module.findByName(moduleName)
			def scriptDirName = Constants.COMPONENT
			if(moduleObj){
				if(moduleObj?.testGroup?.groupValue.equals(TestGroup.E2E.groupValue)){
					scriptDirName = Constants.INTEGRATION
				}
			}

			if(category?.equals(Category.RDKV.toString())){
				dirName = FileStorePath.RDKV.value()
			}else if(category?.equals(Category.RDKB.toString())){
				dirName = FileStorePath.RDKB.value()
			}
			path = "${realPath}//fileStore//"+dirName+"//"+scriptDirName+"//"+moduleName

		}else if(category?.equals(Category.RDKB_TCL.toString())){
			dirName = FileStorePath.RDKTCL.value()
			path = "${realPath}//fileStore//"+dirName
		}
		if(path){
			module = new File (path)
		}
		return module
	}

	/**
	 * Method to update the script groups both RDKv & RDKB from script group page ui
	 */
	def updateScriptGroups(def moduleName , def realPath , def category){
		File module = getModuleDirectory(moduleName, realPath, category)

		if(category?.equals(Category.RDKB_TCL.toString()) || moduleName == 'tcl'){

			updateTCLScriptGroup("${realPath}//fileStore//"+FileStorePath.RDKTCL.value())
		}else{
			updateScriptGroup(module, realPath, category)
		}
	}

	/**
	 * Method to update the script groups
	 */
	private void updateScriptGroup(def moduleDir, def realPath, def category){
		try {
			File [] files = moduleDir.listFiles(new FilenameFilter() {
						@Override
						public boolean accept(File dir, String name) {
							return name.endsWith(".py");
						}
					});
			def sLst = []
			files.each { file ->
				String name = ""+file?.name?.trim()?.replace(".py", "")
				updateDefaultScriptGroupsList(realPath,name,moduleDir?.getName(), category)
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}

	/**
	 * Method to update the TCL script groups
	 */
	private void updateTCLScriptGroup(final String path) {
		def tclPath = path?.trim()
		def tclFiles = new File(tclPath).listFiles(new FileFilter(){
					boolean accept(File file) {
						def fileName = file.name
						if(!(fileName?.toString()?.equals("lib.tcl") || fileName?.toString()?.equals("proc.tcl"))){
							return fileName.endsWith(".tcl")
						}
					}
				})

		try{
			tclFiles.each { tclFile ->
				def fileName = tclFile.name.split(".tcl")[0]
				def scriptName =ScriptFile.findByScriptNameAndCategory(fileName, Category.RDKB_TCL)
				if(scriptName){
					updateTclScriptSuite(scriptName ,"RDKB_TCL")
				}
			}
		}catch(Exception e){
			println e?.getMessage()
			e.printStackTrace()
		}
	}

	/**
	 * Method to update the script groups based on test profile
	 */
	def updateSuiteWithTestProfileScript(def script , def scriptFile , def category){
		try{
			boolean value = false
			removeScriptsFromTestProfiles(scriptFile,[:],category)
			def boxTypeList = script?.boxTypes
			def rdkVersions =  script?.rdkVersions
			def testProfile =  script?.testProfile
			testProfile.each{ tProfile->
				rdkVersions?.each{ rdkVersion ->
					boxTypeList?.each{ bType->
						def suiteName  =  rdkVersion?.toString()+"_"+ bType?.toString()+"_"+ tProfile?.toString()
						def scriptGrpInstance = ScriptGroup?.findByName(suiteName)
						if(testProfileSuite?.toString()?.contains(suiteName?.toString())){
							value = true
						}
						if(value){
							if(!scriptGrpInstance){
								scriptGrpInstance = new ScriptGroup()
								scriptGrpInstance.name = suiteName
								scriptGrpInstance?.category = category
								scriptGrpInstance.save()
								scriptGrpInstance?.addToScriptList(scriptFile)
								scriptGrpInstance.save(flush:true)
							}
							if(scriptGrpInstance && !scriptGrpInstance?.scriptList?.contains(scriptFile)){
								scriptGrpInstance.addToScriptList(scriptFile)
							}
						}
					}
				}
			}
		}catch(Exception e){
			e.printStackTrace()
		}
	}
}
