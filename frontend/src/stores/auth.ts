import { defineStore } from 'pinia'
//import axios from 'axios'
import api from '@/services/api'
interface AuthState {
  //sono i token che mi vengono restituiti dal front
  accessToken: string | null
  refreshToken: string | null
  user: any | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    // mem nel local storage i token così se l'utente ricarica la pagina non deve rifare il login
    accessToken: localStorage.getItem('access_token'),
    refreshToken: localStorage.getItem('refresh_token'),
    user: null,
  }),

  getters: { //si ricalcola autom ogni volta che cambia lo stato
    //il !! converte ogni valore in booleano
    isAuthenticated: (state) => !!state.accessToken,
  },

  actions: {
    async login(credentials: { username: string; password: string }) {
      const response = await api.post('/api/token/', credentials)
      
      const { access, refresh } = response.data
      console.log(response.data)
      this.accessToken = access
      this.refreshToken = refresh

      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)

      api.defaults.headers.common['Authorization'] = `Bearer ${access}`
    },

    logout() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      delete api.defaults.headers.common['Authorization']
    }
  }
})