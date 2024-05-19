<template>
  <div class="flex flex-col gap-2">
    <div
      class="relative h-[360px] rounded-lg border overflow-hidden cursor-pointer hover:scale-105 transition duration-300"
    >
      <div class="absolute top-2 left-2 text-xl w-7 text-center rounded-md text-white bg-slate-800/70">
        {{ props.idx }}
      </div>
      <img
        :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
        alt="Poster"
        class="h-[360px] w-full object-cover"
      />
    </div>
    <div>
      <h3>{{ movie.title }}</h3>
      <div class="flex gap-2 text-sm text-slate-700">
        <p>{{ movie.release_date.split('-')[0] }}</p>
        <p class="leading-3">.</p>
        <p>미국</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  movie: {
    type: Object,
    required: true
  },
  idx: {
    type: Number,
    required: true
  }
})
</script>
