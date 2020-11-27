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


import { Lightning, Utils, Log } from '@lightningjs/sdk'
import { dispTime, logMsg, sleep, setDelay, GetURLParameter, getOperations } from './MediaUtility.js'
import { RDKServicesInterface }  from './RDKServicesUtility';


export default class App extends Lightning.Component {
  static getFonts() {
    return [{ family: 'Regular', url: Utils.asset('fonts/Roboto-Regular.ttf') }]
  }

  static _template() {
    return {
      Background: {
        w: 1920,
        h: 1080,
        src: Utils.asset('images/dark-2024127.png'),
      },
      TDKLogo: {
        mountX: 0.5,
        mountY: 0.5,
        x: 650,
        y: 80,
        h: 80,
        src: Utils.asset('images/TDK_logo.png'),
      },
      TDKTitle: {
        mount: 0.5,
        x: 1200,
        y: 80,
        text: {
          text: "TDK Lightning Animation App",
          fontStyle: 'italic bold',
          fontSize: 40,
          textColor: 0xbbffffff,
        }
      },
      Image:{
        x:100, y:700,
        w:200, h:200,
        src:Utils.asset('images/bird-2028367.png'),
      },
      MsgBox1: {
        x: 80,
        y: 150,
        w: 600,
        text: {
          fontStyle: 'bold',
          fontSize: 20,
          textColor: 0xbbffffff,
        }
      },
      MsgBox2: {
        x: 750,
        y: 150,
        w: 200,
        text: {
          fontStyle: 'bold',
          fontSize: 20,
          textColor: 0xbbffffff,
        }
      },
      MsgBox3: {
        x: 1000,
        y: 150,
        w: 200,
        text: {
          fontStyle: 'bold',
          fontSize: 20,
          textColor: 0xbbffffff,
        }
      },
      MsgBox4: {
        x: 1250,
        y: 150,
        w: 150,
        text: {
          fontStyle: 'bold',
          fontSize: 20,
          textColor: 0xbbffffff,
        }
      },
      MsgBox5: {
        x: 1450,
        y: 150,
        w: 150,
        text: {
          fontStyle: 'bold',
          fontSize: 20,
          textColor: 0xbbffffff,
        }
      },
      MsgBox6: {
        x: 1650,
        y: 150,
        w: 200,
        text: {
          fontStyle: 'bold',
          fontSize: 20,
          textColor: 0xbbffffff,
          wordWrapWidth:150
        }
      },
      RDKServices : { type: RDKServicesInterface }
    }
  }


  // To display Events & Video position in UI
  dispUIMessage(msg){
      this.tag("MsgBox1").text.text = `${msg}`;
  }
  dispUIProgress(msg){
      this.tag("MsgBox2").text.text = `${msg}`;
  }
  dispUIStatus(msg){
      this.tag("MsgBox3").text.text = `${msg}`;
  }


  //Animation Functions
  start(){
    this.expectedEvents = ["start","delayEnd"]
    logMsg("Expected Event: " + this.expectedEvents)
    this.imgObjectAnimation.start();
  }
  pause(){
    this.expectedEvents = ["pause"]
    logMsg("Expected Event: " + this.expectedEvents)
    this.imgObjectAnimation.pause();
  }
  play(){
    this.expectedEvents = ["resume"]
    logMsg("Expected Event: " + this.expectedEvents)
    this.imgObjectAnimation.play();
  }
  stop(){
    this.expectedEvents = ["stop","stopDelayEnd","stopFinish"]
    logMsg("Expected Event: " + this.expectedEvents)
    this.imgObjectAnimation.stop();
  }
  replay(){
    this.expectedEvents = ["start","delayEnd"]
    logMsg("Expected Event: " + this.expectedEvents)
    this.imgObjectAnimation.replay();
  }
  stopNow(){
    this.expectedEvents = ["stop","stopFinish"]
    logMsg("Expected Event: " + this.expectedEvents)
    this.imgObjectAnimation.stopNow();
  }
  finish(){
    this.expectedEvents = ["finish"]
    logMsg("Expected Event: " + this.expectedEvents)
    this.imgObjectAnimation.finish();
  }


  checkAndStartAutoTesting(){
    if (this.autotest == "true")
    {
      var operationsStr = GetURLParameter("operations")
      var operations = getOperations(operationsStr)
      logMsg("********************** STARTING AUTO TEST ***********************")
      this.performOperations(operations)
    }else{
      logMsg("***************** PRESS KEYS TO DO OPERATIONS ********************")
    }
  }

   // Key press for operations
   // Operations validation steps has to be added
   _handleEnter(){
    this.expectedEvents = ["resume"]
    logMsg("Expected Event: " + this.expectedEvents)
    this.play()
   }
   _handleShift(){
    this.expectedEvents = ["pause"]
    logMsg("Expected Event: " + this.expectedEvents)
    this.pause()
   }
   _handleAlt(){
    this.expectedEvents = ["stop","stopFinish"]
    logMsg("Expected Event: " + this.expectedEvents)
    this.stopNow()
   }
   _handleUp(){
    this.expectedEvents = ["start","delayEnd"]
    logMsg("Expected Event: " + this.expectedEvents)
    this.start()
   }
   _handleDown(){
    this.expectedEvents = ["stop","stopDelayEnd","stopFinish"]
    logMsg("Expected Event: " + this.expectedEvents)
    this.stop()
   }
   _handleRight(){
    this.expectedEvents = ["finish"]
    logMsg("Expected Event: " + this.expectedEvents)
    this.finish()
   }
   _handleLeft(){
    this.expectedEvents = ["start","delayEnd"]
    logMsg("Expected Event: " + this.expectedEvents)
    this.replay()
   }


  //Auto-testing setting up animation operations
  performOperations(operations){
      var actionInterval = 0
      logMsg("Setting up the operations...")
      for (var i = 0; i < operations.length; i++)
      {
          var action   = operations[i].split('(')[0];
          var duration = parseInt(operations[i].split('(')[1].split(')')[0]);
          actionInterval = actionInterval + (this.interval*duration)

            if (action == "pause"){
                setTimeout(()=> {
                    this.clearObservedEvents()
                    logMsg("**************** Going to pause ****************")
                    this.pause()
                },actionInterval);
            }
            else if (action == "play"){
                setTimeout(()=> {
                    this.clearObservedEvents()
                    logMsg("**************** Going to play *****************")
                    this.play()
                },actionInterval);
            }
            else if (action == "stop"){
                setTimeout(()=> {
                    this.clearObservedEvents()
                    logMsg("*************** Going to stop ***************")
                    this.stop()
                },actionInterval);
            }
            else if (action == "stopNow"){
                setTimeout(()=> {
                    this.clearObservedEvents()
                    logMsg("*************** Going to stopNow ***************")
                    this.stopNow()
                },actionInterval);
            }
            else if (action == "replay"){
                setTimeout(()=> {
                    this.clearObservedEvents()
                    logMsg("*************** Going to replay ***************")
                    this.replay()
                },actionInterval);
            }
            else if (action == "start"){
                setTimeout(()=> {
                    this.clearObservedEvents()
                    logMsg("*************** Going to start ***************")
                    this.start()
                },actionInterval);
            }
            else if (action == "finish"){
                setTimeout(()=> {
                    this.clearObservedEvents()
                    logMsg("*************** Going to finish ***************")
                    this.finish()
                },actionInterval);
            }
            setTimeout(()=> {
                this.updateEventFlowFlag();
            },actionInterval+1000);

      }
      setTimeout(()=> {
        this.dispTestResult()
      },(actionInterval+3000));
      console.log("\n");
  }


  // Auto-testing animation events validation
  clearObservedEvents(){
      this.observedEvents = []
  }
  updateEventFlowFlag(){
      var Status = "SUCCESS"
      logMsg("Observed Event: " + this.observedEvents)
      if( ! this.expectedEvents.some(e=> this.observedEvents.indexOf(e) >= 0)){
          this.eventFlowFlag = 0
          Status = "FAILURE"
      }
      logMsg("Test step status: " + Status)
      this.clearObservedEvents();
  }

  dispTestResult(){
    clearInterval(this.progressLogger);
    this.tag("RDKServices").getAverageDiagnosticsInfo()
    if (this.eventFlowFlag == 1 )
        logMsg("TEST RESULT: SUCCESS")
    else{
        logMsg("eventFlowFlag: " + this.eventFlowFlag)
        logMsg("TEST RESULT: FAILURE")
    }
  }

  dispProgressLog(){
      logMsg(this.progressEventMsg)
  }
  startDiagnosis(){
     // Method to get diagnostics info for each second
     setInterval(()=> {
         this.tag("RDKServices").getDiagnosticsInfo();
     },1000);
  }




  _init()
  {
    this.autotest  = GetURLParameter("autotest");
    this.deviceIP  = GetURLParameter("ip");
    this.devicePort  = GetURLParameter("port");

    this.init     = 0
    this.interval = 1000
    this.eventMsg = ""
    this.repeatCount = 0;
    this.eventFlowFlag  = 1
    this.expectedEvents = []
    this.observedEvents = []
    this.progressEventMsg = ""

    // Required device IP and Port to communicate with
    // RDK services plugins using ThunderJS
    this.config = {
        host: this.deviceIP,
        port: this.devicePort
    };
    this.settings = {
        consumer:this,
        fpsholder:"MsgBox4",
        cpuholder:"MsgBox5",
        memholder:"MsgBox6"
    };

    this.tag("RDKServices").updateSettings(this.config,this.settings);
    this.tag("RDKServices").rdkservicesInterfaceInit();

    // Animating the image object, by providing position vs time parameters
    this.imgObject = this.tag("Image");
    this.imgObjectAnimation = this.tag("Image").animation({
        duration: 8,
        delay: 0.3,
        repeat: -1,
        repeatDelay: 0,
        repeatOffset: 0,
        stopMethod: 'reverse',
        stopDuration: 1,
        stopDelay: 0.2,
        autostop: true,
        actions:[
               {p: 'x',   v: {0: 0,   0.2: 200, 0.4: 450, 0.6: 650, 0.8: 800 , 1: 1200 }},
               {p: 'y',   v: {0: 400, 0.2: 150, 0.4: 400, 0.6: 200, 0.8: 600 , 1: 200  }}
        ]
    });

    this.imgObjectAnimation.start();


    this.progressLogger = setInterval(()=>{
        this.dispProgressLog()
    },1000);


    //Animation Event Handlers
    this.imgObjectAnimation.on('start', () => {
        this.observedEvents.push("start")
        this.eventMsg = "Animation Event : Start, IsPlaying : " + this.imgObjectAnimation.isPlaying();
        this.dispUIMessage(this.eventMsg);
        logMsg(this.eventMsg);
    });
    this.imgObjectAnimation.on('delayEnd', () => {
        this.observedEvents.push("delayEnd")
        this.eventMsg = "Animation Event : DelayEnd";
        this.dispUIMessage(this.eventMsg);
        logMsg(this.eventMsg);
    });
    this.imgObjectAnimation.on('pause', () => {
        this.observedEvents.push("pause")
        var statusMsg = "IsActive : " +  this.imgObjectAnimation.isActive()
        this.eventMsg = "Animation Event : Pause, IsPaused : " + this.imgObjectAnimation.isPaused();
        this.dispUIStatus(statusMsg)
        this.dispUIMessage(this.eventMsg);
        logMsg(this.eventMsg);
    });
    this.imgObjectAnimation.on('resume', () => {
        this.observedEvents.push("resume")
        this.eventMsg = "Animation Event : Resume, IsPlaying : " + this.imgObjectAnimation.isPlaying();
        this.dispUIMessage(this.eventMsg);
        logMsg(this.eventMsg);
    });
    this.imgObjectAnimation.on('progress', (p) => {
        var progressMsg = "Progress : " + p.toFixed(2)
        var statusMsg   = "IsActive : " +  this.imgObjectAnimation.isActive()
        this.eventMsg = progressMsg + " , " + statusMsg
        this.dispUIStatus(statusMsg)
        this.dispUIProgress(progressMsg)
        if ( this.init == 0 ){
            logMsg("******************* IMAGE ANIMATION STARTED !!! *******************")
            logMsg("Animation " + this.eventMsg );
            this.checkAndStartAutoTesting()
            this.init = 1 //inited
            logMsg("Start getting device diagnostics info...")
            this.startDiagnosis();
        }
        this.progressEventMsg = this.eventMsg;

    });
    this.imgObjectAnimation.on('repeat', () => {
        this.repeatCount = this.repeatCount + 1;
        this.eventMsg = "Animation Event : Repeat, Repeat count : " + this.repeatCount;
        this.dispUIMessage(this.eventMsg);
        logMsg(this.eventMsg);
    });
    this.imgObjectAnimation.on('stop', () => {
        this.observedEvents.push("stop")
        var statusMsg   = "IsActive : " +  this.imgObjectAnimation.isActive()
        this.eventMsg = "Animation Event : Stop, IsStopping : " + this.imgObjectAnimation.isStopping();
        this.dispUIStatus(statusMsg)
        this.dispUIMessage(this.eventMsg);
        logMsg(this.eventMsg);
    });
    this.imgObjectAnimation.on('stopDelayEnd', () => {
        this.observedEvents.push("stopDelayEnd")
        var statusMsg   = "IsActive : " +  this.imgObjectAnimation.isActive()
        this.eventMsg = "Animation Event :  StopDelayEnd, IsStopping : " + this.imgObjectAnimation.isStopping();
        this.dispUIStatus(statusMsg)
        this.dispUIMessage(this.eventMsg);
        logMsg(this.eventMsg);
    });
    this.imgObjectAnimation.on('stopContinue', () => {
        this.eventMsg = "Animation Event : StopContinue";
        this.dispUIMessage(this.eventMsg);
        logMsg(this.eventMsg);
    });
    this.imgObjectAnimation.on('stopFinish', () => {
        this.observedEvents.push("stopFinish")
        var statusMsg   = "IsActive : " +  this.imgObjectAnimation.isActive()
        var progressMsg = "Progress : 0"
        this.eventMsg = "Animation Event : StopFinish, animation reversed to starting";
        this.dispUIStatus(statusMsg)
        this.dispUIMessage(this.eventMsg);
        this.dispUIProgress(progressMsg)
        logMsg(this.eventMsg);
    });
    this.imgObjectAnimation.on('finish', () => {
        this.observedEvents.push("finish")
        this.eventMsg = "Animation Event : Finish, finishing image animation"
        this.dispUIMessage(this.eventMsg);
        logMsg(this.eventMsg);
    });

  }

}




