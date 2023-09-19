import { ApiError, DefaultService, OpenAPI } from '@/client'
import router from '@/router'
import { useTokenStore } from '@/stores/TokenStore'
import { useUserStore } from '@/stores/UserStore'
import { Notify } from 'quasar'

const userStore = useUserStore()
const tokenStore = useTokenStore()

class AuthService {
  
  async update_user_info() {
    // Получение пользователя
    const userResponse = await DefaultService.readCurrentUserUsersMeGet()
    // Запись пользователя
    userStore.saveUser(userResponse.user)
  }

  async login(username: string, password: string) {
    // Получение токена
    const tokenResponse = await DefaultService.loginForAccessTokenTokenPost({
      username: username,
      password: password
    }).catch(error => {
      if (error instanceof ApiError) {
        Notify.create(error.message)
      }
      else {
        Notify.create(error)
      }
      throw error
    })
    // TODO Переместить в обработчик ошибок

    // Сохранение токена в tokenStorage
    tokenStore.saveToken(tokenResponse.access_token)
    // Сохранение токена в клиенте
    OpenAPI.TOKEN = tokenResponse.access_token

    await this.update_user_info()

    router.push({path: '/'})
  }

  logout() {
    userStore.removeUser()
    tokenStore.removeToken()
    OpenAPI.TOKEN = undefined
  }

}

export default new AuthService()
