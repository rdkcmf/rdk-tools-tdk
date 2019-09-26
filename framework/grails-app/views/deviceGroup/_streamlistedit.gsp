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
<%@ page import="com.comcast.rdk.RadioStreamingDetails" %>
	<g:if  test="${deviceStreams?.size() > 0 }" >
	
	<div>
		<table>		
			<thead>
				<tr>
				<td colspan="5" align="right" style="color: brown;">Duplicate Ocap Id's are not allowed </td>
				</tr>
				<tr>
				
					<th>Stream Id</th>
																					
					<th>Channel Type</th>
				
					<th>Audio Format</th>
					
					<th>Video Format</th>
										
					<th>Ocap Id</th>
				
				</tr>
			</thead>
			<tbody>
			<g:each in="${deviceStreams}" status="i" var="deviceStream">
				<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
				
					<td align="center">${deviceStream?.stream?.streamId}</td>										
				
					<td align="center">${deviceStream?.stream?.channelType}</td>
				
					<td align="center">${deviceStream?.stream?.audioFormat}</td>
					
					<td align="center">${deviceStream?.stream?.videoFormat}</td>
					
					<td align="center"><g:hiddenField name="streamid" value="${deviceStream?.stream?.streamId}" />
					
					<g:textField name="ocapId"  style="width:55px;" required="" value="${deviceStream?.ocapId}"/></td>
				</tr>
			</g:each>
			<g:if test="${showBlankRadio}">
			<g:each in="${blankList}" status="i" var="streamingDetailsInstance">
			<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
				
					<td align="center">${fieldValue(bean: streamingDetailsInstance, field: "streamId")}</td>										
				
					<td align="center">Radio</td>
					
					<td align="center">N/A</td>
					
					<td align="center">N/A</td>
				
					<td align="center"><g:hiddenField name="streamid" value="${streamingDetailsInstance.streamId}" />
					
						<g:textField name="ocapId"  style="width:55px;" required="" value=""/></td>
				</tr>
			</g:each>
			</g:if>
			<g:else>
			<g:each in="${radiodeviceStreams}" status="i" var="streamingDetailsInstance">
				<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
				
					<td align="center">${fieldValue(bean: streamingDetailsInstance, field: "stream.streamId")}</td>										
				
					<td align="center">Radio</td>
					
					<td align="center">N/A</td>
					
					<td align="center">N/A</td>
				
					<td align="center"><g:hiddenField name="streamid" value="${streamingDetailsInstance.stream.streamId}" />
					
						<g:textField name="ocapId"  style="width:55px;" required="" value="${streamingDetailsInstance?.ocapId}"/></td>
				</tr>
			</g:each>
			</g:else>
			</tbody>
		</table>
		
	</div>
	</g:if>
