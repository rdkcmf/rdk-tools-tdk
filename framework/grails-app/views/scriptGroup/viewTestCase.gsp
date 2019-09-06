<!--
 If not stated otherwise in this file or this component's Licenses.txt file the
 following copyright and licenses apply:

 Copyright 2019 RDK Management

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

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<style type="text/css">
.tableColumn {
   border:solid 1px black;
   border-collapse: collapse; 
}
</style>
</head>
<body>
	<table class="tableColumn">
		<thead style="background-color: #6699FF; color:#FFFFFF">
			<tr>
				<th class="tableColumn">Test Case ID</th>
				<th class="tableColumn">Test Objective</th>
				<th class="tableColumn">Test Type</th>
				<th class="tableColumn">Test Setup</th>
				<th class="tableColumn">API's / Interface Used</th>
				<th class="tableColumn">Input Parameters(API name: parameter type –
					value)/Interface Input</th>
				<th class="tableColumn">Pre-requisite</th>
				<th class="tableColumn">Automation Approach</th>
				<th class="tableColumn">Exp Output</th>
				<th class="tableColumn">Priority</th>
				<th class="tableColumn">Test Stub</th>
				<th class="tableColumn">Test script</th>
				<th class="tableColumn">Remarks</th>
				<th class="tableColumn">Release version</th>
			</tr>
		</thead>
		<tbody>
			<g:each in="${testCaseList}" status="i" var="testCaseInstance">
				<tr>
					<td class="tableColumn">${testCaseInstance['Test Case ID']}</td>
					<td class="tableColumn">${testCaseInstance['Test Objective']}</td>
					<td class="tableColumn">${testCaseInstance['Test Type']}</td>
					<td class="tableColumn">${testCaseInstance['Supported Box Type']}</td>
					<td class="tableColumn">${testCaseInstance['RDK Interface']}</td>
					<td class="tableColumn">${testCaseInstance['Input Parameters']}</td>
					<td class="tableColumn">${testCaseInstance['Test Prerequisites']}</td>
					<td class="tableColumn">${testCaseInstance['Automation Approach']}</td>
					<td class="tableColumn">${testCaseInstance['Expected Output']}</td>
					<td class="tableColumn">${testCaseInstance['Priority']}</td>
					<td class="tableColumn">${testCaseInstance['Test Stub Interface']}</td>
					<td class="tableColumn">${testCaseInstance['Test Script']}</td>
					<td class="tableColumn">${testCaseInstance['Remarks']}</td>
					<td class="tableColumn">${testCaseInstance['Update Release Version']}</td>
				</tr>
			</g:each>
		</tbody>
	</table>
</html>
</body>