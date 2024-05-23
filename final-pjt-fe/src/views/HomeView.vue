<template>
  <div v-if="isLoading">Loading...</div>
  <div v-if="error">Error: {{ error.message }}</div>

  <div>
    <h2 v-if="!authLoading && authData" class="p-2 font-semibold text-xl">
      {{ authData.userInfo?.username }}님을 위한 추천영화
    </h2>
    <h2 v-else-if="!authData" class="p-2 font-semibold text-xl">로그인하고 영화 추천 받아보세요!</h2>
    <div v-if="!recommendLoading && !recommendError && recommendMovies">
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
      <div v-if="!popularLoading && !popularError && popularMovies">
        <MovieCarousel :movies="popularMovies" />
      </div>
    </div>
  </div>
</template>

<script setup>
import MovieCarousel from '@/components/MovieCarousel.vue'
import { useQuery } from '@tanstack/vue-query'
import { getMovies, getRecommendMovies, getPopularMovies } from '@/apis/movieApi'
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
  isLoading: recommendLoading
} = useQuery({
  queryKey: ['recommend'],
  queryFn: () => getRecommendMovies().then((res) => res.data.movie_recommendations)
})

const {
  data: popularMovies,
  error: popularError,
  isLoading: popularLoading
} = useQuery({
  queryKey: ['movies', 'popular'],
  queryFn: () => getPopularMovies().then((res) => res.data.movie_recommendations)
})
</script>
