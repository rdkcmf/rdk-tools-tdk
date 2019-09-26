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

/**
 * Service class to handle the moca device update
 *
 */
class MocaDeviceService {
	
	static datasource = 'DEFAULT'
	
	def executionService
	
	def grailsApplication
    
	/**
	 * Method to check moca device availability for a device.
	 * Will invoke Port forwading during  for Gateway devices.
	 * Port forwarding has 2 phases.
	 *	1) Get macId of connected devices.
	 *	2) Set routing rules for child devices.
	 *  Get devices will be called every 30 sec and if any new child device connected it will be saved in DB.
	 *  For every new devices, unique execution port, status port and log transfer port will be generated dynamically.
	 *  Routing will be called only once for a device with particular mac id.
	 *  
	 * @param device
	 * @param boxType
	 */
	public void updateMocaDevices(def device1, def boxType ){
		def executionResult
		List existingDevices = []
		List newDevices = []
		List deletedDevices = []
		List macIdList = []

		int childStbPort
		int childStatusPort
		int childLogTransferPort
		int childAgentMonitorPort
		def macIdAppender
		List childDeviceList = []
		Device device
		
		Device.withTransaction{
			device = Device.findById(device1?.id)
		}
		
		try{
			
			def bType
			
			BoxType.withTransaction {
				bType = boxType?.type?.toLowerCase()
			}
			
			if(bType.equals(GATEWAY_BOX)){

				macIdList.removeAll(macIdList) 
				executionResult =  executionService.executeGetDevices(device)   // execute callgetdevices.py

				macIdList = executionService.parseExecutionResult(executionResult)

				childDeviceList.removeAll(childDeviceList)
				if(macIdList.size() > 0 ){

					
					macIdList.each{ macId ->
						Device.withTransaction{
						Device deviceObj = Device.findByMacId(macId)

						Random rand = new Random()
						int max = 100
						def randomIntegerList = []
						int randomVal
						(1..100).each {
							randomVal =  rand.nextInt(max+1)
						}
						macIdAppender = macId.substring(macId.length() - 5, macId.length())
						if(!deviceObj){

							childStbPort = customStbPort +  randomVal
							childStatusPort = customStatusPort +  randomVal
							childLogTransferPort = customLogTransferPort +  randomVal
							childAgentMonitorPort = customAgentMonitorPort +  randomVal
							
							Device childDevice = new Device()
							childDevice.macId = macId
							childDevice.stbName = device.stbName+HYPHEN+BoxType.findByName(XI3_BOX).name+HYPHEN+macIdAppender
							childDevice.stbIp =device.stbIp
							childDevice.boxType = BoxType.findByName(XI3_BOX)
							childDevice.boxManufacturer = BoxManufacturer.findByName(DEFAULT_BOX_MANUFACTURER)
							childDevice.soCVendor = SoCVendor.findByName(DEFAULT_SOCVENDOR)
							childDevice.gatewayIp = device.stbIp
							childDevice.recorderId = device.recorderId

							childDevice?.stbPort = childStbPort
							childDevice?.statusPort = childStatusPort
							childDevice?.logTransferPort = childLogTransferPort
							childDevice?.agentMonitorPort = childAgentMonitorPort
							childDevice?.isChild = 1

							childDevice.save(flush:true)
							//devicegroupService.saveToDeviceGroup(childDevice)

							childDeviceList << childDevice
							device.addToChildDevices(childDevice)
							executionService.executeSetRoute(device, childDevice)   //execute callsetroute.py
						}
						else{
							if(!(deviceObj.gatewayIp?.trim()?.equals(device?.stbIp?.trim()))){
								def oldName = ""
								def newName = ""
									try {
										deviceObj = Device.findByMacId(macId)
										oldName = deviceObj?.stbName
										deviceObj.stbIp =device?.stbIp
										deviceObj.gatewayIp = device?.stbIp
										deviceObj.stbName = device?.stbName+HYPHEN+BoxType.findByName(XI3_BOX)?.name+HYPHEN+macIdAppender
										deviceObj.recorderId = device?.recorderId
										newName = deviceObj.stbName
										if(deviceObj.save(flush:true)){
											try {
												def parentDevice = Device.findByStbIp(deviceObj?.gatewayIp)
												if(parentDevice != null && parentDevice?.childDevices?.id?.contains(deviceObj?.id)){
													def deviceObj1 = parentDevice?.childDevices?.find { it.id == deviceObj?.id }
													parentDevice.removeFromChildDevices(deviceObj1)
												}
												
												if(!device?.childDevices?.id?.contains(deviceObj?.id)){
													deviceObj = Device.findByMacId(macId)
													device.addToChildDevices(deviceObj)
												}
												
											} catch (Exception e) {
												e.printStackTrace()
											}
										}
									} catch (Exception e) {
										e.printStackTrace()
									}
								
								executionService.executeSetRoute(device, deviceObj)
							}else{
								if(DeviceStatusService.deviceResetList.contains(deviceObj?.id)){
									try {
										executionService.executeSetRoute(device, deviceObj)
										DeviceStatusService.deviceResetList.remove(deviceObj?.id)
										Thread.sleep(5000)
										
										String stat = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceObj)
											if(stat.equals(Status.NOT_FOUND.toString())){
												for(int i = 0 ; i < 10 && (stat.equals(Status.NOT_FOUND.toString())) ; i++){
													stat = DeviceStatusUpdater.fetchDeviceStatus(grailsApplication, deviceObj)
													Thread.sleep(2000)
												}
											}
										if(stat.equals(Status.BUSY.toString())){
											executionService.resetAgent(deviceObj)
											Thread.sleep(5000)
										}
									} catch (Exception e) {
										e.printStackTrace()
									}
								}
							}
							childDeviceList << deviceObj
						}
					}
					}
				}
				else{
					Device.withTransaction {
						Device devv = Device.findById(device1?.id)
						if(devv?.childDevices?.size() > 0){
							devv?.childDevices?.each { dev ->
								if(!DeviceStatusService.deviceResetList.contains(dev?.id)){
									DeviceStatusService.deviceResetList.add(dev?.id)
								}
							}
						}
					}
				}
			}
		}
		catch(Exception e){
		}
	}
	
}
