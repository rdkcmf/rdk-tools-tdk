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
 * A class that handles the device creation and device group creation
 * @author sreejasuma
 */
import static com.comcast.rdk.Constants.*
import com.comcast.rdk.Category
import grails.converters.JSON
import java.sql.Timestamp
import java.util.concurrent.ExecutorService
import groovy.xml.StreamingMarkupBuilder
import groovy.xml.MarkupBuilder


import org.apache.shiro.SecurityUtils;
import org.apache.shiro.subject.Subject
import org.springframework.dao.DataIntegrityViolationException
import org.springframework.util.StringUtils;

import com.google.gson.JsonArray
import com.google.gson.JsonObject;

import java.util.concurrent.Executors
import java.util.zip.ZipOutputStream


class DeviceGroupController {

    static allowedMethods = [save: "POST", update: "POST", delete: "POST", updateDevice : "POST"]
    /**
     * Injecting devicegroupService
     */
    def devicegroupService
	def utilityService
	
	private static final String DEVICESTREAM_QUERY = "delete DeviceStream d where d.device = :instance1"
	private static final String DEVICERADIOSTREAM_QUERY = "delete DeviceRadioStream d where d.device = :instance1"
	private static final String GATEWAY = "Gateway"
	
    static ExecutorService executorService = Executors.newCachedThreadPool()
    def executionService
	def grailsApplication
	def logZipService
	
	def index(){
		redirect(action: "list")
	}

    /**
     * Method to list the device groups.
     * When list method is called as ajax from devicegrp_resolver.js with the 
     * params?.streamtable value only the streamlist page will be rendered.
     */    
    def list = {	
		/**
		 * Invoked from 
		 */
        if(params?.streamtable) {
            def result = [url: getApplicationUrl(), streamingDetailsInstanceList: StreamingDetails.list(),radioStreamingDetails : RadioStreamingDetails.findAll(), streamingDetailsInstanceTotal: StreamingDetails.count(), streamingDetailsInstanceTotal: RadioStreamingDetails.count()]
			 render view:"streamlist", model:result
            return
        }		
		def groupsInstance = utilityService.getGroup()
		def deviceInstanceListSTB = getDevicesList(groupsInstance, [category:RDKV])
		
		def deviceInstanceListModem = getDevicesList(groupsInstance, [category:RDKB])
		
		def deviceGrpInstanceListSTB = getDeviceGroupList(groupsInstance, [category:RDKV])
		
		def deviceGrpInstanceListModem = getDeviceGroupList(groupsInstance, [category:RDKB])
		
		[url: getApplicationUrl(), deviceGroupsInstance : params?.deviceGroupsInstance, 
			 deviceInstanceListSTB : deviceInstanceListSTB, deviceInstanceListModem : deviceInstanceListModem,
			 deviceInstanceSTBTotal : deviceInstanceListSTB.size(), deviceInstanceModemTotal : deviceInstanceListModem.size(),  
			 deviceGrpInstanceListSTB : deviceGrpInstanceListSTB, deviceGrpInstanceListModem : deviceGrpInstanceListModem, 
			 deviceGrpInstanceSTBTotal : deviceGrpInstanceListSTB.size(), deviceGrpInstanceModemTotal : deviceGrpInstanceListModem.size(),
			 deviceId: params.deviceId, deviceGroupId: params.deviceGroupId]
		
    }

    /**
     * Method to create a device group.
     */
    def create() {
		def devices = [] 
		def deviceCategory = Utility.getCategory(params?.category)
		devices = Device.findAllByCategory(deviceCategory)
        [deviceGroupsInstance: new DeviceGroup(params), category:params?.category, devices:devices]
    }

    /**
     * Method to save a device group.
     */
    def save() {
        def deviceGroupsInstance = new DeviceGroup(params)
        if(DeviceGroup.findByName(params?.name)){
            flash.message = flash.message = message(code: 'devicegrp.already.exists') 
            redirect(action: "list")
            return
        }
		deviceGroupsInstance.groups = utilityService.getGroup()
		if(params?.devices != null)
		{
        if (!deviceGroupsInstance.save(flush: true)) {
            log.info("Device Group Not Created "+deviceGroupsInstance?.name)
            log.error( deviceGroupsInstance.errors)
            redirect(action: "list")
            return
        }
        log.info("Device Group Saved "+deviceGroupsInstance?.name)
        flash.message = message(code: 'default.created.message', args: [
            message(code: 'deviceGroups.label', default: 'DeviceGroups'),
            deviceGroupsInstance.name
        ])
		}
		else
		{
			/*flash.message =message(code: 'default.not.created.message', args: [
            message(code: 'deviceGroups.label', default: 'DeviceGroups'),
            deviceGroupsInstance.name
        ])*/
			flash.message = "Please select the devices to save DeviceGroup"
		}
		
        redirect(action: "list")
    }

    /**
     * Method to show a device group.
     */
    def show(Long id) {
        def deviceGroupsInstance = DeviceGroup.get(id)
        if (!deviceGroupsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                id
            ])
            redirect(action: "list")
            return
        }
        [deviceGroupsInstance: deviceGroupsInstance]
    }

    /**
     * Method to edit a device group.
     */
    def edit(Long id) {
        def deviceGroupsInstance = DeviceGroup.get(id)
        if (!deviceGroupsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                id
            ])
            redirect(action: "list")
            return
        }
        [deviceGroupsInstance: deviceGroupsInstance]
    }

    /**
     * Method to update a device group.
     */
    def update(Long id, Long version) {
        def deviceGroupsInstance = DeviceGroup.get(id)

        if (!deviceGroupsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                id
            ])
            redirect(action: "list")
            return
        }
        if (version != null) {
            if (deviceGroupsInstance.version > version) {
                deviceGroupsInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
                        [
                            message(code: 'deviceGroups.label', default: 'DeviceGroup')] as Object[],
                        "Another user has updated this DeviceGroups while you were editing")
                redirect(action: "list")
                return
            }
        }
        deviceGroupsInstance.name = params?.name
        deviceGroupsInstance.devices = []
        if (!deviceGroupsInstance.save(flush: true)) {
            redirect(action: "list", params : [deviceGroupsInstance: deviceGroupsInstance])
            return
        }
        else{
            log.info("Device Group Updated "+deviceGroupsInstance?.name)
            def device
            if((params?.devices) instanceof String ){
                device = Device.findByStbName(params?.devices)
                deviceGroupsInstance.addToDevices(device)
            }
            else{
                params.devices.each{ name ->
                    device = Device.findByStbName(name)
                    deviceGroupsInstance.addToDevices(device)
                }
            }
        }

        flash.message = message(code: 'default.updated.message', args: [
            message(code: 'deviceGroups.label', default: 'DeviceGroup'),
            deviceGroupsInstance.name
        ])
		redirect(action: "list", params: [deviceGroupId: params.id])
    }

	/**
	 * Method to delete a device group
	 * @return
	 */
    def delete() {
        def deviceGroupsInstance = DeviceGroup.get(params?.id)
        if (!deviceGroupsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                params?.id
            ])
            redirect(action: "list")
            return
        }

        try {
            deviceGroupsInstance.delete(flush: true)
            flash.message = message(code: 'default.deleted.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                deviceGroupsInstance?.name
            ])
            redirect(action: "list")
        }
        catch (DataIntegrityViolationException e) {
            flash.message = message(code: 'default.not.deleted.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                deviceGroupsInstance?.name
            ])
            redirect(action: "list")
        }
    }

	/**
	 * Method to delete a device group
	 * @return
	 */
    def deleteDeviceGrp() {

        Long id = params.id as Long
        def deviceGroupsInstance = DeviceGroup.get(id)
        if (!deviceGroupsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                deviceGroupsInstance?.id
            ])
            redirect(action: "list")
            return
        }
        try {
            deviceGroupsInstance.delete(flush: true)
            flash.message = message(code: 'default.deleted.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                deviceGroupsInstance?.name
            ])
            render("success")
        }
        catch (DataIntegrityViolationException e) {
            flash.message = message(code: 'default.not.deleted.message', args: [
                message(code: 'deviceGroups.label', default: 'DeviceGroups'),
                deviceGroupsInstance?.name
            ])
            redirect(action: "list")
        }
    }

    /**
     * Create a new device
     * @return
     */
    def createDevice() {
        def devices = Device.where { boxType { type == GATEWAY } && category==Utility.getCategory(params?.category) }
        [url : getApplicationUrl() ,deviceInstance: new Device(params), gateways : devices, editPage : false, category:params?.category, streamingDetailsInstanceTotal: StreamingDetails.count(),radioStreamingDetailsInstanceTotal: RadioStreamingDetails.count()]
    }

    /**
     * Save a new device
     * @return
     */
    def saveDevice() {
        if(Device.findByStbName(params?.stbName)){
            flash.message = message(code: 'stbname.already.exists')
			render(flash.message)
            return
        }
		
		def stbIps = Device.findAllByStbIpAndIsChild(params?.stbIp, 0)
		
		if(stbIps){
			flash.message = message(code: 'stbip.already.exists')
			render(flash.message)
			return
		}
		
		if(params?.macId){
		if(Device.findByMacId(params?.macId)){
			flash.message = "Mac Id already in use. Please use a different Name."
			render("Mac Id already in use. Please use a different Name.")
			return
		}
		}
		
		BoxType boxType = BoxType.findById(params?.boxType?.id)	
		String newBoxType = boxType?.type?.toLowerCase()
		
		if ((newBoxType.equals( BOXTYPE_GATEWAY ) || newBoxType.equals( BOXTYPE_STANDALONE_CLIENT )) && params.category == RDKV){
			String recId =  params?.recorderId
			if(recId?.trim()?.length() ==  0 ){
				flash.message = "Recorder id should not be blank"
				render(flash.message)
			    return
			}
		}
        
        /**
         * Check whether streams are present
         * and there is no duplicate OcapIds
         */
		if((newBoxType.equals( BOXTYPE_GATEWAY ) || newBoxType.equals(BOXTYPE_STANDALONE_CLIENT)) && params.category == RDKV)
		{
        if((params?.streamid)){
			
			if(checkDuplicateOcapId(params?.ocapId)){
                flash.message = message(code: 'duplicate.ocap.id')
				render(flash.message)
                return
            }
        }
		}
		def deviceInstance = new Device(params)
		int enabled = 1;
		int notEnabled = 0;
		deviceInstance.isThunderEnabled = params?.thunderEnabled == "on"? enabled : notEnabled
		deviceInstance.groups = utilityService.getGroup()
		deviceInstance.category = Utility.getCategory(params?.category)
        if (deviceInstance.save(flush: true)) {
            devicegroupService.saveToDeviceGroup(deviceInstance)
			if((newBoxType.equals( BOXTYPE_GATEWAY ) || newBoxType.equals(BOXTYPE_STANDALONE_CLIENT)) && deviceInstance.category == Category.RDKV){
				saveDeviceStream(params?.streamid, params?.ocapId, deviceInstance)
			}
        }
        else{
            flash.message = message(code: 'default.not.created.message', args: [
            message(code: 'device.label', default: 'Device')])			
			render(flash.message)
            return
        }

      flash.message = message(code: 'default.created.message', args: [
            message(code: 'device.label', default: 'Device'),
            deviceInstance.stbName
        ])
		render(message(code: 'default.created.message', args: [
            message(code: 'device.label', default: 'Device'),
            deviceInstance.stbName
        ]))
		
    }

    /**
     * Edit device
     * @return
     */
    def editDevice(Long id, final String flag) {
		def deviceInstance = Device.get(id)
		if (!deviceInstance) {
			return
		}
        def devices = Device.where { boxType { type == GATEWAY } && category == deviceInstance?.category }

		def blankList = []
        def deviceStream = DeviceStream.findAllByDevice(deviceInstance)
		def radiodeviceStream = DeviceRadioStream.findAllByDevice(deviceInstance)
		boolean showBlankRadio = (radiodeviceStream ==null || radiodeviceStream?.size() == 0)
		if(showBlankRadio){
			def all = RadioStreamingDetails.findAll()
			all.each {
				blankList.add(it)
			}
		}
        [url : getApplicationUrl(),deviceInstance: deviceInstance, flag : flag, showBlankRadio:showBlankRadio,blankList:blankList,gateways : devices, deviceStreams : deviceStream,radiodeviceStreams:radiodeviceStream, editPage : true, uploadBinaryStatus: deviceInstance.uploadBinaryStatus, id: id, category:deviceInstance?.category, streamingDetailsInstanceTotal: StreamingDetails.count(),radioStreamingDetailsInstanceTotal: RadioStreamingDetails.count()]
    }

    /**
     * Update device
     * @return
     */
    def updateDevice(Long id, Long version) {
        def deviceInstance = Device.get(id)

        if (!deviceInstance) {
            flash.message = message(code: 'default.not.found.message', args: [
                message(code: 'device.label', default: 'Device'),
                id
            ])
            redirect(action: "list")
            return
        }

        if (version != null) {
            if (deviceInstance.version > version) {
                deviceInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
                        [
                            message(code: 'device.label', default: 'Device')] as Object[],
                        "Another user has updated this Device while you were editing")
				redirect(action: "list")
                return
            }
        }
		
		
		
		
        boolean deviceInUse = devicegroupService.checkDeviceStatus(deviceInstance)
        if(deviceInUse){
			flash.message = message(code: 'device.not.update', args: [deviceInstance.stbIp])
            redirect(action: "list")
            return
        }
        else{
			
			String currentBoxType = deviceInstance?.boxType?.type?.toLowerCase()
			
			BoxType boxType = BoxType.findById(params?.boxType?.id)
			
			String newBoxType = boxType?.type?.toLowerCase()
		   String recId=""
			if ((newBoxType.equals( BOXTYPE_GATEWAY ) || newBoxType.equals(BOXTYPE_STANDALONE_CLIENT)) && deviceInstance.category==Category.RDKV)  {
				if(currentBoxType.equals( BOXTYPE_GATEWAY) || currentBoxType.equals( BOXTYPE_STANDALONE_CLIENT)){
					recId =  params?.recorderIdedit
				}else if(currentBoxType.equals(BOXTYPE_CLIENT) && newBoxType.equals( BOXTYPE_GATEWAY ) ){
				recId =  params?.recorderIdedit
				}else{
					recId = ""
				}
				if(recId?.trim()?.length() ==  0 ){
					flash.message = "Recorder id should not be blank"
					redirect(action: "list", params: [deviceId: params.id])
					return
				}
			}
			

            deviceInstance.properties = params
			int enabled = 1;
			int notEnabled = 0;
			deviceInstance.isThunderEnabled = params?.thunderEnabled == "on"? enabled : notEnabled
			if(deviceInstance?.category == Category.RDKV){
				if(currentBoxType.equals( BOXTYPE_CLIENT )){
					if(newBoxType.equals( BOXTYPE_CLIENT )){
						deviceInstance.gatewayIp = params?.gatewayIp
						deviceInstance.recorderId = ""
						DeviceStream.executeUpdate(DEVICESTREAM_QUERY,[instance1:deviceInstance])
						DeviceRadioStream.executeUpdate("delete DeviceRadioStream d where d.device = :instance1",[instance1:deviceInstance])
					}
					else{
						deviceInstance.gatewayIp = ""
						deviceInstance.recorderId = params?.recorderIdedit
					}
				}
				else{
					if(currentBoxType.equals( BOXTYPE_GATEWAY ) || currentBoxType.equals( BOXTYPE_STANDALONE_CLIENT )){
						if(newBoxType.equals( BOXTYPE_CLIENT )){
							deviceInstance.gatewayIp = params?.gatewayIpedit
							deviceInstance.recorderId = ""
							DeviceStream.executeUpdate(DEVICESTREAM_QUERY,[instance1:deviceInstance])
							DeviceRadioStream.executeUpdate("delete DeviceRadioStream d where d.device = :instance1",[instance1:deviceInstance])
						}else  if(currentBoxType.equals( BOXTYPE_STANDALONE_CLIENT ) && newBoxType.equals( BOXTYPE_STANDALONE_CLIENT )){
							deviceInstance.gatewayIp = params?.gatewayIp
							deviceInstance.recorderId = params?.recorderIdedit
						}
						else{
							deviceInstance.gatewayIp = ""
							deviceInstance.recorderId = params?.recorderIdedit
						}
					}
				}
			}
			
            if (!deviceInstance.save(flush: true)) {
                devicegroupService.saveToDeviceGroup(deviceInstance)
                redirect(action:"list")
                return
            }
           
           DeviceStream deviceStream

			if(deviceInstance?.category == Category.RDKV){
				if(currentBoxType.equals( BOXTYPE_CLIENT )){
					if(newBoxType.equals( BOXTYPE_GATEWAY) || newBoxType.equals( BOXTYPE_STANDALONE_CLIENT )){
						/**
						 * Check whether streams are present
						 * and there is no duplicate OcapIds
						 */
						if((params?.streamid)){

							if(checkDuplicateOcapId(params?.ocapId)){
								flash.message = message(code: 'duplicate.ocap.id')
								redirect(action:"list")
								return
							}
						}

						saveDeviceStream(params?.streamid, params?.ocapId, deviceInstance)
					}
				}
				else{
					if(deviceInstance.boxType.type.toLowerCase().equals( BOXTYPE_GATEWAY ) || deviceInstance.boxType.type.toLowerCase().equals( BOXTYPE_STANDALONE_CLIENT )  ){
						/**
						 * Check whether streams are present
						 * and there is no duplicate OcapIds
						 */
						if((params?.streamid)){

							if(checkDuplicateOcapId(params?.ocapId)){
								flash.message = message(code: 'duplicate.ocap.id')
								redirect(action:"list")
								return
							}
						}
						saveDeviceStream(params?.streamid, params?.ocapId, deviceInstance)
					}
				}
			}

            devicegroupService.saveToDeviceGroup(deviceInstance)
            flash.message = message(code: 'default.updated.message', args: [
                message(code: 'device.label', default: 'Device'),
                deviceInstance.stbName
            ])
        }

		redirect(action: "list", params: [deviceId: params.id])
    }
	
	/**
	 * Check for duplicate ocapid's
	 * @param ocapIdList
	 * @return
	 */
	def boolean checkDuplicateOcapId(def ocapIdList){
		boolean isDuplicate = false
		int ocapIdSize = ocapIdList.size()
		Set setOcapId =  ocapIdList
		int setSize = setOcapId.size()
		if(setSize < ocapIdSize){
			isDuplicate = true
		}
		return isDuplicate
	}
	
	def boolean validateOcapIds(def streams, def ocapIdList){
		boolean valid = true
		int streamSize = StreamingDetails?.list().size()
		streamSize += RadioStreamingDetails?.list().size()
		if(streams?.size() == streamSize){
			int ocapIdSize = streams.size()
			Set setOcapId =  streams
			int setSize = setOcapId.size()
			if(setSize < ocapIdSize){
				valid = false
			}else{
				valid =  true
			}
		}else{
			valid = false
		}
		return valid
	}

    /**
     * Save device specific stream details
     * @return
     */
    def saveDeviceStream(final def streamIdList, final def ocapIdList, final Device deviceInstance){
		def deviceStreamList = DeviceStream.findAllByDevice(deviceInstance)		
		if(deviceStreamList?.size() > 0){
			DeviceStream.executeUpdate("delete DeviceStream d where d.device = :instance1",[instance1:deviceInstance])
		}
		
		def deviceRadioStreamList = DeviceRadioStream.findAllByDevice(deviceInstance)
		if(deviceRadioStreamList?.size() > 0){
			DeviceRadioStream.executeUpdate("delete DeviceRadioStream d where d.device = :instance1",[instance1:deviceInstance])
		}
				
        DeviceStream deviceStream
        StreamingDetails streamingDetails

		for(int i = 0; i < streamIdList?.size() ; i++){

			def streamIdListIToString = streamIdList[i].toString()
			if(streamIdListIToString.startsWith("R")){
				def rStreamingDetails = RadioStreamingDetails.findByStreamId(streamIdListIToString)
				def rDeviceStream = new DeviceRadioStream()
				rDeviceStream.device = deviceInstance
				rDeviceStream.stream = rStreamingDetails
				rDeviceStream.ocapId = ocapIdList[i]
				if(!(rDeviceStream.save(flush:true))){
				}
			}else{
				streamingDetails = StreamingDetails.findByStreamId(streamIdListIToString)
				deviceStream = new DeviceStream()
				deviceStream.device = deviceInstance
				deviceStream.stream = streamingDetails
				deviceStream.ocapId = ocapIdList[i]
				if(!(deviceStream.save(flush:true))){
				}
			}
		}
    }
	
    /**
     * Delete device
     * @return
     */
	def deviceDelete(Long id) {
		List devicesTobeDeleted = []

		def deviceInstance = Device.get(id)
		if (!deviceInstance) {

			redirect(action: "list")
			return
		}
		boolean deviceInUse = devicegroupService.checkDeviceStatus(deviceInstance)
		if(deviceInUse){
			flash.message = message(code: 'device.not.update', args: [deviceInstance.stbIp])
			redirect(action: "list")
		}
		else{
			try {

				def deviceDetailsList = DeviceDetails.findAllByDevice(deviceInstance)

				if(deviceDetailsList?.size() > 0){
					DeviceDetails.executeUpdate("delete DeviceDetails d where d.device = :instance1",[instance1:deviceInstance])
				}

				deviceInstance.childDevices.each { childDevice ->
					devicesTobeDeleted << childDevice?.id
				}

				DeviceStream.executeUpdate(DEVICESTREAM_QUERY,[instance1:deviceInstance])
				def list1 = DeviceRadioStream.findAllByDevice(deviceInstance)
				if(list1?.size()>0){
					DeviceRadioStream.executeUpdate("delete DeviceRadioStream d where d.device = :instance1",[instance1:deviceInstance])
				}
				devicegroupService.updateExecDeviceReference(deviceInstance)
				//DeviceGroup.executeUpdate("delete DeviceGroup d where d.device = :instance1",[instance1:deviceInstance])

				if(deviceInstance?.isChild == 1){
					try {
						def devices = Device.findAll()
						devices?.each{ device ->
							def devInstance = device.childDevices.find { it.id == deviceInstance.id }
							if(devInstance){
								Device.withTransaction {
									Device parentDevice = Device.findById(device?.id)
									parentDevice.removeFromChildDevices(deviceInstance)
								}
							}
						}
					} catch (Exception e) {
						e.printStackTrace()
					}
				}

				try {
					if(deviceInstance?.category?.toString().equals(RDKB)){
						def path = request.getSession().getServletContext().getRealPath(FILE_SEPARATOR)
						def isConfigFileExeists = Utility.isConfigFileExists(path,deviceInstance.stbName)
						if(isConfigFileExeists){
							File toDelete = new File(Utility.getConfigFilePath(path,deviceInstance.stbName))
							toDelete.delete()
						}
					}
					if(!deviceInstance.delete(flush: true)){
							Device.withTransaction {
								Device dev = Device.findById(deviceInstance?.id)
								if(dev){
									dev?.delete(flush: true)
								}
							}
					}
				} catch (Exception e) {
					Device.withTransaction {
						Device dev = Device.findById(deviceInstance?.id)
						if(dev){
							dev?.delete(flush: true)
						}
					}
				}
				devicesTobeDeleted.each { childDeviceId ->
					Device childDevice = Device.findById(childDeviceId)
					devicegroupService.updateExecDeviceReference(childDevice)
					try {
						def status
						Device.withTransaction {
							status = childDevice.delete(flush: true)
						}

						if(!status){
								Device.withTransaction {
									Device dev = Device.findById(childDevice?.id)
									if(dev){
										dev?.delete(flush: true)
									}
								}
						}
					} catch (Exception e) {
						Device.withTransaction {
							Device dev = Device.findById(childDevice?.id)
							if(dev){
								dev?.delete(flush: true)
							}
						}
					}
				}

				flash.message = message(code: 'default.deleted.message', args: [
					message(code: 'device.label', default: 'Device'),
					deviceInstance.stbName
				])
				redirect(action: "list")
			}
			catch (DataIntegrityViolationException e) {
				flash.message = message(code: 'default.not.deleted.message', args: [
					message(code: 'device.label', default: 'Device'),
					deviceInstance.stbName
				])
				redirect(action: "list")
			}
		}
	}
	def deleteDeviceWithName(final String device1)
	{
		def deviceName=Device?.findByStbName(device1)
		try
			{
				def deviceList = Device.list()
				deviceList?.each{ device ->
					if(device1 == device)
					{
					
					}
					else
					{
						def deviceList1 = DeviceGroup.list()
						deviceList1.each{device12 ->
							
						}
					}				
					
				}
			
			}
			catch(Exception e)
			{
					e.printStackTrace()
			}
		
		render "deleteDevice"
		
	}
	
	/**
	 * Delete multiple devices
	 * @return
	 */
	def deleteDevices() {
		List deviceList = params.deviceList?.toString()?.split(",")
		if(deviceList != null && deviceList.size() > 0) {
			for (int i=0; i<deviceList.size(); i++) {
				params.id = deviceList[i]
				deleteDevice();
			}
		}
		redirect(action: "list")
	}

    /**
     * Delete device
     * @return
     */
    def deleteDevice() {
        Long id = params.id as Long
        def deviceInstance = Device.get(id)
		List devicesTobeDeleted = []

        boolean deviceInUse = devicegroupService.checkDeviceStatus(deviceInstance)
        if(deviceInUse){
			flash.message = message(code: 'device.not.update', args: [deviceInstance.stbIp])
            render(flash.message)
        }
        else{
			try {
				
				def deviceDetailsList = DeviceDetails.findAllByDevice(deviceInstance)
				
				if(deviceDetailsList?.size() > 0){
					DeviceDetails.executeUpdate("delete DeviceDetails d where d.device = :instance1",[instance1:deviceInstance])
				}
				

				deviceInstance.childDevices.each { childDevice -> devicesTobeDeleted << childDevice?.id }
				

				DeviceStream.executeUpdate(DEVICESTREAM_QUERY,[instance1:deviceInstance])
				DeviceRadioStream.executeUpdate("delete DeviceRadioStream d where d.device = :instance1",[instance1:deviceInstance])
				devicegroupService.updateExecDeviceReference(deviceInstance)
				
				if(deviceInstance.isChild == 1){
					try {
						def devices = Device.findAll()
					devices?.each{ device ->
						def devInstance = device.childDevices.find { it.id == deviceInstance.id }
						if(devInstance){
							Device.withTransaction {
								Device parentDevice = Device.findById(device?.id)
								parentDevice.removeFromChildDevices(deviceInstance)
							}
						}
					}
					} catch (Exception e) {
						e.printStackTrace()
					}
					
				}
				try {
					if(deviceInstance?.category?.toString().equals(RDKB)){
						def path = request.getSession().getServletContext().getRealPath(FILE_SEPARATOR)
						def isConfigFileExeists = Utility.isConfigFileExists(path,deviceInstance.stbName)
						if(isConfigFileExeists){
							File toDelete = new File(Utility.getConfigFilePath(path,deviceInstance.stbName))
							toDelete.delete()
						}
					}
					if(!deviceInstance.delete(flush: true)){
							Device.withTransaction {
								Device dev = Device.findById(deviceInstance?.id)
								if(dev){
										if(!dev?.delete(flush: true)){
											
										}
								}
							}
					}
				} catch (Exception e) {

						Device.withTransaction {
							Device dev = Device.findById(deviceInstance?.id)
							if(dev){
								if(!dev?.delete(flush: true)){

								}
							}
						}

				}
					devicesTobeDeleted.each { childDeviceId ->

						Device childDevice = Device.findById(childDeviceId)
						devicegroupService.updateExecDeviceReference(childDevice)

						try {
							def status
							Device.withTransaction {
								status = childDevice.delete(flush: true)
							}
							if(!status){
									Device.withTransaction {
										Device dev = Device.findById(childDevice?.id)
										if(dev){
											dev?.delete(flush: true)
										}
									}
							}
						} catch (Exception e) {
								Device.withTransaction {
									Device dev = Device.findById(childDevice?.id)
									if(dev){
										dev?.delete(flush: true)
									}
								}
						}
					}

				flash.message = message(code: 'default.deleted.message', args: [
					message(code: 'device.label', default: 'Device'),
					deviceInstance.stbName
				])
				render("success")
			}
            catch (DataIntegrityViolationException e) {
                flash.message = message(code: 'default.not.deleted.message', args: [
                    message(code: 'device.label', default: 'Device'),
                    deviceInstance.stbName
                ])
                render("Exception")
            }
        } 
    }

    /**
     * Method to get the current url and to create
     * new url upto the application name
     * @return
     */
    def String getApplicationUrl(){
        String currenturl = request.getRequestURL().toString();
        String[] urlArray = currenturl.split( URL_SEPERATOR );
        String url = urlArray[INDEX_ZERO] + DOUBLE_FWD_SLASH + urlArray[INDEX_TWO] + URL_SEPERATOR + urlArray[INDEX_THREE]
        return url
    }
    
    /**
     * Get the type of box from the box selected
     * @return
     */
    def getBoxType(){
        List boxTypes = []
        BoxType boxType = BoxType.findById(params?.id)
        //boxTypes.add( boxType?.type?.toLowerCase()?.trim() )
		boxTypes.add( [type:boxType?.type?.toLowerCase()?.trim(), category:boxType?.category?.name()] )
        render boxTypes as JSON
    }

	/**
	 * Method to upload binary files to box.
	 * Invoked by an ajax call.
	 * Executes expect script with required parameters.
	 *  
	 * @return
	 */
	def uploadBinary(){

		String boxIp = params?.boxIp
		String username = params?.username
		String password = params?.password
		String systemPath = params?.systemPath
		String systemIP = params?.systemIP
		String boxpath = params?.boxpath

		List uploadResult = uploadBinaries(boxIp, username, password, systemPath, systemIP, boxpath)
		render uploadResult as JSON
	}

	
	def uploadBinaries(final String boxIp, final String username, final String password, final String systemPath,
		final String systemIP, final String boxpath){
		
		String outputData = null
		List uploadResult = []
		String EXPECT_COMMAND = KEY_EXPECT
		String  absolutePath
		
		def device = Device.findByStbIp(boxIp)
		String boxType = device?.boxType?.name
		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//uploadbinary.exp").file
		absolutePath = layoutFolder.absolutePath
		try {

			String[] cmd = [
				EXPECT_COMMAND,
				absolutePath,
				boxType,
				boxIp,
				systemIP,
				username,
				password,
				systemPath,
				boxpath
			]

			Device deviceInstance = Device.findByStbIp(boxIp);

			ScriptExecutor scriptExecutor = new ScriptExecutor()
			outputData = scriptExecutor.executeCommand(cmd, deviceInstance)
			uploadResult = Arrays.asList(outputData.split("\\r?\\n"))

			if(uploadResult.contains(KEY_BINARYTRANSFER)){
				deviceInstance.uploadBinaryStatus = UploadBinaryStatus.SUCCESS
			}
			else{
				deviceInstance.uploadBinaryStatus = UploadBinaryStatus.FAILURE
			}

			return uploadResult
		} catch (Exception ex) {
			ex.printStackTrace();
		}
	}
	
	
	def uploadAgentBinaries( final String systemIP, final String systemPath, final String username, final String password, 
		final String boxIp, final String boxpath){
		List uploadResult = uploadBinaries(boxIp, username, password, systemPath, systemIP, boxpath)
		List resultList = []
		def cnt = 0
		if(uploadResult){
			cnt = uploadResult?.size()
			resultList = uploadResult[cnt--]
		}
		render resultList as JSON		
	}
	
	
	/**
	 * Method to check whether device with same IP address exist or not. If yes returns the id of device
	 * @return
	 */
	def fetchDevice(){

		List deviceInstanceList = []
		Device deviceInstance = Device.findByStbName(params.stbName)
		if(deviceInstance){
			deviceInstanceList.add(deviceInstance.id)
		}
		render deviceInstanceList as JSON
	}
	
	/** REST method to retrieve the device info
	 * @param boxType
	 * @return
	 */
	def getDeviceList(String boxType){
		JsonObject deviceJson = new JsonObject()
		try {
			JsonArray devArray = new JsonArray()
			def devList
			BoxType bb
			if(boxType){
				bb = BoxType.findByName(boxType)
				if(bb){
					devList = Device.findAllByBoxType(bb)
				}
			}else{
				devList = Device.list()
			}

			if(boxType && !bb){
				deviceJson.addProperty("status", "failure")
				deviceJson.addProperty("remarks", "no box type found with name "+boxType)
			}else{
				if(devList){
					devList?.each{ dev ->
						JsonObject device = new JsonObject()
						device.addProperty("name", dev?.stbName)
						device.addProperty("boxtype", dev?.boxType?.name)						
						//adding category of device - broadband or video
						device.addProperty("category", dev?.category?.toString())
						
						if(dev?.boxType?.type?.equals("Client")){
							if(dev?.isChild == 1){
								device.addProperty("macid", dev?.macId)
								device.addProperty("mocachild", "true")
								if(dev?.gatewayIp){
									def devv = Device?.findByStbIpAndIsChild(dev?.gatewayIp,0)
									//device.addProperty("gateway", devv?.stbName)
									if(devv){
										device.addProperty("gateway", devv?.stbName)
								  }else{
										 Device gwDev = findGatewayDevice(dev)
										 if(gwDev){
											   device.addProperty("gateway", gwDev?.stbName)
										}else{
											   device.addProperty("gateway", "not available")
										}
								  }
								}
							}else{
								device.addProperty("ip", dev?.stbIp)
								device.addProperty("mocachild", "false")
								device.addProperty("ip", dev?.stbIp)
								if(dev?.gatewayIp){
									device.addProperty("gateway", dev?.gatewayIp)
								}
							}
							
						}else{
							device.addProperty("ip", dev?.stbIp)
						}
						devArray.add(device)
					}
				}
				deviceJson.add("devices",devArray)
			}
		} catch (Exception e) {
			log.info "ERROR "+e.getMessage()
			e.printStackTrace()
		}
		render deviceJson
	}
	
	/**
	 * Function for finding the Gateway device 
	 * @param device
	 * @return
	 */	
	def findGatewayDevice(Device device){
		def btList = BoxType.findAllByType("Gateway")
		btList?.each { bt ->
			def devList = Device.findAllByBoxType(bt)
			devList?.each { dev ->
				if(dev?.childDevices?.contains(device)){
					return dev;
				}
			}
		}
		return null
	}
	
	/**
	 * REST API used to the delete device
	 * @param deviceName
	 * @return
	 */
	
	def deleteDeviceMethod(final String deviceName){
		JsonObject deviceObj = new JsonObject()
		try{
			Subject currentUser = SecurityUtils.getSubject()
			if(currentUser?.hasRole('ADMIN')){
				Device dev1 = Device.findByStbName(deviceName)
				if(dev1){
					def deviceInstance = dev1?.id

					boolean deviceInUse = devicegroupService.checkDeviceStatus(dev1)
					if(deviceInUse){
						deviceObj?.addProperty("STATUS","FAILURE ")
						deviceObj?.addProperty("Remarks", "Device is busy, unable to delete")
					}
					else{
						if(deleteDeviceObject(dev1)){
							deviceObj?.addProperty("status","SUCCESS")
							deviceObj?.addProperty("remarks", "successfully deleted the device ")
						}else{
							deviceObj?.addProperty("status","FAILURE")
							deviceObj?.addProperty("remarks", "failed to delete device")
						}
					}
				}else{
					deviceObj?.addProperty("status","FAILURE")
					deviceObj?.addProperty("remarks", "no device found with name "+deviceName)
				}
			}else{
				deviceObj?.addProperty("status", "FAILURE")
				if(currentUser?.principal){
					deviceObj?.addProperty("remarks","current user ${currentUser?.principal} don't have permission to delete device" )
				}else{
					deviceObj?.addProperty("remarks","login as admin user to perform this operation" )
				}
			}
		}catch(Exception e){
			e.printStackTrace()
		}
		render deviceObj
	}
	
	def deleteDeviceObject(Device deviceInstance){
		try {
			List devicesTobeDeleted = []
			def deviceDetailsList = DeviceDetails.findAllByDevice(deviceInstance)
			if(deviceDetailsList?.size() > 0){
				DeviceDetails.executeUpdate("delete DeviceDetails d where d.device = :instance1",[instance1:deviceInstance])
			}
			deviceInstance?.childDevices?.each { childDevice -> devicesTobeDeleted << childDevice?.id }
			DeviceStream.executeUpdate(DEVICESTREAM_QUERY,[instance1:deviceInstance])
			DeviceRadioStream.executeUpdate("delete DeviceRadioStream d where d.device = :instance1",[instance1:deviceInstance])
			devicegroupService.updateExecDeviceReference(deviceInstance)

			if(deviceInstance.isChild == 1){
				try {
					def devices = Device.findAll()
					devices?.each{ device ->
						def devInstance = device.childDevices.find { it.id == deviceInstance }
						if(devInstance){
							Device.withTransaction {
								Device parentDevice = Device.findById(device?.id)
								parentDevice.removeFromChildDevices(deviceInstance)
							}
						}
					}
				} catch (Exception e) {
					e.printStackTrace()
				}

			}
			try {
				if(!deviceInstance.delete(flush: true)){
					Device.withTransaction {
						Device dev = Device.findById(deviceInstance?.id)
						if(dev){
							if(!dev?.delete(flush: true)){

							}
						}
					}
				}
			} catch (Exception e) {
				Device.withTransaction {
					Device dev = Device.findById(deviceInstance?.id)
					if(dev){
						if(!dev?.delete(flush: true)){


						}
					}
				}
			}
			devicesTobeDeleted.each { childDeviceId ->
				Device childDevice = Device.findById(childDeviceId)
				devicegroupService.updateExecDeviceReference(childDevice)

				try {
					def status
					Device.withTransaction {
						status = childDevice.delete(flush: true)
					}
					if(!status){
						Device.withTransaction {
							Device dev = Device.findById(childDevice?.id)
							if(dev){
								dev?.delete(flush: true)
							}
						}
					}
				} catch (Exception e) {
					Device.withTransaction {
						Device dev = Device.findById(childDevice?.id)
						if(dev){
							dev?.delete(flush: true)
						}
					}
				}
			}

		}
		catch (DataIntegrityViolationException e) {
			return false
		}
		return true
	}
	
	private List getDevicesList(def groups, def params){
		return Device.createCriteria().list(max:params?.max, offset:params?.offset){
			or{
				isNull("groups")
				if(groups != null){
					eq("groups",groups)
				}
			}

			and{
				eq("category", Utility.getCategory(params?.category))
			}
			order 'stbName', 'asc'
		}
	}
	
	private List getDevicesCount(def groups, def params){
		return Device.createCriteria().count(max:params?.max, offset:params?.offset){
			or{
				isNull("groups")
				if(groups != null){
					eq("groups",groups)
				}
			}
			and{
				eq("category", Utility.getCategory(params?.category))
			}
		}
	}
	
	private List getDeviceGroupList(def groups, def params){
		return DeviceGroup.createCriteria().list(max:params?.max, offset:params?.offset){
			or{
				isNull("groups")
				if(groups != null){
					eq("groups",groups)
				}
			}

			and{
				eq("category", Utility.getCategory(params?.category))
			}
			order 'name', 'asc'
		}
	}
	
	private List getDeviceGroupCount(def groups, def params){
		return DeviceGroup.createCriteria().count(max:params?.max, offset:params?.offset){
			or{
				isNull("groups")
				if(groups != null){
					eq("groups",groups)
				}
			}
			and{
				eq("category", Utility.getCategory(params?.category))
			}
		}
	}
	
	/**
	 * REST API for add new device
	 */
	def createNewDevice(){
		JsonObject deviceObj = new JsonObject()
		try {
			String deviceStreams , deviceOcapId
			def node
			if(params?.deviceXml){
				def uploadedFile = request.getFile('deviceXml')
				if(uploadedFile){
					if( uploadedFile?.originalFilename?.endsWith(".xml")) {

						InputStreamReader reader = new InputStreamReader(uploadedFile?.getInputStream())
						def fileContent = reader?.readLines()
						//int indx = 0
						int indx = fileContent?.findIndexOf { it.startsWith("<?xml")}
						String s = ""
						String xml
						if(fileContent && fileContent.size() > 0){
							try{
								if(fileContent.get(indx))	{
									while(indx < fileContent.size()){
										s = s + fileContent.get(indx)+"\n"
										indx++
									}
								}
								xml = s
								XmlParser parser = new XmlParser();
								node = parser.parseText(xml)
								if(node){
									List<String> streams= new ArrayList<String>()
									List<String> ocapId= new ArrayList<String>()
									def deviceName =  node?.device?.stb_name?.text()?.trim()
									def  deviceIp =node?.device?.stb_ip?.text()?.trim()
									String boxType = node?.device?.box_type?.text()?.trim()
									def recorderId = node?.device?.recorder_id?.text()?.trim()
									def socVendor = node?.device?.soc_vendor?.text()?.trim()
									def boxManufacture = node?.device.box_manufacture?.text()?.trim()
									def gateway = node?.device?.gateway_name?.text()?.trim()
									def category = node?.device?.category?.text()?.trim()
									def isThunderEnabled = 0
									if(node?.device?.isThunderEnabled?.text()?.trim() == "1"){
										isThunderEnabled = node?.device?.isThunderEnabled?.text()?.trim()
									}
									isThunderEnabled = isThunderEnabled.toInteger()
									if(node?.device?.streams){
										node?.device?.streams?.stream?.each{
											streams.add(it?.@id)
											ocapId.add(it?.text()?.trim())
										}
									}
									def boxTypeObj = BoxType.findByNameAndCategory(boxType,Utility.getCategory(category))
									def boxManufactureObj = BoxManufacturer.findByNameAndCategory(boxManufacture,Utility.getCategory(category))
									def socVendorObj = SoCVendor.findByNameAndCategory(socVendor,Utility.getCategory(category))
									if(!boxType){
										deviceObj.addProperty("STATUS","FAILURE")
										deviceObj.addProperty("Remarks","Boxtype shouldnot be empty ")
									}else if(!boxTypeObj){
										deviceObj.addProperty("STATUS","FAILURE")
										deviceObj.addProperty("Remarks","No valid boxtype available with name "+boxType)
									}else if(Device.findByStbName(deviceName)){
										deviceObj.addProperty("STATUS","FAILURE")
										deviceObj.addProperty("Remarks","Device name is already exists " +deviceName)
									}else if(!deviceName){
										deviceObj.addProperty("STATUS","FAILURE")
										deviceObj.addProperty("Remarks","Device name shouldnot be empty")
									}else if(!deviceIp){
										deviceObj.addProperty("STATUS","FAILURE")
										deviceObj.addProperty("Remarks","Device IP name shouldnot be empty")
									}else if(deviceIp && Device.findByStbIp(deviceIp)){
										deviceObj.addProperty("STATUS","FAILURE")
										deviceObj.addProperty("Remarks","Device IP is already exists"+deviceIp)
									}else if(!socVendor){
										deviceObj.addProperty("STATUS","FAILURE")
										deviceObj.addProperty("Remarks","SOC Vendor  shouldnot be empty")
									}else if(socVendor && !SoCVendor.findByName(socVendor)){
										deviceObj.addProperty("STATUS","FAILURE")
										deviceObj.addProperty("Remarks","No valid soc vendor available with name "+socVendor)
									}else if(!boxManufacture){
										deviceObj.addProperty("STATUS","FAILURE")
										deviceObj.addProperty("Remarks","Box Manufacture shouldnot be empty")
									}else if(boxManufacture && !BoxManufacturer.findByName(boxManufacture)){
										deviceObj.addProperty("STATUS","FAILURE")
										deviceObj.addProperty("Remarks","No valid box manufacture available with name "+boxManufacture)
									}else if(!category){ 
										deviceObj.addProperty("STATUS","FAILURE")
										deviceObj.addProperty("Remarks","Category shouldnot be empty")
									} else if( category && !Utility.getCategory(category)){
										deviceObj.addProperty("STATUS","FAILURE")
										deviceObj.addProperty("Remarks","No valid category available with name "+category)

									}else{
										BoxType boxTypeInastnce = BoxType.findByNameAndCategory(boxType,Utility.getCategory(category))
										boolean valid = true
										if((boxTypeInastnce?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_GATEWAY)
										|| boxTypeInastnce?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_STANDALONE_CLIENT)) && category?.toString()?.equals(RDKV )){
											if(recorderId?.trim()?.length() ==  0){
												valid = false
												deviceObj.addProperty("STATUS","FAILURE")
												deviceObj.addProperty("Remarks","Recorder  id should not blank ")
											}else if(streams){
												if(validateOcapIds(streams,ocapId)){
													if(checkDuplicateOcapId(ocapId)){
														valid = false
														deviceObj.addProperty("STATUS","FAILURE")
														deviceObj.addProperty("Remarks","Duplicate Ocap id ")
													}
												}else{
													valid = false
													deviceObj.addProperty("STATUS","FAILURE")
													deviceObj.addProperty("Remarks","Stream information is not correct")
												}
											}
										}else{
											if(gateway){
												if(!Device.findByStbName(gateway) && category.equals(RDKV)){
													valid = false
													deviceObj.addProperty("STATUS","FAILURE")
													deviceObj.addProperty("Remarks","No valid gateway device available with name" +gateway)
												}
											}
											
											if(category?.toString()?.equals(RDKB )){
												def serialNo = node?.device?.mac_addr?.text()?.trim()
												if(!serialNo){
													serialNo = node?.device?.serial_no?.text()?.trim()
													if(!serialNo){
													valid = false
													deviceObj.addProperty("STATUS","FAILURE")
													deviceObj.addProperty("Remarks","Serial No should not be empty")
													}
												}
											}
										}
										if(valid){
											try{
												int status = 0
												def serialNo
												Device deviceInstance = new Device()
												deviceInstance.stbName = deviceName
												deviceInstance.stbIp = deviceIp
												deviceInstance.soCVendor = socVendorObj
												deviceInstance.boxType=boxTypeObj
												deviceInstance.boxManufacturer =boxManufactureObj
												deviceInstance.category= Utility.getCategory(category) 
												deviceInstance.isThunderEnabled = isThunderEnabled
												//deviceInstance.groups=utilityService.getGroup()
												if(boxTypeInastnce?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_CLIENT)){
													if(category?.equals(RDKV )){
														status = 1
														deviceInstance.gatewayIp =gateway
													}else if(category?.equals(RDKB)){
														serialNo = node?.device?.mac_addr?.text()?.trim()
														if(!serialNo){
															serialNo = node?.device?.serial_no?.text()?.trim()
														}
															status = 1
															deviceInstance?.serialNo =  serialNo?.toString()
													}
												}else if(boxTypeInastnce?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_GATEWAY)
												|| boxTypeInastnce?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_STANDALONE_CLIENT) ){
													if(category?.equals(RDKV )){
														status = 2
														deviceInstance.recorderId = recorderId
														deviceInstance.macId =null // HERE :  doubt --------->> null  / ""
													}else if(category?.equals(RDKB)){
														serialNo = node?.device?.mac_addr?.text()?.trim()
														if(!serialNo){
															serialNo = node?.device?.serial_no?.text()?.trim()
														}
															status = 1
															deviceInstance?.serialNo =  serialNo?.toString()
													}
												}
												if(status > 0 && deviceInstance.save(flush:true)){
													if(status == 2 && category?.toString()?.equals(RDKV)){
														devicegroupService.saveToDeviceGroup(deviceInstance)
														saveDeviceStream(streams, ocapId, deviceInstance)
													}
													deviceObj.addProperty("STATUS","Success")
													deviceObj.addProperty("Remarks","Device saved successfully ")
												}else{
													deviceObj.addProperty("STATUS","FAILURE")
													deviceObj.addProperty("Remarks","Device not saved ")
												}

											}catch (Exception e){
												println "ERROR"+e.getMessage()
												deviceObj.addProperty("STATUS","FAILURE")
												deviceObj.addProperty("Remarks","Device not saved ")
											}
										}
									}
								}else{
									deviceObj.addProperty("STATUS","FAILURE")
									deviceObj.addProperty("Remarks","XML tags not in correct format ")
								}
							}catch(Exception e){
								println "ERROR "+e.getMessage()
								deviceObj.addProperty("STATUS","FAILURE")
								deviceObj.addProperty("Remarks","Device not saved "+e.getMessage())
							}
						}else{
							deviceObj.addProperty("STATUS","FAILURE")
							deviceObj.addProperty("Remarks","XML tags not in correct format")
						}
					}else {
						deviceObj.addProperty("STATUS","FAILURE")
						deviceObj.addProperty("Remarks","please check the file name ")
					}
				}else{
					deviceObj.addProperty("STATUS","FAILURE")
					deviceObj.addProperty("Remarks","File does not exists  ")
				}
			}else{
				deviceObj.addProperty("STATUS","FAILURE")
				deviceObj.addProperty("Remarks","File does not exists  ")
			}
		} catch (Exception e) {
			println "ERROR "+e.getMessage()
			deviceObj.addProperty("STATUS","FAILURE")
			deviceObj.addProperty("Remarks","Device not saved "+e.getMessage())
		}
		render deviceObj
	}
	/**
	 * Function is used to download the RDKV device details as the .xml file 
	 * @return
	 */
	def downloadRDKVDeviceXml(){			
		def deviceInstance = Device?.findById(params?.id)
		if(deviceInstance){
			def streamsDetails = [:]
			def deviceRadioStreamList = DeviceRadioStream.findAllByDevice(deviceInstance)
			def deviceStreamList = DeviceStream?.findAllByDevice(deviceInstance)		
			//For streaming details 
			deviceStreamList?.each{ 
				streamsDetails.put(it.stream?.toString(),it.ocapId?.toString())
			}
			//For radio streaming details  
			deviceRadioStreamList.each {
				streamsDetails?.put(it.stream?.toString(),it.ocapId?.toString())
			}		
			def writer = new StringWriter()
			def xml = new MarkupBuilder(writer)
			String deviceData
			try{
				deviceData= getRDKVDeviceDetails(deviceInstance)
			} catch(Exception e){
				println  "ERROR "+e.getMessage()
				e.printStackTrace()
			}
			if(deviceData){
				params.format = "text"
				params.extension = "xml"
				response.setHeader("Content-Type", "application/octet-stream;")
				response.setHeader("Content-Disposition", "attachment; filename=\""+ deviceInstance?.toString()+".xml\"")
				//response.setHeader("Content-Length", ""+deviceData.length())
				response.outputStream << deviceData.getBytes()
			}else{
				flash.message = "Download failed due to device information not available."
				redirect(action: "list")
			}
		}else{
			flash.message ="Device does not exist"
			redirect(action:"list")
		}
	}	
	
	/**
	 * Function is used to download the RDKB device details as the .xml file
	 * @return
	 */
	
	def downloadRDKBDeviceXml(){
		def deviceInstance = Device?.findById(params?.id)
		if(deviceInstance){
			
			def writer = new StringWriter()
			def xml = new MarkupBuilder(writer)
			String deviceData
			try{
				deviceData= getRDKBDeviceDetails(deviceInstance)
			} catch(Exception e){
				println  "ERROR "+e.getMessage()
				e.printStackTrace()
			}
			/* Downloading the XML File*/
			if(deviceData){
				params.format = "text"
				params.extension = "xml"
				response.setHeader("Content-Type", "application/octet-stream;")
				response.setHeader("Content-Disposition", "attachment; filename=\""+ deviceInstance?.toString()+".xml\"")
				//response.setHeader("Content-Length", ""+deviceData.length())
				response.outputStream << deviceData.getBytes()
			}else{
				flash.message = "Download failed due to device information not available."
				redirect(action: "list")
			}
		}else{
			flash.message ="Device does not exist"
			redirect(action:"list")
		}
	}
	
	/**
	 * Function is used to upload xml file, extract the content and create new RDKV device
	 * @return
	 */
	def uploadRDKVDevice(){
		String xmlContent=""
		def data = null
		def node
		def uploadedFile = request.getFile('file')
		if( uploadedFile?.originalFilename?.endsWith(".xml")) {
			String fileName = uploadedFile?.originalFilename?.replace(".xml","")
			if(Device.findByStbName(fileName.trim())){
				flash.message="Device with name "+ fileName +" already exists"
			}else{
				InputStreamReader reader = new InputStreamReader(uploadedFile?.getInputStream())
				def fileContent = reader?.readLines()
				if(fileContent){
					fileContent?.each{ xmlData->
						xmlContent += xmlData +"\n"
					}
					if(fileContent && fileContent.size() > 0){
						try{
							XmlParser parser = new XmlParser();
							node = parser.parseText(xmlContent)
							if(node){
							List<String> streams= new ArrayList<String>()
							List<String> ocapId= new ArrayList<String>()
							def deviceName =  node?.device?.stb_name?.text()?.trim()
							def  deviceIp =node?.device?.stb_ip?.text()?.trim()
							String boxType = node?.device?.box_type?.text()?.trim()
							def recorderId = node?.device?.recorder_id?.text()?.trim()
							def socVendor = node?.device?.soc_vendor?.text()?.trim()
							def boxManufacture = node?.device.box_manufacture?.text()?.trim()
							def gateway = node?.device?.gateway_name?.text()?.trim()
							def category = node?.device?.category?.text()?.trim()
							def isThunderEnabled = 0
							if(node?.device?.isThunderEnabled?.text()?.trim() == "1"){
								isThunderEnabled = node?.device?.isThunderEnabled?.text()?.trim()
							}
							isThunderEnabled = isThunderEnabled.toInteger()
							def boxTypeObj = BoxType.findByNameAndCategory(boxType,Utility.getCategory(category))
							def boxManufactureObj = BoxManufacturer.findByNameAndCategory(boxManufacture,Utility.getCategory(category))
							def socVendorObj = SoCVendor.findByNameAndCategory(socVendor,Utility.getCategory(category))
							node?.device?.streams?.stream?.each{
								streams.add(it?.@id)
								ocapId.add(it?.text()?.trim())
							}
							if(!boxType){
								flash.message ="BoxType should not be empty "
							}else if(!boxTypeObj){
								flash.message= " No valid boxtype available with name"
							}else if(Device.findByStbName(deviceName)){
								flash.message= " Device name is already exists "
							}else if(!deviceName){
								flash.message= "Device should not be empty "
							}else if(!deviceIp){
								flash.message="Device IP should not be empty"
							}else if(deviceIp && Device.findByStbIp(deviceIp)){
								flash.message="Device IP already exist"
							}else if(!socVendor){
								flash.message="SOC Vendour should not be empty "
							}else if(socVendor && !SoCVendor.findByName(socVendor)){
								flash.message= " No valid soc vendour available with name"
							}else if(!boxManufacture){
								flash.message= "Box manufacture should not be empty "
							}else if(boxManufacture && !BoxManufacturer.findByName(boxManufacture)){
								flash.message=" No valid box manufacture available with name"
							}else if(category && !Utility.getCategory(category)){
								flash.message=" No valid  category name available with name"
							}
							else{
								BoxType boxTypeInastnce = BoxType.findByNameAndCategory(boxType,Utility.getCategory(category))

								boolean valid = true
								if(boxTypeInastnce?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_GATEWAY)
								|| boxTypeInastnce?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_STANDALONE_CLIENT) && category.equals(RDKV)){
									if(recorderId?.trim()?.length() ==  0){
										valid = false
										flash.message ="Recorder id should not blank "
									}else if(streams){
										if(validateOcapIds(streams,ocapId)){
											if(checkDuplicateOcapId(ocapId)){
												valid = false
												flash.message=" Duplicate Ocap id"
											}
										}else{
											valid = false
											flash.message= " Stream information is not is not correct "
										}
									}
								}else{
									if(gateway && category.equals(RDKV)){
										if(!Device.findByStbName(gateway)){
											valid = false
											flash.message=" No valid device available with name "
										}
									}
								}
								if(valid){
									try{
										int status = 0
										Device deviceInstance = new Device()
										deviceInstance.stbName = deviceName
										deviceInstance.stbIp = deviceIp
										deviceInstance.soCVendor = socVendorObj
										deviceInstance.boxType=boxTypeObj
										deviceInstance.boxManufacturer =boxManufactureObj
										deviceInstance.category= Utility.getCategory(category)
										deviceInstance.isThunderEnabled = isThunderEnabled
										//deviceInstance.groups=utilityService.getGroup()
										if(boxTypeInastnce?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_CLIENT) && category?.equals(RDKV )){
											status = 1
											deviceInstance.gatewayIp =gateway

										}else if(boxTypeInastnce?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_GATEWAY)
										|| boxTypeInastnce?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_STANDALONE_CLIENT) && category?.equals(RDKV)){
											status = 2
											deviceInstance.recorderId = recorderId
											deviceInstance.macId = null
										}
										if(status > 0 && deviceInstance.save(flush:true)){
											if(status == 2){
												devicegroupService.saveToDeviceGroup(deviceInstance)
												if(deviceInstance.category == Category.RDKV){
													saveDeviceStream(streams, ocapId, deviceInstance)
												}
											}
											flash.message=" Device saved successfully"
										}else{
											flash.message=" Device not saved"
										}

									}catch (Exception e){
										println "ERROR"+e.getMessage()
										e.printStackTrace()
									}
								}
							}
							}else{
							flash.message =" XML tags not in correct format "
							}
						}catch(Exception e){
							flash.message =" Device not saved "
						}
					}else{
						flash.message ="File content is empty"
					}
				}
			}
		}else{
			flash.message="Error, The file extension is not in .xml format"
		}

		redirect(action:"list")
		return
	}
	
	/**
	 * Function is used to upload xml file, extract the content and create new RDKB device
	 * @return
	 */
	
	def uploadRDKBDevice(){
		String xmlContent=""
		def data = null
		def node
		def uploadedFile = request.getFile('file')
		if( uploadedFile?.originalFilename?.endsWith(".xml")) {
			String fileName = uploadedFile?.originalFilename?.replace(".xml","")
			if(Device.findByStbName(fileName.trim())){
				flash.message="Device with name "+ fileName +" already exists"
			}else{
				
				/*Reading the XML file */
				InputStreamReader reader = new InputStreamReader(uploadedFile?.getInputStream())
				def fileContent = reader?.readLines()
				if(fileContent){
					fileContent?.each{ xmlData->
						xmlContent += xmlData +"\n"
					}
					/* Saving the details given in the file*/
					if(fileContent && fileContent.size() > 0){
						try{
							XmlParser parser = new XmlParser();
							node = parser.parseText(xmlContent)
							if(node){
							def deviceName =  node?.device?.gateway_name?.text()?.trim()
							def  deviceIp =node?.device?.gateway_ip?.text()?.trim()
							String boxType = node?.device?.box_type?.text()?.trim()
							def socVendor = node?.device?.soc_vendor?.text()?.trim()
							def boxManufacture = node?.device.box_manufacture?.text()?.trim()
							def serialno = node?.device?.mac_addr?.text()?.trim()
							if(!serialno){
								serialno = node?.device?.serial_no?.text()?.trim()
							}
							def category = node?.device?.category?.text()?.trim()
							def boxTypeObj = BoxType.findByNameAndCategory(boxType,Utility.getCategory(category))
							def boxManufactureObj = BoxManufacturer.findByNameAndCategory(boxManufacture,Utility.getCategory(category))
							def socVendorObj = SoCVendor.findByNameAndCategory(socVendor,Utility.getCategory(category))
							//Checking if all the necessary inputs are given in the file
							if(!boxType){
								flash.message ="BoxType should not be empty "
							}else if(!boxTypeObj){
								flash.message= " No valid boxtype available with name"
							}else if(Device.findByStbName(deviceName)){
								flash.message= " Device name is already exists "
							}else if(!deviceName){
								flash.message= "Device should not be empty "
							}else if(!deviceIp){
								flash.message="Device IP should not be empty"
							}else if(deviceIp && Device.findByStbIp(deviceIp)){
								flash.message="Device IP already exist"
							}else if(!socVendor){
								flash.message="SOC Vendour should not be empty "
							}else if(socVendor && !SoCVendor.findByName(socVendor)){
								flash.message= " No valid soc vendour available with name"
							}else if(!boxManufacture){
								flash.message= "Box manufacture should not be empty "
							}else if(boxManufacture && !BoxManufacturer.findByName(boxManufacture)){
								flash.message=" No valid box manufacture available with name"
							}else if(category && !Utility.getCategory(category)){
								flash.message=" No valid  category name available with name"
							}
							else if(!serialno){
								flash.message=" Serial number should not be empty"
							}
							else{
								
								
									try{
										/* Creating a new Device with the given details */
										Device deviceInstance = new Device()
										deviceInstance.stbName = deviceName
										deviceInstance.stbIp = deviceIp
										deviceInstance.soCVendor = socVendorObj
										deviceInstance.boxType=boxTypeObj
										deviceInstance.boxManufacturer =boxManufactureObj
										deviceInstance.category= Utility.getCategory(category)
										deviceInstance.serialNo= serialno
										//deviceInstance.groups=utilityService.getGroup()
										
										if(deviceInstance.save(flush:true)){
											
											devicegroupService.saveToDeviceGroup(deviceInstance)
											
											flash.message=" Device saved successfully"
										}else{
											flash.message=" Device not saved"
										}

									}catch (Exception e){
									flash.message =" XML tags not in correct format "
										println "ERROR"+e.getMessage()
										e.printStackTrace()
									}
								
							}
							}else{
							flash.message =" XML tags not in correct format "
							}
						}catch(Exception e){
							flash.message =" Device not saved "
						}
					}else{
						flash.message ="File content is empty"
					}
				}
			}
		}else{
			flash.message="Error, The file extension is not in .xml format"
		}

		redirect(action:"list")
		return
	}
	
	/**
	 * Function  used to upload RDKB device configuration for python/tcl script execution . 
	 * @return
	 */
	
	def uploadConfiguration(){
		def message = 'Upload failed'
		
		def realPath = request.getSession().getServletContext().getRealPath(FILE_SEPARATOR)

		def configType = params.configType?.trim()

		def filePath
		boolean tclConfig = false

		if(configType == TCL_DEVICE_CONFIG){
			tclConfig = true
			filePath =  realPath+FILESTORE+FILE_SEPARATOR+FileStorePath.RDKTCL.value()+FILE_SEPARATOR
		}else{
			filePath =  realPath+FILESTORE+FILE_SEPARATOR+TDKB_DEVICE_CONFIG+FILE_SEPARATOR
		}

		def gatewayName = params.gatewayName?.trim()
		def deviceIp = params.ip?.trim()
		if(gatewayName && filePath){
			
			if(tclConfig){
				filePath = filePath + 'Config_'+gatewayName+TXT_EXTN
			}else{
				filePath = filePath + gatewayName+CONFIG_EXTN
			}
			
			try{
				def f =  request.getFile('configFile')
				if(!f.empty){
					def content = readFromStream(f, realPath,tclConfig)
					if(tclConfig){
						content = content + "\ndeviceIp  "+deviceIp
					}
					Utility.writeContentToFile(content, filePath)
					message = 'File uploaded successfully'
				}
			}
			catch(Exception e){
				println e.getMessage()
			}
		}
		else{
			message = 'Gateway name missing'
		}
		render message
	}
	/**
	 * Function for reading the config file and in case of TCL execution selecting  TclSocketExecutor/  WebPAClient as per the user requirement. 
	 * - If the execution is done directly at the box from Test Manager, TclSocketExecutor is used 
	 * - If the user needs WebPA, WebPAClient can be added
	 * @param request
	 * @param path
	 * @return
	 */
	
	def readFromStream(def request, def path,boolean appendClasspath){
		BufferedReader reader = new BufferedReader(new InputStreamReader(request.getInputStream()))
		StringBuilder builder = new StringBuilder()
		String t = null
		while((t = reader.readLine()) != null){
			builder.append(t).append('\n')
		}
		reader.close()
		if(appendClasspath){
			def jarPath = path + JAR_PATH
			def classPath = path + CLASS_PATH
			builder.append('class  ').append(SOCKET_CLIENT).append('\n')
			def separator = getSeparator()
			builder.append('classPath ').append(jarPath).append(separator).append(classPath).append('\n')
		}
		builder.toString()
	}
	/**
	 * Function for returning separator according to the OS
	 * @return
	 */
	def getSeparator(){
		def os = System.getProperty(OS_NAME)
		if(os.contains(OS_WINDOWS)){
			return ';'
		}
		return ':'
	}
	/**
	 * Function for return stb  IP  using serial no
	 * @param serialNo
	 * @return
	 */
	
	public static String getDeviceIp(String serialNo){
    	String stbIp = ""
		Device.withTransaction {
			Device device = Device.findBySerialNo(serialNo)
			if(device){
				stbIp = device?.stbIp;
			}
		}
		return stbIp;
	}
	
	/**
	 * REST API
	 * Function  used to upload RDKB device configuration for tcl script execution .
	 * @return
	 */	
		def uploadTclConfig(){
		JsonObject deviceObj = new JsonObject()
		def realPath = request.getSession().getServletContext().getRealPath(FILE_SEPARATOR)
		def filePath =  realPath+FILESTORE+FILE_SEPARATOR+FileStorePath.RDKTCL.value()+FILE_SEPARATOR
		def deviceName = params.deviceName?.trim()
		if(deviceName){
			Device dev = Device?.findByStbName(deviceName)
			if(dev){
				filePath = filePath + 'Config_'+deviceName+".txt"
				try{
					def tclFile =  request?.getFile('tclConfigFile')
					if(tclFile){
						if(!tclFile?.empty){
							def content = readFromStream(tclFile, realPath,true)
							content = content + "\ndeviceIp  "+dev?.stbIp
							Utility.writeContentToFile(content, filePath)
							deviceObj.addProperty(STATUS_C,SUCCESS)
							deviceObj.addProperty(REMARKS_C,"File uploaded successfully ")
						}else{
							deviceObj.addProperty(STATUS_C,FAILURE)
							deviceObj.addProperty(REMARKS_C,"File content is empty ")
						}
					}else{
						deviceObj.addProperty(STATUS_C,FAILURE)
						deviceObj.addProperty(REMARKS_C,"tclConfigFile missing ")
					}
				}
				catch(Exception e){
					deviceObj.addProperty(STATUS_C,FAILURE)
					deviceObj.addProperty(REMARKS_C,"TCL Config file upload failed ")
					println e.getMessage()
				}
			}else{
				deviceObj.addProperty(STATUS_C,FAILURE)
				deviceObj.addProperty(REMARKS_C,"No device found with name "+deviceName)
			}
		}
		else{
			deviceObj.addProperty(STATUS_C,FAILURE)
			deviceObj.addProperty(REMARKS_C,'deviceName missing')
		}
		render deviceObj
	}
		
	/**
	 * REST API to fetch the box type  using device name or device ip
	 */
	def getDeviceBoxType(String deviceName , String deviceIp){
		Map status = [:]
		BoxType bType = null

		if(deviceName){
			status.put("devicename", deviceName)
		}

		if(deviceIp){
			status.put("deviceip", deviceIp)
		}

		try {
			Device dev = null
			if(deviceName){
				dev = Device?.findByStbName(deviceName)
			}else if (deviceIp){
				dev = Device?.findByStbIp(deviceIp)
			}
			if(dev){
				bType = dev?.getBoxType()
				status.put("status", "SUCCESS")
				status.put("boxtype", bType?.getName())
			}else{
				status.put("status", "FAILURE")
				status.put("remarks", "No valid device found with provided data")
			}


		} catch (Exception e) {
			status.put("status", "FAILURE")
			e.printStackTrace()
		}
		render status as JSON
	}
	
	/**
	 * REST API to fetch the device details using device name or device ip
	 */
	def getDeviceDetails(String deviceName , String deviceIp){
		Map status = [:]
		BoxType bType = null

		try {
			Device dev = null
			if(deviceName){
				dev = Device?.findByStbName(deviceName)
			}else if (deviceIp){
				dev = Device?.findByStbIp(deviceIp)
			}
			
			if(dev){
				status.put("status", "SUCCESS")
				status.put("devicename", dev?.stbName)
				status.put("deviceip", dev?.stbIp)
				status.put("category", dev?.category?.toString())
				bType = dev?.getBoxType()
				status.put("boxtype", bType?.getName())
				def mac = dev?.getSerialNo()
				if(mac){
				status.put("mac", mac)
				}
			}else{
				status.put("status", "FAILURE")
				status.put("remarks", "No valid device found with provided data")
			}


		} catch (Exception e) {
			status.put("status", "FAILURE")
			e.printStackTrace()
		}
		render status as JSON
	}
	
	/**
	 * REST API
	 * Function  used to upload RDKB device configuration for TDKB E2E python script execution .
	 * @return
	 */
		def uploadE2EConfig(){
		JsonObject deviceObj = new JsonObject()
		def realPath = request.getSession().getServletContext().getRealPath(FILE_SEPARATOR)
		def filePath = realPath+FILESTORE+FILE_SEPARATOR+TDKB_DEVICE_CONFIG+FILE_SEPARATOR
		def deviceName = params.deviceName?.trim()
		if(deviceName){
			Device dev = Device?.findByStbName(deviceName)
			if(dev){
				filePath = filePath + deviceName+CONFIG_EXTN
				try{
					def configFile =  request?.getFile('configFile')
					if(configFile){
						if(!configFile?.empty){
							def content = readFromStream(configFile, realPath,false)
							Utility.writeContentToFile(content, filePath)
							deviceObj.addProperty(STATUS_C,SUCCESS)
							deviceObj.addProperty(REMARKS_C,"File uploaded successfully ")
						}else{
							deviceObj.addProperty(STATUS_C,FAILURE)
							deviceObj.addProperty(REMARKS_C,"File content is empty ")
						}
					}else{
						deviceObj.addProperty(STATUS_C,FAILURE)
						deviceObj.addProperty(REMARKS_C,"configFile missing ")
					}
				}
				catch(Exception e){
					deviceObj.addProperty(STATUS_C,FAILURE)
					deviceObj.addProperty(REMARKS_C,"Config file upload failed ")
					println e.getMessage()
				}
			}else{
				deviceObj.addProperty(STATUS_C,FAILURE)
				deviceObj.addProperty(REMARKS_C,"No device found with name "+deviceName)
			}
		}
		else{
			deviceObj.addProperty(STATUS_C,FAILURE)
			deviceObj.addProperty(REMARKS_C,'deviceName missing')
		}
		render deviceObj
	}
		
	/**
	 * Function to fetch the rdk-v device details in XML format
	 * @return
	 */
	def getRDKVDeviceDetails(def deviceInstance){
		String deviceData
		if(deviceInstance){
			def streamsDetails = [:]
			def deviceRadioStreamList = DeviceRadioStream.findAllByDevice(deviceInstance)
			def deviceStreamList = DeviceStream?.findAllByDevice(deviceInstance)
			//For streaming details
			deviceStreamList?.each{
				streamsDetails.put(it.stream?.toString(),it.ocapId?.toString())
			}
			//For radio streaming details
			deviceRadioStreamList.each {
				streamsDetails?.put(it.stream?.toString(),it.ocapId?.toString())
			}
			def writer = new StringWriter()
			def xml = new MarkupBuilder(writer)
			try{
				xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
				xml.xml(){
					xml.device(){
						mkp.yield "\r\n  "
						mkp.comment "Unique name for the STB"
						xml.stb_name(deviceInstance?.stbName)
						mkp.yield "\r\n  "
						mkp.comment "Unique IP for the STB "
						xml.stb_ip(deviceInstance?.stbIp)
						mkp.yield "\r\n  "
						if(deviceInstance?.serialNo){
							mkp.comment "Mac Addr for the STB "
							xml.mac_addr(deviceInstance?.serialNo)
							mkp.yield "\r\n "
						}else{
							mkp.comment "Mac Addr for the Device"
							xml.mac_addr("")
							mkp.yield "\r\n  "
						}
						if(deviceInstance?.isThunderEnabled){
							mkp.comment " Is Thunder enabled for STB"
							xml.isThunderEnabled(deviceInstance?.isThunderEnabled)
							mkp.yield "\r\n  "
						}else{
							mkp.comment "Is Thunder enabled for STB "
							xml.isThunderEnabled("")
							mkp.yield "\r\n  "
						}
						mkp.comment " BoxType for STB  "
						xml.box_type(deviceInstance?.boxType)
						mkp.yield "\r\n  "
						mkp.comment "BoxManufacture for the STB"
						xml.box_manufacture(deviceInstance?.boxManufacturer)
						mkp.yield "\r\n  "
						mkp.comment "SoC vendor for the STB"
						xml.soc_vendor(deviceInstance?.soCVendor)
						// Issue fix - category
						mkp.yield "\r\n  "
						mkp.comment "Category for the STB"
						xml.category(deviceInstance?.category)
						BoxType boxTypeInstance = BoxType.findByName(deviceInstance?.boxType?.toString())
						if(boxTypeInstance?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_GATEWAY)
						|| boxTypeInstance?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_STANDALONE_CLIENT)){
							mkp.yield "\r\n  "
							mkp.comment "RecorderId for Gateway device"
							xml.recorder_id(deviceInstance?.recorderId)
							mkp.yield "\r\n  "
							mkp.comment "Streaming details with Ocap id "
							xml.streams(){
								mkp.yield "\r\n "
								mkp.comment "<stream id='streamId'>OCAP_ID</stream>"
								streamsDetails.each { streamid,ocapid->
									xml.stream(id:streamid , ocapid?.toString())
								}
							}
							if(boxTypeInstance?.type?.toString()?.toLowerCase()?.equals(BOXTYPE_STANDALONE_CLIENT)){
								mkp.yield "\r\n  "
								mkp.comment "Gateway IP for Terminal-RNG box"
								xml.gateway_ip(deviceInstance?.gatewayIp)
							}
						}else{
							if(deviceInstance?.gatewayIp){
								mkp.yield "\r\n  "
								mkp.comment "Gateway IP for  IPClient STB"
								xml.gateway_ip(deviceInstance?.gatewayIp)
							}else{
								mkp.yield "\r\n  "
								mkp.comment "Gateway IP for IPClient STB"
								xml.gateway_ip("")
							}
						}
					}
				}
				deviceData= writer.toString()
			} catch(Exception e){
				println  "ERROR "+e.getMessage()
				e.printStackTrace()
			}
		}
		return deviceData
	}
	/**
	 * Function to fetch the rdk-b device details in XML format
	 * @return
	 */
	def getRDKBDeviceDetails(def deviceInstance){
		String deviceData
		if(deviceInstance){
			def writer = new StringWriter()
			def xml = new MarkupBuilder(writer)
			try{
				xml.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")
				xml.xml(){
					xml.device(){
						mkp.yield "\r\n  "
						mkp.comment "Unique name for the Device"
						xml.gateway_name(deviceInstance?.stbName)
						mkp.yield "\r\n  "
						mkp.comment "Unique IP for the Device "
						xml.gateway_ip(deviceInstance?.stbIp)
						mkp.yield "\r\n  "
						mkp.comment " BoxType for Device  "
						xml.box_type(deviceInstance?.boxType)
						mkp.yield "\r\n  "
						mkp.comment "BoxManufacture for the Device"
						xml.box_manufacture(deviceInstance?.boxManufacturer)
						mkp.yield "\r\n  "
						mkp.comment "SoC vendor for the Device"
						xml.soc_vendor(deviceInstance?.soCVendor)
						// Issue fix - category
						mkp.yield "\r\n  "
						mkp.comment "Category for the Device"
						xml.category(deviceInstance?.category)
						mkp.yield "\r\n  "
						mkp.comment "Mac Addr for the Device"
						if(deviceInstance?.serialNo){
							xml.mac_addr(deviceInstance?.serialNo)
						}else{
							xml.mac_addr("")
						}
					}
				}
				deviceData= writer.toString()
			} catch(Exception e){
				println  "ERROR "+e.getMessage()
				e.printStackTrace()
			}
		}
	}
	
	/**
	 * Function for download all device details as XML as zip
	 * @return
	 */
	def downloadAllDevices(){
		String category = params?.category
		try {
			def deviceList = Device.findAllByCategory(category)
			if(deviceList?.size() > 0){
				ZipOutputStream zos = new ZipOutputStream(response.outputStream);
				params.format = EXPORT_ZIP_FORMAT
				params.extension = EXPORT_ZIP_EXTENSION
				response.contentType = grailsApplication.config.grails.mime.types[params.format]
				response.setHeader("Content-Type", "application/zip")
				response.setHeader("Content-disposition", "attachment; filename=DeviceXML_"+ category +".${params.extension}")
				deviceList?.each{ devObj ->
					def xmlData = ""
					if(category?.equals(Category.RDKB?.toString())){
						xmlData = getRDKBDeviceDetails(devObj)
					}else{
						xmlData = getRDKVDeviceDetails(devObj)
					}
					logZipService.writeZipEntry(xmlData , "${category}/${devObj?.stbName}.xml" , zos)
				}
				zos.closeEntry();
				zos.close();
			}else{
				flash.message = "Download failed due to device information not available."
				redirect(action:"list")
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
	}
	
}


