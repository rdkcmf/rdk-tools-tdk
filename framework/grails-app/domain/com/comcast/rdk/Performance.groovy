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

class Performance {

	ExecutionResult executionResult
	
	String performanceType
	
	String processName
	
	String processValue
	
	String processValue1
	
	Category category = Category.RDKV
	
	//static belongsTo = [ executionResult:ExecutionResult ]
	
    static constraints = {
		executionResult(nullable:true, blank:true)
		performanceType(nullable:true, blank:true)
		processName(nullable:true, blank:true)
		processValue(nullable:true, blank:true)
		processValue1(nullable:true, blank:true)
		category(nullable:false, blank:false)
    }
	
	static mapping = {
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
	}
}
