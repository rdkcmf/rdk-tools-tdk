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
<%@ page import="java.io.*"%>
<%@ page import="com.comcast.rdk.ExecutionResult"%>
<%@ page import="com.comcast.rdk.Performance"%>
<%@ page import="com.comcast.rdk.DeviceDetails"%>
<%@ page import="com.comcast.rdk.Device"%>
<head>
<script type='text/javascript'>

$(function() {
	$('#longtext').more({length: 100});
});

</script>

<style>
td {
    border: solid;
    border-width: 1;
    border-color: grey;
	padding:0;
}
</style>


<g:if test="${executionDeviceInstanceList?.size() > 0}">

<g:each in="${executionDeviceInstanceList}" status="k"  var="executionDeviceInstance">
<table id="logtable" style="background: #f0f8ff; width:80%; margin-left:10%;  border-collapse:collapse;">
	<tr>
		<th colspan="2">Execution Details</th>	
	</tr>
	
	<tr class="trborder even">
		<td class="tdhead">Device Name</td>
		<td >${executionDeviceInstance?.device}</td>				
	</tr>
	<tr class="odd">
		<td class="tdhead">IP</td>
		<td>${executionDeviceInstance?.deviceIp}</td>				
	</tr>
	<tr class="trborder even">
		<td class="tdhead">Date Of Execution</td>
		<td >${executionInstance?.dateOfExecution}</td>				
	</tr>
	<tr class="odd">
		<td class="tdhead">Time taken for script execution(min)</td>
		<%
			String time = executionInstance?.executionTime
			try{
				if(time && time?.length() > 0 && time?.contains(".")){
					int indx = ((time.indexOf(".") + 3) <= time?.length() )?  (time.indexOf(".") + 3) : (time?.length() )
					time = time.substring(0, time.indexOf(".")+3);
				}
			}catch(Exception e){
			}
		 %>
		<td>${time}</td>				
	</tr>
	
	<tr class="trborder even">
		<td class="tdhead">Device Parameters</td>
		<td>		
			<%
			   def device = Device.findByStbName(executionDeviceInstance?.device) 
			   def deviceDetailsList = DeviceDetails.findAllByDevice(device)	
			%>			
			<g:if test="${deviceDetailsList}">
						
			<span id="showDevParam${k}" ><g:link  onclick="showParameters(${k}); return false;"><b><i>Show</i></b></g:link></span>
		    <span id="hideDevParam${k}" style="display:none;"><g:link onclick="hideParameters(${k}); return false;"><b><i>Hide</i></b></g:link></span>		
						
			<div id="divDD${k}" style="display:none;width: 600px;overflow: auto;">			
				<table style="width:70%;">
					<g:each in="${deviceDetailsList}" var="deviceDetailsInstance">
						<tr>
							<td>${deviceDetailsInstance.deviceParameter}</td>
							<td>${deviceDetailsInstance.deviceValue}</td>
						</tr>
					</g:each>
				</table>			
			</div>	
			</g:if>
			<g:else>
				Not Available
			</g:else>	
		</td>				
	</tr>
	
	<tr class="trborder even">
		<td class="tdhead">Device Details</td>		
		<td>
		<%
			int c = 0
			def fileContents = ""
			def firstfourLine = ""
			try{
			    def filePath = realPathForLogs + "//logs//version//${executionInstance.id}//${executionDeviceInstance?.id.toString()}//${executionDeviceInstance.id}_version.txt"	
				BufferedReader inn = new BufferedReader(new FileReader(filePath));
				String line;
				while((line = inn.readLine()) != null)
				{				
					if(!(line.isEmpty())){
						if(!(line.startsWith( "=====" ))){
							if(c < 3 )  {
								firstfourLine =  firstfourLine + line + "<br>"
								c++
							}
							fileContents = fileContents + line + "<br>"
						}
					}
				}
		 	}catch(Exception fnf){          		
       	 	}
		 %>	
		<g:if test="${!(fileContents.isEmpty())}">
			<span id="showlessdd${k}" style="display:none;"><g:link onclick="showMintextDeviceDetails(${k}); return false;"><b><i>Show Less</i></b></g:link></span><br>
			<span id="firstfourlines${k}">${firstfourLine} &emsp; <g:link  onclick="showFulltextDeviceDetails(${k}); return false;"><b><i>Show More</i></b></g:link></span>
			<span id="fulltext${k}" style="display:none;">${fileContents}&emsp; </span>
		</g:if>		
		<g:else>
			<g:if test="${executionDeviceInstance.buildName && executionDeviceInstance.buildName != "Image name not available" }">
				<b>${executionDeviceInstance.buildName }</b>
			</g:if>
			<g:else>
				<b>Unable to fetch Device Details</b>
			</g:else>
		</g:else>
		</td>				
	</tr>
	<tr class="odd">
		<th>Test Group 
		</th>
		<th align="left">
		 <g:if test="${executionInstance?.script  || executionInstance?.scriptGroup}">
		 	<g:if test="${executionInstance?.script?.toString()?.equals("Multiple Scripts")}">
		 	<a href="${baseUrl}scriptGroup/downloadMultiScriptXml?name=${executionInstance?.name}&id=${executionInstance?.name}" target="_blank">MultipleScripts </a>
<%--		 	<g:link controller="scriptGroup" action="downloadMultiScriptXml" name = "${executionInstance?.name}" id="${executionInstance?.name}" target="_blank" >MultipleScripts </g:link>	--%>
		 	</g:if>
		 	<g:if test="${executionInstance?.scriptGroup?.toString()?.equals("Multiple Scriptgroups")}">
		 	<a href="${baseUrl}scriptGroup/downloadMultiScriptXml?name=${executionInstance?.name}&id=${executionInstance?.name}" target="_blank">Multiple Scriptgroups </a>
<%--		 	<g:link controller="scriptGroup" action="downloadMultiScriptXml" name = "${executionInstance?.name}" id="${executionInstance?.name}" target="_blank" >MultipleScripts </g:link>	--%>
		 	</g:if>
			 <g:else>${testGroup}
			 </g:else>		 
		  </g:if>
		  <g:else>
		  <a href="${baseUrl}scriptGroup/downloadTestSuiteXml?name=${executionInstance?.scriptGroup}&id=${executionInstance?.scriptGroup}" target="_blank">${executionInstance?.scriptGroup} </a></td>
<%--		  <g:link controller="scriptGroup" action="downloadTestSuiteXml" name="${executionInstance?.scriptGroup}" id="${executionInstance?.scriptGroup}" target="_blank" >${executionInstance?.scriptGroup} </g:link>	--%>
		  </g:else> &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
		  
		  Result : 
		  <g:if test="${ !(executionInstance.result) }" >FAILURE						
							</g:if>
							<g:else>
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
							</g:else>	
		</th>			
	</tr>	
	<tr class="even">
		
		<td colspan="2">
			<table style="border-collapse:collapse; width:100%">
			<g:if test="${(statusResults?.get(executionDeviceInstance))?.size() > 0}">
			<tr class="scripthead" >
					<td colspan="2" class="tdhead">Summary</td>
			</tr>
			</g:if>
			<g:each in="${statusResults.get(executionDeviceInstance)}" status="i"  var="executionStatusInstance">						
				<g:each in="${executionStatusInstance}"  var="statusItem">		
					
				  <tr class="even">
						<td class="tdhead" style="white-space:nowrap;text-align: right;width:15%; padding-right:2%" >${statusItem.key }</td>
						<td style="padding-left:2%">${statusItem.value }</td>
					</tr>
				</g:each>		   
			</g:each>
			</table>	
		</td>
	</tr>
		
	<%
	 def deviceName = executionInstance.device
	 def deviceInstance =  Device.findByStbName(deviceName.toString())
	 String deviceStatus = deviceInstance?.deviceStatus
	 %>	

	<tr class="even">	
		<%--<td class="tdhead" style="vertical-align: middle; text-align: center;">
		  <g:if test="${executionInstance?.script}">
			${testGroup}		 
		  </g:if>
		  <g:else>
		  	${executionInstance?.scriptGroup}
		  </g:else>
		</td>
		--%>
		<td colspan="2">
		<g:each in="${executionDeviceInstance.executionresults}" status="i"  var="executionResultInstance">
		
			<table  style="width:100%;border-collapse: collapse;">
				<%-- <tr class="scripthead">
					<td class="tdhead">Test Script </td>
					<td>${executionResultInstance?.script}</td>					
					<td class="tdhead">Status</td>
					<td>${executionResultInstance?.status}</td>					
				</tr> --%>
				<tr class="scripthead">
					<td style="width:10%;font-weight: bold;">Test Script </td>
					<td style="width:30%"> 
					<a href="${baseUrl}scriptGroup/exportScriptData/${executionResultInstance?.script}" target="_blank">${executionResultInstance?.script} </a></td>					
					<td style="width:10%;font-weight: bold;">Status</td>
					<td style="width:10%;">${executionResultInstance?.status}</td>		
<%-- 					<td style="width:10%;"><g:remoteLink id="expander${k}_${i}" action="getExecutionDetails" update="allmessages${k}_${i}" onSuccess="this.innerHTML='Hide';viewOnClick(this,${k},${i}); return false;" params="[execResId : "${executionResultInstance?.id}"]" >Details</g:remoteLink>	</td>		 --%>
				</tr>
			<tbody id="allmessages${k}_${i}">
			</tbody>
			<tbody id="alllogs${k}_${i}" >
			<tr>
			<td>Agent Console Log		
					
					</td>	
					<td colspan="4">
						&emsp;
						<a href="${baseUrl}execution/showAgentLogFiles?execResId=${executionResultInstance?.id}&execDeviceId=${executionDeviceInstance?.id}&execId=${executionInstance?.id}" target="_blank">Show</a>
					</td>					
				</tr>
				<tr>
					<td>Log	Files <a href="${baseUrl}execution/showExecutionResult?execResult=${executionResultInstance?.id}" target="_blank">Show</a></td>	
					<td colspan="4">
						&emsp;
                        ${executionResultInstance?.executionOutput}
					</td>
				</tr>

				<tr>
					<td>Crash Log Files</td>
					&emsp;
						
					<td colspan="4">
						<a href="${baseUrl}execution/showCrashLogFiles?execResId=${executionResultInstance?.id}&execDeviceId=${executionDeviceInstance?.id}&execId=${executionInstance?.id}" target="_blank">Show</a>
					</td>					
				</tr>
			</tbody>
			</table>
			<g:if test="${executionResultInstance.performance}">
			<table>
						<tr class="scripthead" style=" background:#DFDFDF;">
							<td colspan="4" class="tdhead">Performance</td>					
							<td>
							<a href="#" id="expanderperf${k}_${i}" onclick="this.innerHTML='Hide';viewOnClickperf(this,${k},${i}); return false;">Show</a>
						</tr>
						</table>
						<span id="allmessagesperf${k}_${i}"  style="display: none;">
						<section class="round-border">
						
						<%
							def performance = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,"BenchMark")							
						%>
						<table>
						<g:if test="${performance}">					
						<tbody >
							<tr class="fnhead">
								<td class="tdhead" colspan="2">Time Info</td>
							</tr>
							<tr class="fnhead1">												
								<td class="tdhead">API Name</td>
								<td class="tdhead">Execution Time(millisec)</td>							
							</tr>
							<g:each in="${performance}" var="performanceInstance">
								<tr>																					
									<td>${performanceInstance?.processName}</td>												
									<td>${performanceInstance?.processValue}</td>				
								</tr>					
							</g:each>						
						</tbody>
						</g:if>						
					</table>
					
						<%
							def performance1 = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,"SYSTEMDIAGNOSTICS_CPU")													
						%>
						<table>	
						<g:if test="${performance1}">		
						<tbody>							
							<tr class="fnhead">
								<td class="tdhead" colspan="2">CPU Utilization</td>														
							</tr>		
							<tr class="fnhead1">					
								<td class="tdhead">Diagnostic Type</td>
								<td class="tdhead">Value</td>									
							</tr>
							<g:each in="${performance1}"  var="performanceInstance1">
								<tr>																									
									<td>${performanceInstance1?.processName}</td>
									<td>${performanceInstance1?.processValue}</td>							
								</tr>					
							</g:each>										
						</tbody>
						</g:if>
						</table>
						<%
							def performance2 = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,"SYSTEMDIAGNOSTICS_MEMORY")													
						%>
						<table>	
						<g:if test="${performance2}">
						<tbody>							
							<tr class="fnhead">
								<td class="tdhead" colspan="4">Memory Utilization</td>														
							</tr>



												<tr class="fnhead1">
													<td class="tdhead" style="max-width: 20px"></td>
													<td class="tdhead">Free Memory (KB)</td>
													<td class="tdhead">Used Memory (KB)</td>
													<td class="tdhead">Memory Used (Perc)</td>
												</tr>

												<%
							def freeInitial = Performance.findByExecutionResultAndProcessName(executionResultInstance,"%MEMORY_AVAILABLE_START")													
						%>
												<%
							def usedInitial = Performance.findByExecutionResultAndProcessName(executionResultInstance,"%MEMORY_USED_START")													
						%>
												<%
							def memInitial = Performance.findByExecutionResultAndProcessName(executionResultInstance,"%MEMORY_PERC_START")													
						%>
												<tr>
													<td style="max-width: 20px"><b>Starting<b/></td>
													<td>
														${freeInitial?.processValue}
													</td>
									<td>${usedInitial?.processValue}</td>	
									<td>${memInitial?.processValue}</td>						
								</tr>					


	<%
							def freeEnd = Performance.findByExecutionResultAndProcessName(executionResultInstance,"%MEMORY_AVAILABLE_END")													
						%>
							<%
							def usedEnd = Performance.findByExecutionResultAndProcessName(executionResultInstance,"%MEMORY_USED_END")													
						%>
						<%
							def memEnd = Performance.findByExecutionResultAndProcessName(executionResultInstance,"%MEMORY_PERC_END")													
						%>
								<tr>				
									<td style="max-width: 20px"><b>Ending<b></b></td>
									<td>${freeEnd?.processValue}</td>
									<td>${usedEnd?.processValue}</td>	
									<td>${memEnd?.processValue}</td>						
								</tr>	
								
									<%
							def freePeak = Performance.findByExecutionResultAndProcessName(executionResultInstance,"%MEMORY_AVAILABLE_PEAK")													
						%>
							<%
							def usedPeak = Performance.findByExecutionResultAndProcessName(executionResultInstance,"%MEMORY_USED_PEAK")													
						%>
						<%
							def memPeak = Performance.findByExecutionResultAndProcessName(executionResultInstance,"%MEMORY_PERC_PEAK")													
						%>
								<tr>				
									<td style="max-width: 20px"><b>Peak</b></td>
									<td>${freePeak?.processValue}</td>
									<td>${usedPeak?.processValue}</td>	
									<td>${memPeak?.processValue}</td>						
								</tr>							</tbody>
						</g:if>
						</table>
				</section>		
				</span>		
			</g:if>
		</g:each>	
		</td>
	</tr>	
</table>	
</g:each>
</g:if>
<g:else>
<div>
${executionInstance?.outputData}
</div>
</g:else>
