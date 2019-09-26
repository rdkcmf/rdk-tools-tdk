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

import static com.comcast.rdk.Constants.*
import org.hibernate.StaleObjectStateException
import org.junit.internal.runners.statements.FailOnTimeout;

import groovy.sql.Sql
import java.util.Map;

public class DeviceStatusService {
	
	private static final Object LOCK = new Object()
	
	static datasource = 'DEFAULT'
	def executionService
	def dataSource
	def grailsApplication
	def mocaDeviceService
	
	static transactional = false
	
	public static List deviceResetList = []

	/**
	 * Method to update the current status of device in DB.
	 * After device status updation, it will check for moca device availability.
	 * @param device
	 * @param outData
	 */
	public void updateDeviceStatus(final Device device, final String outData ) throws StaleObjectStateException  {
		def deviceStatus
		def deviceInstance
		def deviceId
		def deviceName = ""
		def boxtype
		Device.withTransaction { deviceStat ->
			deviceInstance = Device.findByStbName(device?.stbName)
			deviceId = deviceInstance?.id
			deviceName = deviceInstance?.stbName.toString()
			boxtype = deviceInstance?.boxType
		}
			if(deviceInstance){
				
				if(executionService.deviceAllocatedList.contains(deviceId)){
					deviceStatus = Status.BUSY
				}
				else{
					deviceStatus = getDeviceStatus(outData)
					/*if(outData.equals( Status.BUSY.toString() )){
						deviceStatus = Status.BUSY
					}
					else if(outData.equals( Status.FREE.toString() )){
						deviceStatus = Status.FREE
					}
					else if(outData.equals( Status.NOT_FOUND.toString() )){
						deviceStatus = Status.NOT_FOUND
					}
					else if(outData.equals( Status.HANG.toString() )){
						deviceStatus = Status.HANG
					}
					else if(outData.equals(Status.TDK_DISABLED.toString())){
						deviceStatus = Status.TDK_DISABLED	
					}
					else{
						deviceStatus = Status.NOT_FOUND
					}*/			
				}				
				try {		
					def sql = new Sql(dataSource)	
					synchronized (LOCK) {
						def status = sql.executeUpdate("update device set device_status = ? where stb_name = ? ",[deviceStatus.toString(),deviceName])
					}				

				} catch (Exception e) {			
				}				
				mocaDeviceService?.updateMocaDevices(deviceInstance,boxtype)
			}
	}
	
	/*public void updateOnlyDeviceStatus(final Device device, final String outData ){
		String deviceStatus
		def deviceInstance
		def deviceId
		def deviceName
		//synchronized (LOCK) {
			Device.withTransaction {
				deviceInstance = Device.findByStbName(device?.stbName)
				deviceId = deviceInstance?.id
				deviceName = deviceInstance.stbName

				if(deviceInstance){
					if(executionService.deviceAllocatedList.contains(deviceId)){
						deviceStatus = Status.BUSY
					}
					else{
						deviceStatus = getDeviceStatus(outData)
					}
					try{
						//deviceInstance = Device.findByStbName(device?.stbName)
						deviceInstance.deviceStatus = deviceStatus
						if(!deviceInstance?.save(flush:true,failOnError:true)){
							println "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
							println deviceInstance?.errors?.allErrors
						}
						def sql = new Sql(dataSource)
						synchronized (LOCK) {
							status = sql.executeUpdate("update device set device_status = ? where stb_name = ? ",[deviceStatus.toString(),deviceName])
						}
					}catch(Exception e){
						println " !!!!!!!!!!!!!!!!!! error heree : "+e.message
					}
		//		}
			}
			//println "status : "+Device.findByStbName(device?.stbName)?.deviceStatus
		}
			println "status :   "+Device.findAll().get(0)?.deviceStatus
		
	}*/
	
	public void updateOnlyDeviceStatus(final Device device, final String outData ){
		String deviceStatus
		def deviceInstance
		def deviceId
		def deviceName
		Device.withTransaction {
			deviceInstance = Device.findByStbName(device?.stbName)
			deviceId = deviceInstance?.id
			deviceName = deviceInstance.stbName.toString()
		}
		if(deviceInstance){
			
			if(executionService.deviceAllocatedList.contains(deviceId)){
				deviceStatus = Status.BUSY
			}
			else{
				deviceStatus = getDeviceStatus(outData)
			}

			try{
				Device.withTransaction{
					Device dev = Device.findById(deviceId)
					dev?.deviceStatus = deviceStatus
					dev?.save(flush:true)
				}
				
//				def sql = new Sql(dataSource)
//				def status = sql.executeUpdate("update device set device_status = ? where stb_name = ? ",[deviceStatus.toString(),deviceName])
			}catch(Exception e){
			}
		}
	}
	
	
	/**
	 * Identifies the device status based on input 
	 * @param data
	 * @return
	 */
	def getDeviceStatus(String data){
		def deviceStatus
		data = data.trim()
		switch(data){
			case  Status.BUSY.toString():   deviceStatus = Status.BUSY
				break
			case Status.FREE.toString(): 	deviceStatus = Status.FREE
				break
			case  Status.NOT_FOUND.toString() : deviceStatus = Status.NOT_FOUND
				break
			case  Status.HANG.toString() : deviceStatus = Status.HANG
				break
			case  Status.TDK_DISABLED.toString() : deviceStatus = Status.TDK_DISABLED
				break
			default : deviceStatus = Status.NOT_FOUND
				break
		}
		deviceStatus
	}

	
	def resetIPRule(final Device device){
		def executionResult
		List existingDevices = []
		List newDevices = []
		List deletedDevices = []
		def boxType
		List macIdList = []
		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//calldevicestatus_cmndline.py").file
		def absolutePath = layoutFolder.absolutePath
		def deviceStatus
		def deviceId
		List childDeviceList = []
		List devicesTobeDeleted = []

		Device.withTransaction {
			try {

				boxType = device?.boxType?.type?.toLowerCase()
				if(boxType == "gateway"){

					macIdList.removeAll(macIdList)
					executionResult =  executionService.executeGetDevices(device)   // execute callgetdevices.py

					macIdList = executionService.parseExecutionResult(executionResult)

					int childStbPort
					int childStatusPort
					int childLogTransferPort

					childDeviceList.removeAll(childDeviceList)


					if(macIdList.size() > 0 ){
						macIdList.each{ macId ->
							Device deviceObj = Device.findByMacId(macId)

							Random rand = new Random()
							int max = 100
							def randomIntegerList = []
							int randomVal
							(1..100).each {
								randomVal =  rand.nextInt(max+1)
							}


							if(deviceObj){
								deviceObj.childDevices.each { childDevice -> devicesTobeDeleted << childDevice }


								devicesTobeDeleted.each { childDevice ->
									childDevice.delete(flush:true)
								}
							}

						}
						existingDevices = device.childDevices
						device.childDevices = childDeviceList
						deletedDevices = existingDevices - childDeviceList
						deletedDevices.each{ stbDevice ->

							stbDevice.delete(flush:true)
						}
					}
					else{
						if(executionResult.contains(FOUND_MACID)){

							existingDevices = device.childDevices
							device.childDevices = childDeviceList
							deletedDevices = existingDevices - childDeviceList
							deletedDevices.each{ stbDevice ->

								stbDevice.delete(flush:true)
							}
						}
					}
				}
			}
			catch(Throwable th) {
			}
		}
	}
	
}
