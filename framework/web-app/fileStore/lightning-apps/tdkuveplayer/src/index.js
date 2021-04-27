import { Launch } from '@lightningjs/sdk'
import App from './TDKUVEPlayerApp.js'

export default function() {
  return Launch(App, ...arguments)
}
