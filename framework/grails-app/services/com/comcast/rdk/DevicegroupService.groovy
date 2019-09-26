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

/**
 * A service class for DeviceGroup domain
 * @author sreejasuma
 */

class DevicegroupService {
	static datasource = 'DEFAULT'
    
    /**
     * Method to save the device to a DeviceGroup, according to the box chosen for execution
     * If the device group exists then add the device to that group.
     * Else create a Device group and add the device to the group.     
     * @param deviceInstance
     * @return
     */
    def saveToDeviceGroup(final Device deviceInstance){
        String boxType = deviceInstance.boxType.name
        def deviceGrpInstance = DeviceGroup.findByName(boxType)
        if(!deviceGrpInstance){   
            deviceGrpInstance = new DeviceGroup()     
            deviceGrpInstance.name = boxType
        }        
        
        deviceGrpInstance?.category = deviceInstance?.category
        deviceGrpInstance?.addToDevices(deviceInstance)
        deviceGrpInstance?.save(flush:true)

    }
    
    /**
     * Checking the status of the device or the device is present in a 
     * device group which is selected to execute, 
     * and if device is free, delete device from the device group to make the
     * fresh update of device. 
     * @author sreejasuma
     */
   
    public boolean checkDeviceStatus(final Device device){
        
        boolean deviceInUse = false
        boolean isAllocatedDeviceGrp = false
        if(device.deviceStatus.equals( Status.BUSY)){
            deviceInUse = true
        }
        else{
            /**
             * Selecting deviceGroups based on whether selected device exists
             * in the device group's and status of the DeviceGroup is Busy.
             * In this case the device cannot be deleted.
             */
            def deviceAllocated = DeviceGroup.where {
                devices { id == device.id } && status == Status.BUSY
            }
            deviceAllocated?.each{
                isAllocatedDeviceGrp = true
                return true
            }
            if(isAllocatedDeviceGrp){
                deviceInUse = true
            }
            else{
                /**
                 * Selecting deviceGroups where the given device is present
                 * And removing the device from the devicegroup
                 */
                def deviceGroups = DeviceGroup.where {
                    devices { id == device.id }
                }
                def deviceInstance
                deviceGroups?.each{ deviceGrp ->
                    deviceInstance = deviceGrp.devices.find { it.id == device.id }
                    if(deviceInstance){
                        deviceGrp?.removeFromDevices(deviceInstance)
                    }
                }
            }
        }
        return deviceInUse
    }
	
	/**
	 * Returns name of selected boxType 
	 * @param boxTypeId
	 * @return
	 */
	public String  getBoxType(boxTypeId){

		BoxType boxType = BoxType.findById(boxTypeId)
		String boxName = boxType.name
		return boxName
	}

	/**
	 * Method to remove the  device reference from execution result objects while deleting the device
	 */
	def updateExecDeviceReference(def device){

		try {
			def exResultList = ExecutionResult.findAllByExecDevice(device)
			exResultList.each {exResult ->
				ExecutionResult.withTransaction{ tran ->
					try {
						ExecutionResult.executeUpdate("update ExecutionResult c set c.execDevice = null  where c.id = :execResultId",
								[execResultId: exResult?.id?.toLong()])
						
					} catch (Exception e) {
						e.printStackTrace()
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
}
