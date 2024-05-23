import axios from 'axios'
import { privateApi } from './authApi'

const movieApi = axios.create({
  baseURL: import.meta.env.VITE_TMDB_BASE_URL,
  params: {
    api_key: import.meta.env.VITE_TMDB_API_KEY
  }
})

export const getMovies = () => {
  return privateApi.get('/api/v1/movies/')
}

export const getMovieDetails = (movieId) => {
  return privateApi.get(`/api/v1/movies/${movieId}`)
}

export const getSimilarMovies = (movieId) => {
  return movieApi.get(`https://api.themoviedb.org/3/movie/${movieId}/similar`, {
    params: {
      language: 'ko-KR'
    }
  })
}

export const postMovieLike = (movieId) => {
  return privateApi.post(`/api/v1/movies/${movieId}/like/`)
}
