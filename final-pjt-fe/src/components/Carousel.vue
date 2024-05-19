<template>
  <div class="relative">
    <button
      @click="prev"
      class="absolute w-10 h-10 flex justify-center items-center -left-3 top-[calc(50%-40px)] transform -translate-y-1/2 bg-white rounded-full z-10 border"
    >
      <i class="pi pi-angle-left text-2xl text-slate-500"></i>
    </button>
    <button
      @click="next"
      class="absolute w-10 h-10 flex justify-center items-center -right-3 top-[calc(50%-40px)] transform -translate-y-1/2 bg-white rounded-full z-10 border"
    >
      <i class="pi pi-angle-right text-2xl text-slate-500"></i>
    </button>

    <div class="overflow-hidden">
      <div
        class="flex transition-transform duration-300 ease-in-out"
        :style="{ transform: `translateX(-${currentIndex * 100}%)` }"
      >
        <div v-for="(movie, index) in movies" :key="movie.id" class="flex-shrink-0 p-2 w-1/5">
          <MovieCard :movie="movie" :idx="index + 1" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MovieCard from '@/components/home/MovieCard.vue'

const props = defineProps({
  movies: {
    type: Array,
    required: true
  }
})

const currentIndex = ref(0)
const itemsPerPage = 5

const prev = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

const next = () => {
  if ((currentIndex.value + 1) * itemsPerPage < props.movies.length) {
    currentIndex.value++
  }
}
</script>
