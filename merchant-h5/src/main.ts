import 'element-plus/dist/index.css'
import './styles/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'

import App from './App.vue'
import router from './router'
import { registerNativeBackButton } from './utils/nativeBackButton'

registerNativeBackButton(router)

createApp(App).use(createPinia()).use(router).use(ElementPlus).mount('#app')
