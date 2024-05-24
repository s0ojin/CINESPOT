<template>
  <div class="flex flex-col gap-4 max-w-4xl mx-auto">
    <div v-if="movieLoading">Loading...</div>
    <div v-if="movieError">Error: {{ movieError.message }}</div>
    <div
      v-if="movie"
      class="flex h-72 gap-4 p-4 pr-8 my-4 border rounded-xl hover:bg-slate-50 transition cursor-pointer"
      @click="handleToMovieDetail"
    >
      <img
        :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
        alt="Poster"
        class="rounded-lg border object-cover w-44"
      />

      <div class="flex flex-col p-2">
        <h2 class="text-xl">{{ movie.title }}</h2>
        <div class="flex gap-2 text-sm text-slate-600">
          <span>{{ movie.release_date.split('-')[0] }}</span>
          <span class="leading-3">.</span>
          <span>{{ getCountryNameInKorean(movie.production_countries[0].iso_3166_1) }}</span>
          <span class="leading-3">.</span>
          <span>{{ movie.runtime }}분</span>
        </div>
        <p class="flex-1 mt-4">{{ movie.overview.slice(0, 412) }}...</p>
        <div class="flex gap-2 flex-wrap text-sm mt-auto">
          <span v-for="genre in movie.genre_ids" :key="genre.id" class="border py-1 px-2 rounded-2xl">{{
            genre.name
          }}</span>
        </div>
      </div>
    </div>
    <div v-if="reviewsLoading">Loading...</div>
    <div v-if="reviewsError">Error: {{ reviewsError.message }}</div>
    <div v-if="reviews && reviews.length > 0" class="grid grid-cols-1 gap-3 mt-4">
      <div v-for="review in reviews" :key="review.id">
        <reviewCard :review="review" :contentLimit="200" />
      </div>
    </div>
  </div>
</template>

<script setup>
import ReviewCard from '@/components/reviewCard.vue'
import { getCountryNameInKorean } from '@/utils/convertCountryName'
import { useQuery } from '@tanstack/vue-query'
import { useRoute, useRouter } from 'vue-router'
import { getMovieReviewList } from '@/apis/reviewApi'
import { getMovieDetails } from '@/apis/movieApi'

const router = useRouter()
const route = useRoute()
const movieId = route.params.movieId

const {
  data: reviews,
  error: reviewsError,
  isLoading: reviewsLoading
} = useQuery({
  queryKey: ['movieReviews'],
  queryFn: () => getMovieReviewList(movieId).then((res) => res.data)
})

const {
  data: movie,
  error: movieError,
  isLoading: movieLoading
} = useQuery({
  queryKey: ['movieDetails', movieId],
  queryFn: () => getMovieDetails(movieId).then((res) => res.data)
})

const handleToMovieDetail = () => {
  router.push({ name: 'movieDetail', params: { movieId: movieId } })
}
</script>
