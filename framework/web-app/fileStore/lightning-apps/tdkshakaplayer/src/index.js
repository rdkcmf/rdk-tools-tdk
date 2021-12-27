import { Launch } from '@lightningjs/sdk'
import App from './TDKSHAKAPlayerApp.js'

export default function() {
  return Launch(App, ...arguments)
}
