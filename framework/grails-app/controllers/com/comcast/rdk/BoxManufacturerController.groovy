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

import static com.comcast.rdk.Constants.KEY_ON
import org.springframework.dao.DataIntegrityViolationException
import grails.converters.JSON

class BoxManufacturerController {

	def utilityService
	
    static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

	def index() {
		redirect(action: "create",params:params)
	}

	def create(Integer max) {
		params.max = Math.min(max ?: 10, 100)
		def groupsInstance = utilityService.getGroup()
		//def boxManufacturerList = BoxManufacturer.findAllByGroupsOrGroupsIsNull(groupsInstance,params)
		//def boxManufacturerListCnt = BoxManufacturer.findAllByGroupsOrGroupsIsNull(groupsInstance)
		def boxManufacturerList = getBoxManufacturerList(groupsInstance,params)
		//[boxManufacturerInstance: new BoxManufacturer(params), boxManufacturerInstanceList: boxManufacturerList, boxManufacturerInstanceTotal: boxManufacturerList.size(), category:params?.category]
		[boxManufacturerInstance: new BoxManufacturer(params), boxManufacturerInstanceList: boxManufacturerList, boxManufacturerInstanceTotal: getBoxManufacturerCount(groupsInstance, params), category:params?.category]
	}

	def save() {
		def groupsInstance = utilityService.getGroup()
		//def boxManufacturerList = BoxManufacturer.findAllByGroupsOrGroupsIsNull(groupsInstance,params)
		//def boxManufacturerListCnt = BoxManufacturer.findAllByGroupsOrGroupsIsNull(groupsInstance)
		def boxManufacturerList = getBoxManufacturerList(groupsInstance,[name:'name',order:'asc'])
		def boxManufacturerInstance = new BoxManufacturer(params)
		boxManufacturerInstance.groups = groupsInstance
		
		if (!boxManufacturerInstance.save(flush: true)) {
			render(view: "create", model: [boxManufacturerInstance: boxManufacturerInstance, boxManufacturerInstanceList: boxManufacturerList, boxManufacturerInstanceTotal: getBoxManufacturerCount(groupsInstance, params), category:params?.category])
			return
		}

		flash.message = message(code: 'default.created.message', args: [message(code: 'boxManufacturer.label', default: 'BoxManufacturer'), boxManufacturerInstance.name])
		redirect(action: "create", params:[category:params?.category])
	}

	def deleteBoxManufacturer(){
		def countVariable = 0
			int deleteCount = 0
		def boxManufacturerInstance
		if(params?.listCount){ // to delete record(s) from list.gsp
			for (iterateVariable in params?.listCount){
				countVariable++
				if(params?.("chkbox"+countVariable) == KEY_ON){
					def idDb = params?.("id"+countVariable).toLong()
					boxManufacturerInstance = BoxManufacturer.get(idDb)
					if (boxManufacturerInstance) {
						try{
						  boxManufacturerInstance.delete(flush: true)
						  deleteCount++
						}
						catch (DataIntegrityViolationException e) {
				            flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'boxManufacturer.label', default: 'BoxManufacturer'),  boxManufacturerInstance.name])				           
				        }
					}
				}
			}
			}
		if(deleteCount  > 1)
		{
			flash.message = "BoxManufactures deleted"
		}
		else
		{
			flash.message = message(code: 'default.deleted.message', args: [message(code: 'boxManufacturer.label', default: 'BoxManufacturer'),  boxManufacturerInstance.name])
		}
		redirect(action: "create", params:[category : params?.category])
	}

	def getBoxManufacturer() {			
		List boxManufacturerInstanceList = []
		BoxManufacturer boxManufacturer = BoxManufacturer.findById(params.id)
		if(boxManufacturer){
			boxManufacturerInstanceList.add(boxManufacturer.name)
		}
		render boxManufacturerInstanceList as JSON
	}

    def update(Long id, Long version, Integer max) {
		def groupsInstance = utilityService.getGroup()
        def boxManufacturerInstance = BoxManufacturer.get(id)
		//def boxManufacturerList = BoxManufacturer.findAllByGroupsOrGroupsIsNull(groupsInstance,params)
		//def boxManufacturerListCnt = BoxManufacturer.findAllByGroupsOrGroupsIsNull(groupsInstance)
		params.max = Math.min(max ?: 10, 100)
		def boxManufacturerList = getBoxManufacturerList(groupsInstance,params)
        if (!boxManufacturerInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'boxManufacturer.label', default: 'BoxManufacturer'), boxManufacturerInstance?.name])
			render(view: "create", model: [boxManufacturerInstance: boxManufacturerInstance, boxManufacturerInstanceList: boxManufacturerList, boxManufacturerInstanceTotal: getBoxManufacturerCount(groupsInstance, params), category:params?.category])
            return
        }

		def boxManufacturerBasedOnName = BoxManufacturer?.findByName(params?.name)
		
		if(boxManufacturerBasedOnName && (boxManufacturerBasedOnName?.id !=  boxManufacturerInstance?.id)){
			flash.message = message(code: 'default.not.unique.message', args: [message(code: 'boxManufacturer.label', default: 'BoxManufacturer Name')])
			render(view: "create", model: [boxManufacturerInstance: boxManufacturerInstance, boxManufacturerInstanceList: boxManufacturerList, boxManufacturerInstanceTotal: getBoxManufacturerCount(groupsInstance, params), category:params?.category])
            return
		}
		
        if (version != null) {
            if (boxManufacturerInstance.version > version) {
                boxManufacturerInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
                          [message(code: 'boxManufacturer.label', default: 'BoxManufacturer')] as Object[],
                          "Another user has updated this BoxManufacturer while you were editing")
				render(view: "create", model: [boxManufacturerInstance: boxManufacturerInstance, boxManufacturerInstanceList: boxManufacturerList, boxManufacturerInstanceTotal: getBoxManufacturerCount(groupsInstance, params),category:params?.category])
                return
            }
        }

        boxManufacturerInstance.properties = params

        if (!boxManufacturerInstance.save(flush: true)) {
			render(view: "create", model: [boxManufacturerInstance: boxManufacturerInstance, boxManufacturerInstanceList: boxManufacturerList, boxManufacturerInstanceTotal: getBoxManufacturerCount(groupsInstance, params), category:params?.category])
            return
        }

        flash.message = message(code: 'default.updated.message', args: [message(code: 'boxManufacturer.label', default: 'BoxManufacturer'), boxManufacturerInstance.name])
        redirect(action: "create", params:[category:params?.category])
    }
	
	private List getBoxManufacturerList(def groups, def params){
		return  BoxManufacturer.createCriteria().list(max:params?.max, offset:params?.offset ){
			or{
				isNull("groups")
				if(groups != null){
					eq("groups",groups)
				}
			}

			and{
				eq("category", Utility.getCategory(params?.category))
				
			}
			order params.sort?params.sort:'name', params.order?params.order:'asc'
		}

	}
	
	private int getBoxManufacturerCount(def groups, def params){
		return  BoxManufacturer.createCriteria().count(){
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

}
