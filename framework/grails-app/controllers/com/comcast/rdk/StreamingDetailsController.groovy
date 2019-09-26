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
/**
 * Controller class for streaming details operations
 * @author sreejasuma
 *
 */
class StreamingDetailsController {

	def utilityService
	
    static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

    def index() {
        redirect(action: "list", params: params)
    }

    /**
     * List stream details
     * @return
     */
    def list() {    
		def streamingDetailsList = StreamingDetails.findAllByGroupsOrGroupsIsNull(utilityService.getGroup())   
		def radioStreamingDetailsList = RadioStreamingDetails.findAllByGroupsOrGroupsIsNull(utilityService.getGroup())
        [streamingDetailsInstanceList: streamingDetailsList,radioStreamingDetails: radioStreamingDetailsList,streamingDetailsInstanceTotal: streamingDetailsList.size(),radioStreamingDetailsInstanceTotal: radioStreamingDetailsList.size()]
    }

    /**
     * Create stream details
     * @return
     */
    def create() {
        [streamingDetailsInstance: new StreamingDetails(params)]
    }
	
	def createRadio() {
		[streamingDetailsInstance: new RadioStreamingDetails(params)]
	}

    /**
     * Save stream details
     * @return
     */
    def save() {
        def streamingDetailsInstance = new StreamingDetails(params)
		streamingDetailsInstance.groups = utilityService.getGroup()
        if (!streamingDetailsInstance.save(flush: true)) {
			flash.message = " StreamId should be  Unique "
          // render(view: "create", model: [streamingDetailsInstance: streamingDetailsInstance])
            redirect(action: "list")
            return
        }

        flash.message = message(code: 'default.created.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
        redirect(action: "list")
    }
	
	def saveRadio() {
		def streamingDetailsInstance = new RadioStreamingDetails(params)
		if(params?.streamId?.startsWith("R")){
		streamingDetailsInstance.groups = utilityService.getGroup()
		if (!streamingDetailsInstance.save(flush: true)) {
		flash.message = " Radio StreamId should be  Unique "
		  // render(view: "create", model: [streamingDetailsInstance: streamingDetailsInstance])
			redirect(action: "list")
			return
		}

		flash.message = message(code: 'default.created.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
		}else{
		flash.message = "Stream id should start with R"
		
		}
		redirect(action: "list")
	}

    /**
     * Show stream details
     * @return
     */
    def show(Long id) {
        def streamingDetailsInstance = StreamingDetails.get(id)
        if (!streamingDetailsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
            return
        }

        [streamingDetailsInstance: streamingDetailsInstance]
    }

    /**
     * Edit stream details
     * @return
     */
    def edit(Long id) {
        def streamingDetailsInstance = StreamingDetails.get(id)
        if (!streamingDetailsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
            return
        }

        [streamingDetailsInstance: streamingDetailsInstance]
    }
	
	def editRadio(Long id) {
		def streamingDetailsInstance = RadioStreamingDetails.get(id)
		if (!streamingDetailsInstance) {
			flash.message = message(code: 'default.not.found.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
			redirect(action: "list")
			return
		}
		[streamingDetailsInstance: streamingDetailsInstance]
	}

    /**
     * Update stream details
     * @return
     */
    def update(Long id, Long version) {
        def streamingDetailsInstance = StreamingDetails.get(id)
        if (!streamingDetailsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
            return
        }

        if (version != null) {
            if (streamingDetailsInstance.version > version) {
                streamingDetailsInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
                          [message(code: 'streamingDetails.label', default: 'StreamingDetails')] as Object[],
                          "Another user has updated this StreamingDetails while you were editing")
                //render(view: "edit", model: [streamingDetailsInstance: streamingDetailsInstance])
                redirect(action: "list")
                return
            }
        }

        streamingDetailsInstance.properties = params

        if (!streamingDetailsInstance.save(flush: true)) {
			flash.message = " StreamId should be  Unique "
           // render(view: "edit", model: [streamingDetailsInstance: streamingDetailsInstance])
            redirect(action: "list")
            return
        }

        flash.message = message(code: 'default.updated.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
        redirect(action: "list")
    }
	/**
	 * update the radio stream details 
	 * @param id
	 * @param version
	 * @return
	 */
	 def updateRadio(Long id,Long version)
	  {
			def radioStreamingDetailsInstance= RadioStreamingDetails.get(id)
			if(!radioStreamingDetailsInstance){
				flash.message = message(code: 'default.not.found.message', args: [message(code: 'radioStreamingDetails.label', default: 'RadioStreamingDetails'), radioStreamingDetailsInstance.streamId])
				redirect(action: "list")
				return
			}
			
			if(version != null )
			{
				if(radioStreamingDetailsInstance.version > version){
					radioStreamingDetailsInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
						[message(code: 'radioStreamingDetails.label', default: 'RadioStreamingDetails')] as Object[],
						"Another user has updated this RadioStreamingDetails while you were editing")
							//render(view: "edit", model: [streamingDetailsInstance: streamingDetailsInstance])
			  redirect(action: "list")
			  return
			}
			radioStreamingDetailsInstance.properties = params
			if (!radioStreamingDetailsInstance.save(flush: true)) {
				flash.message = " Radio StreamId should be  Unique "
				// render(view: "edit", model: [streamingDetailsInstance: streamingDetailsInstance])
				 redirect(action: "list")
				 return
			 }
	 
			 flash.message = message(code: 'default.updated.message', args: [message(code: 'radioStreamingDetails.label', default: 'RadioStreamingDetails'),radioStreamingDetailsInstance.streamId])
			 redirect(action: "list")
			}
	
	  }
	 

    /**
     * Delete stream details
     * @return
     */
    def delete(Long id) {
        def streamingDetailsInstance = StreamingDetails.get(id)
        if (!streamingDetailsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
            return
        }

        try {
            streamingDetailsInstance.delete(flush: true)
            flash.message = message(code: 'default.deleted.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
        }
        catch (DataIntegrityViolationException e) {
            flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
        }
    }
    
    /**
     * Delete stream details
     * @return
     */
    def deleteStreamDetails() {
      Long id = params.id as Long
      def streamingDetailsInstance = StreamingDetails.get(id)
        if (!streamingDetailsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
            return
        }

        try {
            streamingDetailsInstance.delete(flush: true)
            flash.message = message(code: 'default.deleted.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
        }
        catch (DataIntegrityViolationException e) {
            flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
        }
    }
	
	def deleteRadioStreamDetails() {
		Long id = params.id as Long
		def radioStreamingDetailsInstance = RadioStreamingDetails.get(id)
		  if (!radioStreamingDetailsInstance) {
			  flash.message = message(code: 'default.not.found.message', args: [message(code: 'radioStreamingDetails.label', default: 'RadioStreamingDetails'), radioStreamingDetailsInstance.streamId])
			  redirect(action: "list")
			  return
		  }
  
		  try {
			  radioStreamingDetailsInstance.delete(flush: true)
			  flash.message = message(code: 'default.deleted.message', args: [message(code: 'radioStreamingDetails.label', default: 'RadioStreamingDetails'), radioStreamingDetailsInstance.streamId])
			  redirect(action: "list")
		  }
		  catch (DataIntegrityViolationException e) {
			  flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'radioStreamingDetails.label', default: 'RadioStreamingDetails'), radioStreamingDetailsInstance.streamId])
			  redirect(action: "list")
		  }
	  }
    
   
}
