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
import { GetURLParameter, logMsg } from './IPChangeAppUtility.js'
import ThunderJS from 'ThunderJS'

export default class App extends Lightning.Component {
  static getFonts() {
    return [{ family: 'Regular', url: Utils.asset('fonts/Roboto-Regular.ttf') }]
  }

  static _template() {
    return {
      Background: {
        w: 1920,
        h: 1080,
        color: 0xfffbb03b,
        src: Utils.asset('images/background.png'),
      },
      Logo: {
        mountX: 0.5,
        mountY: 1,
        x: 960,
	y: 200,
        src: Utils.asset('images/TDK_logo.png'),
      },
      Text: {
        mount: 0.5,
        x: 960,
	y: 320,
        text: {
          text: "Lightning App for detecting IP change",
          fontFace: 'Regular',
          fontSize: 64,
          textColor: 0xbbffffff,
        },
      },
      MsgBox1: {
	mount: 0.5,
        x: 960,
        y: 500,
        w: 1080,
        text: {
	  text: "No events occurred",
          fontStyle: 'bold',
          fontSize: 25,
          textColor: 0xbbffffff,
        }
      },
      MsgBox2: {
        mount: 0.5,
        x: 960,
        y: 620,
        w: 1080,
        text: {
          fontStyle: 'bold',
          fontSize: 25,
          textColor: 0xbbffffff,
        }
      },

    }
  }
 //Display messages to UI
  dispUIMessage(msgBox,msg){
      this.tag(msgBox).text.text = `${msg}`;
  }
  _init() {
    this.tag('Background')
      .animation({
        duration: 15,
        repeat: -1,
        actions: [
          {
            t: '',
            p: 'color',
            v: { 0: { v: 0xfffbb03b }, 0.5: { v: 0xfff46730 }, 0.8: { v: 0xfffbb03b } },
          },
        ],
      })
      .start()
    
    const config = {
      host: '127.0.0.1',
      port: 9998,
      default: 1,
    };
    const tmURL = GetURLParameter('tmURL')
    let url = tmURL +'/execution/changeDeviceIP?'
    logMsg("URL: " +url)
    const deviceNameInTM = GetURLParameter('deviceName')
    const userName = GetURLParameter('tmUserName')
    const password = GetURLParameter('tmPassword')
    let ipAddressType = GetURLParameter('ipAddressType')
    if (ipAddressType === 'ipv4'){
        ipAddressType = 'ip4Address'
    }
    else{
	ipAddressType = 'ip6Address'
    }
    var thunder = ThunderJS(config);
    logMsg('ThunderJS Initialized')
    //Activating Network plugin and waiting for event
    thunder.call('Controller','activate',{callsign:'org.rdk.Network'}).then(result =>{
      logMsg('Network plugin Activated , Result:' + result)
      thunder.on('org.rdk.Network', 'onIPAddressStatusChanged', (notification) => {
          if (notification.hasOwnProperty(ipAddressType) && notification.status.includes('ACQUIRED')){
            let DeviceIP = notification[ipAddressType]
	    if (!DeviceIP.startsWith('169.')){
            	logMsg('IP Changed to :'+ DeviceIP);
	    	this.dispUIMessage('MsgBox1','IP Changed to :'+ DeviceIP)
            	//Updating new IP to Test manager
            	fetch(url + new URLSearchParams({deviceName: deviceNameInTM,
                          newDeviceIP: DeviceIP,
                          tmUserName: userName,
                          tmPassword: password
                        }))
            	.then(response => response.json())
            	.then((data) => {
	      	     logMsg('Response from Test Manager: '+ JSON.stringify(data))
	      	     this.dispUIMessage('MsgBox2','Response from Test Manager: '+JSON.stringify(data))
            	})
            	.catch(error =>{ 
              	console.error('Error while connecting to Test Manager: '+ error);
              	this.dispUIMessage('MsgBox2','Error while connecting to Test Manager: '+ error);
	    	})
	    } 
	  }
          else{
	    logMsg("Other event message: "+JSON.stringify(notification))
          }
      },(error) =>{
         console.error('[Error]:',error)		
       });
    });
  }
}
