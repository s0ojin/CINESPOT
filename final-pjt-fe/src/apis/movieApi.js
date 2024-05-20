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

export const getSimilarMovies = (movieId) => {
  return movieApi.get(`https://api.themoviedb.org/3/movie/${movieId}/similar`, {
    params: {
      language: 'ko-KR'
    }
  })
}
