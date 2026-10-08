import axios, {
  AxiosError,
  type InternalAxiosRequestConfig
} from 'axios'

import { tokenService } from './tokenService'

const baseURL =
  import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

// Client principale
const api = axios.create({ baseURL })

// Client separato per il refresh:
// non deve attivare gli interceptor del client principale
const refreshApi = axios.create({ baseURL })

interface RetryConfig extends InternalAxiosRequestConfig {
  _retry?: boolean
}

// Evita che più richieste 401 contemporanee
// generino più refresh simultanei
let refreshPromise: Promise<string> | null = null

async function refreshAccessToken(): Promise<string> {
  const refresh = tokenService.getRefresh()

  if (!refresh) {
    throw new Error('Refresh token mancante')
  }

  const response = await refreshApi.post(
    '/api/token/refresh/',
    { refresh }
  )

  const access: string = response.data.access

  tokenService.setAccess(access)

  return access
}

// viene eseguito prima di ogni richiesta Axios e inserisce l'access token
//nell'header Authorization
api.interceptors.request.use((config) => {
  const token = tokenService.getAccess()

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

// intercetta le risponste. Se django rest 401, prova a ottenere un nuovp token
api.interceptors.response.use(
  response => response,

  async (error: AxiosError) => {
    const originalRequest =
      error.config as RetryConfig | undefined

    if (
      error.response?.status !== 401 ||
      !originalRequest ||
      originalRequest._retry
    ) {
      return Promise.reject(error)
    }

    originalRequest._retry = true
    //così impedisco che la stessa richiesta venga ritrasmessa più volte

    try {
      if (!refreshPromise) {// per condividee la stessa operazione tra componenti
        //altirmenti stanno tutti a rinviare la stessa richiesta se token scade
        refreshPromise = refreshAccessToken()
          .finally(() => {
            refreshPromise = null
          })
      }

      const newAccess = await refreshPromise

      originalRequest.headers.Authorization =
        `Bearer ${newAccess}`

      return api(originalRequest)

    } catch (refreshError) {
      tokenService.clear()

      window.dispatchEvent(
        new Event('auth:expired')
      )

      return Promise.reject(refreshError)
    }
  }
)

export default api