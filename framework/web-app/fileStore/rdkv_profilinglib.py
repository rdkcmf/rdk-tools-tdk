##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#########################################################################

import json
import time
import sys
import urllib
from rdkv_performancelib import getConfigFileName
from rdkv_performancelib import getDeviceConfigKeyValue

deviceIP=""
devicePort=""
deviceName=""
deviceType=""

#METHODS
#---------------------------------------------------------------
#INITIALIZE THE MODULE
#---------------------------------------------------------------
def init_module(libobj,port,deviceInfo):
    global deviceIP
    global devicePort
    global deviceName
    global deviceType
    deviceIP = libobj.ip;
    devicePort = port
    deviceName = deviceInfo["devicename"]
    deviceType = deviceInfo["boxtype"]
    libObj = libobj


#----------------------------------------------------------------------------
# Read threshold value from the config file and compare with the given metric
#----------------------------------------------------------------------------
def compare_metric_threshold_values(deviceConfigFile,configParam, metricValue):
    result,threshold_limit = getDeviceConfigKeyValue(deviceConfigFile,configParam)
    if result == "SUCCESS":
        print "Threshold limit for the metric: ",threshold_limit
        if str(threshold_limit).strip() != "":
            status = "SUCCESS"
            for value in metricValue:
                if value > float(threshold_limit):
                    status = "FAILURE"
                    break
            return status
        else:
            print "Unable to check the metric.Please update the threshold limits in device config file"
            return "FAILED"
    else:
        print "Unable to read parameter form device config file"
        return "FAILED"


#----------------------------------------------------------------------------
# To query system wide memory details from grafana server for the given test execution ID.
#
# Values queried from grafana
#                Used (in bytes)
#                Buffered (in bytes)
#                Cached (in bytes)
#                Free (in bytes)
#
# Syntax       : rdkv_profiling_collectd_check_system_memory(tmUrl, resultId, deviceConfig, thresholdCheck="true")
#
# Parameters   : tmUrl - Test manager URL
#                resultId - execution ID
#                deviceConfig - DUT config file
#                thresholdcheck - if thresholdcheck is set to true, threshold value will be retrieved from the config file
#                                 and compared against the parameter. Based on comparison,if value is greater than threshold
#                                 then result is set as success/failure.Default value for thresholdcheck is "true"
#
# Return Value : status and REST API response dict in string format
#----------------------------------------------------------------------------

def rdkv_profiling_collectd_check_system_memory(tmUrl, resultId, deviceConfig, thresholdCheck="true"):
    url = tmUrl + '/execution/fetchDataFromGrafana?executionResultId='+str(resultId)+ str("&") + "parameter=memory.memory-used,memory.memory-free,memory.memory-cached,memory.memory-buffered"
    #print url
    result_details = {}
    try:
        response = urllib.urlopen(url).read()
        response=json.loads(response)
        #print "response: ",response
        memory_metric_list = []
        if response != []:
            print "\n********** Metric From GRAFANA **************"
            for params in response:
                # TODO As of now avg value is taken. Need to confirm on this.Validating memory-used as of now, other metrics the threshold value will vary
                if "memory-used" in params.get("parameter"):
                    memory_metric_list.append(float(params.get("avg")))
                print "%s : min:%s , max:%s , avg:%s \n" %(params.get("parameter").split(".")[-1],params.get("min"),params.get("max"),params.get("avg"))
            print "********************************************\n"
            if thresholdCheck == "true":
                status = compare_metric_threshold_values(deviceConfig,"PROFILING_SYSTEM_MEM_THRESHOLD",memory_metric_list)
                if status == "SUCCESS":
                    result_details["test_step_status"] = "SUCCESS"
                    print "System wide memory-used metric is within the expected threshold level"
                elif status == "FAILURE":
                    result_details["test_step_status"] = "FAILURE"
                    print "System wide memory-used metric is not within the expected threshold level"
                else:
                    result_details["test_step_status"] = "FAILURE"
                print "[SYSTEM-WIDE MEMORY-USED CHECK STATUS]: %s\n" %(status)
            else:
                result_details["test_step_status"] = "SUCCESS"
            result_details["response"] = response
        else:
            result_details["test_step_status"] = "FAILURE"
            print "Received response: ",response
    except:
        result_details["test_step_status"] = "FAILURE"
        print "Unable to get details from grafana server using REST !!!"
    finally:
        result_details = json.dumps(result_details)
        return result_details


#----------------------------------------------------------------------------
# To query system wide load details from grafana server for the given test execution ID.
#
# Values queried from grafana
#                longterm (%)
#                midterm (%)
#                shortterm (%)
#
# Syntax       : rdkv_profiling_collectd_check_system_loadavg(tmUrl, resultId, deviceConfig, thresholdCheck="true")
#
# Parameters   : tmUrl - Test manager URL
#                resultId - execution ID
#                deviceConfig - DUT config file
#                thresholdcheck - if thresholdcheck is set to true, threshold value will be retrieved from the config file
#                                 and compared against the parameter. Based on comparison,if value is greater than threshold
#                                 then result is set as success/failure.Default value for thresholdcheck is "true"
#
# Return Value : status and REST API response dict in string format
#----------------------------------------------------------------------------

def rdkv_profiling_collectd_check_system_loadavg(tmUrl, resultId, deviceConfig, thresholdCheck="true"):
    url = tmUrl + '/execution/fetchDataFromGrafana?executionResultId='+str(resultId)+str("&")+"parameter=load.load.longterm,load.load.midterm,load.load.shortterm"
    result_details = {}
    try:
        response = urllib.urlopen(url).read()
        response=json.loads(response)
        load_metric_list = []
        if response != []:
            print "\n********** Metric From GRAFANA **************"
            for params in response:
                # TODO As of now avg value is taken. Need to confirm on this. Validating shortterm as of now, other metrics the threshold value will vary
                if "shortterm" in params.get("parameter"):
                    load_metric_list.append(float(params.get("avg")))
                print "%s : min:%s , max:%s , avg:%s \n" %(params.get("parameter").split(".")[-1],params.get("min"),params.get("max"),params.get("avg"))
            print "********************************************\n"
            if thresholdCheck == "true":
                status = compare_metric_threshold_values(deviceConfig,"PROFILING_SYSTEM_LOAD_THRESHOLD",load_metric_list)
                if status == "SUCCESS":
                    result_details["test_step_status"] = "SUCCESS"
                    print "System wide load shortterm metric is within the expected threshold level"
                elif status == "FAILURE":
                    result_details["test_step_status"] = "FAILURE"
                    print "System wide load shortterm metric is not within the expected threshold level"
                else:
                    result_details["test_step_status"] = "FAILURE"
                print "[SYSTEM-WIDE LOAD SHORTTERM CHECK STATUS]: %s\n" %(status)
            else:
                result_details["test_step_status"] = "SUCCESS"
            result_details["response"] = response
        else:
            result_details["test_step_status"] = "FAILURE"
            print "Received response: ",response
    except:
        result_details["test_step_status"] = "FAILURE"
        print "Unable to get details from grafana server using REST !!!"
    finally:
        result_details = json.dumps(result_details)
        return result_details


#----------------------------------------------------------------------------
# To query system wide CPU detail from grafana server for the given test execution ID.
#
# Values queried from grafana
#                cpu percent-active (%)
#
# Syntax       : rdkv_profiling_collectd_check_system_CPU(tmUrl, resultId, deviceConfig, thresholdCheck="true")
#
# Parameters   : tmUrl - Test manager URL
#                resultId - execution ID
#                deviceConfig - DUT config file
#                thresholdcheck - if thresholdcheck is set to true, threshold value will be retrieved from the config file
#                                 and compared against the parameter. Based on comparison,if value is greater than threshold
#                                 then result is set as success/failure.Default value for thresholdcheck is "true"
#
# Return Value : status and REST API response dict in string format
#----------------------------------------------------------------------------

def rdkv_profiling_collectd_check_system_CPU(tmUrl, resultId, deviceConfig, thresholdCheck="true"):
    url = tmUrl + '/execution/fetchDataFromGrafana?executionResultId='+str(resultId)+str("&")+"parameter=cpu.percent-active"
    result_details = {}
    try:
        response = urllib.urlopen(url).read()
        response=json.loads(response)
        cpu_metric_list = []
        if response != []:
            print "\n********** Metric From GRAFANA **************"
            for params in response:
                # TODO As of now avg value is taken. Need to confirm on this
                cpu_metric_list.append(float(params.get("avg")))
                print "%s : min:%s , max:%s , avg:%s \n" %(params.get("parameter").split(".")[-1],params.get("min"),params.get("max"),params.get("avg"))
            print "********************************************\n"
            if thresholdCheck == "true":
                status = compare_metric_threshold_values(deviceConfig,"PROFILING_SYSTEM_CPU_THRESHOLD",cpu_metric_list)
                if status == "SUCCESS":
                    result_details["test_step_status"] = "SUCCESS"
                    print "System wide cpu metric is within the expected threshold level"
                elif status == "FAILURE":
                    result_details["test_step_status"] = "FAILURE"
                    print "System wide cpu metric is not within the expected threshold level"
                else:
                    result_details["test_step_status"] = "FAILURE"
                print "[SYSTEM-WIDE CPU CHECK STATUS]: %s\n" %(status)
            else:
                result_details["test_step_status"] = "SUCCESS"
            result_details["response"] = response
        else:
            result_details["test_step_status"] = "FAILURE"
            print "Received response: ",response
    except:
        result_details["test_step_status"] = "FAILURE"
        print "Unable to get details from grafana server using REST !!!"
    finally:
        result_details = json.dumps(result_details)
        return result_details



#----------------------------------------------------------------------------
# To query process wise metrics from grafana server for the given test execution ID.
#
# Values queried from grafana
#                ps_rss (in bytes)
#                ps_vm (in bytes)
#
# Syntax       : rdkv_profiling_collectd_check_process_metrics(tmUrl, resultId, processName, deviceConfig, thresholdCheck="true")
#
# Parameters   : tmUrl - Test manager URL
#                resultId - execution ID
#                processName - name of the process for which details has to be queried
#                deviceConfig - DUT config file
#                thresholdcheck - if thresholdcheck is set to true, threshold value will be retrieved from the config file
#                                 and compared against the parameter. Based on comparison,if value is greater than threshold
#                                 then result is set as success/failure.Default value for thresholdcheck is "true"
#
# Return Value : status and REST API response dict in string format
#----------------------------------------------------------------------------

def rdkv_profiling_collectd_check_process_metrics(tmUrl, resultId, processName, deviceConfig, thresholdCheck="true"):
    url_param = str("&")+"parameter=processes-"+processName+".ps_rss,processes-"+processName+".ps_vm"
    url = tmUrl + '/execution/fetchDataFromGrafana?executionResultId='+str(resultId)+url_param
    result_details = {}
    try:
        response = urllib.urlopen(url).read()
        response=json.loads(response)
        process_metric_list = []
        if response != []:
            print "\n********** Metric From GRAFANA **************"
            print "Process Name: ",processName
            for params in response:
                # TODO As of now avg value is taken. Need to confirm on this
                if "ps_rss" in params.get("parameter"):
                    process_metric_list.append(float(params.get("avg")))
                print "%s : min:%s , max:%s , avg:%s \n" %(params.get("parameter").split(".")[-1],params.get("min"),params.get("max"),params.get("avg"))
            print "********************************************\n"
            if thresholdCheck == "true":
                # TODO: This check will be added for process specific in up coming releases
                status = compare_metric_threshold_values(deviceConfig,"PROFILING_PROCESS_RSS_THRESHOLD",process_metric_list)
                if status == "SUCCESS":
                    result_details["test_step_status"] = "SUCCESS"
                    print "Process rss metric is within the expected threshold level"
                elif status == "FAILURE":
                    result_details["test_step_status"] = "FAILURE"
                    print "Process rss metric is not within the expected threshold level"
                else:
                    result_details["test_step_status"] = "FAILURE"
                print "[%s RSS METRICS CHECK STATUS]: %s\n" %(processName,status)
            else:
                result_details["test_step_status"] = "SUCCESS"
            result_details["response"] = response
        else:
            result_details["test_step_status"] = "FAILURE"
            print "Received response: ",response
    except:
        result_details["test_step_status"] = "FAILURE"
        print "Unable to get details from grafana server using REST !!!"
    finally:
        result_details = json.dumps(result_details)
        return result_details



#----------------------------------------------------------------------------
# To query process wise cpu metric from grafana server for the given test execution ID.
#
# Values queried from grafana
#                used CPU (%)
#
# Syntax       : rdkv_profiling_collectd_check_process_usedCPU(tmUrl, resultId, processName, deviceConfig, thresholdCheck="true")
#
# Parameters   : tmUrl - Test manager URL
#                resultId - execution ID
#                processName - name of the process for which details has to be queried
#                deviceConfig - DUT config file
#                thresholdcheck - if thresholdcheck is set to true, threshold value will be retrieved from the config file
#                                 and compared against the parameter. Based on comparison, if value is greater than threshold
#                                 then result is set as success/failure.Default value for thresholdcheck is "true"
#
# Return Value : status and REST API response dict in string format
#----------------------------------------------------------------------------
def rdkv_profiling_collectd_check_process_usedCPU(tmUrl, resultId, processName, deviceConfig, thresholdCheck="true"):
    url_param = str("&") + "parameter=exec-"+processName+".gauge-"+processName+"_UsedCPU"
    url = tmUrl + '/execution/fetchDataFromGrafana?executionResultId='+str(resultId)+url_param
    result_details = {}
    try:
        response = urllib.urlopen(url).read()
        response=json.loads(response)
        process_metric_list = []
        if response != []:
            print "\n********** Metric From GRAFANA **************"
            print "Process Name: ",processName
            for params in response:
                # TODO As of now avg value is taken. Need to confirm on this
                process_metric_list.append(float(params.get("avg")))
                print "%s : min:%s , max:%s , avg:%s \n" %(params.get("parameter").split(".")[-1],params.get("min"),params.get("max"),params.get("avg"))
            print "********************************************\n"
            if thresholdCheck == "true":
                status = compare_metric_threshold_values(deviceConfig,"PROFILING_PROCESS_CPU_THRESHOLD",process_metric_list)
                if status == "SUCCESS":
                    result_details["test_step_status"] = "SUCCESS"
                    print "Process used CPU metric is within the expected threshold level"
                elif status == "FAILURE":
                    result_details["test_step_status"] = "FAILURE"
                    print "Process used CPU metric is not within the expected threshold level"
                else:
                    result_details["test_step_status"] = "FAILURE"
                print "[%s CPU METRICS CHECK STATUS]: %s\n" %(processName,status)
            else:
                result_details["test_step_status"] = "SUCCESS"
            result_details["response"] = response
        else:
            result_details["test_step_status"] = "FAILURE"
            print "Received response: ",response
    except:
        result_details["test_step_status"] = "FAILURE"
        print "Unable to get details from grafana server using REST !!!"
    finally:
        result_details = json.dumps(result_details)
        return result_details



#----------------------------------------------------------------------------
# To query process wise shared memory metric from grafana server for the given test execution ID.
#
# Values queried from grafana
#                used SHR (in Bytes)
#
# Syntax       : rdkv_profiling_collectd_check_process_usedSHR(tmUrl, resultId, processName, deviceConfig, thresholdCheck="false")
#
# Parameters   : tmUrl - Test manager URL
#                resultId - execution ID
#                processName - name of the process for which details has to be queried
#                deviceConfig - DUT config file
#                thresholdcheck - if thresholdcheck is set to true, threshold value will be retrieved from the config file
#                                 and compared against the parameter. Based on comparison, if value is greater than threshold
#                                 then result is set as success/failure.Default value for thresholdcheck is "false"
#
# Return Value : status and REST API response dict in string format
#----------------------------------------------------------------------------

def rdkv_profiling_collectd_check_process_usedSHR(tmUrl, resultId, processName, deviceConfig, thresholdCheck="false"):
    url_param = str("&") + "parameter=exec-"+processName+".counter-"+processName+"_UsedSHR"
    url = tmUrl + '/execution/fetchDataFromGrafana?executionResultId='+str(resultId)+url_param
    result_details = {}
    try:
        response = urllib.urlopen(url).read()
        response=json.loads(response)
        process_metric_list = []
        if response != []:
            print "\n********** Metric From GRAFANA **************"
            print "Process Name: ",processName
            for params in response:
                # TODO As of now avg value is taken. Need to confirm on this
                process_metric_list.append(float(params.get("avg")))
                print "%s : min:%s , max:%s , avg:%s \n" %(params.get("parameter").split(".")[-1],params.get("min"),params.get("max"),params.get("avg"))
            print "********************************************\n"
            # TODO As of now SHR memory validation is disabled. Need to confirm on this
            if thresholdCheck == "true":
                status = compare_metric_threshold_values(deviceConfig,"PROFILING_PROCESS_SHR_THRESHOLD",process_metric_list)
                if status == "SUCCESS":
                    result_details["test_step_status"] = "SUCCESS"
                    print "Process used SHR metric is within the expected threshold level"
                elif status == "FAILURE":
                    result_details["test_step_status"] = "FAILURE"
                    print "Process used SHR metric is not within the expected threshold level"
                else:
                    result_details["test_step_status"] = "FAILURE"
                print "[%s SHR METRICS CHECK STATUS]: %s\n" %(processName,status)
            else:
                result_details["test_step_status"] = "SUCCESS"
            result_details["response"] = response
        else:
            result_details["test_step_status"] = "FAILURE"
            print "Received response: ",response
    except:
        result_details["test_step_status"] = "FAILURE"
        print "Unable to get details from grafana server using REST !!!"
    finally:
        result_details = json.dumps(result_details)
        return result_details


