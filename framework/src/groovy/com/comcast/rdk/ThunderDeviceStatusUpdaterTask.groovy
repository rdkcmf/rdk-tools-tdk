/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2020 RDK Management
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

class ThunderDeviceStatusUpdaterTask implements Runnable {

	String[] cmd;
	Device device;
	def deviceStatusService
	def executescriptService
	def executionService
	def grailsApplication

	public ThunderDeviceStatusUpdaterTask(String[] cmd,Device device,def deviceStatusService,def executescriptService,def grailsApplication){
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
			String devIp = device?.stbIp
			String [] cmdArray = [
						          cmd[0],
						          cmd[1],
						          devIp,
								  cmd[3]
					             ]
			cmd = cmdArray
		} catch (Exception e) {
			e.printStackTrace()
		}

		def time1 = System.currentTimeMillis()
		if(devExist){
			try {
				outData = new ScriptExecutor().executeScript(cmd,1)
			} catch (Exception e) {
				println "Error on trying to complete "+cmd+ " time "+ ((System.currentTimeMillis() - time1) /1000)
			}
			outData = outData?.trim()
			if(outData){
				if(outData.equals(Status.FREE.toString())){
					deviceStatusService.updateDeviceStatus(device,outData)
					String status = "FREE"
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
									}
								}
								if(status == "FREE"){
									try{
										if(execDevice?.category == Category.RDKV){
											Thread.start {
												try{
													if(!ExecutionService.deviceAllocatedList.contains(device?.id)){
														ExecutionService.deviceAllocatedList.add(device?.id)
													}
													deviceStatusService.updateOnlyDeviceStatus(device,"BUSY")
												}
												catch(Exception e){
												}
											}
											paused = executescriptService.restartExecution(execDevice,grailsApplication)
										}else{
											paused = executescriptService.restartThunderExecution(execDevice,grailsApplication)
										}
									}finally{
										if(ExecutionService.deviceAllocatedList.contains(device?.id)){
											ExecutionService.deviceAllocatedList.remove(device?.id)
										}
									}
								}
							}
							if(!paused){
							}
						}
					}
				}else if(outData.equals(Status.BUSY.toString())){
					deviceStatusService.updateDeviceStatus(device,outData)
				}else if(outData.equals("")){
					deviceStatusService.updateDeviceStatus(device,"NOT_FOUND")
				}else if(outData.equals("NOT_FOUND")){
					deviceStatusService.updateDeviceStatus(device,"NOT_FOUND")
				}else{
				    synchronized (ExecutionController.lock) {
				        if(ExecutionService.deviceAllocatedList.contains(device?.id)){
					        outData = "BUSY"
					        deviceStatusService.updateDeviceStatus(device,outData)
				        }
			        }
				}
		    }else{
			    deviceStatusService.updateDeviceStatus(device,"NOT_FOUND")
		    }
	    }
    }
}
