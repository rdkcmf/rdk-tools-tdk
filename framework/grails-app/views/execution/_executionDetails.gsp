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
<tr>
	<td class="tdhead">TimeTaken(min)</td>
	<td colspan="4">
		${executionResultInstance?.executionTime}
	</td>
</tr>
<g:each in="${executionResultInstance.executemethodresults}"
	var="executionResultMthdsInstance">
	<tr class="fnhead">
		<td>Function Name</td>
		<td colspan="4">
			${executionResultMthdsInstance?.functionName}
		</td>
	</tr>
	<tr>
		<td>ExpectedResult</td>
		<td colspan="4">
			${executionResultMthdsInstance?.expectedResult}
		</td>
	</tr>
	<tr>
		<td>ActualResult</td>
		<td colspan="4">
			${executionResultMthdsInstance?.actualResult}
		</td>
	</tr>
	<tr>
		<td>Status</td>
		<td colspan="4">
			${executionResultMthdsInstance?.status}
		</td>
	</tr>
</g:each>
<tr>
	<td>Log Data <br> <g:link action="showExecutionResult" params="[execResult : "${executionResultInstance?.id}"]" target="_blank"> Log link </g:link>
	</td>
	<td colspan="6"><div style="overflow: auto; height: 180px;">${executionResultInstance?.executionOutput}</div></td>
</tr>