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
package com.comcast.rdk.socketCommuniation

import static com.comcast.rdk.Constants.COMMA_SEPERATOR
import static com.comcast.rdk.Constants.UNDERSCORE

import com.comcast.rdk.Device
import com.comcast.rdk.ExecutionResult;
import com.comcast.rdk.Module
import com.comcast.rdk.ScriptExecutor
import com.comcast.rdk.ScriptFile

public class SocketPortConnector extends Thread {

	private static ServerSocket serverSocket;

	private static String fileTransferPath
	private static String destinationCrashFile
	private static final String CRASH_TOKEN = "CRASH_"
	public SocketPortConnector(){
	}

	public SocketPortConnector(int port, String filePath, String destFile) throws IOException {
		fileTransferPath = filePath
		destinationCrashFile = destFile
		serverSocket = new ServerSocket(port);
		//serverSocket.setSoTimeout(10000);
	}

	public static closeServerSocket(){
		//	println "closeServerSocket ---------------------------------- "
		serverSocket.close()
	}

	public void run() {
		while(!(serverSocket.closed)) {
			try {
				//  println " BEGIN "
				Socket server = serverSocket.accept()
				BufferedReader br = new BufferedReader(new InputStreamReader(server.getInputStream(), "UTF8"))
				String dataFromSocket = br.readLine()
				if(dataFromSocket.toString().startsWith(CRASH_TOKEN)){
					String[] dataArray1 = dataFromSocket.split( UNDERSCORE )
					String details = dataArray1[1]
					String[] detailsArray = details.split( COMMA_SEPERATOR )
					if(detailsArray.length == 5){
						String execId = detailsArray[0]
						String deviceId = detailsArray[1]
						String scriptId = detailsArray[2]
						String execDeviceId = detailsArray[3]
						String execResultId = detailsArray[4]

						def devStbIp
						def devLogTransferPort
						Device.withTransaction{
							Device device = Device.findById(deviceId)
							devStbIp = device?.stbIp
							devLogTransferPort = device?.logTransferPort
						}
						ScriptFile.withTransaction {
							ScriptFile script = ScriptFile.findById(scriptId)
							if(script == null){
								def er = ExecutionResult.findById(execResultId)
//								er.s
							}
							def moduleName = script?.getModuleName()
							def module = Module.findByName(moduleName)
							String filePath = ""
							String directoryPath = ""
							int cnt = 0
							module?.logFileNames?.each{ logfilename ->

								String logFileName  = logfilename.toString()
								int lastIndex = logFileName.lastIndexOf('/')
								int stringLength = logFileName.length()
								String extractedFileName = logFileName.substring(lastIndex+1, stringLength)

								cnt++
								if((logFileName) && !(logFileName.isEmpty())){
									filePath = destinationCrashFile.replace("execId_logdata.txt", "${execId}//${execDeviceId}//${execResultId}//${execId}_${execDeviceId}_${cnt}${extractedFileName}")
									directoryPath = destinationCrashFile.replace("execId_logdata.txt", "${execId}//${execDeviceId}//${execResultId}")
									new File(directoryPath).mkdirs()

									String[] cmd = [
										"python",
										fileTransferPath,
										devStbIp,
										devLogTransferPort,
										logFileName,
										filePath
									]

									try {
										ScriptExecutor scriptExecutor = new ScriptExecutor()
										def outputData = scriptExecutor.executeScript(cmd,1)
									}catch (Exception e) {
										e.printStackTrace()
									}
								}
							}
						}
					}
				}
				else{
					try {
						String[] dataArray = dataFromSocket.split( COMMA_SEPERATOR )
						if(dataArray){
							if(dataArray[0] && dataArray[1]){
								String stbName = dataArray[0]
								String stbIp = dataArray[1]
								Device device = Device.findByStbName(stbName.trim())
								if(device){
									if(!device?.isChild){
										Device.executeUpdate("update Device c set c.stbIp = :newStatus where c.id = :devId",[newStatus: stbIp,  devId: (device?.id)])
										device?.childDevices.each { child ->
											try {
												Device.executeUpdate("update Device c set c.stbIp = :newStatus  where c.id = :devId",[newStatus: stbIp, devId: (child?.id)])
											} catch (Exception e) {
												e.printStackTrace()
											}
										}
									}
								}
							}
						}
					} catch (Exception e) {
						e.printStackTrace()
					}
				}
				server.close();
			}catch(IOException e)
			{
				e.printStackTrace()
			}
			catch(Exception ex)
			{
				ex.printStackTrace()
			}
		}
	}
}
