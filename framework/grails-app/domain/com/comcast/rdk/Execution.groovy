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

import com.comcast.rdk.Category

/**
 * Domain class for saving the script execution details
 * @author sreejasuma
 *
 */

class Execution {
    
    /**
     * Name of execution
     */
    String name
    
    /**
     * Script that is executed
     */
    String script
    
    /**
     * Devices in which the script is executed
     */
    String device 
    
    /**
     * ScriptGroup that is executed
     */
    String scriptGroup
    
    /**
     * Device Group in which the script 
     * is executed
     */
    String deviceGroup
       
    /**
     * Result of the script execution
     */
    String result
    
    /**
     * The complete data obtained after the
     * execution of the script
     */
    String outputData
    
    /**
     * Date and time in which the script is executed
     */
    Date dateOfExecution
    
    /**
     * time taken for execution
     */
    String executionTime
	String realExecutionTime

    /**
     * Set of ExecutionResults to the execution
     */
     Set executionresults
	 
	/**
	 * Flag to identify the whether the given instance is marked for deletion or not.
	 */
	int isMarked = 0;
	
	/**
	 * Flag to mark the execution as aborted
	 */
	boolean isAborted = false
	
	boolean isRerunRequired = false
	
	boolean isStbLogRequired = false

	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
	boolean isPerformanceDone
	
	String executionStatus
	
	/**
	 * application url data
	 */
	String applicationUrl
	
	/**
	 * Flag to mark is bench mark enabled for the execution 
	 */
	boolean isBenchMarkEnabled = false
	
	/**
	 * Flag to mark is SystemDiagnostics enabled for the execution
	 */
	boolean isSystemDiagnosticsEnabled = false
	
	/**
	 *  Flag to mark as re-run failure  enabled for execution
	 */
	boolean rerunOnFailure = false
	
	
	
	/**
	 * Object to save the third party execution details for the execution(optional)
	 */
	ThirdPartyExecutionDetails thirdPartyExecutionDetails = null
	
	/**
	 * Script Count
	 */
	int scriptCount = 0
	
	Category category = Category.RDKV
	
	/**
	 * Execution can have many execution results.
	 */
	static hasMany = [ executionresults : ExecutionResult ]
    
    static constraints = {
        name(nullable:false, blank:false,unique:true)
        scriptGroup(nullable:true, blank:true)       
        deviceGroup(nullable:true, blank:true)
        result(nullable:true, blank:true)
        outputData(nullable:true, blank:true)       
        dateOfExecution(nullable:true, blank:true)  
        executionTime(nullable:true, blank:true)
        script(nullable:true, blank:true)
        device(nullable:true, blank:true)
		groups(nullable:true, blank:true)
		isPerformanceDone(nullable:true, blank:true)
		executionStatus(nullable:true, blank:true)
		thirdPartyExecutionDetails(nullable:true, blank:true)
		isBenchMarkEnabled(nullable:true, blank:true)
		isSystemDiagnosticsEnabled(nullable:true, blank:true)
		isAborted(nullable:true, blank:true)
		isRerunRequired(nullable:true, blank:true)
		isStbLogRequired(nullable:true, blank:true)
		applicationUrl(nullable:true, blank:true)
		rerunOnFailure(nullable:true, blank:true)
		scriptCount(nullable:true, blank:true)
		realExecutionTime(nullable:true, blank:true)
		category(nullable:false, blank:false)
    }
    
    static mapping = {
        //cache true
        outputData type: 'text'
        sort id : "desc"
		executionresults sort:'id' , order: 'asc'
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
    }
    
    @Override
    String toString() {
        return name ?: 'NULL'
    }
}
