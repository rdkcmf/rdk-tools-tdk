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
<%@ page import="java.io.*"%>
<%@ page import="com.comcast.rdk.ExecutionResult"%>
<%@ page import="com.comcast.rdk.Performance"%>
<%@ page import="com.comcast.rdk.DeviceDetails"%>
<%@ page import="com.comcast.rdk.Device"%>

<script type='text/javascript'>
function viewOnClick(me,k,i)
{ 
  if(document.getElementById('allmessages'+k+'_'+i).style.display == 'none') {
    document.getElementById('allmessages'+k+'_'+i).style.display = '';
    document.getElementById('alllogs'+k+'_'+i).style.display = '';
    $('#expander'+k+'_'+i).text('Hide');  
  }
  else {
    document.getElementById('allmessages'+k+'_'+i).style.display = 'none';
    document.getElementById('alllogs'+k+'_'+i).style.display = 'none';
    $('#expander'+k+'_'+i).text('Details');    
  }
  return false;
}

function viewOnClickperf(me,k,i)
{ 
  if(document.getElementById('allmessagesperf'+k+'_'+i).style.display == 'none') {
    document.getElementById('allmessagesperf'+k+'_'+i).style.display = '';
    $('#expanderperf'+k+'_'+i).text('Hide');  
  }
  else {
    document.getElementById('allmessagesperf'+k+'_'+i).style.display = 'none';
    $('#expanderperf'+k+'_'+i).text('Show');    
  }
  return false;
}

$(function() {
	$('#longtext').more({length: 100});
});

function showHideLink(k,i){
	$('#hidelink'+k+'_'+i).show();
	$('#showlink'+k+'_'+i).hide();
	$('#testSucc'+k+'_'+i).show();
}

function hideLogs(k,i){
	$('#showlink'+k+'_'+i).show();
	$('#testSucc'+k+'_'+i).hide();
	$('#hidelink'+k+'_'+i).hide();
}


function showCrashHideLink(k,i){
	$('#hidecrashlink'+k+'_'+i).show();
	$('#showcrashlink'+k+'_'+i).hide();
	$('#testCrashSucc'+k+'_'+i).show();
}

function hideCrashLogs(k,i){
	$('#showcrashlink'+k+'_'+i).show();
	$('#testCrashSucc'+k+'_'+i).hide();
	$('#hidecrashlink'+k+'_'+i).hide();
}


function showConsoleHideLink(k,i){
	$('#hideconsolelink'+k+'_'+i).show();
	$('#consoleLog'+k+'_'+i).show();
	$('#showconsolelink'+k+'_'+i).hide();
}

function hideConsoleLogs(k,i){
	$('#showconsolelink'+k+'_'+i).show();
	$('#consoleLog'+k+'_'+i).hide();
	$('#hideconsolelink'+k+'_'+i).hide();
}


function showParameters(k){
	$('#divDD'+k).show();
	$('#hideDevParam'+k).show();
	$('#showDevParam'+k).hide();
}

function hideParameters(k){
	$('#divDD'+k).hide();
	$('#hideDevParam'+k).hide();
	$('#showDevParam'+k).show();
}

function showFulltextDeviceDetails(k){
	$("#fulltext"+k).show();
	$("#firstfourlines"+k).hide();
	$("#showlessdd"+k).show();	
}

function showMintextDeviceDetails(k){
	$("#fulltext"+k).hide();
	$("#firstfourlines"+k).show();
	$("#showlessdd"+k).hide();	
}

</script>


<g:if test="${executionDeviceInstanceList?.size() > 0}">

<g:each in="${executionDeviceInstanceList}" status="k"  var="executionDeviceInstance">
<span id="boxtype" hidden="true" ></span>
<span id="resultCounts" hidden="true" ></span>
<span id="scriptname" hidden="true" ></span>

<table id="logtable" >
	<tr>
		<th colspan="2">Execution Details</th>	
	</tr>
	<tr>
		<td colspan="2"> 
			<g:link controller="execution"  action="exportConsolidatedToExcel" id="${executionInstance.id}" style="float:right"> Download report<img src="../images/excel.png"  title = "Download Consolidated Report(Excel)" style="padding-left: 3px"/>
			</g:link>
		</td>
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
			    def filePath = "${request.getRealPath('/')}//logs//version//${executionInstance.id}//${executionDeviceInstance?.id.toString()}//${executionDeviceInstance.id}_version.txt"	
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
		<th width="50%"> 
		<span style="display:flex;justify-content:left;">Test Group : 
		 <g:if test="${executionInstance?.script}">
		 	<g:if test="${executionInstance?.script?.toString()?.equals("Multiple Scripts")}">
		 	<g:link controller="scriptGroup" action="downloadMultiScriptXml" name = "${executionInstance?.name}" id="${executionInstance?.name}" target="_blank" >MultipleScripts </g:link>	
		 	</g:if>
			 <g:else>${testGroup}
			 </g:else>		 
		  </g:if>
		  <g:else>
		  <g:link controller="scriptGroup" action="downloadTestSuiteXml" name="${executionInstance?.scriptGroup}" id="${executionInstance?.scriptGroup}" target="_blank" >${executionInstance?.scriptGroup} </g:link>	
		  </g:else>
		 </span>
		  </th>
		  <th width="50%">
		  <span style="display:flex;justify-content:left;">
		  Result : 
		  <g:if test="${ !(executionInstance.result) }" >FAILURE </g:if>
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
			</span>	
		</th>			
	</tr>	
	<tr class="even">
		
		<td colspan="2">
			<table style="font: normal;font-size: 12px">
			<g:if test="${tDataMap?.size() > 0}">
			<tr class="even">
						<td class="tdhead" width="20%" style="white-space:nowrap;text-align: left;background-color: #b0beb3;">Module Name</td>
						<td class="tdhead" style="white-space:nowrap;text-align: left;background-color: #b0beb3; width:5%">Executed</td>
						<td class="tdhead" style="white-space:nowrap;text-align: left;background-color: #b0beb3;width:5%">SUCCESS</td>
						<td class="tdhead" style="white-space:nowrap;text-align: left;width:5%;background-color: #b0beb3;">FAILURE</td>
						<td class="tdhead" style="text-align: left;background-color: #b0beb3;width:5%">SCRIPT TIME OUT</td>
						<td class="tdhead" style="white-space:nowrap;text-align: left;background-color: #b0beb3;width:5%">N/A</td>
						<td class="tdhead" style="white-space:nowrap;text-align: left;background-color: #b0beb3;width:5%">SKIPPED</td>
						<td class="tdhead" style="text-align: left;background-color: #b0beb3;width:5%">SCRIPT ISSUE</td>
						<td class="tdhead" style="white-space:nowrap;text-align: left;background-color: #b0beb3;width:5%">NEW ISSUE</td>
						<td class="tdhead" style="text-align: left;background-color: #b0beb3;width:5%">ENV ISSUE</td>
						<td class="tdhead" style="text-align: left;background-color: #b0beb3;width:5%">INTERFACE CHANGE</td>
						<td class="tdhead" style="white-space:nowrap;text-align: left;background-color: #b0beb3;width:5%">RDK ISSUE</td>
						<td class="tdhead" style="white-space:nowrap;text-align: left;background-color: #b0beb3;width:5%">Analysis %</td>
						<td class="tdhead" style="white-space:nowrap;text-align: left;background-color: #b0beb3;width:5%">PASS %</td>
				</tr>
			<g:each in="${detailDataMap?.keySet()}" status="i"  var="moduleName">						
					<% def mapp =  detailDataMap?.get(moduleName)
					%>
				  <tr class="${i % 2 == 0 ? 'even' : 'odd'}">
						<td class="tdhead" style="white-space:nowrap;text-align: left;">${moduleName}</td>
						<td style="white-space:nowrap;text-align: right;">
						<g:if test="${mapp?.get("Executed") != null}">
							${mapp?.get("Executed")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;">
						<g:if test="${mapp?.get("SUCCESS") != null}">
							${mapp?.get("SUCCESS")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;">
						<g:if test="${mapp?.get("FAILURE") != null}">
							${mapp?.get("FAILURE")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;">
						<g:if test="${mapp?.get("SCRIPT TIME OUT") != null}">
							${mapp?.get("SCRIPT TIME OUT")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;">
						<g:if test="${mapp?.get("N/A") != null}">
							${mapp?.get("N/A")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;">
						<g:if test="${mapp?.get("SKIPPED") != null}">
							${mapp?.get("SKIPPED")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;">
						<g:if test="${mapp?.get("Script Issue") != null}">
							${mapp?.get("Script Issue")}
						</g:if>
						<g:else>
							0
						</g:else>
						<td style="white-space:nowrap;text-align: right;">
							<g:if test="${mapp?.get("New Issue") != null}">
								${mapp?.get("New Issue")}
							</g:if>
							<g:else>
								0
							</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;">
							<g:if test="${mapp?.get("Environment Issue") != null}">
								${mapp?.get("Environment Issue")}
							</g:if>
							<g:else>
								0
							</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;">
							<g:if test="${mapp?.get("Interface Change") != null}">
								${mapp?.get("Interface Change")}
							</g:if>
							<g:else>
								0
							</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;">
							<g:if test="${mapp?.get("RDK Issue") != null}">
								${mapp?.get("RDK Issue")}
							</g:if>
							<g:else>
								0
							</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;">
							<g:if test="${mapp?.get("analyzed") != null}">
								${mapp?.get("analyzed")}
							</g:if>
							<g:else>
								0
							</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;">
							<g:if test="${mapp?.get("PassRate") != null}">
								${mapp?.get("PassRate")}
							</g:if>
							<g:else>
								0
							</g:else>
						</td>
				</tr>
			</g:each>
			<tr class="even">
						<td class="tdhead" style="white-space:nowrap;text-align: left;font-weight: bold;background-color: #C4C3C7;">Total</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
						<g:if test="${tDataMap?.get("Executed") != null}">
							${tDataMap?.get("Executed")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
						<g:if test="${tDataMap?.get("SUCCESS") != null}">
							${tDataMap?.get("SUCCESS")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
						<g:if test="${tDataMap?.get("FAILURE") != null}">
							${tDataMap?.get("FAILURE")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
						<g:if test="${tDataMap?.get("SCRIPT TIME OUT") != null}">
							${tDataMap?.get("SCRIPT TIME OUT")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
						<g:if test="${tDataMap?.get("N/A") != null}">
							${tDataMap?.get("N/A")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
						<g:if test="${tDataMap?.get("SKIPPED") != null}">
							${tDataMap?.get("SKIPPED")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
						<g:if test="${tDataMap?.get("Script Issue") != null}">
							${tDataMap?.get("Script Issue")}
						</g:if>
						<g:else>
							0
						</g:else>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
							<g:if test="${tDataMap?.get("New Issue") != null}">
								${tDataMap?.get("New Issue")}
							</g:if>
							<g:else>
								0
							</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
							<g:if test="${tDataMap?.get("Environment Issue") != null}">
								${tDataMap?.get("Environment Issue")}
							</g:if>
							<g:else>
								0
							</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
							<g:if test="${tDataMap?.get("Interface Change") != null}">
								${tDataMap?.get("Interface Change")}
							</g:if>
							<g:else>
								0
							</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
							<g:if test="${tDataMap?.get("RDK Issue") != null}">
								${tDataMap?.get("RDK Issue")}
							</g:if>
							<g:else>
								0
							</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
							<g:if test="${tDataMap?.get("analyzed") != null}">
								${tDataMap?.get("analyzed")}
							</g:if>
							<g:else>
								0
							</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
						<g:if test="${tDataMap?.get("PassRate") != null}">
							${tDataMap?.get("PassRate")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
				</tr>
			</g:if>
			</table>	
		</td>
	</tr>
	
	<%
	 def deviceName = executionInstance.device
	 def deviceInstance =  Device.findByStbName(deviceName.toString())
	 String deviceStatus = deviceInstance?.deviceStatus
	 %>	
	 	<%-- For Test Suite / Multiple scripts execution completed then shows the rerun on failure and repeat execution option  --%>

</table>

	<table id="logtable">
			<tr>
				<th colspan="3">Analysis Details</th>
			</tr>
			<tr class="even">
				<td class="tdhead"
					style="white-space: nowrap; text-align: left; min-width: 34%; max-width: 10%; background-color: #b0beb3;">TOTAL
					FAILURE</td>
				<td class="tdhead"
					style="white-space: nowrap; text-align: left; min-width: 33%; max-width: 10%; background-color: #b0beb3;">ANALYZED</td>
				<td class="tdhead"
					style="white-space: nowrap; text-align: left; min-width: 13%; max-width: 10%; background-color: #b0beb3;">NOT
					ANALYZED</td>
			</tr>
			<tr>
				<g:if test="${(tDataMap?.get("FAILURE") != null && tDataMap?.get("SCRIPT TIME OUT") != null)}">
					<td>${tDataMap?.get("FAILURE") + tDataMap?.get("SCRIPT TIME OUT")}</td>
				</g:if>
				<g:elseif test="${tDataMap?.get("FAILURE") != null && tDataMap?.get("SCRIPT TIME OUT") == null}">
					<td>${tDataMap?.get("FAILURE")}</td>
				</g:elseif>
				<g:elseif test="${tDataMap?.get("FAILURE") == null && tDataMap?.get("SCRIPT TIME OUT") != null}">
					<td>${tDataMap?.get("SCRIPT TIME OUT")}</td>
				</g:elseif>
				<g:else>
					<td>0</td>
				</g:else>
				<td>${defectData?.size()}</td>
				<g:if test="${(tDataMap?.get("FAILURE") != null && tDataMap?.get("SCRIPT TIME OUT") != null)}">
					<td>${(tDataMap?.get("FAILURE") + tDataMap?.get("SCRIPT TIME OUT"))- (defectData? defectData?.size() :0)}</td>
				</g:if>
				<g:elseif test="${tDataMap?.get("FAILURE") != null && tDataMap?.get("SCRIPT TIME OUT") == null}">
					<td>${tDataMap?.get("FAILURE")- (defectData? defectData?.size() :0)}</td>
				</g:elseif>
				<g:elseif test="${tDataMap?.get("FAILURE") == null && tDataMap?.get("SCRIPT TIME OUT") != null}">
					<td>${tDataMap?.get("SCRIPT TIME OUT")- (defectData? defectData?.size() :0)}</td>
				</g:elseif>
				<g:else>
					<td>0</td>
				</g:else>
			</tr>
	</table>
	<table id="logtable">
		<tr>
			<th colspan="6">Failure Details</th>
		</tr>
		<g:each in="${executionDeviceInstance.executionresults}" status="i"  var="executionResultInstance">
			<g:if test="${executionResultInstance?.status == 'FAILURE' || executionResultInstance?.status == 'SCRIPT TIME OUT' }">
					<tr class="scripthead">
					<td style="width:10%;font-weight: bold;">Test Script </td>
					<td style="width:50%"><g:link controller="scriptGroup" action="exportScriptData" id="${executionResultInstance?.script}" target="_blank" >${executionResultInstance?.script} </g:link> </td>					
					<td style="width:10%;font-weight: bold;">Status</td>
					<td style="width:10%;">${executionResultInstance?.status}</td>
					<g:if test="${defectData[executionResultInstance?.script]}">
						<td><g:link onclick="showResultAnalysis('${executionInstance.id}', '${executionResultInstance?.script}', '${boxType?.id}', '${executionDeviceInstance?.id}','${executionResultInstance?.id}'); return false;" id="${executionInstance.id}_analyze" style="color:green">${defectData[executionResultInstance?.script]}</g:link></td>		
						<td style="width:10%;"><g:remoteLink id="expander${k}_${i}" action="getExecutionDetails" update="allmessages${k}_${i}" onSuccess="this.innerHTML='Hide';viewOnClick(this,${k},${i}); return false;" params="[execResId : "${executionResultInstance?.id}"]" >Details</g:remoteLink>	</td>	
					</g:if>
					<g:else>
						<td><g:link onclick="showResultAnalysis('${executionInstance.id}', '${executionResultInstance?.script}', '${boxType?.id}', '${executionDeviceInstance?.id}','${executionResultInstance?.id}'); return false;" id="${executionInstance.id}_analyze">${"Analyze"}</g:link></td>		
						<td style="width:10%;"><g:remoteLink id="expander${k}_${i}" action="getExecutionDetails" update="allmessages${k}_${i}" onSuccess="this.innerHTML='Hide';viewOnClick(this,${k},${i}); return false;" params="[execResId : "${executionResultInstance?.id}"]" >Details</g:remoteLink>	</td>		
					</g:else>
				</tr>
			</g:if>
			<tbody id="allmessages${k}_${i}"  style="display: none;">
			</tbody>
			<tbody id="alllogs${k}_${i}"  style="display: none;">
				<tr>
					<td>Agent Console Log</td>	
					<td colspan="4">
						&emsp;<span id="showconsolelink${k}_${i}" >
						<g:remoteLink controller="execution" action="showAgentLogFiles" update="consoleLog${k}_${i}" onSuccess="showConsoleHideLink(${k},${i});" params="[execResId : "${executionResultInstance?.id}", execDeviceId:"${executionDeviceInstance?.id}", execId:"${executionInstance?.id}"]">Show</g:remoteLink>
						<g:link controller="execution" action="showAgentLogFiles" update="consoleLog${k}_${i}" onSuccess="showConsoleHideLink(${k},${i});" params="[execResId : "${executionResultInstance?.id}", execDeviceId:"${executionDeviceInstance?.id}", execId:"${executionInstance?.id}"]"  target="_blank"> Agent Console Log Link</g:link>						
						</span>
						<span id="hideconsolelink${k}_${i}" style="display:none;"><a style="color:#7E2217;" href="#" onclick="hideConsoleLogs(${k},${i})">Hide</a></span>
						<br>
						<div id="consoleLog${k}_${i}"></div>	
					</td>					
				</tr>
				<tr>
					<td>Log	Files</td>	
					<td colspan="4">
						&emsp;<span id="hidelink${k}_${i}" style="display:none;"><a  href="#" onclick="hideLogs(${k},${i})">Hide</a></span>
						<span id="showlink${k}_${i}">
						<g:remoteLink controller="execution" action="showLogFiles" id="1" update="testSucc${k}_${i}" onSuccess="showHideLink(${k},${i});" params="[execDeviceId:"${executionDeviceInstance?.id}", execId:"${executionInstance?.id}", execResId:"${executionResultInstance?.id}"]">Show</g:remoteLink>								
						</span>
						<br>
						<div id="testSucc${k}_${i}"></div>		
						
					</td>					
				</tr>
				<tr>
					<td>Crash Log Files</td>	
					<td colspan="4">
						&emsp;<span id="hidecrashlink${k}_${i}" style="display:none;"><a href="#" onclick="hideCrashLogs(${k},${i})">Hide</a></span>
						<span id="showcrashlink${k}_${i}">			
						<g:remoteLink controller="execution" action="showCrashLogFiles" id="1" update="testCrashSucc${k}_${i}" onSuccess="showCrashHideLink(${k},${i});" params="[execDeviceId:"${executionDeviceInstance?.id}", execId:"${executionInstance?.id}", execResId:"${executionResultInstance?.id}"]">Show</g:remoteLink>
						</span>
						<br>
						<div id="testCrashSucc${k}_${i}"></div>		
					</td>					
				</tr>
			</tbody>
		</g:each>	
	</table>		
</g:each>
</g:if>
<g:else>
<div>
${executionInstance?.outputData}
</div>
</g:else>