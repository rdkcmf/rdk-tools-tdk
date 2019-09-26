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
<g:if test="${logFileNames}">
<table>
	<g:each in="${logFileNames}" status="i"  var="fileName">				
	<tr><%  j = i + 1 %>
		<td>
		<g:form controller="execution">
		<g:link style="text-decoration:none;" action="showCrashExecutionLog" id="${execId+"_"+execDeviceId+"_"+fileName.key}" 
		 params="[execId: "${execId}", execDeviceId: "${execDeviceId}", execResultId: "${execResId}" ]" >
		<span class="customizedLink" >${j} &nbsp;:&nbsp; ${fileName.key} </span>	
		</g:link>
		</g:form>			
		</td>
	</tr>				
	</g:each>
</table>
</g:if>
