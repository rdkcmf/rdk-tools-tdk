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
 * domain object to save the third party execution details
 *
 */
class ThirdPartyExecutionDetails {
	
	Execution execution
	
	String execName
	
	String url
	
	String callbackUrl
	
	String filePath
	
	long executionStartTime
	
	String imageName
	
	String boxType
	
	Category category = Category.RDKV

    static constraints = {
		execName(nullable:true, blank:true)
		url(nullable:true, blank:true)
		callbackUrl(nullable:true, blank:true)
		filePath(nullable:true, blank:true)
		imageName(nullable:true, blank:true)
		boxType(nullable:true, blank:true)
		executionStartTime(nullable:true, blank:true)
		category(nullable:false, blank:false)
    }
	
	static mapping = {
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
	}
}
