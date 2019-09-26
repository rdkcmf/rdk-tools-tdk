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
 * Domain class for grouping the scripts
 * @author sreejasuma
 *
 */

class ScriptGroup {

    /**
     * Name of the Group.     
     */
    String name

    /**
     * Set of Scripts to the ScriptGroup
     */    
    Set scripts
	
	List scriptsList
	
	List scriptList

    /**
     * Status of the scriptgroup
     * Whether the scriptgroup is selected for execution
     */
    Status status = Status.FREE

	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
	Category category = Category.RDKV
	
    /**
     * ScriptGroup can have many scripts.
     */
    static hasMany = [ scripts : Script , scriptsList : Script, scriptList: ScriptFile]

    static constraints = {
        name(nullable:false, blank:false, unique:true)
        status(nullable:true, blank:true)
		groups(nullable:true, blank:true)
		scriptList(nullable:true,blank:true)
		category(nullable:false,blank:false)
    }
    
    static mapping = {
        cache true
        sort name : "asc"            
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
    }
    
    @Override
    String toString() {
        return name ?: 'NULL'
    }

   
    
    
}
