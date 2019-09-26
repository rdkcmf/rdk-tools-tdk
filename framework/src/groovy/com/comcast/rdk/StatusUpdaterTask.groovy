/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2016 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/
package com.comcast.rdk

/**
 * Runnable task to update the device status of one device.
 *
 */
class StatusUpdaterTask implements Runnable {
	
	String[] cmd;
	Device device;
	def deviceStatusService
	def executescriptService
	def executionService
	def grailsApplication
	
	public StatusUpdaterTask(String[] cmd,Device device,def deviceStatusService,def executescriptService,def grailsApplication){
		this.cmd = cmd;
		this.device = device;
		this.deviceStatusService = deviceStatusService;
		this.executescriptService = executescriptService
		this.grailsApplication = grailsApplication
	}

	@Override
	public void run() {
		String outData = ""
		boolean devExist = true
		
		try {

			def resultArray = Device.executeQuery("select a.stbIp, a.stbName,a.statusPort from Device a where a.id = :devId",[devId: device?.id])

			if(resultArray && resultArray?.size() == 1){
				def subArray = resultArray[0]
				if(subArray && subArray?.size() == 3){
					String devIp = subArray[0]
					String devName = subArray[1]
					int port = Integer.parseInt(subArray[2])
					Device.withTransaction {
						device = Device.findByIdAndStbName(device?.id,devName)
					}

					String [] cmdArray = [
						cmd[0],
						cmd[1],
						devIp,
						port,
						cmd[4],
						devName
					]
					cmd = cmdArray
				}
			}else{
				devExist = false
			}
		} catch (Exception e) {
			e.printStackTrace()
		}
		
		if(devExist){
			try {
				outData = new ScriptExecutor().executeScript(cmd,1)
			} catch (Exception e) {
				e.printStackTrace()
			}
		outData = outData?.trim()
		if(outData){
			if(outData.equals(Status.FREE.toString())){
				String status = Status.FREE.toString()
				
				def executionList = Execution.findAllByExecutionStatusAndDevice("PAUSED",device.getStbName());
				if(executionList.size() > 0){
				executionList.each{
					Execution execution = it
					def execDevice = ExecutionDevice.findByStatusAndDeviceAndExecution("PAUSED",device.getStbName(),execution);
					boolean paused = false
						if(execDevice){
							
							synchronized (ExecutionController.lock) {
								if(ExecutionService.deviceAllocatedList.contains(device?.id)){
									status = "BUSY"
								}else{
									if(!ExecutionService.deviceAllocatedList.contains(device?.id)){
										ExecutionService.deviceAllocatedList.add(device?.id)
									}
								}
							}
							if(status.equals(Status.FREE.toString())){
							Thread.start {
								try{
									deviceStatusService.updateDeviceStatus(device,"BUSY")
								}
								catch(Exception e){
								}
							}
							try{
								paused = executescriptService.restartExecution(execDevice,grailsApplication)
							}finally{
								if(ExecutionService.deviceAllocatedList.contains(device?.id)){
									ExecutionService.deviceAllocatedList.remove(device?.id)
								}
							}
							}
						}
					if(!paused){
						RepeatPendingExecution rExecution = RepeatPendingExecution.findByDeviceNameAndStatus(device.getStbName(),"PENDING")
						if(rExecution){
						runCompleteRepeat(device)
						}
					}
				}
				}else{
					def executionList11 = Execution.findAllByExecutionStatusAndDevice(Constants.INPROGRESS_STATUS,device.getStbName());
					if(executionList.size() == 0 && executionList11.size() < 1){
						RepeatPendingExecution rExecution = RepeatPendingExecution.findByDeviceNameAndStatus(device.getStbName(),"PENDING")
						if(rExecution){
							runCompleteRepeat(device)
						}
					}
				}
			}
			else if(outData.equals(Status.BUSY.toString()))
			{
					String status = Status.BUSY.toString()
					def execList = Execution.findAllByExecutionStatusAndDevice(Constants.PAUSED,device?.getStbName());
					def deviceObj = Device.findById(device?.id)
					if (execList?.size() > 0)
					{
						executescriptService.resetAgent(deviceObj, Constants.FALSE)
						Thread.sleep(6000)
					}
			}							
			if(devExist){
				callStatusUpdater(device,outData)
			}
			
		}
	}
	}
	
	def callStatusUpdater(device,outData) throws Exception{
		try{
			deviceStatusService.updateDeviceStatus(device,outData) 
		}
		catch(Exception e){
		}
	}
	
	
	
	/**
	 * Method to restart a complete repeat once device is free
	 * @param device
	 */
	private void runCompleteRepeat(def device){
		RepeatPendingExecution rExecution = RepeatPendingExecution.findByDeviceNameAndStatus(device.getStbName(),"PENDING")
		Execution execution = Execution.findByName(rExecution?.executionName)
		boolean paused = false
		try{
			if(execution != null && rExecution?.completeExecutionPending > 0){

				if(!ExecutionService.deviceAllocatedList.contains(device?.id)){
					ExecutionService.deviceAllocatedList.add(device?.id)
				}

				def th = Thread.start {
					try{
						deviceStatusService.updateDeviceStatus(device,"BUSY")
					}
					catch(Exception e){
					}
				}

				try{
					RepeatPendingExecution.withTransaction{
						RepeatPendingExecution rEx = RepeatPendingExecution.findById(rExecution?.id)
						rEx?.status = "IN-PROGRESS"
						rEx.save(flush:true)
					}

					int count = 0
					String exName= execution.name
					if(rExecution?.currentExecutionCount > 0){
						count = (rExecution?.currentExecutionCount)
						try {
							if(exName.contains("_")){
								exName = exName.substring(0,exName.lastIndexOf("_"));
							}
						} catch (Exception e) {
							e.printStackTrace()
						}
					}
					int pendingExecutions = rExecution?.completeExecutionPending
					for(int i = 1 ; i <= pendingExecutions && !paused; i++){
						RepeatPendingExecution.withTransaction{
							rExecution = RepeatPendingExecution.findById(rExecution?.id)
						}
						try {
							String newExName = exName+"_"+(count+i)
							try {
								paused = executescriptService.triggerRepeatExecution(execution,newExName,grailsApplication,device?.getStbName())
							} catch (Exception e) {
								e.printStackTrace()
							}
							RepeatPendingExecution.withTransaction{
								RepeatPendingExecution rEx = RepeatPendingExecution.findById(rExecution?.id)
								rEx?.currentExecutionCount = (rExecution?.currentExecutionCount + 1)
								rEx?.completeExecutionPending = (rExecution?.completeExecutionPending - 1)
								rEx.save(flush:true)
							}
						} catch (Exception e) {
							e.printStackTrace()
						}
					}
					saveRepeatExecutionStatus(paused, rExecution)
				}finally{
					if(ExecutionService.deviceAllocatedList.contains(device?.id)){
						ExecutionService.deviceAllocatedList.remove(device?.id)
					}
				}
			}else{
				if(rExecution?.completeExecutionPending == 0){
					saveRepeatExecutionStatus(false, rExecution)
				}
			}
		}finally{
			if(ExecutionService.deviceAllocatedList.contains(device?.id)){
				ExecutionService.deviceAllocatedList.remove(device?.id)
			}
		}
	}
	
	private void saveRepeatExecutionStatus(boolean paused , def rExecution){
		String status = ""
		if(!paused){
			status = "COMPLETED"
		}else{
			status = "PENDING"
		}
		
		RepeatPendingExecution.withTransaction{
			RepeatPendingExecution rEx = RepeatPendingExecution.findById(rExecution?.id)
			rEx?.status = status
			rEx.save(flush:true)
		}
	}

}
