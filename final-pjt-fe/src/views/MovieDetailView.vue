<template>
  <div>
    <div v-if="isLoading" class="text-center">Loading...</div>
    <div v-if="error" class="text-center text-red-500">Error: {{ error.message }}</div>
    <div v-if="detailInfo">
      <header class="relative h-[500px]">
        <img
          :src="`https://image.tmdb.org/t/p/original${detailInfo.backdrop_path}`"
          alt="Poster"
          class="w-full h-full object-cover"
        />
        <div class="absolute inset-0 bg-black bg-opacity-50"></div>
        <div class="max-w-screen-xl mx-auto">
          <div class="absolute bottom-10 text-white">
            <h1 class="text-3xl font-bold mb-4">{{ detailInfo.title }}</h1>
            <p class="mb-2">{{ detailInfo.release_date }}</p>
            <div class="flex gap-2 flex-wrap">
              <span v-for="genre in detailInfo.genres" :key="genre.id">{{ genre.name }}</span>
            </div>
          </div>
        </div>
      </header>
      <div class="flex flex-col gap-20 my-20 max-w-screen-xl mx-auto">
        <section class="flex gap-20">
          <img
            :src="`https://image.tmdb.org/t/p/w500${detailInfo.poster_path}`"
            alt="Poster"
            class="h-96 object-cover border rounded-md"
          />
          <div>
            <p class="mb-4">
              <strong class="block">줄거리</strong>
              <span v-if="detailInfo.overview">
                {{ detailInfo.overview }}
              </span>
              <span v-else> 줄거리가 없지만 줄거리 없이 보는 맛이 있어요😏</span>
            </p>
          </div>
        </section>
        <section>
          <div class="flex justify-between items-end px-2">
            <h2 class="text-2xl font-bold">
              리뷰 <span class="font-normal text-primary-500 ml-1">{{ detailInfo.review_set.length }}개</span>
            </h2>
            <button class="text-slate-700">더보기</button>
          </div>

          <div v-if="detailInfo.review_set.length > 0" class="grid grid-cols-1 md:grid-cols-3 gap-3 mt-4">
            <div v-for="review in detailInfo.review_set" :key="review.id">
              <reviewCard :review="review" />
            </div>
          </div>
          <div v-else class="text-center py-10">
            아직 리뷰가 없습니다...😔<br />
            < {{ detailInfo.title }} >의 첫 번째 리뷰어가 되어주세요!
          </div>
        </section>
        <section>
          <h2 class="text-2xl font-bold p-2">스틸컷</h2>
          <div class="flex gap-2 overflow-hidden">
            <div v-if="detailInfo.still_cut_paths.length > 0">
              <div v-for="(image, index) in detailInfo.still_cut_paths" :key="index">
                <img :src="`https://image.tmdb.org/t/p/w500/${image}`" alt="still_cut" />
              </div>
            </div>
            <div v-else class="mx-auto py-10">영화 이미지가 존재하지 않습니다😫</div>
          </div>
        </section>
        <section>
          <h2 class="text-2xl font-bold p-2">
            <span>< {{ detailInfo.title }} ></span>과 비슷한 영화들 추천드려요!
          </h2>
          <div v-if="!similarLoading">
            <div v-if="similarMovies.length > 0">
              <Carousel :movies="similarMovies" />
            </div>
            <div v-else class="text-center py-10">
              비슷한 영화가 없네요...😔 <br />매우 특별한 영화라고 할 수 있습니다ㅎ
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useQuery } from '@tanstack/vue-query'
import { getMovieDetails, getSimilarMovies } from '@/apis/movieApi'
import reviewCard from '@/components/reviewCard.vue'
import Carousel from '@/components/Carousel.vue'

const route = useRoute()
const movieId = route.params.movieId

const {
  data: detailInfo,
  error,
  isLoading
} = useQuery({
  queryKey: ['movieDetails', movieId],
  queryFn: () => getMovieDetails(movieId).then((res) => res.data)
})

const { data: similarMovies, isLoading: similarLoading } = useQuery({
  queryKey: ['similarMovies', movieId],
  queryFn: () => getSimilarMovies(movieId).then((res) => res.data.results)
})
</script>
