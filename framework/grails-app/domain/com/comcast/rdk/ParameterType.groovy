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
 * Represents a ParameterType.
 * @author ajith
 */

class ParameterType {
    
    /**
     * Name of the Parameter
     */
    String name
    
    /**
     * Type of the parameter.
     */
    ParameterTypeEnum parameterTypeEnum
    
    /**
     * Value: To be removed from here.
     */
    String rangeVal
    
    /**
     * Parent Function to which this belong to.
     */
    Function function

    static constraints = {
        name(nullable: false, blank: false)
        parameterTypeEnum(nullable: false)
        rangeVal(nullable: false, blank: false)
        function(nullable:false)
    }
  
    
    @Override
    String toString() {
        return name ?: 'NULL'
    }
	
	static mapping = {
		datasource 'ALL'
	}
}
