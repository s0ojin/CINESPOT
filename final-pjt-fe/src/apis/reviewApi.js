import { privateApi, publicApi } from './authApi'

export const postCreateReview = (movieId, reviewData) => {
  return privateApi.post(`/api/v1/movies/${movieId}/review/`, reviewData)
}

export const getMovieReviewList = (movieId) => {
  return publicApi.get(`/api/v1/movies/${movieId}/review_list/`)
}
