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
 * Domain class for grouping the devices 
 * @author sreejasuma
 *
 */

class DeviceGroup
{
      
    /**
     * Name of the Group.     
     */
    String name
    
   /**
    * Set of Devices to the user
    */    
    Set devices
    
    /**
     * Status of the devicegroup
     * Whether the script is executed on the selected devicegroup
     */
    Status status
    
	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
	
	/**
	 * Category RDK-V or RDK-B
	 */
	Category category = Category.RDKV
	
    /**
     * DeviceGroup can have many devices.
     */
    static hasMany = [ devices: Device ]
    
    static constraints = {
        name(nullable:false, blank:false, unique:true)      
        status(nullable:true, blank:true)      
		groups(nullable:true, blank:true)
		category(nullable:false, blank:false)
    }
   
    static mapping = {
        cache true
        sort id : "asc"        
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
    }

   
  
    @Override
    String toString() {
        return name ?: 'NULL'
    }
    
}
