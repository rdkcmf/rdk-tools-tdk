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
import { dispTime, logMsg, logEventMsg, GetURLParameter, getVideoOperations } from './MediaUtility.js'
import VideoPlayerAdvanced from './VideoPlayerAdvanced'

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
      VideoPlayer: { type: VideoPlayerAdvanced }
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
    VideoPlayer.pause()
  }
  playPause(){
    if (VideoPlayer.playing){
        this.expectedEvents = ["paused"]
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
    VideoPlayer.skip(pos)
  }
  seekbwd(pos){
    this.expectedEvents   = ["seeking","seeked"]
    this.expectedPos = VideoPlayer.currentTime - pos
    logMsg("Expected Event: " + this.expectedEvents)
    logMsg("Expected Pos  : [ " + (this.expectedPos).toFixed(2) + " - " + (this.expectedPos+ 7).toFixed(2) + " ]")
    VideoPlayer.skip(-pos)
  }
  seekpos(pos){
    this.expectedEvents   = ["seeking","seeked"]
    this.expectedPos = pos
    logMsg("Expected Event: " + this.expectedEvents)
    logMsg("Expected Pos  : [ " + (this.expectedPos).toFixed(2) + " - " + (this.expectedPos+ 7).toFixed(2) + " ]")
    VideoPlayer.seek(pos)
  }

  // Methods to change video rate
  fastfwd() {
    if (this.playbackRateIndex < this.playbackSpeeds.length - 1) {
      this.playbackRateIndex++
    }
    this.rate = this.playbackSpeeds[this.playbackRateIndex]
    this.expectedEvents = ["ratechange"]
    this.expectedRate   = this.rate
    logMsg("Expected Event: " + this.expectedEvents)
    logMsg("Expected Rate : " + this.expectedRate)
    VideoPlayer._videoEl.playbackRate = this.rate
  }
  fastfwdspeed(n){
    this.playbackRateIndex = this.playbackSpeeds.indexOf(n)
    this.rate = this.playbackSpeeds[this.playbackRateIndex]
    this.expectedEvents = ["ratechange"]
    this.expectedRate   = this.rate
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
  setExpPlayBackEvents(){
    this.expectedEvents = ["play","ended"]
    logMsg("Expected Event: " + this.expectedEvents)
    logMsg("Observed Event: " + this.observedEvents)
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
  $videoPlayerProgress() {
    this.progressEventHandler()
  }
  $videoPlayerTimeUpdate() {
    this.timeUpdateEventHandler()
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
              if ( event == "ended")
                this.errorFlag = 1
          });
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
     this.videoEl.addEventListener("progress", () => {
         this.progressEventHandler();
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

  // Progress Event Handler
  progressEventHandler(){
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
  }
  // Pause Event Handler
  pauseEventHandler(){
    this.observedEvents.push("paused")
    this.message1 = "Video Player Paused"
    this.dispUIMessage(this.message1)
    this.checkAndLogEvents("paused",this.message1 + " !!!")
  }
  // VolumeChange Event Handler
  volumeChangeEventHandler(){
    this.observedEvents.push("volumechange")
    this.observedMute = VideoPlayer.muted
    this.message1 = "Video Player Volume Change, Mute Status: " + this.observedMute
    this.dispUIMessage(this.message1)
    this.checkAndLogEvents("volumechange",this.message1)
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
    /*if ( e =="seeked" && this.expectedEvents.includes("seeked")){
    setTimeout(()=>{
        this.videoEl.playbackRate = 1
        this.videoEl.play()
    },1000);
    }*/
  }
  // RateChange Event Handler
  rateChangeEventHandler(){
    this.observedEvents.push("ratechange")
    this.observedRate = VideoPlayer._videoEl.playbackRate
    this.message1 = "Video Player Rate Change to " + this.observedRate
    this.dispUIMessage(this.message1)
    this.checkAndLogEvents("ratechange",this.message1)
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
      var duration = 0, position = 0
      logMsg("Setting up the operations...")
      for (var i = 0; i < operations.length; i++)
      {
          var action = operations[i].split('(')[0];
          if ( action == "seekpos" ){
              duration = parseInt(operations[i].split('(')[1].split(')')[0].split(":")[0]);
              position = parseInt(operations[i].split('(')[1].split(')')[0].split(":")[1]);
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
                    this.seekpos(position)
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
            else if (action == "playtillend"){
                setTimeout(()=> {
                    this.setExpPlayBackEvents()
                },actionInterval);
            }
            else if (action == "close"){
                setTimeout(()=> {
                    logMsg("**************** Going to close ****************")
                    this.close()
                },actionInterval);
            }
            if (action != "close"){
                setTimeout(()=> {
                    this.updateEventFlowFlag();
                },actionInterval+this.checkInterval);
            }
            if (action == "seekfwd" || action == "seekbwd" || action == "seekpos"){
                setTimeout(()=> {
                  if (VideoPlayer.playing == false){
                    this.videoEl.playbackRate = 1
                    this.videoEl.play()
                  }
                },actionInterval+this.checkInterval);
            }
      }
      if (! operations.find(o=> o.includes("close"))){
          setTimeout(()=> {
            logMsg("**************** Going to close ****************")
            this.close()
          },(actionInterval+10000));
      }
      setTimeout(()=> {
        this.dispTestResult()
      },(actionInterval+15000));
      console.log("\n");
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
  }
  updateEventFlowFlag(){
      var Status = "SUCCESS"
      if( ! this.expectedEvents.every(e=> this.observedEvents.indexOf(e) >= 0)){
          this.eventFlowFlag = 0
          Status = "FAILURE"
      }
      else{
          if (this.expectedEvents.includes("seeking")){
              var currTime = parseInt(this.observedPos)
              var expTime  = parseInt(this.expectedPos)
              //logMsg("Observed Pos  : " + currTime)
              if ( currTime >= expTime && currTime <= (expTime+7) ){
                  logMsg("video seek operation success")
              }else{
                  this.eventFlowFlag = 0
                  Status = "FAILURE"
                  logMsg("video seek operation failure")
              }
          }
          else if(this.expectedEvents.includes("ratechange")){
              var currRate = parseInt(this.observedRate)
              //logMsg("Observed Rate : " + currRate)
              if( currRate == this.expectedRate ){
                logMsg("video rate change operation success")
              }else{
                this.eventFlowFlag = 0
                Status = "FAILURE"
                logMsg("video rate change operation failure")
              }
           }
          else if(this.expectedEvents.includes("volumechange")){
              var currMute = this.observedMute
              //logMsg("Observed Mute : " + currMute)
              if( currMute == this.expectedMute ){
                logMsg("video volume change operation success")
              }else{
                this.eventFlowFlag = 0
                Status = "FAILURE"
                logMsg("video volume change operation failure")
              }
           }
           else{
              Status = "SUCCESS"
           }
      }
      logMsg("Test step status: " + Status)
      this.clearEvents();
  }

  dispProgressLog(){
      if(this.progressEventMsg != "")
          logMsg(this.progressEventMsg)
  }

  dispTestResult(){
    clearInterval(this.progressLogger);
    if (this.eventFlowFlag == 1 && this.errorFlag == 0)
        logMsg("TEST RESULT: SUCCESS")
    else{
        logMsg("eventFlowFlag: " + this.eventFlowFlag + " errorFlag: " + this.errorFlag)
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
    this.expectedMute   = ""
    this.observedMute   = ""
    this.errorFlag      = 0
    this.eventFlowFlag  = 1
    this.observedEvents = []
    this.expectedEvents = []
    this.playbackSpeeds = [1, 2, 4, 16]
    this.playbackRateIndex = this.playbackSpeeds.indexOf(1)
    this.progressEventMsg  = ""
    this.progressLogger    = null
    logMsg("URL Info: " + this.videoURL + " - " + this.urlType)

    this.vidElementEvents = {
        "loadstart":"Load Start", "loadeddata":"Loaded Data", "loadedmetadata":"Loaded MetaData",
        "encrypted": "Encrypted", "playing":"Playing", "emptied":"Emptied", "durationchange":"Duration Change",
        "canplay":"CanPlay", "canplaythrough":"CanPlay Through", "waiting":"Waiting", "stalled":"Stalled", "error":"Error"
    }
    this.vidplayerEvents = {
        "LoadStart":"Load Start", "LoadedData":"Loaded Data", "LoadedMetadata":"Loaded MetaData",
        "Encrypted": "Encrypted", "Playing":"Playing", "Emptied":"Emptied", "DurationChange":"Duration Change",
        "CanPlay":"CanPlay", "CanPlayThrough":"CanPlay Through", "Waiting":"Waiting", "Stalled":"Stalled", "Error":"Error"
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
    if (this.options.includes("mute"))
        VideoPlayer.mute()

    this.options.forEach(item => {
      if(item.includes("seekInterval")){
         this.seekInterval = parseInt(item.split('(')[1].split(')')[0]);
      }
      else if(item.includes("checkInterval")){
         this.checkInterval = parseInt(item.split('(')[1].split(')')[0])*1000;
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
    });

    // check the DRM options provided in the url and update the configs
    this.license_header = "";
    this.configs.forEach(item => {
      if(item.includes("headers")){
          this.license_header = String(item.split('(')[1].split(')')[0]);
      }
    });
    this.configs.forEach(item => {
      if(! item.includes("headers")){
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
          }else if(this.urlType == "hls"){
             this.DRMconfig[drm] = license_url;
          }
      }
    });
    //logMsg("DRM info: "+ JSON.stringify(this.DRMconfig));

    this.loadVideoPlayer();
    this.vidDuration = VideoPlayer.duration;

  }

}


