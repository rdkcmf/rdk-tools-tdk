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
 * Class for storing SocVendors.
 * @author sreejasuma
 */

class SoCVendor {

    /**
     * Name of the SoCVendor
     */
    String name

	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
	/**
	 * Indicates the group name which the device belongs
	 */
	Category category = Category.RDKV
	
    static constraints = {
       // name(unique:true, blank:false, nullable:false)
		groups(nullable:true, blank:true)
		category(nullable:false, blank:false)
		name(blank:false, nullable:false,unique:['category'])
    }


    @Override
    public String toString() {
        return name ?: 'NULL'
    }

    @Override
	public int hashCode() {
		int result = 1;
		final int primeNumber = 13;
		int internalHash = ( ( name == null ) ? 0 : name.hashCode() )
		result = primeNumber * result + internalHash;
		return result;
	}

    @Override
	public boolean equals( Object obj ) {
		boolean equals = true
		if ( this == obj ){
			equals = true;
		}else if ( obj == null ){
			equals = false;
		}else if ( getClass() != obj.getClass() ){
			equals = false;
		}else{
			SoCVendor other = ( SoCVendor ) obj;
			if ( name == null ) {
				if ( other.name != null ){
					equals =  false;
				}
			} else if ( !name.equals( other.name ) ){
				equals =  false;
			} else if(category == null){
				if(other.category != null){
					equals =  false
				}
			}else if(category != other.category){
				equals =  false
			}
		}
		return equals;
	}
	
	static mapping = {
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
	}
}
