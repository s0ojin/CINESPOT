import axios from 'axios'

const movieApi = axios.create({
  baseURL: import.meta.env.VITE_TMDB_BASE_URL,
  params: {
    api_key: import.meta.env.VITE_TMDB_API_KEY
  }
})

export const getPopularMovies = () => {
  return movieApi.get('/movie/popular', {
    params: {
      language: 'ko-KR',
      page: 1
    }
  })
}

export const getMovieDetails = (movieId) => {
  return movieApi.get(`/movie/${movieId}`, {
    params: {
      language: 'ko-KR'
    }
  })
}
