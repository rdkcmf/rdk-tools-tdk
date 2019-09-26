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

import org.grails.datastore.gorm.finders.MethodExpression.IsNull;
import org.springframework.dao.DataIntegrityViolationException
import grails.converters.JSON

import com.comcast.rdk.Category 


class SoCVendorController {

	def utilityService
	
    static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

    def index() {
        redirect(action: "create", params: params)
    }
	
    def create(Integer max) {
		params.max = Math.min(max ?: 10, 100)
		def groupsInstance = utilityService.getGroup()
		def category = Utility.getCategory(params?.category)
		def soCVendorList = getVendorList(groupsInstance, params) 
		def soCVendorListCnt = getVendorListCount(groupsInstance, category)
		[soCVendorInstance: new SoCVendor(params) ,soCVendorInstanceList: soCVendorList, soCVendorInstanceTotal: soCVendorListCnt, category:params?.category]
    }

    def save(Integer max) {
        def soCVendorInstance = new SoCVendor(params)
		params.max = Math.min(max ?: 10, 100)		
		def groupsInstance = utilityService.getGroup()
		def category = Utility.getCategory(params?.category)
		def soCVendorList = getVendorList(groupsInstance, [name:'name',order:'asc']) 
		def soCVendorListCnt =  getVendorListCount(groupsInstance, category)
		soCVendorInstance.groups = groupsInstance
        if (!soCVendorInstance.save(flush: true)) {
            render(view: "create", model: [soCVendorInstance: soCVendorInstance,soCVendorInstanceList: soCVendorList, soCVendorInstanceTotal: soCVendorListCnt], category:params?.category)
            return
        }

        flash.message = message(code: 'default.created.message', args: [message(code: 'soCVendor.label', default: 'SoCVendor'), soCVendorInstance.name])
        redirect(action: "create", params:[category:params?.category])
    }

    def update(Long id, Long version,Integer max) {
        def soCVendorInstance = SoCVendor.get(id)		
		def groupsInstance = utilityService.getGroup()
		def category = Utility.getCategory(params?.category)
		def soCVendorList = getVendorList(groupsInstance, params) 
		def soCVendorListCnt =  getVendorListCount(groupsInstance, category)
		params.max = Math.min(max ?: 10, 100)
        if (!soCVendorInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'soCVendor.label', default: 'SoCVendor'), id])
            render(view: "create", model: [soCVendorInstance: soCVendorInstance,soCVendorInstanceList: soCVendorList, soCVendorInstanceTotal: soCVendorListCnt, category:params?.category])
            return
        }
		
		def socVendorBasedOnName = SoCVendor?.findByName(params?.name)
		
		if(socVendorBasedOnName && (socVendorBasedOnName?.id !=  soCVendorInstance?.id)){
			flash.message = message(code: 'default.not.unique.message', args: [message(code: 'soCVendor.label', default: 'SoCVendor Name')])
			render(view: "create", model: [soCVendorInstance: soCVendorInstance,soCVendorInstanceList: soCVendorList, soCVendorInstanceTotal: soCVendorListCnt, category:params?.category])
			return
		}
		
        if (version != null) {
            if (soCVendorInstance.version > version) {
                soCVendorInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
                          [message(code: 'soCVendor.label', default: 'SoCVendor')] as Object[],
                          "Another user has updated this SoCVendor while you were editing")
                render(view: "create", model: [soCVendorInstance: soCVendorInstance,soCVendorInstanceList: soCVendorList, soCVendorInstanceTotal: soCVendorListCnt, category:params?.category])
                return
            }
        }

        soCVendorInstance.properties = params

        if (!soCVendorInstance.save(flush: true)) {
			render(view: "create", model: [soCVendorInstance: soCVendorInstance,soCVendorInstanceList: soCVendorList, soCVendorInstanceTotal: soCVendorListCnt, category:params?.category])
            return
        }

        flash.message = message(code: 'default.updated.message', args: [message(code: 'soCVendor.label', default: 'SoCVendor'), soCVendorInstance.name])
        redirect(action: "create",params:[category:params?.category])
    }
	
	def deleteSoCVendor(){
		def countVariable = 0
		int deleteCount = 0
		def soCVendorInstance
		if(params?.listCount){ // to delete record(s) from list.gsp
			for (iterateVariable in params?.listCount){
				countVariable++
				if(params?.("chkbox"+countVariable) == KEY_ON){
					def idDb = params?.("id"+countVariable).toLong()
					soCVendorInstance = SoCVendor.get(idDb)
					if (soCVendorInstance) {
						try{
							 soCVendorInstance.delete(flush: true)
							 deleteCount++
						 }
						 catch (DataIntegrityViolationException e) {
							 flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'soCVendor.label', default: 'SoCVendor'),  soCVendorInstance.name])
						 }						 
					}
				}
			}
		}
		
		if(deleteCount  > 1)
		{
			flash.message = "SoCVendors deleted"
		}
		else
		{
			flash.message = message(code: 'default.deleted.message', args: [message(code: 'soCVendor.label', default: 'SoCVendor'),  soCVendorInstance.name])
		}
		redirect(action: "create", params:[category:params?.category])
	}

	def getSoCVendor() {
		List soCVendorInstanceList = []
		SoCVendor soCVendor = SoCVendor.findById(params.id)
		if(soCVendor){
			soCVendorInstanceList.add(soCVendor.name)
		}
		render soCVendorInstanceList as JSON
	}
	
	private List getVendorList(def groups, def params){
		return  SoCVendor?.createCriteria().list(max:params?.max, offset:params?.offset ){
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
	
	private int getVendorListCount(def groups, def category){
		return  SoCVendor.createCriteria().count{
			or{
				isNull("groups")
				if(groups != null){
					eq("groups",groups)
				}
			}

			and{
				eq("category", category)
			}
		}
	}
}
