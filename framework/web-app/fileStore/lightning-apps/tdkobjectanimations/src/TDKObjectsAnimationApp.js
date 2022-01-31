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

  AnimateObjByLinearMotion(i){
     this._objAnimation = this.tag(this.object+"_"+i).animation({
            duration: 120, repeat: -1, stopMethod: 'immediate',
            actions: [
                     {p: 'x', v: {0: 100,0.1: 800,0.2: 1500,0.3: 1500,0.4: 1500,0.5: 800,0.6:300,0.7:300,0.8:600,0.9:900,1:1200}},
                     {p: 'y', v: {0: 100,0.1: 100,0.2: 100, 0.3: 300, 0.4: 500, 0.5: 500,0.6:500,0.7:700,0.8:700,0.9:700,1:700}}
                     ]
     });
     this._objAnimation.start();
     this.tag(this.object+"_"+i).visible = true;
  }

  AnimateObjByRotation(i){
     this._objAnimation = this.tag(this.object+"_"+i).animation({
            duration: 2, repeat: -1, stopMethod: 'immediate',
            actions: [{ p: 'rotation', v: { 0: { v: 0, sm: 0 }, 1: { v: -Math.PI * 2, sm: 0 } } }]
     });
     this._objAnimation.start();
     this.tag(this.object+"_"+i).visible = true;
  }


  performSingleObjectAnimation(){
     var i = 1;    //single object id
     this.object = this.objects[0];
     var c = this.colors[this.randomInteger(0,4)]
     this.tag(this.object+"_"+i).w = 100;
     this.tag(this.object+"_"+i).h = 100;
     this.tag(this.object+"_"+i).color = c;
     this.AnimateObjByLinearMotion(i);
  }


  performMultiObjectAnimation(){
      var x,y,c,id,num=0;
      var n1=0,n2=0,n3=0;
      var pos = [0,540,960,1080,1920]
      var qval = [1,((this.quadcount*1)+1),((this.quadcount*2)+1),((this.quadcount*3)+1)]
      if (this.objects.length == 1)
          this.object = this.objects[0];
      for (var i = 1; i<=this.totalcount; i++){
          c = this.colors[this.randomInteger(0,4)]
          if (i <= this.quadcount){
              x = this.randomInteger(pos[0],pos[2])
              y = this.randomInteger(pos[0],pos[1])
          }else if (i <= (this.quadcount*2)){
              x = this.randomInteger(pos[2],pos[4])
              y = this.randomInteger(pos[0],pos[1])
          }else if (i <= (this.quadcount*3)){
              x = this.randomInteger(pos[0],pos[2])
              y = this.randomInteger(pos[1],pos[3])
          }else{
              x = this.randomInteger(pos[2],pos[4])
              y = this.randomInteger(pos[1],pos[3])
          }
          if (this.objects.length != 1){
              if (qval.includes(i)){
                  num = 1       // moving to next quadrant
              }else{
                  num = num + 1 // remain in same quadrant
              }
              if(num <= this.splitcount){
                  n1 += 1;
                  id = n1;
                  this.object = this.objects[0];
              }else if(num <= (this.splitcount*2)){
                  n2 += 1;
                  id = n2;
                  this.object = this.objects[1];
              }else{
                  n3 += 1;
                  id = n3;
                  this.object = this.objects[(this.objects.length-1)];
              }
          }else{
              id = i;
          }
          this.tag(this.object+"_"+id).x = x
          this.tag(this.object+"_"+id).y = y
          if (this.object == "Rect" || this.object == "Text"){
              this.tag(this.object+"_"+id).color = c
          }
          this.AnimateObjByRotation(id);
      }
      if (this.objects.length == 1)
          logMsg("animatecount {"+this.objects[0]+":"+id+"}");
      else if(this.objects.length == 3)
          logMsg("animatecount {"+this.objects[0]+":"+n1+","+this.objects[1]+":"+n2+","+this.objects[2]+":"+n3+"}");
      else
          logMsg("animatecount {"+this.objects[0]+":"+n1+","+this.objects[1]+":"+(n2+n3)+"}");
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
    // Using device local host IP
    this.deviceIP   = "127.0.0.1"
    this.devicePort = GetURLParameter("port");
    this.objects    = GetURLParameter("object").split(",")
    this.showfps    = GetURLParameter("showfps")
    this.totalcount = parseInt(GetURLParameter("count"))
    this.duration   = parseInt(GetURLParameter("duration"))
    this.quadcount  = Math.floor(this.totalcount/4);
    this.splitcount = 0
    this.colors     = [0xffff00ff,0xff00ffff,0xFF0034DD,0xFF24DD00,0xFFFF0000]

    // Required device IP and Port to communicate with
    // RDK services plugins using ThunderJS
    this.config = {
        host: this.deviceIP,
        port: this.devicePort
    };
    this.settings = {
        consumer:this,
        fpsholder:"MsgBox"
    };

    this.tag("RDKServices").updateSettings(this.config,this.settings);
    this.tag("RDKServices").rdkservicesInterfaceInit();

    // Checking input elements and calculating how many child objects
    // has to be created for each element to get the total count
    this.object      = ""
    this.objectcount = {}
    if (this.objects.length == 1){
        this.objectcount[this.objects[0]] = this.totalcount
    }else{
        this.splitcount = Math.floor(this.quadcount/this.objects.length);
        var balancecount = (this.totalcount - ((this.objects.length - 1)*(this.splitcount*4)))
        for (var n=0; n < (this.objects.length-1); n++){
            this.objectcount[this.objects[n]] = (this.splitcount*4)
        }
        this.objectcount[this.objects[this.objects.length-1]] = balancecount
    }
    //console.log("objectcount:",this.objectcount);

    //creating N child image objects
    logMsg("******* Creating Child " + this.objects + " objects *******")
    for (var n=0; n < this.objects.length; n++){
      if (this.objects[n] == "Rect"){
        for (var i = 1; i <= this.objectcount[this.objects[n]]; i++){
            this.tag("Background").childList.a({
                                   ref:"Rect_" + i,
                                   rect: true,
                                   w:50,h:50,
                                   visible:false
            });
        }
      }else if(this.objects[n] == "Text"){
        var data = GetURLParameter("text")
        for (var i = 1; i <= this.objectcount[this.objects[n]]; i++){
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
      }else if (this.objects[n] == "Image"){
        for (var i = 1; i <= this.objectcount[this.objects[n]]; i++){
            this.tag("Background").childList.a({
                               ref:"Image_" + i,
                               src:Utils.asset('testimages/penrose-3163507.png'),
                               w:50,h:50,
                               x:50,y:50,visible:false
            });
        }
      }
    }
    logMsg("******* Child "+ this.objects +" objects created *******")

    if (this.showfps == "false"){
        this.tag("MsgBox").visible = false;
    }else{
        this.tag("MsgBox").visible = true;
    }
    this.startDiagnosis();
    if (this.autotest == "true"){
        logMsg("********************** STARTING AUTO TEST ***********************")
        if (this.totalcount == 1){
            this.performSingleObjectAnimation();
        }else{
            this.performMultiObjectAnimation();
        }
        setTimeout(() => {
          this.tag("RDKServices").getAverageDiagnosticsInfo();
          logMsg("TEST COMPLETED")
        },(this.duration*1000)+1000);
    }
  }
}


