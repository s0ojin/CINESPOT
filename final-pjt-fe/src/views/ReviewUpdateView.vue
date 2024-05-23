<template>
  <div v-if="isLoading">Loading review...</div>
  <div v-if="error">Error loading review: {{ error.message }}</div>
  <div v-if="!isLoading && !error && review">
    <div
      class="flex h-32 gap-4 p-4 pr-8 my-4 border rounded-xl hover:bg-slate-50 transition cursor-pointer"
      @click="handleToMovieDetail"
    >
      <img
        :src="`https://image.tmdb.org/t/p/w500${review.movieInfo.poster_path}`"
        alt="Poster"
        class="rounded-lg border object-cover"
      />
      <div class="flex w-full justify-between items-center">
        <div>
          <h2>
            {{ review.movieInfo.title }}
          </h2>
          <div class="flex gap-2 text-sm text-slate-600">
            <span>{{ review.movieInfo.release_date.split('-')[0] }}</span>
            <span class="leading-3">.</span>
            <span>{{ getCountryNameInKorean(review.movieInfo.production_countries[0].iso_3166_1) }}</span>
            <span class="leading-3">.</span>
            <span>{{ review.movieInfo.runtime }}분</span>
          </div>
          <div class="flex gap-2 flex-wrap mt-2 text-sm">
            <span v-for="(genre, idx) in review.movieInfo.genres" :key="idx" class="border py-1 px-2 rounded-2xl">{{
              genre
            }}</span>
          </div>
        </div>
      </div>
    </div>
    <div class="border p-6 rounded-lg">
      <h1 class="text-xl mb-1">리뷰 수정하기</h1>
      <StarRating v-model="rating" />
      <textarea
        v-model="content"
        class="input resize-none h-28 pt-2 mt-2"
        placeholder="영화에 대한 감상평이나 기대평을 남겨주세요!"
      ></textarea>
      <button @click="handleSubmit" class="submit-btn w-full h-10 rounded-lg">리뷰 남기기</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { putReview, getReviewDetail } from '@/apis/reviewApi'
import StarRating from '@/components/StarRating.vue'
import { getCountryNameInKorean } from '@/utils/convertCountryName'

const route = useRoute()
const router = useRouter()
const reviewId = route.params.reviewId
const queryClient = useQueryClient()

const {
  data: review,
  error,
  isLoading
} = useQuery({
  queryKey: ['reviewDetail', reviewId],
  queryFn: async () => {
    const response = await getReviewDetail(reviewId)
    const data = response.data
    rating.value = data.rating
    content.value = data.content
    return data
  },
  staleTime: 0
})

const rating = ref(0)
const content = ref('')

const mutation = useMutation({
  mutationFn: (reviewData) => putReview(reviewId, reviewData),
  onSuccess: (data) => {
    queryClient.invalidateQueries(['reviewDetail', reviewId])
    alert('리뷰수정이 완료되었습니다')
    router.push({ name: 'reviewDetail', params: { reviewId: data.data.id } })
  },
  onError: (error) => {
    alert('리뷰 생성 실패:', error)
  }
})

const handleSubmit = () => {
  const reviewData = {
    content: content.value,
    rating: rating.value
  }
  mutation.mutate(reviewData)
}

const handleToMovieDetail = () => {
  router.push({ name: 'movieDetail', params: { movieId: review.value.movieInfo.id } })
}
</script>
