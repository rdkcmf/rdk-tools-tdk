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

class User {
    /**
	 * Username of the User
	 */
    String username
	/**
	 * Password of the User
	 */
    String passwordHash
	/**
	 * email address of user
	 */
    String email
	/**
	 * Name of the User
	 */
    String name
	/**
	 * Status of the user 
	 */
    String status
	
	Groups groupName
    
    /**
     * User has many roles and permissions
     */
    static hasMany = [ roles: Role, permissions: String ]

    static constraints = {
        username(nullable: false, blank: false, unique: true)
        email(nullable: false, blank: false)
        name(nullable: false, blank: false)
        status(nullable: true, blank: true)   
        passwordHash(nullable: true, blank: true)
		groupName(nullable: true, blank: true)
    }
    
    @Override
    public String toString()
    {
        return username ?: 'NULL'
    }
	
	static mapping = {
		datasource 'ALL'
	}
    
}
