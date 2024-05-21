<template>
  <!-- <GoogleMap /> -->
  <div>
    <div v-if="isLoading">Loading...</div>
    <div v-if="error">Error: {{ error.message }}</div>

    <h2 class="p-2 font-semibold text-xl">로맨스를 좋아하는 경령님을 위한 추천영화</h2>
    <div v-if="!isLoading && !error">
      <Carousel :movies="movies" />
    </div>
  </div>
  <div>
    <div v-if="isLoading">Loading...</div>
    <div v-if="error">Error: {{ error.message }}</div>

    <h2 class="p-2 font-semibold text-xl">오늘 날씨와 어울리는 추천영화</h2>
    <div v-if="!isLoading && !error">
      <Carousel :movies="movies" />
    </div>
  </div>
  <div>
    <div v-if="isLoading">Loading...</div>
    <div v-if="error">Error: {{ error.message }}</div>

    <h2 class="p-2 font-semibold text-xl">현재 인기있는 영화</h2>
    <div v-if="!isLoading && !error">
      <Carousel :movies="movies" />
    </div>
  </div>
</template>

<script setup>
import Carousel from '@/components/Carousel.vue'
import { useQuery } from '@tanstack/vue-query'
import { getMovies } from '@/apis/movieApi'

const {
  data: movies,
  error,
  isLoading
} = useQuery({
  queryKey: ['movies'],
  queryFn: () => getMovies().then((res) => res.data)
})
</script>
