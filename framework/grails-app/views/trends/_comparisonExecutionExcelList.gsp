<!--
 If not stated otherwise in this file or this component's Licenses.txt file the
 following copyright and licenses apply:

 Copyright 2020 RDK Management

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
<%@ page import="com.comcast.rdk.Execution"%>
<g:if test="${validate != "false" }">
	<g:if test="${checker == 1 }">
		<div id="messageDiv" class="message" role="status">${messageDiv}
		</div>
	</g:if>
	<g:else>
		<g:if test="${executionInstanceList}">
			<div id="comparisonlist" class="content scaffold-list" role="main">
				<table style="table-layout: fixed;">
					<thead>
						<tr style="background: #dfdfdf;font-weight: bold;">
							<th style="width: 5%;"></th>
							<th style="width: 35%;">Execution Name</th>
							<th style="width: 25%;">Script/ScriptGroup</th>
							<th>Device</th>
							<th>DateOfExecution</th>
							<th>Result</th>
						</tr>
					</thead>
					<tbody>
						<g:each in="${executionInstanceList}" status="i"
							var="executionInstance">
							<tr class="${(i % 2) == 0 ? 'evenForCombined' : 'oddForCombined'}">
								<td style="width: 5%;">
									<g:checkBox name="comparisonExecutionsCheckbox" id="comparisonExecutionsCheckbox_${executionInstance?.id}" />
								</td>
								<td align="center"
									style="width: 35%; overflow: hidden; word-wrap: break-word;">
									${fieldValue(bean: executionInstance, field: "name")}
								</td>
								<g:if test="${executionInstance?.script}">
									<g:set var="titlevar"
										value="${fieldValue(bean: executionInstance, field: "script")}" />
								</g:if>
								<g:else>
									<g:set var="titlevar"
										value="${fieldValue(bean: executionInstance, field: "scriptGroup")}" />
								</g:else>
								<td align="center" style="width: 25%; word-wrap: break-word;"
									title="${ titlevar}"><g:if
										test="${executionInstance?.script}">
										<%
									 String scriptName = executionInstance?.script;
									 if(scriptName.length() > 35){
										 scriptName = scriptName?.substring(0, 32) + "...";
									 }
									 %>
										${scriptName}
									</g:if> <g:else>
										${fieldValue(bean: executionInstance, field: "scriptGroup")}
									</g:else> <g:if
										test="${executionInstance?.isBenchMarkEnabled || executionInstance?.isSystemDiagnosticsEnabled }">
									(p)
								</g:if></td>
								<td align="center" style="width: 20%; word-wrap: break-word;">
									${fieldValue(bean: executionInstance, field: "device")}
								</td>
								<td align="center" nowrap>
									${fieldValue(bean: executionInstance, field: "dateOfExecution")}
								</td>
								<td align="center">
									${fieldValue(bean: executionInstance, field: "result")}
								</td>
							</tr>
						</g:each>
					</tbody>
				</table>
			</div>
			<div id="confirmComparisonButton">
				<input type="button" class=" buttons" value="Confirm Comparison Executions" onclick="comparisonExecutionSelection('${executionIdList}');"/> <br>		
			</div>
		</g:if>
		<g:else>
			<div class="message" role="status">No Records Found
			</div>
		</g:else>
	</g:else>
</g:if>