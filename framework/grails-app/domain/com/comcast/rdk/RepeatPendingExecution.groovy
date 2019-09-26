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
 * Domain class to save the pending execution repeat details
 *
 */
class RepeatPendingExecution {
	
	/**
	 * Name of the device for which repeat is pending
	 */
	String deviceName
	
	/**
	 * status of repeat pending execution
	 */
	String status
	
	/**
	 * name of the execution which is to be repeated
	 */
	String executionName
	
	/**
	 * number of complete execution pending
	 */
	int completeExecutionPending = 0
	
	/**
	 * index of the current execution
	 */
	int currentExecutionCount = -1
	
	Category category = Category.RDKV

    static constraints = {
		deviceName(nullable:false, blank:false)
		status(nullable:false, blank:false)
		completeExecutionPending(nullable:true, blank:true)
		currentExecutionCount(nullable:true, blank:true)
		executionName(nullable:false, blank:false)
		category(nullable:false, blank:false)
    }
	
	@Override
	String toString() {
		return (deviceName + " - " + executionName) ?: 'NULL'
	}
	static mapping = {
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
	}
}
