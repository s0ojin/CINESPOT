<template>
  <div v-if="isLoading">Loading...</div>
  <div v-if="error">Error: {{ error.message }}</div>

  <div>
    <h2 v-if="!authLoading && authData" class="p-2 font-semibold text-xl">
      {{ authData.userInfo?.username }}님을 위한 추천영화
    </h2>
    <h2 v-else-if="!authData" class="p-2 font-semibold text-xl">로그인하고 영화 추천 받아보세요!</h2>
    <div v-if="!rocommendLoading && !recommendError && recommendMovies">
      <MovieCarousel :movies="recommendMovies" :is-like-base-recommend="true" />
    </div>
  </div>
  <div>
    <div v-if="isLoading">Loading...</div>
    <div v-if="error">Error: {{ error.message }}</div>

    <h2 class="p-2 font-semibold text-xl">오늘 날씨와 어울리는 추천영화</h2>
    <div v-if="!isLoading && !error">
      <MovieCarousel :movies="movies" />
    </div>
  </div>
  <div>
    <div v-if="isLoading">Loading...</div>
    <div v-if="error">Error: {{ error.message }}</div>

    <h2 class="p-2 font-semibold text-xl">현재 인기있는 영화</h2>
    <div v-if="!isLoading && !error">
      <MovieCarousel :movies="movies" />
    </div>
  </div>
</template>

<script setup>
import MovieCarousel from '@/components/MovieCarousel.vue'
import { useQuery } from '@tanstack/vue-query'
import { getMovies, getRecommendMovies } from '@/apis/movieApi'
import { useAuthQuery } from '@/composables/useAuthQuery'

const { data: authData, isLoading: authLoading } = useAuthQuery()

const {
  data: movies,
  error,
  isLoading
} = useQuery({
  queryKey: ['movies'],
  queryFn: () => getMovies().then((res) => res.data)
})

const {
  data: recommendMovies,
  error: recommendError,
  isLoading: rocommendLoading
} = useQuery({
  queryKey: ['recommend'],
  queryFn: () => getRecommendMovies().then((res) => res.data.movie_recommendations)
})
</script>
