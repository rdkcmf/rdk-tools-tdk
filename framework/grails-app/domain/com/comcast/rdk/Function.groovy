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
 * Indicates a function inside a Module.
 * @author ajith
 */

class Function {
    
    /**
     * Name of the Function.
     */
    String name
    
    /**
     * Parent Module.
     */
    Module module
	
	Category category = Category.RDKV

    static constraints =  {
        module(nullable:false)
		category(nullable:false, blank:false)
		name(nullable:false, blank:false, unique:'category')
    }
    /**
     * Generated HashCode and Equals
     */
    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ( ( module == null ) ? 0 : module.hashCode() );
        result = prime * result + ( ( name == null ) ? 0 : name.hashCode() );
        return result;
    }

    @Override
    public boolean equals( Object obj ) {
        if ( obj == null )
            return false;
        if ( getClass() != obj.getClass() )
            return false;
        Function other = ( Function ) obj;
        if ( module == null ) {
            if ( other.module != null )
                return false;
        }
        else if ( !module.equals( other.module ) )
            return false;
        if ( name == null ) {
            if ( other.name != null )
                return false;
        }
        else if ( !name.equals( other.name ) )
            return false;
		if ( category == null ) {
			if ( other.category != null )
				return false;
		}
		else if (category != other.category)
			return false;
        return true;
    }

    @Override
    String toString() {
        return name ?: 'NULL'
    }
	
	static mapping = {
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
	}
}
