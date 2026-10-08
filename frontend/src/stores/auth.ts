import { defineStore } from 'pinia'
import axios from 'axios'

import { tokenService } from '@/services/tokenService'

const baseURL =
  import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: tokenService.getAccess(),
    refreshToken: tokenService.getRefresh()
  }),

  getters: {
    hasSession: state => !!state.refreshToken
  },

  actions: {
    async login(credentials: {
      username: string
      password: string
    }) {
      // Client senza interceptor di autenticazione
      const response = await axios.post(
        `${baseURL}/api/token/`,
        credentials
      )

      const { access, refresh } = response.data

      tokenService.setTokens(access, refresh)

      this.accessToken = access
      this.refreshToken = refresh
    },

    logout() {
      tokenService.clear()

      this.accessToken = null
      this.refreshToken = null
    }
  }
})