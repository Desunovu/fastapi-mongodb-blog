import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Quasar, Notify } from 'quasar'
import App from './App.vue'
import router from './router'
import { ApiError, OpenAPI } from './client'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { useTokenStore } from './stores/TokenStore'
// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css'
// Import Quasar css
import 'quasar/src/css/index.sass'
import AuthService from './services/AuthService'

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

// Global error handler
app.config.errorHandler = (error, instance, info) => {
  // Handle the error globally
  console.error('Global error:', error)
  console.log('Vue instance:', instance)
  console.log('Error info:', info)

  if (error instanceof ApiError) {
    Notify.create(error.message)
    if (error.status == 401) {
      AuthService.logout()
      router.push("/login")
    }
    if (error.status == 404) {
      router.push("/page-not-found")
    }
    // if (error.status == 422) {
    //   router.push("/validation-error")
    // }
  } else {
    Notify.create('Произошла ошибка')
  }
}

app.mount('#app')
