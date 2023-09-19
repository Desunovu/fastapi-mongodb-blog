import { ApiError, DefaultService, OpenAPI } from '@/client'
import router from '@/router'
import { useTokenStore } from '@/stores/TokenStore'
import { useUserStore } from '@/stores/UserStore'
import { Notify } from 'quasar'

class AuthService {
  async update_user_info() {
    const userStore = useUserStore()

    // Получение пользователя
    const userResponse = await DefaultService.readCurrentUserUsersMeGet()
    // Запись пользователя
    userStore.saveUser(userResponse.user)
  }

  async login(username: string, password: string) {
    const tokenStore = useTokenStore()

    // Получение токена
    const tokenResponse = await DefaultService.loginForAccessTokenTokenPost({
      username: username,
      password: password
    })

    // Сохранение токена в tokenStorage
    tokenStore.saveToken(tokenResponse.access_token)
    // Сохранение токена в клиенте
    OpenAPI.TOKEN = tokenResponse.access_token

    await this.update_user_info()

    router.push({ path: '/' })
  }

  logout() {
    const userStore = useUserStore()
    const tokenStore = useTokenStore()

    userStore.removeUser()
    tokenStore.removeToken()
    OpenAPI.TOKEN = undefined
  }
}

export default new AuthService()
