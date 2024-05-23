import { privateApi, publicApi } from './authApi'

export const postCreateReview = (movieId, reviewData) => {
  return privateApi.post(`/api/v1/movies/${movieId}/review/`, reviewData)
}

export const getReviewDetail = (reviewId) => {
  return publicApi.get(`/api/v1/reviews/${reviewId}/review_detail/`)
}

export const putReview = (reviewId, reviewData) => {
  return privateApi.put(`api/v1/reviews/${reviewId}/review_detail/`, reviewData)
}

export const deleteReview = (reveiwId) => {
  return privateApi.delete(`api/v1/reviews/${reveiwId}/review_detail/`)
}

export const getMovieReviewList = (movieId) => {
  return publicApi.get(`/api/v1/movies/${movieId}/review_list/`)
}

export const postCreateComment = (reviewId, commentData) => {
  return privateApi.post(`/api/v1/reviews/${reviewId}/comments/`, commentData)
}

export const deleteComment = (commentId) => {
  return privateApi.delete(`/api/v1/comments/${commentId}/`)
}

export const postReviewLike = (reviewId) => {
  return privateApi.post(`/api/v1/reviews/${reviewId}/like/`)
}
