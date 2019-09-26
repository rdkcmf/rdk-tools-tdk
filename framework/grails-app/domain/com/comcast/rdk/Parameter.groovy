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
 * Class holds the parameter type and parameter value. 
 * @author ajith
 */

class Parameter {
    
    /**
     * Type of Parameter
     */
    ParameterType parameterType
    
    /**
     * Value of Parameter.
     */
    String value
    
    /**
     * A Parameter shall belong to a PrimitiveTest.
     * TODO: This can be any test not limited to primitive.
     */
    static belongsTo = [primitiveTest: PrimitiveTest]
    /**
     * If the value is integer, its verified and confirmed if it falls in range given.
     * TODO: Range check only done for Integer.
     */
    static constraints = {
        value(nullable:false, validator:{ val, obj ->
            boolean isValid = true
            switch ( obj.parameterType.parameterTypeEnum) {
                case ParameterTypeEnum.INTEGER:
                    try{
                        Integer.valueOf( val )
                    }catch (NumberFormatException e) {
                        isValid = false
                    }
                        if(isValid) {
                            // Check for range here
                            if(obj.parameterType.rangeVal){                                     
                                String range = obj.parameterType.rangeVal
                                String[] edges = range?.split( "-" );
                                if(edges && edges.size() == 2) {
                                    isValid = ((val.toInteger() >= edges[0].toInteger())
                                            && (val.toInteger() <= edges[1].toInteger()))
                                }
                            }
                        }
                    break

                default:
                    break;
            }
            return isValid
        })

        parameterType(nullable:false)

        primitiveTest(nullable:true, blank:true)
    }
    
    @Override
    public String toString()
    {
        return parameterType ?: 'NULL'
    }
	
	static mapping = {
		datasource 'ALL'
	}
}
