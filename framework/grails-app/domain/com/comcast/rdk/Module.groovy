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
 * Class represents a RDK module.
 * @author ajith
 */
class Module{

    /**
     * Name of the module
     */
    String name

    /**
     * Group associated with the module
     */
    TestGroup testGroup
    
    /**
     * RDK Version
     */
    String rdkVersion = "1"
	
	/**
	 * Time required for executing script
	 */
	int executionTime
    
	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
	/**
	 * Indicates the category to which the device belongs - RDK-V or RDK-B
	 */
	Category category = Category.RDKV

	static hasMany = [logFileNames: String , stbLogFiles :String]
	
    static constraints = {
//        name(unique:true, blank:false, nullable:false)
        testGroup(nullable:false, blank:false)
        rdkVersion(nullable:false, blank:false)
		groups(nullable:true, blank:true)	
		executionTime(nullable:true, blank:true)
		category(nullable:false, blank:false)
		name(blank:false, nullable:false,unique:'category' )
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
