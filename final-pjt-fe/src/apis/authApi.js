import axios from 'axios'

export const publicApi = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL
})

export const privateApi = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL
})

privateApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export const postSignUp = ({ username, password1, password2 }) => {
  return publicApi.post('/accounts/signup/', { username, password1, password2 })
}

export const postSignIn = ({ username, password }) => {
  return publicApi.post('/accounts/login/', { username, password })
}
