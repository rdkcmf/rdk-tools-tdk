/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2019 RDK Management
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

import org.springframework.dao.DataIntegrityViolationException
import static com.comcast.rdk.Constants.*
import grails.converters.JSON

/**
 *  A class that handles the device template creation for filling ocapId's
 * @author neerada.n
 *
 */
class DeviceTemplateController {

	static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

	/**
	 * The default method of the class
	 * @return
	 */
	def index() {
		redirect(action: "list", params: params)
	}

	/**
	 * Method which lists all the device templates
	 * @param max
	 * @return
	 */
	def list(Integer max) {
		params.max = Math.min(max ?: 10, 100)
		[deviceTemplateInstanceList: DeviceTemplate.list(params), deviceTemplateInstanceTotal: DeviceTemplate.count()]
	}

	/**
	 * Method to create a device template
	 * @return
	 */
	def create() {
		[deviceTemplateInstance: new DeviceTemplate(params),streamingDetailsInstanceList: StreamingDetails.list(),radioStreamingDetails : RadioStreamingDetails.findAll(), streamingDetailsInstanceTotal: StreamingDetails.count(), streamingDetailsInstanceTotal: RadioStreamingDetails.count()]
	}

	/**
	 * Method to save a device template
	 * @return
	 */
	def save() {
		def deviceTemplateInstance = new DeviceTemplate(params)
		if (!deviceTemplateInstance.save(flush: true)) {
			render(view: "create", model: [deviceTemplateInstance: deviceTemplateInstance])
			return
		}

		flash.message = message(code: 'default.created.message', args: [
			message(code: 'deviceTemplate.label', default: 'DeviceTemplate'),
			deviceTemplateInstance.id
		])
		redirect(action: "show", id: deviceTemplateInstance.id)
	}

	/**
	 * Method to display a device template 
	 * @param id
	 * @return
	 */
	def show(Long id) {
		def deviceTemplateInstance = DeviceTemplate.get(id)
		if (!deviceTemplateInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'deviceTemplate.label', default: 'DeviceTemplate'),
				id
			])
			redirect(action: "list")
			return
		}

		[deviceTemplateInstance: deviceTemplateInstance]
	}

	/**
	 * Method to edit a device template
	 * @param id
	 * @return
	 */
	def edit(Long id) {
		def deviceTemplateInstance = DeviceTemplate.get(id)
		if (!deviceTemplateInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'deviceTemplate.label', default: 'DeviceTemplate'),
				id
			])
			redirect(action: "list")
			return
		}
		List deviceTemplateList = []
		def i;
		for(i=1;i<=RadioStreamingDetails.count()+StreamingDetails.count();i++){
			deviceTemplateList.add(i)
		}
		def applicationUrl = getApplicationUrl()
		[applicationUrl: applicationUrl, deviceTemplateInstance: deviceTemplateInstance, streamingDetailsInstanceList: StreamingDetails.list(),radioStreamingDetails : RadioStreamingDetails.findAll(), streamingDetailsInstanceTotal: StreamingDetails.count(), radioStreamingDetailsInstanceTotal: RadioStreamingDetails.count(),deviceTemplateList:deviceTemplateList]
	}

	/**
	 * Method to update a device template
	 * @param id
	 * @param version
	 * @return
	 */
	def update(Long id, Long version) {
		def deviceTemplateInstance = DeviceTemplate.get(id)
		if (!deviceTemplateInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'deviceTemplate.label', default: 'DeviceTemplate'),
				id
			])
			redirect(action: "list")
			return
		}

		if (version != null) {
			if (deviceTemplateInstance.version > version) {
				deviceTemplateInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
						[
							message(code: 'deviceTemplate.label', default: 'DeviceTemplate')] as Object[],
						"Another user has updated this DeviceTemplate while you were editing")
				render(view: "edit", model: [deviceTemplateInstance: deviceTemplateInstance])
				return
			}
		}

		deviceTemplateInstance.properties = params

		if (!deviceTemplateInstance.save(flush: true)) {
			render(view: "edit", model: [deviceTemplateInstance: deviceTemplateInstance])
			return
		}

		flash.message = message(code: 'default.updated.message', args: [
			message(code: 'deviceTemplate.label', default: 'DeviceTemplate'),
			deviceTemplateInstance.id
		])
		redirect(action: "show", id: deviceTemplateInstance.id)
	}

	/**
	 * Method to delete a device template
	 * @param id
	 * @return
	 */
	def delete(Long id) {
		def deviceTemplateInstance = DeviceTemplate.get(id)
		if (!deviceTemplateInstance) {
			flash.message = message(code: 'default.not.found.message', args: [
				message(code: 'deviceTemplate.label', default: 'DeviceTemplate'),
				id
			])
			redirect(action: "list")
			return
		}

		try {
			deviceTemplateInstance.delete(flush: true)
			flash.message = message(code: 'default.deleted.message', args: [
				message(code: 'deviceTemplate.label', default: 'DeviceTemplate'),
				id
			])
			redirect(action: "list")
		}
		catch (DataIntegrityViolationException e) {
			flash.message = message(code: 'default.not.deleted.message', args: [
				message(code: 'deviceTemplate.label', default: 'DeviceTemplate'),
				id
			])
			redirect(action: "show", id: id)
		}
	}

	/**
	 * Method to fetch a device template ocapId's 
	 * @return
	 */
	def fetchDeviceTemplate(){
		def deviceTemplateInstance = DeviceTemplate.get(params.deviceTemplateInstanceId)
		render deviceTemplateInstance?.ocapId as JSON
		return
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
}
