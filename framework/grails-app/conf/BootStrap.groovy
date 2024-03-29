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
import grails.util.Environment;
import groovy.sql.Sql;

import java.io.IOException
import com.comcast.rdk.Category;
import com.comcast.rdk.Constants;
import com.comcast.rdk.Device;
import com.comcast.rdk.DeviceGroup;
import com.comcast.rdk.ExecuteMethodResult;
import com.comcast.rdk.Execution;
import com.comcast.rdk.ExecutionDevice;
import com.comcast.rdk.ExecutionResult;
import com.comcast.rdk.Function;
import com.comcast.rdk.Groups;
import com.comcast.rdk.JobDetails;
import com.comcast.rdk.Performance;
import com.comcast.rdk.RDKVersions;
import com.comcast.rdk.RepeatPendingExecution;
import com.comcast.rdk.ScriptFile
import com.comcast.rdk.ScriptGroup
import com.comcast.rdk.ScriptTag;
import com.comcast.rdk.SoCVendor;
import com.comcast.rdk.TestGroup;
import com.comcast.rdk.ThirdPartyExecutionDetails;
import com.comcast.rdk.User
import com.comcast.rdk.Role
import com.comcast.rdk.Module
import com.comcast.rdk.BoxType
import com.comcast.rdk.BoxManufacturer
import com.comcast.rdk.socketCommuniation.SocketPortConnector
import com.comcast.rdk.ExecutionService;
import org.apache.shiro.crypto.hash.Sha256Hash

class BootStrap {
	
	def grailsApplication
    def primitivetestService
	def migrationService
	def scriptService
	def primitiveService
	def executionService
    def utilityService
	def mailService
	
    def init = { servletContext ->
		
		try {
			migratetoUnifiedTM();
		} catch (Exception e) {
			e.printStackTrace()
		}
		
		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//filetransfer.py").file
		def absolutePath = layoutFolder.absolutePath

		layoutFolder = grailsApplication.parentContext.getResource("//logs//crashlogs//execId_logdata.txt").file
		def absolutePath1 = layoutFolder.absolutePath
		User.withTransaction {
		def user = new User(username: "admin", passwordHash: new Sha256Hash("password").toHex(),
			name : "ADMINISTRATOR", email : "sreelal@tataelxsi.co.in")
        user.addToPermissions("*:*")
        user.save(flush:true)
		}
		createRolesAndAssignForAdmin()

		
		BoxType.withTransaction {
        def boxTypes = BoxType.list()
        if(!boxTypes){
			def boxtype = new BoxType(name : "IPClient-3", type : "Client", category: Category.RDKV )
			boxtype.save(flush:true)
			boxtype = new BoxType(name : "Hybrid-1", type : "Gateway", category: Category.RDKV)
			boxtype.save(flush:true)
        }
		}
       int port = Integer.parseInt("8089")
        try
        {
           Thread t = new SocketPortConnector(port,absolutePath.toString(),absolutePath1.toString())
           t.start()
        }catch(IOException e)
        {
           e.printStackTrace() 
        }
		
//		migrateScriptGroupContents();
		
		
		if(Environment.current.name == 'production'){
			migrationService.doMigration()
		}
		
		
		/*def sgList = ScriptGroup.list();
		sgList.each { sg ->
			sg.scriptsList.each { script ->
				def mm
				ScriptFile.withTransaction {
					mm = ScriptFile.findByScriptNameAndModuleName(script?.name,script?.primitiveTest?.module?.name)
					if(mm == null){
						mm = new ScriptFile()
						mm.setScriptName(script?.name)
						mm.setModuleName(script?.primitiveTest?.module?.name)
						mm.save()
					}
				}
				if(mm && !sg.scriptList.contains(mm)){
					sg.addToScriptList(mm)
				}

			}
		}*/
		
		Device.withTransaction {
			def thunderDevices = Device.findAllByIsThunderEnabled(1)
			if(thunderDevices){
				thunderDevices.each{ thunderDevice ->
					if(!thunderDevice?.thunderPort){
						thunderDevice?.thunderPort = 80
						thunderDevice.save(flush:true)
					}
				}
			}
		}
		
		def rootFile = grailsApplication.parentContext.getResource("/")
		scriptService?.testProfileTestSuiteList()
		scriptService.initializeScriptsData(rootFile.file.getAbsolutePath())
		primitiveService.initializePrimitiveTests(rootFile.file.getAbsolutePath())
//		scriptService?.createSuite()
		executionService.handleInprogressExecutionOnStartup()
		executionService.tftpServerStartUp(rootFile.file.getAbsolutePath())
		// creates tcl module if it doesn't exist
		createTclModule()
		//create thunder module if it doesn't exist
		createThunderModule()
		try{
			createRdkServiceModules(rootFile.file.getAbsolutePath())
		}catch(Exception e){
			e.printStackTrace()
		}
		try{
			removeDuplicateCertificationScripts(rootFile.file.getAbsolutePath())
		}catch(Exception e){
			e.printStackTrace()
		}
		/*List<Script> scriptList = Script.list()
		
		scriptList.each{ scriptInstance ->
			String moduleName = scriptInstance?.primitiveTest?.module?.name
			def scriptGrpInstance = ScriptGroup.findByName(moduleName)
			if(!scriptGrpInstance){
				scriptGrpInstance = new ScriptGroup()
				scriptGrpInstance.name = moduleName
			}
				
			scriptGrpInstance.addToScriptsList(scriptInstance)
			scriptGrpInstance.save(flush:true)
		}*/
		
		//Code to generate the box type & rdk version based script group. Needs to execute once.
		
		/*try {
			List<Script> scriptsList = Script.list()
					
					scriptsList.each{ scriptInstance ->
					
					scriptInstance?.boxTypes?.each{ bType ->
					
					scriptInstance?.rdkVersions?.each{ vers ->
					
					String name = vers?.toString()+"_"+bType?.name
							def scriptGrpInstance = ScriptGroup.findByName(name)
							if(!scriptGrpInstance){
								scriptGrpInstance = new ScriptGroup()
								scriptGrpInstance.name = name
							}
					if(scriptGrpInstance && !scriptGrpInstance?.scriptsList?.contains(scriptInstance)){
						scriptGrpInstance.addToScriptsList(scriptInstance)
						scriptGrpInstance.save(flush:true)
					}
					}
					}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}*/
		
    }
	
	def createTclModule() {
		def tclModule = Module.findByName('tcl')
		if(tclModule == null){
			Module?.withTransaction{
				def moduleInstance = new Module()
				moduleInstance.name = 'tcl'
				moduleInstance.testGroup = TestGroup.Component
				moduleInstance.groups= null
				
				moduleInstance.category= Category.RDKB_TCL
				if(!moduleInstance.save(flush:true)){
					moduleInstance.errors.each{
						println it
					}
				}
			}
		}
	}
	
    
    def destroy = {   
		if(ExecutionService.tftpProcess != null){
			println " Stopping tftp "
			try {
				ExecutionService.tftpProcess?.destroy()
				ExecutionService.tftpProcess?.exitValue()
			} catch (Exception e) {
				println "ERROR "+ e.getMessage()
				e.printStackTrace()
			}
		}
		SocketPortConnector.closeServerSocket()
    }
	
	def createRolesAndAssignForAdmin()
	{
		def permDeviceGroup = "DeviceGroup:*:*"
		def permScriptGroup = "ScriptGroup:*:*"
		def permExecution = "Execution:*:*"
		def permChart = "Trends:*:*"
		def permPrimitiveTest = "PrimitiveTest:*:*"
		def permModule = "Module:*:*"
		def permStreamingDetails = "StreamingDetails:*:*"
		
		
		Role.withTransaction {
		def adminRole = Role.findByName("ADMIN")
		if(!adminRole)
		{
			def adminUser  = User.findByUsername("admin")
			adminRole = new Role(name: "ADMIN")
			adminRole.addToPermissions("*:*")
			adminRole.save(flush:true)
		   
			if(adminUser){
				adminUser.addToRoles(adminRole)
			}
		}
		}
		Role.withTransaction {
		Role testerRole = Role.findByName("TESTER")
		if(!testerRole)
		{
			testerRole = new Role(name: "TESTER")
			testerRole.addToPermissions(permDeviceGroup)
			testerRole.addToPermissions(permScriptGroup)
			testerRole.addToPermissions(permExecution)
			testerRole.addToPermissions(permChart)
			//testerRole.addToPermissions(permPrimitiveTest)
			//testerRole.addToPermissions(permModule)
			//testerRole.addToPermissions(permStreamingDetails)
			
			testerRole.save(flush:true)
		}else{
			if(testerRole.permissions){
				
				if(!testerRole.permissions.contains(permDeviceGroup)){
					testerRole.addToPermissions(permDeviceGroup)
				}
				
				if(!testerRole.permissions.contains(permScriptGroup)){
					testerRole.addToPermissions(permScriptGroup)
				}
				
				if(!testerRole.permissions.contains(permExecution)){
					testerRole.addToPermissions(permExecution)
				}
				
				if(!testerRole.permissions.contains(permChart)){
					testerRole.addToPermissions(permChart)
				}
	
			/*	if(!testerRole.permissions.contains(permPrimitiveTest)){
					testerRole.addToPermissions(permPrimitiveTest)
				}
				
				if(!testerRole.permissions.contains(permModule)){
					testerRole.addToPermissions(permModule)
				}
				
				if(!testerRole.permissions.contains(permStreamingDetails)){
					testerRole.addToPermissions(permStreamingDetails)
				}*/
				
			
				testerRole.save(flush:true)
			}
		}		
		}	
	}

	/**
	 * Method to migrate the existing tables to unified TM.
	 */
	def migratetoUnifiedTM(){
        println " migrate to UnifiedTM Start "
       
        BoxType.executeUpdate("update BoxType m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
        Function.executeUpdate("update Function m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
        Module.executeUpdate("update Module m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
        RDKVersions.executeUpdate("update RDKVersions m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
        ScriptFile.executeUpdate("update ScriptFile m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
        ScriptTag.executeUpdate("update ScriptTag m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
        SoCVendor.executeUpdate("update SoCVendor m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
        BoxManufacturer.executeUpdate("update BoxManufacturer m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
       
        ScriptGroup.executeUpdate("update ScriptGroup m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
       
        Device.executeUpdate("update Device m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
        DeviceGroup.executeUpdate("update DeviceGroup m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
        ExecuteMethodResult.executeUpdate("update ExecuteMethodResult m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
        Execution.executeUpdate("update Execution m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
        ExecutionDevice.executeUpdate("update ExecutionDevice m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
        ExecutionResult.executeUpdate("update ExecutionResult m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
       
        JobDetails.executeUpdate("update JobDetails m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
        Performance.executeUpdate("update Performance m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
        RepeatPendingExecution.executeUpdate("update RepeatPendingExecution m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
        ThirdPartyExecutionDetails.executeUpdate("update ThirdPartyExecutionDetails m set m.category=:rdkvcat where m.category !=:rdkbcat and category !=:rdkbtclcat and category !=:rdkvthundercat and category !=:rdkc and category !=:rdkvrdkservicecat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB,rdkbtclcat:Category.RDKB_TCL,rdkvthundercat:Category.RDKV_THUNDER,rdkc:Category.RDKC,rdkvrdkservicecat:Category.RDKV_RDKSERVICE]);
       
        println " migrate to UnifiedTM End "
    }
	
	/**
	 * Method to create thunder module if it is not already present
	 * @return
	 */
	def createThunderModule() {
		def thunderModule = Module.findByName(Constants.THUNDER)
		if(thunderModule == null){
			Module?.withTransaction{
				def moduleInstance = new Module()
				moduleInstance.name = Constants.THUNDER
				moduleInstance.testGroup = TestGroup.Component
				moduleInstance.groups= null
			   
				moduleInstance.category= Category.RDKV_THUNDER
				if(!moduleInstance.save(flush:true)){
					moduleInstance.errors.each{
						println it
					}
				}
			}
		}
	}
	
	
	/**
	 * Method to create RdkService module if it is not already present
	 * @return
	 */
	def createRdkServiceModules(def realPath){
		def rdkServiceModule = Module.findByName(Constants.RDKSERVICES)
		if(rdkServiceModule == null){
			Module?.withTransaction{
				def moduleInstance = new Module()
				moduleInstance.name = Constants.RDKSERVICES
				moduleInstance.testGroup = TestGroup.Component
				moduleInstance.groups= null
				moduleInstance.category= Category.RDKV
				if(!moduleInstance.save(flush:true)){
					moduleInstance.errors.each{
						println it
					}
				}
			}
		}
		File certificationDirectory = new File( "${realPath}//fileStore//"+Constants.TESTSCRIPTS_RDKV+"//"+Constants.CERTIFICATION+"//")
		if(certificationDirectory.exists()){
			def folders = certificationDirectory.list()
			folders.each{folder->
				File folderDirectory = new File( "${realPath}//fileStore//"+Constants.TESTSCRIPTS_RDKV+"//"+Constants.CERTIFICATION+"//"+folder)
				if(folderDirectory.exists()){
					def module = Module.findByName(folder)
					if(module){
						if(!module?.testGroup.equals(TestGroup.Certification)){
							module?.testGroup = TestGroup.Certification
						}
						if(!module.save(flush:true)){
							module.errors.each{
								println it
							}
						}
					}
					if(module == null){
							Module?.withTransaction{
								def certificationModuleInstance = new Module()
								certificationModuleInstance.name = folder
								certificationModuleInstance.testGroup = TestGroup.Certification
								certificationModuleInstance.groups= null
								certificationModuleInstance.category= Category.RDKV
								if(!certificationModuleInstance.save(flush:true)){
									certificationModuleInstance.errors.each{
										println it
									}
								}
							}
						}
				}
			}
		}
	}
	
	/*
	 * Method to remove duplicate certification scripts
	 */
	def removeDuplicateCertificationScripts(def realPath){
		List moduleList = [Constants.RDKV_PERFORMANCE,Constants.RDKV_STABILITY,Constants.RDKV_MEDIA,Constants.RDKV_SECURITY,Constants.RDKV_MEDIAVALIDATION,Constants.RDKV_PROFILING,Constants.RDKSERVICES]
		ScriptFile.withTransaction {
			def sFObjectList = []
			try{
				moduleList?.each{
					def sFList = ScriptFile.findAllByModuleNameAndCategory(it,Category.RDKV_RDKSERVICE)
					if(sFList){
						sFList?.each{sF->
							sFObjectList.add(sF)
						}
					}
				}
				sFObjectList?.each{sFO->
					scriptService.verifyScriptFile(realPath,sFO?.id, sFO?.scriptName)
				}
			}catch(Exception e){
				e.printStackTrace()
			}
		}
	}

}           
