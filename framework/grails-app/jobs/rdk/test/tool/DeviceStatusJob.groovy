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
package rdk.test.tool

import java.awt.RadialGradientPaintContext;

import com.comcast.rdk.*
import javax.servlet.http.HttpServletRequest
import static com.comcast.rdk.Constants.*
import org.springframework.web.context.request.RequestContextHolder
import org.codehaus.groovy.grails.validation.routines.InetAddressValidator
import org.hibernate.loader.custom.CustomLoader;

//@DisallowConcurrentExecution
class DeviceStatusJob {
	static triggers = { //simple repeatCount : -1
		simple repeatInterval: 20000l }
	def executionService
	def executescriptService
	def devicegroupService
	def deviceStatusService
	def grailsApplication
	private HttpServletRequest servletRequest;

	def concurrent = false
	
	/**
	 * Method which is invoked based on the schedule time.
	 * Synchonized thread block which will be triggered in every 30 sec(It is configurable - Currently givesn as 30 sec)
	 * It will trigger device status checking for all devices and update the same in DB.
	 * Preform Port forwading for moca devices.
	 * @param context
	 */
	synchronized def execute() {
		try{
			DeviceStatusUpdater.updateDeviceStatus(grailsApplication,deviceStatusService,executescriptService);		
		}catch(Exception e){			
			e.printStackTrace();
		}
	}

}
