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
/**
 * Class that holds script details.
 * @author ajith
 */
class Script {
    
    /**
     * Name of the script.
     * Name shall not be empty.
     */
    String name
    
    /**
     * ScriptContent    
     */
    String scriptContent

    /**
     * Primitive test Name
     */
    PrimitiveTest primitiveTest

    /**
     * Short description about the script
     */
    String synopsis
	
	/**
	 * Boxtypes of script
	 */
    Set boxTypes
	
	/**
	 * RDK Versions of script
	 */
	Set rdkVersions
	
    /**
     * Status of the script
     * Whether the script is selected for execution 
     */
    Status status =  Status.FREE
	
	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
	/**
	 * Execution Time
	 */
	int executionTime
	
	/**
	 * true if script needs to be skipped while executing test suite
	 */
	boolean skip = false
	
	/**
	 * Short description about the reason for skipping the script
	 */
	String remarks = ""
	
	/**
	 * true if script is a long duration script 
	 */
	boolean longDuration = false
	
	
	static hasMany = [boxTypes: BoxType , rdkVersions : RDKVersions]

    static constraints = {
        name(nullable:false, blank:false, unique:true)
        synopsis(nullable:true, blank:true)
        scriptContent(blank:true)
        status(nullable:true, blank:true)
		groups(nullable:true, blank:true)
		executionTime(nullable:true, blank:true)		
    }
	
    /**
     * ScriptContent can be LongText field.
     */
    static mapping = {
        scriptContent type: 'text'
        synopsis type: 'text'
        sort name : "asc"
		datasource 'ALL'
    }

    @Override
    String toString() {
        return name ?: 'NULL'
    }
 
   
    
}
