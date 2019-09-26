<!--
 If not stated otherwise in this file or this component's Licenses.txt file the
 following copyright and licenses apply:

 Copyright 2016 RDK Management

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->
<%@ page import="com.comcast.rdk.StreamingDetails" %>
 <script type="text/javascript">
	        $(document).ready(function(){	
	        	$("#locktable").dataTable( {
					"sPaginationType": "full_numbers"
				} );		        	
			});	   
</script>
<div id="list-streamingDetails" class="content scaffold-list" role="main">
	<g:set var="entityName" value="${message(code: 'streamingDetails.label', default: 'StreamingDetails')}" />

	<h1><g:message code="default.list.label" args="[entityName]" /></h1>
	
	<table  id="locktable" class="display">
		<thead>			
           <tr>
                   <th>StreamId</th>                             
                   <th>ChannelType</th>
                   <th>AudioFormat</th>
                   <th>VideoFormat</th>
           </tr>              
		</thead>
		<tbody>
		<g:each in="${streamingDetailsInstanceList}" status="i" var="streamingDetailsInstance">
			<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
			
				<td class="center">${fieldValue(bean: streamingDetailsInstance, field: "streamId")}</td>							
			
				<td class="center">${fieldValue(bean: streamingDetailsInstance, field: "channelType")}</td>
			
				<td class="center">${fieldValue(bean: streamingDetailsInstance, field: "audioFormat")}</td>
				
				<td class="center">${fieldValue(bean: streamingDetailsInstance, field: "videoFormat")}</td>
			
			</tr>
		</g:each>
		<g:each in="${radioStreamingDetails}" status="i" var="radioStreamingInstance">
			<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
			
				<td class="center">${fieldValue(bean: radioStreamingInstance, field: "streamId")}</td>							
			
				<td class="center">Radio</td>
			
				<td class="center">N/A</td>
				
				<td class="center">N/A</td>
			
			</tr>
		</g:each>
		</tbody>
	</table>
	
</div>

