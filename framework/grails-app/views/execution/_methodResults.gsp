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
<script type="text/javascript">
	/*Method to show the execution method results for a script execution*/
	function showMethodResults(execResId){
    	$('#hideMethodResultLink'+execResId).show();
    	if(document.getElementById('MethodResult'+execResId).style.display == 'none') {
    		document.getElementById('MethodResult'+execResId).style.display ='';
    	}
    	$('#showMethodResultLink'+execResId).hide();
	}
	/*Method to hide the execution method results for a script execution*/
	function hideMethodResults(execResId){
    	$('#showMethodResultLink'+execResId).show();
    	if(document.getElementById('MethodResult'+execResId).style.display == '') {
    		document.getElementById('MethodResult'+execResId).style.display ='none';
    	}
    	$('#hideMethodResultLink'+execResId).hide();
	}
</script>
<br/>
<table style="width:70%;">
	<g:each in="${executionResultInstance.executemethodresults}" var="executionResultMthdsInstance">
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
</table>