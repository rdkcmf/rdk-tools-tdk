/*
 This file will be invoked by index.html and instead of
 default name App.js imported TDKMediaPlayerApp.js
 This file is part of lightning sdk we just update the
 app js file name here
*/
import { Launch } from '@lightningjs/sdk'
//import App from './App.js'
import App from './TDKMediaPlayerApp.js'

export default function() {
  return Launch(App, ...arguments)
}
