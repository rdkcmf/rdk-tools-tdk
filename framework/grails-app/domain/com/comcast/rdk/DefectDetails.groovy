/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2019 RDK Management
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
 * Domain class for saving the defect  analysis details
 * 
 * @author divyarajam
 */

class DefectDetails {

	/**
	 * Name of the script
	 */
	String scriptName
	/**
	 * Execution id
	 */
	int executionId
	/**
	 * JIRA ticket number corresponding to the defect
	 */
	String ticketNumber
	/**
	 * Type of defect like script issue, environment issue, RDK issue etc
	 */
	String  defectType
	/**
	 * Remarks field to store more details about the defect
	 */
	String remarks
	static constraints = {
		scriptName(nullable:false, blank:false)
		executionId(nullable:false, blank:false)
		ticketNumber(nullable:true, blank:true)
		defectType(nullable:true, blank:true)
		remarks(nullable:true, blank:true)
	}

	static mapping = {
		cache true
		sort id : "asc"
		datasource 'ALL'
	}
}
