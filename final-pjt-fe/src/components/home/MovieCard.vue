<template>
  <div class="flex flex-col gap-2" @click="goToDetail">
    <div
      class="relative h-[360px] rounded-lg border overflow-hidden cursor-pointer hover:scale-105 transition duration-300"
    >
      <div class="absolute top-2 left-2 text-xl w-7 text-center rounded-md text-white bg-slate-800/70">
        {{ props.idx }}
      </div>

      <i
        v-if="movie.is_liked === false || movie.is_liked === true"
        @click.prevent.stop="toggleLike(movie.id)"
        :class="[
          'absolute bottom-3 right-3 pi pi-bookmark-fill text-2xl text-gray-100 hover:text-primary-500',
          (movie.is_liked || isLiked) && 'text-primary-500'
        ]"
      ></i>

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
        <p v-if="koreanCountryName" class="leading-3">.</p>
        <p>{{ koreanCountryName }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { getCountryNameInKorean } from '@/utils/convertCountryName'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { computed, defineProps } from 'vue'
import { useRouter } from 'vue-router'
import { postMovieLike } from '@/apis/movieApi'

const queryClient = useQueryClient()

const props = defineProps({
  movie: {
    type: Object,
    required: true
  },
  idx: {
    type: Number,
    required: true
  },
  isLikeBaseRecommend: {
    type: Boolean,
    required: false,
    default: false
  }
})

const isLiked = ref(false)

const koreanCountryName = computed(() => {
  if (props.movie.production_countries && props.movie.production_countries.length > 0) {
    return getCountryNameInKorean(props.movie.production_countries[0].iso_3166_1)
  }
  return ''
})

const router = useRouter()
const goToDetail = () => {
  router.push({ name: 'movieDetail', params: { movieId: props.movie.id } })
}

const movieLikeMutation = useMutation({
  mutationFn: (movieId) => postMovieLike(movieId),
  onSuccess: async (data) => {
    if (props.isLikeBaseRecommend === true) {
      isLiked.value = data.data.liked
    } else {
      await queryClient.invalidateQueries(
        {
          queryKey: ['movies'],
          exact: false,
          refetchType: 'active'
        },
        { throwOnError: false, cancelRefetch: true }
      )
    }
  },
  onError: (err) => {
    if (err.response.status === 403) {
      alert('자신의 리뷰에 좋아요를 누를 수 없어요!😜')
    }
    if (err.response.status === 401) {
      alert('로그인 후 좋아요 기능을 이용할 수 있어요!🧐')
    }
  }
})

const toggleLike = (movieId) => {
  movieLikeMutation.mutate(movieId)
}
</script>
