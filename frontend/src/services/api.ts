import axios from 'axios'


// Creiamo un'istanza dedicata di Axios
const api = axios.create({
  baseURL: 'http://localhost:8000',
})

// INTERCEPTOR: Scatta AUTOMATICAMENTE prima di ogni singola chiamata HTTP!
//così prima di ogni chiamata http va a recueprare il token (dallo store) e lo aggiunge nell'header
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    // Aggiunge l'header "Authorization: Bearer <token>"
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api