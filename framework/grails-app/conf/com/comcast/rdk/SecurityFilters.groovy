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

import java.io.File;

import javax.servlet.http.HttpServletResponse

import org.apache.shiro.authc.UsernamePasswordToken
import org.apache.shiro.authc.AuthenticationException
import org.apache.shiro.SecurityUtils;
import org.apache.shiro.subject.Subject

/**
 * Generated by the Shiro plugin. This filters class protects all URLs
 * via access control by convention.
 */
class SecurityFilters {
	def grailsApplication
	
	/**
	 * publicActions is a list of all REST API methods which can be accessed without 
	 * authentication. Some of these methods are also included in securedPublicActions.
	 * So the methods which are present in both publicActions and securedPublicActions 
	 * needs authentication to be accessed if rest.authentication.enabled is enabled
	 * to true in tm.config file 
	 */
    def publicActions = [     
		user: ['changePassword','registerUser','saveUser'],
		primitiveTest : ['getJson','getStreamDetails'],
		execution : ['saveLoadModuleStatus','saveResultDetails','getDeviceStatusList','getDeviceStatus','thirdPartyJsonResult','thirdPartyTest','showResult','getDetailedTestResult','getClientPort','stopThirdPartyTestExecution','getAgentConsoleLog','getRealtimeDeviceStatus','getExecutionOutput','thirdPartySingleTestExecution','thirdPartyJsonPerformanceResult','getExecutionId','getImageName','getExecutionList', 'getDeviceImageName','thirdPartyMultipleScriptExecution','uploadLogs','getExecutionStatus','exportConsolidatedToExcel','getTMIPAddress','securedUploadLogs', 'resultSummary', 'changeDeviceIP','fetchDataFromGrafana','getAlertNotification','fetchAlertDataForMemoryProfiling','setExecutionResultStatus','showFileContents','fetchDataFromGrafanaMultiple','showSVGContents'],
		deviceGroup : ['uploadAgentBinaries','getDeviceList','deleteDeviceMethod','createNewDevice','uploadTclConfig','getDeviceBoxType','getDeviceDetails','uploadE2EConfig','getDevicePorts','getThunderDevicePorts'],
		scriptGroup : ['getScriptsByScriptGroup','getScriptsByModule','getAllScriptGroups','deleteScriptGroup','createNewScriptGroup','verifyScriptGroup','getScriptTimeout','getTestJavaScript'],
		module : ['getModuleScriptTimeOut'],
		thunder : ['thirdPartySingleTestExecutionThunder','thirdPartySuiteExecutionThunder', 'thirdPartyMultipleTestExecutionThunder']
    ];

	/**
	 * securedPublicActions is a list of REST API methods which require authentication to be 
	 * accessed if rest.authentication.enabled is enabled to true in tm.config file.
	 */
    def securedPublicActions = [
			user: ['changePassword'],
			execution : ['getDeviceStatusList', 'getDeviceStatus','thirdPartyJsonResult','thirdPartyTest','showResult','getDetailedTestResult','stopThirdPartyTestExecution','getAgentConsoleLog','getRealtimeDeviceStatus','getExecutionOutput','thirdPartySingleTestExecution','thirdPartyJsonPerformanceResult','getExecutionId','getImageName','getExecutionList', 'getDeviceImageName','thirdPartyMultipleScriptExecution','getExecutionStatus','exportConsolidatedToExcel', 'resultSummary', 'changeDeviceIP'],
			deviceGroup :['getDeviceList','deleteDeviceMethod','createNewDevice'],
			scriptGroup : ['getScriptsByScriptGroup','getScriptsByModule','getAllScriptGroups','deleteScriptGroup','createNewScriptGroup','verifyScriptGroup','getScriptTimeout','getTestJavaScript'],
			module : ['getModuleScriptTimeOut'],
			thunder : ['thirdPartySingleTestExecutionThunder','thirdPartySuiteExecutionThunder', 'thirdPartyMultipleTestExecutionThunder']
		];

    private boolean findAction(actionMap, controllerName, actionName) {
        def c = actionMap[controllerName]
        return (c) ? c.find { (it == actionName || it == '*')} != null : false
    }

    def filters = {
        publica(controller: '*', action: '*') {
            before = {

                if (!controllerName) return true
                
                // Check for public controller/actions
                def isPublic = findAction(publicActions, controllerName, actionName)
				
                if (isPublic){
					def isSecured = false;
					def isRestAuthEnabled = false
					
					String realPath = grailsApplication.parentContext.getResource("/").file
					realPath = realPath+"/"
					Properties prop = new Properties();
					String fileName = realPath+"/fileStore/tm.config";
					File ff = new File(fileName)
					if(ff.exists()){
						InputStream is = new FileInputStream(fileName);
						prop.load(is);
						def value = prop.getProperty(Constants.REST_AUTH_ENABLED);
						if(value){
							if(value.equals("true")){
								isRestAuthEnabled = true
							}
						}
					}
					if(isRestAuthEnabled) {
						isSecured = findAction(securedPublicActions, controllerName, actionName)
					}
					if(isSecured) {
						if (SecurityUtils.subject.principal == null) {
							def isValidUser = false;
							def key = params.key
							def tmUserName = params.tmUserName
							def tmPassword = params.tmPassword
							if(key) {
								isValidUser = UtilityService.validateKey(key);
							}						
							if(tmUserName && tmPassword) {
								def authToken = new UsernamePasswordToken(tmUserName, tmPassword as String)
								try{
									SecurityUtils.subject.login(authToken) 
									isValidUser =  true
									SecurityUtils.subject.logout()
									
								}
								catch (Exception ex){
									println "Error in validation"
								}
							}
							if(isValidUser) {
								return true;
							} else {
								if(key) {
							     	((HttpServletResponse) response).sendError(HttpServletResponse.SC_UNAUTHORIZED, "The token is not valid.");
								}else{
									((HttpServletResponse) response).sendError(HttpServletResponse.SC_UNAUTHORIZED, "Incorrect username or password. Authentication failed.");
								} 
								return false
							}
						}else{
							return accessControl()
						}
					} else {
                        return true
					}
                }
                
                return accessControl()
            }
        }
    }
}
