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

import org.apache.catalina.util.Base64;
import org.apache.shiro.SecurityUtils
import org.apache.shiro.crypto.hash.Sha256Hash

import groovy.xml.MarkupBuilder

import java.security.MessageDigest
import java.security.NoSuchAlgorithmException;

import javax.crypto.Cipher
import javax.crypto.spec.SecretKeySpec
import javax.xml.bind.DatatypeConverter;

import org.custommonkey.xmlunit.*


class UtilityService {
	static datasource = 'DEFAULT'
	static String ENCRYPT_KEY = "RDK_TEST_TOOL_KEY";
	
	def scriptService

	def Groups getGroup(){
		def user = User.findByUsername(SecurityUtils.subject.principal)
		def group = Groups.findById(user.groupName?.id)
		return group
	}
	
	
	def String writexmldata(String execName){
		Execution executionInstance = Execution.findByName(execName)
		def executionDevice = ExecutionDevice.findAllByExecution(executionInstance)
		def device = Device.findByStbName(executionInstance?.device)
		
		def writer = new StringWriter()
		def xml = new MarkupBuilder(writer)
		
		xml.TestExecutionResult(name=executionInstance.name status=executionInstance.result)() {
			
			executionDevice.each{ executionDeviceInstance ->
				Device(name=executionDeviceInstance?.device ip=executionDeviceInstance?.deviceIp exectime=executionDeviceInstance?.executionTime status=executionDeviceInstance?.status)
				
				executionDeviceInstance.executionresults.each{ executionResultInstance ->
					Scripts(name=executionResultInstance?.script status=executionResultInstance?.status)
					executionResultInstance.executemethodresults.each{executionResultMthdsInstance ->
						Function(name:executionResultMthdsInstance?.functionName){												
							ExpectedResult(executionResultMthdsInstance?.expectedResult)
							ActualResult(executionResultMthdsInstance?.actualResult)
							Status(executionResultMthdsInstance?.status)
						}
					}
					LogData(executionResultInstance?.executionOutput)
				}
			}		
		}
	}
	
	/**
	 * Method to generate an encrypted key for accessing REST API'S if authentication is required
	 * @param userName
	 * @return
	 */
	def String generateKey (String userName) {
		String combinedKey = userName + ENCRYPT_KEY
		byte[] encryptedCode
		String encoded = "";
		try {
			encryptedCode = combinedKey.getBytes("UTF-8");
			encoded = DatatypeConverter.printBase64Binary(encryptedCode);
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
		return encoded
	}
	
	/**
	 * Method to validate an encrypted key for accessing REST API'S if authentication is required
	 * @param key
	 * @return
	 */
	def static boolean validateKey(String key) {
		byte[] decoded = DatatypeConverter.parseBase64Binary(key);
		String decrypted = "";
		boolean isValid = false;
		try {
			decrypted = new String(decoded, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		String userName = decrypted.replace(ENCRYPT_KEY, "")
		User user = User.findByUsername(userName);
		if(user != null) {
			isValid = true;
		}
		
		return isValid;

	}

}

