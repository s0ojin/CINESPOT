<template>
  <div>
    <div v-if="isLoading">Loading...</div>
    <div v-if="error">Error: {{ error.message }}</div>

    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4" v-if="!isLoading && !error">
      <div
        v-for="movie in popularMovies"
        :key="movie.id"
        class="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer"
      >
        <img
          :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
          alt="Poster"
          class="w-full h-88 object-cover"
        />
        <div class="">
          <h3 class="text-lg font-semibold">{{ movie.title }}</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { getPopularMovies } from '@/apis/movieApi'

const { data, error, isLoading } = useQuery({ queryKey: ['popularMovies'], queryFn: getPopularMovies })
const popularMovies = ref([])

watch(data, (newValue) => {
  if (newValue) {
    popularMovies.value = newValue.data.results
  }
})
</script>
