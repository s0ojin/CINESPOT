<template>
  <div class="flex flex-col gap-2" @click="goToDetail">
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
        <p>{{ koreanCountryName }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { getCountryNameInKorean } from '@/utils/convertCountyName'
import { computed, defineProps } from 'vue'
import { useRouter } from 'vue-router'

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

const koreanCountryName = computed(() => {
  if (props.movie.production_countries && props.movie.production_countries.length > 0) {
    return getCountryNameInKorean(props.movie.production_countries[0].iso_3166_1)
  }
  return '국가 정보 없음'
})

const router = useRouter()
const goToDetail = () => {
  router.push({ name: 'movieDetail', params: { movieId: props.movie.id } })
}
</script>
