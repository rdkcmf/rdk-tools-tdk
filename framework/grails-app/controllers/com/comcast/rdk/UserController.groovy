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
import grails.converters.JSON

import org.apache.shiro.SecurityUtils
import org.apache.shiro.crypto.hash.Sha256Hash

class UserController {

   def mailService
	
   static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

    def index() {
        redirect(action: "create")
    }

    def create(Integer max) {
        params.max = Math.min(max ?: 10, 100)
        [userInstance: new User(params),userInstanceList: User.list(params), userInstanceTotal: User.count()]
    }

	
    def save(Integer max) {		
        params.max = Math.min(max ?: 10, 100)
        def userInstance = new User(params)
		userInstance.passwordHash = new Sha256Hash(params?.passwordHash).toHex()
        if (!userInstance.save(flush: true)) {
            render(view: "create", model: [userInstance: userInstance, userInstanceList: User.list(params), userInstanceTotal: User.count()])
            return
        }

        flash.message = message(code: 'default.created.message', args: [message(code: 'user.label', default: 'User'), userInstance.username])
        redirect(action: "create")
    }
	
	/**
	 * Method to get the page to register a new user.
	 * @return
	 */
	def registerUser(){
		if(params?.userId){
			[userInstance: User.findById(params?.userId)]
		}
		else{
			[userInstance: new User(params)]
		}
	}

	/**
	 * Method to save the new user from the register user page
	 * @return
	 */
	def saveUser() {
		def userInstance = new User(params)
		/*if( params?.passwordHash!= params?.confirmPassword){
			flash.error = "The passwords you entered has a mismatch"
			render(view: "registerUser", model: [userInstance: userInstance])
			return
		}*/
		userInstance.passwordHash = new Sha256Hash(params?.passwordHash).toHex()
		if (!userInstance.save(flush: true)) {
			render(view: "registerUser", model: [userInstance: userInstance])
			return
		}
		Role role = Role.findByName("ADMIN")
		def userCriteria = User.createCriteria()
		def results = userCriteria.list {
			roles {
				eq('name', "ADMIN")
			}
		}
		try {
			mailService.sendMail {
				to results.email.toArray()
				subject "New User Registration"
				body ' [RDK Tool] : User '+userInstance.name+' is registed with username '+userInstance?.username + "Approval pending from Administrator"
			}

		} catch (Exception e) {
			e.printStackTrace()
		}
		flash.message = message(code: 'default.registered.message', args: [message(code: 'user.label', default: 'User'), userInstance?.name])
		redirect(action: "registerUser", params: [userId: userInstance?.id])
	}
	
	def changePassword = {
		if(!(params?.username).trim()){
			flash.error =  "Please enter valid username"
		}
		else {
			def userInstance = User.findByUsername(params?.username)
		
			if (!userInstance || userInstance == null) {
				flash.error =  "Please enter valid username"
			}
			else {
				if((userInstance.roles).empty){
					flash.error="Your approval is pending.Please contact admin for approval"
				}
				else {
					def oldPasswordByUser =new Sha256Hash (params?.oldPassword).toHex()
					
					if(oldPasswordByUser != userInstance.passwordHash){
						flash.error = "Invalid username or password"
					}
					else {
			
						if((!(params?.newPassword).trim())&&(!(params?.confirmPassword).trim())) {
							flash.error = "Enter valid new password"
						}
						else {
							if( params?.newPassword!= params?.confirmPassword){
								flash.error = "The passwords you entered has a mismatch"
							}
							else {
								userInstance.passwordHash =new Sha256Hash(params?.newPassword).toHex()
								if (!userInstance.save(flush: true)) {
									flash.error  ="Password updation failed"
								}
								else {
									flash.message = "Password is updated successfully"
								}
							}
						}
					}
				}
			}
		}
		render(template: "resultMessage", model: [params : params])
	}
	
    def update(Long id, Long version, Integer max) {
        def userInstance = User.get(id)
		params.max = Math.min(max ?: 10, 100)
        if (!userInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'user.label', default: 'User'), id])
            render(view: "create", model: [userInstance: userInstance, userInstanceList: User.list(params), userInstanceTotal: User.count()])
            return
        }
		
		def userBasedOnName = User?.findByName(params?.username)
		
		if(userBasedOnName && (userBasedOnName?.id !=  userInstance?.id)){
			flash.message = message(code: 'default.not.unique.message', args: [message(code: 'user.label', default: 'UserName')])
			render(view: "create", model: [userInstance: userInstance, userInstanceList: User.list(params), userInstanceTotal: User.count()])
            return
		}
		
        if (version != null) {
            if (userInstance.version > version) {
                userInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
                          [message(code: 'user.label', default: 'User')] as Object[],
                          "Another user has updated this User while you were editing")
                render(view: "create", model: [userInstance: userInstance, userInstanceList: User.list(params), userInstanceTotal: User.count()])
                return
            }
        }
		def oldRole = userInstance.roles
		def oldpassword=userInstance.passwordHash
		def passwrd = userInstance.passwordHash
		userInstance.properties = params
		if(params?.passwordHash){
			def updatedPassword = params?.passwordHash
			if(updatedPassword.equals(passwrd)){
				userInstance.passwordHash = params?.passwordHash
			}
			else{
				userInstance.passwordHash = new Sha256Hash(params?.passwordHash).toHex()
			}
		}
		else{
			userInstance.passwordHash = passwrd
		}
        if (!userInstance.save(flush: true)) {
            render(view: "create", model: [userInstance: userInstance, userInstanceList: User.list(params), userInstanceTotal: User.count()])
            return
        }

        flash.message = message(code: 'default.updated.message', args: [message(code: 'user.label', default: 'User'), userInstance.username])
        redirect(action: "create")
    }
	
	def populateFields(){
		def valueList = []
		User user = User.findById(params?.id)
		valueList.add( user?.id )
		valueList.add( user?.name )
		valueList.add( user?.email )
		valueList.add( user?.username )
		valueList.add( user?.groupName?.id )
		if(user?.passwordHash){
			valueList.add( user?.passwordHash )
		}
		else{
			valueList.add("null")
		}
		user?.roles.each{rol ->
			valueList.add( rol?.id )
		}
		render valueList as JSON
	}
	
	def deleteUser(){
		def countVariable = 0
		def userInstance
		int deleteCount = 0
		String currentUser = ""
		if(params?.listCount){
			// to delete record(s) from list.gsp
			for (iterateVariable in params?.listCount){
				countVariable++
				if(params?.("chkbox"+countVariable) == KEY_ON){
					def idDb = params?.("id"+countVariable).toLong()
					userInstance = User.get(idDb)
					if (userInstance) {
						User userInst = User.findByUsername(SecurityUtils.subject.principal)
						if(userInst && userInst?.id == idDb ){
							currentUser = "ADMINISTRATOR"
							//flash.message = "Cannot delete the current user..."
						}else{
							try{							
								userInstance.delete(flush:true)
								deleteCount++
							}
							catch (Exception e) {
								flash.message = message(code: 'default.not.deleted.message', args: [
									message(code: 'user.label', default: 'User'),
									userInstance?.username
								])
							}
						}
					}
				}
			}
		}
		if(deleteCount  > 1){
			flash.message = "Multiple users deleted"
		}else if (currentUser.toString().equals("ADMINISTRATOR")){
			flash.message = "Cannot delete the current user..."
		}
		else{
			flash.message = message(code: 'default.deleted.message', args: [
			message(code: 'user.label', default: 'User'),
			userInstance.username
			])
		}

		

		redirect(action: "create")
	}
	
	
}
