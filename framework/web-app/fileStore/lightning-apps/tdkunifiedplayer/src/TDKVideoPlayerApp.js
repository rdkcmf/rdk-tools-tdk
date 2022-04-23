/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2021 RDK Management
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

import { Lightning, Utils, Log, Metrics, VideoPlayer} from '@lightningjs/sdk'
import { dispTime, logMsg, logEventMsg, GetURLParameter, getVideoOperations, getPosValResult } from './MediaUtility.js'
import VideoPlayerAdvanced from './VideoPlayerAdvanced'
import { RDKServicesInterface }  from './RDKServicesUtility';

export default class App extends Lightning.Component {
  static getFonts() {
    return [{ family: 'Regular', url: Utils.asset('fonts/Roboto-Regular.ttf') }]
  }

  static _template() {
    return {
      TDKLogo: {
        mountX: 0.5,
        mountY: 0.5,
        x: 500,
        y: 60,
        h: 70,
        w: 200,
        src: Utils.asset('images/TDK_logo.png'),
      },
      TDKTitle: {
        mount: 0.5,
        x: 1000,
        y: 60,
        text: {
          text: "TDK Lightning Player Test App",
          fontFace: 'bold',
          fontSize: 40,
          textColor: 0xffffffff,
        },
      },
      MsgBox1: {
        x: 100,
        y: 1000,
        w: 800,
        text: {
          fontFace: 'bold',
          fontSize: 30,
          textColor: 0xffffffff,
        },
      },
      MsgBox2: {
        x: 1200,
        y: 1000,
        w: 500,
        text: {
          fontFace: 'bold',
          fontSize: 30,
          textColor: 0xffffffff,
        },
      },
      VideoPlayer: { type: VideoPlayerAdvanced },
      RDKServices : { type: RDKServicesInterface }
    }
  }


  // To display Events & Video position in UI
  dispUIMessage(msg){
      this.tag("MsgBox1").text.text = `Evt: ${msg}`;
  }
  dispUIVideoPosition(msg){
      this.tag("MsgBox2").text.text = `${msg}`;
  }



  /* Methods to perform video playback/trickplay */

  // Methods to perform play / pause operations
  play(){
    this.expectedEvents = ["play"]
    logMsg("Expected Event: " + this.expectedEvents)
    VideoPlayer._videoEl.playbackRate = 1
    VideoPlayer.play(this.videoURL)
  }
  pause() {
    this.expectedEvents = ["paused"]
    logMsg("Expected Event: " + this.expectedEvents)
    this.pos_zero_index_flag = 1
    VideoPlayer.pause()
  }
  playPause(){
    if (VideoPlayer.playing){
        this.expectedEvents = ["paused"]
        this.pos_zero_index_flag = 1
    }else{
        this.expectedEvents = ["play"]
        VideoPlayer._videoEl.playbackRate = 1
    }
    logMsg("Expected Event: " + this.expectedEvents)
    VideoPlayer.playPause()
  }
  playNow(){
    this.playbackRateIndex = this.playbackSpeeds.indexOf(1)
    this.rate = this.playbackSpeeds[this.playbackRateIndex]
    this.expectedEvents = ["ratechange"]
    this.expectedRate   = this.rate
    this.observedRates  = []
    logMsg("Expected Event: " + this.expectedEvents)
    logMsg("Expected Rate : " + this.expectedRate)
    VideoPlayer._videoEl.playbackRate = this.rate
  }

  //  Methods to change video volume (mute/unmute)
  mute(){
    this.expectedEvents = ["volumechange"]
    this.expectedMute   = true
    logMsg("Expected Event: " + this.expectedEvents)
    logMsg("Expected Mute : " + this.expectedMute)
    VideoPlayer.mute()
  }
  unmute(){
    this.expectedEvents = ["volumechange"]
    this.expectedMute   = false
    logMsg("Expected Event: " + this.expectedEvents)
    logMsg("Expected Mute : " + this.expectedMute)
    VideoPlayer.mute(false)
  }


  // Methods to change video position
  seekfwd(pos){
    this.expectedEvents   = ["seeking","seeked"]
    this.expectedPos = VideoPlayer.currentTime + pos
    logMsg("Expected Event: "   + this.expectedEvents)
    logMsg("Expected Pos  : [ " + (this.expectedPos).toFixed(2) + " - " + (this.expectedPos + 7).toFixed(2) + " ]")
    this.videoEl.currentTime += pos
  }
  seekbwd(pos){
    this.expectedEvents   = ["seeking","seeked"]
    this.expectedPos = VideoPlayer.currentTime - pos
    logMsg("Expected Event: " + this.expectedEvents)
    logMsg("Expected Pos  : [ " + (this.expectedPos).toFixed(2) + " - " + (this.expectedPos+ 7).toFixed(2) + " ]")
    this.videoEl.currentTime -= pos
  }
  seekpos(){
    this.expectedEvents   = ["seeking","seeked"]
    var pos = this.seekPositions[this.seekPosIndex]
    this.seekPosIndex += 1
    this.expectedPos = pos
    logMsg("Expected Event: " + this.expectedEvents)
    logMsg("Expected Pos  : [ " + (this.expectedPos).toFixed(2) + " - " + (this.expectedPos+ 7).toFixed(2) + " ]")
    this.videoEl.currentTime = pos
  }

  // Methods to change video rate
  fastfwd() {
    if (this.playbackRateIndex < this.playbackSpeeds.length - 1) {
      this.playbackRateIndex++
    }
    this.rate = this.playbackSpeeds[this.playbackRateIndex]
    this.expectedEvents = ["ratechange"]
    this.expectedRate   = this.rate
    this.observedRates  = []
    logMsg("Expected Event: " + this.expectedEvents)
    logMsg("Expected Rate : " + this.expectedRate)
    VideoPlayer._videoEl.playbackRate = this.rate
  }
  fastfwdspeed(n){
    this.playbackRateIndex = this.playbackSpeeds.indexOf(n)
    this.rate = this.playbackSpeeds[this.playbackRateIndex]
    this.expectedEvents = ["ratechange"]
    this.expectedRate   = this.rate
    this.observedRates  = []
    logMsg("Expected Event: " + this.expectedEvents)
    logMsg("Expected Rate : " + this.expectedRate)
    VideoPlayer._videoEl.playbackRate = this.rate
  }
  rewind() {
    if (this.playbackRateIndex > 0) {
      this.playbackRateIndex--
    }
    this.rate = this.playbackSpeeds[this.playbackRateIndex]
    this.expectedEvents = ["ratechange"]
    this.expectedRate = this.rate
    logMsg("Expected Event: " + this.expectedEvents)
    logMsg("Expected Rate : " + this.expectedRate)
    VideoPlayer._videoEl.playbackRate = this.rate
  }

  // Methods to set events for EOS,Loop and Reload tests
  setExpPlayBackEvents(){
    this.expectedEvents = ["play","ended"]
    logMsg("Expected Event: " + this.expectedEvents)
    logMsg("Observed Event: " + this.observedEvents)
  }
  setLoopPlayBackEvents(){
    this.expectedEvents = ["playing","ended"]
    logMsg("Expected Event: " + this.expectedEvents)
    VideoPlayer.loop(false)
  }

  reload(url){
    this.expectedEvents = ["playing"]
    logMsg("Expected Event: " + this.expectedEvents)
    this.videoURL = this.secondaryURL;
    this.tag('VideoPlayer').reload(this.videoURL);
  }
  close(){
    logMsg("Closing Video Player...")
    this.tag('VideoPlayer').close()
    this.dispUIMessage("Video Player Closed")
  }


  // Video Player Events
  $videoPlayerEvent(eventName){
    if ( Object.keys(this.vidplayerEvents).includes(eventName)){
        this.message1 = "Video Player " + this.vidplayerEvents[eventName]
        this.dispUIMessage(this.message1)
        logMsg(this.message1 + " !!!")
        if (eventName == "Error")
            this.errorFlag = 1
    }
  }
  $videoPlayerTimeUpdate() {
    this.timeUpdateEventHandler()
  }
  $videoPlayerPlaying(){
    this.playingEventHandler()
  }
  $videoPlayerPlay(){
    this.playEventHandler()
  }
  $videoPlayerPause(){
    this.pauseEventHandler()
  }
  $videoPlayerVolumeChange(){
    this.volumeChangeEventHandler()
  }
  $videoPlayerSeeking() {
    this.seekEventHandler("seeking")
  }
  $videoPlayerSeeked() {
    this.seekEventHandler("seeked")
  }
  $videoPlayerRatechange(){
    this.rateChangeEventHandler()
  }
  $videoPlayerEnded(){
    this.endedEventHandler()
  }



  //Register video events
  registerEvents(){
      Object.keys(this.vidElementEvents).forEach(event => {
          this.videoEl.addEventListener(event, () => {
              this.message1 = "Video Player " + this.vidElementEvents[event];
              logMsg(this.message1 + " !!!")
              if ( event == "error")
                this.errorFlag = 1
          });
      });

     this.videoEl.addEventListener("playing", () => {
         this.playingEventHandler()
     });
     this.videoEl.addEventListener("play", () => {
         this.playEventHandler()
     });
     this.videoEl.addEventListener("pause", () => {
         this.pauseEventHandler()
     });
     this.videoEl.addEventListener("volumechange", () => {
         this.volumeChangeEventHandler()
     });
     this.videoEl.addEventListener("seeking", () => {
         this.seekEventHandler("seeking")
     });
     this.videoEl.addEventListener("seeked", () => {
         this.seekEventHandler("seeked")
     });
     this.videoEl.addEventListener("ratechange", () => {
         this.rateChangeEventHandler()
     });
     this.videoEl.addEventListener("timeupdate", () => {
         this.timeUpdateEventHandler();
     });
     this.videoEl.addEventListener("ended", () => {
         this.endedEventHandler();
     });
  }



  // Video progress Event handler
  // Below are the event handler methods for video operations

  // Playing Event Handler
  playingEventHandler(){
    this.observedEvents.push("playing")
    this.message1 = "Video Player Playing"
    this.dispUIMessage(this.message1)
    this.checkAndLogEvents("playing",this.message1 + " !!!")
    if ( this.init == 0 ){
        logMsg("******************* VIDEO STARTED PLAYING !!! *******************")
        logMsg("VIDEO LOOP: " + VideoPlayer.looped)
        logMsg("VIDEO AUTOPLAY: " + this.autoplay)
        logMsg("VIDEO DURATION: " + VideoPlayer.duration.toFixed(4))
        this.vidDuration = VideoPlayer.duration.toFixed(2)
        this.checkAndStartAutoTesting()
        this.init = 1 //inited
        this.progressLogger = setInterval(()=>{
            this.dispProgressLog()
        },1000);
    }
    // Enable video progress position validation after playing event
    this.pos_val_flag = 1;
  }

  // TimeUpdate Event handler
  timeUpdateEventHandler(){
    var currentTime = VideoPlayer.currentTime
    var duration = VideoPlayer.duration
    this.message2 = "Pos: " + currentTime.toFixed(2) + "/" + duration.toFixed(2)
    this.dispUIVideoPosition(this.message2)
    this.progressEventMsg = "Video Progressing "  + currentTime.toFixed(2) + "/" + duration.toFixed(2)
  }

  // Play Event Handler
  playEventHandler(){
    this.observedEvents.push("play")
    this.message1 = "Video Player Play"
    this.dispUIMessage(this.message1)
    this.checkAndLogEvents("play",this.message1 + " !!!")
    // Enable video progress pos validation with pos diff 1
    this.updatePosValidationInfo(1)
  }
  // Pause Event Handler
  pauseEventHandler(){
    this.observedEvents.push("paused")
    this.message1 = "Video Player Paused"
    this.dispUIMessage(this.message1)
    this.checkAndLogEvents("paused",this.message1 + " !!!")
    // Enable video progress pos validation with pos diff 0
    if(this.pos_zero_index_flag){
      this.pos_zero_index_flag = 0
      this.updatePosValidationInfo(0)
    }
  }
  // VolumeChange Event Handler
  volumeChangeEventHandler(){
    this.observedEvents.push("volumechange")
    this.observedMute = VideoPlayer.muted
    this.message1 = "Video Player Volume Change, Mute Status: " + this.observedMute
    this.dispUIMessage(this.message1)
    this.checkAndLogEvents("volumechange",this.message1)
    // Enable video progress pos validation with pos diff 1
    this.updatePosValidationInfo(1)
  }
  // Seek Event Handler
  seekEventHandler(e){
    this.observedEvents.push(e)
    var currentTime = VideoPlayer.currentTime
    var duration = VideoPlayer.duration
    this.observedPos = currentTime
    this.message1 = "Video Player " + e + " " + currentTime.toFixed(2) + "/" + duration.toFixed(2)
    this.dispUIMessage(this.message1)
    this.checkAndLogEvents(e,this.message1)
    if (e == "seeked")
      this.updatePosValidationInfo(1)
  }
  // RateChange Event Handler
  rateChangeEventHandler(){
    this.observedEvents.push("ratechange")
    this.observedRate = VideoPlayer._videoEl.playbackRate
    this.observedRates.push(parseInt(this.observedRate))
    this.message1 = "Video Player Rate Change to " + this.observedRate
    this.dispUIMessage(this.message1)
    this.checkAndLogEvents("ratechange",this.message1)
    if (parseInt(this.observedRate) > 0){
        // Enable video progress pos validation with pos diff rate
        // using same rate for 1x,2x,4x
        var rate_index = parseInt(this.observedRate)
        // providing some buffer for 16x
        if (parseInt(this.observedRate) == 16)
          rate_index = 10
      this.updatePosValidationInfo(rate_index)
    }
  }
  endedEventHandler(){
    this.observedEvents.push("ended")
    this.message1 = "Video Player Ended"
    this.dispUIMessage(this.message1)
    logMsg(this.message1 + " !!!")
  }


   // Key press for operations
   // Operations validation steps has to be added
   _handleEnter(){
     this.play()
   }
   _handleShift(){
     this.pause()
   }
   _handleAlt(){
     this.playPause()
   }
   _handleUp(){
     this.seekfwd(this.seekInterval)
   }
   _handleDown(){
     this.seekbwd(this.seekInterval)
   }
   _handleRight(){
     this.fastfwd()
   }
   _handleLeft(){
     this.rewind()
   }


  // Method to open the video player with the video URL
  loadVideoPlayer(){
    if (this.urlType == "hls" && this.usehlslib){
        this.registerEvents();
        this.tag('VideoPlayer').openHls(this.videoURL,this.DRMconfig)
    }else if (this.urlType == "hls" && ! this.usehlslib){
        this.tag('VideoPlayer').open(this.videoURL)
    }else if (this.urlType == "dash" && this.usedashlib){
        this.registerEvents();
        this.tag('VideoPlayer').openDash(this.videoURL,this.DRMconfig)
    }else if (this.urlType == "dash" && ! this.usedashlib){
        this.tag('VideoPlayer').open(this.videoURL)
    }else{
        this.tag('VideoPlayer').open(this.videoURL)
    }

  }

  checkAndStartAutoTesting(){
    if (this.autotest == "true")
    {
      var operationsStr = GetURLParameter("operations")
      var operations = getVideoOperations(operationsStr)
      logMsg("********************** STARTING AUTO TEST ***********************")
      this.performOperations(operations)
    }else{
      logMsg("***************** PRESS KEYS TO DO OPERATIONS ********************")
    }
  }


  performOperations(operations){
      var actionInterval = 0
      var duration = 0, index = 0
      logMsg("Setting up the operations...")
      for (var i = 0; i < operations.length; i++)
      {
          var action = operations[i].split('(')[0];
          if ( action == "seekpos" ){
              duration = parseInt(operations[i].split('(')[1].split(')')[0].split(":")[0]);
              this.seekPositions[index] = parseInt(operations[i].split('(')[1].split(')')[0].split(":")[1]);
              index += 1;
          }else{
              duration = parseInt(operations[i].split('(')[1].split(')')[0]);
          }
          if ( action == "playtillend" )
              actionInterval = actionInterval + (this.interval*parseInt(this.vidDuration)) + 60000;
          else
              actionInterval = actionInterval + (this.interval*duration)

          //logMsg("setting " + action + " at " + actionInterval + " th sec")
            if (action == "pause"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.pause()
                },actionInterval);
            }
            else if (action == "play"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.play()
                },actionInterval);
            }
            else if (action == "playnow"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.playNow()
                },actionInterval);
            }
            else if (action == "switch"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.playPause()
                },actionInterval);
            }
            else if (action == "seekfwd"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.seekfwd(this.seekInterval)
                },actionInterval);
            }
            else if (action == "seekbwd"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.seekbwd(this.seekInterval)
                },actionInterval);
            }
            else if (action == "seekpos"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.seekpos()
                },actionInterval);
            }
            else if (action == "fastfwd"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.fastfwd()
                },actionInterval);
            }
            else if (action == "fastfwd2x" || action == "fastfwd4x" || action == "fastfwd16x"){
                if (action == "fastfwd2x"){
                setTimeout(()=> {
                    this.clearEvents()
                      this.fastfwdspeed(2)
                },actionInterval);
                }else if (action == "fastfwd4x"){
                setTimeout(()=> {
                    this.clearEvents()
                      this.fastfwdspeed(4)
                },actionInterval);
                }else if (action == "fastfwd16x"){
                setTimeout(()=> {
                    this.clearEvents()
                      this.fastfwdspeed(16)
                },actionInterval);
                }
            }
            else if (action == "rewind"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.rewind()
                },actionInterval);
            }
            else if (action == "mute"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.mute()
                },actionInterval);
            }
            else if (action == "unmute"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.unmute()
                },actionInterval);
            }
            else if (action == "changeurl"){
                setTimeout(()=> {
                    this.clearEvents()
                    this.reload(this.secondaryURL);
                },actionInterval);
            }
            else if (action == "playtillend"){
                setTimeout(()=> {
                    this.setExpPlayBackEvents()
                },actionInterval);
            }
            else if (action == "checkloop"){
                setTimeout(()=> {
                    this.setLoopPlayBackEvents()
                },actionInterval);
            }
            else if (action == "close"){
                setTimeout(()=> {
		    this.updatePrevPosValidationResult()
                    logMsg("**************** Going to close ****************")
                    this.close()
                },actionInterval);
            }
            if (action != "close"){
                setTimeout(()=> {
                    this.updateEventFlowFlag();
                },actionInterval+this.checkInterval);
            }
      }
      if (! operations.find(o=> o.includes("close"))){
          setTimeout(()=> {
            this.updatePrevPosValidationResult()
            logMsg("**************** Going to close ****************")
            this.close()
          },(actionInterval+10000));
      }
      setTimeout(()=> {
        this.dispTestResult()
      },(actionInterval+15000));
      //console.log("\n");
  }



  checkAndLogEvents(checkevent,msg){
    if ( this.expectedEvents.includes(checkevent) ){
        logEventMsg(this.observedEvents,msg)
    }else{
        logMsg(msg)
    }
  }
  clearEvents(){
      this.observedEvents = []
      this.expectedEvents = []
      this.updatePrevPosValidationResult()
  }
  updateEventFlowFlag(){
      var Status = "SUCCESS"
      if( ! this.expectedEvents.every(e=> this.observedEvents.indexOf(e) >= 0)){
          this.eventFlowFlag = 0
          Status = "FAILURE"
          logMsg("Failure Reason: Expected events not occurred")
      }
      else{
          if (this.expectedEvents.includes("seeking")){
              var currTime = parseInt(this.observedPos)
              var expTime  = parseInt(this.expectedPos)
              if ( currTime >= expTime && currTime <= (expTime+7) ){
                  logMsg("video seek operation success")
              }else{
                  this.eventFlowFlag = 0
                  Status = "FAILURE"
                  logMsg("video seek operation failure")
                  logMsg("Failure Reason: Seeked pos is not within expected range")
              }
          }
          else if(this.expectedEvents.includes("ratechange")){
              logMsg("Observed Rates: " + this.observedRates)
              if( this.observedRates.includes(this.expectedRate) ){
                logMsg("video rate change operation success")
              }else{
                this.eventFlowFlag = 0
                Status = "FAILURE"
                logMsg("video rate change operation failure")
                logMsg("Failure Reason: Playback rate is not as expected")
              }
           }
          else if(this.expectedEvents.includes("volumechange")){
              var currMute = this.observedMute
              if( currMute == this.expectedMute ){
                logMsg("video volume change operation success")
              }else{
                this.eventFlowFlag = 0
                Status = "FAILURE"
                logMsg("video volume change operation failure")
                logMsg("Failure Reason: Volume mute status is not as expected")
              }
           }
          else if(this.loop_test_flag){
              logMsg("Video Loop Count:" + this.pos_zero_count)
              logMsg("Observed Event: "  + this.observedEvents)
              if(this.pos_zero_count > 0){
                logMsg("video loop playback operation success")
              }else{
                this.eventFlowFlag = 0
                Status = "FAILURE"
                logMsg("video loop playback operation failure")
                logMsg("Failure Reason: Video progress 0 count is not as expected")
              }
           }
           else{
              Status = "SUCCESS"
           }
      }
      logMsg("Test step status: " + Status)
  }

  updatePosValidationInfo(index){
      if (!this.pos_val_flag){
          this.pos_val_flag  = 1
          this.pos_val_index = index
          logMsg("Video pos index set as "+this.pos_val_index+", Capturing video progress pos values ...");
      }
  }
  updatePrevPosValidationResult(){
      this.pos_val_flag = 0
      this.pos_val_result.push(getPosValResult(this.pos_list,this.pos_val_index))
      this.pos_list = [];
  }

  updateRDKServicesInterface(){
    // Required device IP and Port to communicate with
    // RDK services plugins using ThunderJS
    this.deviceconfig = {
        host: this.deviceIP,
        port: this.devicePort
    };
    this.settings = {
        consumer:this,
        webkitinstance:this.webkitInstance
    };
    this.tag("RDKServices").updateSettings(this.deviceconfig,this.settings);
    this.tag("RDKServices").rdkservicesInterfaceInit();
  }

  dispProgressLog(){
      if(this.progressEventMsg != ""){
          // Get the video position value from the progress message
    	  var pos = this.progressEventMsg.split("Video Progressing")[1].trim().split("/")[0]
          // Only for the video loop playback secnario
          if(this.loop_test_flag == 1){
	      // count the video pos 0 which occurred after the end of the video to track the video loops
              if(parseInt(pos) == 0){
                if(this.pos_end_flag){
                    this.pos_end_flag    = 0
                    this.pos_zero_count += 1
                    this.updatePrevPosValidationResult()
                    logMsg("Loop Count: "+this.pos_zero_count+", Video Re-starting....")
                    this.updatePosValidationInfo(1)
	        }
              }
	      // enable flags when the video position is near video duration
              if(parseInt(pos) >= (parseInt(this.vidDuration)-3)){
                  this.pos_end_flag = 1
              }
          }
	  // display the video progress message and capture the video position
          logMsg(this.progressEventMsg)
          if(this.pos_val_flag == 1){
     	      this.pos_list.push(pos)
          }
	  // Get the FPS data only when collect fps option is enabled
          if(this.enable_fps_flag == 1){
              this.tag("RDKServices").getDiagnosticsInfo();
          }
      }
  }

  dispTestResult(){
    clearInterval(this.progressLogger);
    // Check the average FPS if collect fps option is enabled
    if(this.enable_fps_flag == 1){
        var avgFPS = this.tag("RDKServices").getAverageDiagnosticsInfo()
        if ( Math.round(avgFPS) >= this.expectedFPS )
            logMsg("Average FPS >= " + this.expectedFPS)
        else{
            this.errorFlag = 1
            logMsg("Failure Reason: Average FPS < " + this.expectedFPS)
        }
    }
    // display error, events & pos validation results
    logMsg("**************** TEST STATUS ****************")
    if (this.errorFlag == 0)
        logMsg("OVERALL VIDEO PLAYBACK ERROR EVENT STATUS : FALSE")
    else
        logMsg("OVERALL VIDEO PLAYBACK ERROR EVENT STATUS : TRUE")

    var overall_pos_val_status = 1
    if (this.pos_val_result.includes("FAILURE")){
        overall_pos_val_status = 0
        logMsg("OVERALL VIDEO PROGRESS POSITION VALIDATION STATUS : FAILURE")
    }else
        logMsg("OVERALL VIDEO PROGRESS POSITION VALIDATION STATUS : SUCCESS")

    if (this.eventFlowFlag == 1)
        logMsg("OVERALL VIDEO OPERATIONS EVENTS VALIDATION STATUS : SUCCESS")
    else
        logMsg("OVERALL VIDEO OPERATIONS EVENTS VALIDATION STATUS : FAILURE")


    //Generate TEST RESULT based on error, events & pos validation results
    if (this.eventFlowFlag == 1 && this.errorFlag == 0 && overall_pos_val_status == 1)
        logMsg("TEST RESULT: SUCCESS")
    else{
        logMsg("TEST RESULT: FAILURE")
    }
  }


  _init() {

    this.inputs = window.location.search.substring(1).split("&");
    this.videoURL = GetURLParameter("url").replace(/:and:/g,"&").replace(/:eq:/g, "=")
    this.autotest = GetURLParameter("autotest")
    this.urlType  = GetURLParameter("type")
    this.autoplay = true
    this.options  = []
    this.configs  = []
    this.DRMconfig= {}
    this.message1 = ""
    this.message2 = ""
    this.init     = 0
    this.usedashlib = false
    this.usehlslib  = false
    this.interval = 1000
    this.checkInterval= 3000
    this.seekInterval = 10
    this.expectedPos    = 0
    this.observedPos    = 0
    this.expectedRate   = 0
    this.observedRate   = 0
    this.observedRates  = []
    this.expectedMute   = ""
    this.observedMute   = ""
    this.errorFlag      = 0
    this.eventFlowFlag  = 1
    this.observedEvents = []
    this.expectedEvents = []
    this.seekPositions  = []
    this.seekPosIndex   = 0
    this.playbackSpeeds = [1, 2, 4, 16]
    this.playbackRateIndex = this.playbackSpeeds.indexOf(1)
    this.progressEventMsg  = ""
    this.progressLogger    = null
    this.secondaryURL = "";
    this.loop_test_flag = 0
    this.pos_zero_count = 0
    this.pos_end_flag	= 0
    this.pos_val_flag   = 0
    this.pos_val_index  = 1
    this.pos_list       = []
    this.pos_val_result = []
    this.pos_zero_index_flag = 0
    // Using device local host IP
    this.deviceIP        = "127.0.0.1"
    this.devicePort      = 0
    this.expectedFPS     = 0
    this.webkitInstance  = null
    this.enable_fps_flag = 0
    logMsg("URL Info: " + this.videoURL + " - " + this.urlType)

    this.vidElementEvents = {
        "loadstart":"Load Start", "loadeddata":"Loaded Data", "loadedmetadata":"Loaded MetaData",
        "encrypted": "Encrypted", "progress":"Progress", "emptied":"Emptied", "canplay":"CanPlay","durationchange":"Duration Change",
	"canplaythrough":"CanPlay Through", "waiting":"Waiting", "stalled":"Stalled", "error":"Error"
    }
    this.vidplayerEvents = {
        "LoadStart":"Load Start", "LoadedData":"Loaded Data", "LoadedMetadata":"Loaded MetaData",
        "Encrypted": "Encrypted", "Progress":"Progress", "Emptied":"Emptied", "CanPlay":"CanPlay","durationchange":"Duration Change",
	"CanPlayThrough":"CanPlay Through", "Waiting":"Waiting", "Stalled":"Stalled", "Error":"Error"
    }
    this.inputs.forEach(item => {
        if(item.split("=")[0] == "options"){
            this.options = GetURLParameter("options").split(",");
        }
        else if(item.split("=")[0] == "drmconfigs"){
            this.configs = GetURLParameter("drmconfigs").split(",");
        }
    });

    // Set Video Player Properties
    this.tag('VideoPlayer').setConsumer(this);
    VideoPlayer._videoEl.setAttribute('crossOrigin', 'anonymous');
    this.tag('VideoPlayer').updateDimensions(0,1920,1080,0);
    VideoPlayer.show()      // Default visible
    VideoPlayer.mute(false) // Default unmute
    this.videoEl = VideoPlayer._videoEl

    // check options provided in the url and update video properties
    if (! this.options.includes("noautoplay"))
        VideoPlayer._videoEl.autoplay = true
    else
        this.autoplay = false
    if (this.options.includes("loop"))
        VideoPlayer.loop()
    if (this.options.includes("looptest")){
        this.loop_test_flag = 1
        VideoPlayer.loop()
    }
    if (this.options.includes("mute"))
        VideoPlayer.mute()

    this.options.forEach(item => {
      if(item.includes("seekInterval")){
         this.seekInterval = parseInt(item.split('(')[1].split(')')[0]);
      }
      else if(item.includes("checkInterval")){
         this.checkInterval = parseInt(item.split('(')[1].split(')')[0])*1000;
      }
      else if(item.includes("secondaryURL")){
         this.secondaryURL = item.split('(')[1].split(')')[0];
      }
      else if(item.includes("useDashlib")){
         var dashlib = item.split('(')[1].split(')')[0]
         if (dashlib == "yes" || dashlib == "YES")
           this.usedashlib = true;
      }
      else if(item.includes("useHlslib")){
         var hlslib = item.split('(')[1].split(')')[0]
         if (hlslib == "yes" || hlslib == "YES")
           this.usehlslib = true;
      }
      else if(item.includes("collectfps")){
         this.enable_fps_flag = 1
         this.webkitInstance = item.split('(')[1].split(')')[0];
      }
      else if(item.includes("deviceport")){
         this.devicePort = parseInt(item.split('(')[1].split(')')[0]);
      }
      else if(item.includes("expectedfps")){
         this.expectedFPS = parseInt(item.split('(')[1].split(')')[0]);
      }
    });

    // check the DRM options provided in the url and update the configs
    this.license_header = "";
    this.preferred_drm = "";
    this.configs.forEach(item => {
      if(item.includes("headers")){
          this.license_header = String(item.split('(')[1].split(')')[0]);
      }
      else if(item.includes("preferred")){
          this.preferred_drm = String(item.split('(')[1].split(')')[0]);
      }
    });
    this.configs.forEach(item => {
      if((! item.includes("headers"))&&(! item.includes("preferred"))){
          var drm = String(item.split('(')[0]);
          var license_url = String(item.split('(')[1].split(')')[0]);
          license_url = license_url.replace(/:and:/g,"&").replace(/:eq:/g, "=").replace(/:ob:/g,"(").replace(/:cb:/g,")").replace(/:comma:/g,",");
          if(this.urlType == "dash"){
             this.DRMconfig[drm] = {"serverURL":license_url};
             if(this.license_header != ""){
               var header_tag  = this.license_header.split(":")[0];
               var header_info = this.license_header.split(":")[1];
               this.DRMconfig[drm]["httpRequestHeaders"] = {};
               this.DRMconfig[drm]["httpRequestHeaders"][header_tag] = header_info;
             }
             if(drm == this.preferred_drm){
               //by default priority is 0. drm with highest priority value is taken as preferred
               this.DRMconfig[drm]["priority"] = 1;
             }
          }else if(this.urlType == "hls"){
             this.DRMconfig[drm] = license_url;
          }
      }
    });
    //logMsg("DRM info: "+ JSON.stringify(this.DRMconfig));

    if(this.enable_fps_flag)
        this.updateRDKServicesInterface()

    this.loadVideoPlayer();
    this.vidDuration = VideoPlayer.duration;

  }

}

