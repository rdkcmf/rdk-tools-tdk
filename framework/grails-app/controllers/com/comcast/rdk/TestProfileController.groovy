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

import java.util.List;

import org.springframework.dao.DataIntegrityViolationException
import grails.converters.JSON

class TestProfileController {
	def utilityService
	static allowedMethods = [save: "POST", update: "POST", delete: "POST"]
	
	def index() {
		redirect(action: "create", params: params)
	}
	/**
	 * For creating the TM  
	 * @param max
	 * @return
	 */
	def create(Integer max) {
		params.max = Math.min(max ?: 10, 100)
		def groupsInstance = utilityService.getGroup()
		//def scriptTagList = ScriptTag.findAllByGroupsOrGroupsIsNull(groupsInstance,params)
		//def scriptTagListCnt = ScriptTag.findAllByGroupsOrGroupsIsNull(groupsInstance)
		def testProfileList = getTestProfileList(groupsInstance,params)
		[testProfileInstance: new TestProfile(params) ,testProfileInstanceList: testProfileList, testProfileInstanceTotal: getTestProfileCount(groupsInstance, params), category:params?.category]
	}
	/**
	 * function for save the test profile
	 * @param max
	 * @return
	 */
	def save(Integer max) {

		def testProfileInstance = new TestProfile(params)
		params.max = Math.min(max ?: 10, 100)
		def groupsInstance = utilityService.getGroup()
		def testProfileList = getTestProfileList(groupsInstance,[name:'name',order:'asc'])

		testProfileInstance.groups = groupsInstance
		if (!testProfileInstance.save(flush: true)) {
			render(view: "create", model: [testProfileInstance: testProfileInstance,testProfileInstanceList: testProfileList, testProfileInstanceTotal: getTestProfileCount(groupsInstance, params), category:params?.category])
			return
		}

		flash.message = message(code: 'default.created.message', args: [message(code: 'testProfile.label', default: 'TestProfile'), testProfileInstance.name])
		redirect(action: "create",  params:[category:params?.category])
	}
	/**
	 * Function for updating the test profile
	 * @param id
	 * @param version
	 * @param max
	 * @return
	 */
	def update(Long id, Long version,Integer max) {
		def testProfileInstance = TestProfile.get(id)
		def groupsInstance = utilityService.getGroup()
		def testProfileList = getTestProfileList(groupsInstance,params)
		params.max = Math.min(max ?: 10, 100)
		if (!testProfileInstance) {
			flash.message = message(code: 'default.not.found.message', args: [message(code: 'testProfile.label', default: 'TestProfile'), id])
			render(view: "create", model: [testProfileInstance: testProfileInstance,testProfileInstanceList: testProfileList])
			return
		}

		def testProfileBasedOnName = TestProfile?.findByName(params?.name)

		if(testProfileBasedOnName && (testProfileBasedOnName?.id !=  testProfileInstance?.id)){
			flash.message = message(code: 'default.not.unique.message', args: [message(code: 'scriptTag.label', default: 'ScriptTag Name')])
			render(view: "create", model: [testProfileInstance: testProfileInstance,testProfileList: testProfileList])
			return
		}

		if (version != null) {
			if (testProfileInstance.version > version) {
				testProfileInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
						[message(code: 'testProfile.label', default: 'TestProfile')] as Object[],
						"Another user has updated this ScriptTag while you were editing")
				render(view: "create", model: [testProfileInstance: testProfileInstance,testProfileInstanceList: testProfileList])
				return
			}
		}

		testProfileInstance.properties = params

		if (!testProfileInstance.save(flush: true)) {
			render(view: "create", model: [testProfileInstance: testProfileInstance,testProfileInstanceList: testProfileList])
			return
		}

		flash.message = message(code: 'default.updated.message', args: [message(code: 'testProfile.label', default: 'TestProfile'), testProfileInstance.name])
		redirect(action: "create",  params:[category:params?.category])
	}
	
	/**
	 *  Function for deleting one or more test profile.
	 * @return
	 */
	
	def deleteTestProfile(){
		def countVariable = 0
		int deleteCount = 0
		def testProfileInstance
		if(params?.listCount){ // to delete record(s) from list.gsp
			for (iterateVariable in params?.listCount){
				countVariable++
				if(params?.("chkbox"+countVariable) == KEY_ON){
					def idDb = params?.("id"+countVariable).toLong()
					testProfileInstance = TestProfile.get(idDb)
					if (testProfileInstance) {
						try{
							testProfileInstance.delete(flush: true)
							deleteCount++
						}
						catch (DataIntegrityViolationException e) {
							flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'testProfile.label', default: 'TestProfile'),  testProfileInstance.name])
						}
					}
				}
			}
		}

		if(deleteCount  > 1)
		{
			flash.message = "TestProfiles deleted"
		}
		else
		{
			flash.message = message(code: 'default.deleted.message', args: [message(code: 'testProfile.label', default: 'TestProfile'),  testProfileInstance.name])
		}
		redirect(action: "create" ,  params:[category:params?.category])
	}
/**
 * function for get all test profile list
 * @return
 */
	def getTestProfile() {
		List testProfileInstanceList = []
		TestProfile testProfile = TestProfile.findById(params.id)
		if(testProfile){
			testProfileInstanceList.add(testProfile.name)
		}
		render testProfileInstanceList as JSON
	}
	/**
	 * function for get all test profile based using the category
	 * @param groups
	 * @param params
	 * @return
	 */

	private List getTestProfileList(def groups, def params){
		return  TestProfile.createCriteria().list(max:params?.max, offset:params?.offset ){
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
	/**
	 * Function for getting number of test profile count
	 * @param groups
	 * @param params
	 * @return
	 */
	private int getTestProfileCount(def groups, def params){
		return  TestProfile.createCriteria().count(){
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
