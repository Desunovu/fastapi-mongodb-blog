import type { UserDocument } from '@/client'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  persist: true,
  state: () => {
    return {
      user: undefined as UserDocument | undefined
    }
  },
  actions: {
    saveUser(user: UserDocument) {
        this.user = user
    },
    removeUser() {
        this.user = undefined
    }
  }
})
