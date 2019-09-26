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

import java.io.InputStream;
import java.net.URLConnection;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors
import grails.util.Holders
import org.springframework.util.CollectionUtils

class LogTransferService {

	//def grailsApplication

	private static ExecutorService executorService = Executors.newCachedThreadPool()
	private static final String CONFIG_FILE = "/appConfig/logServer.properties"
	private static Properties props = null


	public static void transferLog(def executionName, def deviceInstance) {
		if(props == null){
			loadServerConfiguration()
		}
		if(!CollectionUtils.isEmpty(props)) {
			try {
				// initiating log transfer
				if(props.get("logServerUrl")){
					Runnable runnable = new Runnable(){
								public void run(){
									def startStatus = initiateLogTransfer(executionName, props.get("logServerUrl"), props.get("logServerAppName"), deviceInstance)
									if(startStatus){
										println "Log transfer job start initiated for $executionName"
									}
									else{
										println "Cannot create Log transfer job for $executionName"
									}
								}
							}
					executorService.execute(runnable);
				}
			} catch (Exception e) {
				e.printStackTrace()
			}
		}
	}

	public static void closeLogTransfer(def executionName){
		if(props == null){
			loadServerConfiguration()
		}
		if(!CollectionUtils.isEmpty(props)) {
			try {
				// stopping log transfer
				if(props.get("logServerUrl")){
					Runnable runnable = new Runnable(){
								public void run(){
									def stopStatus = stopLogTransfer(executionName, props.get("logServerUrl"), props.get("logServerAppName"))
									if(stopStatus){
										println "Stop Log transfer job initiated for $executionName"
									}
									else{
										println "Cannot stop Log transfer job for $executionName"
									}
								}
							}
					executorService.execute(runnable);
				}
			}catch (Exception e) {
				e.printStackTrace()
			}
		}
	}

	private static void initiateLogTransfer(String executionName, String server, String logAppName, Device device){
		int count = 3
		boolean logTransferInitiated = false
		try{
			println "start url : http://$server/$logAppName/startScheduler/$executionName/$device.stbName/$device.stbIp/$device.statusPort/$device.logTransferPort"
		}
		catch(Exception e){
			println e.getMessage()
		}

		while(count > 0 && !logTransferInitiated){
			HttpURLConnection connection = null
			try{
				println "initiating transaction"
				connection = new URL("http://$server/$logAppName/startScheduler/$executionName/$device.stbName/$device.stbIp/$device.statusPort/$device.logTransferPort").openConnection()
				connectToLogServerAndExecute(connection)
				println "Initiated log transfer for $executionName"
				logTransferInitiated = true
			}
			catch(Exception e) {
				e.printStackTrace()
				--count
			}
			finally{
				if(connection != null){
					connection.disconnect()
				}
			}
		}
		println "logTransferInitiated : $logTransferInitiated"
		logTransferInitiated

	}

	private static void stopLogTransfer(String executionName, String server, String logAppName){

		int count = 3
		boolean logTransferStopInitiated = false
		while(count > 0 && !logTransferStopInitiated){
			HttpURLConnection connection = null
			try{
				String url = "http://$server/$logAppName/stopScheduler/$executionName"
				print "url : $url"
				connection = new URL(url).openConnection()
				connectToLogServerAndExecute(connection)
				logTransferStopInitiated = true
			}
			catch(Exception e){
				e.printStackTrace()
				--count
			}
			finally{
				if(connection != null){
					connection.disconnect()
				}
			}
		}
		logTransferStopInitiated
	}

	private static void connectToLogServerAndExecute(URLConnection connection) {
		connection.setConnectTimeout(120000)
		int responseCode = connection.getResponseCode()
		if(responseCode == 200){
			String finalresp = getResponse(connection.getInputStream())
			println finalresp
		}
		else{
			String finalresp = getResponse(connection.getErrorStream())
			try{
				String resp = finalresp.substring(finalresp.indexOf("<body><h1>")+"<body><h1>".length(), finalresp.indexOf("</h1>"))
				println resp.split("-")[1].trim()
			}
			catch(Exception e){
				println finalresp
			}
		}
	}

	private static String getResponse(InputStream inputStream){
		BufferedReader buf = new BufferedReader(new InputStreamReader(inputStream))
		StringBuilder build = new StringBuilder()
		String x = null
		while( (x = buf.readLine())!= null){
			build.append(x).append("\n")
		}
		buf.close()
		String finalresp = build.toString()
		finalresp
	}

	private static void loadServerConfiguration(){
		try{
			def resource = Holders.grailsApplication.parentContext.getResource(CONFIG_FILE)
			if(resource?.file){
				props = new Properties()
				props.load(resource?.inputStream)
			}
		}
		catch(Exception e){
			println e.message
		}

	}
}
