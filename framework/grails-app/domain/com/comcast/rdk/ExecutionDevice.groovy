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

import java.util.Date;
import java.util.Set;
import com.comcast.rdk.Category

/**
 * Domain class for saving the device in script Execution
 * @author sreejasuma
 */

class ExecutionDevice {

    Execution execution

    /**
     * Device in which the script is executed
     */
    String device
	
	/**
	 * DeviceIP in which the script is executed
	 */
	String deviceIp
	
	/**
	 * Status of the execution
	 */
    String status = "UNDEFINED"
	
	/**
	 * Date and time in which the script is executed
	 */
	Date dateOfExecution
	
	/**
	 * Build name of the executed device
	 */
	String buildName 
	
	/**
	 * Start time of execution
	 */
	String executionTime
	
	/**
	 * Set of ExecutionResults to the execution
	 */
	Set executionresults
	
	Category category = Category.RDKV
	 
    /**
	 * Execution can have many execution results.
	 */
	static hasMany = [ executionresults : ExecutionResult ]
    
    static constraints = {             
        device(nullable:false, blank:false)
		execution(nullable:false, blank:false)
		dateOfExecution(nullable:true, blank:true)
		buildName(nullable:true, blank:true)
		executionTime(nullable:true, blank:true)
		status(nullable:false, blank:false)
		deviceIp(nullable:false, blank:false)
		category(nullable:false, blank:false)
    }
    
    static mapping = {
        cache true
        sort id : "desc"
		executionresults sort: 'id', order: 'asc'
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
    }
    
}
