import axios from 'axios'
import { publicApi } from './authApi'

const movieApi = axios.create({
  baseURL: import.meta.env.VITE_TMDB_BASE_URL,
  params: {
    api_key: import.meta.env.VITE_TMDB_API_KEY
  }
})

export const getMovies = () => {
  return publicApi.get('/api/v1/movies/')
}

export const getMovieDetails = (movieId) => {
  return publicApi.get(`/api/v1/movies/${movieId}`, {
    params: {
      language: 'ko-KR'
    }
  })
}

export const getSimilarMovies = (movieId) => {
  return movieApi.get(`https://api.themoviedb.org/3/movie/${movieId}/similar`, {
    params: {
      language: 'ko-KR'
    }
  })
}
