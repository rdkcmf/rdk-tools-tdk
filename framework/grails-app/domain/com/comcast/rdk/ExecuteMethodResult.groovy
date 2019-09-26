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
 * Domain class for saving the ExecuteMethodResult of each script execution details
 * @author sreejasuma
 *
 */

import com.comcast.rdk.Category

class ExecuteMethodResult {
    
    /**
     * ExecutionResult object 
     */
    ExecutionResult executionResult
    
    /**
     * Test function name
     */
    String functionName
    
    /**
     * Expected result of the script execution
     */
    String expectedResult
    
    /**
     * Actual result after the script execution
     */
    String actualResult
    
    /**
     * Status of the string
     */
    String status
	Category category = Category.RDKV
   
       
    static constraints = {  
        executionResult(nullable:false)
        expectedResult(nullable:true, blank:true)
        actualResult(nullable:true, blank:true)    
        status(nullable:true, blank:true)
        functionName(nullable:true, blank:true)
		category(nullable:false, blank:false)
    }
    
    static mapping = {
        cache true
        sort id : "desc"
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
    }
    
}
