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


import { Lightning, Utils, Log } from '@lightningjs/sdk'
import { dispTime, logMsg, GetURLParameter} from './MediaUtility.js'
import { RDKServicesInterface }  from './RDKServicesUtility';

let tag = this;
export default class App extends Lightning.Component {
  static getFonts() {
    return [{ family: 'Regular', url: Utils.asset('fonts/Roboto-Regular.ttf') }]
  }

  static _template() {
    return {
      Background: {
        w: 1920,
        h: 1080,
        rect: true,
        color: 0xFFFFFFFF
      },
      MsgBox: {
        x: 1300,
        y: 150,
        w: 250,
        text: {
          fontStyle: 'bold',
          fontSize: 30,
          textColor: 0xFF000000,
        }
      },
	  RDKServices : { type: RDKServicesInterface }
    }
  }


  AnimateObjByRotation(i){
     this._objAnimation = this.tag(this.object+"_"+i).animation({
            duration: 2, repeat: -1, stopMethod: 'immediate',
            actions: [{ p: 'rotation', v: { 0: { v: 0, sm: 0 }, 1: { v: -Math.PI * 2, sm: 0 } } }]
     });
     this._objAnimation.start();
     this.tag(this.object+"_"+i).visible = true;
  }

  performObjectAnimation(){
      var x,y,c;
      var pos = [0,540,960,1080,1920]
      for (var i = 1; i<=this.count; i++){
          c = this.colors[this.randomInteger(0,4)]
          if (i <= this.objcount){
              x = this.randomInteger(pos[0],pos[2])
              y = this.randomInteger(pos[0],pos[1])
          }else if (i <= (this.objcount*2)){
              x = this.randomInteger(pos[2],pos[4])
              y = this.randomInteger(pos[0],pos[1])
          }else if (i <= (this.objcount*3)){
              x = this.randomInteger(pos[0],pos[2])
              y = this.randomInteger(pos[1],pos[3])
          }else{
              x = this.randomInteger(pos[2],pos[4])
              y = this.randomInteger(pos[1],pos[3])
          }
          this.tag(this.object+"_"+i).x = x
          this.tag(this.object+"_"+i).y = y
          this.tag(this.object+"_"+i).color = c
          this.AnimateObjByRotation(i);
      }
      logMsg("Objects Animated !!!")
  }

 
  randomInteger(min, max) {
      return Math.floor(Math.random() * (max - min + 1)) + min;
  }
  startDiagnosis(){
     // Method to get diagnostics info for each second
     setInterval(()=> {
         this.tag("RDKServices").getDiagnosticsInfo();
     },1000);
  }

  _init()
  {
    this.autotest   = GetURLParameter("autotest");
    this.deviceIP   = GetURLParameter("ip");
    this.devicePort = GetURLParameter("port");
    this.object     = GetURLParameter("object")
    this.showfps    = GetURLParameter("showfps")
    this.count      = parseInt(GetURLParameter("count"))
    this.duration   = parseInt(GetURLParameter("duration"))
    this.objcount   = Math.floor(this.count/4);
    this.colors     = [0xffff00ff,0xff00ffff,0xFF0034DD,0xFF24DD00,0xFFFF0000]

    // Required device IP and Port to communicate with
    // RDK services plugins using ThunderJS
    this.config = {
        host: this.deviceIP,
        port: this.devicePort
    };
    this.settings = {
        consumer:this,
        fpsholder:"MsgBox",
		showfps:this.showfps,
    };

    this.tag("RDKServices").updateSettings(this.config,this.settings);
    this.tag("RDKServices").rdkservicesInterfaceInit();

    //creating N child image objects
    logMsg("******* Creating Child " + this.object + "objects *******")
    if (this.object == "Rect"){	  
        for (var i = 1; i <= this.count; i++){
            this.tag("Background").childList.a({
                                   ref:"Rect_" + i,
                                   rect: true,
                                   w:50,h:50,
                                   visible:false
            });
        }
    }else if(this.object == "Text"){
	var data = GetURLParameter("text")
        for (var i = 1; i <= this.count; i++){
            this.tag("Background").childList.a({
                                   ref:"Text_" + i,
		                   x:50,y:50,
		                   text: {
                                   fontSize: 25,
                                   text: data,
                                   fontStyle: 'italic bold',
                                   textColor: 0xff00ffff,
                                },visible:false
            });
        }    	    
    }
    logMsg("******* Child "+ this.object +" objects created *******")
    this.startDiagnosis();
    if (this.autotest == "true"){
        logMsg("********************** STARTING AUTO TEST ***********************")
        this.performObjectAnimation();
        setTimeout(() => {
	  this.tag("RDKServices").getAverageDiagnosticsInfo();
          logMsg("TEST COMPLETED")
        },(this.duration*1000)+1000);
    }
  }
}

