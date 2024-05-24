import { publicApi } from './authApi'

export const getRecommendedTravelDestination = (movieInfo) => {
  return publicApi.get('api/v1/recommendations/recommend/', {
    params: movieInfo
  })
}
