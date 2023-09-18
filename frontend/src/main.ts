import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Quasar, Notify } from 'quasar'
import App from './App.vue'
import router from './router'
import { OpenAPI } from './client'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { useTokenStore } from './stores/TokenStore'
// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css'
// Import Quasar css
import 'quasar/src/css/index.sass'

const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(router)
app.use(pinia)
app.use(Quasar, {
  plugins: {
    Notify
  }
})

const tokenStore = useTokenStore()
OpenAPI.BASE = 'http://localhost:8000'
OpenAPI.TOKEN = tokenStore.token
console.log(tokenStore.token)

app.mount('#app')
