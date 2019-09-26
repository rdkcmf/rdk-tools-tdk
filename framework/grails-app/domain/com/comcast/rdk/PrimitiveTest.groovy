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
 * Represents a PrimitiveTest
 * @author ajith
 *
 */

class PrimitiveTest {
    
    /**
     * Name of the Test.
     */
    String name
    
    /**
     * Name of the Module.
     */
    Module module
    
    /**
     * Name of the function.
     */
    Function function
    
    /**
     * Parameters list
     */
    Set<Parameter> parameters
    
	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
    /**
     * Can have many parameters.
     */
    static hasMany = [parameters:Parameter]

    /**
     * Constraints.
     * Ensures that the function parent module and module selected are same.
     * Ensures that the parameter parent is a valid function.
     */
    static constraints = {

        name (nullable:false, blank:false, unique:true)

        module(nullable: false, blank: false)
		groups(nullable:true, blank:true)
        function(nullable:false, validator:{ val, obj ->
            boolean isValid = (val.module == obj.module)
            return isValid
        })

        parameters(nullable:true, blank:true
                , validator: {val, obj ->
                    boolean isValid = false
                    if(val) {
                        for ( Parameter param : val ) {
                            isValid = (param.parameterType.function == obj.function)
                            if(!isValid) {
                                break;
                            }
                        }
                        return isValid
                    }
                    else {
                        return true
                    }
                })
    }
	
	@Override
	String toString() {
		return name ?: ''
	}
	static mapping = {
		datasource 'ALL'
	}
    
}
