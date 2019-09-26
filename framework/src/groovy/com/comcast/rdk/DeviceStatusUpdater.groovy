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
package com.comcast.rdk;

import static com.comcast.rdk.Constants.PYTHON_COMMAND
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors
import java.util.concurrent.Future

import javax.servlet.http.HttpServletRequest;

import org.codehaus.groovy.grails.validation.routines.InetAddressValidator

public class DeviceStatusUpdater {

	static final int THREAD_COUNT = 20;
	
	public static transient boolean flag = false;

	/**
	 * Executer service for handling the device status update process.
	 * Currently 10 threads are assigned for this.
	 */
	static ExecutorService executorService = Executors.newFixedThreadPool(THREAD_COUNT)

	/**
	 * Method to trigger the device status update.
	 * @param grailsApplication
	 * @param deviceStatusService
	 */
	public static void updateDeviceStatus(def grailsApplication,def deviceStatusService,def executescriptService){
		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//calldevicestatus_cmndline.py").file
		def absolutePath = layoutFolder.absolutePath
		def deviceStatus
		def deviceId
		String filePath = absolutePath//"${RequestContextHolder.currentRequestAttributes().currentRequest.getRealPath("/")}//fileStore//calldevicestatus_cmndline.py"
		def deviceList 
		
		try {
			if(!flag){
				Device.executeUpdate("update Device m set m.category=:rdkvcat where m.category !=:rdkbcat",[rdkvcat:Category.RDKV,rdkbcat:Category.RDKB]);
				flag = true;
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		
		Device.withTransaction {
			try{
			deviceList = Device.getAll()
			}catch(Exception e){
				e.printStackTrace()
			}
		}
		
		def ipAddress
		NetworkInterface nface
		
		File configFile = grailsApplication.parentContext.getResource("/fileStore/tm.config").file
		
		def nwInterface = getDefaultNetworkInterface(configFile)
		if(nwInterface != null){
			NetworkInterface  netFace = NetworkInterface.getByName(nwInterface)
			if(netFace){
				Enumeration ae = netFace?.getInetAddresses();
				while (ae?.hasMoreElements()) {
					InetAddress address = (InetAddress) ae.nextElement();
					if(InetAddressValidator.getInstance().isValidInet4Address(address.getHostAddress())){
						if(!address.isLoopbackAddress()){
							ipAddress = address.getHostAddress()
						}
					}
				}
			}
		}
		
		if(ipAddress == null ){
			Enumeration ne = NetworkInterface.getNetworkInterfaces();
			while (ne.hasMoreElements()) {
				NetworkInterface netFace = (NetworkInterface) ne.nextElement();
				Enumeration ae = netFace.getInetAddresses();
				while (ae.hasMoreElements()) {
					InetAddress address = (InetAddress) ae.nextElement();
					if(InetAddressValidator.getInstance().isValidInet4Address(address.getHostAddress())){
						if(!address.isLoopbackAddress()){
							ipAddress = address.getHostAddress()
						}
					}
				}
			}
		}
		
		String ipV6Address = InetUtility.getIPAddress(configFile, Constants.IPV6_INTERFACE)
		
		List childDeviceList = []
		deviceList?.each{ dev ->
			def device
			String devIp = ""
			String devName = ""

			try {
				def resultArray = Device.executeQuery("select a.stbIp, a.stbName,a.statusPort from Device a where a.id = :devId",[devId: dev?.id])
				if(resultArray && resultArray?.size() == 1){
					def subArray = resultArray[0]
					if(subArray && subArray?.size() == 3){
						devIp = subArray[0]
						devName = subArray[1]
						int port = Integer.parseInt(subArray[2])
						Device.withTransaction {
							device = Device.findByIdAndStbName(dev?.id,devName)
						}

						def tmIP = ipAddress
						if(ipV6Address != null && device.getCategory() == Category.RDKV &&InetUtility.isIPv6Address(device?.stbIp)){
							tmIP = ipV6Address
						}
						
						String[] cmd = [
							PYTHON_COMMAND,
							filePath,
							devIp,
							port,
							tmIP,
							devName
						]
						Runnable statusUpdator = new StatusUpdaterTask(cmd, device, deviceStatusService,executescriptService,grailsApplication);
						executorService.execute(statusUpdator);
					}
				}
			} catch (Exception e) {
				e.printStackTrace()
			}
		}
	}

	public static String fetchDeviceStatus(def grailsApplication,Device device){		
		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//calldevicestatus_cmndline.py").file

		def absolutePath = layoutFolder.absolutePath

		def deviceStatus

		def deviceId

		String filePath = absolutePath//"${RequestContextHolder.currentRequestAttributes().currentRequest.getRealPath("/")}//fileStore//calldevicestatus_cmndline.py"

		def ipAddress

		NetworkInterface nface
		
		File configFile = grailsApplication.parentContext.getResource("/fileStore/tm.config").file
		
		def nwInterface = getDefaultNetworkInterface(configFile)
		if(nwInterface != null){
			NetworkInterface  netFace = NetworkInterface.getByName(nwInterface)
			if(netFace){
				Enumeration ae = netFace?.getInetAddresses();
				while (ae.hasMoreElements()) {
					InetAddress address = (InetAddress) ae.nextElement();
					if(InetAddressValidator.getInstance().isValidInet4Address(address.getHostAddress())){
						if(!address.isLoopbackAddress()){
							ipAddress = address.getHostAddress()
						}
					}
				}
			}
		}
		
		if(ipAddress == null ){		
			
			Enumeration ne = NetworkInterface.getNetworkInterfaces();
	
			while (ne.hasMoreElements()) {
	
				NetworkInterface netFace = (NetworkInterface) ne.nextElement();
	
				Enumeration ae = netFace.getInetAddresses();
	
				while (ae.hasMoreElements()) {
	
					InetAddress address = (InetAddress) ae.nextElement();
	
					if(InetAddressValidator.getInstance().isValidInet4Address(address.getHostAddress())){
	
						if(!address.isLoopbackAddress()){
	
							ipAddress = address.getHostAddress()
	
						}
	
					}
	
				}
	
			}
		}

		String ipV6Address = InetUtility.getIPAddress(configFile, Constants.IPV6_INTERFACE)
		
		int port = Integer.parseInt(device?.statusPort)
		
		
		def tmIP = ipAddress
		if(ipV6Address != null && device.getCategory() == Category.RDKV &&InetUtility.isIPv6Address(device?.stbIp)){
			tmIP = ipV6Address
		}
		
		String[] cmd = [
			PYTHON_COMMAND,
			filePath,
			device?.stbIp,
			port,
			tmIP,
			device?.stbName
		]

		String outData = ""
		
		try {
			outData =  new ScriptExecutor().executeScript(cmd,1)
			if(outData != null){
				outData = outData.trim()
			}
		} catch (Exception e) {
			e.printStackTrace()
		}

		return outData;

	}
	
	public static getDefaultNetworkInterface(File configFile){
		try {
		Properties prop = new Properties();
		if(configFile.exists()){
			InputStream is = new FileInputStream(configFile);
			prop.load(is);
			def value = prop.getProperty("interface");
			if(value){
				return value
			}
		}
		} catch (Exception e) {
			e.printStackTrace()
		}
		return null
	}
}

