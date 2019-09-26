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

import java.io.File;

/**
 * Custom file name filter to filter the files for which name starting with the provided name.
 *
 */
class CustomFileNameFilter implements FilenameFilter{
	
	String matchingName = null;
	
	public CustomFileNameFilter(String matchingName){
		this.matchingName = matchingName;
	}

	@Override
	boolean accept(File arg0, String name) {
		if(matchingName != null){
			return name.startsWith(matchingName) ? true : false;
		}
		return false;
	}

}
