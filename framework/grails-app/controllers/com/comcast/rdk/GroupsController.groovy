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
import grails.converters.JSON

class GroupsController {

    static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

    def index() {
        redirect(action: "create",params:params)
    }

	def create(Integer max) {
		params.max = Math.min(max ?: 10, 100)
		[groupsInstance: new Groups(params), groupsInstanceList: Groups.list(), groupsInstanceTotal: Groups.count(), category:params?.category]
	}
   
    def save(Integer max) {
        def groupsInstance = new Groups(params)
		params.max = Math.min(max ?: 10, 100)
        if (!groupsInstance.save(flush: true)) {
            render(view: "create", model: [groupsInstance: groupsInstance,groupsInstanceList: Groups.list(), groupsInstanceTotal: Groups.count(), category:params?.category])
            return
        }
        flash.message = message(code: 'default.created.message', args: [message(code: 'groups.label', default: 'Groups'), groupsInstance?.name])
        redirect(action: "create", params:[category:params?.category])
    }

   
    def update(Long id, Long version, Integer max) {
        def groupsInstance = Groups.get(id)
		params.max = Math.min(max ?: 10, 100)
        if (!groupsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'groups.label', default: 'Groups'), groupsInstance?.name])
            redirect(action: "create", params:[category:params?.category])
            return
        }

		def groupBasedOnName = BoxType?.findByName(params?.name)
		
		if(groupBasedOnName && (groupBasedOnName?.id !=  groupsInstance?.id)){
			flash.message = message(code: 'default.not.unique.message', args: [message(code: 'groups.label', default: 'Group Name')])
			render(view: "create", model: [groupsInstance: groupsInstance,groupsInstanceList: Groups.list(), groupsInstanceTotal: Groups.count(),category:params?.category])
            return
		}
		
        if (version != null) {
            if (groupsInstance.version > version) {
                groupsInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
                          [message(code: 'groups.label', default: 'Groups')] as Object[],
                          "Another user has updated this Groups while you were editing")
                render(view: "create", model: [groupsInstance: groupsInstance,groupsInstanceList:Groups.list(), groupsInstanceTotal: Groups.count(), category:params?.category])
                return
            }
        }

        groupsInstance.properties = params

        if (!groupsInstance.save(flush: true)) {
            render(view: "create", model: [groupsInstance: groupsInstance,groupsInstanceList: Groups.list(), groupsInstanceTotal: Groups.count(),category:params?.category])
            return
        }

        flash.message = message(code: 'default.updated.message', args: [message(code: 'groups.label', default: 'Groups'), groupsInstance?.name])
        redirect(action: "create", params:[category:params?.category])
    }

    def deleteGroup(){
		def countVariable = 0
		int deleteCount = 0
		def groupInstance
		if(params?.listCount){
			// to delete record(s) from list.gsp
			for (iterateVariable in params?.listCount){
				countVariable++
				if(params?.("chkbox"+countVariable) == "on"){
					def idDb = params?.("id"+countVariable).toLong()
					groupInstance = Groups.get(idDb)
					if (groupInstance) {
						try{
							groupInstance.delete(flush: true)
							deleteCount++	
						}
						catch (DataIntegrityViolationException e) {
							flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'groups.label', default: 'Groups'),  groupInstance?.name])
						}						
					}
				}
			}
			}
		if(deleteCount  == 1)
		{
			flash.message = message(code: 'default.deleted.message', args: [message(code: 'groups.label', default: 'Groups'),  groupInstance?.name])
		}
		else
		{
			flash.message = "Multiple groups deleted"
		}
		redirect(action: "create",params:[category:params?.category])
	}

	def getGroup() {
		List groupInstanceList = []
		Groups groupInstance = Groups.findById(params.id)
		if(groupInstance){
			groupInstanceList.add(groupInstance.name)
		}
		render groupInstanceList as JSON
	}
	
}
