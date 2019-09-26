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
<g:form  method="post">

	<g:hiddenField name="deviceId" id="deviceId" value="${device}" />	
	<g:hiddenField name="scriptlist" id="scriptlist" value="${scripts}" />	
	<g:hiddenField name="scriptGroup" id="scriptGroup" value="${scriptGroup}" />
	<g:hiddenField name="isSystemDiagnostics" id="isSystemDiagnostics" value="${isSystemDiagnostics}" />
	<g:hiddenField name="isBenchMark" id="isBenchMark" value="${isBenchMark}" />
	<g:hiddenField name="rerun" id="rerun" value="${rerun}" />
	<g:hiddenField name="repeatCount" id="repeatCount" value="${repeatCount}" />
	<g:hiddenField name="devices" id="repeatCount" value="${devices}" />
	<g:hiddenField name="isStbLogRequired" id="transferLogs" value="${isStbLogRequired}" />
	<g:hiddenField name="category" id="category" value="${category}"/>
	
	<table id="scheduletable">
	<tr>
	
	
	<th>Schedule Job</th>		
	</tr>
	<tr>
		<td>
		    <div id="scheduleOptionDiv">Select Schedule Type :	&emsp;			
			<input onclick="showOnetimeSchedule();" type="radio" checked="checked" name="scheduleGroup" value="OnetimeSchedule" />OnetimeSchedule 
			&emsp;<input onclick="showReccuranceSchedule();" type="radio" name="scheduleGroup" value="ReccurenceSchedule" />ReccurenceSchedule
			</div>				
		</td>
	</tr>
	<tr>			
		<td align="left">					
			<div id="onetimeScheduleDiv">Select Date & Time ::	&emsp;&emsp;&emsp;		
				<g:datePicker name="testdate"/>&emsp;					
				<span id="executeBtn" class="buttons">
				<g:submitToRemote class="save" 
					action="scheduleOneOff" controller="execution" value="Schedule" 
					update="newScheduleTable" onSuccess="baseScheduleTableSave();">
				</g:submitToRemote>
				</span>	
			</div>								
		</td>
	</tr>		
	<tr>			
		<td>
			<div id="reccuranceScheduleDiv" style="display: none; ">						
				<table>
					<tr>
						<td width="20%"><div class="verticalLine">
							<input onclick="showDaily();" type="radio" name="reccurGroup" value="Daily" checked="checked" />Daily 
							</br></br><input onclick="showWeekly();" type="radio" name="reccurGroup" value="Weekly" />Weekly	
							</br></br><input onclick="showMonthly();" type="radio" name="reccurGroup" value="Monthly" />Monthly										
							</div>										
						</td>						
						<td width="80%">
							<div id="reccurDaily">
								<input type="radio" name="reccurDaily" checked="checked" value="dailyDays" />Every 
								<g:textField id="dailyDaysCount" name="dailyDaysCount" required="" value="1" size="2"/>days 
								</br></br><input type="radio" name="reccurDaily" value="dailyWeekday" />Every weekday	
							</div>
							<div id="reccurWeekly" style="display: none;">
								<g:checkBox name="weekDay" value="SUN" checked="false" />SUN&emsp;	
								<g:checkBox name="weekDay" value="MON" checked="false" />MON&emsp;
								<g:checkBox name="weekDay" value="TUE" checked="false" />TUE&emsp;
								<g:checkBox name="weekDay" value="WED" checked="false" />WED&emsp;
								<g:checkBox name="weekDay" value="THU" checked="false" />THU&emsp;
								<g:checkBox name="weekDay" value="FRI" checked="false" />FRI&emsp;
								<g:checkBox name="weekDay" value="SAT" checked="false" />SAT&emsp;											
							</div>
							<div id="reccurMonthly" style="display: none;">
								<input type="radio" name="reccurMonthly" value="monthlyDays" checked="checked"/> Day&nbsp; 
								<g:textField id="monthlyDaysCount" name="monthlyDaysCount" required="" value="1" size="2"/>
								&nbsp;of every&nbsp;<g:textField id="monthlyMonthCount" name="monthlyMonthCount" 
								required="" value="1" size="2"/> months
								</br></br>
								<input type="radio" name="reccurMonthly" value="monthlyComplex" /> The&nbsp; 
								<select name="daytype">
								  <option value="1">first</option>
								  <option value="2">second</option>
								  <option value="3">third</option>
								  <option value="4">fourth</option>
								  <option value="L">last</option>
								</select>
								<select name="dayName">
								  <option value="1">Sunday</option>
								  <option value="2">Monday</option>
								  <option value="3">Tuesday</option>
								  <option value="4">Wednesday</option>
								  <option value="5">Thursday</option>
								  <option value="6">Friday</option>
								  <option value="7">Saturday</option>
								</select> 
								&nbsp;of every&nbsp;<g:textField id="monthlyMonthCnt" name="monthlyMonthCnt" required="" value="1" size="2"/> months 
							</div>
						</td>
					</tr>
					<tr>
						<td width="100%" colspan="2">
							Start Date &nbsp;: <g:datePicker name="startdate"/>&emsp;	
							<br><br>End Date&emsp;: <g:datePicker name="enddate"/>&emsp;&emsp;&emsp;
							
							<span class="buttons">
								<g:submitToRemote class="save" 
									action="scheduleOneOff" controller="execution" value="Schedule" 
									update="newScheduleTable" onSuccess="baseScheduleTableSave();" >
								</g:submitToRemote>		
							</span>
						</td>									
					</tr>
				</table>							
			</div>												
		</td>
	</tr>	
	</table>
	</g:form>
	<g:form method="post">
	<div id="newMessage" style="width:100%; text-align : right;">Cannot delete an entry if its start/end date is after the current date</div>
	<div id="baseScheduleTable" class="hello">
		<g:render template="scheduleTable" ></g:render>		
	</div>	
	<div id="newScheduleTable"></div>
</g:form>


