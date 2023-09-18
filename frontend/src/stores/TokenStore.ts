import { defineStore } from 'pinia'

export const useTokenStore = defineStore('token', {
  persist: true,
  state: () => {
    return {
      token: undefined as string | undefined
    }
  },
  actions: {
    saveToken(token: string) {
      this.token = token
    },
    removeToken() {
      this.token = undefined
    }
  }
})
