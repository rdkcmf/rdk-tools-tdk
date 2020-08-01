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

<%@ page import="com.comcast.rdk.Execution" %>
	<g:if test="${executionInstanceList}">
		<div id="list-executor" class="content scaffold-list" role="main">		
			<div id="historytable" style="width:99%; overflow: auto;">		
			<table style="table-layout: auto; overflow: scroll;">
				<thead>
					<tr>
						<th colspan="7" align="center" style="width:50%;" ><h1>Execution History</h1></th>
					</tr>
					<tr>
						<g:sortableColumn style="width:2%;" property="markAll" title="${message(code: 'execution.result.label', default: '        ')}" />
						
						<g:sortableColumn style="width:20%;" property="name" title="${message(code: 'execution.name.label', default: 'Execution Name')}" params="[category:category]"/>
						
						<th width="30%" style="max-width: 330px;text-align: center;">Script/ScriptGroup</th>
						
						<g:sortableColumn style="width:14%;" property="device" title="${message(code: 'execution.device.label', default: 'Device')}" params="[category:category]"/>
					
						<g:sortableColumn style="width:14%;" property="dateOfExecution" title="${message(code: 'execution.dateOfExecution.label', default: 'Date Of Execution')}" params="[category:category]"/>
					
						<g:sortableColumn style="width:8%;" property="result" title="${message(code: 'execution.result.label', default: 'Result')}" params="[category:category]"/>
					
						<g:sortableColumn style="width:12%;" property="export" title="${message(code: 'execution.result.label', default: 'Reports')}" />
					</tr>
				</thead>
				<tbody>
				<g:each in="${executionInstanceList}" status="i" var="executionInstance">
				
					<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
					
						<td align="left" width="2%">
						<g:if test="${executionInstance.isMarked == 1 }">
							 <g:checkBox name="deleteExecutionCheckbox" id="${executionInstance?.id}" class="resultCheckbox" onClick="mark(this);" checked="true"/>
						</g:if>
						<g:else>
							<g:checkBox name="deleteExecutionCheckbox" id="${executionInstance?.id}" class="resultCheckbox" onClick="mark(this);" />
						</g:else>
						 </td>
						<td align="center" width="20%"> <g:link controller = "trends" action ="analyze" params="[name: executionInstance?.name]" target="_blank" title="Analyze execution" > ${executionInstance?.name}</g:link> </td>
							 <g:if test="${executionInstance?.script}">
								 <g:set var="titlevar" value="${fieldValue(bean: executionInstance, field: "script")}"/>
								
							</g:if>
							<g:else>
								 <g:set var="titlevar" value="${fieldValue(bean: executionInstance, field: "scriptGroup")}"/>
							</g:else>	
							
						<td align="center" width="30%" style="max-width: 330px;overflow: hidden;"title="${titlevar}" >
							<g:if test="${executionInstance?.script}">
								 <%
						 String scriptName = executionInstance?.script;
						 if(scriptName.length() > 35){
							 scriptName = scriptName?.substring(0, 32) + "...";
						 }
						  %>
								${scriptName}
							</g:if>
							<g:else>
								${fieldValue(bean: executionInstance, field: "scriptGroup")}
							</g:else>	
							
							<g:if test=	"${executionInstance?.isBenchMarkEnabled || executionInstance?.isSystemDiagnosticsEnabled }">
								(p)
							</g:if>													
						</td>
						<td align="center" width="14%">${fieldValue(bean: executionInstance, field: "device")}</td>
						<td align="center" nowrap width="14%">${fieldValue(bean: executionInstance, field: "dateOfExecution")}</td>
						<td align="center" width="10%"><g:link onclick="showExecutionLog(${executionInstance.id}); return false;" id="${executionInstance.id}" title="Execution details">
							<g:if test="${(executionInstance.executionStatus)}"> 
							
							<g:if test="${fieldValue(bean: executionInstance, field: 'executionStatus').equals('COMPLETED')}"> 
								${fieldValue(bean: executionInstance, field: "result")}
							</g:if>
							<g:else>
								${fieldValue(bean: executionInstance, field: "executionStatus")}
							</g:else>
							</g:if>	
							<g:else>
								${fieldValue(bean: executionInstance, field: "result")}
							</g:else>				
						</g:link>
						</td>
					
						<td width="10%">
						 <g:if test="${(executionInstance.executionStatus)}"> 
							
							<g:if test="${fieldValue(bean: executionInstance, field: 'executionStatus').equals('IN-PROGRESS') || fieldValue(bean: executionInstance, field: 'executionStatus').equals('PAUSED')}"> 
								<g:if test="${executionInstance?.scriptGroup}">
									<img src="../images/execution_stop.png" onclick="stopExecution(${executionInstance.id})" id="${executionInstance.id}" />
								</g:if>
								<g:elseif test="${executionInstance?.script }">
						 			<%
									 String scriptName = executionInstance?.script.toString();
								     String scriptGroupName = executionInstance?.scriptGroup.toString();
									 String multiple = "FALSE"
									 if((scriptName.toString().equals("Multiple Scripts")) || (scriptGroupName.toString().equals("Multiple Scriptgroups"))){
										multiple = "TRUE" 							
						 			}
						  			%>
									<g:if test ="${multiple == "TRUE" }">
								   		 <img src="../images/execution_stop.png" onclick="stopExecution(${executionInstance.id})" id="${executionInstance.id}" />
									</g:if>
						          </g:elseif>
							</g:if>
								<g:link onclick="executionStatus(${executionInstance.id}); return false;" id="${executionInstance.id}" > <img src="../images/execution_status.png" style="padding-left: 3px"/></g:link>
							</g:if> 
						<g:link action="exportConsolidatedToExcel" id="${executionInstance.id}" ><img src="../images/excel.png" style="padding-left: 3px" /></g:link>
						<g:link action="exportConsolidatedToZip" id="${executionInstance.id}_zip" ><img src="../images/folder-zip.png"  title = " Download Consolidated Report(zip)" style="padding-left: 3px"/></g:link>
						</td>
					</tr>
				</g:each>
				</tbody>
			</table>
			</div>
			
			<div class="pagination" style="width: 99%;">
					<a href="#" onclick="showCleanUpPopUp();"><label> <b>Date based CleanUp </b></label></a>
					<a href="#" onclick="showCombinedExcelPopUp();"><img src="../images/excel.png"  title = " Download Combined Report(Excel)" style="padding-left: 3px"/></a>
					<input type="checkbox" name="markAll" id="markAll2" class="markAll" onclick="clickCheckbox(this)">
					<label> <b>Mark All </b></label>	
					<img src="../images/trash.png" onclick="deleteResults();return false;" style="cursor: pointer;" alt="Delete" />
					<g:paginate total="${executorInstanceTotal}" params="[category:category]"/>
			</div>
			
			</div>
			<g:hiddenField name="pageOffset" id="pageOffset" value="${params.offset}"/>
		
	</g:if>
