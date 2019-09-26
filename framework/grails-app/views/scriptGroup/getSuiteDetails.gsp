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
<%@ page import="org.apache.shiro.SecurityUtils;com.comcast.rdk.Category"%>
<%@ page import="com.comcast.rdk.ScriptGroup" %>
<%@ page import="com.comcast.rdk.Script"%>
<%@ page import="com.comcast.rdk.User" %>
  <g:javascript library="jquery"/>
<style type="text/css" media="screen">
</style>
<script type="text/javascript">
window.onload = $(function(){
	$("#rdkB").hide();
	$("#rdkV").show();
	var ele = document.getElementsByName("category");
		ele[0].checked = true;
		ele[1].checked = false;
});

function display(val) {
	if (val.trim() === 'RDKV') {
		$("#rdkB").hide();
		$("#rdkV").show();
	} else if (val.trim() === 'RDKB') {
		$("#rdkV").hide();
		$("#rdkB").show();
	} else {}
}

$('#selectAllV').click(function() {
	   if (this.checked) {
	       $(':checkbox').each(function() {
	           this.checked = true;                        
	       });
	   } else {
	      $(':checkbox').each(function() {
	           this.checked = false;                        
	       });
	   } 
});
$('#selectAllB').click(function() {
	   if (this.checked) {
	       $(':checkbox').each(function() {
	           this.checked = true;                        
	       });
	   } else {
	      $(':checkbox').each(function() {
	           this.checked = false;                        
	       });
	   } 
	});
	


function checkChecked(moduleSelect,scriptGroupList,newScriptName)
{
	var i;
    var anyBoxesChecked = false;
    $('#' + moduleSelect + ' input[type="checkbox"]').each(function() 
    	    {
       			 if ($(this).is(":checked")) 
           			 {
           				 anyBoxesChecked = true;
       					 }
   			 });
    
    if (anyBoxesChecked == false) 
        {
     	 alert('Please select at least one Module Name');
   	  	 return false;
   	 } 

  
    if ((scriptGroupList.indexOf("["+newScriptName+", ") > -1 )||( scriptGroupList.indexOf(", "+newScriptName+", ")>-1)||
    (scriptGroupList.indexOf(", "+newScriptName+"]")>-1)||(scriptGroupList.indexOf("["+newScriptName+"]")>-1))
        {
	    	alert("Duplicate Test Suite Name. Try again.");	
	    	console.log("Duplicate Test Suite Name ")
	    	return false;
        }	 	 
  
}
</script>




<g:set var="entityName" value="${message(code: 'scriptGroup.label', default: 'TestSuite')}" />
<h1><g:message code="default.create.label" args="[entityName]" /></h1>
	<div style="padding: 20px;margin-left:1%;">
		<b style="color: #A24C15;">Select the Category</b>&nbsp;&nbsp;&nbsp;
		<input type="radio" onclick="display('RDKV')" name="category" checked >RDK-V</input> &nbsp;&nbsp;
		<input type="radio" onclick="display('RDKB')" name="category">RDK-B</input>
	</div>


	<div id="rdkV">
		<g:form action="saveCustomGrp" id="searchForm" name="searchForm" method="POST" onsubmit="return confirm('Test Suite creation takes some time');" >


		<div class="contextMenu" style="padding: 20px; margin-left:1%; width: 950px;">
				<table style="width: 80%">
					<tr >
						<td width = "40%" >
							<label for="name">
								<g:message code="scriptGroup.name.label" default="Name" />
								<span class="required-indicator">*</span>
							</label>
							<g:textField id= "scriptName" name="name" required=""  style="width: 240px"/>
						</td>
					</tr>
				</table>
				<table >
					<tr>
						<td width = "30%">
							<br><br>
							<div id="boxType" >
								<label>Select Box Type</label> &nbsp;&nbsp;
								<g:select id="boxTypeId" name="boxname" from="${com.comcast.rdk.BoxType.findAllByCategory(Category.RDKV)}" 
												noSelection="['' : 'Please Select']" optionKey="id"
												required="" value="" class="many-to-one" />
							</div>				
						</td>
						<td width = "30%">
							<br><br>
							<div id="rdkVersion">
								<label>Select RDK Version</label> &nbsp;&nbsp;
									<g:select id="RDKVersionsId" name="RDKVersionsName" from="${com.comcast.rdk.RDKVersions.findAllByCategory(Category.RDKV)}" 
												noSelection="['' : 'Please Select']" optionKey="id"
												required="" value="" class="many-to-one" />
							</div>		
						</td>
						<td width = "30%" >
							<br><br>
							
							<label>Include Long Duration Scripts</label> &nbsp;&nbsp;
							<g:checkBox id="longDuration" name="longDuration" checked="false" onmouseover ="long duration test will be included only if selected" />

			 			</td>					
					</tr>
				</table>								
				<br><br>			
				<h1><g:message code="Module List" /></h1>					
				<br><br>
				<input type="checkbox" id="selectAllV" value="selectAll"> Select / Deselect All<br/><br/>			
				<table style="width:100%; align: center;">
					<thead>								
						<tr >
							<th style="text-align : center;" width="1%">  Select</th>
							<th style="text-align : center;" >Module Name</th>
								
							<th style="text-align : center; " width="1%">Select</th>
							
							<th style="text-align : center;" >Module Name</th>																				
						</tr>
					</thead>	
						
						<tbody>
							<% int count = 0; %> 
							<% int halfSize = (int)((moduleListSizeRDKV/2)+1) %>
							<g:each in="${0..<halfSize}" status="k" var="i">																
								<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
									<g:if test = "${moduleListRDKV[2*i]!=null }">	
									<g:hiddenField id="listCount" name="listCount" value="${count}"/>
									<% count++ %>
									<td style="text-align : center;" width="1%" >						
										<g:checkBox name="chkbox${count}" class ="checkbox" id ="${moduleListRDKV[2*i]?.id}" value="${false}"  checked = "false"  onclick ="checkBoxClicked(this)" /> 
										<g:hiddenField id="id${count}" name="id${count}" value="${moduleListRDKV[2*i]?.id}" />
									</td>
									<td style="text-align : center;"  >
										${fieldValue(bean: moduleListRDKV[2*i], field: "name")}
									</td>	
								
									<g:hiddenField id="listCount" name="listCount" value="${count}"/>
									<% count++ %>
									<g:if test = "${moduleListRDKV[2*i+1]!=null }">
										<td style="text-align : center;" width="1%" >						
											<g:checkBox name="chkbox${count}" class ="checkbox" id ="${moduleListRDKV[2*i+1]?.id}" value="${false}"  checked = "false"  onclick ="checkBoxClicked(this)" /> 
											<g:hiddenField id="id${count}" name="id${count}" value="${moduleListRDKV[2*i+1].id}" />
										</td>
										<td style="text-align : center;" >
											${fieldValue(bean: moduleListRDKV[2*i+1], field: "name")}								
										</td>	
									</g:if>	
									</g:if>
								</tr>
							</g:each>													
						</tbody>
					</table>	
			
				<br>
				<br>
				<g:if test="${SecurityUtils.getSubject().hasRole('ADMIN')}" >
					<g:actionSubmit value="Create" action="saveCustomGrp"
					 onclick=" return checkChecked('searchForm','${scriptGroupList }',document.getElementById('scriptName').value);"/>
				</g:if>
			</div>		
		</g:form>	
	  </div>
	       
	       
	  <div id="rdkB">
		<g:form action="saveCustomGrp" id="searchForm" name="searchForm" 
		method="POST" onsubmit="return confirm('Test Suite creation takes some time');">
			<div class="contextMenu" style="padding: 20px; margin-left:1%; width: 950px;">						
				<table style="width: 80%">
					<tr>
						<td width = "40%">
							<label for="name">
								<g:message code="scriptGroup.name.label" default="Name" />
									<span class="required-indicator">*</span>
							</label>
							<g:textField id= "scriptNameB" name="name" required=""  style="width: 240px"/>
						</td>
					</tr>
				</table>
				<table>
					<tr>
						<td width = "30%">
							<br><br>
							<div id="boxType">
								<label>Select Box Type</label> &nbsp;&nbsp;
								<g:select id="boxTypeId" name="boxname" from="${com.comcast.rdk.BoxType.findAllByCategory(Category.RDKB)}" 
									noSelection="['' : 'Please Select']" optionKey="id"
									required="" value="" class="many-to-one" />
							</div>										
						</td>
						<td width = "30%">
							<br><br>
							<div id="rdkVersion">
								<label>Select RDK Version</label> &nbsp;&nbsp;
								<g:select id="RDKVersionsId" name="RDKVersionsName" from="${com.comcast.rdk.RDKVersions.findAllByCategory(Category.RDKB)}" 
									noSelection="['' : 'Please Select']" optionKey="id"
									required="" value="" class="many-to-one" />
							</div>										
						</td>	
						
						<td width = "30%">
							<br><br>
							
							<label>Include Long Duration Scripts</label> &nbsp;&nbsp;
							<g:checkBox id="longDuration" name="longDuration" checked="false" onmouseover ="long duration test will be included only if selected" />
			 	
			 			</td>	
			 							
					</tr>
				</table>								
				<br><br>
				<h1><g:message code="Module List" /></h1>	
				<br><br>
				<input type="checkbox" id="selectAllB" value="selectAll"> Select / Deselect All<br/><br/>
				<table style="width:100%; align: center;">
					<thead>								
						<tr >
							<th style="text-align : center;" width="1%">  Select</th>
							<th style="text-align : center;" >Module Name</th>
								
							<th style="text-align : center; " width="1%">Select</th>
							
							<th style="text-align : center;">Module Name</th>																			
						</tr>
					</thead>	
					
						<tbody>
							<% int count = 0; %> 
							<% int halfSizeB = (int)((moduleListSizeRDKB/2)+1) %>
							<g:each in="${0..<halfSizeB}" status="k" var="i">																
								<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
									<g:if test = "${moduleListRDKB[2*i]!=null }">	
									<g:hiddenField id="listCount" name="listCount" value="${count}"/>
									<% count++ %>
									<td style="text-align : center;" width="1%" >						
										<g:checkBox name="chkbox${count}" class ="checkbox" id ="${moduleListRDKB[2*i]?.id}" value="${false}"  checked = "false"  onclick ="checkBoxClicked(this)" /> 
										<g:hiddenField id="id${count}" name="id${count}" value="${moduleListRDKB[2*i]?.id}" />
									</td>
									<td style="text-align : center;"  >
										${fieldValue(bean: moduleListRDKB[2*i], field: "name")}
									</td>	
								
									<g:hiddenField id="listCount" name="listCount" value="${count}"/>
									<% count++ %>
									<g:if test = "${moduleListRDKB[2*i+1]!=null }">
										<td style="text-align : center;" width="1%" >						
											<g:checkBox name="chkbox${count}" class ="checkbox" id ="${moduleListRDKB[2*i+1]?.id}" value="${false}"  checked = "false"  onclick ="checkBoxClicked(this)" /> 
											<g:hiddenField id="id${count}" name="id${count}" value="${moduleListRDKB[2*i+1].id}" />
										</td>
										<td style="text-align : center;" >
											${fieldValue(bean: moduleListRDKB[2*i+1], field: "name")}								
										</td>	
									</g:if>	
									</g:if>
								</tr>
							</g:each>													
						</tbody>

					</table>
				
				<br>
				<br>
				<g:if test="${SecurityUtils.getSubject().hasRole('ADMIN')}" >
					<g:actionSubmit value="Create" action="saveCustomGrp"
					 onclick=" return checkChecked('searchForm','${scriptGroupList }',document.getElementById('scriptNameB').value);"/>
				</g:if>
			</div>
		</g:form>	
 	 </div> 

