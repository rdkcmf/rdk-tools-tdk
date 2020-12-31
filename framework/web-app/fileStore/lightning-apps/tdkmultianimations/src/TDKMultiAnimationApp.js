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
        src: Utils.asset('testimages/underwater-2797613.png'),
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
          textColor: 0xffffffff,
        }
      },
      MsgBox: {
        x: 80,
        y: 150,
        w: 600,
        text: {
          fontStyle: 'bold',
          fontSize: 30,
          textColor: 0xffffffff,
        }
      },
      MsgBox1: {
        x: 1000,
        y: 150,
        w: 250,
        text: {
          fontStyle: 'bold',
          fontSize: 30,
          textColor: 0xffffffff,
        }
      },
      MsgBox2: {
        x: 1300,
        y: 150,
        w: 250,
        text: {
          fontStyle: 'bold',
          fontSize: 30,
          textColor: 0xffffffff,
        }
      },
      MsgBox3: {
        x: 1600,
        y: 150,
        w: 300,
        text: {
          fontStyle: 'bold',
          fontSize: 30,
          textColor: 0xffffffff,
        }
      },
      RDKServices : { type: RDKServicesInterface }
    }
  }



  /* Below are the function to animate the provided objects in different ways
     (i.e) the movement and size of the objects will vary */

  animatePatternA(i,n,d,t){
       var x=0;
       if ( n <= 10 )
           x = 10
       this.imgObjectAnimation = this.tag("Image_"+i).animation({
           duration: 3+(n*t),
           delay: d,
           repeat: -1,
           repeatDelay: 0,
           repeatOffset: 0,
           stopMethod: 'reverse',
           stopDuration: 1,
           stopDelay: 0.1,
           autostop: true,
           actions:[
                {p: 'x',     v: {0: {v:50-(n*10),se:0}, 0.1: {v:300-(n*10),se:0}, 0.2: {v:300-(n*10),se:0}, 0.3: {v:1500+(n*10),se:0}, 0.4: {v:1500+(n*10),se:0}, 0.5: {v:200+(n*10), se:0}, 0.6: {v:200+(n*10), se:0}, 0.7: {v:1200+(n*10),se:0}, 0.8: {v:1600+(n*10),se:0}, 0.9: {v:1600+(n*10),se:0}, 1:1900-(n*x)}},
                {p: 'y',     v: {0: {v:0+(n*50),se:0},  0.1: {v:0+(n*50),se:0},   0.2: {v:0+(n*50),se:0},   0.3: {v:300 +(n*10),se:0}, 0.4: {v:300 +(n*10),se:0}, 0.5: {v:800+(n*10), se:0}, 0.6: {v:800+(n*10), se:0}, 0.7: {v:400+(n*10),se:0},  0.8: {v:200+(n*10),se:0},  0.9: {v:200+(n*10),se:0},  1:200+(n*10)}},
                {p: 'scale', v: {0: {v:0.5,  se:0}, 0.1:0.8, 0.3: 0.5 , 0.5:0.3,          0.7: 1,        1:0.3}},
                {p: 'scaleX',v: {0: {v:0.5,   s:1}, 0.1:0.8, 0.3: 0.5 , 0.5:{v:-0.3,s:1}, 0.7:{v:1,s:1}, 1:{v:0.3,s:1} }}
           ]
      });
      this.imgObjectAnimation.start();
      this.tag("Image_"+i).visible = true;
  }


  animatePatternB(i,n,d,t){
       var x=0;
       if ( n <= 10 )
           x = 10
       this.imgObjectAnimation = this.tag("Image_"+i).animation({
           duration: 3+(n*t),
           delay: d,
           repeat: -1,
           repeatDelay: 0,
           repeatOffset: 0,
           stopMethod: 'reverse',
           stopDuration: 1,
           stopDelay: 0.1,
           autostop: true,
           actions:[
                {p: 'x',     v: {0: {v:1900+(n*10),se:0}, 0.1: {v:1650+(n*10),se:0}, 0.2: {v:1100+(n*10),se:0}, 0.3: {v:0+(n*10),se:0},   0.4: {v:0+(n*10),se:0} ,  0.5: {v:1200+(n*10), se:0}, 0.6: {v:1200+(n*10), se:0}, 0.7: {v:1550+(n*10),se:0}, 0.8: {v:1550+(n*10),se:0}, 0.9: {v:1650+(n*10),se:0}, 1:1900-(n*x)}},
                {p: 'y',     v: {0: {v:0+(n*50),se:0},    0.1: {v:0+(n*50),se:0},    0.2: {v:0+(n*50),se:0},    0.3: {v:500+(n*10),se:0}, 0.4: {v:500+(n*10),se:0}, 0.5: {v:800+(n*10), se:0},  0.6: {v:800+(n*10), se:0},  0.7: {v:600+(n*10),se:0},  0.8: {v:600+(n*10),se:0},  0.9: {v:600+(n*10),se:0},  1:600+(n*10)}},
                {p: 'scale', v: {0: {v:0.5,  se:0}, 0.1:0.8, 0.3: 0.5 , 0.5:0.3,          0.7: {v:1,   s:1}, 0.8:0.3}},
                {p: 'scaleX',v: {0: {v:0.5,   s:1}, 0.1:0.8, 0.3: 0.5 , 0.5:{v:-0.3,s:1}, 0.7: {v:-1,  s:1}, 0.8:{v:-0.3,s:1} }}
           ]
      });
      this.imgObjectAnimation.start();
      this.tag("Image_"+i).visible = true;
  }


  animatePatternC(i,n,d,t){
       var x=0;
       if ( n <= 10 )
           x = 10
       this.imgObjectAnimation = this.tag("Image_"+i).animation({
           duration: 5+(n*t),
           delay: d,
           repeat: -1,
           repeatDelay: 0,
           repeatOffset: 0,
           stopMethod: 'reverse',
           stopDuration: 1,
           stopDelay: 0,
           autostop: true,
           actions:[
                 {p: 'x',     v: {0: 0+(n*10), 0.1:100+(n*10), 0.2:1200+(n*10), 0.3:800+(n*10), 0.4:800+(n*10), 0.5:600+(n*10), 0.6:600+(n*10), 0.7:600+(n*10), 0.8:200+(n*10), 0.9: 200+(n*10), 1:0+(n*x)}},
                 {p: 'y',     v: {0: 0+(n*50), 0.1:0+(n*50), 0.2:0+(n*50), 0.3:400+(n*10), 0.4:400+(n*10),  0.5:600+(n*10), 0.6:600+(n*10), 0.7:800+(n*10), 0.8:800+(n*10), 0.9: 900+(n*10), 1:900}},
                 {p: 'scale', v: {0: {v:1,  se:0}, 0.3: 0.3         , 0.4: 0.4,          0.5: 0.5,         0.6:0.5,         0.7:0.5, 0.8:1, 0.9:1, 1:0.3}},
                 {p: 'scaleX',v: {0: {v:1,   s:1}, 0.3: {v:-0.3,s:1}, 0.4: {v:-0.4,s:1}, 0.5: {v:-0.5,s:1},0.6:{v:-0.5,s:1},0.7:{v:-0.7,s:1}, 0.8:{v:-1,s:1}, 0.9:{v:-1,s:1}, 1:{v:-0.3,s:1} }}
           ]
       });
       this.imgObjectAnimation.start();
       this.tag("Image_"+i).visible = true;
  }



  animatePatternD(i,n,p,d,t,c,space,size){
       var interval=0,time=0;
       if ( n <= 10 ){
           time = 0.8
           interval = 0.2
       }else if ( n <= 20 ){
           time = 0.5
           interval = 0.1
       }else{
           time = 0.2
           interval = 0.05
       }
       this.imgObjectAnimation = this.tag("Image_"+i).animation({
           duration:t+(n*time),
           delay: d+(n*interval),
           repeat: -1,
           repeatDelay: 0,
           repeatOffset: 0,
           stopMethod: 'immediate',
           stopDuration: 1,
           stopDelay: 0.1,
           autostop: true,
           actions:[
                {p: 'x',     v: {0: {v:-200,se:0},        0.1: {v:200+(n*2)+(p*2),se:0},        0.2: {v:500+(n*2)+(p*2),se:0},       0.3: {v:900+(n*10)+(p*10),se:0},     0.4: {v:1500+(n*5)+(p*2),se:0},      0.5: {v:1200+(n*10)+(p*10),se:0},   0.6: {v:800+(n*10)+(p*10),se:0},     0.7: {v:800+(n*10)+(p*10),se:0},     0.8: {v:400+(n*10)+(p*10),se:0} ,    0.9: {v:200+(n*10)+(p*10),se:0},     1:-200}},
                {p: 'y',     v: {0: {v:0+(c*space),se:0}, 0.1: {v:0+(c*space)+(n*space),se:0},  0.2: {v:0+(c*space)+(n*space),se:0}, 0.3: {v:0+(c*space)+(n*space),se:0}, 0.4: {v:0+(c*space)+(n*space),se:0}, 0.5: {v:+(c*space)+(n*space),se:0}, 0.6: {v:0+(c*space)+(n*space),se:0}, 0.7: {v:0+(c*space)+(n*space),se:0}, 0.8: {v:0+(c*space)+(n*space),se:0}, 0.9: {v:0+(c*space)+(n*space),se:0}, 1:0+(c*space)}},

                {p: 'scale', v: {0: {v:size,  se:0}, 0.2:size+0.1,  0.4: size+0.2 , 0.5:size,          0.6:size,          0.7: size,         0.8: size,         0.9: size,         1:size}},
                {p: 'scaleX',v: {0: {v:size,   s:1}, 0.2:size+0.1,  0.4: size+0.2 , 0.5:{v:-size,s:1}, 0.6:{v:-size,s:1}, 0.7:{v:-size,s:1}, 0.8:{v:-size,s:1}, 0.9:{v:-size,s:1}, 1:{v:-size,s:1}}}
           ]
      });
      this.imgObjectAnimation.start();
      this.tag("Image_"+i).visible = true;
  }


  animatePatternE(i,n,p,d,t,c,space,size){
       var interval=0,time=0;
       if ( n <= 10 ){
           time = 0.8
           interval = 0.2
       }else if ( n <= 20 ){
           time = 0.5
           interval = 0.1
       }else{
           time = 0.2
           interval = 0.05
       }
       this.imgObjectAnimation = this.tag("Image_"+i).animation({
           duration:t+(n*time),
           delay: d+(n*interval),
           repeat: -1,
           repeatDelay: 0,
           repeatOffset: 0,
           stopMethod: 'immediate',
           stopDuration: 1,
           stopDelay: 0.1,
           autostop: true,
           actions:[
                {p: 'x',     v: {0: {v:1900+(n*10),se:0}, 0.1: {v:1500+(n*2)+(p*2),se:0},      0.2: {v:1200+(n*2)+(p*2),se:0},      0.3: {v:600+(n*10)+(p*10),se:0},     0.4: {v:100+(n*5)+(p*10),se:0},      0.5: {v:400+(n*10)+(p*10),se:0},    0.6: {v:1300+(n*10)+(p*10),se:0},    0.7: {v:1300+(n*10)+(p*2),se:0},     0.8: {v:1600+(n*10)+(p*2),se:0} ,    0.9: {v:1900+(n*10)+(p*2),se:0},     1:2000}},
                {p: 'y',     v: {0: {v:0+(c*space),se:0}, 0.1: {v:0+(c*space)+(n*space),se:0}, 0.2: {v:0+(c*space)+(n*space),se:0}, 0.3: {v:0+(c*space)+(n*space),se:0}, 0.4: {v:0+(c*space)+(n*space),se:0}, 0.5: {v:+(c*space)+(n*space),se:0}, 0.6: {v:0+(c*space)+(n*space),se:0}, 0.7: {v:0+(c*space)+(n*space),se:0}, 0.8: {v:0+(c*space)+(n*space),se:0}, 0.9: {v:0+(c*space)+(n*space),se:0}, 1:0+(c*space)}},

                {p: 'scale', v: {0: {v:size,  se:0}, 0.2:size+0.1, 0.4: size+0.2 , 0.5:size,          0.6:size,          0.7: size,         0.8: size,         0.9: size,         1:size}},
                {p: 'scaleX',v: {0: {v:size,   s:1}, 0.2:size+0.1, 0.4: size+0.2 , 0.5:{v:-size,s:1}, 0.6:{v:-size,s:1}, 0.7:{v:-size,s:1}, 0.8:{v:-size,s:1}, 0.9:{v:-size,s:1}, 1:{v:-size,s:1}}}
           ]
      });
      this.imgObjectAnimation.start();
      this.tag("Image_"+i).visible = true;
  }


  /* Below are the functions to define the start delay(d) & animation time(t) for the objects,
     based on total number of objects to be animated. Total number is splitted into segments
     and animation factors values are set differently for each segment. So that each object
     gets random factors to thus movement is random */

  _get_animation_factors_20_Objs(i){
      var t,d;
      if(i % 2 != 0 &&  i <=10 ){
          t = 1
          d = 0.1
      }else if (i % 2 == 0 &&  i <= 10){
          t = 2
          d = 0.3
      }else if (i % 2 != 0 &&  i > 10 ){
          t = 0.5
          d = 0.1
      }else{
          t = 1
          d = 0.3
      }
      return {d,t}
  }

  _get_animation_factors_100_Objs(i){
      var d,t,num,pad;
      if(i % 2 != 0 && i <= 50){
          d = 0.1
          t = 3
          num = this.randomInteger(1,15)
      }else if (i % 2 != 0 && i > 50){
          d = 0.3
          t = 5
          num = this.randomInteger(1,30)
      }else if (i % 2 == 0 && i <= 50){
          d = 0.3
          t = 5
          num = this.randomInteger(1,15)
      }else if (i % 2 == 0 && i > 50){
          d = 0.1
          t = 3
          num = this.randomInteger(1,30)
      }
      pad = this.randomInteger(1,30)
      return {d,t,num,pad}
  }

  _get_animation_factors_500_Objs(i){
      var d,t,num,pad;
      if(i % 2 != 0 && i <= 150){
          t = 3
          d = 0.1
          num = this.randomInteger(1,15)
      }else if (i % 2 == 0 && i <= 150){
          t = 5
          d = 0.3
          num = this.randomInteger(1,30)
      }else if (i % 2 != 0 && i <= 300){
          t = 6
          d = 0.2
          num = this.randomInteger(1,20)
      }else if (i % 2 == 0 && i <= 300){
          t = 3
          d = 0.3
          num = this.randomInteger(1,30)
      }else if (i % 2 != 0 && i <= 400){
          t = 5
          d = 0.1
          num = this.randomInteger(1,15)
      }else if (i % 2 == 0 && i <= 400){
          t = 2
          d = 0.3
          num = this.randomInteger(1,30)
      }else if (i % 2 != 0 && i <= 500){
          t = 6
          d = 0.2
          num = this.randomInteger(1,25)
      }else if (i %2 == 0 && i <= 500) {
          t = 7
          d = 0.1
          num = this.randomInteger(1,15)
      }
      pad = this.randomInteger(1,30)
      return {d,t,num,pad}
  }


  // Funtion to handle Multi object animations
  animateMultiObjects(n){
      logMsg("Going to animate " + n + " object(s)....")
      this.objectsCount = n;
      var data,num1,num2,num3,c,space,size;
      if (n == 1 ){
          this.tag("Image_"+n).src = Utils.asset('testimages/fish-1331816.png')
          this.animatePatternA(n,5,0,2);
      }
     else if ( n == 10 || n == 20){
          num1=2,num2=0,c=0;
          if ( n  == 10)
              c = 5
          else
              c = 10
          for (var i = 1; i <= n; i++){
              this.tag("Image_"+i).visible = false;
              if ( i <= c){
                  num1 += 1;
                  data = this._get_animation_factors_20_Objs(num1)
                  this.tag("Image_"+i).src = Utils.asset('testimages/fish-1331812.png')
                  this.animatePatternA(i,num1,data.d,data.t);
              }else{
                  num2 += 1;
                  data = this._get_animation_factors_20_Objs(num2)
                  this.tag("Image_"+i).src = Utils.asset('testimages/fish-1331813.png')
                  this.animatePatternB(i,num2,data.d,data.t);
              }
          }
      }
      else if (n == 50){
          num1=0,num2=0,num3=0;
          for (var i = 1; i <= n; i++){
              this.tag("Image_"+i).visible = false;
              if ( i <= 15){
                  num1 += 1;
                  data = this._get_animation_factors_20_Objs(num1)
                  this.tag("Image_"+i).src = Utils.asset('testimages/clown-fish-4033036.png')
                  this.animatePatternC(i,num1,data.d,data.t);
              }else if ( i > 15 && i <= 30 ){
                  num2 += 1;
                  data = this._get_animation_factors_20_Objs(num2)
                  this.tag("Image_"+i).src = Utils.asset('testimages/fish-1332205.png')
                  this.animatePatternA(i,num2,data.d,data.t);
              }else{
                  num3 += 1;
                  data = this._get_animation_factors_20_Objs(num3)
                  this.tag("Image_"+i).src = Utils.asset('testimages/fish-1331813.png')
                  this.animatePatternB(i,num3,data.d,data.t);
              }
          }
      }
      else if ( n == 100){
          space=8,size=0.5;
          for (var i = 1; i <= n; i++){
              this.tag("Image_"+i).visible = false;
              data = this._get_animation_factors_100_Objs(i)
              this.tag("Image_"+i).src = Utils.asset('testimages/clown-fish-4033036.png')
              this.animatePatternD(i,data.num,data.pad,data.d,data.t,i,space,size);
          }
      }
      else if ( n == 250){
          space=4,size=0.3;
          for (var i = 1; i <= n; i++){
              this.tag("Image_"+i).visible = false;
              data = this._get_animation_factors_500_Objs(i)
              this.tag("Image_"+i).src = Utils.asset('testimages/fish-1331813.png')
              this.animatePatternE(i,data.num,data.pad,data.d,data.t,i,space,size);
          }
      }
      else if ( n == 500){
          space=1.8,size=0.2;
          for (var i = 1; i <= n; i++){
              this.tag("Image_"+i).visible = false;
              data = this._get_animation_factors_500_Objs(i)
              this.tag("Image_"+i).src = Utils.asset('testimages/clown-fish-4033036.png')
              this.animatePatternD(i,data.num,data.pad,data.d,data.t,i,space,size);
          }
      }
      else if ( n == 1000){
          space=1.8,size=0.2,num1=0,num2=0;
          for (var i = 1; i <= n; i++){
              this.tag("Image_"+i).visible = false;
              if (i <= 500){
                  num1 += 1
                  data = this._get_animation_factors_500_Objs(num1)
                  this.tag("Image_"+i).src = Utils.asset('testimages/clown-fish-4033036.png')
                  this.animatePatternD(i,data.num,data.pad,data.d,data.t,num1,space,size);
              }else{
                  num2 += 1
                  data = this._get_animation_factors_500_Objs(num2)
                  this.tag("Image_"+i).src = Utils.asset('testimages/fish-1331813.png')
                  this.animatePatternE(i,data.num,data.pad,data.d,data.t,num2,space,size);
              }
          }
      }
      this.dispUIMsg(n);
      logMsg("Animation of " + n + " object(s) initiated")
      setTimeout(() => {
          this.tag("RDKServices").setFPSIndex();
      },1000);
  }




  dispUIMsg(n){
    this.tag("MsgBox").text.text = `No.of Objects: ${n}`;
  }

  startDiagnosis(){
     // Method to get diagnostics info for each second
     setInterval(()=> {
         this.tag("RDKServices").getDiagnosticsInfo();
     },1000);
  }

  randomInteger(min, max) {
      return Math.floor(Math.random() * (max - min + 1)) + min;
  }


  clearAnimatedImages(n){
    logMsg("Clearing " + n + " animated objects");
    for (var i = 1; i <= n; i++){
        this.tag("Image_"+i).visible = false;
    }
    this.objectsCount = 0;
    this.dispUIMsg(0);
  }
  getFPS(n){
     var data = this.tag("RDKServices").getAverageLastNFPS(n)
     this.avgFPS = data.avg;
     logMsg("[DiagnosticInfo]: No.of Animated Objects: " + this.objectsCount + ",Average of " + data.len + " FPS values: " + this.avgFPS);
  }

  checkFPS(index){
     var avgfps = Math.round(this.avgFPS)
     var minfps = this.expFPS - this.threshold;
     logMsg("Rounding off FPS " + this.avgFPS + " to " + avgfps)
     if ( avgfps < minfps ){
         for (var j=index; j < this.timeoutParams.length; j++)
             clearTimeout(this.timeoutParams[j])
         this.lowFPSFlag = 1;
         logMsg("Average FPS " + avgfps + " < " + minfps);
         logMsg("FPS is not as expected. Cancelling further more object animations")
     }else{
         logMsg("Average FPS " + avgfps + " >= " + minfps);
     }
  }


  /*Initiating the Test here. Based on the provided duration, multi object animation
   API call is scheduled using timeout. If FPS is not as expected, next scheduled calls
   will be cancelled */

  performGenericTest(){
      var duration,buffer=11,interval;
      duration = parseInt(GetURLParameter("duration"));
      for (let i=0,index=0; i < this.allObjectsCount.length; i++){
         interval = ((duration*i)+(15*i))
         this.timeoutParams[index] = setTimeout(()=> {
             this.animateMultiObjects(this.allObjectsCount[i]);
         },interval*1000);
         this.timeoutParams[index+1] = setTimeout(() => {
             this.getFPS(duration);
         },(interval+duration+buffer)*1000);
         this.timeoutParams[index+2] = setTimeout(()=> {
             this.clearAnimatedImages(this.objectsCount);
             this.checkFPS(index);
             if(this.lowFPSFlag)
                 logMsg("TEST STOPPED !!!");
         },(interval+duration+buffer+2)*1000);
         index += 3;
      }
      this.timeoutParams[this.timeoutParams.length] = setTimeout(()=> {
          logMsg("TEST COMPLETED !!!");
      },(interval+duration+buffer+5)*1000);
  }


  _init()
  {
    // URL arguments
    this.autotest    = GetURLParameter("autotest");
    this.deviceIP    = GetURLParameter("ip");
    this.devicePort  = GetURLParameter("port");
    this.expFPS      = GetURLParameter("fps");
    this.threshold   = GetURLParameter("threshold");
    this.testtype    = GetURLParameter("testtype");

    this.objectsCount    = 0;
    this.avgFPS          = 0;
    this.lowFPSFlag      = 0;
    this.allObjectsCount = [ 1, 10, 20, 50, 100, 250, 500, 1000 ]
    this.timeoutParams   = []


    // Required device IP and Port to communicate with
    // RDK services plugins using ThunderJS
    this.config = {
        host: this.deviceIP,
        port: this.devicePort
    };
    this.settings = {
        consumer:this,
        fpsholder:"MsgBox1",
        cpuholder:"MsgBox2",
        memholder:"MsgBox3"
    };

    this.tag("RDKServices").updateSettings(this.config,this.settings);
    this.tag("RDKServices").rdkservicesInterfaceInit();


    //creating N child image objects
    logMsg("******* Creating Child Image objects *******")
    for (var i = 1; i <= 1000; i++){
        this.tag("Background").childList.a({
                               ref:"Image_" + i,
                               src:Utils.asset('testimages/fish-1331816_960_720.png'),
                               w:100,h:100,
                               x:100,y:700,visible:false
        })
    }
    logMsg("******* Child Image objects created *******")
    this.startDiagnosis();
    if (this.autotest == "true"){
        logMsg("********************** STARTING AUTO TEST ***********************")
        if(this.testtype == "generic"){
            setTimeout(() => {
                this.performGenericTest();
            },3000);
        }
    }
  }

}


