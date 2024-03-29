<!--
 If not stated otherwise in this file or this component's Licenses.txt file the
 following copyright and licenses apply:

 Copyright 2021 RDK Management

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

<script type="text/javascript">

function viewOnClickTool(me,k,i)
{ 
  if(document.getElementById('toolMetrics'+k+'_'+i).style.display == 'none') {
    document.getElementById('toolMetrics'+k+'_'+i).style.display = '';
    $('#expandertool'+k+'_'+i).text('Hide');  
  }
  else {
    document.getElementById('toolMetrics'+k+'_'+i).style.display = 'none';
    $('#expandertool'+k+'_'+i).text('Show');    
  }
  return false;
}

function viewOnClickToolSmem(me,k,i)
{ 
  if(document.getElementById('toolSmem'+k+'_'+i).style.display == 'none') {
    document.getElementById('toolSmem'+k+'_'+i).style.display = '';
    $('#expanderSmem'+k+'_'+i).text('Hide');  
  }
  else {
    document.getElementById('toolSmem'+k+'_'+i).style.display = 'none';
    $('#expanderSmem'+k+'_'+i).text('Show');    
  }
  return false;
}

function showSmemHideLink(m,k,i){
	$('#hideSmemContents'+m+'_'+k+'_'+i).show();
	$('#smemDetails'+m+'_'+k+'_'+i).show();
	$('#showSmemContents'+m+'_'+k+'_'+i).hide();
}


function hideSmemLogs(m,k,i){
	$('#showSmemContents'+m+'_'+k+'_'+i).show();
	$('#smemDetails'+m+'_'+k+'_'+i).hide();
	$('#hideSmemContents'+m+'_'+k+'_'+i).hide();
}

function viewOnClickToolPmap(me,k,i)
{ 
  if(document.getElementById('toolPmap'+k+'_'+i).style.display == 'none') {
    document.getElementById('toolPmap'+k+'_'+i).style.display = '';
    $('#expanderPmap'+k+'_'+i).text('Hide');  
  }
  else {
    document.getElementById('toolPmap'+k+'_'+i).style.display = 'none';
    $('#expanderPmap'+k+'_'+i).text('Show');    
  }
  return false;
}

function viewOnPmapClick(m,k,i)
{ 
  if(document.getElementById('pmapDetails'+m+'_'+k+'_'+i).style.display == 'none') {
    document.getElementById('pmapDetails'+m+'_'+k+'_'+i).style.display = '';
    $('#showPmapContents'+m+'_'+k+'_'+i).hide();
    $('#hidePmapContents'+m+'_'+k+'_'+i).show();
  }
  else {
    document.getElementById('pmapDetails'+m+'_'+k+'_'+i).style.display = 'none';  
    $('#showPmapContents'+m+'_'+k+'_'+i).show();
    $('#hidePmapContents'+m+'_'+k+'_'+i).hide(); 
  }
  return false;
}

function hidePmapLogs(m,k,i){
	$('#showPmapContents'+m+'_'+k+'_'+i).show();
	$('#pmapDetails'+m+'_'+k+'_'+i).hide();
	$('#hidePmapContents'+m+'_'+k+'_'+i).hide();
}

function viewOnClickToolSystemdAnalyis(me,k,i)
{ 
  if(document.getElementById('toolSystemdAnalysis'+k+'_'+i).style.display == 'none') {
    document.getElementById('toolSystemdAnalysis'+k+'_'+i).style.display = '';
    $('#expanderSystemdAnalysis'+k+'_'+i).text('Hide');  
  }
  else {
    document.getElementById('toolSystemdAnalysis'+k+'_'+i).style.display = 'none';
    $('#expanderSystemdAnalysis'+k+'_'+i).text('Show');    
  }
  return false;
}

function showSystemdAnalysisHideLink(m,k,i){
	$('#hideSystemdAnalysisContents'+m+'_'+k+'_'+i).show();
	$('#SystemdAnalysisDetails'+m+'_'+k+'_'+i).show();
	$('#showSystemdAnalysisContents'+m+'_'+k+'_'+i).hide();
}


function hideSystemdLogs(m,k,i){
	$('#showSystemdAnalysisContents'+m+'_'+k+'_'+i).show();
	$('#SystemdAnalysisDetails'+m+'_'+k+'_'+i).hide();
	$('#hideSystemdAnalysisContents'+m+'_'+k+'_'+i).hide();
}

function viewOnClickToolSystemdBootchart(me,k,i)
{ 
  if(document.getElementById('toolSystemdBootchart'+k+'_'+i).style.display == 'none') {
    document.getElementById('toolSystemdBootchart'+k+'_'+i).style.display = '';
    $('#expanderSystemdBootchart'+k+'_'+i).text('Hide');  
  }
  else {
    document.getElementById('toolSystemdBootchart'+k+'_'+i).style.display = 'none';
    $('#expanderSystemdBootchart'+k+'_'+i).text('Show');    
  }
  return false;
}

function showSystemdBootchartHideLink(m,k,i){
	$('#hideSystemdBootchartContents'+m+'_'+k+'_'+i).show();
	$('#SystemdBootchartDetails'+m+'_'+k+'_'+i).show();
	$('#showSystemdBootchartContents'+m+'_'+k+'_'+i).hide();
}


function hideSystemdBootchartLogs(m,k,i){
	$('#showSystemdBootchartContents'+m+'_'+k+'_'+i).show();
	$('#SystemdBootchartDetails'+m+'_'+k+'_'+i).hide();
	$('#hideSystemdBootchartContents'+m+'_'+k+'_'+i).hide();
}

function viewOnClickToollmbench(me,k,i)
{ 
  if(document.getElementById('toollmbench'+k+'_'+i).style.display == 'none') {
    document.getElementById('toollmbench'+k+'_'+i).style.display = '';
    $('#expanderlmbench'+k+'_'+i).text('Hide');  
  }
  else {
    document.getElementById('toollmbench'+k+'_'+i).style.display = 'none';
    $('#expanderlmbench'+k+'_'+i).text('Show');    
  }
  return false;
}

function showlmbenchHideLink(m,k,i){
	$('#hidelmbenchContents'+m+'_'+k+'_'+i).show();
	$('#lmbenchDetails'+m+'_'+k+'_'+i).show();
	$('#showlmbenchContents'+m+'_'+k+'_'+i).hide();
}


function hidelmbenchLogs(m,k,i){
	$('#showlmbenchContents'+m+'_'+k+'_'+i).show();
	$('#lmbenchDetails'+m+'_'+k+'_'+i).hide();
	$('#hidelmbenchContents'+m+'_'+k+'_'+i).hide();
}

</script>

<%
	def grafanaPerformance = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,"GrafanaData")
	def grafanautility = grafanaPerformance.performanceType[0]
	List processNameList = []
	grafanaPerformance.each{ grafana ->
		if(!processNameList?.contains(grafana.processName)){
			processNameList?.add(grafana.processName)
		}
	}
%>
<g:if test="${profilingDetails}">	
	<table>
		<tbody >
			<tr>
			<td colspan="4" >
			<g:if test="${grafanaPerformance || alertListMap}">	
				<table>
					<tr class="scripthead" style=" background:#DFDFDF;">
						<td colspan="4" class="tdhead">collectd</td>					
						<td>
							<a href="#" id="expandertool${k}_${i}" onclick="this.innerHTML='Hide';viewOnClickTool(this,${k},${i}); return false;">Show</a>
					</tr>
				</table>
			</g:if>	
			<span id="toolMetrics${k}_${i}"  style="display: none;">
				<section class="round-border">
						<g:if test="${alertListMap}">
							<table>
								<tbody >
									<tr class="fnhead1">
										<td class="tdhead" style="width:30%;">Alerts Received</td>
										<td class="tdhead"></td>
										<td class="tdhead"></td>
										<td class="tdhead"></td>
										<td class="tdhead"></td>
									</tr>
									<tr class="fnhead1">												
										<td class="tdhead" style="width:30%;">Metric</td>
										<td class="tdhead">Time</td>		
										<td class="tdhead">Threshold Value</td>		
										<td class="tdhead">Metric Value</td>
										<td class="tdhead">State</td>					
									</tr>
									<g:each in="${alertListMap?.keySet()}" status="metricStatus"  var="metricKey">					
										<%
											List alertList = alertListMap?.get(metricKey)
											int alertListLength = alertList?.size() + 1
										%>
										<g:if test="${alertList?.size() > 0}">
											<tr>																					
												<td style="width:30%;" rowspan="${alertListLength}">${metricKey}</td>
											</tr>
											<g:each in="${alertList}" var="alertInstance">
												<tr>																					
													<td>${alertInstance?.get("system_time")}</td>
													<td>${alertInstance?.get("threshold")}</td>
													<td>${alertInstance?.get("value")}</td>
													<g:if test="${alertInstance?.get("state") == "alerting"}">
														<td title="Alert with state as 'alerting' is received from Grafana
when the collectd metric value went above the threshold value">${alertInstance?.get("state")}</td>
													</g:if>
													<g:elseif test="${alertInstance?.get("state") == "ok"}">
														<td title="Alert with state as 'ok' is received from Grafana
when the collectd metric value went below the threshold value">${alertInstance?.get("state")}</td>
													</g:elseif>
													<g:elseif test="${alertInstance?.get("state") == "no_data"}">
														<td title="Alert with state as 'no_data' is received from Grafana
if no metric data is received from the device">${alertInstance?.get("state")}</td>
													</g:elseif>
												</tr>
											</g:each>	
										</g:if>	
									</g:each>
								</tbody>
							</table>
						</g:if>
					<g:if test="${grafanaPerformance}">	
						<g:each in="${processNameList}" var="processNameInstance">
							<table>
								<tbody >
									<tr class="fnhead1">
										<td class="tdhead" style="width:30%;">${processNameInstance}</td>
										<td class="tdhead"></td>
										<td class="tdhead"></td>
									</tr>
									<tr class="fnhead1">												
										<td class="tdhead" style="width:30%;">Parameter</td>
										<td class="tdhead">Threshold</td>		
										<td class="tdhead">Value</td>							
									</tr>
									<g:each in="${grafanaPerformance}" var="grafanaPerformanceInstance">
										<g:if test="${grafanaPerformanceInstance.processName == processNameInstance}">	
											<tr>																					
												<td style="width:30%;">${grafanaPerformanceInstance?.processType}</td>	
												<g:if test="${grafanaPerformanceInstance?.processValue1}">	
													<td>${grafanaPerformanceInstance?.processValue1}</td>	
												</g:if>
												<g:else>
													<td>NIL</td>	
												</g:else>				
												<td>${grafanaPerformanceInstance?.processValue}</td>	
											</tr>			
										</g:if>
									</g:each>						
								</tbody>
							</table>	
						</g:each>
					</g:if>	
				</section>		
			</span>	
			<g:if test="${smemFileMap}">	
				<table>
					<tr class="scripthead" style=" background:#DFDFDF;">
						<td colspan="4" class="tdhead">smem</td>					
						<td>
							<a href="#" id="expanderSmem${k}_${i}" onclick="this.innerHTML='Hide';viewOnClickToolSmem(this,${k},${i}); return false;">Show</a>
					</tr>
				</table>
			</g:if>	
			<span id="toolSmem${k}_${i}"  style="display: none;">
				<section class="round-border">
					<g:if test="${smemFileMap}">	
						<table>
							<tbody >
								<tr class="fnhead1">
										<td class="tdhead" style="width:5%;">File Name</td>
										<td class="tdhead" style="max-width: 450px;">Contents</td>
								</tr>
								<g:each in="${smemFileMap}" status="m"  var="map">
									<tr>
										<td style="width:5%;">
											<g:form controller="execution">
												<g:link style="text-decoration:none;" action="downloadFileContents" id="${execId+"_"+map.key}" 
													 params="[execId: "${execId}", execDeviceId: "${execDeviceId}", execResultId: "${executionResultInstance.id}" ]" >
													<span class="customizedLink" >${map.key}</span>	
												</g:link>
											</g:form>	
										</td>
										<td style="max-width: 450px;">
											
												&emsp;<span id="showSmemContents${m}_${k}_${i}" >	
												<a href="#" onclick="showSmemHideLink(${m},${k},${i})">Show</a>	&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
												<g:link action="showFileContents" onSuccess="showSmemHideLink(${m},${k},${i});" params="[fileName: "${execId+"_"+map.key}", execId: "${execId}", execDeviceId: "${execDeviceId}", execResultId: "${executionResultInstance.id}" ]"  target="_blank"> Log Link</g:link>						
												</span>
												<span id="hideSmemContents${m}_${k}_${i}" style="display:none;"><a href="#" onclick="hideSmemLogs(${m},${k},${i})">Hide</a></span>
												<br>
											<pre>
												<div id="smemDetails${m}_${k}_${i}" style="display:none;overflow: auto; height: 300px;width:540px;">${map.value}</div>	
											</pre>
										</td>
									</tr>
								</g:each>
							</tbody>
						</table>	
					</g:if>
				</section>
			</span>
			<g:if test="${pmapFileMap}">	
				<table>
					<tr class="scripthead" style=" background:#DFDFDF;">
						<td colspan="4" class="tdhead">pmap</td>					
						<td>
							<a href="#" id="expanderPmap${k}_${i}" onclick="this.innerHTML='Hide';viewOnClickToolPmap(this,${k},${i}); return false;">Show</a>
					</tr>
				</table>
			</g:if>	
			<span id="toolPmap${k}_${i}"  style="display: none;">
				<section class="round-border">
					<g:if test="${pmapFileMap}">	
						<table>
							<tbody >
								<tr class="fnhead1">
										<td class="tdhead" style="width:5%;">File Name</td>
										<td class="tdhead" style="max-width: 450px;">Contents</td>
								</tr>
								<g:each in="${pmapFileMap}" status="m"  var="map">
									<tr>
										<td style="width:5%;">
											<g:form controller="execution">
												<g:link style="text-decoration:none;" action="downloadFileContents" id="${execId+"_"+map.key}" 
													 params="[execId: "${execId}", execDeviceId: "${execDeviceId}", execResultId: "${executionResultInstance.id}" ]" >
													<span class="customizedLink" >${map.key}</span>	
												</g:link>
											</g:form>	
										</td>
										<td style="max-width: 450px;">
											
												&emsp;<span id="showPmapContents${m}_${k}_${i}" >	
												<g:remoteLink id="pmapShow${m}_${k}_${i}" before="alert('Please wait, Fetching pmap file contents may take few seconds');" action="getPmapContents" update="pmapDetails${m}_${k}_${i}" onSuccess="viewOnPmapClick(${m},${k},${i}); return false;" params="[fileName: "${execId+"_"+map.key}", execId: "${execId}", execDeviceId: "${execDeviceId}", execResultId: "${executionResultInstance.id}" ]" >Show</g:remoteLink>
												&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
												<g:link id="pmapLinkShow${m}_${k}_${i}" action="showFileContents" params="[fileName: "${execId+"_"+map.key}", execId: "${execId}", execDeviceId: "${execDeviceId}", execResultId: "${executionResultInstance.id}" ]"  target="_blank"> Log Link</g:link>	
												</span>
												<span id="hidePmapContents${m}_${k}_${i}" style="display:none;"><a href="#" onclick="hidePmapLogs(${m},${k},${i})">Hide</a></span>					
												<br>
											<pre>
												<div id="pmapDetails${m}_${k}_${i}" style="display:none;overflow: auto; height: 300px;width:540px;">${pmapFileData}</div>	
											</pre>
										</td>
									</tr>
								</g:each>
							</tbody>
						</table>	
					</g:if>
				</section>
			</span>
			<g:if test="${systemdanalysisFileMap}">	
				<table>
					<tr class="scripthead" style=" background:#DFDFDF;">
						<td colspan="4" class="tdhead">systemd-analyze</td>					
						<td>
							<a href="#" id="expanderSystemdAnalysis${k}_${i}" onclick="this.innerHTML='Hide';viewOnClickToolSystemdAnalyis(this,${k},${i}); return false;">Show</a>
					</tr>
				</table>
			</g:if>	
			<span id="toolSystemdAnalysis${k}_${i}"  style="display: none;">
				<section class="round-border">
					<g:if test="${systemdanalysisFileMap}">	
						<table>
							<tbody >
								<tr class="fnhead1">
										<td class="tdhead" style="width:5%;">File Name</td>
										<td class="tdhead" style="max-width: 450px;">Contents</td>
								</tr>
								<g:each in="${systemdanalysisFileMap}" status="m"  var="map">
									<tr>
										<td style="width:5%;">
											<g:form controller="execution">
												<g:link style="text-decoration:none;" action="downloadFileContents" id="${execId+"_"+map.key}" 
													 params="[execId: "${execId}", execDeviceId: "${execDeviceId}", execResultId: "${executionResultInstance.id}" ]" >
													<span class="customizedLink" >${map.key}</span>	
												</g:link>
											</g:form>	
										</td>
										<g:if test="${map.key.contains('svg')}">	
											<td style="max-width: 450px;">
												
													&emsp;<span id="showSystemdAnalysisContents${m}_${k}_${i}" >	
													<a href="#" onclick="showSystemdAnalysisHideLink(${m},${k},${i})">Show</a>	&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
													<g:link action="showSVGContents" onSuccess="showSystemdAnalysisHideLink(${m},${k},${i});" params="[fileName: "${execId+"_"+map.key}", execId: "${execId}", execDeviceId: "${execDeviceId}", execResultId: "${executionResultInstance.id}" ]"  target="_blank"> Log Link</g:link>						
													</span>
													<span id="hideSystemdAnalysisContents${m}_${k}_${i}" style="display:none;"><a href="#" onclick="hideSystemdLogs(${m},${k},${i})">Hide</a></span>
													<br>
												<pre>
													<div id="SystemdAnalysisDetails${m}_${k}_${i}" style="display:none;overflow: auto; height: 500px;width:500px;"><img src="${map.value}" /></div>	
												</pre>
											</td>
										</g:if>
										<g:else>
											<td style="max-width: 450px;">
													&emsp;<span id="showSystemdAnalysisContents${m}_${k}_${i}" >	
													<a href="#" onclick="showSystemdAnalysisHideLink(${m},${k},${i})">Show</a>	&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
													<g:link action="showFileContents" onSuccess="showSystemdAnalysisHideLink(${m},${k},${i});" params="[fileName: "${execId+"_"+map.key}", execId: "${execId}", execDeviceId: "${execDeviceId}", execResultId: "${executionResultInstance.id}" ]"  target="_blank"> Log Link</g:link>						
													</span>
													<span id="hideSystemdAnalysisContents${m}_${k}_${i}" style="display:none;"><a href="#" onclick="hideSystemdLogs(${m},${k},${i})">Hide</a></span>
													<br>
												<pre>
													<div id="SystemdAnalysisDetails${m}_${k}_${i}" style="display:none;overflow: auto; height: 300px;width:500px;">${map.value}</div>	
												</pre>
											</td>
										</g:else>
									</tr>
								</g:each>
							</tbody>
						</table>	
					</g:if>
				</section>
			</span>
			<g:if test="${systemdBootchartFileMap}">	
				<table>
					<tr class="scripthead" style=" background:#DFDFDF;">
						<td colspan="4" class="tdhead">systemd-bootchart</td>					
						<td>
							<a href="#" id="expanderSystemdBootchart${k}_${i}" onclick="this.innerHTML='Hide';viewOnClickToolSystemdBootchart(this,${k},${i}); return false;">Show</a>
					</tr>
				</table>
			</g:if>	
			<span id="toolSystemdBootchart${k}_${i}"  style="display: none;">
				<section class="round-border">
					<g:if test="${systemdBootchartFileMap}">	
						<table>
							<tbody >
								<tr class="fnhead1">
										<td class="tdhead" style="width:5%;">File Name</td>
										<td class="tdhead" style="max-width: 450px;">Contents</td>
								</tr>
								<g:each in="${systemdBootchartFileMap}" status="m"  var="map">
									<tr>
										<td style="width:5%;">
											<g:form controller="execution">
												<g:link style="text-decoration:none;" action="downloadFileContents" id="${execId+"_"+map.key}" 
													 params="[execId: "${execId}", execDeviceId: "${execDeviceId}", execResultId: "${executionResultInstance.id}" ]" >
													<span class="customizedLink" >${map.key}</span>	
												</g:link>
											</g:form>	
										</td>	
											<td style="max-width: 450px;">
												&emsp;<span id="showSystemdBootchartContents${m}_${k}_${i}" >	
													<a href="#" onclick="showSystemdBootchartHideLink(${m},${k},${i})">Show</a>	&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
													<g:link action="showSVGContents" onSuccess="showSystemdBootchartHideLink(${m},${k},${i});" params="[fileName: "${execId+"_"+map.key}", execId: "${execId}", execDeviceId: "${execDeviceId}", execResultId: "${executionResultInstance.id}" ]"  target="_blank"> Log Link</g:link>						
												</span>
												<span id="hideSystemdBootchartContents${m}_${k}_${i}" style="display:none;"><a href="#" onclick="hideSystemdBootchartLogs(${m},${k},${i})">Hide</a></span>
												<br>
											<pre>
												<div id="SystemdBootchartDetails${m}_${k}_${i}" style="display:none;overflow: auto; height: 500px;width:500px;"><img src="${map.value}" /></div>	
											</pre>
										</td>
									</tr>
								</g:each>
							</tbody>
						</table>	
					</g:if>
				</section>
			</span>	
			<g:if test="${lmbenchFileMap}">	
				<table>
					<tr class="scripthead" style=" background:#DFDFDF;">
						<td colspan="4" class="tdhead">lmbench</td>					
						<td>
							<a href="#" id="expanderlmbench${k}_${i}" onclick="this.innerHTML='Hide';viewOnClickToollmbench(this,${k},${i}); return false;">Show</a>
					</tr>
				</table>
			</g:if>	
			<span id="toollmbench${k}_${i}"  style="display: none;">
				<section class="round-border">
					<g:if test="${lmbenchFileMap}">	
						<table>
							<tbody >
								<tr class="fnhead1">
										<td class="tdhead" style="width:5%;">File Name</td>
										<td class="tdhead" style="max-width: 450px;">Contents</td>
								</tr>
								<g:each in="${lmbenchFileMap}" status="m"  var="map">
									<tr>
										<td style="width:5%;">
											<g:form controller="execution">
												<g:link style="text-decoration:none;" action="downloadFileContents" id="${execId+"_"+map.key}" 
													 params="[execId: "${execId}", execDeviceId: "${execDeviceId}", execResultId: "${executionResultInstance.id}" ]" >
													<span class="customizedLink" >${map.key}</span>	
												</g:link>
											</g:form>	
										</td>
										<td style="max-width: 450px;">
											
												&emsp;<span id="showlmbenchContents${m}_${k}_${i}" >	
												<a href="#" onclick="showlmbenchHideLink(${m},${k},${i})">Show</a>	&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
												<g:link action="showFileContents" onSuccess="showlmbenchHideLink(${m},${k},${i});" params="[fileName: "${execId+"_"+map.key}", execId: "${execId}", execDeviceId: "${execDeviceId}", execResultId: "${executionResultInstance.id}" ]"  target="_blank"> Log Link</g:link>						
												</span>
												<span id="hidelmbenchContents${m}_${k}_${i}" style="display:none;"><a href="#" onclick="hidelmbenchLogs(${m},${k},${i})">Hide</a></span>
												<br>
											<pre>
												<div id="lmbenchDetails${m}_${k}_${i}" style="display:none;overflow: auto; height: 300px;width:540px;">${map.value}</div>	
											</pre>
										</td>
									</tr>
								</g:each>
							</tbody>
						</table>	
					</g:if>
				</section>
			</span>
			</td>
			</tr>
		</tbody>
	</table>
</g:if>
<g:elseif test="${svgDetails}">
	<img src="${logPath}" />
</g:elseif>
<g:else>
<pre>
	<div style="">${consoleFileData}</div>	
</pre>
</g:else>
