const ACCESS_KEY = 'access_token'
const REFRESH_KEY = 'refresh_token'
//solo tokenService sa dove vengono memorizzati i token
//DOMANDA: ma i token che conservo in local storage?
//sono accessibili da js
export const tokenService = {
  getAccess(): string | null {
    return localStorage.getItem(ACCESS_KEY)
  },

  getRefresh(): string | null {
    return localStorage.getItem(REFRESH_KEY)
  },

  setTokens(access: string, refresh: string): void {
    localStorage.setItem(ACCESS_KEY, access)
    localStorage.setItem(REFRESH_KEY, refresh)
  },

  setAccess(access: string): void {
    localStorage.setItem(ACCESS_KEY, access)
  },

  clear(): void {
    localStorage.removeItem(ACCESS_KEY)
    localStorage.removeItem(REFRESH_KEY)
  }
}