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
            <div>
              <span class="mb-2 mr-2">{{ detailInfo.release_date }}</span>
              <span>{{ getCountryNameInKorean(detailInfo.production_countries[0].iso_3166_1) }}</span>
            </div>
            <span>{{ detailInfo.runtime }} 분</span>
            <div class="flex gap-2 flex-wrap">
              <span v-for="(genre, idx) in detailInfo.genres" :key="idx">{{ genre }}</span>
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
          <div class="flex-1">
            <p class="mb-6">
              <strong class="block">줄거리</strong>
              <span v-if="detailInfo.overview">
                {{ detailInfo.overview }}
              </span>
              <span v-else> 줄거리가 없지만 줄거리 없이 보는 맛이 있어요😏</span>
            </p>
            <CreateReview />
          </div>
        </section>
        <section>
          <div class="flex justify-between items-end px-2">
            <h2 class="text-2xl font-bold">
              리뷰 <span class="font-normal text-primary-500 ml-1">{{ detailInfo.review_set.length }}개</span>
            </h2>
            <button v-if="detailInfo.review_set.length > 0" @click="goToReviewList" class="text-slate-700">
              더보기
            </button>
          </div>

          <div v-if="detailInfo.review_set.length > 0" class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
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
          <h2 class="text-2xl font-bold p-2">갤러리</h2>
          <div class="flex">
            <div class="overflow-x-auto whitespace-nowrap py-2 px-4">
              <img
                v-for="(image, idx) in detailInfo.still_cut_paths"
                :key="idx"
                :src="`https://image.tmdb.org/t/p/w500/${image}`"
                class="inline-block mr-4 h-48"
                alt="Image"
              />
            </div>
          </div>
        </section>
        <section>
          <h2 class="text-2xl font-bold p-2">
            <span>< {{ detailInfo.title }} ></span>과 비슷한 영화들 추천드려요!
          </h2>
          <div v-if="!similarLoading && !similarError && similarMovies.length > 0">
            <MovieCarousel :movies="similarMovies" />
          </div>
          <div v-else class="text-center py-10">
            비슷한 영화가 없네요...😔 <br />매우 특별한 영화라고 할 수 있습니다ㅎ
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useQuery } from '@tanstack/vue-query'
import { getMovieDetails, getSimilarMovies } from '@/apis/movieApi'
import { getCountryNameInKorean } from '@/utils/convertCountryName'
import reviewCard from '@/components/reviewCard.vue'
import MovieCarousel from '@/components/MovieCarousel.vue'
import CreateReview from '@/components/CreateReview.vue'

const route = useRoute()
const router = useRouter()
const movieId = route.params.movieId

const {
  data: detailInfo,
  error,
  isLoading
} = useQuery({
  queryKey: ['movieDetails', movieId],
  queryFn: () => getMovieDetails(movieId).then((res) => res.data)
})

const {
  data: similarMovies,
  error: similarError,
  isLoading: similarLoading
} = useQuery({
  queryKey: ['similarMovies'],
  queryFn: () => getSimilarMovies(movieId).then((res) => res.data.results)
})

const goToReviewList = () => {
  router.push({
    name: 'movieReviewList',
    params: { movieId: detailInfo.id }
  })
}
</script>
