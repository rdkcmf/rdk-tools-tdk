/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2019 RDK Management
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

/**
 * Function to show the device template form
 */
function showTemplate(deviceTemplateInstanceId, streamingDetailsInstanceTotal, applicationUrl){
	var fetchDeviceTemplateURL = applicationUrl+'/deviceTemplate/fetchDeviceTemplate'
	$.get(fetchDeviceTemplateURL, {deviceTemplateInstanceId: deviceTemplateInstanceId}, function(data) {
		for(i=1;i<=streamingDetailsInstanceTotal;i++){
			document.getElementById("ocapIdCount_"+i).value = data[i-1]
		}
		for(i=streamingDetailsInstanceTotal+1;i<=data.length;i++){
			var j = i-streamingDetailsInstanceTotal
			document.getElementById("ocapIdCount_R0"+j).value = data[i-1]
		}
	});
}