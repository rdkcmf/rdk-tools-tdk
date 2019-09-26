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
import com.comcast.rdk.Category

/**
 * Domain class for saving the script execution details
 * @author sreejasuma
 *
 */


class ExecutionResult {

    Execution execution
    
	ExecutionDevice executionDevice	
	
    /**
     * Script that is executed
     */
    String script
    
    /**
     * Devices in which the script is executed
     */
    String device
    
    /**
     * Status of execution of script
     */
    String status = "UNDEFINED"
    
    /**
     * Set of ExecuteMethodResult to the ExecutionResult
     */
    Set executemethodresults
	
	String executionOutput
	
	Set performance
	
	Device execDevice
	
	String deviceIdString
	
	/**
	 * Date and time in which the script is executed
	 */
	Date dateOfExecution
	
	String executionTime
	
	String moduleName
	
	String totalExecutionTime 
	
	Category category = Category.RDKV
	
    /**
     * Execution can have many execution results.
     */
    static hasMany = [ executemethodresults : ExecuteMethodResult, performance :  Performance]
	
    
    static constraints = {             
        script(nullable:false, blank:false)
        device(nullable:false, blank:false)
        status(nullable:true, blank:true)
		executionOutput(nullable:true, blank:true)		
		execDevice(nullable:true, blank:true)
		deviceIdString(nullable:true, blank:true)
		dateOfExecution(nullable:true, blank:true)
		executionTime(nullable:true, blank:true)
		moduleName(nullable:true, blank:true)
		totalExecutionTime(nullable:true, blank:true)
		category(nullable:false, blank:false)
		
    }
    
    static mapping = {
        cache true
		executionOutput type: 'text'
        sort id : "asc"
		executemethodresults sort: 'id', order: 'asc'
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
    }
    
}
