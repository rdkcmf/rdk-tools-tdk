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

import org.springframework.dao.DataIntegrityViolationException
import static com.comcast.rdk.Constants.KEY_ON
import com.comcast.rdk.Utility

import java.util.List;

import org.springframework.dao.DataIntegrityViolationException
import grails.converters.JSON

class BoxTypeController {

	def utilityService
	
	static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

	def index() {
		redirect(action: "create", params:params)
	}

	def create(Integer max) {
		params.max = Math.min(max ?: 10, 100)
		def groupsInstance = utilityService.getGroup()
		def category = Utility.getCategory(params?.category)
		def boxTypeList =  getBoxList(groupsInstance, params)
		def boxTypeInstance =  new BoxType(params)
		boxTypeInstance.category = category
		[boxTypeInstance: boxTypeInstance, boxTypeInstanceList: boxTypeList, boxTypeInstanceTotal: getBoxListCount(groupsInstance, category), category : params?.category]
	}

	def save() {
		def groupsInstance = utilityService.getGroup()
		def boxTypeList = getBoxList(groupsInstance, [name:'name',order:'asc'])
		def boxTypeInstance = new BoxType(params)
		boxTypeInstance.groups = groupsInstance
		if (!boxTypeInstance.save(flush: true)) {
			render(view: "create", model: [boxTypeInstance: boxTypeInstance, boxTypeInstanceList: boxTypeList, boxTypeInstanceTotal: getBoxListCount(groupsInstance, Utility.getCategory(params?.category)), category:params?.category])
			return
		}

		flash.message = message(code: 'default.created.message', args: [message(code: 'boxType.label', default: 'BoxType'), boxTypeInstance.name])
		redirect(action: "create", params:[category:params?.category])
	}
	
	def deleteBoxType(){
		def countVariable = 0
			int deleteCount = 0
		def boxTypeInstance
		if(params?.listCount){ // to delete record(s) from list.gsp
			for (iterateVariable in params?.listCount){
				countVariable++
				if(params?.("chkbox"+countVariable) == KEY_ON){
					def idDb = params?.("id"+countVariable).toLong()
					boxTypeInstance = BoxType.get(idDb)
					if (boxTypeInstance) {
						try{
							 boxTypeInstance.delete(flush: true)
							deleteCount++
						  }
						  catch (DataIntegrityViolationException e) {
							  flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'boxType.label', default: 'BoxType'),  boxTypeInstance.name])
						  }						 
					}
					
				}
			}
			}
		if(deleteCount  > 1)
		{
			flash.message = "BoxTypes deleted"
		}
		else
		{
			flash.message = message(code: 'default.deleted.message', args: [message(code: 'boxType.label', default: 'BoxType'),  boxTypeInstance.name])
		}
		redirect(action: "create", params:[category:params?.category])
	}

	def getBoxType() {
		List boxTypeInstanceList = []
		BoxType boxType = BoxType.findById(params.id)
		if(boxType){
			boxTypeInstanceList.add(boxType.name)
			boxTypeInstanceList.add(boxType.type)
		}
		render boxTypeInstanceList as JSON
	}

	def update(Long id, Long version, Integer max) {
		def groupsInstance = utilityService.getGroup()
		def boxTypeInstance = BoxType.get(id)
		//def boxTypeList = BoxType.findAllByGroupsOrGroupsIsNull(groupsInstance,params)
		//def boxTypeListCnt = BoxType.findAllByGroupsOrGroupsIsNull(groupsInstance) 
		params.max = Math.min(max ?: 10, 100)
		def boxTypeList = getBoxList(groupsInstance, params)
		def category = Utility.getCategory(params?.category)
		def boxTypeListCnt = getBoxListCount(groupsInstance, category)
		if (!boxTypeInstance) {
			flash.message = message(code: 'default.not.found.message', args: [message(code: 'boxType.label', default: 'BoxType'), id])
			render(view: "create", model: [boxTypeInstance: boxTypeInstance, boxTypeInstanceList: boxTypeList, boxTypeInstanceTotal: boxTypeListCnt.size()])
			return
		}
		
		def boxTypeBasedOnName = com.comcast.rdk.BoxType?.findByNameAndCategory(params?.name,category)	
		
		if(boxTypeBasedOnName && (boxTypeBasedOnName?.id !=  boxTypeInstance?.id)){
			flash.message = message(code: 'default.not.unique.message', args: [message(code: 'boxType.label', default: 'BoxType Name')])
			//render(view: "create", model: [boxTypeInstance: boxTypeInstance, boxTypeInstanceList: boxTypeList, boxTypeInstanceTotal: boxTypeListCnt?.size(), category : params?.category])
			render(view: "create", model: [boxTypeInstance: boxTypeInstance, boxTypeInstanceList: boxTypeList, boxTypeInstanceTotal: boxTypeListCnt, category:params?.category])
			
			return
		}
		
		if (version != null) {
			if (boxTypeInstance.version > version) {
				boxTypeInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
						  [message(code: 'boxType.label', default: 'BoxType')] as Object[],
						  "Another user has updated this BoxType while you were editing")
				render(view: "create", model: [boxTypeInstance: boxTypeInstance, boxTypeInstanceList: boxTypeList, boxTypeInstanceTotal: boxTypeListCnt.size(), category : params?.category])
				return
			}
		}

		boxTypeInstance.properties = params

		if (!boxTypeInstance.save(flush: true)) {
			render(view: "create", model: [boxTypeInstance: boxTypeInstance, boxTypeInstanceList: boxTypeList, boxTypeInstanceTotal: boxTypeListCnt.size(), category : params?.category])
			return
		}

		flash.message = message(code: 'default.updated.message', args: [message(code: 'boxType.label', default: 'BoxType'), boxTypeInstance.name])
		redirect(action: "create", params:[category : params?.category])
	}
	
	private List getBoxList(def groups, def params){
		return  BoxType?.createCriteria().list(max:params?.max, offset:params?.offset ){
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
	
	private int getBoxListCount(def groups, def category){
		return  com.comcast.rdk.BoxType?.createCriteria().count(){
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
	 * Function to get the box types from category
	 * @return
	 */
	def getBoxTypeFromCategory() {
		List boxTypeList = []
		boxTypeList = BoxType.findAllByCategory(params.category)
		render boxTypeList as JSON
	}


}
