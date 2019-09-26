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
 * Class represents RDK Versions.
 */
class RDKVersions {
    
    /**
     * Name of the RDK Version
     */
	String buildVersion

	/**
	 * Indicates the group name which the box belongs
	 */
	Groups groups
	
	Category category = Category.RDKV
    
    static constraints = {
		buildVersion(unique:true, blank:false, nullable:false)
		groups(nullable:true, blank:true)
		category(nullable:false,blank:false)
    }

	@Override
	String toString() {
		return buildVersion ?: 'NULL'
	}
	
	static mapping = {
		sort buildVersion : "asc"
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
	}
}
