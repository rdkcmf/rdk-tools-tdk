##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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
import time
import websocket
import threading
import thread
import requests
import json,ast
import inspect
from datetime import datetime

#-----------------------------------------------------------------------------------------------
#               ***  RDK SERVICES VALIDATION FRAMEWORK SUPPORTING FUNCTIONS ***
#-----------------------------------------------------------------------------------------------

class createEventListener(object):
    def __init__(self,deviceIP,devicePort,events,url,trace):
        self.ip = deviceIP
        self.port = devicePort
        self.events = events
	self.url = url
        self.trace = trace
        thread = threading.Thread(target=self.connect, args=())
        thread.daemon = True
        thread.start()
        self.listen = True
        self.listenflag = False
        self.connStatus = True
        self.eventsbuffer = []
        self.eventsregisterinfo = []
        if not events:
	    self.events = ['{"id":1,"method":"Inspector.enable"}','{"id":22,"method":"Console.enable"}','{"id":23,"method":"Inspector.initialized"}']
	self.firstElement = None
    def getEventsRegisterInfo(self):
        return self.eventsregisterinfo
    def getEventsBuffer(self):
        return self.eventsbuffer
    def clearEventsBuffer(self):
        self.eventsbuffer = []
    def getListenerFlag(self):
        return self.listenflag
    def setListenerFlag(self):
        self.listenflag = True
    def getConnectionStatus(self):
        return self.connStatus
    def getFirstElement(self):
	self.firstElement = self.eventsbuffer[0]

    def connect(self):
        try:
            print "[INFO]: Opening websocket Connection"
            websocket.enableTrace(self.trace)
            websocketConnection = "ws://" + self.ip + ":" + str(self.port) + str(self.url)
            self.ws = websocket.WebSocketApp(websocketConnection,
                                             on_message = self.on_message,
                                             on_error   = self.on_error,
                                             on_close   = self.on_close,
                                             on_open    = self.on_open)
            self.ws.keep_running = True
            print "[INFO]: Start Event Handler..."
            self.ws.run_forever()
        except Exception as e:
            print "\nException Occurred while connecting to target device\n"

    def on_open(self):
        def run(*args):
            registerResponse = ''
            print("[INFO]: Registering Events...")
            for event in self.events:
                count = 0
                if self.trace:
                    print "\n Register Event %s" %(event)
                self.clearEventsBuffer()
                self.ws.send(event)
                while count < 3:
                    if len(self.getEventsBuffer()) == 0:
                        time.sleep(2)
                        count +=1
                    else:
                        break
                if count < 3:
                    registerResponse = json.loads(self.getEventsBuffer().pop(0))
                    if (registerResponse.get("result")) == {} and (json.loads(event).get("id")== registerResponse.get("id")):
                        status = "SUCCESS"
                    else:
                        status = "FAILURE"
                    self.clearEventsBuffer()
                else:
                    status = "FAILURE"
                eventinfo = {}
                eventinfo["method"]  = json.loads(event).get("method")
                eventinfo["status"] = status
                eventinfo["response"] = registerResponse
                self.eventsregisterinfo.append(eventinfo)
            print("[INFO]: Starting Event listener...")
            self.setListenerFlag()
            while self.listen:
                time.sleep(1)
            print ("[INFO]: Stopped Event listener...")
            self.ws.close()
        thread.start_new_thread(run, ())

    def on_message(self,message):
        if ("method" in message) and "client.events" in json.loads(message).get("method"):
            message = str(datetime.utcnow()).split()[1] + '$$$' + message
        elif ("KeyCode" in message) and "KeyCode" in json.loads(message).get("params").get("message").get("text"):
            message = str(datetime.utcnow()).split()[1] + '$$$' + message
        elif ("RepeatCountUpdated" in message) and "count" in json.loads(message).get("params"):
            message = str(datetime.utcnow()).split()[1] + '$$$' + message
        if self.trace:
            print "\n Received Event Response: %s" %(message)
        if "\\" in message:
            message = message.replace("\\","\\\\")
        self.eventsbuffer.append(message)
    def on_error(self,error):
        print(error)
        if "[Errno 111] Connection refused" in str(error):
            self.connStatus = False
    def on_close(self):
        print("[INFO]: Closed websocket Connection")

    def disconnect(self):
        self.listen = False
        self.listenflag = False
