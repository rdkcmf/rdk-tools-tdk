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
 * Class to hold the job details 
 * @author Sreeja
 *
 */
class JobDetails {
   
	/**
	 * Name of job
	 */
	String jobName
    
    /**
     * Name of trigger
     */
	String triggerName
    
    /**
     * Type of Schedule
     */
	String scheduleType
	
    /**
     * Script that is executed
     */   
    List script
    
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
    
    String appUrl
    
    String realPath
    
    String filePath
    
    Date startDate
    
    Date endDate
    
    Date oneTimeScheduleDate
    
    String queryString   
	
	String isSystemDiagnostics
	
	String isBenchMark
	
	String isStbLogRequired
	
	Category category = Category.RDKV
	/**
	 * Rerun on failure
	 */
	String rerunOnFailure
	
	
	String rerun
	
	int repeatCount = 1
	
	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
    static hasMany = [script : String ]

    static constraints = {
        jobName(nullable:false, blank:false)
        triggerName(nullable:false, blank:false)
        scheduleType(nullable:true, blank:true)
        script(nullable:true, blank:true)
        scriptGroup(nullable:true, blank:true)
        device(nullable:true, blank:true)
        deviceGroup(nullable:true, blank:true)
        appUrl(nullable:false, blank:false)
        realPath(nullable:false, blank:false)
        startDate(nullable:true, blank:true)
        endDate(nullable:true, blank:true)
        oneTimeScheduleDate(nullable:true, blank:true)
        queryString(nullable:true, blank:true)
		isSystemDiagnostics(nullable:true, blank:true)
		isBenchMark(nullable:true, blank:true)
		isStbLogRequired(nullable:true, blank:true)
		rerun(nullable:true, blank:true)
		repeatCount(nullable:true, blank:true)
		groups(nullable:true, blank:true)
		category(nullable:false, blank:false) 
		rerunOnFailure(nullable:true, blank:true)
		
    }
    
    @Override
    String toString() {
        return jobName ?: 'NULL'
    }
	
	static mapping = {
		sort id : "desc"
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
	}
   
}
