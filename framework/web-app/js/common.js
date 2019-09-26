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

/**
 * Function to highlight selected tree node.
 * @param componentId
 * @param currentId
 * @param treeElementCount
 */
function highlightTreeElement(componentId, currentId, treeElementCount){
	
	for ( var i = 1; i <= treeElementCount; i++) {
		
		$('#'+componentId+i).css('background-color','')
	}
    $('#'+componentId+currentId).css('background-color','#FAE2D2')
    
    if(componentId == "deviceExecutionList_"){
			updateSelectedDeviceId(currentId);
	}
}

/**
 * Function to cache previously selected device id.
 * This is needed for tree element highlight during device refresh.
 * @param selectedId
 */
function updateSelectedDeviceId(selectedId){
	
	$("#selectedDevice").val(selectedId);
}
